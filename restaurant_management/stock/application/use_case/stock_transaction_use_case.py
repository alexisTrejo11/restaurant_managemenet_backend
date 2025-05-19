from injector import inject
from ..service.stock_transaction_service import StockTransactionService
from ..service.stock_service import StockService
from ...domain.exceptions.stock_exceptions import *
from ..dto.stock_response import StockDTO
from ..mapper.stock_transaction_mappers import StockTransactionMappers


    # TODO: MAP AND CREATE DTO 
class TransactionQueryUseCase:
    @inject
    def __init__(self, transaction_service: StockTransactionService, stock_service: StockService):
        self.transaction_service = transaction_service
        self.stock_service = stock_service

    def get_by_id(self, stock_id: int) -> StockDTO:
        stock = self.transaction_service.ger_transaction_by_id(stock_id)
        if not stock:
            raise StockTransactionNotFound("Stock Not Found")

        return stock

    def get_today_transactions(self) -> list:
        return self.transaction_service.get_today_transactions()

    def get_transaction_history(self, stock_id) -> list:
        stock = self.stock_service.get_stock_by_id(stock_id, raise_exception=True)
        transactions = self.transaction_service.get_stock_transactions(stock)
        return transactions

class RegisterStockMovementUseCase:
    @inject
    def __init__(self, transaction_service: StockTransactionService, stock_service: StockService):
        self.transaction_service = transaction_service
        self.stock_service = stock_service

    def execute(self, transaction_data: dict) -> StockDTO:
        stock_id = transaction_data.get('stock_id')
        stock = self.stock_service.get_stock_by_id(stock_id, raise_exception=True)
        
        new_transacion = StockTransactionMappers.dictToDomain(transaction_data)

        updated_stock = self.transaction_service.register_transaction(new_transacion, stock)
        
        return updated_stock
    

class AdjustStockMovementUseCase:
    @inject
    def __init__(self, transaction_service: StockTransactionService, stock_service: StockService):
        self.transaction_service = transaction_service
        self.stock_service = stock_service

    def execute(self, transaction_data: dict) -> StockDTO:
        stock_id = transaction_data.get('stock_id')
        stock = self.stock_service.get_stock_by_id(stock_id, raise_exception=True)
        
        new_transacion = StockTransactionMappers.dictToDomain(transaction_data)

        updated_stock = self.transaction_service.update_transaction(new_transacion, stock)
        
        return updated_stock
    

"""FIX"""
class DeleteStockMovementUseCase:
    @inject
    def __init__(self, transaction_service: StockTransactionService, stock_service: StockService):
        self.transaction_service = transaction_service
        self.stock_service = stock_service

    def execute(self, stock_id) -> StockDTO:
        stock = self.stock_service.get_stock_by_id(stock_id, raise_exception=True)
        
        new_transacion = StockTransactionMappers.dictToDomain(None)
        self.transaction_service.delete_transaction(new_transacion, stock)
