from fastapi import FastAPI,HTTPException,status
from typing import List,Optional
from db import models
from sqlalchemy.sql.functions import user
from db.database import engine
from auth import authentication
from routers import user,todo




app = FastAPI()

app.include_router(user.router)
app.include_router(todo.router)
app.include_router(authentication.router)



@app.get("/")
def root():
    return "hello world!!"

# CRED operations

#store_todo = []  #to store todo list

# @app.post('/todo/', tags=['create Todo'])
# def create_todo(todo: Todo):
#     store_todo.append(todo)
#     return todo

# @app.get('/todo/',response_model=List[Todo], tags=['Show all Todo'])
# def get_all_todos():
#     return store_todo

# @app.get('/todo/{id}', tags=['Show specific Todo'])
# def get_todo(id: int):
#     try:
#         return store_todo[id]
#     except:
#         raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="ToDo doesn't exist")

# @app.put('/todo/{id}', tags=['Update Todo'])
# def update_todo(id: int, todo: Todo):
#     try:
#         store_todo[id] = todo
#         return store_todo[id]
#     except:
#         raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found")


# @app.delete('/todo/{id}', tags=['Delete Todo'])
# def delete_todo(id:int):
#     try:
#         obj = store_todo[id]
#         store_todo.pop(id)
#         return obj
#     except:
#         raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found")


models.Base.metadata.create_all(engine)

    