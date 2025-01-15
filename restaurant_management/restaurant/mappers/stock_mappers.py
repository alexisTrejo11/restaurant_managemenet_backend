from restaurant.services.domain.stock import Stock, StockTransaction
from restaurant.models import StockModel, StockTransactionModel
from restaurant.mappers.ingredient_mappers import IngredientMappers

class StockMappers:
     @staticmethod
     def modelToDomain(model: StockModel) -> Stock:
        transactions = [
            StockTransactionMappers.modelToDomain(transaction) 
            for transaction in model.transactions.all()
        ]
        
        return Stock(
            id=model.id,
            ingredient=IngredientMappers.modelToDomain(model.ingredient),
            total_stock=model.total_stock,
            optimal_stock_quantity=model.optimal_stock_quantity,
            stock_transactions=transactions,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

     @staticmethod
     def domainToModel(domain: Stock) -> StockModel:    
        return StockModel(
            id=domain.id,
            ingredient=IngredientMappers.domainToModel(domain.ingredient),
            total_stock=domain.total_stock,
            optimal_stock_quantity=domain.optimal_stock_quantity,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )


class StockTransactionMappers:
    @staticmethod
    def modelToDomain(model: StockTransactionModel) -> StockTransaction:
        return StockTransaction(
            ingredient_quantity=model.ingredient_quantity,
            expires_at=model.expires_at,
            employee_name=model.employee_name,
            transaction_type=model.transaction_type,
            date=model.date
        )


    @staticmethod
    def domainToModel(domain: StockTransaction) -> StockTransactionModel:
        stock = StockMappers.domainToModel(domain=domain.stock)
        
        return StockTransactionModel(
            ingredient_quantity=domain.ingredient_quantity,
            expires_at=domain.expires_at,
            employee_name=domain.employee_name,
            transaction_type=domain.transaction_type,
            date=domain.date,
            stock=stock
        )


    @staticmethod
    def serializerToDomain(serializer) -> StockTransaction:
        return StockTransaction(
            ingredient_quantity=serializer.get("ingredient_quantity"),
            transaction_type=serializer.get("transaction_type"),
            date=serializer.get("date"),
            employee_name=serializer.get('employee_name'),
            expires_at=serializer.get("expires_at")
        )
