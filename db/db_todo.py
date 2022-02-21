from fastapi import HTTPException, status
from routers.schemas import TodoBase, Update_TodoBase, Upadate_Work, Update_TodoDisplay
from sqlalchemy.orm.session import Session
from db.models import DbTodo
from sqlalchemy.orm import Query
# from sqlalchemy.orm.query import 
# from sqlalchemy.exc import ArgumentError
from sqlalchemy import update




def create_todo(db: Session, request: TodoBase, creator_id: int):
  new_todo = DbTodo(
    task = request.task,
    assigned_to = request.assigned_to,
    due_date = request.due_date,
    is_completed = request.is_completed,
    user_id = creator_id,
    grp_txt = request.grp_txt,
    grp_id = request.grp_id
  )
  db.add(new_todo)
  db.commit()
  db.refresh(new_todo)
  return new_todo

def get_all_todos(db: Session):
  return db.query(DbTodo).all()

def update_todo(id: int, db: Session, request:Update_TodoBase):# current_user: int, request: Update_TodoBase):

  u_id = db.query(DbTodo).filter(DbTodo.id == id).first()
  if not u_id:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with id {id} not found')

  db.query(DbTodo).filter(DbTodo.id == id).update({
    "task" : f"{request.task}",
    "assigned_to" : f"{request.assigned_to}",
    "due_date" : f"{request.due_date}",
    "is_completed" : f"{request.is_completed}",
    "grp_txt" : f"{request.grp_txt}",
    "grp_id" : f"{request.grp_id}"
  })
  db.commit()
  return u_id



def delete(db: Session, id: int,user_id: int):
  todo = db.query(DbTodo).filter(DbTodo.id == id).first()
  if not todo:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with id {id} not found')
  if todo.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
          detail='Only todo creator can delete task')

  db.delete(todo)
  db.commit()
  return '---Task is deleted---'


def delete_grp(db: Session, grp_id: int,user_id: int):
  g_todo=[]
  g_todo = db.query(DbTodo).filter(DbTodo.grp_id == grp_id).all()   #to fetch all the task which having same grp_id
  if not g_todo:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with group id {grp_id} not found')
  for x in g_todo:
    if x.user_id != user_id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail='Only todo group creator can delete task')
  while(g_todo):
    db.delete(g_todo[0])
    g_todo.pop(0)
    db.commit()
  return '---Group is deleted---'