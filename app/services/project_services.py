from sqlalchemy.orm import Session
from app.schemas.project_schemas import CreateProject, UpdateProject
from app.models.project_models import ProjectModel
from app.models.project_models import ProjectMemberModel
from app.models.user_model import UserModel
from fastapi import status, HTTPException
from datetime import datetime

def create_new_project_service(user: UserModel, new_project: CreateProject, db: Session):
    
    existed_project = db.query(ProjectModel).filter(ProjectModel.name == new_project.name).first()
    
    if existed_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This project is existed'
        )
    
    project = ProjectModel(
        name= new_project.name.title(),
        description = new_project.description,
        owner_id = user.id
        
    )
    
    existed_user = db.query(UserModel).filter(UserModel.id == user.id).first()
    
    if not existed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with ID {user.id} not found.'
        )
        
    db.add(project)
    db.flush()
    member = ProjectMemberModel(
        project_id = project.id,
        user_id = user.id,
        role = 'OWNER'
    )
    
    db.add(member)
    db.commit()
    db.refresh(project)
    
    return project

def get_project_by_user_service(user: UserModel, db: Session, name_project: str = None) :
    projects = db.query(ProjectModel).join(ProjectMemberModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.is_deleted == False)
    
    if name_project:
        projects = projects.filter(ProjectModel.name.ilike(f'%{name_project}%'))
    
    if not projects.all():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No projects found.'
        )
    
    return projects.all()

def get_project_by_user_and_id_service(id: int, user: UserModel, db: Session) :
    project = db.query(ProjectModel).join(ProjectMemberModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == id, ProjectModel.is_deleted == False).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not found project with ID {id}'
        )
    
    return project
    
    
def update_project_service(id: int, user: UserModel, update_project: UpdateProject, db: Session):

    project = db.query(ProjectModel).join(ProjectMemberModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == id, ProjectModel.is_deleted == False).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not found project with ID {id} in your project list'
        )
    
    existed_project = db.query(ProjectModel).filter(ProjectModel.name == update_project.name, ProjectModel.id != id).first()
        
    if existed_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This project is existed'
        )
    
    
    role_user = db.query(ProjectMemberModel.role).join(ProjectModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == id).scalar()
    
    if role_user != 'OWNER':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can perform this function."
        )
    
    for key, values in update_project.model_dump(exclude_unset=True).items():
        setattr(project, key, values)
        
    db.commit()
    db.refresh(project)
    
    return project

def soft_delete_project_service(id: int, user: UserModel, db: Session):
    project = db.query(ProjectModel).join(ProjectMemberModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == id, ProjectModel.is_deleted == False).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not found project with ID {id} in your project list'
        )
        
    role_user = db.query(ProjectMemberModel.role).join(ProjectModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == id).scalar()
        
    if role_user != 'OWNER':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can perform this function."
        )
    project.deleted_at = datetime.now()
    project.is_deleted = True
    
    db.commit()
    
    return None

