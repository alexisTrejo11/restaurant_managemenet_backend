from restaurant.services.domain.user import User
from restaurant.repository.user_repository import UserRepository
from common.mappers.user_mappers import UserMapper
from injector import inject
from common.utils.result import Result
from common.utils.password.password_handler import PasswordService
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class UserService:
    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id) -> User:
        cache_key = f'user_{user_id}'
        user = cache.get(cache_key)
        
        if user is None:
            user = self.user_repository.get_by_id(user_id)
            if user:
                cache.set(cache_key, user, timeout=3600)  # 1 hour
        
        return user

    def get_user_by_email(self, email) -> User:
        cache_key = f'user_email_{email}'
        user = cache.get(cache_key)
        
        if user is None:
            user = self.user_repository.get_by_email(email)
            if user:
                cache.set(cache_key, user, timeout=3600)  # 1 hour
        
        return user

    def get_by_phone_number(self, phone_number) -> User:
        cache_key = f'user_phone_{phone_number}'
        user = cache.get(cache_key)
        
        if user is None:
            user = self.user_repository.get_by_phone(phone_number)
            if user:
                cache.set(cache_key, user, timeout=3600)  #  1 hour
        
        return user

    def get_all_users(self) -> list:
        cache_key = 'all_users'
        users = cache.get(cache_key)
        
        if users is None:
            users = self.user_repository.get_all()
            cache.set(cache_key, users, timeout=3600)  # 1 hour
        
        return users

    def validate_user_creation(self, serializer_data) -> Result:
        email_result = User.validate_email(serializer_data.get('email'))
        phone_result = User.validate_phone_number(serializer_data.get('phone_number'))
        password_result = User.validate_password(serializer_data.get('password'))

        if email_result.is_failure():
            return email_result

        if phone_result.is_failure():
            return phone_result

        if password_result.is_failure():
            return password_result

        return Result.success()

    def create_user(self, serializer: dict) -> User:
        user = UserMapper.serializer_to_domain(serializer)
        hashed_password = PasswordService.hash_password(user.password)
        user.set_password(hashed_password)
            
        created_user = self.user_repository.create(user)
        logger.info(f"User with ID {created_user.id} created successfully.")
        cache_key = f'user_{created_user.id}'
        cache.set(cache_key, created_user, timeout=3600)  # 1 hour
        
        return created_user

    def validate_unique_values(self, serializer_data) -> Result:
        exists_by_email = self.user_repository.exists_by_email(serializer_data.get('email'))
        exists_by_phone = self.user_repository.exists_by_phone(serializer_data.get('phone_number'))

        if exists_by_email:
            logger.warning(f"User creation failed: Email {serializer_data.get('email')} already taken.")
            return Result.error("Email already taken")
        elif exists_by_phone:
            logger.warning(f"User creation failed: Phone number {serializer_data.get('phone_number')} already taken.")
            return Result.error("Phone number already taken")
        else:
            logger.info(f"User creation validation for unique values passed successfully.")
            return Result.success()

    def delete_user_by_id(self, user_id: int) -> bool:
        is_deleted = self.user_repository.delete(user_id)
        
        if is_deleted:
            cache_key = f'user_{user_id}'
            cache.delete(cache_key)  
            logger.info(f"User with ID {user_id} deleted successfully.")
        else:
            logger.warning(f"User with ID {user_id} could not be deleted (not found).")
        
        return is_deleted
