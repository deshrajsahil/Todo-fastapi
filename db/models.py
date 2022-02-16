from datetime import date
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship


class DbUser(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String)
  email = Column(String)
  password = Column(String)
  items = relationship('DbTodo', back_populates='user')

class DbTodo(Base):
  __tablename__ = 'todo'
  id = Column(Integer, primary_key=True, index=True)
  task = Column(String)
  assigned_to = Column(String)
  is_completed = Column(String)
  due_date = Column(Date)
  user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship('DbUser', back_populates='items')

