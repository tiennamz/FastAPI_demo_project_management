from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class CreateProject(BaseModel):
    name: str = Field(gt=0, lt=20)
    description: str
    
class ResponseProject(CreateProject):
    id: int
    owner_id: int
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class UpdateProject(BaseModel):
    name: Optional[str]
    description: Optional[str]