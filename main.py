from fastapi import FastAPI,HTTPException,status
from typing import List,Optional
from db import models
from sqlalchemy.sql.functions import user
from db.database import engine
from auth import authentication
from routers import user,todo
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

app.include_router(user.router)
app.include_router(todo.router)
app.include_router(authentication.router)



@app.get("/")
def root():
    return "hello world!!"


models.Base.metadata.create_all(engine)

    