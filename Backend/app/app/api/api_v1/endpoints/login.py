from fastapi import APIRouter,Depends,HTTPException
from db.init_db import Session,get_session
from schemas.user import login
from model import Users
from core.security.auth_handler import signJWT
import bcrypt
router = APIRouter()


@router.post('/login')
def login(*,session: Session = Depends(get_session),details:login):
    user = session.get(Users,details.email)
    if user and bcrypt.checkpw(details.password.encode('utf-8'),user.password.encode('utf-8')):
        return signJWT(user)
    raise HTTPException(
        status_code=400,
        detail="Incorrect email or password"
    )


