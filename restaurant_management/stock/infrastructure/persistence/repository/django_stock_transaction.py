from typing import Optional, List
from ....application.repositories.stock_transaction import StockTransactionRepository as TransactionRepository
from ....domain.entities.stock import StockTransaction as Transaction
from ..models.stock_model import StockTransactionModel as TransactionModel
from ....application.mapper.stock_mappers import StockMappers, StockTransactionMappers
from ....domain.entities.stock import Stock

class DjangoStockTransactionRepository(TransactionRepository):
    def __init__(self):
        super().__init__()

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        transaction = self._get_transaction(transaction_id)
        if transaction:
            transaction = StockTransactionMappers.modelToDomain(transaction)
        
        return transaction

    def get_transaction_list_by_stock(self, stock: Stock) -> List[Transaction]:
        stock_model = StockMappers.domainToModel(stock)
        transactions = TransactionModel.objects.filter(stock=stock_model)
        return [
            StockTransactionMappers.modelToDomain(transaction) 
            for transaction in transactions
        ]

    def add_transaction(self, transaction: Transaction) -> Transaction:
        stock_model = StockMappers.domainToModel(transaction.stock)  # Asegúrate de tener 'stock' en el dominio
        transaction_model = StockTransactionMappers.domainToModel(transaction, stock_model)
        transaction_model.save()
        return StockTransactionMappers.modelToDomain(transaction_model)

    def remove_transaction(self, transaction_id: int) -> None:
        transaction_model = self._get_transaction(transaction_id=transaction_id)
        if transaction_model:
            transaction_model.delete()

    def update_transaction(self, transaction_updated: Transaction):
        existing_transaction = self._get_transaction(transaction_id=transaction_updated.id)
        updated_transaction = StockTransactionMappers.update_model(transaction_updated, existing_transaction)
        updated_transaction.save()
        return StockTransactionMappers.modelToDomain(updated_transaction)

    def _get_transaction(self, transaction_id: int) -> TransactionModel:
        try:
            return TransactionModel.objects.get(id=transaction_id)
        except TransactionModel.DoesNotExist:
            return None
