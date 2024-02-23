from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class UserBase(SQLModel):
    name: str = Field(index=True, nullable=False)
    role: str = Field(nullable=False)
    DOB: Optional[date] = Field(default=None)
    address: str = Field(nullable=False)
    email: str = Field(nullable=False)
    phonenumber: int = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id")


class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: Optional[str] = None
    role: Optional[str] = None
    DOB: Optional[date] = None
    address: Optional[str] = None
    phonenumber: Optional[int] = None


class login(SQLModel):
    email : str
    password : str