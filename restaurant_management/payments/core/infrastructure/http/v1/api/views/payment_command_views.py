from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from injector import inject
from core.response.django_response import DjangoResponseWrapper
from ......application.use_case.payment_command_use_case import (
    CompletePaymentUseCase,
    UpdateStatusUseCase,
    CancelPaymentUseCase,
)

class PaymentCommandView(viewsets.ViewSet):
    @inject
    def __init__(
        self,
        complete_payment: CompletePaymentUseCase,
        update_status: UpdateStatusUseCase,
        cancel_payment: CancelPaymentUseCase,
        **kwargs
    ):
        self._complete = complete_payment
        self._update = update_status
        self._cancel = cancel_payment
        super().__init__(**kwargs)


    def complete_payment(self, request, pk):
        self._complete.execute(pk)
        return DjangoResponseWrapper.success(message="Payment Successfully Completed")   


    def cancel_payment(self, request, pk):
        self._cancel.execute(pk)
        return DjangoResponseWrapper.success(message="Payment Successfully Cancelled")


    def udpate_payment_status(self, request, status):
        self._update.execute(status)
        return DjangoResponseWrapper.success(message="Payment Status Successfully Updated")      