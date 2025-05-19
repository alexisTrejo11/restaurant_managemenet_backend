from dependency_injector import containers, providers
from authorization.infrastructure.session.django_session_service import DjangoSessionService
from authorization.application.usecase.login_use_case import LoginUseCase
from authorization.application.usecase.signup_use_case import SignUpUseCase
from authorization.application.usecase.logout_user_case import LogoutUseCase
from users.application.service.user_validator_service import UserValidator
from users.infrastructure.reposiitories.DjangoUserRepository import DjangoUserRepository

class AuthContainer(containers.DeclarativeContainer):
    """Container with providers."""
    # Repository
    user_repository = providers.Singleton(DjangoUserRepository)
    
    # Service
    session_service = providers.Singleton(DjangoSessionService)

    user_validator = providers.Factory(
        UserValidator,
        user_repository=user_repository,
    )

    login_use_case = providers.Factory(
        LoginUseCase,
        user_repository=user_repository,
        session_service=session_service
    )

    signup_use_case = providers.Factory(
        SignUpUseCase,
        user_validation_service=user_validator,
        user_repository=user_repository,
        session_service=session_service
    )

    logout_use_case = providers.Factory(
        LogoutUseCase,
        user_repository=user_repository,
        session_service=session_service
    )