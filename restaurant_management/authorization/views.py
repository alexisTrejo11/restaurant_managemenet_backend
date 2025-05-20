
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    SignUpSerializer,
    LoginSerializer
)
from core.response.django_response import DjangoResponseWrapper
from .service.auth_service import AuthService
from .service.user_session_service import SessionService

@swagger_auto_schema(method='post', operation_description="Register new staff user")
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    AuthService.validate_signup_data(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
        password2=serializer.validated_data['password2']
    )

    user = serializer.save()
    user_session = SessionService.create_session(user)

    return DjangoResponseWrapper.success(
        data=user_session,
        message="Signup Successfully Processed"
    )


@swagger_auto_schema(method='post', operation_description="Login user and get JWT token")
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = AuthService.authenticate_user(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password']
    )

    user_session = SessionService.create_session(user)

    return DjangoResponseWrapper.success(
        data=user_session,
        message="Login Successfully Processed"
    )

"""
@swagger_auto_schema(method='post', operation_description="Logout user by blacklisting refresh token")
@api_view(['POST'])
@permission_classes([AllowAny])
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
"""