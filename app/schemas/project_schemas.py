from pydantic import BaseModel, ConfigDict
from typing import Optional

class CreateProject(BaseModel):
    name: str
    description: str
    
class ResponseProject(CreateProject):
    id: int
    owner_id: int
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class UpdateProject(BaseModel):
    name: Optional[str]
    description: Optional[str]