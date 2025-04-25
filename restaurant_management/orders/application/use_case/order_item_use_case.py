from injector import inject
from ...core.repositories.order_item_repository import OrderItemRepository
from ...core.repositories.order_repository import OrderRepository
from ...core.mappers.order_mappers import OrderItemMapper

class UpdateOrderItemUseCase:
    @inject
    def __init__(self, order_repository: OrderRepository, order_item_repository: OrderItemRepository):
        self.order_repository = order_repository
        self.order_item_repository = order_item_repository

    def execute(self, order_id : int, order_item_data : dict) -> None:
        order = self.order_repository.get_by_id(order_id, raise_exception=True)
        items = [OrderItemMapper.dict_to_domain(item) for item in order_item_data]

        new_item_list = order.get_new_items(items)
        if len(new_item_list) > 0:
            # TODO:
            print(f"{len(new_item_list)} items send to kitchen prepare queue")

        order.update_items(items)
        
        self.order_item_repository.update_order_items(order)


class SetItemDeliveredStausUseCase:
    @inject
    def __init__(self, order_repository: OrderRepository, order_item_repository: OrderItemRepository):
        self.order_repository = order_repository
        self.order_item_repository = order_item_repository

    def execute(self, item_id : int, is_delivered : bool) -> None:
        existing_item = self.order_item_repository.get_by_id(item_id, raise_exception=True)

        existing_item.is_delivered = is_delivered
        
        self.order_item_repository.save(existing_item)

        
        