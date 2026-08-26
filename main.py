from fastapi import FastAPI, Depends, HTTPException, status, Request
from app.database.database import get_db, Base, engine, SessionLocal
from sqlalchemy.orm import Session
from app.utils.response import handle_exception, create_response
from sqlalchemy import text
from tests.seed import add_member, add_project, add_task, add_user
from app.routers.auth_routers import router as auth_routers
from app.routers.user_routers import router as user_routers
from app.routers.project_routers import router as project_routers
from app.routers.task_routers import router as task_routers
from app.core.config import UPLOAD_DIRECTORY
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title= 'TEAM PROJECT MANAGEMENT API',
    version='1.0.0'
)


handle_exception(app)

Base.metadata.create_all(bind=engine)

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
app.mount('/static', StaticFiles(directory='static'), name='statics')

@app.on_event('startup')
def add_seed():
    db = SessionLocal()
    
    try:
        add_user(db)
        add_project(db)
        add_member(db)
        add_task(db)
        
    except:
        pass
    finally:
        db.close()



@app.get('/health/check', tags=['Check system'])
def check_system(request: Request, db: Session = Depends(get_db)):
    try: 
        db.execute(text('SELECT 1'))
        
        return create_response(
            request,
            status.HTTP_200_OK,
            'Success'
        )
    
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Can't connect to server"
        )
    
    
app.include_router(auth_routers)
app.include_router(user_routers)
app.include_router(project_routers)
app.include_router(task_routers)