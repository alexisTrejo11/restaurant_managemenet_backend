from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.utils.permission import RoleBasedPermission
from core.response.django_response import DjangoResponseWrapper

# Application
from ....application.dto.user_response import UserResponse
from ....application.use_case.user_query_use_case import (
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    GetUserByEmailUseCase,
    GetUserByPhoneNumberUseCase,
)

# DI
from dependency_injector.wiring import inject, Provide
from core.injector.user_container import UserContainer

# Permiso personalizado (Fix)
admin_only = permission_classes([RoleBasedPermission(['admin'])])

import logging
logger = logging.getLogger(__name__)


# Injection Does Not Work :(

@admin_only
@api_view(['GET'])
def list_users(request):
    """
    Retrieves all users.
    """
    usecase = UserContainer.list_users_use_case()
    users = usecase.execute()
    users_response = [UserResponse.from_entity(user).to_dict() for user in users]
    
    return DjangoResponseWrapper.found(
        data=users_response,
        entity='User List'    
    )


@admin_only
@api_view(['GET'])
def get_user_by_id(request, pk):
    """
    Retrieves a user by ID.
    """
    use_case = UserContainer.get_user_by_id_use_case()
    if not pk:
        return DjangoResponseWrapper.bad_request(
            errors={'detail': 'User ID is required for retrieval.'},
            entity='User'
        )
    
    user_response = use_case.execute(user_id=pk)
    return DjangoResponseWrapper.found(
        data=user_response.to_dict(),
        entity='User',
        param='ID',
        value=pk
    )

@admin_only
@api_view(['GET'])
def get_user_by_email(request, email):
    use_case = UserContainer.get_user_by_email_use_case()
    
    if not email:
        return DjangoResponseWrapper.bad_request(message='Email address is required.')
    
    user = use_case.execute(email=email)
    return DjangoResponseWrapper.found(
        data=user.to_dict(),
        entity='User',
        param='email',
        value=email
    )


@admin_only
@api_view(['GET'])
def get_user_by_phone(request, phone_number):
    """
    Retrieves a user by phone number.
    """
    use_case = UserContainer.get_user_by_phone_use_case()
    if not phone_number:
        return DjangoResponseWrapper.bad_request(message='Phone number is required.')
    

    user = use_case.execute(phone_number=phone_number)
    return DjangoResponseWrapper.found(
        data=user.to_dict(),
        entity='User',
        param='phone_number',
        value=phone_number
    )