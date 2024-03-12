from fastapi import Depends,APIRouter,HTTPException
from db.init_db import Session,get_session
from schemas.user import UserCreate,UserUpdate,UserRead
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


@router.patch('/profile_update')
def profile_update(*,session:Session = Depends(get_session),updated_user:UserUpdate,userid:int): #JWT to be added
    try:
        user = UserCRUD()
        status = user.profile_update(session=session,user_update=updated_user,id=userid)
        
        return status
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error Encountered {e}"
        )
    
@router.get("/get_user_by_id",response_model=UserRead)
def get_user_by_id(*,session:Session = Depends(get_session),id): #jwt token
    user = session.get(Users , id)
    return user


@router.get("/get_all_user",response_model=UserRead) #Error : Joined eger load, Solution : .Unique() add to remove duplicate rows
def get_all_user(*,session:Session = Depends(get_session)): #jwt token by role(pm)
    statement = select(Users) #Need to be used: selectinload(Users.task_assigned) retrieve related objects along with the main objects in a single query thus reducing the number of database round-trips and improving performance.
    user = session.exec(statement).unique().all()
    return user

@router.put('/change_password')
def change_password(*,session:Session = Depends(get_session),id,new_password): #jwt token
    status = UserCRUD.password_change(session=session,id=id,new_password=new_password)
    return status