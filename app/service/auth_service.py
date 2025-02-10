from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from app.models import UserDB
from sqlalchemy.orm import Session
from app.config import SECRET_KEY, ALGORITHM, SPREADSHEET_ID, SHEET_NAME
import json
import gspread
from google.oauth2.service_account import Credentials


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire, "sub": data.get("sub")})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None 
    



creds = Credentials.from_service_account_file("/app/service/credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)

def update_google_sheet(row_index, cell_index, new_value):
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    
    row = row_index + 2
    col = cell_index + 1

    sheet.update_cell(row, col, new_value)
    return {"message": "✅ Celda actualizada"}