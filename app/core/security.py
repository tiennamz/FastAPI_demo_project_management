from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHMS, REFRESH_TOKEN_EXPIRE_DAY
from datetime import datetime, timedelta, timezone
from fastapi import status, HTTPException
import bcrypt
import jwt


def handle_hash_password(password: str):
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode(), salt)
    
    return hash_password.decode()

def verify_password(password: str, hash_password: str):
    return bcrypt.checkpw(password.encode(), hash_password.encode())

def create_access_token(data: dict):
    payload = data.copy()
    
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    
    payload.update({
        'exp': expire_time
    })
    
    token = jwt.encode(payload, SECRET_KEY, ALGORITHMS)
    
    return token

def create_refresh_token(data: dict):
    payload = data.copy()
    
    expire_time = datetime.now(timezone.utc) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAY))
    
    payload.update({
        'exp': expire_time
    })
    
    token = jwt.encode(payload, SECRET_KEY, ALGORITHMS)
    
    return token

def decode_access_token(token: str):
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            ALGORITHMS
        )
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token Expired'
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )
    