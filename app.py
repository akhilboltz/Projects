import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import json

CHROMA_DIR = './chroma_db'
OLLAMA_MODEL = 'Llama3.1:Latest'

st.set_page_config(page_title='Machining Advisor',page_icon='⚙️',layout='wide')

with st.sidebar:
    st.title('Settings')
    k_val = st.slider("Choose the number of documents to retrieve : ",min_value=1,max_value=10,step=1)
    temp_val = st.slider("Choose the temperature settings :" , min_value=0.00,max_value=1.00,step=0.05 )
    st.info('***Tip***: Please decrease the temperature if we want to get factual information.😃')
    model_choice = st.selectbox("choose the model",options=["llama3.1:latest","gemma3:4b","mistral:latest"])
    st.info('***Tip***: Please increase the number of documents if there is not much information to support the conditions.😃')

@st.cache_resource
def load_db():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    try:
        db = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function= embeddings
        )
        return db
    except:
        st.error(f'❌..........Failed to load the database..............❌')
        return None

vector_db = load_db()

def format_docs(docs):
    nl = '\n'
    if docs:
        clean_docs = []
        for idx,doc in enumerate(docs):
            content = doc.page_content
            if isinstance(content, dict):
                content = json.dumps(content, indent=2)
              
            context_meta_string = f"source: {doc.metadata.get('source')} |" + f"page_num: {doc.metadata.get('page_num')} |" 
            context_meta_string += f"table_idx: {doc.metadata.get('table_idx')} |"
            context_meta_string += f"Content : {content}"
            clean_docs.append(context_meta_string)
        return "\n\n".join(clean_docs)
    else:
        return ""

if vector_db:
    st.title('Welcome to Machining Advisor')
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    input_query = st.chat_input('write your query')
    if input_query:
        st.session_state.messages.append({"role":"user","content":input_query})
        with st.chat_message("user"):
            st.markdown(input_query)
            
        with st.chat_message("assistant"):
            with st.spinner("✅Response generating.........."):
                try:
                    retriever = vector_db.as_retriever(
                            search_type = 'mmr',
                            search_kwargs = {'k':k_val,'fetch_k':25}
                    )
                    retrieved_doc = retriever.invoke(input_query)
                    with st.expander("🔍 Engineering Debug: What did the database retrieve?"):
                         if not retrieved_doc:
                             st.error("⚠️ No documents retrieved! Try increasing 'k' or changing your query.")
                         else:
                             for i, doc in enumerate(retrieved_doc):
                                 st.caption(f"Chunk #{i+1} | Source: Page {doc.metadata.get('page_num')}")
                                 # This shows the RAW text the LLM is reading
                                 st.code(doc.page_content, language="text") 
                                 st.divider()
                    retrieved_data = format_docs(retrieved_doc)

                    llm = ChatOllama(model=model_choice , temperature=temp_val)

                    prompt = ChatPromptTemplate.from_template(
                        """You are an expert Production Engineering Assistant. 
                        
                        ### CONTEXT DATA (Retrieved from Catalogs)
                        {context}

                        ### USER QUESTION
                        {question}

                        ### CRITICAL INSTRUCTION: MATERIAL MAPPING
                        The user may use common names, but the catalog uses ISO codes or Grades. You MUST map them:
                        * **"Steel"** = Look for **"ISO P"**, "Carbon Steel", or grades like "42CrMo4", "C45".
                        * **"Stainless"** = Look for **"ISO M"**, "Inox", "304", "316".
                        * **"Cast Iron"** = Look for **"ISO K"**, "GG25", "GGG40".
                        * **"Aluminum"** = Look for **"ISO N"**, "Alu", "Non-ferrous".
                        * **"Super Alloys/Titanium"** = Look for **"ISO S"**.
                        * **"Hardened Steel"** = Look for **"ISO H"**.

                        ### EXTRACTION RULES
                        1. **Identify the Operation**: (e.g., Milling, Drilling) from the context.
                        2. **Find Parameters**:
                           - Speed: Keys like 'vc', 'v_c', 'Speed', 'Cutting Speed'.
                           - Feed: Keys like 'fz', 'f_z', 'Feed', 'mm/tooth'.
                        3. **Check Conditions**: If user asks for "Wet" or "Dry", prioritize rows that mention those terms or cooling emulsions.

                        ### FINAL DECISION RULE
                        - If you find RELEVANT data matching the mapped material (e.g., found "ISO P" when user asked for "Steel"), output the table.
                        - ONLY say "Data not found" if the context is empty or completely unrelated (e.g., user asks for Steel but context is only about Aluminum).

                        ### OUTPUT FORMAT
                        * **Material Found**: [e.g., ISO P / Low Alloy Steel]
                        * **Operation**: [Operation Name]
                        * **Speed ($v_c$)**: [Value] m/min
                        * **Feed ($f_z$)**: [Value] mm/z
                        * **Source**: Page [Page Num]
                        """  
                    )
                    chain = prompt | llm | StrOutputParser()
                    response = chain.invoke({'context':retrieved_data,"question": input_query})

                    st.markdown(response)
                    st.session_state.messages.append({'role':'assistant','content':response})

                except Exception as e:
                    st.error(f"🚨 An error occurred: {str(e)}")








                    