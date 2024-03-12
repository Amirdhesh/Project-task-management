from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from schemas.user import UserCreate,UserUpdate
from model import Users
from sqlmodel import SQLModel,select
import bcrypt
class userCRUD:
    def display_all_user(self,session):
        statement = select(Users)
        result = session.exec(statement).unique().all() #Error encountered: exec() arg 1 must be a string, bytes or code object solution: session
        return result
    def New_user(self,session,User_details: UserCreate):
        User_details.password = bcrypt.hashpw(User_details.password.encode('utf-8').bcrypt.gensalt())
        details = jsonable_encoder(User_details)
        user = Users(**details)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status":'Success'}
    

    def get_user_by_mail_id(self,session,email:str):
        user = session.exec(select(Users).where(Users.email == email)).one()
        return user
    

    def profile_update(self,session,user_update:UserUpdate,id):
        user = session.get(Users,id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail= "User not found"
            )
        
        updates = user_update.model_dump(exclude_unset=True)
        print(updates)
        user.sqlmodel_update(updates)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {'status' : True}
    

    def password_change(session,id,new_password):
        user = session.get(Users,id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail= "User not found"
            )
        user.password = bcrypt.hashpw(new_password.encode('utf-8'),bcrypt.gensalt())
        session.add(user)
        session.commit()
        session.refresh(user)
        return {'status':True}
        

UserCRUD = userCRUD()
