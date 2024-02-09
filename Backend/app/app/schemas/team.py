from typing import Optional , List
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import Users
    from .project import Projects
class TeamBase(SQLModel):
    Name : str = Field(index= True,nullable=False)


class Teams(TeamBase, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    users : List["Users"] = Relationship(back_populates="team_name")
    project_assigned : Optional["Projects"] = Relationship(back_populates="project_assigned")


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id : int


class TeamUpdate(SQLModel):
    Name : Optional[str] = None
    