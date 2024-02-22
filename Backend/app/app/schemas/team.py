from typing import Optional
from sqlmodel import SQLModel, Field
class TeamBase(SQLModel):
    Name: str = Field(index=True, nullable=False)



class TeamCreate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: int

class TeamUpdate(SQLModel):
    Name: Optional[str] = None
