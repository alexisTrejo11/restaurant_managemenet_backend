from restaurant.models import Stock, Ingredient, StockTransaction
from restaurant.serializers import StockInsertSerializer, StockSerializer
from restaurant.utils.result import Result
from django.db import transaction
from restaurant.dtos.stock_dtos import StockUpdateDTO

class StockService:
    @staticmethod
    def get_stock_by_ingredient_id(ingredient_id):
        stock_result = StockService._get_stock_by_ingredient_id(ingredient_id)
            
        # The validation of an existing ingredient is not handled here, if stock not 
        # founded with ingredient id is cause is not created yet
        if stock_result.is_failure():
            return Result.error(f'Stock with ingredient Id {ingredient_id} not initialized yet')
        else:
            return Result.success(stock_result.get_data())

    @staticmethod
    def get_stock_by_id(stock_id):
        try:
            stock = Stock.objects.get(pk=stock_id)
            return Result.success(stock)
        except Stock.DoesNotExist:
            return Result.error(f'Stock with Id {stock_id} not found')

    @staticmethod
    def init_stock(ingredient, optimal_quantity):
        stock = Stock(
            ingredient=ingredient,
            current_quantity=0,
            optimal_quantity=optimal_quantity,
        )
        stock.save()
        stock_serializer = StockSerializer(stock)
        return stock_serializer.data

    @staticmethod
    def update_stock(data):
        ingredient_id = data.get('ingredient_id')
        update_status =  data.get('update_status')
        quantity =  data.get('quantity')

        stock_result = StockService._get_stock_by_ingredient_id(ingredient_id)
        if stock_result.is_failure():
            return Result.error(stock_result.get_error_msg())

        stock = stock_result.get_data()

        if update_status == 'IN':
            return StockService._increase_stock(stock, quantity)
        elif update_status == 'OUT':
            return StockService._decrease_stock(stock, quantity)
        else:
            return Result.error('Invalid update status')

        
    @staticmethod
    def delete_stock_by_ingredient_id(ingredient_id):
        stock_result = StockService._get_stock_by_ingredient_id(ingredient_id)
        if stock_result.is_failure():
            return Result.error(stock_result.get_error_msg())

        stock = stock_result.get_data()
        stock.delete()

        return Result.success(None)

    @staticmethod
    def validate_stock_creation(ingredient_id):
        try:
            stock = Stock.objects.select_related('ingredient').get(ingredient__id=ingredient_id)
            return Result.error('Ingredient already has a stock')
        except Stock.DoesNotExist:
            return Result.success(None)

    @staticmethod
    def _get_stock_by_ingredient_id(ingredient_id):
        try:
            stock = Stock.objects.select_related('ingredient').get(ingredient__id=ingredient_id)
            return Result.success(stock)
        except Stock.DoesNotExist:
            return Result.error(f'Stock for ingredient ID {ingredient_id} not found')

    @staticmethod
    def _increase_stock(stock, quantity):
        stock.increase_current_quantity(quantity)
        return StockService._save_stock(stock, 'IN')

    @staticmethod
    def _decrease_stock(stock, quantity):
        try:
            stock.decrease_current_quantity(quantity)
            return StockService._save_stock(stock, 'OUT')
        except Exception as e:
            return Result.error(str(e))

    @staticmethod
    def _save_stock(stock, stock_update):
        with transaction.atomic():
            stock.save()
            StockTransaction.objects.create(stock=stock, stock_update=stock_update)
        return Result.success(None)
