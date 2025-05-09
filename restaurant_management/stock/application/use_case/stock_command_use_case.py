from injector import inject
from ..service.stock_service_impl import StockService
from ...domain.exceptions.stock_exceptions import *
from ..dto.stock_response import StockDTO
from ..mapper.stock_mappers import StockMappers

class CreateStockUseCase:
    @inject
    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def execute(self, stock_data: dict) -> StockDTO:
        """
        Crea un nuevo registro de stock para un ingrediente
        :param ingredient: Ingrediente para el cual se crea el stock
        :param optimal_quantity: Cantidad óptima de stock
        :return: Stock creado
        :raises: DuplicateStockError si ya existe stock para el ingrediente
        """
        try:
            new_stock = StockMappers.dictToDomian(stock_data)
            
            stock_created = self.stock_service.create_stock(new_stock) 
            
            return StockMappers.domain_to_dto(stock_created)
        except DuplicateStockError:
            raise 
        except Exception as e:
            raise StockException(f"Error al crear stock: {str(e)}")


class UpdateStockUseCase:
    @inject
    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def execute(self, stock_id, optimal_quantity=None, is_active=None):
        """
        Actualiza los parámetros de un stock existente
        :param stock_id: ID del stock a actualizar
        :param optimal_quantity: Nueva cantidad óptima (opcional)
        :param is_active: Estado activo/inactivo (opcional)
        :return: Stock actualizado
        :raises: StockNotFoundError si el stock no existe
        """
        try:
            stock = self.stock_service.get_stock_by_id(stock_id)
            
            if optimal_quantity is not None:
                stock.optimal_stock_quantity = optimal_quantity
            
            if is_active is not None:
                stock.is_active = is_active
            
            stock_updated = self.stock_service.update_stock(stock)
            return StockMappers.domain_to_dto(stock_updated)
        except StockNotFoundError:
            raise
        except Exception as e:
            raise StockException(f"Error al actualizar stock: {str(e)}")
        

class DeleteStockUseCase:
    @inject
    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def execute(self, stock_id: int):    
        self.stock_service.delete_stock(stock_id)


class ClearStockUseCase:
    @inject
    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def execute(self, stock_id: int):    
        stock = self.stock_service.clear_stock(stock_id)
        return StockMappers.domain_to_dto(stock)


