from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from datetime import datetime, timedelta

class CustomJWTAuthentication(BaseAuthentication):
    def __init__(self, token=None):
        self.token = token
        self.payload = None
        self.user = None

    def validate_token(self):
        if self.payload:
            return 

        try:
            self.payload = jwt.decode(
                self.token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"],
                audience=settings.JWT_AUDIENCE,
                issuer=settings.JWT_ISSUER
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

    def get_claims(self):
        if not self.payload:
            self.validate_token()
        return self.payload

    def get_user_id(self):
        claims = self.get_claims()
        return claims.get('user_id')

    def get_role(self):
        claims = self.get_claims()
        return claims.get('role')

    def get_expiry_time(self):
        claims = self.get_claims()
        exp = claims.get('exp')
        if exp:
            return datetime.fromtimestamp(exp)
        return None

    def get_issued_at(self):
        claims = self.get_claims()
        iat = claims.get('iat')
        if iat:
            return datetime.fromtimestamp(iat)
        return None

    def check_role(self, allowed_roles):
        user_role = self.get_role()
        if user_role not in allowed_roles:
            raise AuthenticationFailed(f"User does not have the required role. Required: {allowed_roles}, Found: {user_role}")
        return True

    @staticmethod
    def get_bearer_token(request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        raise AuthenticationFailed("Authorization header missing or invalid.")

    def authenticate(self, request):
        pass

    def get_user(self, user_id):
        from restaurant.repository.models.models import UserModel  
        try:
            return UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            raise AuthenticationFailed('User not found')

    @staticmethod
    def generate_token(user_id, role, email, expiration_minutes=60):
        """
        Genera un JWT con el user_id, rol y una fecha de expiración.
        :param user_id: ID del usuario
        :param role: Rol del usuario (por ejemplo, 'admin', 'customer')
        :param expiration_minutes: Tiempo de expiración en minutos (por defecto 60 minutos)
        :return: El token JWT generado
        """
        expiration_time = datetime.now() + timedelta(minutes=expiration_minutes)
        payload = {
            'user_id': user_id,
            'role': role,
            'email': email,
            'exp': expiration_time,
            'iat': datetime.now(),
            'aud': settings.JWT_AUDIENCE,
            'iss': settings.JWT_ISSUER
        }

        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
        return token