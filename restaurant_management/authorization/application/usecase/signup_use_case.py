from ....users.application.dto.user_request import CreateUserRequestModel as SignupCredentials
from ....users.application.service.user_validator_service import UserValidator as UserValidatorService
from ....users.domain.ports.output.user_repository import UserRepository
from ..session.session_service import SessionService
from users.domain.entities.user import User, UserRole, Gender

class SignUpUseCase:
    def __init__(
            self, 
            user_validation_service: UserValidatorService, 
            user_repository: UserRepository,
            session_service: SessionService,
        ):
        self.validation_service = user_validation_service
        self.user_repository= user_repository
        self.session_service = session_service

    def execute(self, signup_credentials: SignupCredentials):
        self.validation_service.validate_creation_unique_values(signup_credentials)

        user = User(
            username=signup_credentials.username,
            email=signup_credentials.email,
            first_name=signup_credentials.first_name,
            last_name=signup_credentials.last_name,
            role=UserRole(signup_credentials.role),
            gender=Gender(signup_credentials.gender),
            birth_date=signup_credentials.birth_date,
            phone_number=signup_credentials.phone_number,
                )

        user = self.user_repository.save(user)

        return self.session_service.create_session(user)






