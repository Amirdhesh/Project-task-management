from fastapi import APIRouter
from api.api_v1.endpoints import user,project 

api = APIRouter()

api.include_router(user.router,prefix='/users',tags=['Users'])
api.include_router(project.route,prefix='/projects',tags=['Projects'])