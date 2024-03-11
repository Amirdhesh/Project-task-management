from model import Tasks
from sqlmodel import select,SQLModel
from schemas.task import Taskcreate,TaskRead,TaskUpdate
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

class TasksCrud:
    def get_task_by_name(self,session,task_name):
        statement = select(Tasks).where(Tasks.name == task_name)
        result = session.exec(statement).first()
        return result
    def add_new_task(self,session,task_details:Taskcreate):
        task_details = jsonable_encoder(task_details)
        task = Tasks(**task_details)
        session.add(task)
        session.commit()
        session.refresh(task)
        return True
    def update_task(self,session,task_update:TaskUpdate,user_id):
        task = session.get(Tasks,user_id)
        task_update = task_update.model_dump(exclude_unset = True)
        Tasks.sqlmodel_update(task_update)
        session.add(task)
        session.commit()
        session.refresh()
        return True
    def task_delete(self,session,id):
        task = session.get(Tasks,id)
        print(task)
        if not task:
            raise HTTPException(
                status_code=400,
                detail="task not found"
            )
        session.delete(task)
        session.commit()
        return {'status':True}






taskCRUD = TasksCrud()