from .app_module import AppModule
from dependency_injector.wiring import inject, Provide

container = AppModule()

def configure_di():
    container.wire(
        modules=[
            "menu.infrastructure.api.views.menu_views",
        ],
        packages=[
            "menu",
            "orders",
        ]
    )