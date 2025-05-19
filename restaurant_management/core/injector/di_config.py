from .app_module import AppModule as MenuContainer
from .table_container import TableContainer
from .reservation_container import ReservationContainer
from .stock_container import StockContainer, StockTransaxtionContainer

menu_container = MenuContainer()
table_container = TableContainer()
reservation_container = ReservationContainer()
stock_container = StockContainer()

def configure_di():
    menu_container.wire(
        modules=["menu.infrastructure.api.views.menu_views"],
        packages=["menu"]
    )
    table_container.wire(
        modules=["orders.infrastructure.api.views.table_views"],
        packages=["menu"]
    ),
    reservation_container.wire(
        modules=["reservations.infrastructure.views.reservation_views"],
        packages=["reservations"]
    )
    stock_container.wire(
        modules=[
        "stock.infrastructure.views.stock_views", 
        "stock.infrastructure.views.stock_transaction_views"
        ],
        packages=["stock"]
    )


