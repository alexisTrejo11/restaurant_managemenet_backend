from .serializers import StaffSignupSerializer, LoginSerializer
from rest_framework.viewsets import ViewSet
from core.injector.app_module import AppModule
from injector import Injector
from users.serializers import StaffSignupSerializer
from core.response.django_response import DjangoResponseWrapper
from ...application.usecase.login_use_case import LoginUseCase
from ...application.usecase.signup_use_case import SignUpUseCase
from ...application.usecase.logout_user_case import LogoutUseCase
from ....users.application.dto.user_request import CreateUserRequestModel as SignupCredentials
from dataclasses import asdict


from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from drf_yasg.utils import swagger_auto_schema

container = Injector([AppModule()])

class AuthViews(ViewSet):
    def __init__(self, **kwargs):
        self.login_use_case = container.get(LoginUseCase)
        self.signup_use_case = container.get(SignUpUseCase)
        self.logout_use_case = container.get(LogoutUseCase)
        super().__init__(**kwargs)


    @swagger_auto_schema(
        operation_description="Signup staff user",
        responses={
            201: "JWT token with successful signup",
            400: "Bad Request (Validation error)"
        }
    )
    def signup(self, request):
        serializer = StaffSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data 
        signupCredentials = SignupCredentials(
            username=data.get('username', data['email']),
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            gender=data['gender'],
            birth_date=data['birth_date'],
            phone_number=data.get('phone_number', None)
        )
        
        userSession = self.signup_use_case.execute(signupCredentials)
        
        return DjangoResponseWrapper.success(
            data=asdict(userSession), 
            message="Signup Succesfully Proccesed"
        )


    @swagger_auto_schema(
        operation_description="Login user and get JWT",
        responses={
            201: "JWT token with successful login",
            400: "Bad Request (Validation error)"
        }
    )
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_session = self.login_use_case.execute(**serializer.data)

        return DjangoResponseWrapper.success(
            data=asdict(user_session), 
            message="Login Successfully Processed"
        )


    def log_out(self, request, refresh_token):
        self.logout_use_case.logout(refresh_token)

        return DjangoResponseWrapper.success(
            message="Logout Successfully Proccesed"
        )