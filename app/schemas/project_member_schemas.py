from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class NewMember(BaseModel):
    user_id: int
    
class ResponseMember(NewMember):
    project_id: int
    role: str
    model_config = ConfigDict(from_attributes=True)
    


class ProjectWithMembersResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    members: List[ResponseMember] 
    
    model_config = ConfigDict(from_attributes=True)