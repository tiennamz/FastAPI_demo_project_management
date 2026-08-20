from pydantic import BaseModel, ConfigDict
from enum import Enum


class RoleProjectMember(str, Enum):
    OWNER = 'OWNER'
    MEMBER = 'MEMBER'

class AddNewMember(BaseModel):
    project_id: int
    user_id: int
    role: RoleProjectMember
    
class ResponseMember(AddNewMember):
    
    model_config = ConfigDict(from_attributes=True)
    


