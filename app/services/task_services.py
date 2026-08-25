from sqlalchemy.orm import Session
from app.models.task_model import TaskModel
from app.models.user_model import UserModel
from app.schemas.task_schmes import CreateTask
from fastapi import status, HTTPException


def create_new_task_service(project_id: int, user: UserModel, db: Session):
    pass