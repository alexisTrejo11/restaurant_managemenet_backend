from datetime import datetime
from restaurant.utils.result import Result
from restaurant.services.user_service import UserService
from restaurant.repository.user_repository import UserRepository
from injector import inject
from rest_framework_simplejwt.tokens import RefreshToken
from restaurant.services.domain.user import User
from restaurant.utils.password.password_handler import PasswordService


class AuthService:
    @inject
    def __init__(self, user_service : UserService, user_repository: UserRepository):
        self.user_service = user_service
        self.user_repository = user_repository

    def validate_staff_singup_credentials(self, serializer_data) -> Result:
        unique_result = self.user_service.validate_unique_values(serializer_data)
        user_format_result = self.user_service.validate_user_creation(serializer_data)

        if unique_result.is_failure():
            return unique_result
        elif user_format_result.is_failure():
            return user_format_result
        else:
            return Result.success()


    def validate_login_credentials(self, serializer_data)-> Result:
        identifier_field = serializer_data.get('identifier_field') # Email or Phone number
        
        user_founded = self.user_service.get_user_by_email(identifier_field)
        if user_founded is None:       
            user_founded = self.user_service.get_by_phone_number(identifier_field)

        if user_founded is None:
            return Result.error('User not found with given credentials')

        is_password_correct = PasswordService.verify_password(serializer_data.get('password'), user_founded.hashed_password)  
        if is_password_correct:
            return Result.success(user_founded)
        else:
            return Result.error('Incorrect Password')


    def proccess_login(self, user: User) -> dict:
        user.update_last_login(datetime.now())

        self.user_repository.update(user)

        return self.__generate_token(user)    


    def proccess_signup(self, user: User) -> dict:
        return self.__generate_token(user)
    

    def __generate_token(self, user: User) -> dict:
        refresh = RefreshToken.for_user(user)

        refresh['id'] = user.id.value
        refresh['email'] = user.email
        refresh['role'] = user.role.value

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }