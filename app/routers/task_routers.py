from app.services.task_services import get_task_by_id_service, update_task_service, delete_task_service, search_task_service, sort_task_service, add_comment_task_service
from fastapi import Depends, APIRouter, Request, status
from app.schemas.task_schemas import ResopnseTask, UpdateTask
from app.utils.response import create_response, BaseResponse
from sqlalchemy.orm import Session
from app.dependencies.middleware import get_current_user
from app.models.user_model import UserModel
from app.database.database import get_db

router = APIRouter(prefix='/tasks', tags=['Tasks'])

@router.get('/search', response_model=BaseResponse[list[ResopnseTask]])
def search_task(request: Request, task_status: str = None, priority: str = None, assignee: str = None, title: str = None, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = search_task_service(db, user, task_status, priority, assignee, title)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        tasks
    )

@router.get('/sort', response_model=BaseResponse[list[ResopnseTask]])
def sort_task(request: Request, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db), limit: int = 2, offset: int = 2):
    tasks = sort_task_service(user, db, limit, offset)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        tasks
    )

@router.patch('/{task_id}/comment', response_model=BaseResponse[ResopnseTask])
def add_comment_task(request: Request,task_id: int, comment: str,  user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    task = add_comment_task_service(task_id, user, comment, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        task
    )


@router.get('/{task_id}', response_model=BaseResponse[ResopnseTask])
def get_task_by_id(request: Request, task_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    task = get_task_by_id_service(task_id, user, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        task
    )
    
@router.patch('/{task_id}', response_model=BaseResponse[ResopnseTask])
def update_task(request: Request, task_id: int, update_task: UpdateTask, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    task = update_task_service(task_id, user, update_task, db)
    
    return create_response(
        request,
        status.HTTP_200_OK,
        'Success',
        task
    )

@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    task = delete_task_service(task_id, user, db)
    
    return 

