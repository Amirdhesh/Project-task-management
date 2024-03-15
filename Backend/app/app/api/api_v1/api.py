from fastapi import APIRouter
from api.api_v1.endpoints import login,user,project ,task,team

api = APIRouter()


api.include_router(login.router,tags=['Login'])
api.include_router(user.router,prefix='/user',tags=['Users'])
api.include_router(project.route,prefix='/project',tags=['Projects'])
api.include_router(task.route,prefix='/task',tags=['tasks'])
api.include_router(team.route,prefix='/team',tags=['team'])