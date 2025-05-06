from ..dto.user_request import UpdateUserRequestModel, CreateUserRequestModel
from ...domain.entities.user import User
from ..exceptions.app_excpetions import  UniqueFieldAlreadyTaken

class UserValidator:
    def __init__(self):
        pass

    def validate_creation_unique_values(self, request: CreateUserRequestModel) -> None:
        self.validate_not_duplicated_email(request.email)
        self.validate_not_duplicated_phone(request.phone_number)

    # Move
    def validate_update_unique_values(self, request: UpdateUserRequestModel, user) -> User:
        if request.email and request.email != user.email:
            self.validate_not_duplicated_email(request.email)
            User.validate_email(request.email)
            
            user.email = request.email
        
        if request.phone_number and request.phone_number != user.phone_number:
            self.validate_not_duplicated_phone(request.phone_number)            
            User.validate_phone_number(request.phone_number)
            user.phone_number = request.phone_number

        return user

    def validate_creation_unique_values(self, request: CreateUserRequestModel) -> None:
        self.validateEmail(request.email)

            
    def validate_not_duplicated_email(self, email):
        exists_by_email = self.user_repository.exists_by_email(email)
        if exists_by_email:
            raise UniqueFieldAlreadyTaken("Email already taken")

    def validate_not_duplicated_phone(self, phone_number):
        if phone_number:
            exists_by_phone = self.user_repository.exists_by_phone(phone_number)
            if exists_by_phone:
                raise UniqueFieldAlreadyTaken("Phone number already taken")
