from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from schemas.user import UserCreate,UserUpdate
from model import Users
from sqlmodel import SQLModel,select
class UserCRUD:
    def New_user(self,session,User_details: UserCreate):
        details = jsonable_encoder(User_details)
        user = Users(**details)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"Status":'Success'}
    

    def get_user_by_mail_id(self,session,email:str):
        user = session.exec(select(Users).where(Users.email == email)).one()
        return user
    

    def profile_update(self,session,user_update:UserUpdate,user_id):
        user = session.get(Users,user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail= "User not found"
            )
        updates = user_update.model_dump(exclude_unset=True)
        user.sqlmodel_update(updates)
        session.add(user)
        session.commit()
        session.refresh()
        return {'status' : True}
