from sqlalchemy.orm import Session
from app.models.user_model import UserModel



def get_profile_service(current_user: UserModel, db: Session):
    user = db.query(UserModel).filter(UserModel.email == current_user.email).first()
    
    return user
def get_all_profile_service(db: Session):
    users = db.query(UserModel).all()
    return users