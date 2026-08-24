from app.services.project_services import create_new_project_service, get_project_by_user_service, get_project_by_user_and_id_service, update_project_service, soft_delete_project_service
from fastapi import APIRouter, Request, Depends, status
from app.schemas.project_schemas import CreateProject, ResponseProject, UpdateProject
from app.utils.response import create_response, BaseResponse
from app.models.user_model import UserModel
from app.dependencies.middleware import get_current_user
from sqlalchemy.orm import Session
from app.database.database import get_db

router = APIRouter(prefix='/projects', tags=['Projects'])

@router.post('', response_model=BaseResponse[ResponseProject], status_code=status.HTTP_201_CREATED)
def create_new_project(request: Request,new_project: CreateProject, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    project = create_new_project_service(user, new_project, db)
    
    return create_response(
        request, 
        status.HTTP_201_CREATED,
        'Success',
        project
    )

@router.get('/', response_model=BaseResponse[list[ResponseProject]])
def get_project_by_user(request: Request, name_project: str = None, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = get_project_by_user_service(user, db, name_project)
    
    return create_response(
        request, 
        status.HTTP_200_OK,
        'Success',
        projects
    )

@router.get('/{id}', response_model=BaseResponse[ResponseProject])
def get_project_by_user_and_id(request: Request, id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = get_project_by_user_and_id_service(id, user, db)
    
    return create_response(
        request,    
        status.HTTP_200_OK,
        'Success',
        projects
    )
    
@router.patch('/{id}')
def update_project(request: Request, id: int, update_project: UpdateProject, user: UserModel =Depends(get_current_user), db: Session =Depends(get_db)):
    project = update_project_service(id, user, update_project, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        project
    )
    
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_project(request: Request, id: int, user: UserModel =Depends(get_current_user), db: Session = Depends(get_db)):
    project = soft_delete_project_service(id, user, db)
    
    return create_response(
        request,
        status.HTTP_204_NO_CONTENT,
        'Success'
    )