from sqlalchemy.orm import Session, joinedload
from app.models.user_model import UserModel
from app.models.project_models import ProjectModel, ProjectMemberModel
from fastapi import status, HTTPException, Depends
from app.schemas.project_member_schemas import NewMember
from fastapi import status, HTTPException
from app.dependencies.middleware import get_current_user
from app.database.database import get_db
import logging

project_member_logger = logging.getLogger("project_member_logger")
project_member_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(r"C:\Users\ghast\OneDrive\Tài liệu\[IT-215] Phát triển dịch vụ Web với FastAPI\Project Team Management\app\logging\project_member_logging.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - Executor: %(user)s - Action: %(action)s - Detail: %(message)s")
file_handler.setFormatter(formatter)

if not project_member_logger.handlers:
    project_member_logger.addHandler(file_handler)

def add_new_member_service(pro_id: int, members: list[NewMember], user: UserModel, db: Session):
    project = db.query(ProjectModel).join(ProjectMemberModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == pro_id, ProjectModel.is_deleted == False).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not found project with ID {pro_id}'
        )

    role_user = db.query(ProjectMemberModel.role).join(ProjectModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == pro_id).scalar()
        
    if role_user != 'OWNER':
        project_member_logger.warning(
            "Failed to add member because you are not owner.",
            extra={
                "user": user.email,
                "action": "Add members"
            }
        )
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
                detail=f'This member has been on this project.'
            )
            
        new_member = ProjectMemberModel(
            project_id = pro_id,
            user_id = member.user_id
        )
        db.add(new_member)
        
    db.commit()
    db.refresh(project)
    _ = project.members
    
    project_member_logger.info(
        f"Add successful members to the project {pro_id}",
        extra={
            "user": user.email,
            "action": "Add members"
        }
    )
    
    return project
    
    
def delete_member_service(pro_id: int, member_id: int, user: UserModel, db: Session):
    project = db.query(ProjectModel).filter(ProjectModel.id == pro_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not found project with ID {pro_id}'
        )
    
    
    member = db.query(ProjectMemberModel).options(
        joinedload(ProjectMemberModel.project)
    ).filter(ProjectMemberModel.project_id == pro_id, ProjectMemberModel.user_id == member_id, ProjectModel.is_deleted == False).first()
    
    role_user = db.query(ProjectMemberModel.role).join(ProjectModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == pro_id).scalar()
            
    if role_user == 'MEMBER' and member_id == member.user_id:
        db.delete(member)
        db.commit() 
            
            
    if role_user != 'OWNER':
        project_member_logger.warning(
            "Failed to delete member because you are not owner.",
            extra={
                "user": user.email,
                "action": "Delete member"
            }
        )
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
        
    if member_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The owner cannot delete themselves.'
        )
        
    db.delete(member)
    db.commit()
    
    project_member_logger.info(
        f"Successfully removed member {member_id} from the project {pro_id}.",
        extra={ 
            "user": user.email,
            "action": "Delete member"
        }
    )
    
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
    