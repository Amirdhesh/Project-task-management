from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date
class ProjectBase(SQLModel):
    name : str = Field(index=True,nullable=False)
    description : str = Field(nullable=False)
    status : str = Field(nullable=False)
    due_date : date = Field(default="Not Completed",nullable=False)
    team_id : Optional[int] = Field(default=None, foreign_key="teams.id")
    # It causes a many-many mapping
    # task_id : Optional[int] = Field(default=None , foreign_key="tasks.id")




class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id : int


class ProjectUpdate(SQLModel):
    name : Optional[str] = None
    description : Optional[str] = None
    status : Optional[str] = None
    due_date : Optional[date] = None