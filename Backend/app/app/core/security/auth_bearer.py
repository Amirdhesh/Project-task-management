from typing import Coroutine
from typing_extensions import Annotated, Doc
from fastapi import requests,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from auth_handler import decodeJWT
class JWTBearer(HTTPBearer):
    role = "member"
    def __init__(self, auto_error: bool = True, role:str | None = "member"):
        super(JWTBearer,self).__init__( auto_error=auto_error)
        self.role = role
    
    async def __call__(self, request: requests.Request):
        token: HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        if token:

            if not token.scheme == 'Bearer':
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication scheme."
                )
            try:
                payload = self.verify_JWT(token.credentials)
                if payload:
                    if self.role == "member":
                        return payload
                    elif self.role == "Project manager":
                        if payload['role'] == 'Project manager':
                            return payload
                        raise HTTPException(
                            status_code=403,
                            detail="Authorized only for Project Manager"
                        )
                    elif self.role == "Team leader":
                        if payload['role'] == 'Team leader':
                            return payload
                        raise HTTPException(
                            status_code=403,
                            detail="Authorized only for Team Leader"
                        ) 
                else:
                    raise HTTPException(
                        status_code= "401",
                        detail="Invalid or Expired token"
                    )
            except Exception as e:
                raise HTTPException(
                    status_code = "401",
                    detail="Invalid Token"
                )
        else:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            ) 
    

    def verify_JWT(self,JWT_token):
        try:
            payload = decodeJWT(JWT_token)
        except Exception as e:
            payload = None
        if payload:
            return payload
        return False
                    

member_auth = JWTBearer()
project_manager_auth = JWTBearer(role='Project manager')
team_leader_auth = JWTBearer(role="Team lember")