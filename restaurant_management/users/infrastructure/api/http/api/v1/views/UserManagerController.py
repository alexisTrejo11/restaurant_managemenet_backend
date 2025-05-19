from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from core.injector.app_module import AppModule
from injector import Injector
from core.utils.permission import RoleBasedPermission
from core.response.django_response import DjangoResponseWrapper
from .......application.dto.user_response import UserResponse 
from .......application.use_case.use_case_query_impl import (
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
    
"""
from common.utils.response import ApiResponse
from restaurant.serializers import UserSerializer, UserInsertSerializer
from rest_framework.viewsets import ViewSet
from .application.service.user_service import UserService
from common.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema

container = Injector([AppModule()])

class UserViews(ViewSet):
    def get_permissions(self):
        return [RoleBasedPermission(['admin'])]

    def get_user_service(self):
        return container.get(UserService)

    @swagger_auto_schema(
        operation_description="Get user by ID",
        responses={
            200: UserSerializer,
            404: "User not found"
        }
    )
    def get_user_by_id(self, request, user_id):
        user_service = self.get_user_service()

        user = user_service.get_user_by_id(user_id)
        if not user:
            return ApiResponse.not_found('User', 'ID', user_id)
        
        user_data = UserSerializer(user).data
        return ApiResponse.found(user_data, 'User', 'ID', user_id)


    @swagger_auto_schema(
        operation_description="Get user by email",
        responses={
            200: UserSerializer,
            404: "User not found"
        }
    )
    def get_user_by_email(self, request, email):
        user_service = self.get_user_service()

        user = user_service.get_user_by_email(email)
        if not user:
            return ApiResponse.not_found('User', 'email', email)
        
        user_data = UserSerializer(user).data
        return ApiResponse.found(user_data, 'User', 'email', email)


    @swagger_auto_schema(
        operation_description="Get all users",
        responses={
            200: UserSerializer(many=True),
        }
    )
    def get_all_users(self, request):
        user_service = self.get_user_service()

        users = user_service.get_all_users()
        user_data = UserSerializer(users, many=True).data
        return ApiResponse.ok(user_data, 'All users successfully fetched')


    @swagger_auto_schema(
        operation_description="Create a new user",
        responses={
            201: UserSerializer,
            400: "Bad Request (Validation error)",
            409: "Conflict (Unique value error)"
        }
    )
    def create_user(self, request):
        user_service = self.get_user_service()

        serializer = UserInsertSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        validation_result = user_service.validate_unique_values(serializer.data)
        if validation_result.is_failure():
            return ApiResponse.conflict(validation_result.get_error_msg())

        user_result = user_service.validate_user_creation(serializer.data)
        if user_result.is_failure():
            return ApiResponse.bad_request(user_result.get_error_msg())

        user = user_service.create_user(serializer.data)
        
        user_data = UserSerializer(user).data
        return ApiResponse.created(user_data, "User successfully created")


    @swagger_auto_schema(
        operation_description="Delete user by ID",
        responses={
            200: "User successfully deleted",
            404: "User not found"
        }
    )
    def delete_user_by_id(self, request, user_id):
        user_service = self.get_user_service()

        is_user_deleted = user_service.delete_user_by_id(user_id)
        if not is_user_deleted:
            return ApiResponse.not_found('User', 'ID', user_id)
        
        return ApiResponse.deleted('User')

"""