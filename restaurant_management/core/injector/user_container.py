from dependency_injector import containers, providers
from authorization.infrastructure.session.django_session_service import DjangoSessionService
from users.application.use_case.user_command_use_case import (
    CreateUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)
from users.application.use_case.user_query_use_case import (
    GetAllUsersUseCase,
    GetUserByEmailUseCase,
    GetUserByIdUseCase,
    GetUserByPhoneNumberUseCase,
)

from users.application.service.user_validator_service import UserValidator
from users.infrastructure.repositories.DjangoUserRepository import DjangoUserRepository

class UserContainer(containers.DeclarativeContainer):
    """Container with providers."""
    # Repository
    user_repository = providers.Singleton(DjangoUserRepository)
    
    user_validator = providers.Factory(
        UserValidator,
        user_repository=user_repository,
    )

    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        user_repository=user_repository,
        user_validator=user_validator,
    )

    update_user_use_case = providers.Factory(
        UpdateUserUseCase,
        user_repository=user_repository,
        user_validator=user_validator,
    )

    get_user_by_phone_use_case = providers.Factory(
        GetUserByPhoneNumberUseCase,
        user_repository=user_repository,
    )

    delete_user_use_case = providers.Factory(
        DeleteUserUseCase,
        user_repository=user_repository,
    )

    list_users_use_case = providers.Factory(
        GetAllUsersUseCase,
        user_repository=user_repository,
    )

    get_user_by_id_use_case = providers.Factory(
        GetUserByIdUseCase,
        user_repository=user_repository,
    )

    get_user_by_email_use_case = providers.Factory(
        GetUserByEmailUseCase,
        user_repository=user_repository,
    )

    