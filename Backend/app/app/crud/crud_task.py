from model import Tasks
from sqlmodel import select,SQLModel
from schemas.task import Taskcreate,TaskRead,TaskUpdate
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

class TasksCrud:
    def get_task_by_name(session,task_name):
        statement = select(Tasks).where(Tasks.name == task_name)
        result = exec(statement).first()
        return result
    def add_new_task(*,session,task_details:Taskcreate):
        task_details = jsonable_encoder(task_details)
        task = Tasks(**task_details)
        session.add(task)
        session.commit()
        session.refresh(task)
        return True
    





taskCRUD = TasksCrud()