from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..serializers import StockTransactionSerializer as TransactionSerializer
from ..services.stock_transaction_service import StockTransactionService as TransactionService
from shared.response.django_response import DjangoResponseWrapper as ResponseWrapper 
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_transaction(request):
    user_id = request.user.id
    logger.info(f"User {user_id} is requesting to register a stock transaction")

    serializer = TransactionSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)

    transaction = TransactionService.process_transaction(serializer.validated_data)

    logger.info(f"Transaction ID: {transaction.id} for Stock {transaction.stock.id} created successfully by user {user_id}.")

    transaction_serialized = TransactionSerializer(transaction)
    return ResponseWrapper.created(
        data=transaction_serialized.data,
        entity="Stock Transaction"
    )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_transaction(request, transaction_id):
    user_id = request.user.id
    logger.info(f"User {user_id} is requesting to update stock transaction {transaction_id}")

    serializer = TransactionSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)

    existing_transaction = TransactionService.get_transaction(transaction_id)
    transaction_updated = TransactionService.update_transaction(existing_transaction, serializer.validated_data)

    logger.info(f"Transaction ID: {transaction_updated.id} for Stock {transaction_updated.stock.id} updated successfully by user {user_id}.")
    
    transaction_serialized = TransactionSerializer(transaction_updated)
    return ResponseWrapper.updated(
        data=transaction_serialized.data,
        entity="Stock Transaction"
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_transaction(request, transaction_id):
    user_id = request.user.id
    logger.info(f"User {user_id} is requesting to delete stock transaction {transaction_id}")

    transaction_to_delete = TransactionService.get_transaction(transaction_id)
    TransactionService.delete_transaction(transaction_to_delete)

    logger.info(f"Transaction ID: {transaction_id} deleted successfully by user {user_id}.")

    return ResponseWrapper.deleted(
        entity="Stock Transaction"
    )