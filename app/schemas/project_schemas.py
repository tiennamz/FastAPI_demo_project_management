from pydantic import BaseModel, ConfigDict
from typing import Optional

class CreateProject(BaseModel):
    name: str
    description: str
    owner_id: int
    
class ResponseProject(CreateProject):
    id: int
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class UpdateProject(BaseModel):
    name: Optional[str]
    description: Optional[str]
    owner_id: Optional[int]