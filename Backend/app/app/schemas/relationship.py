from schemas.user import UserRead
from schemas.team import TeamRead
from schemas.project import ProjectRead
from schemas.task import TaskRead
from typing import Optional

class userrelationship(UserRead):
    team: Optional[TeamRead] = None
    task:Optional[TaskRead] = None


class teamrelationship(TeamRead):
    user: Optional[UserRead] = []
    project: Optional[ProjectRead] = None


class projectrelationship(ProjectRead):
    task: Optional[TaskRead] = []
    team: Optional[TeamRead] = None


class taskrelationship(TaskRead):
     project: Optional[ProjectRead] = []

