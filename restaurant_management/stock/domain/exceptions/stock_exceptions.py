class StockException(Exception):
    """Excepción base para errores de stock"""
    pass

class StockNotFoundError(StockException):
    """Cuando no se encuentra un stock"""
    pass

class DuplicateStockError(StockException):
    """Cuando ya existe un stock para un ingrediente"""
    pass

class InvalidTransactionError(StockException):
    """Cuando una transacción no es válida"""
    pass

class InsufficientStockError(StockException):
    """Cuando no hay suficiente stock para una operación"""
    pass

class InvalidStockFieldError(StockException):
    """Cuando una propiedad tiene un valor no valido"""
    pass

class StockTransactionException(Exception):
    """Excepción base para errores de stock"""
    pass

class StockTransactionNotFound(StockTransactionException):
    """Excepción base para errores de stock"""
    pass