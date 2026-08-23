from pydantic import BaseModel, ConfigDict
from enum import Enum
from app.models.project_models import RoleProjectMember

class AddNewMember(BaseModel):
    project_id: int
    user_id: int
    role: RoleProjectMember
    
class ResponseMember(AddNewMember):
    
    model_config = ConfigDict(from_attributes=True)
    


