from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import APIException
from shared.response.django_response import DjangoResponseWrapper as ResponseWrapper

def custom_exception_handler(exc, context):
    """
    Unified exception handler that processes:
    1. Standard DRF exceptions (validation, authentication, etc.)
    2. Custom APIException-based exceptions
    3. All other unhandled exceptions (500 Internal Server Error)
    
    Returns consistent responses using DjangoResponseWrapper.
    """
    response = drf_exception_handler(exc, context)
    
    if response is not None:
        error_data = {
            'type': exc.__class__.__name__,
            'code': getattr(exc, 'default_code', None),
            'details': response.data if isinstance(response.data, dict) else None
        }
        return ResponseWrapper.failure(
            data=error_data,
            message=str(exc.detail) if hasattr(exc, 'detail') else "Request failed",
            status_code=response.status_code
        )
    
    if isinstance(exc, APIException):
        error_data = {
            'type': exc.__class__.__name__,
            'code': getattr(exc, 'default_code', None)
        }
        return ResponseWrapper.failure(
            data=error_data,
            message=str(exc.detail),
            status_code=getattr(exc, 'status_code', 400)
        )
    
    if hasattr(exc, 'status_code'):
        return ResponseWrapper.failure(
            data={'type': exc.__class__.__name__},
            message=str(exc),
            status_code=exc.status_code
        )
    
    return ResponseWrapper.internal_server_error(
        data={'type': 'InternalServerError'},
        message="An unexpected error occurred"
    )