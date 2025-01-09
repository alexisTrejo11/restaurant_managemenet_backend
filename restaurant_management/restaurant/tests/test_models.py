from restaurant.tests.factories.model_factories import TableFactory, MenuItemFactory, MenuExtraFactory, OrderItemFactory, OrderFactory
from restaurant.repository.models.models import TableModel, MenuItemModel, MenuExtraModel
from restaurant.repository.models.models import ReservationModel, TableModel, IngredientModel, StockModel, OrderItemModel, OrderModel, PaymentModel, PaymentItemModel
from restaurant.tests.factories.model_factories import ReservationFactory, TableFactory, IngredientFactory, MenuItemFactory, StockFactory, PaymentFactory, PaymentItemFactory, UserFactory  
from decimal import Decimal
from django.test import TestCase
from faker import Faker

fake = Faker()

class TableModelTest(TestCase):
    def test_default_values(self):
        table = TableFactory(number=2)

        self.assertEqual(table.number, 2)
        self.assertTrue(table.is_available)
        self.assertIsNotNone(table.capacity)


    def test_create_table_with_specific_values(self):
        table = TableFactory(number=10, capacity=4, is_available=False)

        self.assertEqual(table.number, 10)
        self.assertEqual(table.capacity, 4)
        self.assertFalse(table.is_available)

    def test_table_creation_and_persistence(self):
        table = TableFactory()

        table.save()

        saved_table = TableModel.objects.get(id=table.id)
        self.assertEqual(saved_table.number, table.number)
        self.assertEqual(saved_table.capacity, table.capacity)
        self.assertEqual(saved_table.is_available, table.is_available)

    def test_updated_at_on_update(self):
        table = TableFactory()
        original_updated_at = table.updated_at

        table.capacity = 6
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
        self.assertIsInstance(menu_extra, MenuExtraModel)

        self.assertIsInstance(menu_extra.created_at, type(fake.date_this_decade()))
        self.assertIsInstance(menu_extra.updated_at, type(fake.date_this_decade()))

    def test_menu_extra_persistence(self):
        menu_extra = MenuExtraFactory()

        menu_extra.save()

        saved_extra = MenuExtraModel.objects.get(id=menu_extra.id)
        self.assertEqual(saved_extra.name, menu_extra.name)

    def test_delete_menu_extra(self):
        menu_extra = MenuExtraFactory()
        menu_extra.save()

        self.assertTrue(MenuExtraModel.objects.filter(id=menu_extra.id).exists())

        menu_extra.delete()

        self.assertFalse(MenuExtraModel.objects.filter(id=menu_extra.id).exists())


class ReservationModelTest(TestCase):
    def setUp(self):
        self.table = TableFactory()
        
    def test_create_reservation(self):
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
        self.order = OrderFactory()
        self.order_item = OrderItemFactory(order=self.order)

    def test_create_order(self):
        order = OrderModel.objects.get(id=self.order.id)

        self.assertEqual(order.table, self.order.table)
        self.assertEqual(order.status, self.order.status)
        self.assertEqual(order.created_at, self.order.created_at)
        self.assertEqual(order.end_at, self.order.end_at)

    def test_order_str_method(self):
        order = OrderFactory()
        self.assertEqual(str(order), f'Order {order.id} - Table {order.table.number}')

    def test_read_order(self):
        order = OrderModel.objects.get(id=self.order.id)

        self.assertEqual(order.status, self.order.status)
        self.assertEqual(order.created_at, self.order.created_at)

    def test_update_order(self):
        order = OrderFactory()
        new_status = 'COMPLETED'
        order.status = new_status
        order.save()

        updated_order = OrderModel.objects.get(id=order.id)

        self.assertEqual(updated_order.status, new_status)

    def test_delete_order(self):
        order = OrderFactory()
        self.assertTrue(OrderModel.objects.filter(id=order.id).exists())

        order.delete()

        self.assertFalse(OrderModel.objects.filter(id=order.id).exists())


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.order_item = OrderItemFactory()

    def test_create_order_item(self):
        order_item = OrderItemModel.objects.get(id=self.order_item.id)

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

        updated_order_item = OrderItemModel.objects.get(id=order_item.id)

        self.assertEqual(updated_order_item.is_delivered, new_is_delivered)

    def test_delete_order_item(self):
        order_item = OrderItemFactory()
        self.assertTrue(OrderItemModel.objects.filter(id=order_item.id).exists())

        order_item.delete()

        self.assertFalse(OrderItemModel.objects.filter(id=order_item.id).exists())


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


class PaymentItemModelTest(TestCase):
    def setUp(self):
        self.payment_item = PaymentItemFactory()

    def test_create_payment_item(self):
        payment_item = PaymentItemModel.objects.get(id=self.payment_item.id)

        self.assertEqual(payment_item.payment, self.payment_item.payment)
        self.assertEqual(payment_item.order_item, self.payment_item.order_item)
        self.assertEqual(payment_item.menu_item, self.payment_item.menu_item)
        self.assertEqual(payment_item.menu_item_extra, self.payment_item.menu_item_extra)
        self.assertEqual(payment_item.price, self.payment_item.price)
        self.assertEqual(payment_item.quantity, self.payment_item.quantity)
        self.assertEqual(payment_item.extras_charges, self.payment_item.extras_charges)
        self.assertEqual(payment_item.total, self.payment_item.total)

    def test_payment_item_str_method(self):
        payment_item = PaymentItemFactory()
        self.assertEqual(str(payment_item), f'{payment_item.quantity}x {payment_item.menu_item.name} - {payment_item.total}')

    def test_read_payment_item(self):
        payment_item = PaymentItemModel.objects.get(id=self.payment_item.id)

        self.assertEqual(payment_item.price, self.payment_item.price)
        self.assertEqual(payment_item.quantity, self.payment_item.quantity)
        self.assertEqual(payment_item.total, self.payment_item.total)

    def test_update_payment_item(self):
        payment_item = PaymentItemFactory()
        new_price = Decimal('19.99')
        payment_item.price = new_price
        payment_item.save()

        updated_payment_item = PaymentItemModel.objects.get(id=payment_item.id)

        self.assertEqual(updated_payment_item.price, new_price)

    def test_delete_payment_item(self):
        payment_item = PaymentItemFactory()
        self.assertTrue(PaymentItemModel.objects.filter(id=payment_item.id).exists())

        payment_item.delete()

        self.assertFalse(PaymentItemModel.objects.filter(id=payment_item.id).exists())

from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_create_user(self):
        user = get_user_model().objects.get(id=self.user.id)

        self.assertEqual(user.first_name, self.user.first_name)
        self.assertEqual(user.last_name, self.user.last_name)
        self.assertEqual(user.gender, self.user.gender)
        self.assertEqual(user.email, self.user.email)
        self.assertEqual(user.password, self.user.password)
        self.assertEqual(user.role, self.user.role)
        self.assertEqual(user.phone_number, self.user.phone_number)

    def test_user_str_method(self):
        user = UserFactory()
        self.assertEqual(str(user), f'{user.first_name} {user.last_name}')

    def test_read_user(self):
        user = get_user_model().objects.get(id=self.user.id)

        self.assertEqual(user.first_name, self.user.first_name)
        self.assertEqual(user.last_name, self.user.last_name)
        self.assertEqual(user.email, self.user.email)

    def test_update_user(self):
        user = UserFactory()
        new_email = 'newemail@example.com'
        user.email = new_email
        user.save()

        updated_user = get_user_model().objects.get(id=user.id)

        self.assertEqual(updated_user.email, new_email)

    def test_delete_user(self):
        user = UserFactory()
        self.assertTrue(get_user_model().objects.filter(id=user.id).exists())

        user.delete()

        self.assertFalse(get_user_model().objects.filter(id=user.id).exists())