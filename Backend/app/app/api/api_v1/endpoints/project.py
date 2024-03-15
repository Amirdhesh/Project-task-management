from fastapi import APIRouter,Depends,HTTPException
from db.init_db import Session,get_session
from crud.crud_project import projectCRUD
from crud.crud_team import teamCRUD
from schemas.project import ProjectCreate,ProjectRead,ProjectUpdate
from core.security.auth_bearer import project_manager_auth
from schemas.relationship import projectrelationship
from model import Teams,Projects
route = APIRouter()


@route.post('/create_projects')
def create_projects(*,session : Session = Depends(get_session),new_project:ProjectCreate,jwt_data = Depends(project_manager_auth)):#JWT token by role
    try:
        project_exist = projectCRUD.get_project_by_name(session=session,project_name=new_project.name)
        if project_exist:
            raise HTTPException(
                status_code=400,
                detail="Project already existing under this name"
            )
        status = projectCRUD.new_project(session=session,new_project=new_project)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f'Error Encounter: {e}'
        )
    

@route.get('/get_project_by_name',response_model=projectrelationship)
def get_project_by_name(*,session:Session = Depends(get_session),project_name,jwt_data = Depends(project_manager_auth)):
    project = projectCRUD.get_project_by_name(session=session,project_name=project_name)
    return project

@route.put('/update_project')
def update_project(*,session:Session = Depends(get_session),project_name,project_update:ProjectUpdate,jwt_data = Depends(project_manager_auth)):
    update = projectCRUD.update_project(session=session,project_name=project_name,project_update=project_update)
    return update


@route.delete('/delete_project')
def delete_project(*,session:Session = Depends(get_session),project_id,jwt_data = Depends(project_manager_auth)): #JWT_token
    try:
        result = projectCRUD.project_delete(session=session,project_id=project_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error occured {e}"
        )
    
@route.put('/assign_team')
def assign_user_team(*,session:Session = Depends(get_session),project_name,team_name,jwt_data = Depends(project_manager_auth)):
    team = teamCRUD.team_by_name(session=session,team_name=team_name)
    project = projectCRUD.get_project_by_name(session=session,project_name=project_name)
    if not team :
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    if not project:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    project.team_id = team.id
    session.add(project)
    session.commit()
    session.refresh(project)
    return {"status":True}