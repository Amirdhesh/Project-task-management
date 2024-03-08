from sqlmodel import SQLModel,select
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.project import ProjectCreate,ProjectUpdate,ProjectRead
from model import Projects
from sqlmodel import SQLModel,select


class ProjectCRUD:
    def new_project(self,session,new_project:ProjectCreate):
        new_project = jsonable_encoder(new_project)

        project = Projects(**new_project)
        session.add(project)
        session.commit()
        session.refresh(project)
        return {"status":True}
    

    def get_project_by_name(self, session, project_name) -> ProjectRead:
        statement = select(Projects).where(Projects.name == project_name)
        result = session.execute(statement).first()
        return {"status" : True , "project" : result}
    

    def update_project(self,session,project_name,project_update):
        statement = select(Projects).where(Projects.name == project_name)
        result = session.execute(statement).first()
        if not result:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )
        updates = project_update.model_dump(exclude_unset = True)
        result.sqlmodel_update(updates)
        session.add(result)
        session.commit()
        session.refresh()
        return {"status":True}
    
    def project_delete(session,project_id):
        project = session.get(Projects,project_id)
        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project Not Found"
            )
        session.delete(project)
        session.commit()
        return {"status":True}
    






projectCRUD =ProjectCRUD()