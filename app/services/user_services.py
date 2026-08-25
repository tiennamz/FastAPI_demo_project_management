from sqlalchemy.orm import Session
from app.models.user_model import UserModel



def get_profile_service(current_user: UserModel, db: Session):
    user = db.query(UserModel).filter(UserModel.email == current_user.email).first()
    
    return user

def get_all_profile_service(db: Session, keyword: str = None):
    users = db.query(UserModel)
    if keyword:
        is_active_search = keyword.lower() in ['true', '1', 'active', 'yes']
        users = users.filter(
            (UserModel.email.ilike(f'%{keyword}%')) |
            (UserModel.full_name.ilike(f'%{keyword}%')) |
            ((UserModel.is_active == is_active_search))
        )
    return users.all()