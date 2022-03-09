from fastapi import Depends, FastAPI,HTTPException,status
from typing import List,Optional
from db import models
from sqlalchemy.sql.functions import user
from db.database import engine, get_db
from auth import authentication
from routers import user,todo
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm.session import Session
from datetime import date
import slack
from db.models import DbTodo
from sqlalchemy import or_
import uvicorn





# app = FastAPI()


# origins = [
#   'http://localhost:3000',
#   'http://localhost:3001',
#   'http://localhost:3002'
# ]

# app.add_middleware(
#   CORSMiddleware,
#   allow_origins=origins,
#   allow_credentials=True,
#   allow_methods=['*'],
#   allow_headers=['*']
# )

# app.include_router(user.router)
# app.include_router(todo.router)
# app.include_router(authentication.router)



# @app.get("/")
# def root():
#     return "hello world!!"



# models.Base.metadata.create_all(engine)


from fastapi import FastAPI
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Migration service")
scheduler = BackgroundScheduler()


app.include_router(user.router)
app.include_router(todo.router)
app.include_router(authentication.router)

def st():#db: Session = Depends(get_db)):
  # t=[]
  # todo.today_due_date()
  print('inside st...')
  # today = date.today()
  # t = Session.query(DbTodo).filter(DbTodo.due_date == today).filter( or_(DbTodo.is_completed == 0, DbTodo.is_completed == 'false', DbTodo.is_completed == 'False')).all()
  # for x in t:
  #   p=f"{x.assigned_to}, REMINDER!! Today is due date for task {x.task} assigned to {x.assigned_to} and the task is not completed yet...!!! "
  #   slack.task(p)

@app.on_event("startup")
def scheduled_migration():
    print('Started the scheduler.')
    # todo.due_today()
    scheduler.start()

@app.on_event("shutdown")
def end_migration():
    print('Shutting down the scheduler.')
    scheduler.shutdown(wait=False)

@app.get("/health", status_code = 200)
def healthcheck():
    print('Health check done.')

if __name__ == "__main__":
    # scheduler.add_job(st, 'cron',  minute=0, second=3, timezone=pytz.timezone('Asia/Kolkata'))
    scheduler.add_job(st, 'interval', seconds=3)
    print('Added all jobs.')
    uvicorn.run(app, port=8000, host='0.0.0.0')



models.Base.metadata.create_all(engine)
