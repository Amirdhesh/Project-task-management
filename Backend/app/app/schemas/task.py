from typing import Optional, List 
from sqlmodel import SQLModel , Field, Relationship
from typing import TYPE_CHECKING
from datetime import date
if TYPE_CHECKING:
    from .user import Users
    from .project import Projects

class TaskBase(SQLModel):
    name : str = Field(index=True,nullable=False)
    discription : str = Field(nullable=False)
    status : str = Field(default="Not Completed",nullable=False)
    due_date : date = Field(nullable=False)
    user_id : Optional[int] = Field(default=None , foreign_key="users.id")
    project_id : Optional[int] = Field(default=None, foreign_key="projects.id")

class Tasks(TaskBase,table=True):
    id : Optional[int] = Field(default=None , primary_key=True)
    user_assigned : Optional["Users"] = Relationship(back_populates="task_assigned")
    project : List["Projects"] = Relationship(back_populates="tasks")


class Taskcreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id : int


class TaskUpdate(SQLModel):
    name : Optional[str] = None
    description : Optional[str] = None
    status : Optional[str] = None
    due_date : Optional[date] = None