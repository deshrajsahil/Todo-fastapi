from typing import List
from fastapi import HTTPException, status
from routers.schemas import TodoBase, Update_TodoBase, Upadate_Work, Update_TodoDisplay
from sqlalchemy.orm.session import Session
from db.models import DbTodo
from sqlalchemy.orm import Query
from sqlalchemy import update
from datetime import date
from routers.schemas import Task_Inside_Display


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
  x = db.query(DbTodo).all()
  print("x : ", x)

  return x

def update_todo(id: int, db: Session, request:Update_TodoBase, current_user: int):
  u_id = db.query(DbTodo).filter(DbTodo.id == id).first()
  if not u_id:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with id {id} not found')
  if u_id.user_id != current_user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
          detail='Only todo creator can update task')


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

def update_workdone(id: int, db: Session, request:Upadate_Work):
  u_work = db.query(DbTodo).filter(DbTodo.id == id).first()
  if not u_work:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with id {id} not found')

  db.query(DbTodo).filter(DbTodo.id == id).update({
    "is_completed" : f"{request.is_completed}"
  })
  db.commit()
  return u_work


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
  flag=0
  for x in g_todo:
    if x.user_id != user_id:
      flag=1
    else:
      db.delete(x)
      db.commit()

  if flag==1:
    return 'Some tasks were not deleted bcoz it has been created by others'
  else:
    return '---Group is deleted---'   

def get_all_passed_due_date(db: Session):
  today = date.today()
  p_todo=[]
  p_todo = db.query(DbTodo).filter(DbTodo.due_date < today ).all()
  return p_todo

def groupwise_task(g_id:int, db: Session):
  g_w_todo = []
  g_w_todo = db.query(DbTodo).filter(DbTodo.grp_id == g_id ).all()
  # # g_w_todo.to_json
  # y = Task_Inside_Display(g_w_todo)
  # print("g_w_todo : ", g_w_todo)
  # r = {
  #   "grp_id": f"{g_id}",
  #   # "grp_txt": f"{DbTodo.grp_txt}",
  #   # "tasks": y
  #   "tasks": f"{g_w_todo}"
  # }
  # print("R: ", r)
  r = g_w_todo
  return r
