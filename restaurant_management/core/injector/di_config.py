from .stock_container import StockContainer, StockTransactionContainer, IngredientContainer

stock_container = StockContainer()
stock_transaction_container = StockTransactionContainer()
ingredient_container = IngredientContainer()

def configure_di():
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
