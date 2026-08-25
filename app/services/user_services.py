from sqlalchemy.orm import Session
from app.models.user_model import UserModel



def get_profile_service(current_user: UserModel, db: Session):
    user = db.query(UserModel).filter(UserModel.email == current_user.email).first()
    
    return user
def get_all_profile_service(db: Session, keyword: str = None):
    users = db.query(UserModel)
    if keyword:
        users = users.filter(UserModel.email.ilike(f'%{keyword}%') | UserModel.full_name.ilike(f'%{keyword}%') | UserModel.is_active == keyword.title())
    return users