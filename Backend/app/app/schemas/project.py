from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Tasks
    from .team import Teams
class ProjectBase(SQLModel):
    name : str = Field(index=True,nullable=False)
    description : str = Field(nullable=False)
    status : str = Field(nullable=False)
    due_date : date = Field(default="Not Completed",nullable=False)
    team_id : Optional[int] = Field(default=None, foreign_key="teams.id")
    # It causes a many-many mapping
    # task_id : Optional[int] = Field(default=None , foreign_key="tasks.id")

class Projects(ProjectBase,table=True):
    id : Optional[int] = Field(default=True , primary_key=True)
    tasks : List["Tasks"] = Relationship(back_populates="project")
    team_assigned : Optional["Teams"] = Relationship(back_populates="project_assigned")


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id : int


class ProjectUpdate(SQLModel):
    name : Optional[str] = None
    description : Optional[str] = None
    status : Optional[str] = None
    due_date : Optional[date] = None