from restaurant.utils.response import ApiResponse
from restaurant.serializers import UserSerializer, UserInsertSerializer
from rest_framework.viewsets import ViewSet
from restaurant.services.user_service import UserService
from restaurant.injector.app_module import AppModule
from injector import Injector

container = Injector([AppModule()])

class UserViews(ViewSet):
    def get_user_service(self):
        return container.get(UserService)

    def get_user_by_id(self, request, user_id):
        user_service = self.get_user_service()

        user = user_service.get_user_by_id(user_id)
        if user is None:
            return ApiResponse.not_found('User', 'id', user_id)
        
        user_data = UserSerializer(user).data

        return ApiResponse.found(user_data, 'User', 'id', user_id)
    
    
    def get_user_by_email(self, request, email):
        user_service = self.get_user_service()

        user = user_service.get_user_by_email(email)
        if user is None:
            return ApiResponse.not_found('User', 'email', email)
        
        user_data = UserSerializer(user).data

        return ApiResponse.found(user_data, 'User', 'email', email)


    def get_all_users(self, request):
        user_service = self.get_user_service()

        users = user_service.get_all_users()
        user_data = UserSerializer(users, many=True).data
        return ApiResponse.ok(user_data, 'All users succesfully fetched')


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

        return ApiResponse.created(user_data, "user successfully created")


    def delete_user_by_id(self, request, user_id):
        user_service = self.get_user_service()

        is_user_deleted = user_service.delete_user_by_id(user_id)
        if not is_user_deleted:
            return ApiResponse.not_found(f'user', 'ID', user_id)
        
        return ApiResponse.deleted('user')
