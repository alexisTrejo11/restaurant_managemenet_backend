from injector import Module, singleton
from menu.infrastructure.repositories.django_menu_item_repository import DjangoMenuItemRepository as MenuItemRepository 
from menu.application.use_cases.command_menu_items_use_cases import (
    CreateMenuUseCase,
    DeleteMenuUseCase
)
from menu.application.use_cases.query_menu_items_use_cases import (
    GetAllMenusUseCase,
    GetMenuByIdUseCase
)

class AppModule(Module):
    def configure(self, binder):
        #Menu Item
        binder.bind(MenuItemRepository, to=MenuItemRepository, scope=singleton)
        binder.bind(MenuItemRepository, to=CreateMenuUseCase, scope=singleton)
        binder.bind(MenuItemRepository, to=DeleteMenuUseCase, scope=singleton)
        binder.bind(MenuItemRepository, to=GetAllMenusUseCase, scope=singleton)
        binder.bind(MenuItemRepository, to=GetMenuByIdUseCase, scope=singleton)
        
        """
        #Ingredient
        binder.bind(IngredientRepository, to=IngredientRepository, scope=singleton)
        binder.bind(IngredientService, to=IngredientService, scope=singleton)

        #Stock
        binder.bind(StockRepository, to=StockRepository, scope=singleton)
        binder.bind(StockService, to=StockService, scope=singleton)

        #Table
        binder.bind(TableRepository, to=TableRepository, scope=singleton)
        binder.bind(TableService, to=TableService, scope=singleton)

        # Reservation
        binder.bind(ReservationRepository, to=ReservationRepository, scope=singleton)
        binder.bind(ReservationService, to=ReservationService, scope=singleton)

        # Order
        binder.bind(OrderRepository, to=OrderRepository, scope=singleton)
        binder.bind(OrderService, to=OrderService, scope=singleton)

        # Payment
        binder.bind(PaymentRepository, to=PaymentRepository, scope=singleton)
        binder.bind(PaymentService, to=PaymentService, scope=singleton) 

        # User
        binder.bind(UserRepository, to=UserRepository, scope=singleton)
        binder.bind(UserService, to=UserService, scope=singleton) 

        #Auth
        binder.bind(AuthService, to=AuthService, scope=singleton) 
        """
