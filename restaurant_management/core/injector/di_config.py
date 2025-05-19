from .app_module import AppModule as MenuContainer
from .table_container import TableContainer
from .reservation_container import ReservationContainer
from .auth_container import AuthContainer
from .stock_container import StockContainer, StockTransactionContainer, IngredientContainer

menu_container = MenuContainer()
table_container = TableContainer()
reservation_container = ReservationContainer()
stock_container = StockContainer()
stock_transaction_container = StockTransactionContainer()
ingredient_container = IngredientContainer()
auth_container = AuthContainer()

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
        "stock.infrastructure.api.views.stock_views", 
        ],
        packages=["stock"]
    )
    ingredient_container.wire(
        modules=["stock.infrastructure.api.views.ingredient_views"
        ],
        packages=["stock"]
    )

    auth_container.wire(
          modules=["authorization.infrastructure.api.views"
        ],
        packages=["authorization"]
    )

