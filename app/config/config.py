import os
from dotenv import load_dotenv

load_dotenv()

# Variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALGORITHM = os.getenv("ALGORITHM")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")

if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER", "postgres") 
    DB_PASS = os.getenv("DB_PASS")  
    DB_NAME = os.getenv("DB_NAME")  
    INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME") 

    DATABASE_URL = f"postgresql+pg8000://{DB_USER}:{DB_PASS}@/{DB_NAME}?unix_sock=/cloudsql/{INSTANCE_CONNECTION_NAME}/.s.PGSQL.5432"


print(f"DATABASE_URL: {DATABASE_URL}")
