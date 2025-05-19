from datetime import datetime
from injector import inject
from typing import List, Optional
from ...domain.entities.stock import Stock, StockTransaction
from ...application.repositories.stock_transaction import StockTransactionRepository

class StockTransactionService:
    @inject
    def __init__(self, transaction_repository: StockTransactionRepository):
        self.transaction_repository = transaction_repository

    def get_transaction_by_id(self, stock_id: int) -> Optional[StockTransaction]:
        return self.transaction_repository.get_transaction_by_id(stock_id)
    
    def get_today_transactions(self) -> List[StockTransaction]:
        now = datetime.now()
        tomorrow_day = now.day + 1
        start_of_current_day = datetime(now.year, now.month, now.day, 0, 0, 0, 0)
        start_of_next_day = datetime(now.year, now.month, tomorrow_day, 0, 0, 0, 0)

        return self.transaction_repository.get_transaction_by_date_range(
            start_date=start_of_current_day, 
            end_date=start_of_next_day
        )

    def get_stock_transactions(self, stock: Stock) -> List[StockTransaction]:
        return self.transaction_repository.get_transaction_list_by_stock(stock)

    def update_transaction(self, stock_transaction: StockTransaction, stock: Stock) -> Stock:
        stock.update_transaction(stock_transaction)
        transaction_updated = self.transaction_repository.save_transaction(stock_transaction)
    
        stock.update_transaction(transaction_updated)
        return stock

    def register_transaction(self, stock_transaction: StockTransaction, stock: Stock) -> Stock:
        stock.add_transaction(stock_transaction)
        transaction_created = self.transaction_repository.add_transaction(stock_transaction)

        stock.update_transaction(transaction_created)
        return stock
    

    def delete_transaction(self, stock_transaction: StockTransaction, stock: Stock) -> Stock:
        stock.delete_transaction(stock_transaction)
    
        self.transaction_repository.remove_transaction(stock_transaction)
        
        return stock