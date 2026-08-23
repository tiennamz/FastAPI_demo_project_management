from sqlalchemy.orm import Session
from app.core.config import DATABASE_URL
from app.models.project_models import ProjectMemberModel, ProjectModel
from app.models.user_model import UserModel
from app.models.task_model import TaskModel
from datetime import datetime, timedelta

def add_user(db: Session):
    
    try:
        user = UserModel(
            email = 'nva@gmail.com',
            password_hash = 'sdfghjklzxcvbhnjmefghjkl.dfghjkxcvbn.ertyuiofghjk',
            full_name= 'Nguyen Van A',
            role='USER',
            is_active = 1
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
    
    except:
        db.rollback()
        
def add_project(db: Session):
    
    try:
        project = ProjectModel(
            name= 'To do list',
            description= 'Quản lý công việc',
            owner_id = 1
        )
        
        db.add(project)
        db.commit()
        db.refresh(project)
    
    except:
        db.rollback()
        
def add_member(db: Session):
    

    try:
        member = ProjectMemberModel(
            project_id = 1,
            user_id = 1,
            role = 'OWNER'
        )
        
        db.add(member)
        db.commit()
        db.refresh(member)
    
    except:
        db.rollback()
        
def add_task(db: Session):
    

    try:
        task = TaskModel(
            project_id= 1,
            title = 'Hoàn thành frontend',
            description= 'Tối ưu UI/UX',
            assignee_id=1,
            status = 'TODO',
            priority= 'HIGH',
            due_date = datetime.now() + timedelta(days=7)
        )
        
        db.add(task)
        db.commit()
        db.refresh(task)
    
    except:
        db.rollback()
        

