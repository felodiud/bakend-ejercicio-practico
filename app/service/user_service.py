from app.schemas import CreatrUser
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.database import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.models import UserDB



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def register(user: CreatrUser, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Cifrar la contraseña antes de guardarla
    hashed_password = pwd_context.hash(user.password)
    
    # Crear nuevo usuario
    new_user = UserDB(username=user.username, hashed_password=hashed_password,
                      full_name = user.full_name, email = user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario creado exitosamente"}