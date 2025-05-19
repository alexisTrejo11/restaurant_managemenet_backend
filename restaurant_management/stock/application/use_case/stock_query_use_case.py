from injector import inject
from ..service.stock_service import StockService
from ...domain.exceptions.stock_exceptions import *

class GetStockByIdUseCase:
    @inject
    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def execute(self, stock_id, include_transactions=False):
        """
        Obtiene un stock por su ID
        :param stock_id: ID del stock a recuperar
        :param include_transactions: Incluir historial de transacciones
        :return: Stock encontrado
        :raises: StockNotFoundError si no se encuentra el stock
        """
        try:
            stock = self.stock_service.get_stock_by_id(stock_id)
            
            if include_transactions:
                transactions = self.stock_service.get_transactions_by_stock(stock_id)
                stock.transactions = transactions
            
            return stock
            
        except StockNotFoundError:
            raise
        except Exception as e:
            raise StockException(f"Error al obtener stock: {str(e)}")
        

class GetStockByIngredientUseCase:
    @inject
    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def execute(self, stock_id, include_transactions=False):
        """
        Obtiene un stock por su ID
        :param stock_id: ID del stock a recuperar
        :param include_transactions: Incluir historial de transacciones
        :return: Stock encontrado
        :raises: StockNotFoundError si no se encuentra el stock
        """
        try:
            stock = self.stock_service.get_stock_by_id(stock_id)
            
            if include_transactions:
                transactions = self.stock_service.get_transactions_by_stock(stock_id)
                stock.transactions = transactions
            
            return stock
            
        except StockNotFoundError:
            raise
        except Exception as e:
            raise StockException(f"Error al obtener stock: {str(e)}")
        

class ListStocksUseCase:
    @inject
    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def execute(self, active_only=True, low_stock_threshold=None):
        """
        Lista todos los stocks con opciones de filtrado
        :param active_only: Mostrar solo stocks activos
        :param low_stock_threshold: Filtrar por stock bajo (porcentaje del óptimo)
        :return: Lista de stocks
        """
        try:
            stocks = self.stock_service.get_all_stocks(active_only=active_only)
            
            if low_stock_threshold is not None:
                return [
                    stock for stock in stocks 
                    if stock.current_quantity < (stock.optimal_stock_quantity * low_stock_threshold)
                ]
            
            return stocks
        except Exception as e:
            raise StockException(f"Error al listar stocks: {str(e)}")
        


class GetStockHistoryUseCase:
    @inject
    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def execute(self, stock_id, limit=None, date_from=None, date_to=None):
        """
        Obtiene el historial de transacciones de un stock
        :param stock_id: ID del stock
        :param limit: Límite de resultados
        :param date_from: Fecha inicial para filtrar
        :param date_to: Fecha final para filtrar
        :return: Lista de transacciones
        :raises: StockNotFoundError
        """
        try:
            self.stock_service.get_stock_by_id(stock_id)
            
            return self.stock_service.get_transactions_by_stock(
                stock_id=stock_id,
                limit=limit,
                date_from=date_from,
                date_to=date_to
            )
            
        except StockNotFoundError:
            raise
        except Exception as e:
            raise StockException(f"Error al obtener historial: {str(e)}")
        

class GenerateStockReportUseCase:
    @inject
    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def execute(self, report_type='full'):
        """
        Genera un reporte de stock
        :param report_type: Tipo de reporte ('full', 'low', 'critical')
        :return: Diccionario con datos del reporte
        """
        try:
            stocks = self.stock_service.get_all_stocks(active_only=True)
            
            report_data = {
                'total_items': len(stocks),
                'total_value': sum(s.current_quantity * s.ingredient.unit_cost for s in stocks),
                'items': []
            }
            
            for stock in stocks:
                item_data = {
                    'ingredient': stock.ingredient.name,
                    'current': stock.current_quantity,
                    'optimal': stock.optimal_stock_quantity,
                    'status': 'normal'
                }
                
                # Determinar estado
                if stock.current_quantity <= 0:
                    item_data['status'] = 'out_of_stock'
                elif stock.current_quantity < stock.optimal_stock_quantity * 0.2:
                    item_data['status'] = 'critical'
                elif stock.current_quantity < stock.optimal_stock_quantity * 0.5:
                    item_data['status'] = 'low'
                
                # Filtrar según tipo de reporte
                if report_type == 'full' or \
                   (report_type == 'low' and item_data['status'] in ['low', 'critical', 'out_of_stock']) or \
                   (report_type == 'critical' and item_data['status'] in ['critical', 'out_of_stock']):
                    report_data['items'].append(item_data)
            
            return report_data
            
        except Exception as e:
            raise StockException(f"Error al generar reporte: {str(e)}")