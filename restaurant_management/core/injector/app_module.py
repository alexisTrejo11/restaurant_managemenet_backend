from dependency_injector import containers, providers
from menu.infrastructure.repositories.django_menu_item_repository import DjangoMenuItemRepository
from orders.infrastructure.repositories.django_table_repository import DjangoTableRepository

from menu.application.use_cases.command_menu_items_use_cases import (
    CreateMenuUseCase,
    DeleteMenuUseCase
)
from menu.application.use_cases.query_menu_items_use_cases import (
    GetAllMenusUseCase,
    GetMenuByIdUseCase
)


class AppModule(containers.DeclarativeContainer):
    """Container with providers."""
    # Menu
    menu_repository = providers.Singleton(DjangoMenuItemRepository)
    
    get_menu_by_id_use_case = providers.Factory(
        GetMenuByIdUseCase,
        menu_repository=menu_repository
    )
    
    get_all_menus_use_case = providers.Factory(
        GetAllMenusUseCase,
        menu_repository=menu_repository
    )
    
    create_menus_use_case = providers.Factory(
        CreateMenuUseCase,
        menu_repository=menu_repository
    )
    
    delete_menus_use_case = providers.Factory(
        DeleteMenuUseCase,
        menu_repository=menu_repository
    )
