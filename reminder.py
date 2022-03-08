from slack_bolt import App
from datetime import date
import time
import os
from db.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from routers import todo
from dotenv import load_dotenv
from db.db_todo import lol
from sqlalchemy.orm.session import Session




load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]


app = App(token=SLACK_BOT_TOKEN)



def task(d):
    app.client.chat_postMessage(channel='#simple-bot-test',text=f"{d}")

def st():
    db: Session = Depends(get_db)
    todo.today_due_date()



if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(st, 'interval', seconds=3)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()


