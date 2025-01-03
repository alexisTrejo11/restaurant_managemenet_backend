from injector import Module, singleton
from restaurant.repository.ingredient_repository import IngredientRepository
from restaurant.services.ingredient_service import IngredientService
from restaurant.repository.stock_repository import StockRepository
from restaurant.services.stock_service import StockService 
from restaurant.repository.table_respository import TableRepository
from restaurant.services.table_service import TableService 
from restaurant.repository.menu_item_repository import MenuItemRepository
from restaurant.services.menu_service import MenuItemService 
from restaurant.repository.reservation_repository import ReservationRepository
from restaurant.services.reservation_service import ReservationService 
from restaurant.repository.order_repository import OrderRepository
from restaurant.services.order_service import OrderService 
from restaurant.repository.payment_repository import PaymentRepository
from restaurant.services.payment_service import PaymentService 

class AppModule(Module):
    def configure(self, binder):
        #Ingredient
        binder.bind(IngredientRepository, to=IngredientRepository, scope=singleton)
        binder.bind(IngredientService, to=IngredientService, scope=singleton)

        #Stock
        binder.bind(StockRepository, to=StockRepository, scope=singleton)
        binder.bind(StockService, to=StockService, scope=singleton)

        #Table
        binder.bind(TableRepository, to=TableRepository, scope=singleton)
        binder.bind(TableService, to=TableService, scope=singleton)

        #Menu Item
        binder.bind(MenuItemRepository, to=MenuItemRepository, scope=singleton)
        binder.bind(MenuItemService, to=MenuItemService, scope=singleton)

        # Reservation
        binder.bind(ReservationRepository, to=ReservationRepository, scope=singleton)
        binder.bind(ReservationService, to=ReservationService, scope=singleton)

        # Order
        binder.bind(OrderRepository, to=OrderRepository, scope=singleton)
        binder.bind(OrderService, to=OrderService, scope=singleton)

        # Payment
        binder.bind(PaymentRepository, to=PaymentRepository, scope=singleton)
        binder.bind(PaymentService, to=PaymentService, scope=singleton) 
