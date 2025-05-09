from ...domain.entities.stock import Stock, StockTransaction
from ...infrastructure.models.stock_model import StockModel, StockTransactionModel
from .ingredient_mappers import IngredientMappers
from ..dto.stock_response import StockDTO
from dataclasses import asdict
from datetime import datetime
from .stock_transaction_mappers import StockTransactionMappers

class StockMappers:
    @staticmethod
    def dictToDomian(data: dict) -> Stock:
        return Stock(
            ingredient=data.get('ingredient'),
            optimal_stock_quantity=data.get('optimal_stock')
        )

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
     
    @staticmethod
    def domain_to_dto(stock_domain) -> StockDTO:
        """
        Convierte una instancia de la entidad Stock (de dominio)
        a un objeto DTO plano (StockDTO).
        """
        if not stock_domain:
            return None

        transactions = []
        if stock_domain.stock_transactions:
            for tx in stock_domain.stock_transactions:
                transactions.append(StockTransactionMappers.to_dto(tx))

        return StockDTO(
            id=stock_domain.id,
            ingredient_id=stock_domain.ingredient.id,
            optimal_stock_quantity=stock_domain.optimal_stock_quantity,
            total_stock=stock_domain.total_stock,
            transactions=transactions or [],
            created_at=stock_domain.created_at,
            updated_at=stock_domain.updated_at
        )

    @staticmethod
    def dto_to_dict(stock_dto: StockDTO) -> dict:
        """
        Serializa el DTO a un diccionario (útil para APIs REST).
        """
        dto_dict = asdict(stock_dto)

        # Opcional: formatear fechas
        if dto_dict.get("created_at") and isinstance(dto_dict["created_at"], datetime):
            dto_dict["created_at"] = dto_dict["created_at"].isoformat()

        if dto_dict.get("updated_at") and isinstance(dto_dict["updated_at"], datetime):
            dto_dict["updated_at"] = dto_dict["updated_at"].isoformat()

        return dto_dict
