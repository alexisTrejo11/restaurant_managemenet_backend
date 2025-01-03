from rest_framework.viewsets import ViewSet
from restaurant.services.menu_service import MenuItemService
from restaurant.serializers import MenuItemSerializer, MenuInsertItemSerializer
from restaurant.utils.response import ApiResponse
from restaurant.injector.app_module import AppModule
from injector import Injector

container = Injector([AppModule()])

class MenuViews(ViewSet):
    def get_menu_service(self):
        return container.get(MenuItemService)


    def get_menu_item_by_id(self, request, menu_id=None):
        menu_service = self.get_menu_service()

        menu = menu_service.get_menu_by_id(menu_id)
        if not menu:
            return ApiResponse.not_found('Menu', 'ID', menu_id)

        menu_data = MenuItemSerializer(menu).data
        return ApiResponse.found(menu_data, 'Menu', 'ID', menu_id)


    def get_menus_items_by_category(self, request, category=None):
        menu_service = self.get_menu_service()

        menus = menu_service.get_menus_by_category(category)
        if not menus:
            return ApiResponse.not_found('Category', 'name', category)

        menu_data = MenuItemSerializer(menus, many=True).data
        return ApiResponse.found(menu_data, 'Menu Items', 'category', category)


    def get_all_menu_items(self, request):
        menu_service = self.get_menu_service()

        menus = menu_service.get_all_menus()
        menu_data = MenuItemSerializer(menus, many=True).data
        return ApiResponse.ok(menu_data, 'Menus successfully fetched')


    def create_menu_item(self, request):
        menu_service = self.get_menu_service()

        serializer = MenuInsertItemSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        menu_item = menu_service.create_menu(serializer.validated_data)
        menu_item_data = MenuItemSerializer(menu_item).data
        
        return ApiResponse.created(menu_item_data, 'Menu Item successfully created')


    def delete_menu_item_by_id(self, request, menu_id=None):
        menu_service = self.get_menu_service()

        is_deleted = menu_service.delete_menu_by_id(menu_id)
        if not is_deleted:
            return ApiResponse.not_found('Menu', 'ID', menu_id)

        return ApiResponse.deleted('Menu Item')
