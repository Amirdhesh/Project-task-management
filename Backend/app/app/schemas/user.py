from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Tasks
    from .team import Teams
class UserBase(SQLModel):
    name : str = Field(index=True,nullable=False)
    role : str = Field(nullable=False)
    DOB : Optional[date] 
    address : str = Field(nullable=False)
    email : str = Field(nullable=False)
    phonenumber : int = Field(unique= True , nullable= False)
    password : str = Field(nullable=False)
    team_id : Optional[int] = Field(default=None , foreign_key="teams.id")


class Users(UserBase,table = True):
    id : Optional[int] = Field(default=None,primary_key=True)
    team_name : Optional["Teams"] = Relationship(back_populates="users")
    task_assigned : List["Tasks"] = Relationship(back_populates="user_assigned")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id : int


class UserUpdate(UserBase):
    name : Optional[str] = None
    role : Optional[str] = None
    email : Optional[str] = None
    phonenumber : Optional[int] = None
    password : Optional[int] = None