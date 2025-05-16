from rest_framework.viewsets import ViewSet
from ..serializers.serializers import MenuItemSerializer, MenuInsertItemSerializer
from core.response.django_response import DjangoResponseWrapper
from core.injector.app_module import AppModule
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

from dependency_injector.wiring import inject, Provide

class MenuViews(ViewSet):
    @inject
    def __init__(self,
        get_menu_by_id_use_case: GetMenuByIdUseCase = Provide[AppModule.get_menu_by_id_use_case],
        get_all_menus_use_case: GetAllMenusUseCase = Provide[AppModule.get_all_menus_use_case],
        create_menus_use_case: CreateMenuUseCase = Provide[AppModule.create_menus_use_case],
        delete_menus_use_case: DeleteMenuUseCase = Provide[AppModule.delete_menus_use_case],
        **kwargs):
        
        self.get_menu_by_id_use_case = get_menu_by_id_use_case
        self.get_all_menus_use_case = get_all_menus_use_case
        self.create_menus_use_case = create_menus_use_case
        self.delete_menus_use_case = delete_menus_use_case
        super().__init__(**kwargs)

        

    def retrieve(self, request, pk=None):
        menu_item_response = self.get_menu_by_id_use_case.execute(pk, raise_expection=True)

        return DjangoResponseWrapper.found(
            data= asdict(menu_item_response), 
            entity= 'Menu Item', 
            param= 'ID', 
            value= pk)


    def list(self, request): 
        menus = self.get_all_menus_use_case.execute()
        if not menus or len(menus) == 0:
            return DjangoResponseWrapper.success(
                data=menus,
                message="Any Menu Items Found")

        menus_to_dict = [asdict(menu) for menu in menus]
        return DjangoResponseWrapper.found(
            data=menus_to_dict, 
            entity='Menus Item List'
        )

    def create(self, request):
        serializer = MenuInsertItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        menu_item_created = self.create_menus_use_case.execute(serializer.validated_data)

        return DjangoResponseWrapper.created(
            data=asdict(menu_item_created),
            entity="Menu Item"    
        )

    def destroy(self, request, pk):
        self.delete_menus_use_case.execute(pk)

        return DjangoResponseWrapper.no_content('Menu Item Successfully Deleted')