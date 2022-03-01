from asyncio import tasks
from typing import List
from fastapi import HTTPException, status
from routers.schemas import TodoBase, TodoGrpBase , Update_TodoBase, Upadate_Work
from sqlalchemy.orm.session import Session
from db.models import DbTodo , Dbgrp
from sqlalchemy.orm import Query
from sqlalchemy import update
from datetime import date




def create_todo_grp(db: Session, request: TodoGrpBase, creator_id: int):
  new_grp = Dbgrp(
    g_name = request.g_name,
  )
  x = db.query(Dbgrp).filter(Dbgrp.g_name == new_grp.g_name).first()
  if x:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail= f'Group with Name:- {new_grp.g_name} already exist')
  db.add(new_grp)
  db.commit()
  db.refresh(new_grp)
  return new_grp


def create_todo(db: Session, request: TodoBase, creator_id: int):
  new_todo = DbTodo(
    task = request.task,
    assigned_to = request.assigned_to,
    due_date = request.due_date,
    is_completed = request.is_completed,
    user_id = creator_id,
    grp_name = request.grp_name,
    # grp_id = request.grp_id
  )
  check_g_name = db.query(Dbgrp).filter(Dbgrp.g_name == new_todo.grp_name).first()
  if not check_g_name:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail= f'Group Name with Name:- {new_todo.grp_name} not found')
  db.add(new_todo)
  db.commit()
  db.refresh(new_todo)
  return new_todo

def get_all_todos(db: Session):
  # x = db.query(DbTodo).join(Dbgrp).all()
  x = db.query(DbTodo).all()
  return db.query(DbTodo).all()


def update_group(group_name:int, request: TodoGrpBase,db: Session):
  u_name = db.query(Dbgrp).filter(Dbgrp.g_name == group_name).first()
  if not u_name:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'Group with Name:- {group_name} not found')
  db.query(Dbgrp).filter(Dbgrp.g_name == group_name).update({
    "g_name" : f"{request.g_name}"
  })
  db.query(DbTodo).filter(DbTodo.grp_name == group_name).update({
    "grp_name" : f"{request.g_name}"
  })
  
  db.commit()
  return u_name


def update_todo(id: int, db: Session, request:Update_TodoBase):#, current_user: int):
  u_id = db.query(DbTodo).filter(DbTodo.id == id).first()
  if not u_id:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with id {id} ,not found')
  # if u_id.user_id != current_user:
  #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
  #         detail='Only todo creator can update task')

  # x = db.query(Dbgrp).filter(Dbgrp.g_name == request.grp_name).first()
  # if not x:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
  #         detail=f'Group that you enter does not exist')

  db.query(DbTodo).filter(DbTodo.id == id).update({
    "task" : f"{request.task}",
    "assigned_to" : f"{request.assigned_to}",
    "due_date" : f"{request.due_date}",
    "is_completed" : f"{request.is_completed}"
    # "grp_name" : f"{request.grp_name}"
  })
  
  db.commit()
  return u_id

def update_workdone(id: int, db: Session, request:Upadate_Work):
  u_work = db.query(DbTodo).filter(DbTodo.id == id).first()
  if not u_work:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with id {id} ,not found')

  db.query(DbTodo).filter(DbTodo.id == id).update({
    "is_completed" : f"{request.is_completed}"
  })
  db.commit()
  return u_work


def delete_task(db: Session, id: int):#,user_id: int):
  todo = db.query(DbTodo).filter(DbTodo.id == id).first()
  if not todo:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with id {id} ,not found')
  # if todo.user_id != user_id:
  #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
  #         detail='Only todo creator can delete task')

  db.delete(todo)
  db.commit()
  return '---Task is deleted---'



def delete_grp(db: Session, grp_name: str):#,current_user.id)
  grp = db.query(Dbgrp).filter(Dbgrp.g_name == grp_name).first()
  if not grp:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'Group with Name:- {grp_name} ,not found')
  # if todo.user_id != user_id:
  #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
  #         detail='Only todo creator can delete task')

  db.delete(grp)
  db.commit()
  g_gtodo=[]
  g_gtodo = db.query(DbTodo).filter(DbTodo.grp_name == grp_name).all()
  for x in g_gtodo:
    db.delete(x)
    db.commit()
  return '---Group is deleted---'


 

def get_all_passed_due_date(db: Session):
  today = date.today()
  p_todo=[]
  p_todo = db.query(DbTodo).filter(DbTodo.due_date < today).filter( DbTodo.is_completed == 0).all()
  return p_todo


def mark_all_group_work_completed(group_name:str,db:Session):
  g = []
  g = db.query(DbTodo).filter(DbTodo.grp_name == group_name).all()
  for x in g:
    db.query(DbTodo).filter(DbTodo.id == x.id).update({
      "is_completed" : f"{True}"
    })
    db.commit()
  return g



def groupwise_task(g_name:str, db: Session):
  t = []
  g_todo = []
  l_todo = []
  g_todo = db.query(Dbgrp).filter(Dbgrp.g_name == g_name).first()
  l_todo = db.query(DbTodo).filter(DbTodo.grp_name == g_name).all()
  a=[]
  for x in range(len(l_todo)):
    t = {
      "id": f"{l_todo[x].id}",
      "task": f"{l_todo[x].task}",
      "assigned_to": f"{l_todo[x].assigned_to}",
      "due_date": f"{l_todo[x].due_date}",
      "is_completed": f"{l_todo[x].is_completed}"
    }
    a.append(t)

  r = {
    "grp_name": f"{g_name}",
    "grp_id": f"{g_todo.g_id}",
    "tasks": a
  }
  return r
  


