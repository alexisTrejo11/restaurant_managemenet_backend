from dependency_injector import containers, providers
from reservations.infrastructure.repositories.django_reservation_repository import DjangoReservationRepository
from orders.infrastructure.repositories.django_table_repository import DjangoTableRepository
from reservations.application.service.reservation_service import ReservationService
from reservations.application.use_case.reservation_use_case import (
    GetReservationsByDateRangeUseCase,
    GetTodaysReservationUseCase,
    RequestReservationUseCase,
    UpdateReservationUseCase,
    CancelReservationUseCase,
)

class ReservationContainer(containers.DeclarativeContainer):
    """Container with providers."""

    # Repository
    reservation_repository = providers.Singleton(DjangoReservationRepository)
    table_repository = providers.Singleton(DjangoTableRepository)

    # Servcice
    reservation_service = providers.Singleton(
        ReservationService,
        reservation_repository=reservation_repository,
        table_repository=table_repository
    )
    
    get_reservation_by_date_range = providers.Factory(
        GetReservationsByDateRangeUseCase,
        reservation_service=reservation_service
    )
    
    get_today_reservations = providers.Factory(
        GetTodaysReservationUseCase,
        reservation_service=reservation_service
    )
    
    request_reservation = providers.Factory(
        RequestReservationUseCase,
        reservation_service=reservation_service
    )

    update_reservation = providers.Factory(
        UpdateReservationUseCase,
        reservation_service=reservation_service
    )
    
    cancel_reservation = providers.Factory(
        CancelReservationUseCase,
        reservation_service=reservation_service
    )
