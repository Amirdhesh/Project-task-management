from typing import Optional 
from sqlmodel import SQLModel , Field
from datetime import date


class TaskBase(SQLModel):
    name : str = Field(index=True,nullable=False)
    discription : str = Field(nullable=False)
    status : str = Field(default="Not Completed",nullable=False)
    due_date : date = Field(nullable=False)
    user_id : Optional[int] = Field(default=None , foreign_key="users.id")
    project_id : Optional[int] = Field(default=None, foreign_key="projects.id")




class Taskcreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id : int


class TaskUpdate(SQLModel):
    name : Optional[str] = None
    description : Optional[str] = None
    status : Optional[str] = None
    due_date : Optional[date] = None