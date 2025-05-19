from dependency_injector import containers, providers
from stock.infrastructure.persistence.repository.django_stock_repository import DjangoStockRepository
from stock.application.use_case.stock_command_use_case import (
    CreateStockUseCase,
    UpdateStockUseCase,
    DeleteStockUseCase,
    ClearStockUseCase,
)

from stock.application.use_case.stock_query_use_case import (
    GenerateStockReportUseCase,
    GetStockByIdUseCase,
    GetStockByIngredientUseCase,
    GetStockHistoryUseCase,
)

from stock.infrastructure.persistence.repository.django_stock_transaction import DjangoStockTransactionRepository
from stock.application.service.stock_transaction_service import StockTransactionService
from stock.application.service.stock_service import StockService
from stock.application.use_case.stock_transaction_use_case import (
    RegisterStockMovementUseCase,
    AdjustStockMovementUseCase,
    DeleteStockMovementUseCase,
)

from stock.infrastructure.persistence.repository.django_ingredient_repository import DjangoIngredientRepository
from stock.application.use_case.ingredient_use_case import (
    CreateIngredientUseCase,
    GetAllIngredientsUseCase,
    GetIngredientsByIdUseCase,
    UpdateIngredientUseCase,
    DeleteIngredientUseCase
)

class StockContainer(containers.DeclarativeContainer):
    """Container with providers."""

    stock_repository = providers.Singleton(DjangoStockRepository)
    
    create_stock_use_case = providers.Factory(
        CreateStockUseCase,
        stock_repository=stock_repository
    )
    
    update_stock_use_case = providers.Factory(
        UpdateStockUseCase,
        stock_repository=stock_repository
    )
    
    delete_stock_use_case = providers.Factory(
        DeleteStockUseCase,
        stock_repository=stock_repository
    )

    clear_stock_use_case = providers.Factory(
        ClearStockUseCase,
        stock_repository=stock_repository
    )
    
    get_stock_history_use_case = providers.Factory(
        GetStockHistoryUseCase,
        stock_repository=stock_repository
    )

    get_stock_by_ingredient_use_case = providers.Factory(
        GetStockByIngredientUseCase,
        stock_repository=stock_repository
    )

    get_stock_by_id_use_case = providers.Factory(
        GetStockByIdUseCase,
        stock_repository=stock_repository
    )

    generate_stock_use_case = providers.Factory(
        GenerateStockReportUseCase,
        stock_repository=stock_repository
    )


class StockTransactionContainer(containers.DeclarativeContainer):
    """Container with providers."""
    stock_repository = providers.Singleton(DjangoStockRepository)
    stock_transaction_repository = providers.Singleton(DjangoStockTransactionRepository)
    
    stock_transaction_service = providers.Singleton(
        StockTransactionService,
        transaction_repository=stock_transaction_repository
    )
      
    stock_service = providers.Singleton(
        StockService,
        stock_repository=stock_repository
    )

    register_transaction_use_case = providers.Factory(
        RegisterStockMovementUseCase,
        transaction_service=stock_transaction_service,
        stock_service=stock_service
    )

    adjust_transaction_use_case = providers.Factory(
        AdjustStockMovementUseCase,
        transaction_service=stock_transaction_service,
        stock_service=stock_service
    )

    delete_transaction_use_case = providers.Factory(
        DeleteStockMovementUseCase,
        transaction_service=stock_transaction_service,
        stock_service=stock_service
    )
    

class IngredientContainer(containers.DeclarativeContainer):
    ingredient_repository = providers.Singleton(DjangoIngredientRepository)

    get_all_ingredient_use_case = providers.Factory(
        GetAllIngredientsUseCase,
        ingredient_repository=ingredient_repository
    )

    get_ingredient_by_id_use_case = providers.Factory(
        GetIngredientsByIdUseCase,
        ingredient_repository=ingredient_repository
    )

    create_ingredient_use_case = providers.Factory(
        CreateIngredientUseCase,
        ingredient_repository=ingredient_repository
    )

    update_ingredient_use_case = providers.Factory(
        UpdateIngredientUseCase,
        ingredient_repository=ingredient_repository
    )

    delete_ingredient_use_case = providers.Factory(
        DeleteIngredientUseCase,
        ingredient_repository=ingredient_repository
    )