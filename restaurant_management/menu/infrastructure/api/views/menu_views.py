from rest_framework.viewsets import ViewSet
from ..serializers.serializers import MenuItemSerializer, MenuInsertItemSerializer
from core.response.django_response import DjangoResponseWrapper
from core.injector.app_module import AppModule
from injector import Injector
from dataclasses import asdict
from core.utils.permission import RoleBasedPermission
from ....application.use_cases.query_menu_items_use_cases import (
    GetMenuByIdUseCase,
    GetAllMenusUseCase,
)
from ....application.use_cases.command_menu_items_use_cases import (
    CreateMenuUseCase,
    DeleteMenuUseCase
)

container = Injector([AppModule()])

class MenuViews(ViewSet):
    def __init__(self, **kwargs):
        self.get_menu_by_id_use_case = container.get(GetMenuByIdUseCase)
        self.get_all_menus_use_case = container.get(GetAllMenusUseCase)
        self.create_menus_use_case = container.get(CreateMenuUseCase)
        self.delete_menus_use_case = container.get(DeleteMenuUseCase)
        super().__init__(**kwargs)

    # Role Permissions
    def get_permissions(self):
        permissions = []
        if self.action in ['create_menu_item', 'delete_menu_item_by_id']:
            permissions = [RoleBasedPermission(['admin'])]
        
        return permissions

    def retieve(self, request, menu_id=None):
        menu_item_response = self.get_menu_by_id_use_case.execute(menu_id, raise_expection=True)

        return DjangoResponseWrapper.found(
            data= asdict(menu_item_response), 
            entity= 'Menu Item', 
            param= 'ID', 
            value= menu_id)


    def list(self, request): 
        menus_response = self.get_all_menus_user_case.execute()

        menus_to_dict = [asdict(menu) for menu in menus_response]
        return DjangoResponseWrapper.found(
            data=menus_to_dict, 
            entity='Menus Item List'
        )

    def create(self, request):
        serializer = MenuInsertItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        menu_item_created = self.create_menus_use_case.execute(**serializer.validated_data)

        return DjangoResponseWrapper.created(
            data=asdict(menu_item_created),
            entity="Menu Item"    
        )

    def destroy(self, request, menu_id):
        self.delete_menus_use_case.execute(menu_id)

        return DjangoResponseWrapper.deleted('Menu Item')