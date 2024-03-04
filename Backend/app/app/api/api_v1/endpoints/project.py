from fastapi import APIRouter,Depends,HTTPException
from db.init_db import Session,get_session
from crud.crud_project import projectCRUD
from schemas.project import ProjectCreate,ProjectRead,ProjectUpdate
route = APIRouter()


@route.post('/create_projects')
def create_projects(*,session : Session = Depends(get_session),new_project:ProjectCreate):#JWT token by role
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
    

@route.get('/get_project_by_name')
def get_project_by_name(*,session:Session = Depends(get_session),project_name):
    project = projectCRUD.get_project_by_name(session=session,project_name=project_name)
    print(project)

@route.put('/update_project')
def update_project(*,session:Session = Depends(get_session),project_name,project_update:ProjectUpdate):
    update = projectCRUD.update_project(session=session,project_name=project_name,project_update=project_update)
    return update
