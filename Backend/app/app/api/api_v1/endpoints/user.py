from fastapi import Depends,APIRouter,HTTPException
from db.init_db import Session,get_session
from schemas.user import UserCreate,UserUpdate
from crud.crud_user import UserCRUD
from model import Users
from sqlmodel import select
router = APIRouter()


@router.post('/')
def create_user(*,session:Session = Depends(get_session),user_detail:UserCreate):
    try:
        user = UserCRUD()
        already_existing_user = user.get_user_by_mail_id(session=session,email=user_detail.email)
        if already_existing_user:
            raise HTTPException(
                status_code= 400,
                detail="User already exist"
            )
        status = user.New_user(session=session,User_details=user_detail)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error encountered : {e}"
        )

@router.put('/profile_update')
def profile_update(*,session:Session = Depends(get_session),updated_user:UserUpdate,userid): #JWT to be added
    try:
        user = UserCRUD()
        status = user.profile_update(session=session,user_update=updated_user,user_id=userid)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail="Error Encountered"
        )
    
@router.get("/get_user_by_id")
def get_user_by_id(*,session:Session = Depends(get_session)): #jwt token
    user = session.get(Users , id)
    return user


@router.get("/get_all_user")
def get_all_user(*,session:Session = Depends(get_session)): #jwt token by role(pm)
    user = session.exec(select(Users)).all()
    return user

@router.put('/chanage_password')
def change_password(*,session:Session = Depends(get_session),new_password): #jwt token
    status = UserCRUD.password_change(session=session,new_password=new_password)
    return status