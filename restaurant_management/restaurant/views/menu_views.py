from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from restaurant.services.menu_service import MenuService
from restaurant.serializers import MenuItemSerializer, MenuInsertItemSerializer
from restaurant.utils.response import ApiResponse

menu_service = MenuService()

class MenuViewSet(ViewSet):
    def retrieve(self, request, pk=None):
        """
        GET /menus/<id> - Retrieve a single menu by ID.
        """
        menu = menu_service.get_menu_by_id(pk)
        if not menu:
            return ApiResponse.not_found('Menu', 'ID', pk)

        menu_data = MenuItemSerializer(menu).data
        return ApiResponse.found(menu_data, 'Menu', 'ID', pk)


    def list(self, request):
        """
        GET /menus/ - Retrieve all menus.
        """
        menus = menu_service.get_all_menus()
        menu_data = MenuItemSerializer(menus, many=True).data
        return ApiResponse.ok(menu_data, 'Menus successfully fetched')


    def create(self, request):
        """
        POST /menus/ - Create a new menu.
        """
        serializer = MenuInsertItemSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        menu_item = menu_service.create_menu(serializer.validated_data)
        menu_item_data = MenuItemSerializer(menu_item).data
        
        return ApiResponse.created(menu_item_data, 'Menu Item successfully created')


    def destroy(self, request, pk=None):
        """
        DELETE /menus/<id> - Delete a menu by ID.
        """
        is_deleted = menu_service.delete_menu_by_id(pk)
        if not is_deleted:
            return ApiResponse.not_found('Menu', 'ID', pk)

        return ApiResponse.deleted('Menu Item')

    """
    @action(detail=False, methods=['get'], url_path='category/(?P<category>[^/.]+)')
    def get_by_category(self, request, category=None):
    \"\"\"
        GET /menus/category/<category> - Retrieve menus by category.
        \"\"\"
        menus = menu_service.get_menus_by_category(category)
        if not menus:
            return ApiResponse.not_found('Category', 'name', category)

        menu_data = MenuItemSerializer(menus, many=True).data
        return ApiResponse.found(menu_data, 'Menu Items', 'category', category)
    """