from restaurant.serializers import StaffSignupSerializer, LoginSerializer
from rest_framework.viewsets import ViewSet
from core.injector.app_module import AppModule
from injector import Injector
from drf_yasg.utils import swagger_auto_schema

container = Injector([AppModule()])

class AuthViews(ViewSet):
    @swagger_auto_schema(
        operation_description="Signup staff user",
        responses={
            201: "JWT token with successful signup",
            400: "Bad Request (Validation error)"
        }
    )
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

        signup_token = auth_service.proccess_signup(user)

        return ApiResponse.created(signup_token, "Signup Successfully Processed")


    @swagger_auto_schema(
        operation_description="Login user and get JWT",
        responses={
            201: "JWT token with successful login",
            400: "Bad Request (Validation error)"
        }
    )
    def login(self, request):
        auth_service = self.get_auth_service()

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        credentials_result = auth_service.validate_login_credentials(serializer.data)
        if credentials_result.is_failure():
            return ApiResponse.bad_request(credentials_result.get_error_msg())
        
        login_token = auth_service.proccess_login(credentials_result.get_data())

        return ApiResponse.created(login_token, "Login Successfully Processed")
