from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth as firebase_auth
import firebase_admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token["uid"]
        return uid
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def requires_auth(func):
    async def wrapper(*args, **kwargs):
        uid = await authenticate_user(*args, **kwargs)
        return await func(uid, *args, **kwargs)

    return wrapper
