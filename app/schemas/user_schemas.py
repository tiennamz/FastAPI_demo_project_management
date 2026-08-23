from pydantic import BaseModel, ConfigDict

class ResponseUser(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: str
    
