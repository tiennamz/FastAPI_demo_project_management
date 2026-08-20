from fastapi import FastAPI, status, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    statusCode: int
    message: str
    data: Optional[T]
    error: Optional[Any]
    timestamp: str
    path: str
    

def create_response(request: Request, status_code: int, message: str, data: Any = None, error: Any = None):
    return BaseResponse(
        statusCode=status_code,
        message= message,
        data= jsonable_encoder(data),
        error= error,
        timestamp= datetime.now().isoformat(),
        path= request.url.path
        
    )
    
def handle_exception(app):

    @app.exception_handler(HTTPException)
    def handle_http_exceptin(
        request: Request,
        exc: HTTPException
    ):
        response = create_response(request, status_code=exc.status_code, message='Failed', error=exc.detail)
        
        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump()
        )

    @app.exception_handler(Exception)
    def handle_http_exceptin(
        request: Request,
        exc: Exception
    ):
        response = create_response(request, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Failed', error=str(exc))
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump()
        )

    @app.exception_handler(RequestValidationError)
    def handle_http_exceptin(
        request: Request,
        exc: RequestValidationError
    ):
        response = create_response(request, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Failed', error=exc.errors())
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump()
        )


