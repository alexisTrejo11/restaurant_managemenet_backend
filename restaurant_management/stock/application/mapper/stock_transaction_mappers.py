from ...domain.entities.stock import Stock, StockTransaction
from ...infrastructure.persistence.models.stock_model import StockTransactionModel, StockModel
from .ingredient_mappers import IngredientMappers
from ..dto.stock_response import StockDTO
from dataclasses import asdict
from datetime import datetime

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
    def dictToDomain(request_data: dict) -> StockTransaction:
        return StockTransaction(
            ingredient_quantity=request_data.get("ingredient_quantity"),
            transaction_type=request_data.get("transaction_type"),
            date=request_data.get("date"),
            employee_name=request_data.get('employee_name'),
            expires_at=request_data.get("expires_at")
        )

    @staticmethod
    def domainToModel(domain: StockTransaction, stock_model: StockModel) -> StockTransactionModel:
        return StockTransactionModel(
            ingredient_quantity=domain.ingredient_quantity,
            expires_at=domain.expires_at,
            employee_name=domain.employee_name,
            transaction_type=domain.transaction_type,
            date=domain.date,
            stock=stock_model
        )

    @staticmethod
    def update_model(domain: StockTransaction, model: StockTransactionModel) -> StockTransactionModel:
        model.ingredient_quantity = domain.ingredient_quantity
        model.expires_at = domain.expires_at
        model.employee_name = domain.employee_name
        model.transaction_type = domain.transaction_type
        model.date = domain.date
        return model
    