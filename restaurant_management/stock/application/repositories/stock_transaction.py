from abc import abstractmethod
from ...domain.entities.stock import StockTransaction as Transaction, Stock
from typing import Optional, List
from datetime import datetime

class StockTransactionRepository:
    @abstractmethod
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        pass

    @abstractmethod
    def get_transaction_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        pass

    @abstractmethod
    def get_transactions_by_stock(self, stock: Stock) -> List[Transaction]:
        pass

    @abstractmethod
    def add_transaction(self, transaction : Transaction) -> Transaction:
        pass

    @abstractmethod
    def remove_transaction(self, transaction : Transaction) -> None:
        pass

    @abstractmethod
    def update_transaction(self, transaction : Transaction) -> Transaction:
        pass