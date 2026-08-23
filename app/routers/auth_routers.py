from fastapi import APIRouter, Depends, Request, status
from app.services.auth_services import register_service, login_service, delete_refresh_token_before_logout, refresh_token_service
from app.schemas.auth_schema import RegisterSchema, LoginSechma
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.utils.response import create_response, BaseResponse
from app.schemas.user_schemas import ResponseUser
from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter(prefix='/auth', tags=['Auth'])
limiter = Limiter(key_func=get_remote_address)

@router.post('/register', response_model=BaseResponse[ResponseUser], status_code=status.HTTP_201_CREATED)
def handle_register(request: Request, new_user: RegisterSchema, db: Session = Depends(get_db)):
    user = register_service(new_user, db)
    
    return create_response(
        request,
        status.HTTP_201_CREATED,
        'Success',
        user
    )

@router.post('/login')
@limiter.limit('5/minutes')
def handle_login(request: Request, infor: LoginSechma, db: Session =Depends(get_db)):
    token = login_service(infor, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        token
    )
    
@router.post('/refresh')
def refresh_token(request: Request, access_token: str, db: Session = Depends(get_db)):
    token = refresh_token_service(access_token, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        token
    )
    
@router.post('/refresh_token/delete')
def delete_refresh_token(request: Request, token: str, db: Session = Depends(get_db)):
    refresh_token = delete_refresh_token_before_logout(token, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success'
    )

