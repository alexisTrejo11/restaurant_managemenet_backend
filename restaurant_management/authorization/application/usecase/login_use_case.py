from ....users.domain.ports.output.user_repository import UserRepository
from typing import Dict
from django.contrib.auth.hashers import check_password
from ..session.session_service import SessionService
from users.domain.entities.user import User
from ..session.user_session import UserSession

class LoginUseCase:
    def __init__(self, user_repository: UserRepository, sesion_service: SessionService):
        self.user_repository = user_repository
        self.session_service = sesion_service
    
    def execute(self, login_credentials: Dict) -> UserSession:
        password = login_credentials.get('password')
        
        user = self.__find_user(login_credentials)
        self.__check_password(password)

        # Update Last Login

        return self.session_service.create_session(user)
    
    def __find_user(self,  login_credentials: Dict) -> User:
        identifier_field = login_credentials.get('identifier_field')
        password = login_credentials.get('password')

        if not identifier_field or not password:
            raise ValueError("Identifier and password are required")

        user = self.user_repository.get_by_email(identifier_field)
        
        if not user:
            user = self.user_repository.get_by_phone(identifier_field)

        if not user:
            raise ValueError("User Not Found With Given Credentials")

        return user

    def __check_password(self, user: User, raw_password: str) -> None:
        if not check_password(raw_password, user.password):
            raise ValueError("Invalid password")