from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from enum import Enum
from datetime import datetime
from app.models.task_model import StatusEnum, PriorityEnum

class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum
    due_date: datetime
    
    
class ResopnseTask(BaseModel):
    id: int
    project_id: int
    title: str  
    description: str
    assignee_id: Any
    status: str
    priority: str
    comment: Any
    attachment: Any
    due_date: str
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class UpdateTask(BaseModel):
    title: Optional[str]
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[StatusEnum]
    priority: Optional[PriorityEnum]
    due_date: Optional[datetime]