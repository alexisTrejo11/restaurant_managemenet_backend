from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from injector import inject
from core.response.django_response import DjangoResponseWrapper
from ......application.use_case.payment_query_use_case import (
    GetPaymentByIdUseCase,
    GetPaymentByOrderUseCase,
    ListByDateRangeUseCase,
    ListByStatusUseCase
)
from core.utils.dateTimeHandler import DateTimeHandler


class PaymentCommandViews(viewsets.ViewSet):
    @inject
    def __init__(
        self,
        get_payment_by_id_use_case: GetPaymentByIdUseCase,
        get_payment_by_order_use_case: GetPaymentByOrderUseCase,
        list_by_status_use_case: ListByStatusUseCase,
        list_by_date_use_case: ListByDateRangeUseCase,
        **kwargs
    ):
        self.get_payment_by_id = get_payment_by_id_use_case
        self.get_payment_by_order = get_payment_by_order_use_case
        self.list_by_status = list_by_status_use_case
        self.list_by_date = list_by_date_use_case
        super().__init__(**kwargs)

    def retrieve(self, request, pk=None):
        payment = self.get_payment_by_id.execute(pk)
        return DjangoResponseWrapper.found(data=payment.to_dict(), entity="Payment")

    @action(detail=False, methods=['get'], url_path='by-order/(?P<order_id>[^/.]+)')
    def by_order(self, request, order_id=None):
        payment = self.get_payment_by_order.execute(order_id)
        return DjangoResponseWrapper.found(data=payment.to_dict(), entity="Payment")

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status = request.query_params.get('status')
        if not status:
            return Response(
                {"error": "Parámetro 'status' requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payments = self.list_by_status.execute(status)
        return self._build_list_response(payments)


    @action(detail=False, methods=['get'])
    def by_date(self, request):
        start_date = DateTimeHandler.parse_date_to_ISO_8601(request.query_params.get('start_date'))
        end_date = DateTimeHandler.parse_date_to_ISO_8601(request.query_params.get('end_date'))
        completed = request.query_params.get('only_completed', 'true').lower() == 'true'

        payments = self.list_by_date.execute(start_date, end_date, only_completed=completed)

        return self._build_list_response(payments)
    

    def _build_list_response(self, payments):
        if not payments:
            return DjangoResponseWrapper.success("No payments found")
        return DjangoResponseWrapper.found(
            [p.to_dict() for p in payments], 
            "Payment List"
        )