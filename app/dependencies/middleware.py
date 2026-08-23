from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, status, HTTPException
from app.models.user_model import UserModel
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.core.security import decode_access_token



security = HTTPBearer()

def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = cred.credentials
    payload = decode_access_token(token)
    
    user = db.query(UserModel).filter(UserModel.email == payload['sub']).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not existed'
        )
        
    return user

def check_admin(user: UserModel = Depends(get_current_user)):
    if user.role != 'ADMIN':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only allow admin'
        )    
    return user

