from auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from routers.schemas import TodoBase, TodoDisplay, Update_TodoBase,Upadate_Work, Update_TodoDisplay
from db.database import get_db
from db import db_todo
from typing import List
from routers.schemas import UserAuth


router = APIRouter(
  prefix='/post',
  tags=['post']
)



@router.post('', response_model=TodoDisplay)
def create_todo(request: TodoBase, db: Session = Depends(get_db), creator_id: UserAuth = Depends(get_current_user)):
  if not request.task:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="Task cannot be Empty")
  return db_todo.create_todo(db, request, creator_id.id)


@router.get('/all', response_model=List[TodoDisplay])
def todos(db: Session = Depends(get_db)):
  return db_todo.get_all_todos(db)

@router.put('/update/{id}',response_model=Update_TodoDisplay)
def update_todo(id: int,request: Update_TodoBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  if not id:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="ID cannot be Empty")
  if not request.task:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="Task cannot be Empty")
  return db_todo.update_todo(id, db, request,current_user.id)


@router.put('/update_workdone/{id}', response_model=Update_TodoDisplay)
def update_workdone_todo(id: int, request:Upadate_Work , db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  return db_todo.update_workdone(id,db,request)


# @router.put('/mark_all_complete/{id}', response_model=Update_TodoDisplay)
# def mark_all_grp_complete(id: int, db: Session = Depends(get_db)):#, current_user: UserAuth = Depends(get_current_user)):
#   return db_todo.mark_grp_complete(id,db)



@router.get('/delete/{id}')
def delete_todo(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  return db_todo.delete(db, id,current_user.id)


@router.get('/delete_grp/{grp_id}')
def delete_todo_grp(grp_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
  return db_todo.delete_grp(db, grp_id,current_user.id)

