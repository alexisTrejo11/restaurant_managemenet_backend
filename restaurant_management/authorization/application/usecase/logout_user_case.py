from rest_framework_simplejwt.tokens import RefreshToken

class LogoutUseCase:
    def __init__(self):
        pass
    
    def logout(self, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise ValueError(f"Error al cerrar sesión: {str(e)}")

    def logout_all():
        pass
    