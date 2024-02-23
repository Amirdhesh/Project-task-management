from fastapi import APIRouter,Depends,HTTPException
from db.init_db import Session,get_session
from schemas.user import login
from model import Users
from core.security.auth_handler import signJWT

router = APIRouter()


@router.post('/')
def login(*,session: Session = Depends(get_session),details : login):
    user = session.get(Users,details.email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        ) 
    return signJWT(user)


