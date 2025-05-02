from typing import List, Optional
from uuid import UUID
import logging
from django.core.cache import cache
from ....core.exceptions.custom_exceptions import EntityNotFoundException 
from ...domain.ports.input.use_case import UseCase
from ...domain.ports.output.user_repository import UserRepository
from ..dto.user_response import UserResponseModel

logger = logging.getLogger(__name__)


class GetUserByIdUseCase(UseCase):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: UUID) -> UserResponseModel:        
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException("User", user_id) 

        return UserResponseModel.from_entity(user) if user else None


class GetUserByEmailUseCase(UseCase):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, email: str) -> UserResponseModel:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise EntityNotFoundException("User", email) 

        return UserResponseModel.from_entity(user) if user else None


class GetUserByPhoneNumberUseCase(UseCase):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, phone_number: str) -> UserResponseModel:
        user = self.user_repository.get_by_phone(phone_number)
        if not user:
            raise EntityNotFoundException("User", phone_number) 

        return UserResponseModel.from_entity(user) if user else None


class GetAllUsersUseCase(UseCase):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self) -> List[UserResponseModel]:
        users = self.user_repository.get_all()
        
        return [UserResponseModel.from_entity(user) for user in users]
