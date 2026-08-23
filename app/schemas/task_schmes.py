from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum
from app.models.task_model import StatusEnum, PriorityEnum

class CreateTask(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: StatusEnum
    priority: PriorityEnum
    due_date: str
    
    
class ResopnseTask(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    assignee_id: str
    status: str
    priority: str
    due_date: str
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class UpdateTask(BaseModel):
    project_id: Optional[int]
    title: Optional[str]
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[StatusEnum]
    priority: Optional[PriorityEnum]
    due_date: Optional[str]