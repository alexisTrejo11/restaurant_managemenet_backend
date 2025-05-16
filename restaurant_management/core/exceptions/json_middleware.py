from django.http import JsonResponse
from django.conf import settings
import sys
import traceback
from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response

class JSONExceptionMiddleware:
    """
    Middleware que intercepta todas las excepciones y las convierte en respuestas JSON.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as exc:
            # Capturar cualquier excepción y transformarla en JSON
            return self.process_exception(request, exc)

    def process_exception(self, request, exception):
        """
        Procesa la excepción y devuelve una respuesta JSON.
        Este método se asegura de que todas las excepciones se manejen correctamente,
        independientemente de si están en el contexto de DRF o no.
        """
        # Determinar el código de estado HTTP
        status_code = 500
        if hasattr(exception, 'status_code'):
            status_code = exception.status_code
        
        # Formato de respuesta común para errores
        error_data = {
            'error': {
                'type': exception.__class__.__name__,
                'message': str(exception),
                'code': status_code,
            }
        }
        
        # Añadir detalles del traceback en modo DEBUG
        if settings.DEBUG:
            error_data['error']['traceback'] = traceback.format_exc()
        
        # Devolver una respuesta JsonResponse (para Django normal)
        return JsonResponse(error_data, status=status_code)