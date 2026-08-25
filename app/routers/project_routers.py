from app.services.project_services import create_new_project_service, get_project_by_user_service, get_project_by_user_and_id_service, update_project_service, soft_delete_project_service
from app.services.project_member_services import add_new_member_service, delete_member_service, get_all_member_service
from app.services.task_services import create_new_task_service, get_all_task_of_project_service
from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session
from app.schemas.project_member_schemas import NewMember, ProjectWithMembersResponse, ResponseMember
from app.schemas.project_schemas import CreateProject, ResponseProject, UpdateProject
from app.schemas.task_schmes import CreateTask, ResopnseTask
from app.utils.response import create_response, BaseResponse
from app.models.user_model import UserModel
from app.dependencies.middleware import get_current_user
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

@router.get('/{project_id}', response_model=BaseResponse[ResponseProject])
def get_project_by_user_and_id(request: Request, project_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = get_project_by_user_and_id_service(project_id, user, db)
    
    return create_response(
        request,    
        status.HTTP_200_OK,
        'Success',
        projects
    )
    
@router.patch('/{project_id}')
def update_project(request: Request, project_id: int, update_project: UpdateProject, user: UserModel =Depends(get_current_user), db: Session =Depends(get_db)):
    project = update_project_service(project_id, user, update_project, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        project
    )
    
@router.delete('/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_project(request: Request, project_id: int, user: UserModel =Depends(get_current_user), db: Session = Depends(get_db)):
    project = soft_delete_project_service(project_id, user, db)
    
    return create_response(
        request,
        status.HTTP_204_NO_CONTENT,
        'Success'
    )

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


@router.post('/{project_id}/tasks', status_code=status.HTTP_201_CREATED, response_model=BaseResponse[ResopnseTask])
def create_task(request: Request, project_id: int, new_task: CreateTask, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    task = create_new_task_service(project_id, new_task, user, db)
    
    return create_response(
        request,
        status.HTTP_201_CREATED,
        'Success',
        task
    )   
    
@router.get('/{project_id}/tasks', response_model=BaseResponse[list[ResopnseTask]])
def get_all_task_of_project(request: Request, project_id: int, user: UserModel = Depends(get_current_user), db: Session =Depends(get_db)):
    tasks = get_all_task_of_project_service(project_id, user, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        tasks
    )