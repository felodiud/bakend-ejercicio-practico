from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import UserDB
from app.service.auth_service import authenticate_user, create_access_token, verify_access_token, update_google_sheet
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}


@router.post("/verify_token")
def verify_token(token: str):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": "Token is valid", "payload": payload}

@router.post("/update-sheet")
async def update_sheet(data: dict):
    return update_google_sheet(data["rowIndex"], data["cellIndex"], data["newValue"])
