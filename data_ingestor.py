#The necessary library are pdfplumber , pathlib , pandas and json
#Importing these library for the code throughout this file

import pdfplumber
from pathlib import Path
import pandas as pd
import json

#Creating a Class Instance and storing all the functions within it so that the below code has scalability and reusability

class Ingestor:
    def __init__(self,pdf_path:str):
        
        #Using Path function so as to treat file system paths as objects rather than strings
        # Raising Error if the file is not found using the try-except clause
                
        self.pdf_path = Path(pdf_path)
        self.pdf_path_set = set()     
        try:
            if self.pdf_path.exists():
                print(f"File found Successfully at {pdf_path}")
            else:
                raise FileNotFoundError
        except:
            raise Exception("Unknown error has occured")            

    #Error : The words were read backwards because of words written from bottom to top
    #Solution : Reversed the text using simple replace method under string
    
    def fix_reversed_text(self,text):
        if not isinstance(text, str): return text
        replacements = {
            "gnilliM": "Milling", "gnillirD": "Drilling",
            "edibrac": "carbide", "diloS": "Solid"
        }
        for old, new in replacements.items():
            if old in text: return text.replace(old, new)
        return text

    #Error : Headers were'nt in a single line because improper understanding of pandas while shifting each table to pandas dataframe
    #Solution : Flattened the headers and cleaned them of any words read backwards and changed newline to " "

    def flatten_headers(self,df):
        if df.empty: return df
        headers = [self.fix_reversed_text(str(c).replace('\n', ' ')) for c in df.columns]
        seen = {}
        new_headers = []
        for idx,h in enumerate(headers):
            if h in seen:
                seen[h]+=1
                new_headers.append(f'{h}_{seen[h]}')
            else:
                seen[h] = 0
                new_headers.append(h)
        df.columns = new_headers
        return df

    #Error : Due to presence of nested headers most secondary headers did not receive the primary header precedence
    #Solution : When there is a None change in primary header change it to the previous header name

    def fill_missing_headers(self,df):
        col = df.columns.to_list()
        for col_idx in range(1,len(col)):
            if col[col_idx] == 'None' : col[col_idx] = col[col_idx-1]
        df.columns=col
        return df

    #Error : Most of the Secondary headers where included in the first row of dataframe
    #Solution : As the first row is serial.no it is empty , Hence if it was empty then there is a nested header try to add the header to previous headers and forward fill to the next header

    def merge_header_rows(self,df,depth=0):
        if df.empty or len(df.columns) < 2: 
            return df
        if df.iloc[0,1] == '' or df.iloc[0,1]==None:
            col = df.columns.to_list()
            if depth+1 > len(df):
                return df
            for row_no in range(0,depth+1):
                if row_no >= len(df):
                    break
                else:
                    for col_idx in range(len(col)):
                        val = df.iloc[row_no,col_idx]
                        if pd.isna(val) or str(val).strip() in ['', 'None']:
                            val = '' 
                        else:
                            val = str(val).strip()
                        if val : col[col_idx] = str(col[col_idx]) +'_'+ val
            df.columns=col
            if len(df) > depth + 1:
                df = df.iloc[depth + 1:, :]
            else:
                df = df.iloc[0:0]   
        
        return df
    
    #Error: There is a presence of nested header within the nested header 
    #Solution : Had joined both the nested header into a data seperated by ":" so as to reduce columns and have proper column name to data

    def headers_depth(self,df,depth = 1):
        if df.empty or len(df) < depth: return df
        for row_idx in range(depth,0,-1):
            for col_idx in range(len(df.columns)-1,0,-1): 
                if pd.isna(df.iloc[row_idx-1,col_idx]) and pd.notna(df.iloc[row_idx-1,col_idx-1]):
                    df.iloc[row_idx-1,col_idx] = ' '
                    df.iloc[:,col_idx-1] = df.iloc[:,col_idx-1].fillna('').astype(str)+':' +df.iloc[:,col_idx].fillna('').astype(str)         
                    cols_to_keep = list(range(len(df.columns)))
                    cols_to_keep.pop(col_idx)
                    df = df.iloc[:, cols_to_keep]            
                else:
                    continue
        return df

    #Solution : Trying to save the data into json format so as to constrict the retrival of data to the material rather than a table and make retrieval much easier

    def save_to_json(self,df,tip_text:str,page_num:int,input_file:str,table_idx:int,output_file:str ='test_inventory.json'):
        if df.empty: return 
        records = df.to_dict(orient = 'records')
        with open(output_file,'a',encoding='utf-8') as f:
            for row_data in records:
                row_data['tip_text'] = tip_text
                entry = {
                    'page_content' : row_data,
                    'metadata' : {
                        'source' : str(input_file),
                        'page_num'  : page_num,
                        'table_idx' : table_idx
                    }
                }
                f.write(json.dumps(entry , ensure_ascii=False) + '\n')
        return None

    #Error : There are some important tips present under the table required for the table which can state some exceptional cases 
    #Solution : tried to scan the data below the table using coordinates (bbox) so that we can safely extract the necessary text

    def extract_tips_below_table(self, page, table_bbox, search_height=50):
        x0, top, x1, bottom = table_bbox
        page_height = page.height
        tip_bbox = (x0,bottom,x1,min(bottom + search_height, page_height))
        
        try:
            tip_area = page.crop(bbox=tip_bbox)
            tip_text = tip_area.extract_text()
            
            if tip_text:
                
                return tip_text.replace('\n', ' ').strip()
        except ValueError:
            pass
        return None

    #Error : some serial numbers and Material type are not filled and cause data distortion
    #Solution : Implemented forward fill so that the data if filled with the proper serial data

    def forward_fill_iso_column(self, df):
        if 'ISO' in df.columns:
            df['ISO'] = df['ISO'].ffill()
        if 'Material' in df.columns:    
            df['Material'] = df['Material'].ffill()
        return df

    # Main function where all the above functions are called with the input parameters as the start page, end page,output file directory

    def extract_tables(self,start_page:int = 0,end_page:int = None,output_file ='test_inventory.json'):
        
        #If the path is already mentioned then start fresh and perform the functions otherwise add the perform data ingestion for the new file
        if len(self.pdf_path_set) == 0:
            out_path = Path(output_file)
            if out_path.exists():
                try:
                    out_path.unlink()
                    print(f"Deleted old {output_file} to start fresh.")
                except Exception as e:
                    print(f"Could not delete {output_file}: {e}")
        if self.pdf_path in self.pdf_path_set: return 
        else: self.pdf_path_set.add(self.pdf_path)

        #Use pdfplumber to read through each page of the file and extract the tables and perform all the above functions by calling them
        with pdfplumber.open(self.pdf_path) as pdf:
            if end_page is None: end_page = len(pdf.pages)
            end_page =  min(end_page,len(pdf.pages))

            for page_num in range(start_page,end_page):

                page = pdf.pages[page_num]
                tables  = page.find_tables()

                for table_idx,table in enumerate(tables):
                    data = table.extract()
                    tip_text = ' '
                    if data:
                        df = pd.DataFrame(data[1:],columns=data[0])
                        df = df.map(self.fix_reversed_text)
                        df = self.flatten_headers(df)
                        df = self.headers_depth(df)
                        df = self.fill_missing_headers(df)
                        df= self.merge_header_rows(df)
                        df = self.forward_fill_iso_column(df)
                        tip_text = self.extract_tips_below_table(page, table.bbox)

                        self.save_to_json(df,tip_text,page_num = page_num,input_file = self.pdf_path,table_idx=table_idx+1,output_file =output_file)

#To prevent code from executing automatically when a script is imported as a module into another file          
if __name__ == '__main__':
    ingestor = Ingestor(r".\Hanbuch_Schnittwerte.pdf") 
    ingestor_2 = Ingestor(r".\Ingersoll Milling Catalog.pdf")                    
    ingestor.extract_tables()                   
    ingestor_2.extract_tables()
             


