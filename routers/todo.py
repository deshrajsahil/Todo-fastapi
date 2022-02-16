from auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from routers.schemas import TodoBase, TodoDisplay
from db.database import get_db
from db import db_todo
from typing import List
from routers.schemas import UserAuth


router = APIRouter(
  prefix='/post',
  tags=['post']
)



@router.post('', response_model=TodoDisplay)
def create(request: TodoBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  if not request.task:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="Task cannot be Empty")
  return db_todo.create(db, request)


@router.get('/all', response_model=List[TodoDisplay])
def todos(db: Session = Depends(get_db)):
  return db_todo.get_all_todos(db)



@router.get('/delete/{id}')
def delete_todo(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  return db_todo.delete(db, id, current_user.id)