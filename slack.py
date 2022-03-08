from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
import time
from apscheduler.schedulers.background import BackgroundScheduler
from db import db_todo
from db.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime



load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]


app = App(token=SLACK_BOT_TOKEN)



def task(d):
    app.client.chat_postMessage(channel='#simple-bot-test',text=f"{d}")


# schedule.every().day.at("13:26").do(task)

# while True:
#     schedule.run_pending()
# #     time.sleep(1)
# def today_due_date(db: Session = Depends(get_db)):
#   # t = await db_todo.today_due_date(db)

#   return db_todo.today_due_date(db)

# def today_due_date(db: Session = Depends(get_db)):
#   # today = date.today()
#   # p_todo=[]
#   # p_todo = db.query(DbTodo).filter(DbTodo.due_date == today).filter( or_(DbTodo.is_completed == 0, DbTodo.is_completed == 'false', DbTodo.is_completed == 'False')).all()
#   # for x in p_todo:
#   #   p=f"{x.assigned_to}, REMINDER!! Today is due date for task {x.task} assigned to {x.assigned_to} and the task is not completed yet...!!! "
#   #   slack.task(p)
#   # return p_todo
#   a="hummmmmaaaa"
#   task(a)
#   return a


# if __name__ == '__main__':
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(today_due_date)
#     scheduler.start()
#     # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

#     try:
#         # This is here to simulate application activity (which keeps the main thread alive).
#         while True:
#             time.sleep(2)
#     except (KeyboardInterrupt, SystemExit):
#         # Not strictly necessary if daemonic mode is enabled but should be done if possible
#         scheduler.shutdown()