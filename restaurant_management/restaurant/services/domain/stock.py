from datetime import datetime
from datetime import datetime
from typing import List

class Stock:
    def __init__(self, 
                 id, 
                 ingredient, 
                 optimal_stock_quantity, 
                 total_stock=0,
                 stock_transactions=None, 
                 created_at=None, 
                 updated_at=None):
        self.id = id
        self.ingredient = ingredient
        self.total_stock = total_stock
        self.optimal_stock_quantity = optimal_stock_quantity
        self.stock_transactions = stock_transactions or [] 
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now() 


    def __str__(self):
        return f'{self.ingredient.name} - {self.total_stock} {self.ingredient.unit}'


    def validate_transaction(self, transaction: "StockTransaction") -> dict:
        if transaction.transaction_type == 'OUT' and not self.is_out_valid(transaction.ingredient_quantity):
            return {"is_valid": False, "message": "Quantity to withdraw exceeds current total stock"}
        if transaction.transaction_type == 'IN' and not self.is_in_valid(transaction.ingredient_quantity):
            return {"is_valid": False, "message": f"Quantity to insert exceeds the allowed limit of {self.optimal_stock_quantity}"}
        
        return {"is_valid": True, "message": "Transaction is valid"}


    def add_transaction(self, transaction: "StockTransaction"):
        self.adjust_stock(
            ingredient_quantity=transaction.ingredient_quantity if transaction.transaction_type == 'IN' else -transaction.ingredient_quantity
        )

        self.stock_transactions.append(transaction)
    

    def is_stock_available(self, quantity: int) -> bool:
        """
        Check if the stock is sufficient for the given quantity.
        For withdrawal, ensure total_stock is greater than or equal to the absolute value of quantity.
        """
        return self.total_stock >= abs(quantity)


    def adjust_stock(self, ingredient_quantity: int):
        """Adjust the total stock and update the timestamp."""
        self.total_stock += ingredient_quantity
        self.updated_at = datetime.now()


    def is_out_valid(self, ingredient_quantity: int) -> bool:
        """Check if enough stock is available to withdraw."""
        return self.total_stock >= ingredient_quantity


    def is_in_valid(self, ingredient_quantity: int) -> bool:
        """Check if the incoming stock doesn't exceed the optimal quantity."""
        return self.total_stock + ingredient_quantity <= self.optimal_stock_quantity


    def clear(self):
        """Reset stock to zero and clear transactions."""
        self.total_stock = 0
        self.stock_transactions = []


class StockTransaction:
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    def __init__(
        self, 
        ingredient_quantity: int, 
        date: datetime, 
        employee_name : str,
        transaction_type: str, 
        expires_at=None,  
        stock=None  
    ):
        self.ingredient_quantity = ingredient_quantity
        self.transaction_type = transaction_type
        self.date = date
        self.expires_at = expires_at
        self.stock = stock
        self.employee_name = employee_name


    def __str__(self):
        return f'{self.transaction_type} - {self.ingredient_quantity}'


