from fastapi import HTTPException, status
from routers.schemas import TodoBase
from sqlalchemy.orm.session import Session
from db.models import DbTodo



def create(db: Session, request: TodoBase):
  new_todo = DbTodo(
    task = request.task,
    assigned_to = request.assigned_to,
    due_date = request.due_date,
    is_completed = request.is_completed,
    # user_id = request.creator_id
  )
  db.add(new_todo)
  db.commit()
  db.refresh(new_todo)
  return new_todo

def get_all_todos(db: Session):
  return db.query(DbTodo).all()

def delete(db: Session, id: int, user_id: int):
  todo = db.query(DbTodo).filter(DbTodo.id == id).first()
  if not todo:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
          detail=f'ToDo with id {id} not found')
  if todo.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
          detail='Only todo creator can delete post')

  db.delete(todo)
  db.commit()
  return 'ok'