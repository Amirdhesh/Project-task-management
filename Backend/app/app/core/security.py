from typing import Any, Coroutine
from typing_extensions import Annotated, Doc
from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials


class JWTChecker(HTTPBearer):
    
    def __init__(self,auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) :
        credentials: HTTPAuthorizationCredentials =await super(JWTChecker, self).__call__(request)
        print(credentials.scheme)
        print(credentials.credentials)
        if credentials.schema == 'Bearer':
            