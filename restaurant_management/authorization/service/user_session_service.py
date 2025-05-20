from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class SessionService:
    @staticmethod
    def delete_session(refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise ValueError(f"Error al cerrar sesión: {str(e)}")

    @staticmethod
    def refresh_session(refresh_token, user):
        """
        Refresca la sesión generando un nuevo access token.
        """
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token

            new_access_token['user_id'] = user.id
            new_access_token['email'] = user.email
            new_access_token['role'] = user.role

            return {
                'refresh_token' : refresh_token,
                'access_token': str(new_access_token),
            }
        except Exception as e:
            raise ValueError(f"Error al refrescar la sesión: {str(e)}")

    @staticmethod
    def create_session(user) -> dict:
        refresh_token = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)

        access_token['user_id'] = user.id
        access_token['email'] = user.email
        access_token['role'] = user.role

        return {
            'refresh_token': str(refresh_token),
            'access_token': str(access_token),
        }
