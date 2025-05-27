from rest_framework import viewsets 
from rest_framework.permissions import IsAdminUser
from .services.payment_service import PaymentService
from .serializers import PaymentSerializer
from .models import Payment
from shared.response.django_response import DjangoResponseWrapper as ResponseWrapper
from shared.pagination import CustomPagination
import logging

logger = logging.getLogger(__name__)

class PaymentAdminViews(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    #permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

    def get_queryset(self):
        """Apply search filters to the base queryset"""
        queryset = Payment.objects.all()
        query_params = self.request.query_params
        search_params = PaymentService.get_search_params(query_params)
        return Payment.objects.dynamic_search(search_params)

    def list(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous') 
        logger.info(f"User {user_id} is requesting payment list.")
        
        query_params = self.request.query_params
        search_params = PaymentService.get_search_params(query_params)
        applied_filters = PaymentService.get_applied_filter_names(search_params)
        
        queryset = Payment.objects.dynamic_search(search_params)
        page = self.paginate_queryset(queryset)
        
        logger.info(f"Returning {len(page if page else [])} payments with applied filters: {applied_filters}")
        
        serializer = self.get_serializer(page, many=True)
        return ResponseWrapper.found(
            data=serializer.data,
            entity="Payment List",
            metadata={
                "pagination": self.paginator.get_paginated_response({}).data,
                "applied_filters": applied_filters
            }
        )

    def retrieve(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous')
        instance = self.get_object()
        logger.info(f"User {user_id} is requesting details for payment ID: {instance.id}.")
        
        serializer = self.get_serializer(instance).data
        logger.info(f"Returning details for table ID: {instance.id}.")
        return ResponseWrapper.found(
            data=serializer.data,
            entity=f"Payment {instance.id}"
        )
 
    def create(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous') 
        logger.info(f"User {user_id} is requesting to create a Payment.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = PaymentService.create_payment(serializer.validated_data)
        logger.info(f"Payment ID: {payment.id} created successfully.")
        
        serializer = self.get_serializer(payment)
        return ResponseWrapper.created(
            data=serializer.data,
            entity="Payment"
        )
    
    def update(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous') 
        instance = self.get_object()
        logger.info(f"User {user_id} is requesting to update Payment Id {instance.id}.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = PaymentService.update_payment(instance, serializer.validated_data)
        logger.info(f"Payment ID: {payment.id} updated successfully.")
        
        serializer = self.get_serializer(payment)
        return ResponseWrapper.created(
            data=serializer.data,
            entity=f"Payment {payment.id}",
        )
    
    def destroy(self, request, *args, **kwargs):
        user_id = getattr(request.user, 'id', 'Anonymous') 
        instance = self.get_object()
        payment_id = instance.id
        is_hard_delete = self.request.query_params.get("hard_delete", False)

        logger.info(f"User {user_id} is requesting to delete Payment Id {payment_id}.")
        PaymentService.delete_payment(instance, hard_delete=is_hard_delete)

        return ResponseWrapper.deleted(f"Payment {payment_id}")