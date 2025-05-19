from users.models import UserModel
from users.domain.valueobjects.gender import Gender
from users.domain.valueobjects.user_roles import UserRole as Role
from users.domain.entities.user import User
from typing import Optional, List
from datetime import datetime

class UserMapper:
    @staticmethod
    def serializer_to_domain(serilizer : dict) -> User:
        return User(
            first_name=serilizer.get('first_name'),
            last_name=serilizer.get('last_name'),
            gender=Gender(serilizer.get('gender')),
            email=serilizer.get('email'),
            password=serilizer.get('password'),
            birth_date=serilizer.get('birth_date'),
            role=Role(serilizer.get('role')),
            joined_at=datetime.now(),
            last_login=datetime.now(),
            phone_number=serilizer.get('phone_number')
        )


    @staticmethod
    def to_domain(user_model: UserModel) -> User:
        return User(
            id=user_model.id if user_model.id else None,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            gender=Gender(user_model.gender),
            email=user_model.email,
            password=user_model.password,
            birth_date=user_model.birth_date,
            role=Role(user_model.role),
            joined_at=user_model.joined_at,
            last_login=user_model.last_login,
            phone_number=user_model.phone_number
        )

    @staticmethod
    def to_model(user: User) -> UserModel:
        return UserModel(
            id=user.id if user.id else None,
            first_name=user.first_name,
            last_name=user.last_name,
            gender=user.Gender,
            email=user.email,
            password=user.password,
            birth_date=user.birth_date,
            role=user.role.value,
            joined_at=user.joined_at,
            last_login=user.last_login,
            phone_number=user.phone_number
        )

    @staticmethod
    def to_domain_list(user_models: List[UserModel]) -> List[User]:
        return [UserMapper.to_domain(user_model) for user_model in user_models]

    @staticmethod
    def update_model(user_model: UserModel, user: User) -> UserModel:
        user_model.first_name = user.first_name
        user_model.last_name = user.last_name
        user_model.gender = user.gender.value
        user_model.email = user.email
        user_model.password = user.password
        user_model.birth_date = user.birth_date
        user_model.role = user.role.value
        user_model.last_login = user.last_login
        user_model.phone_number = user.phone_number
        return user_model