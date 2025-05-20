from typing import Optional, List
from core.utils.password.password_handler import PasswordService
from django.core.exceptions import ObjectDoesNotExist
from ...domain.entities.user import User, UserRole
from ...models import UserModel
from ...domain.ports.output.user_repository import UserRepository
from ...application.mappers.user_mappers import UserMappers

class DjangoUserRepository(UserRepository):
    def get_by_id(self, user_id: int) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(id=user_id)
            return UserMappers.modelToDomain(user_model)
        except ObjectDoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(email=email)
            return UserMappers.modelToDomain(user_model)
        except ObjectDoesNotExist:
            return None

    def get_by_phone(self, phone_number: str) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(phone_number=phone_number)
            return UserMappers.modelToDomain(user_model)
        except ObjectDoesNotExist:
            return None

    def get_all(self) -> List[User]:
        user_models = UserModel.objects.all()
        return [UserMappers.modelToDomain(model) for model in user_models]

    def save(self, user: User) -> User:
        if user.id:   
            try:
                user_model = UserModel.objects.get(id=user.id)
                # Update existing user
                user_model.username = user.username
                user_model.email = user.email
                user_model.first_name = user.first_name
                user_model.last_name = user.last_name
                user_model.role = user.role.value
                user_model.gender = user.gender.value
                user_model.password = PasswordService.hash_password(user.password)
                user_model.birth_date = user.birth_date
                user_model.phone_number = user.phone_number
                user_model.last_login = user.last_login
                user_model.is_active = user.is_active
                
                user_model.save()
                
                return UserMappers.modelToDomain(user)
            except UserModel.DoesNotExist:
                raise ValueError('User Not Found') 
        else:
            user_model = UserMappers.domainToModel(user)
            
            user_model.password = PasswordService.hash_password(user.password)
            user_model.is_superuser = user_model.role is UserRole.ADMIN.value
            user_model.is_staff = user_model.role is (UserRole.STAFF.value or UserRole.ADMIN.value)
            
            user_model.save()
            
            return UserMappers.modelToDomain(user)

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
