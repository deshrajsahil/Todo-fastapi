from routers.schemas import UserBase,UserDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from typing import List


router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('',response_model=UserDisplay)
def create_user(request:UserBase,db:Session = Depends(get_db)):
    return db_user.create_user(db,request)

@router.get('/all', response_model=List[UserDisplay])
def show_users(db: Session = Depends(get_db)):
  return db_user.get_all_users(db)