from restaurant.tests.factories.model_factories import TableFactory, MenuItemFactory, MenuExtraFactory, OrderItemFactory, OrderModelFactory
from restaurant.repository.models.models import TableModel, MenuItemModel, MenuExtra
from restaurant.repository.models.models import ReservationModel, TableModel, IngredientModel, StockModel, OrderItem, OrderModel, PaymentModel
from restaurant.tests.factories.model_factories import ReservationFactory, TableFactory, IngredientFactory, MenuItemFactory, StockFactory, PaymentFactory

from django.utils import timezone
from django.test import TestCase
from faker import Faker

fake = Faker()

class TableModelTest(TestCase):
    def test_default_values(self):
        table = TableFactory(number=2)

        self.assertEqual(table.number, 2)
        self.assertTrue(table.is_available)
        self.assertEqual(table.seats, 2)


    def test_create_table_with_specific_values(self):
        table = TableFactory(number=10, seats=4, is_available=False)

        self.assertEqual(table.number, 10)
        self.assertEqual(table.seats, 4)
        self.assertFalse(table.is_available)

    def test_table_creation_and_persistence(self):
        table = TableFactory()

        table.save()

        saved_table = TableModel.objects.get(id=table.id)
        self.assertEqual(saved_table.number, table.number)
        self.assertEqual(saved_table.seats, table.seats)
        self.assertEqual(saved_table.is_available, table.is_available)

    def test_updated_at_on_update(self):
        table = TableFactory()
        original_updated_at = table.updated_at

        table.seats = 6
        table.save()

        self.assertNotEqual(original_updated_at, table.updated_at)

    def test_delete_table(self):
        table = TableFactory()
        table.save()

        self.assertTrue(TableModel.objects.filter(id=table.id).exists())

        table.delete()

        self.assertFalse(TableModel.objects.filter(id=table.id).exists())


class MenuItemModelTest(TestCase):
    def test_create_menu_item(self):
        menu_item = MenuItemFactory()


        self.assertIsNotNone(menu_item)
        self.assertIsInstance(menu_item, MenuItemModel)

        self.assertTrue(menu_item.price > 0) 
        self.assertIn(menu_item.category, dict(MenuItemModel.CATEGORY_CHOICES).keys())
        self.assertIsInstance(menu_item.created_at, type(fake.date_this_decade()))
        self.assertIsInstance(menu_item.updated_at, type(fake.date_this_decade()))

    def test_menu_item_persistence(self):
        menu_item = MenuItemFactory()

        menu_item.save()

        saved_item = MenuItemModel.objects.get(id=menu_item.id)
        self.assertEqual(saved_item.name, menu_item.name)
        self.assertEqual(saved_item.price, menu_item.price)
        self.assertEqual(saved_item.category, menu_item.category)
        self.assertEqual(saved_item.description, menu_item.description)

    def test_delete_menu_item(self):
        menu_item = MenuItemFactory()
        menu_item.save()

        self.assertTrue(MenuItemModel.objects.filter(id=menu_item.id).exists())

        menu_item.delete()

        self.assertFalse(MenuItemModel.objects.filter(id=menu_item.id).exists())
    

class MenuExtraTest(TestCase):
    def test_create_menu_extra(self):
        menu_extra = MenuExtraFactory()

        self.assertIsNotNone(menu_extra)
        self.assertIsInstance(menu_extra, MenuExtra)

        self.assertIsInstance(menu_extra.created_at, type(fake.date_this_decade()))
        self.assertIsInstance(menu_extra.updated_at, type(fake.date_this_decade()))

    def test_menu_extra_persistence(self):
        menu_extra = MenuExtraFactory()

        menu_extra.save()

        saved_extra = MenuExtra.objects.get(id=menu_extra.id)
        self.assertEqual(saved_extra.name, menu_extra.name)

    def test_delete_menu_extra(self):
        menu_extra = MenuExtraFactory()
        menu_extra.save()

        self.assertTrue(MenuExtra.objects.filter(id=menu_extra.id).exists())

        menu_extra.delete()

        self.assertFalse(MenuExtra.objects.filter(id=menu_extra.id).exists())


class ReservationModelTest(TestCase):
    def setUp(self):
        self.table = TableFactory()
        
    def test_create_reservation(self):
        # Crear una nueva reserva
        reservation = ReservationFactory(table=self.table)

        self.assertEqual(reservation.status, 'BOOKED')
        self.assertEqual(reservation.table, self.table)
        self.assertIsNotNone(reservation.reservation_date)

    def test_reservation_str_method(self):
        reservation = ReservationFactory(table=self.table)

        self.assertEqual(str(reservation), f'{reservation.name} - {reservation.reservation_date}')

    def test_read_reservation(self):
        reservation = ReservationFactory(table=self.table)

        fetched_reservation = ReservationModel.objects.get(id=reservation.id)

        self.assertEqual(fetched_reservation.name, reservation.name)
        self.assertEqual(fetched_reservation.phone_number, reservation.phone_number)

    def test_update_reservation(self):
        reservation = ReservationFactory(table=self.table)

        reservation.status = 'ATTENDED'
        reservation.save()

        updated_reservation = ReservationModel.objects.get(id=reservation.id)

        self.assertEqual(updated_reservation.status, 'ATTENDED')

    def test_delete_reservation(self):
        reservation = ReservationFactory(table=self.table)

        self.assertTrue(ReservationModel.objects.filter(id=reservation.id).exists())

        reservation.delete()

        self.assertFalse(ReservationModel.objects.filter(id=reservation.id).exists())

    def test_cancelled_reservation(self):
        reservation = ReservationFactory(table=self.table, status='CANCELLED')

        self.assertIsNotNone(reservation.cancelled_at)
        self.assertEqual(reservation.status, 'CANCELLED')


class IngredientModelTest(TestCase):
    def setUp(self):
        self.menu_item = MenuItemFactory()
        
    def test_create_ingredient(self):
        ingredient = IngredientFactory(menu_item=self.menu_item)

        self.assertEqual(ingredient.name, ingredient.name)
        self.assertEqual(ingredient.unit, ingredient.unit)
        self.assertEqual(ingredient.menu_item, self.menu_item)

    def test_ingredient_str_method(self):
        ingredient = IngredientFactory(menu_item=self.menu_item)

        self.assertEqual(str(ingredient), ingredient.name)

    def test_read_ingredient(self):
        ingredient = IngredientFactory(menu_item=self.menu_item)

        fetched_ingredient = IngredientModel.objects.get(id=ingredient.id)

        self.assertEqual(fetched_ingredient.name, ingredient.name)
        self.assertEqual(fetched_ingredient.unit, ingredient.unit)

    def test_update_ingredient(self):
        ingredient = IngredientFactory(menu_item=self.menu_item)

        new_name = "Updated Ingredient"
        ingredient.name = new_name
        ingredient.save()

        updated_ingredient = IngredientModel.objects.get(id=ingredient.id)

        self.assertEqual(updated_ingredient.name, new_name)

    def test_delete_ingredient(self):
        ingredient = IngredientFactory(menu_item=self.menu_item)

        self.assertTrue(IngredientModel.objects.filter(id=ingredient.id).exists())

        ingredient.delete()

        self.assertFalse(IngredientModel.objects.filter(id=ingredient.id).exists())


class StockModelTest(TestCase):
    def setUp(self):
        self.ingredient = IngredientFactory()

    def test_create_stock(self):
        stock = StockFactory(ingredient=self.ingredient)

        self.assertEqual(stock.ingredient, self.ingredient)
        self.assertEqual(stock.total_stock, stock.total_stock)
        self.assertEqual(stock.optimal_stock_quantity, stock.optimal_stock_quantity)

    def test_stock_str_method(self):
        stock = StockFactory(ingredient=self.ingredient)

        self.assertEqual(str(stock), f'{self.ingredient.name} - {stock.total_stock} {self.ingredient.unit}')

    def test_read_stock(self):
        stock = StockFactory(ingredient=self.ingredient)

        fetched_stock = StockModel.objects.get(id=stock.id)

        self.assertEqual(fetched_stock.total_stock, stock.total_stock)

    def test_update_stock(self):
        stock = StockFactory(ingredient=self.ingredient)

        new_total_stock = 200
        stock.total_stock = new_total_stock
        stock.save()

        updated_stock = StockModel.objects.get(id=stock.id)

        self.assertEqual(updated_stock.total_stock, new_total_stock)

    def test_delete_stock(self):
        stock = StockFactory(ingredient=self.ingredient)

        self.assertTrue(StockModel.objects.filter(id=stock.id).exists())

        stock.delete()

        self.assertFalse(StockModel.objects.filter(id=stock.id).exists())

class OrderModelTest(TestCase):

    def setUp(self):
        # Crear una orden y sus ítems
        self.order = OrderModelFactory()
        self.order_item = OrderItemFactory(order=self.order)

    def test_create_order(self):
        # Verificar que la orden se haya creado correctamente
        order = OrderModel.objects.get(id=self.order.id)

        # Verificar los datos de la orden
        self.assertEqual(order.table, self.order.table)
        self.assertEqual(order.status, self.order.status)
        self.assertEqual(order.created_at, self.order.created_at)
        self.assertEqual(order.end_at, self.order.end_at)

    def test_order_str_method(self):
        # Verificar que el método __str__ devuelve la representación correcta
        order = OrderModelFactory()
        self.assertEqual(str(order), f'Order {order.id} - Table {order.table.number}')

    def test_read_order(self):
        # Recuperar la orden desde la base de datos
        order = OrderModel.objects.get(id=self.order.id)

        # Verificar que los datos de la orden coinciden
        self.assertEqual(order.status, self.order.status)
        self.assertEqual(order.created_at, self.order.created_at)

    def test_update_order(self):
        # Actualizar el estado de la orden
        order = OrderModelFactory()
        new_status = 'COMPLETED'
        order.status = new_status
        order.save()

        # Recuperar la orden actualizada
        updated_order = OrderModel.objects.get(id=order.id)

        # Verificar que el estado de la orden ha sido actualizado
        self.assertEqual(updated_order.status, new_status)

    def test_delete_order(self):
        # Verificar que la orden existe en la base de datos
        order = OrderModelFactory()
        self.assertTrue(OrderModel.objects.filter(id=order.id).exists())

        # Eliminar la orden
        order.delete()

        # Verificar que la orden ha sido eliminada
        self.assertFalse(OrderModel.objects.filter(id=order.id).exists())


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.order_item = OrderItemFactory()

    def test_create_order_item(self):
        order_item = OrderItem.objects.get(id=self.order_item.id)

        self.assertEqual(order_item.menu_item, self.order_item.menu_item)
        self.assertEqual(order_item.order, self.order_item.order)
        self.assertEqual(order_item.is_delivered, self.order_item.is_delivered)

    def test_order_item_str_method(self):
        order_item = OrderItemFactory()
        self.assertEqual(str(order_item), f'{order_item.menu_item.name} - Order {order_item.order.id}')

    def test_update_order_item(self):
        order_item = OrderItemFactory()
        new_is_delivered = True
        order_item.is_delivered = new_is_delivered
        order_item.save()

        updated_order_item = OrderItem.objects.get(id=order_item.id)

        self.assertEqual(updated_order_item.is_delivered, new_is_delivered)

    def test_delete_order_item(self):
        order_item = OrderItemFactory()
        self.assertTrue(OrderItem.objects.filter(id=order_item.id).exists())

        order_item.delete()

        self.assertFalse(OrderItem.objects.filter(id=order_item.id).exists())


class PaymentModelTest(TestCase):

    def setUp(self):
        self.payment = PaymentFactory()

    def test_create_payment(self):
        payment = PaymentModel.objects.get(id=self.payment.id)

        self.assertEqual(payment.order, self.payment.order)
        self.assertEqual(payment.payment_method, self.payment.payment_method)
        self.assertEqual(payment.payment_status, self.payment.payment_status)
        self.assertEqual(payment.sub_total, self.payment.sub_total)
        self.assertEqual(payment.discount, self.payment.discount)
        self.assertEqual(payment.vat_rate, self.payment.vat_rate)
        self.assertEqual(payment.vat, self.payment.vat)
        self.assertEqual(payment.currency_type, self.payment.currency_type)
        self.assertEqual(payment.total, self.payment.total)

    def test_payment_str_method(self):
        payment = PaymentFactory()
        self.assertEqual(str(payment), f'Payment for Order {payment.order_id} - {payment.total} {payment.currency_type}')

    def test_read_payment(self):
        payment = PaymentModel.objects.get(id=self.payment.id)

        self.assertEqual(payment.sub_total, self.payment.sub_total)
        self.assertEqual(payment.total, self.payment.total)

    def test_update_payment(self):
        payment = PaymentFactory()
        new_status = 'COMPLETED'
        payment.payment_status = new_status
        payment.save()

        updated_payment = PaymentModel.objects.get(id=payment.id)

        self.assertEqual(updated_payment.payment_status, new_status)

    def test_delete_payment(self):
        payment = PaymentFactory()
        self.assertTrue(PaymentModel.objects.filter(id=payment.id).exists())

        payment.delete()

        self.assertFalse(PaymentModel.objects.filter(id=payment.id).exists())

