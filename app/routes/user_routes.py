from fastapi import APIRouter, Depends
from app.schemas import CreatrUser
from sqlalchemy.orm import Session 
from app.database import get_db
from app.service import register


router = APIRouter()



@router.post("/register")
def register_user(user: CreatrUser, db: Session = Depends(get_db)):
    return register(user, db)