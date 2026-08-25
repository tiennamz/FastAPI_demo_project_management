from sqlalchemy.orm import Session
from app.models.task_model import TaskModel
from app.models.user_model import UserModel
from app.models.project_models import ProjectMemberModel, ProjectModel
from app.schemas.task_schmes import CreateTask
from fastapi import status, HTTPException
from app.schemas.task_schmes import CreateTask, UpdateTask


def create_new_task_service(project_id: int, new_task: CreateTask,  user: UserModel, db: Session):
    project = db.query(ProjectMemberModel).filter(ProjectMemberModel.project_id == project_id, ProjectMemberModel.user_id == user.id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You do not belong to this project.'
        )
    task = TaskModel(
        project_id = project_id,
        title = new_task.title,
        description = new_task.description,
        priority = new_task.priority,
        due_date = new_task.due_date,
        
    )
    
    existed_task = db.query(TaskModel).filter(TaskModel.title == new_task.title, TaskModel.project_id == project_id).first()
    
    if existed_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This task is existed'
        )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task

def get_all_task_of_project_service(pro_id, user: UserModel, db: Session):
    
    project = db.query(ProjectMemberModel).filter(ProjectMemberModel.project_id == pro_id, ProjectMemberModel.user_id == user.id).first()
        
    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You do not belong to this project.'
        )
        
    tasks = db.query(TaskModel).filter(TaskModel.project_id == pro_id).all()
    
    return tasks

def get_task_by_id_service(task_id: int, user: UserModel, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not found task with ID {task_id}'
        )
        
    project = db.query(TaskModel).select_from(TaskModel).join(ProjectModel).join(ProjectMemberModel).filter(ProjectMemberModel.user_id == user.id).first()
        
    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You do not belong to this project.'
        )
        
    return task

def update_task_service(task_id: int, user: UserModel, upd_task: UpdateTask, db: Session):
    
    task = get_task_by_id_service(task_id, user, db)
    
    existed_task = db.query(TaskModel).filter(TaskModel.title == upd_task.title, TaskModel.project_id != task.project_id).first()
        
    if existed_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This task is existed'
        )
    
    if upd_task.assignee_id:
        extisted_member = db.query(ProjectMemberModel).filter(task.project_id == ProjectMemberModel.project_id, upd_task.assignee_id == ProjectMemberModel.user_id).first()
        existed_user = db.query(UserModel).filter(UserModel.id == upd_task.assignee_id).first()
        if not extisted_member or not existed_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='This user not belong to project'
            )
    
    role_user = db.query(ProjectMemberModel.role).join(ProjectModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == task.project_id).scalar()
        
    if role_user != 'OWNER':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can perform this function."
        )
        
    for key, value in upd_task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
        
    db.commit()
    db.refresh(task)
    
    return task

def delete_task_service(task_id: int, user: UserModel, db: Session):
    task = get_task_by_id_service(task_id, user, db)
    
    role_user = db.query(ProjectMemberModel.role).join(ProjectModel).filter(ProjectMemberModel.user_id == user.id, ProjectModel.id == task.project_id).scalar()
    
    if role_user != 'OWNER':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can perform this function."
        )

    db.delete(task)
    db.commit()
    
    return task

def search_task_service(db: Session, user: UserModel, status: str = None, priority: str = None, assignee: int = None, title: str = None):
    tasks = (
        db.query(TaskModel)
        .select_from(TaskModel)
        .join(ProjectModel, TaskModel.project_id == ProjectModel.id)
        .join(ProjectMemberModel, ProjectModel.id == ProjectMemberModel.project_id)
        .filter(ProjectMemberModel.user_id == user.id)
    )    
    if status:
        tasks = tasks.filter(TaskModel.status == status)
        
    if priority:
        tasks = tasks.filter(TaskModel.priority == priority)
        
    if assignee:
        tasks = tasks.filter(TaskModel.assignee == assignee)
        
    if title:
        tasks = tasks.filter(TaskModel.title.ilike(f'%{title}%'))
        
    return tasks.all()
        
        
def sort_task_service(user: UserModel, db: Session, limit: int = 2, offset: int = 2):
    tasks = (
            db.query(TaskModel)
            .select_from(TaskModel)
            .join(ProjectModel, TaskModel.project_id == ProjectModel.id)
            .join(ProjectMemberModel, ProjectModel.id == ProjectMemberModel.project_id)
            .filter(ProjectMemberModel.user_id == user.id)
            .order_by(TaskModel.created_at.desc())
            .limit(limit).offset(offset)
        ).all()
    return tasks