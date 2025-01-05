from restaurant.utils.response import ApiResponse
from restaurant.serializers import UserSerializer, UserInsertSerializer
from rest_framework.viewsets import ViewSet
from restaurant.services.user_service import UserService
from restaurant.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from restaurant.utils.permission import RoleBasedPermission

container = Injector([AppModule()])

class UserViews(ViewSet):
    # Role Permissions
    def get_permissions(self):
        return [RoleBasedPermission(['admin'])]

    # User Service injection
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
        if user is None:
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
        if user is None:
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
