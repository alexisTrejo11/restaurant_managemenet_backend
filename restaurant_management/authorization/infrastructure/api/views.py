from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from dataclasses import asdict

# Serializers
from .serializers import StaffSignupSerializer, LoginSerializer

# Use Cases
from ...application.usecase.login_use_case import LoginUseCase
from ...application.usecase.signup_use_case import SignUpUseCase
from ...application.usecase.logout_user_case import LogoutUseCase

# DTOs
from users.application.dto.user_request import CreateUserRequestModel as SignupCredentials

# DI
from dependency_injector.wiring import inject, Provide

# Container
from core.injector.auth_container import AuthContainer

# Response Wrapper
from core.response.django_response import DjangoResponseWrapper


@swagger_auto_schema(method='post', operation_description="Register new staff user")
@api_view(['POST'])
@permission_classes([AllowAny])
@inject
def signup(
    request,
    use_case: SignUpUseCase = Provide[AuthContainer.signup_use_case]
):
    serializer = StaffSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    signup_credentials = SignupCredentials(
        username=data.get('username', data['email']),
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        gender=data['gender'],
        birth_date=data['birth_date'],
        phone_number=data.get('phone_number', None)
    )

    user_session = use_case.execute(signup_credentials)

    return DjangoResponseWrapper.success(
        data=user_session,
        message="Signup Successfully Processed"
    )


@swagger_auto_schema(method='post', operation_description="Login user and get JWT token")
@api_view(['POST'])
@permission_classes([AllowAny])
@inject
def login(
    request,
    use_case: LoginUseCase = Provide[AuthContainer.login_use_case]
):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_session = use_case.execute(serializer.validated_data)

    return DjangoResponseWrapper.success(
        data=user_session,
        message="Login Successfully Processed"
    )


@swagger_auto_schema(method='post', operation_description="Logout user by blacklisting refresh token")
@api_view(['POST'])
@permission_classes([AllowAny])
@inject
def logout(
    request,
    use_case: LogoutUseCase = Provide[AuthContainer.logout_use_case]
):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return DjangoResponseWrapper.bad_request("Refresh token is required")

    try:
        use_case.logout(refresh_token)
        return DjangoResponseWrapper.success(message="Logout Successfully Processed")
    except Exception as e:
        return DjangoResponseWrapper.bad_request(str(e))