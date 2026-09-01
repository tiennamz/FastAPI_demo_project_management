from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, status, HTTPException
from app.models.user_model import UserModel
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
import logging

middlewarw_logger = logging.getLogger("middlewarw_logger")
middlewarw_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(r"C:\Users\ghast\OneDrive\Tài liệu\[IT-215] Phát triển dịch vụ Web với FastAPI\Project Team Management\app\logging\middleware_logging.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - Executor: %(user)s - Action: %(action)s - Detail: %(message)s")
file_handler.setFormatter(formatter)

if not middlewarw_logger.handlers:
    middlewarw_logger.addHandler(file_handler)

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
        middlewarw_logger.warning(
            "Insufficient permissions",
            extra={
                "user": user.email,
                "action": "Login"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only allow admin'
        )    
    return user

