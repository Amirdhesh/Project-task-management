from fastapi import Depends,APIRouter,HTTPException
from db.init_db import Session,get_session
from schemas.user import UserCreate,UserUpdate
from crud.crud_user import UserCRUD
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

@router.post('/update_user')
def update_user(*,session:Session = Depends(get_session),updated_user:UserUpdate):
    # try:
    #     user = UserCRUD()
    pass