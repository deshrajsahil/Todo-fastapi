from email.mime import base
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
  # items = relationship('DbTodo', back_populates='usert')

class Dbgrp(Base):
  __tablename__ = 'grp'
  g_id = Column(Integer, primary_key=True)
  g_name = Column(String)


class DbTodo(Base):
  __tablename__ = 'todo'
  id = Column(Integer, primary_key=True, index=True)
  task = Column(String)
  assigned_to = Column(String)
  is_completed = Column(String)
  due_date = Column(String)
  user_id = Column(Integer, ForeignKey('user.id'))
  grp_name = Column(String, ForeignKey('grp.g_id'))
  # grp_id = Column(Integer, ForeignKey('grp.g_id'))
  # usert = relationship('DbUser', back_populates='items')

