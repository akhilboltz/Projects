from langchain_community.document_loaders import JSONLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
import json
from pathlib import Path

class Vector_Database:
    def __init__(self,json_path:str):
        self.json_path = Path(json_path)
        if self.json_path.exists():
            print(f'Path {self.json_path} is found successfully ')
        else:
            raise FileNotFoundError

    def format_content(self,page_content:dict)->str:
        try:
            content = []
            text = page_content.pop('tip_text','')
            for key,values in page_content.items():
                if values !='' and values !=None:
                    content.append(f" {key}:{values}")
            if text:
                content.append(f"***Note***: {text}")
            return (" | ").join(content)
        except:
            raise KeyError

    def metadata_function(self,record:dict,metadata:dict)->dict:
        metadata['page_num'] = record.get('metadata',{}).get('page_num')
        metadata['source'] = record.get('metadata',{}).get('source')
        metadata['table_idx'] = record.get('metadata',{}).get('table_idx')
        return metadata
    
    def format_document(self,raw_files):
            format_doc = []
            for doc in raw_files:
                if isinstance(doc.page_content,str):
                    page_content = json.loads(doc.page_content)
                else:
                    page_content = doc.page_content
                clean_content = self.format_content(page_content)

                new_doc = Document(
                    page_content= clean_content,
                    metadata = doc.metadata
                    )
                format_doc.append(new_doc)
            return self.add_doc_to_chromadb(format_doc)

    def load_data(self):
        data_direct = str(self.json_path)
        loader = JSONLoader(
            file_path= data_direct,
            jq_schema='.',
            content_key= 'page_content',
            metadata_func= self.metadata_function,
            text_content= False,
            json_lines=True
        )
        raw_files = loader.load()
        return self.format_document(raw_files)
    
    def add_doc_to_chromadb(self,format_doc):
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2"
            )

            database = Chroma.from_documents(
                documents= format_doc,
                embedding= embeddings,
                persist_directory="./chroma_db"
            )
            print(f"Added the data to the database succesfully .......................................")
            return database
        except:
            return None

if __name__ == "__main__":
    vector_db = Vector_Database('test_inventory.json')
    db = vector_db.load_data()

    