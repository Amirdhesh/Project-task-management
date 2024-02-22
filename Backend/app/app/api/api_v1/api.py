from fastapi import APIRouter
from api.api_v1.endpoints import user 

api = APIRouter()

api.include_router(user.router,prefix='/users',tags=['Users'])