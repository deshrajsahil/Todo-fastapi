from auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from routers.schemas import TodoBase, TodoDisplay, TodoGrpBase, TodoGrpDisplay , Update_TodoBase , Update_TodoDisplay, Upadate_Work, Groupwise_Task, Task_Inside_Display
from db.database import get_db
from db import db_todo
from typing import List
from routers.schemas import UserAuth
from apscheduler.schedulers.background import BackgroundScheduler
import time
import os



router = APIRouter(
  prefix='/todo',
  tags=['todo']
)


@router.post('', response_model=TodoGrpDisplay)
def create_todo_grp(request: TodoGrpBase, db: Session = Depends(get_db), creator_id: UserAuth = Depends(get_current_user)):
  print(request.g_name)
  if not request.g_name:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="Group text cannot be Empty")
  return db_todo.create_todo_grp(db, request, creator_id.id)


@router.post('/task', response_model=TodoDisplay)
def create_todo(request: TodoBase, db: Session = Depends(get_db), creator_id: UserAuth = Depends(get_current_user)):
  if not request.task:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="Task cannot be Empty")
  return db_todo.create_todo(db, request, creator_id.id)


@router.get('/all', response_model=List[TodoDisplay])
def todos(db: Session = Depends(get_db)):
  return db_todo.get_all_todos(db)


@router.put('/group/{group_name}', response_model=TodoGrpDisplay)
def update_group(group_name: str ,request: TodoGrpBase, db: Session = Depends(get_db)):
  return db_todo.update_group(group_name,request,db)


@router.put('/update_todo/{id}',response_model=Update_TodoDisplay)
def update_todo(id: int,request: Update_TodoBase, db: Session = Depends(get_db)):#, current_user: UserAuth = Depends(get_current_user)):
  if not id:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="ID cannot be Empty")
  if not request.task:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
              detail="Task cannot be Empty")
  return db_todo.update_todo(id, db, request)#,current_user.id)


@router.put('/update_workdone/{id}', response_model=Update_TodoDisplay)
def update_workdone_todo(id: int, request:Upadate_Work , db: Session = Depends(get_db)):#, current_user: UserAuth = Depends(get_current_user)):
  return db_todo.update_workdone(id,db,request)


@router.get('/delete_task/{id}')
def delete_todo(id: int, db: Session = Depends(get_db)):#, current_user: UserAuth = Depends(get_current_user)):
  return db_todo.delete_task(db, id)#,current_user.id)


@router.get('/delete_grp/{grp_name}')
def delete_todo_grp(grp_name: str, db: Session = Depends(get_db)):#, current_user: UserAuth = Depends(get_current_user)):
  return db_todo.delete_grp(db, grp_name)#,current_user.id)


@router.get('/passed_due_date', response_model=List[TodoDisplay])
def display_passsed_due_date(db: Session = Depends(get_db)):
  return db_todo.get_all_passed_due_date(db)


@router.put('/completed_group/{grp_name}', response_model=List[TodoDisplay])
def mark_all_group_work_completed(group_name:str, db: Session = Depends(get_db)):
  return db_todo.mark_all_group_work_completed(group_name,db)


@router.get('/groupwise_task/{id}')
def display_task_groupwiwise(grp_name:str, db: Session=Depends(get_db)):
  # print("id: ", id)
  x = db_todo.groupwise_task(grp_name, db)
  # print("x", x)
  return x

@router.get('/notify_due_date_passed')
def nofify_due_date_passed(db: Session = Depends(get_db)):
  return db_todo.nofify_due_date_passed(db)


# @router.get('/today_due_date')
def today_due_date(db: Session ):#= Depends(get_db)):
  # t = await db_todo.today_due_date(db)
  print('inside today due date in todo')
  db_todo.today_due_date(db)#db)
  # return db_todo.today_due_date(db)


def due_today():
  print('inside due today in todo')
  db: Session = Depends(get_db)
  db_todo.get_today_values(db)
  # return p
  
# if __name__ == '__main__':
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(today_due_date, 'interval', seconds=3)
#     scheduler.start()
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

#     try:
#         # This is here to simulate application activity (which keeps the main thread alive).
#         while True:
#             time.sleep(2)
#     except (KeyboardInterrupt, SystemExit):
#         # Not strictly necessary if daemonic mode is enabled but should be done if possible
#         scheduler.shutdown()
