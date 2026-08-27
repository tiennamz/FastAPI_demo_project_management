from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class CreateProject(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: Optional[str] = None
    
class ResponseProject(CreateProject):
    id: int
    owner_id: int
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class UpdateProject(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None