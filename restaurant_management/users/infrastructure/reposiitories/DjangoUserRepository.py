from abc import abstractmethod
from typing import Optional, List
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from ...domain.entities.user import User, UserRole, Gender
from ...models import UserModel
from ...domain.ports.output.user_repository import UserRepository

class DjangoUserRepository(UserRepository):
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(id=user_id)
            return self._map_model_to_entity(user_model)
        except ObjectDoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(email=email)
            return self._map_model_to_entity(user_model)
        except ObjectDoesNotExist:
            return None

    def get_by_phone(self, phone_number: str) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(phone_number=phone_number)
            return self._map_model_to_entity(user_model)
        except ObjectDoesNotExist:
            return None

    def get_all(self) -> List[User]:
        user_models = UserModel.objects.all()
        return [self._map_model_to_entity(model) for model in user_models]

    def save(self, user: User) -> User:
        try:
            user_model = UserModel.objects.get(id=user.id)
            # Update existing user
            user_model.username = user.username
            user_model.email = user.email
            user_model.first_name = user.first_name
            user_model.last_name = user.last_name
            user_model.role = user.role.value
            user_model.gender = user.gender.value
            user_model.password = user.password
            user_model.birth_date = user.birth_date
            user_model.phone_number = user.phone_number
            user_model.last_login = user.last_login
            user_model.is_active = user.is_active
            user_model.save()
            return user
        except ObjectDoesNotExist:
            # Create a new user
            user_model = UserModel(
                id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role.value,
                gender=user.gender.value,
                password=user.password,
                birth_date=user.birth_date,
                phone_number=user.phone_number,
                joined_at=user.joined_at,
                last_login=user.last_login,
                is_active=user.is_active,
            )
            user_model.save()
            return user

    def delete(self, user: User) -> bool:
        try:
            user_model = UserModel.objects.get(id=user.id)
            user_model.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def exists_by_email(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()

    def exists_by_phone(self, phone_number: str) -> bool:
        return UserModel.objects.filter(phone_number=phone_number).exists()

    def _map_model_to_entity(self, user_model: UserModel) -> User:
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

    def _map_entity_to_model(self, user: User) -> UserModel:
        return UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role.value,
            gender=user.gender.value,
            password=user.password,
            birth_date=user.birth_date,
            phone_number=user.phone_number,
            joined_at=user.joined_at,
            last_login=user.last_login,
            is_active=user.is_active,
        )