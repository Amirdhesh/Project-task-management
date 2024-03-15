from fastapi import Depends,APIRouter,HTTPException
from db.init_db import Session,get_session
from schemas.user import UserCreate,UserUpdate,UserRead
from crud.crud_user import UserCRUD
from crud.crud_team import teamCRUD
from schemas.relationship import userrelationship
from core.security.auth_bearer import member_auth,project_manager_auth
from model import Users
from typing import List
router = APIRouter()


@router.post('/')
def create_user(*,session:Session = Depends(get_session),user_detail:UserCreate,jwt_data = Depends(project_manager_auth)):
    try:
        
        already_existing_user = UserCRUD.get_user_by_mail_id(session=session,email=user_detail.email)
        if already_existing_user:
            raise HTTPException(
                status_code= 400,
                detail="User already exist"
            )
        status = UserCRUD.New_user(session=session,User_details=user_detail)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error encountered : {e}"
        )


@router.patch('/profile_update')
def profile_update(*,session:Session = Depends(get_session),updated_user:UserUpdate,jwt_data = Depends(member_auth)): #JWT to be added
    try:
        
        status = UserCRUD.profile_update(session=session,user_update=updated_user,id=jwt_data['id'])
        
        return status
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error Encountered {e}"
        )
    
@router.get("/get_user_by_id",response_model=userrelationship)
def get_user_by_id(*,session:Session = Depends(get_session),jwt_data = Depends(member_auth)): #jwt token
    user = session.get(Users , jwt_data["id"])
    return user


@router.get("/get_all_user",response_model=List[userrelationship]) #Error : Joined eger load, Solution : .Unique() add to remove duplicate rows
def get_all_user(*,session:Session = Depends(get_session),jwt_data = Depends(project_manager_auth)): #jwt token by role(pm)
    try:
        result = UserCRUD.display_all_user(session=session)
        if not result:
            raise HTTPException(
                status_code=404,
                detail="No user available"
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"Error occured {e}"
        )

@router.put('/change_password')
def change_password(*,session:Session = Depends(get_session),jwt_data = Depends(member_auth),new_password): #jwt token
    status = UserCRUD.password_change(session,jwt_data["id"],new_password)
    return status


@router.put('/assign_user_team')
def assign_user_team(*,session:Session = Depends(get_session),user_id:int,team_name,jwt_data = Depends(project_manager_auth)):
    team = teamCRUD.team_by_name(session=session,team_name=team_name)
    user = session.get(Users,user_id)
    if not team :
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    user.team_id = team.id
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status":True}
    
