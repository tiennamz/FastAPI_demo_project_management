from app.services.project_member_services import add_new_member_service, delete_member_service, get_all_member_service
from fastapi import APIRouter, Depends, Request, status
from app.utils.response import create_response, BaseResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.dependencies.middleware import get_current_user
from app.models.user_model import UserModel
from app.schemas.project_member_schemas import NewMember, ProjectWithMembersResponse, ResponseMember
    
    
    
    
router = APIRouter(prefix='/projects', tags=['Project members'])

@router.post('/{project_id}/members', response_model=BaseResponse[ProjectWithMembersResponse], status_code=status.HTTP_201_CREATED)
def add_member(request: Request, project_id: int, members: list[NewMember], user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    project = add_new_member_service(project_id, members, user, db)
    
    return create_response(
        request,
        status.HTTP_201_CREATED,
        'Success',
        project
    )

@router.delete('/{project_id}/members/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_member(request: Request, project_id: int, user_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    member = delete_member_service(project_id, user_id, user, db)
    
    return create_response(
        request,
        status.HTTP_204_NO_CONTENT,
        'Success'
    )
    
@router.get('/{project_id}/members', response_model=BaseResponse[list[ResponseMember]])
def get_all_member(request: Request, project_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    members = get_all_member_service(project_id, user, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        members
    )
    
    