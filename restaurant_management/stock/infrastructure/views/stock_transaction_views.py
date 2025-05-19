#Django
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from core.response.django_response import DjangoResponseWrapper
# Use Case
from ...application.use_case.stock_transaction_use_case import (
    RegisterStockMovementUseCase,
    AdjustStockMovementUseCase,
    DeleteStockMovementUseCase
) 
# utils
from ...application.mapper.stock_mappers import StockMappers
from ...serializers import StockTransactionInsertSerializer

# Inject
from dependency_injector.wiring import inject, Provide
from core.injector.stock_container import StockTransactionContainer as TransactionContainer

@inject
@api_view(['POST'])
def register_stock_transaction(
    request, 
    usecase: RegisterStockMovementUseCase = Provide[TransactionContainer.register_transaction_use_case]
    ):
    serializer = StockTransactionInsertSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    transaction_details = usecase.execute(serializer.data)

    return DjangoResponseWrapper.created(
        data=StockMappers.dto_to_dict(transaction_details),
        entity='Stock Transaction'
    )

@inject
@api_view(['PUT'])
def adjust_stock_transaction(
    request, 
    usecase: AdjustStockMovementUseCase = Provide[TransactionContainer.adjust_transaction_use_case]
    ):
    serializer = StockTransactionInsertSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    transaction_details = usecase.execute(serializer.data)

    return DjangoResponseWrapper.updated(
        data=StockMappers.dto_to_dict(transaction_details),
        entity='Stock Transaction'
    )

@inject
@api_view(['PUT'])
def adjust_stock_transaction(
    request, 
    transaction_id,
    usecase: DeleteStockMovementUseCase = Provide[TransactionContainer.delete_transaction_use_case]
    ):
    usecase.execute(transaction_id)

    return DjangoResponseWrapper.deleted(
        entity='Stock Transaction'
    )
