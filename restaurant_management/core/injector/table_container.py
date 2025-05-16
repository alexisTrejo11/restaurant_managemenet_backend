from dependency_injector import containers, providers
from orders.infrastructure.repositories.django_table_repository import DjangoTableRepository

from orders.application.use_case.table_command_use_cases import (
    CreateTableUseCase,
    UpdateTableUseCase,
    DeleteTableUseCase,
    SetTableAsAvailableUseCase,
    SetTableAsUnavailableUseCase,
)
from orders.application.use_case.table_query_use_cases import (
    GetAllTablesUseCase,
    GetTableByIdUseCase
)

class TableContainer(containers.DeclarativeContainer):
    """Container with providers."""

    table_repository = providers.Singleton(DjangoTableRepository)
    
    get_table_by_id = providers.Factory(
        GetTableByIdUseCase,
        table_repository=table_repository
    )
    
    set_table_as_available = providers.Factory(
        SetTableAsAvailableUseCase,
        table_repository=table_repository
    )
    
    set_table_as_unavailable = providers.Factory(
        SetTableAsUnavailableUseCase,
        table_repository=table_repository
    )

    get_all_tables = providers.Factory(
        GetAllTablesUseCase,
        table_repository=table_repository
    )
    
    create_table = providers.Factory(
        CreateTableUseCase,
        table_repository=table_repository
    )

    update_table = providers.Factory(
        UpdateTableUseCase,
        table_repository=table_repository
    )
    
    delete_table = providers.Factory(
        DeleteTableUseCase,
        table_repository=table_repository
    )