from sqlalchemy.orm import Session, joinedload
from app.models.user_model import UserModel
from app.models.project_models import ProjectModel, ProjectMemberModel
from fastapi import status, HTTPException, Depends
from app.schemas.project_member_schemas import NewMember
from fastapi import status, HTTPException
from app.dependencies.middleware import get_current_user
from app.database.database import get_db


def add_new_member_service(pro_id: int, members: list[NewMember], user: UserModel, db: Session):
    project = db.query(ProjectModel).join(ProjectMemberModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == pro_id, ProjectModel.is_deleted == False).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not found project with ID {pro_id}'
        )

    role_user = db.query(ProjectMemberModel.role).join(ProjectModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == pro_id).scalar()
        
    if role_user != 'OWNER':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can perform this function."
        )
        
    for member in members:
        true_user = db.query(UserModel).filter(UserModel.id == member.user_id).first()
        existed_member = db.query(ProjectMemberModel).filter(ProjectMemberModel.user_id == member.user_id, ProjectMemberModel.project_id == pro_id).first()
        if not true_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Not found user with ID {member.user_id}'
            )
        elif existed_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Member with {member.user_id} in this project'
            )
            
        new_member = ProjectMemberModel(
            project_id = pro_id,
            user_id = member.user_id
        )
        db.add(new_member)
        
    db.commit()
    db.refresh(project)
    _ = project.members
    return project
    
    
def delete_member_service(pro_id: int, member_id: int, user: UserModel, db: Session):
    member = db.query(ProjectMemberModel).options(
        joinedload(ProjectMemberModel.project)
    ).filter(ProjectMemberModel.project_id == pro_id, ProjectMemberModel.user_id == member_id, ProjectModel.is_deleted == False).first()
    
    role_user = db.query(ProjectMemberModel.role).join(ProjectModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == pro_id).scalar()
            
    if role_user != 'OWNER':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can perform this function."
        )
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not found mamber with ID {member_id}'
        )
    
    if member.user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You are owner so you can delete yourself'
        )
        
    db.delete(member)
    db.commit()
    
    return None

def is_belong_to_project(pro_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    is_true = db.query(ProjectMemberModel).filter(ProjectMemberModel.project_id == pro_id, ProjectMemberModel.user_id ==user.id).first()
    
    if not is_true:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You haven't joined any project with ID {pro_id}."
        )

def get_all_member_service(project_id: int, user: UserModel, db: Session):
    is_belong_to_project(project_id, user, db)
    members = db.query(ProjectMemberModel).filter(ProjectMemberModel.project_id == project_id).all()

    
    return members
    