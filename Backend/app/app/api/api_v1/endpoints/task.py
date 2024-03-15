from fastapi import APIRouter,HTTPException,Depends
from schemas.task import Taskcreate,TaskRead,TaskUpdate
from db.init_db import Session,get_session
from crud.crud_task import taskCRUD
from crud.crud_project import projectCRUD
from core.security.auth_bearer import project_manager_auth,team_leader_auth,member_auth
from model import Tasks,Users,Projects
from schemas.relationship import taskrelationship
route = APIRouter()


@route.post('/create_task')
def add_task(*,session:Session = Depends(get_session),task_details:Taskcreate,jwt_data = Depends(team_leader_auth)):#jwt by role
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
    

@route.get('/get_user_task',response_model=taskrelationship)
def get_user_task(*,session:Session = Depends(get_session),jwt_data = Depends(member_auth)):#jwt_token
    try:
        task = session.get(Tasks,jwt_data["id"])
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
def update_task_status(*,session:Session = Depends(get_session),task_update:TaskUpdate,jwt_data = Depends(member_auth)):
    try:
        result = taskCRUD.update_task(session=session,task_update=task_update,user_id=jwt_data["id"])
        return result
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error occured {e}"
        )
    

@route.delete('/delete_task')
def delete_task(*,session:Session = Depends(get_session),task_id:int,jwt_data = Depends(team_leader_auth)):
    try:
        result = taskCRUD.task_delete(session=session,id=task_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error occured {e}"
        )
    

@route.put('/assign_user')
def assign_user_team(*,session:Session = Depends(get_session),task_id:int,user_id,jwt_data = Depends(project_manager_auth)):
    task = session.get(Tasks,task_id)
    user = session.get(Users,user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    task.user_id = user_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status":True}


@route.put('/assign_project')
def assign_user_team(*,session:Session = Depends(get_session),task_id:int,project_name,jwt_data = Depends(project_manager_auth)):
    project = projectCRUD.get_project_by_name(session=session,project_name=project_name)
    task = session.get(Users,task_id)
    if not task :
        raise HTTPException(
            status_code=404,
            detail="task not found"
        )
    if not project:
        raise HTTPException(
            status_code=404,
            detail="project not found"
        )

    task.project_id = project.id
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status":True}
