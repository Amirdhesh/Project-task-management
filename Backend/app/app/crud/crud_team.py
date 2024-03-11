from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.team import TeamCreate,TeamRead,TeamUpdate
from model import Teams
from sqlmodel import SQLModel,select


class TeamCRUD:
    def display_all_team(self,session):
        statement = select(Teams)
        result = session.exec(statement).all() #Error encountered: exec() arg 1 must be a string, bytes or code object solution: session
        return result
    
    def team_by_name(self,session,team_name):
        statement = select(Teams).where(Teams.Name == team_name)
        result = session.exec(statement).all()
        return result
    
    def add_new_team(self,session,team_details):
        team_details = jsonable_encoder(team_details)
        team = Teams(**team_details)
        session.add(team)
        session.commit()
        session.refresh(team)
        return {"status":True}
    
    def update_team(self,session,team_update,team_id):
        team = session.get(Teams,team_id)
        if not team:
            raise HTTPException(
                status_code=404,
                detail="Team not found"
            )
        team_update = team_update.model_dump(exclude_unset = True)
        team.sqlmodel_update(team_update)
        session.add(team)
        session.commit()
        session.refresh()
        return {"status":True}
    






teamCRUD = TeamCRUD()