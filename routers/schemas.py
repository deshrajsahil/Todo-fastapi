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

class TodoBase(BaseModel):
  task: str
  assigned_to: str
  due_date: date
  is_completed: Optional[bool]='false'
  # grp_txt: Optional[str] = ''
  # grp_id: Optional[int] = ''

class TodoGrpBase(BaseModel):
  g_txt: Optional[str] = ''
  g_id: Optional[int] = ''


class TodoGrpDisplay(BaseModel):
  g_txt: Optional[str] = ''
  g_id: Optional[int] = ''
  class Config():
    orm_mode = True

# For user who assigned task Display
class User(BaseModel):
  username: str
  class Config():
    orm_mode = True

# for todo display
class TodoDisplay(BaseModel):
  id: int
  task: str
  assigned_to: str
  due_date: date
  is_completed: bool
  # grp_txt: str
  # grp_id: int
  # user: User
  class Config():
    orm_mode = True

class UserAuth(BaseModel):
  id: int
  username: str
  email: str


# class Upadate_Work(BaseModel):
#   is_completed: Optional[bool]='false'

# update todo
# class Update_TodoBase(BaseModel):
#   task: str
#   assigned_to: str
#   due_date: date
#   is_completed: Optional[bool]='false'
#   grp_txt: Optional[str] = ''
#   grp_id: Optional[int] = ''



# class Update_TodoDisplay(BaseModel):
#   id: int
#   task: str
#   assigned_to: str
#   due_date: date
#   is_completed: bool
#   user_id: int
#   grp_txt: str
#   grp_id: int
#   class Config():
#     orm_mode = True


# class Task_Inside_Display(BaseModel):
#   id: int
#   task: str
#   assigned_to: str
#   due_date: date
#   is_completed: bool
#   class Config():
#     orm_mode = True



# class Groupwise_Task(BaseModel):
#   grp_id: int
#   grp_txt: str
#   # task: str
#   tasks: Optional[List[Task_Inside_Display]]
#   # tasks: str
#   class Config():
#     orm_mode = True

