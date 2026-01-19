from langchain_ollama import OllamaLLM , ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

model_name = 'Llama3.1'
model = ChatOllama(model= model_name)

parser = StrOutputParser()


user_request = "I am milling Tool Steel (Grade D2) using a 12mm End Mill. I want to run at Vc = 250 m/min."
retrieved_context = """
    MATERIAL DATA: Tool Steel (D2, H13)
    HARDNESS: 200-250 HB
    RECOMMENDED CUTTING SPEED (Vc):
    - Roughing: 120 - 150 m/min
    - Finishing: 150 - 180 m/min
    SAFETY LIMIT: Do not exceed 190 m/min without specialized cooling.
    """

prompt = ChatPromptTemplate.from_messages([
    ("system" , 
        """You are a CNC Safety Advisor. 
         Compare the USER REQUEST against the TECHNICIAN GUIDELINES.
         
         Output a JSON object with:
         - "status": "SAFE" or "WARNING" or "DANGER"
         - "parameter_checked": The name of the parameter (e.g., "Surface Speed")
         - "user_value": The value the user wants
         - "limit_value": The maximum allowed value from text
         - "advice": A short technical recommendation."""
    ), 
    ("user" , "GUIDELINES:\n{context}\n\nUSER REQUEST:\n{query}" )
    ])

try:
    chain = prompt | model | parser
    result = chain.invoke({'context': retrieved_context, 'query': user_request})
    print(result)
    print("Test Case Successful")
except:
    print("Error !!!. Please check the chain")