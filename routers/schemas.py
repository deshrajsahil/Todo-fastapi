from pydantic import BaseModel
from datetime import date
from typing import List, Optional

from sqlalchemy import false


class UserBase(BaseModel):
  username: str
  email: str
  password: str

# for user display
class UserDisplay(BaseModel):
  username: str
  email: str
  class Config():
    orm_mode = True


class TodoGrpBase(BaseModel):
  g_name: Optional[str] = 'GroupName'


class TodoGrpDisplay(BaseModel):
  g_id: Optional[int] = ''
  g_name: Optional[str] = ''
  class Config():
    orm_mode = True

class TodoBase(BaseModel):
  task: str
  assigned_to: str
  is_completed: Optional[bool]='false'
  due_date: date
  grp_name: Optional[str] = 'GroupName'

# for todo display
class TodoDisplay(BaseModel):
  # grp_id: int
  grp_name: str
  id: int
  task: str
  assigned_to: str
  due_date: date
  is_completed: bool
  class Config():
    orm_mode = True

class UserAuth(BaseModel):
  id: int
  username: str
  email: str



# update todo
class Update_TodoBase(BaseModel):
  task: str
  assigned_to: str
  due_date: date
  is_completed: Optional[bool]='false'
  # grp_name: Optional[str] = ''
  # grp_id: Optional[int] = ''



class Update_TodoDisplay(BaseModel):
  id: int
  task: str
  assigned_to: str
  due_date: date
  is_completed: bool
  # user_id: int
  grp_name: str
  # grp_id: int
  class Config():
    orm_mode = True

class Upadate_Work(BaseModel):
  is_completed: Optional[bool]='false'

class Task_Inside_Display(BaseModel):
  id: int
  task: str
  assigned_to: str
  due_date: date
  is_completed: bool
  grp_name: str
  class Config():
    orm_mode = True



class Groupwise_Task(BaseModel):
  grp_id: int
  grp_name: str
  # task: str
  tasks: Optional[List[Task_Inside_Display]]
  # tasks: str
  class Config():
    orm_mode = True

