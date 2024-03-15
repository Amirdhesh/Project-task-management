from fastapi import APIRouter,Depends,HTTPException
from db.init_db import get_session,Session
from crud.crud_team import teamCRUD
from schemas.team import TeamCreate,TeamUpdate
from schemas.relationship import teamrelationship
from core.security.auth_bearer import project_manager_auth
from typing import List
route = APIRouter()

@route.get('/display_all_teams',response_model=List[teamrelationship])
def display_all_teams(*,session:Session=Depends(get_session),depends = Depends(project_manager_auth)):#jwt token
    try:
        result = teamCRUD.display_all_team(session=session)
        if not result:
            raise HTTPException(
                status_code=404,
                detail="No teams available"
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error occured {e}"
        )
    
@route.post('/add_new_team')
def add_new_team(*,session :Session= Depends(get_session),team_detail:TeamCreate,jwt_data = Depends(project_manager_auth)):
    try:
        existing_name = teamCRUD.team_by_name(session=session,team_name=team_detail.Name)
        if existing_name:
            raise HTTPException (
                status_code=400,
                detail="Team already exist"
            )
        print("OK")
        result = teamCRUD.add_new_team(session=session,team_details=team_detail)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error Occured {e}"
        )
    

@route.put('/update_team')
def update_team(*,session:Session = Depends(get_session),team_update : TeamUpdate,team_id,jwt_data = Depends(project_manager_auth) ):
    try:
        team = teamCRUD.update_team(session=session,team_id=team_id,team_update=team_update)
        return team
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error Occured {e}"
        )
    

@route.delete('/delete_team')
def delete_task(*,session:Session = Depends(get_session),team_id:int,jwt_data = Depends(project_manager_auth)):
    try:
        result = teamCRUD.team_delete(session=session,id=team_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error occured {e}"
        )