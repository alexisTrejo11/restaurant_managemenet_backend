from restaurant.dtos.order_item_dtos import OrderItemInsertDTO

class OrderMappers:
    @staticmethod  
    def map_request_to_order_item_dtos(data):
        order_items = data.get('order_items', [])
        
        return [
            OrderItemInsertDTO(
                menu_id=item.get('menu_id'),
                quantity=item.get('quantity'),
                notes=item.get('notes')
            )
            for item in order_items
        ]