from typing import Dict, Any
from ...domain.entities.user import User
from ...models import UserModel
from ..dto.user_response import UserResponse
from ...domain.valueobjects.user_roles import UserRole
from ...domain.valueobjects.gender import Gender

class UserMappers:
    @staticmethod
    def dictToDomain(user_data: Dict[str, Any]) -> User:
        try:
            return User(
                id=user_data.get('id'),
                username=user_data.get('username'),
                email=user_data.get('email'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                role=UserRole(user_data.get('role')),
                gender=Gender(user_data.get('gender', Gender.NOT_SPECIFIED.value)),
                password=user_data.get('password'),
                birth_date=user_data.get('birth_date'),
                phone_number=user_data.get('phone_number'),
                joined_at=user_data.get('joined_at'),
                last_login=user_data.get('last_login'),
                is_active=user_data.get('is_active', True),
            )
        except ValueError as e:
            raise ValueError(f"Error mapping dictionary to User domain: {e}")

    @staticmethod
    def domainToModel(user: User) -> UserModel:
        return UserModel(
            id=str(user.id),
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            gender=user.gender.value,
            password=user.password,
            birth_date=user.birth_date,
            role=user.role.value,
            joined_at=user.joined_at,
            last_login=user.last_login,
            phone_number=user.phone_number,
            is_active=user.is_active,
        )

    @staticmethod
    def modelToDomain(user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            role=UserRole(user_model.role),
            gender=Gender(user_model.gender),
            password=user_model.password,
            birth_date=user_model.birth_date,
            phone_number=user_model.phone_number,
            joined_at=user_model.joined_at,
            last_login=user_model.last_login,
            is_active=user_model.is_active,
        )

    @staticmethod
    def domainToResponse(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role.value,
            gender=user.gender.value,
            birth_date=user.birth_date,
            phone_number=user.phone_number,
            joined_at=user.joined_at,
            last_login=user.last_login,
            is_active=user.is_active,
        )