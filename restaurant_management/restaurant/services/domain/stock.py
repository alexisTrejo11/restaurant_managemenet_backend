from datetime import datetime

class Stock:
    def __init__(self, 
                 id, 
                 ingredient, 
                 optimal_stock_quantity, 
                 total_stock=0,
                 stock_transactions=None, 
                 created_at=None, 
                 updated_at=None):
        self.__id = id
        self.__ingredient = ingredient
        self.__total_stock = total_stock
        self.__optimal_stock_quantity = optimal_stock_quantity
        self.__stock_transactions = stock_transactions or [] 
        self.__created_at = created_at or datetime.now()
        self.__updated_at = updated_at or datetime.now() 


    @property
    def id(self):
        return self.__id

    @property
    def ingredient(self):
        return self.__ingredient

    @property
    def total_stock(self):
        return self.__total_stock

    @total_stock.setter
    def total_stock(self, value):
        self.__total_stock = value
        self.__updated_at = datetime.now()  # Update timestamp when stock changes

    @property
    def optimal_stock_quantity(self):
        return self.__optimal_stock_quantity

    @optimal_stock_quantity.setter
    def optimal_stock_quantity(self, value):
        self.__optimal_stock_quantity = value

    @property
    def stock_transactions(self):
        return self.__stock_transactions

    @property
    def created_at(self):
        return self.__created_at

    @property
    def updated_at(self):
        return self.__updated_at

    def __str__(self):
        return f'{self.__ingredient.name} - {self.__total_stock} {self.__ingredient.unit}'

    def validate_transaction(self, transaction: "StockTransaction") -> dict:
        if transaction.transaction_type == 'OUT' and not self.is_out_valid(transaction.ingredient_quantity):
            return {"is_valid": False, "message": "Quantity to withdraw exceeds current total stock"}
        if transaction.transaction_type == 'IN' and not self.is_in_valid(transaction.ingredient_quantity):
            return {"is_valid": False, "message": f"Quantity to insert exceeds the allowed limit of {self.__optimal_stock_quantity}"}
        
        return {"is_valid": True, "message": "Transaction is valid"}

    def add_transaction(self, transaction: "StockTransaction"):
        self.adjust_stock(
            ingredient_quantity=transaction.ingredient_quantity if transaction.transaction_type == 'IN' else -transaction.ingredient_quantity
        )

        self.__stock_transactions.append(transaction)

    def is_stock_available(self, quantity: int) -> bool:
        return self.__total_stock >= abs(quantity)

    def adjust_stock(self, ingredient_quantity: int):
        self.__total_stock += ingredient_quantity
        self.__updated_at = datetime.now()

    def is_out_valid(self, ingredient_quantity: int) -> bool:
        """Check if enough stock is available to withdraw."""
        return self.__total_stock >= ingredient_quantity

    def is_in_valid(self, ingredient_quantity: int) -> bool:
        return self.__total_stock + ingredient_quantity <= self.__optimal_stock_quantity

    def clear(self):
        self.__total_stock = 0
        self.__stock_transactions = []


class StockTransaction:
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    def __init__(
        self, 
        ingredient_quantity: int, 
        date: datetime, 
        employee_name: str,
        transaction_type: str, 
        expires_at=None,  
        stock=None  
    ):
        self.__ingredient_quantity = ingredient_quantity
        self.__transaction_type = transaction_type
        self.__date = date
        self.__expires_at = expires_at
        self.__stock = stock
        self.__employee_name = employee_name

    # Encapsulating getter and setter methods for each attribute
    @property
    def ingredient_quantity(self):
        return self.__ingredient_quantity

    @ingredient_quantity.setter
    def ingredient_quantity(self, value):
        self.__ingredient_quantity = value

    @property
    def transaction_type(self):
        return self.__transaction_type

    @transaction_type.setter
    def transaction_type(self, value):
        self.__transaction_type = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def expires_at(self):
        return self.__expires_at

    @expires_at.setter
    def expires_at(self, value):
        self.__expires_at = value

    @property
    def stock(self):
        return self.__stock

    @property
    def employee_name(self):
        return self.__employee_name

    def __str__(self):
        return f'{self.__transaction_type} - {self.__ingredient_quantity}'
