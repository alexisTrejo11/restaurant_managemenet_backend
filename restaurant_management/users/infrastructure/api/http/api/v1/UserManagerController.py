from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from core.injector.app_module import AppModule
from injector import Injector
from core.utils.permission import RoleBasedPermission
from core.response.django_response import DjangoResponseWrapper
from ......application.dto.user_response import UserResponse 
from ......application.use_case.use_case_query_impl import (
    GetAllUsersUseCase,
    GetUserByEmailUseCase,
    GetUserByIdUseCase,
    GetUserByPhoneNumberUseCase,
)

container = Injector([AppModule()])

class UserAdminManager(ViewSet):
    def __init__(self, **kwargs):
        self.get_all_user_use_case = container.get(GetAllUsersUseCase)
        self.get_user_by_id_use_case = container.get(GetUserByIdUseCase)
        self.get_user_by_email_use_case = container.get(GetUserByEmailUseCase)
        self.get_user_by_phone_number_use_case = container.get(GetUserByPhoneNumberUseCase)
        super().__init__(**kwargs)

    def get_permissions(self):
        return [RoleBasedPermission(['admin'])]

    def list(self, request):
        """
        Overrides the default list method to retrieve all users.
        """
        users = self.get_all_user_use_case.execute()
        users_response = [UserResponse.from_entity(user).to_dict() for user in users]
        return DjangoResponseWrapper.found(
            data=users_response,
            entity='User',
            message='All users retrieved successfully'
        )

    def retrieve(self, request, pk=None):
        """
        Overrides the default retrieve method to get a user by ID.
        """
        if pk is None:
            return DjangoResponseWrapper.bad_request(
                errors={'detail': 'User ID is required for retrieval.'},
                entity='User'
            )
        
        user_response = self.get_user_by_id_use_case.execute(user_id=pk)
        
        user_data = user_response.to_dict()
        return DjangoResponseWrapper.found(
            data=user_data,
            entity='User',
            param='ID',
            value=pk
        )

    def get_by_email(self, request, email=None):
        """
        Retrieves a user by their email address.
        """
        if email is None:
            return DjangoResponseWrapper.bad_request(message = 'Email address is required.')
        
        user = self.get_user_by_email_use_case.execute(email=email)
        user_response = user.to_dict()
        
        return DjangoResponseWrapper.found(
            data=user_response,
            entity='User',
            param='email',
            value=email
        )

    def get_by_phone(self, request, phone_number=None):
        """
        Retrieves a user by their phone number.
        """
        if phone_number is None:
            return DjangoResponseWrapper.bad_request(message= 'Phone number is required.')
        
        user = self.get_user_by_phone_number_use_case.execute(phone_number=phone_number)
        user_response = user.to_dict()
        
        return DjangoResponseWrapper.found(
            data=user_response,
            entity='User',
            param='phone_number',
            value=phone_number
        )