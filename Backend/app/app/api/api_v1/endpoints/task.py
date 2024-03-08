from fastapi import APIRouter,HTTPException,Depends
from schemas.task import Taskcreate,TaskRead,TaskUpdate
from db.init_db import Session,get_session
from crud.crud_task import taskCRUD
from model import Tasks
route = APIRouter()


@route.post('/create_task')
def add_task(*,session:Session = Depends(get_session),task_details):#jwt by role
    try:
        task_exist = taskCRUD.get_task_by_name(session,task_details.name)
        if not task_exist:
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
    

@route.get('/get_user_task',response_model=TaskRead)
def get_user_task(*,session:Session = Depends(get_session),user_id):#jwt_token
    try:
        task = session.get(Tasks,user_id)
        if not task:
            raise HTTPException(
                status_code=400,
                detail="Task not assigned"
            )
        return {'status':True , 'tasks' : task}
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error encountered {e}"
        )
    

@route.put('/update_task_status')
def update_task_status(*,session:Session = Depends(get_session),task_update:TaskUpdate,user_id):
    try:
        result = taskCRUD.update_task(session=session,task_update=task_update,user_id=user_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error occured {e}"
        )
    

@route.delete('/delete_task')
def delete_task(*,session:Session = Depends(get_session),task_id):
    try:
        result = taskCRUD.task_delete(session=session,task_id=task_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error occured {e}"
        )
