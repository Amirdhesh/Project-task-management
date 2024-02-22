from schemas.user import UserBase
from schemas.team import TeamBase
from schemas.task import TaskBase
from schemas.project import ProjectBase
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Users(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_name: Optional['Teams'] = Relationship(back_populates="users", sa_relationship_kwargs={"lazy": "joined"})
    task_assigned: List['Tasks'] = Relationship(back_populates="user_assigned", sa_relationship_kwargs={"lazy": "joined"})

class Teams(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    users: List[Users] = Relationship(back_populates="team_name", sa_relationship_kwargs={"lazy": "joined"})
    project_assigned: Optional['Projects'] = Relationship(back_populates="team_assigned", sa_relationship_kwargs={"lazy": "joined"})

class Tasks(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_assigned: Optional[Users] = Relationship(back_populates="task_assigned")
    project: List['Projects'] = Relationship(back_populates="tasks")

class Projects(ProjectBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    tasks: List[Tasks] = Relationship(back_populates="project")
    team_assigned: Optional[Teams] = Relationship(back_populates="project_assigned")



#Error I encountered
    
# sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. 
# Triggering mapper: 'Mapper[Teams(teams)]'. Original exception was: Mapper 'Mapper[Projects(projects)]' has no property 'teams_assigned'.  
# If this property was indicated from other mappers or configure events, ensure registry.configure() has been called. 

#Corretion made to solve
    
# In your Users and Teams models, you are referencing the related models using strings instead of actual classes. You should use the classes themselves.
# In your Projects model, the default value for the id field is set to True, which is incorrect. The id field should not have a default value.
# The team_assigned relationship in the Projects model is specified as Optional['Teams'], but it should be Optional[Teams] without quotes.