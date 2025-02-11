from fastapi import FastAPI
from app.routes import router
from app.database.db_conection import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.models import UserDB

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

Base.metadata.create_all(bind=engine)

app.include_router(router)