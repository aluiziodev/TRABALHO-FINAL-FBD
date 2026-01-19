import os  
import pymssql 
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

#------------- CONEXAO SQL SERVER -------------

def getConnection():
    return pymssql.connect(
        server=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=1433,
    )

