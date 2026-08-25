from app.services.user_services import get_profile_service, get_all_profile_service
from fastapi import APIRouter, Depends, Request, status
from app.dependencies.middleware import get_current_user, check_admin
from app.models.user_model import UserModel
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user_schemas import ResponseUser
from app.utils.response import BaseResponse, create_response

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/me', response_model=BaseResponse[ResponseUser])
def get_profile(request: Request, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_profile_service(current_user, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        user
    )

@router.get('/', response_model=BaseResponse[list[ResponseUser]])
def get_all_profile(request: Request, keyword: str = None, is_active: bool = None, current_user: UserModel = Depends(check_admin), db: Session = Depends(get_db)):
    users = get_all_profile_service(db, keyword, is_active)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        users
    )