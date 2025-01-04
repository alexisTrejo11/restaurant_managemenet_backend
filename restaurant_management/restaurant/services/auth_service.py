from datetime import datetime
from restaurant.utils.result import Result
from restaurant.services.user_service import UserService
from restaurant.repository.user_repository import UserRepository
from injector import inject
from rest_framework_simplejwt.tokens import RefreshToken
from restaurant.services.domain.user import User
from restaurant.utils.password.password_handler import PasswordService
from django.core.cache import cache
import hashlib


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


    def validate_login_credentials(self, serializer_data) -> Result:
        identifier_field = serializer_data.get('identifier_field')
        password = serializer_data.get('password')

        # Check Cache
        cache_key = self._generate_login_cache_key(identifier_field, password)
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        # Find User
        user = self._get_user_from_cache_or_service(identifier_field)
        if user is None:
            result = Result.error('User not found with given credentials')
            cache.set(cache_key, result, timeout=600)
            return result

        # Validate password
        if self._validate_password(password, user.hashed_password):
            result = Result.success(user)
        else:
            result = Result.error('Incorrect Password')

        # Save Cache
        cache.set(cache_key, result, timeout=600) 
        return result


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
    

    def _generate_login_cache_key(self, identifier, password):
        hashed_password_key = hashlib.md5(password.encode('utf-8')).hexdigest()
        return f'user_credentials_{identifier}_{hashed_password_key}'


    def _get_user_from_cache_or_service(self, identifier):
            cache_key_user = f'user_{identifier}'
            user = cache.get(cache_key_user)

            if user is None:
                user = self.user_service.get_user_by_email(identifier) or \
                    self.user_service.get_by_phone_number(identifier)

                if user:
                    cache.set(cache_key_user, user, timeout=3600)  # 1 hora de caché

            return user
    

    def _validate_password(self, input_password, hashed_password):
        return PasswordService.verify_password(input_password, hashed_password)
