from fastapi.encoders import jsonable_encoder
from schemas.user import UserCreate,UserUpdate
from model import Users
from sqlmodel import select
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
    

    def user_update(self,session,user_update:UserUpdate):
        pass
