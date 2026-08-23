from sqlalchemy.orm import Session
from app.schemas.auth_schema import RegisterSchema, LoginSechma, DeleteRefreshToken
from app.models.user_model import UserModel, RoleEnum
from app.models.refresh_token_model import RefreshTokenModel
from fastapi import status, HTTPException
from enum import Enum
from app.core.security import handle_hash_password, verify_password, create_access_token, create_refresh_token, decode_access_token

def register_service(new_user: RegisterSchema, db: Session):
    existed_email = db.query(UserModel).filter(UserModel.email == new_user.email.strip()).first()
    
    if existed_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already exists'
        )
    
    role_user = new_user.role.strip().upper()
    
    if not role_user:
        role_user = 'ADMIN'
    
    if role_user not in [role.value for role in RoleEnum]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Role invalid'
        )
    
    user = UserModel(
        email = new_user.email.strip(),
        password_hash = handle_hash_password(new_user.password.strip()),
        full_name = new_user.full_name.strip().title(),
        role = role_user
    )
    try:
    
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
        
        
    except:
        db.rollback()
        
def login_service(infor: LoginSechma, db: Session):
    user = db.query(UserModel).filter(UserModel.email == infor.email.strip()).first()
    
    if not user or not verify_password(infor.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect email or password.'
        )
    
    existed_user = db.query(RefreshTokenModel).filter(RefreshTokenModel.email_user == user.email).first()
    
    # if existed_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail='You must logout first to login'
    #     )
    
    token = RefreshTokenModel(
        email_user= user.email,
        refresh_token = create_refresh_token({
                            'sub': user.email,
                            'fullName': user.full_name,
                            'role': user.role
                        })    
    )
    try:
        db.add(token)
        db.commit()
        db.refresh(token)
        
    except:
        db.rollback()
    
    return {
        'accessToken': create_access_token({
            'sub': user.email,
            'fullName': user.full_name,
            'role': user.role
        }),
        'typeToken': 'Bearer'
        
    }


def delete_refresh_token_before_logout(token: str, db: Session):
    
    payload = decode_access_token(token)
    
    refresh_token = db.query(RefreshTokenModel).filter(RefreshTokenModel.email_user == payload['sub']).first()
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token invalid'
        )
    
    try:
        db.delete(refresh_token)
        db.commit()
        
        return refresh_token
        
    except:
        db.rollback()
        
def refresh_token_service(acc_token: str, db: Session):
    payload = decode_access_token(acc_token)
    
    refresh_token = db.query(RefreshTokenModel).filter(RefreshTokenModel.email_user == payload['sub']).first()
        
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token invalid'
        )
    
    new_access_token = create_access_token({
        'sub': payload['sub'],
        'fullName': payload['fullName'],
        'role': payload['role']
        
})
    return {
        'accessToken': new_access_token,
        'typeToken': 'Bearer'
    }
    