from restaurant.models import OrderModel, OrderItemModel
from restaurant.services.domain.order import Order
from restaurant.repository.common_repository import CommonRepository
from typing import List, Optional
from restaurant.mappers.order_mappers import OrderMappers, OrderItemMappers


class OrderRepository(CommonRepository):
    def __init__(self):
        self.order_model = OrderModel
        self.item_model = OrderItemModel
    

    def get_by_id(self, id: int) -> Optional[Order]:
        order = self.order_model.objects.filter(id=id).first()
        return OrderMappers.to_domain(order) if order else None


    def get_by_status(self, status: str) -> List[Order]:
        models = self.order_model.objects.filter(status=status)

        return [OrderMappers.to_domain(model) for model in models]
    

    def create(self, order: Order) -> Order:
        order_model = OrderMappers.to_model(order)
        
        order_model.save()

        return OrderMappers.to_domain(order_model)
    

    def update(self, order: Order) -> Order:
        order_model = OrderModel.objects.filter(id=order.id).first()
        if not order_model:
            raise ValueError(f"Order with id {order.id} not found")

        # Update order fields
        model = OrderMappers.to_model(order)
        for field, value in model.__dict__.items():
            if field != 'id' and not field.startswith('_'):
                setattr(order_model, field, value)
        
        order_model.save()

        return OrderMappers.to_domain(order_model)

    def get_all(self) -> List[Order]:
        order_models = self.order_model.objects.all()
        return [OrderMappers.to_domain(model) for model in order_models] if order_models else []


    def delete(self, id: int) -> bool:
        deleted, _ = self.order_model.objects.filter(id=id).delete()
        return deleted > 0
    

    def delete(self, id: int) -> bool:
        deleted, _ = self.order_model.objects.filter(id=id).delete()
        return deleted > 0
    

    def update_items(self, order: Order):
        order_model = OrderModel.objects.filter(id=order.id).first()
        self.__delete_items(order)
        
        for item in order.items:
            item_model = OrderItemMappers.to_model(item)
            item_model.order = order_model
            
            if item.id:
                self.__update_items(item, item_model)
            else:
                item_model.save()
        
        return OrderMappers.to_domain(order_model)

    def get_not_delivered_items(self):
        model_items = OrderItemModel.objects.filter(is_delivered=False)

        return [OrderItemMappers.to_domain(model_item) for model_item in model_items]

    def __delete_items(self, order: Order):
        existing_items = OrderItemModel.objects.filter(order=order.id)

        existing_item_ids = {item.id for item in existing_items}
        current_item_ids = {item.id for item in order.items if item.id}

        items_to_delete = existing_item_ids - current_item_ids
        if items_to_delete:
            OrderItemModel.objects.filter(id__in=items_to_delete).delete()


    def __update_items(self, item, item_model):
        existing_item = OrderItemModel.objects.filter(id=item.id).first()
        for field, value in item_model.__dict__.items():
            if field != 'id' and not field.startswith('_'):
                setattr(existing_item, field, value)
            
        existing_item.save()
    