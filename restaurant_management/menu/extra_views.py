from rest_framework.decorators import api_view
from .services.menu_item_service import MenuItemService
from core.response.django_response import DjangoResponseWrapper

@api_view(['GET'])
def list_dish_status(request):
    status_list = MenuItemService.list_all_categories()

    return DjangoResponseWrapper.found(
        data=status_list,
        entity="Dish Status List",
    )