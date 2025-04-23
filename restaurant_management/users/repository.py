from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from restaurant.repository.common_repository import CommonRepository
from restaurant.services.domain.user import User
from restaurant.mappers.user_mappers import UserMapper
from restaurant.models import UserModel
from restaurant.utils.exceptions import RepositoryException

class UserRepository(CommonRepository[User]):
    def __init__(self):
        self.mapper = UserMapper()

    @transaction.atomic
    def create(self, entity: User) -> User:
        try:
            user_model = self.mapper.to_model(entity)
            user_model.save()
            return self.mapper.to_domain(user_model)
        except Exception as e:
            raise RepositoryException(f"Error creating user: {str(e)}")

    def get_by_id(self, id: int) -> Optional[User]:
        user_model = UserModel.objects.filter(id=id).first()
        if user_model:
            return self.mapper.to_domain(user_model)

    def get_all(self) -> List[User]:
        user_models = UserModel.objects.all()
        return self.mapper.to_domain_list(user_models)


    @transaction.atomic
    def update(self, entity: User) -> User:
        try:
            if not entity.id:
                raise RepositoryException("Cannot update user without ID")

            try:
                user_model = UserModel.objects.get(id=entity.id)
            except ObjectDoesNotExist:
                raise RepositoryException(f"User with id {entity.id} not found")

            updated_model = self.mapper.update_model(user_model, entity)
            updated_model.save()
            return self.mapper.to_domain(updated_model)
        except Exception as e:
            raise RepositoryException(f"Error updating user: {str(e)}")

    @transaction.atomic
    def delete(self, id: int) -> bool:
        try:
            result = UserModel.objects.filter(id=id).delete()
            return result[0] > 0
        except Exception as e:
            raise RepositoryException(f"Error deleting user: {str(e)}")


    def get_by_email(self, email: str) -> Optional[User]:
            user_model = UserModel.objects.filter(email=email).first()
            if user_model:
                return self.mapper.to_domain(user_model)


    def exists_by_email(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()
    
    def exists_by_phone(self, phone_number: str) -> bool:
        return UserModel.objects.filter(phone_number=phone_number).exists()


    def get_by_phone(self, phone_number: str) -> Optional[User]:
        user_model = UserModel.objects.filter(phone_number=phone_number)
        if user_model:
            return self.mapper.to_domain(user_model)


    def get_by_role(self, role: str) -> List[User]:
        user_models = UserModel.objects.filter(role=role)
        return self.mapper.to_domain_list(user_models)
    
    
    def get_active_users(self) -> List[User]:
        user_models = UserModel.objects.filter(is_active=True)
        return self.mapper.to_domain_list(user_models)