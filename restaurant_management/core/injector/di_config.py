from .app_module import AppModule as MenuContainer
from .table_container import TableContainer
from dependency_injector.wiring import inject, Provide

menu_container = MenuContainer()
table_container = TableContainer()

def configure_di():
    menu_container.wire(
        modules=["menu.infrastructure.api.views.menu_views"],
        packages=["menu"]
    )
    table_container.wire(
        modules=["orders.infrastructure.api.views.table_views"],
        packages=["menu"]
    )

