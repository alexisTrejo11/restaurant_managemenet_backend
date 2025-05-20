from ...domain.ports.input.use_case import UseCase
from ...domain.ports.output.user_repository import UserRepository
from ..dto.user_response import UserResponse
from ..dto.user_request import UpdateUserRequestModel, CreateUserRequestModel
from ...domain.entities.user import User, UserRole, Gender
from ..service.user_validator_service import UserValidator

class CreateUserUseCase(UseCase):
    def __init__(self, user_repository: UserRepository, user_validator : UserValidator):
        self.user_repository = user_repository
        self.validator_service = user_validator
    
    def execute(self, request: CreateUserRequestModel) -> None:
        self.validator_service.validate_creation_unique_values(request)
        
        # Add Mapper
        user = User(
            username=request.username,
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            role=UserRole(request.role),
            gender=Gender(request.gender),
            birth_date=request.birth_date,
            phone_number=request.phone_number,
        )
        
        created_user = self.user_repository.save(user)
    
        return UserResponse.from_entity(created_user)
    
    def _validate_user_creation(self, request: CreateUserRequestModel) -> None:
        User.validate_email(request.email)
        User.validate_phone_number(request.phone_number)
        User.validate_password(request.password)
        
        
class UpdateUserUseCase(UseCase):
    def __init__(self, user_repository: UserRepository, user_validator : UserValidator):
        self.user_repository = user_repository
        self.user_validator = user_validator
    
    def execute(self, user_id: int, request: UpdateUserRequestModel) -> UserResponse:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise (f"User with ID {user_id} not found")
        
        user = self.user_validator.validate_update_unique_values(request, user)
        
        if request.password:
            password_result = User.validate_password(request.password)
            if password_result.is_failure():
                return password_result
            
        if request.first_name:
            user.first_name = request.first_name
        
        if request.last_name:
            user.last_name = request.last_name
        
        if request.gender:
            user.gender = Gender(request.gender)
        
        if request.birth_date:
            user.birth_date = request.birth_date
        
        if request.role:
            user.role = UserRole(request.role)

        updated_user = self.user_repository.save(user)
    
        return UserResponse.from_entity(updated_user)
    
class DeleteUserUseCase(UseCase):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: int) -> None:
        user = self.user_repository.get_by_id(user_id)
        
        self.user_repository.delete(user)    

    
