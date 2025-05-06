from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class DjangoSessionService:
    def __init__(self):
        pass

    def delete_session(self, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise ValueError(f"Error al cerrar sesión: {str(e)}")

    def refresh_session(self, refresh_token):
        """
        Refresca la sesión generando un nuevo access token.
        """
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token

            user_id = refresh.payload.get('user_id')
            user = self.user_service.get_user_by_id(user_id)
            new_access_token['user_id'] = user.id
            new_access_token['email'] = user.email
            new_access_token['role'] = user.role

            return {
                'refresh_token' : refresh_token,
                'access_token': str(new_access_token),
            }
        except Exception as e:
            raise ValueError(f"Error al refrescar la sesión: {str(e)}")


    def create_session(self, user) -> dict:
        refresh_token = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)

        access_token['user_id'] = user.id
        access_token['email'] = user.email
        access_token['role'] = user.role

        return {
            'refresh_token': str(refresh_token),
            'access_token': str(access_token),
        }
