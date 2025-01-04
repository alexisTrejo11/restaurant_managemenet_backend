from restaurant.services.domain.user import User
from restaurant.repository.user_repository import UserRepository
from restaurant.mappers.user_mappers import UserMapper
from injector import inject
from restaurant.utils.result import Result
from restaurant.utils.password.password_handler import PasswordService

class UserService:
    @inject
    def __init__(self, user_repository : UserRepository):
        self.user_repository = user_repository
    

    def get_user_by_id(self, user_id):
        return self.user_repository.get_by_id(user_id)
    

    def get_user_by_email(self, email):
        return self.user_repository.get_by_email(email)

    def get_by_phone_number(self, phone_number):
        return self.user_repository.get_by_phone(phone_number)


    def get_all_users(self):
        return self.user_repository.get_all()
    
    def validate_user_creation(self, serilizer_data) -> Result:
        email_result = User.validate_email(serilizer_data.get('email'))
        phone_result = User.validate_phone_number(serilizer_data.get('phone_number'))
        password_result = User.validate_password(serilizer_data.get('password'))

        if email_result.is_failure():
            return email_result

        if phone_result.is_failure():
            return phone_result
    
        if password_result.is_failure():
            return password_result
    
        return Result.success()


    def create_user(self, serializer: dict):
        user = UserMapper.serializer_to_domain(serializer)
        
        hashed_password = PasswordService.hash_password(user.hashed_password)
        user.set_hashed_password(hashed_password)
        
        return self.user_repository.create(user)


    def validate_unique_values(self, serializer_data):
        exists_by_email = self.user_repository.exists_by_email(serializer_data.get('email'))
        exists_by_phone = self.user_repository.exists_by_phone(serializer_data.get('phone_number'))

        if exists_by_email:
            return Result.error("Email already taken")
        elif exists_by_phone:
            return Result.error("Phone number already taken")
        else:
            return Result.success()


    def delete_user_by_id(self, user_id):
        return self.user_repository.delete(user_id)
        