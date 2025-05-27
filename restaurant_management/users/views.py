import logging
from rest_framework import generics, permissions
from .models import User
from .serializers import UserCreateUpdateSerializer, UserResponseSerializer
from .service.user_service import UserService
from shared.response.django_response import DjangoResponseWrapper
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        admin = request.user
        logger.info(f"Admin {admin.id} init creation of user.")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserService.validate_user_creation(serializer.validated_data)
        user = serializer.save()

        logger.info(
            f"Admin {admin.id} succesfully create new User {user.id}",
            extra={'user_id': user.id, 'admin_id': admin.id}
        )

        response_data = UserResponseSerializer(user).data
        return DjangoResponseWrapper.created(data=response_data, entity="User")
    

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer

    def update(self, request, *args, **kwargs):
            admin = request.user
            user = self.get_object()

            logger.info(
                f"Admin {admin.id} updating user {user.id}. Data: {request.data}",
                extra={'admin_id': admin.id, 'user_id': user.id}
            )

            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            UserService.validate_user_update(
                user_data=serializer.validated_data,
                current_user=user
            )

            updated_user = serializer.save()

            logger.info(
                f"Admin {admin.id} successfully updated user {user.id}",
                extra={'admin_id': admin.id, 'user_id': user.id}
            )

            return DjangoResponseWrapper.updated(
                data=UserResponseSerializer(updated_user).data,
                entity="User",
            )

class UserListAPIView(generics.ListAPIView):
    """
    List all users with pagination.
    Permissions: Admin only (customize as needed)
    """
    queryset = User.objects.all().order_by('-joined_at')
    serializer_class = UserResponseSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = PageNumberPagination 

    def list(self, request, *args, **kwargs):
        admin = request.user
        logger.info(
            f"Admin {admin.id} listing users. Query params: {request.query_params}",
            extra={'admin_id': admin.id}
        )

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer_data = self.get_serializer(queryset, many=True).data
        return DjangoResponseWrapper.found(data=serializer_data, entity="User List")


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Retrieve a single user by ID.
    Permissions: Admin only (customize as needed)
    """
    queryset = User.objects.all()
    serializer_class = UserResponseSerializer
    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        admin = request.user
        user = self.get_object()

        logger.info(
            f"Admin {admin.id} retrieved user {user.id}",
            extra={'admin_id': admin.id, 'user_id': user.id}
        )

        serializer = self.get_serializer(user)
        return DjangoResponseWrapper.found(data=serializer.data, entity="User")
    
class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Soft-delete or hard-delete a user.
    Permissions: Admin only (customize as needed)
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        admin = request.user
        user = self.get_object()

        logger.warning(
            f"Admin {admin.id} initiating deletion of user {user.id}",
            extra={'admin_id': admin.id, 'user_id': user.id}
        )

        user.is_active = False
        user.save()

        # Hard delete: user.delete()
        logger.info(
            f"Admin {admin.id} successfully deleted user {user.id}",
            extra={'admin_id': admin.id, 'user_id': user.id}
        )

        return DjangoResponseWrapper.deleted("User")
