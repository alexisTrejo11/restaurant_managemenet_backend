from restaurant.services.auth_service import AuthService
from restaurant.services.user_service import UserService
from restaurant.serializers import StaffSignupSerializer, LoginSerializer
from rest_framework.viewsets import ViewSet
from restaurant.injector.app_module import AppModule
from injector import Injector
from restaurant.utils.response import ApiResponse
from restaurant.services.domain.user import Role

container = Injector([AppModule()])

class AuthViews(ViewSet):
    def get_auth_service(self):
            return container.get(AuthService)

    def get_user_service(self):
            return container.get(UserService)

    def signup_staff(self, request):
        auth_service = self.get_auth_service()
        user_service = self.get_user_service()

        serializer = StaffSignupSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        credentials_result = auth_service.validate_staff_singup_credentials(serializer.data)
        if credentials_result.is_failure():
            return ApiResponse.bad_request(credentials_result.get_error_msg())
        
        user = user_service.create_user(serializer.data)

        JWT = auth_service.proccess_signup(user)

        return ApiResponse.created(JWT, "Signup Succesfully Proccesed")

    def login(self, request):
        auth_service = self.get_auth_service()

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        credentials_result = auth_service.validate_login_credentials(serializer.data)
        if credentials_result.is_failure():
            return ApiResponse.bad_request(credentials_result.get_error_msg())
        
        JWT = auth_service.proccess_login(credentials_result.get_data())

        return ApiResponse.created(JWT, "Signup Succesfully Proccesed")