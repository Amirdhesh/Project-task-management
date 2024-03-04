from fastapi import APIRouter,HTTPException,Depends
from schemas.task import Taskcreate,TaskRead,TaskUpdate
from db.init_db import Session,get_session
from crud.crud_task import taskCRUD

route = APIRouter()


@route.post('/create_task')
def add_task(*,session:Session = Depends(get_session),task_details):#jwt by role
    try:
        task_exist = taskCRUD.get_task_by_name(session,task_details.name)
        if task_exist:
            raise HTTPException(
                status_code=400,
                detail="Task already exist under this name"
            )
        result = taskCRUD.add_new_task(session=session,task_details=task_details)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error encountered {e}"
        )