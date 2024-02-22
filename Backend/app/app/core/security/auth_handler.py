import time
from typing import Dict
import jwt
from core.config import settings
JWT_secret = settings.JWT_secret
JWT_algorithm = "HS256"

def signJWT(user) -> Dict[str,str]:
    payload = {
        "Id" : user.id,
        "expiry" : time() + 600,
        "role" : user.role,
        "issued_time" : time.time()
    }
    token = jwt.encode(payload,JWT_secret,algorithm = JWT_algorithm)
    return token

def decodeJWT(token:str) -> dict:
    try :
        decoded_token = jwt.decode(token,JWT_secret,algorithms=[JWT_algorithm])
        return decoded_token
    except Exception:
        return {}