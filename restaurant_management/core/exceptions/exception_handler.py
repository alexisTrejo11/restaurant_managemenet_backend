from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Manejador global de excepciones personalizado para DRF.
    Este manejador es específico para vistas de DRF.
    """
    # Llamar primero al manejador por defecto de DRF
    response = drf_exception_handler(exc, context)
    
    # Si la respuesta es None, es una excepción no manejada por DRF
    if response is None:
        # Manejar excepciones personalizadas
        if hasattr(exc, 'status_code'):
            error_data = {
                'error': {
                    'type': exc.__class__.__name__,
                    'message': str(exc),
                    'code': exc.status_code,
                }
            }
            return Response(error_data, status=exc.status_code)
        
        # Manejar cualquier otra excepción como error 500
        error_data = {
            'error': {
                'type': 'InternalServerError',
                'message': 'Ocurrió un error inesperado en el servidor',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        }
        return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if hasattr(response, 'data'):
        response.data = {
            'error': {
                'type': exc.__class__.__name__,
                'message': response.data.get('detail', str(exc)),
                'code': response.status_code,
            }
        }
    
    return response