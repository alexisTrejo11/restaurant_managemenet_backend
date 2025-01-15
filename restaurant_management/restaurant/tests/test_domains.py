import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from restaurant.services.domain.ingredient import Ingredient
from restaurant.services.domain.table import Table
from restaurant.services.domain.order import OrderItem, Order
from restaurant.services.domain.stock import Stock, StockTransaction
from restaurant.services.domain.payment import Payment, PaymentItem
from restaurant.services.domain.reservation import Reservation
from restaurant.tests.factories.model_factories import TableFactory, ReservationFactory
from restaurant.mappers.reservation_mappers import ReservationMapper
from restaurant.services.domain.order import Order, OrderItem, OrderStatus
from restaurant.services.domain.menu_item import MenuItem, CategoryEnum
from restaurant.utils.exceptions import DomainException
import pytest
import unittest

class TestIngredient(unittest.TestCase):
    def setUp(self):
        self.ingredient = Ingredient(
            id="1",
            name="Sugar",
            unit="kg"
        )

    def test_initialization(self):
        self.assertEqual(self.ingredient.id, "1")
        self.assertEqual(self.ingredient.name, "Sugar")
        self.assertEqual(self.ingredient.unit, "kg")
        self.assertIsInstance(self.ingredient.created_at, datetime)
        self.assertIsInstance(self.ingredient.updated_at, datetime)

    def test_update_quantity(self):
        new_quantity = Decimal("10.5")
        initial_updated_at = self.ingredient.updated_at

        self.ingredient.update_quantity(new_quantity)

        self.assertEqual(self.ingredient.quantity, new_quantity)
        self.assertGreater(self.ingredient.updated_at, initial_updated_at)

    def test_update_quantity_negative(self):
        with self.assertRaises(ValueError) as context:
            self.ingredient.update_quantity(Decimal("-5"))
        self.assertEqual(str(context.exception), "Quantity cannot be negative.")

    def test_str_representation(self):
        self.assertEqual(str(self.ingredient), "Sugar")


class TestTable(unittest.TestCase):
    def setUp(self):
        self.table = Table(
            number=1,
            capacity=4
        )

    def test_initialization(self):
        self.assertEqual(self.table.number, 1)
        self.assertEqual(self.table.capacity, 4)
        self.assertTrue(self.table.is_available)
        self.assertIsInstance(self.table.created_at, datetime)
        self.assertIsInstance(self.table.updated_at, datetime)

    def test_mark_unavailable(self):
        initial_updated_at = self.table.updated_at

        self.table.mark_unavailable()

        self.assertFalse(self.table.is_available)
        self.assertGreater(self.table.updated_at, initial_updated_at)

    def test_mark_available(self):
        initial_updated_at = self.table.updated_at

        self.table.mark_available()

        self.assertTrue(self.table.is_available)
        self.assertGreater(self.table.updated_at, initial_updated_at)

    def test_str_representation(self):
        self.assertEqual(str(self.table), "Table 1 (Capacity: 4)")


class TestReservation(unittest.TestCase):
    def setUp(self):
        self.future_date = datetime.now() + timedelta(days=10)
        self.table = Table(number=1,capacity=4)

    def test_create_reservation_success(self):
        reservation = Reservation(
            name="John Doe",
            email="john.doe@example.com",
            phone_number="1234567890",
            customer_number=4,
            reservation_date=self.future_date,
            table=Table(number=1, capacity=4)
        )
        self.assertEqual(reservation.name, "John Doe")
        self.assertEqual(reservation.status, Reservation.Status.BOOKED)
        self.assertIsNotNone(reservation.created_at)

    @pytest.mark.django_db
    def test_cancel_reservation(self):
        reservation = ReservationFactory()
        domain_reservation = ReservationMapper.to_domain(reservation)

        domain_reservation.cancel()
        self.assertEqual(domain_reservation.status, Reservation.Status.CANCELLED)
        self.assertIsNotNone(domain_reservation.cancelled_at)

        with self.assertRaises(ValueError):
            domain_reservation.cancel()

    @pytest.mark.django_db
    def test_attend_reservation(self):
        reservation = ReservationFactory()
        domain_reservation = ReservationMapper.to_domain(reservation)

        domain_reservation.attend()
        self.assertEqual(domain_reservation.status, Reservation.Status.ATTENDED)

    def test_validate_date_future_date(self):
        reservation = Reservation(
            name="Valid Date",
            email="valid.date@example.com",
            phone_number="7778889999",
            customer_number=4,
            reservation_date=self.future_date,
            table=Table(number=2, capacity=4)
        )
        result = reservation.validate_date()
        self.assertTrue(result.is_success())

    def test_validate_hour_within_limits(self):
        valid_time = datetime.now().replace(hour=15, minute=0, second=0, microsecond=0)
        reservation = Reservation(
            name="Valid Hour",
            email="valid.hour@example.com",
            phone_number="1231231234",
            customer_number=4,
            reservation_date=valid_time,
            table=self.table
        )
        result = reservation.validate_hour()
        self.assertTrue(result.is_success())

    def test_validate_customer_limit_exceeds_limit(self):
        reservation = Reservation(
            name="Exceeds Limit",
            email="exceeds.limit@example.com",
            phone_number="3434343434",
            customer_number=10,
            reservation_date=self.future_date,
            table=self.table
        )
        result = reservation.validate_customer_limit()
        self.assertTrue(result.is_failure())
        self.assertEqual(result.get_error_msg(), "Reservation can't be above 8 customers")


class TestStock(unittest.TestCase):
    
    def setUp(self):
        ingredient = type('Ingredient', (object,), {'name': 'Tomato', 'unit': 'kg'})
        self.stock = Stock(id=1, ingredient=ingredient, optimal_stock_quantity=100, total_stock=50)
        self.transaction_in = StockTransaction(
            ingredient_quantity=30,
            date=datetime.now(),
            employee_name="John Doe",
            transaction_type='IN',
            stock=self.stock
        )
        self.transaction_out = StockTransaction(
            ingredient_quantity=20,
            date=datetime.now(),
            employee_name="Jane Doe",
            transaction_type='OUT',
            stock=self.stock
        )

    def test_validate_transaction_in_valid(self):
        result = self.stock.validate_transaction(self.transaction_in)
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["message"], "Transaction is valid")

    def test_validate_transaction_out_valid(self):
        result = self.stock.validate_transaction(self.transaction_out)
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["message"], "Transaction is valid")

    def test_validate_transaction_out_invalid(self):
        self.stock.total_stock = 10
        result = self.stock.validate_transaction(self.transaction_out)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["message"], "Quantity to withdraw exceeds current total stock")

    def test_validate_transaction_in_invalid(self):
        self.stock.total_stock = 80
        result = self.stock.validate_transaction(self.transaction_in)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["message"], "Quantity to insert exceeds the allowed limit of 100")

    def test_add_transaction_in(self):
        initial_stock = self.stock.total_stock
        self.stock.add_transaction(self.transaction_in)
        self.assertEqual(self.stock.total_stock, initial_stock + self.transaction_in.ingredient_quantity)
        self.assertEqual(len(self.stock.stock_transactions), 1)

    def test_add_transaction_out(self):
        initial_stock = self.stock.total_stock
        self.stock.add_transaction(self.transaction_out)
        self.assertEqual(self.stock.total_stock, initial_stock - self.transaction_out.ingredient_quantity)
        self.assertEqual(len(self.stock.stock_transactions), 1)

    def test_is_stock_available(self):
        self.assertTrue(self.stock.is_stock_available(20))
        self.assertFalse(self.stock.is_stock_available(60))

    def test_adjust_stock(self):
        self.stock.adjust_stock(20)
        self.assertEqual(self.stock.total_stock, 70)
        self.stock.adjust_stock(-10)
        self.assertEqual(self.stock.total_stock, 60)

    def test_clear_stock(self):
        self.stock.clear()
        self.assertEqual(self.stock.total_stock, 0)
        self.assertEqual(len(self.stock.stock_transactions), 0)

    def test_stock_str(self):
        self.assertEqual(str(self.stock), "Tomato - 50 kg")

    def test_transaction_str(self):
        self.assertEqual(str(self.transaction_in), "IN - 30")



class TestMenuItem(unittest.TestCase):
    def setUp(self):
        self.menu_item = MenuItem(
            id=1,
            name="Pizza Margherita",
            price=Decimal('150.00'),
            category=CategoryEnum.MEALS,
            description="Delicious Italian pizza",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def test_update_price_success(self):
        new_price = Decimal('180.00')
        self.menu_item.update_price(new_price)
        
        self.assertEqual(self.menu_item.price, new_price)
        self.assertTrue(self.menu_item.updated_at > datetime.now() - timedelta(seconds=1))

    def test_update_price_fail(self):
        with self.assertRaises(ValueError):
            self.menu_item.update_price(Decimal('-10.00'))

    def test_update_category_success(self):
        new_category = CategoryEnum.DESSERTS
        self.menu_item.update_category(new_category)

        self.assertEqual(self.menu_item.category, new_category)
        self.assertTrue(self.menu_item.updated_at > datetime.now() - timedelta(seconds=1))

    def test_update_category_fail(self):
        with self.assertRaises(ValueError):
            self.menu_item.update_category("INVALID_CATEGORY")

    def test_is_meal(self):
        self.assertTrue(self.menu_item.is_meal())

        self.menu_item.update_category(CategoryEnum.DESSERTS)
        self.assertFalse(self.menu_item.is_meal())


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.menu_item_1 = self.create_menu_item(id=1, name="Pizza Margherita", price=Decimal('150.00'))
        self.menu_item_2 = self.create_menu_item(id=2, name="Burger", price=Decimal('120.00'))
        self.order_item_1 = self.create_order_item(menu_item=self.menu_item_1, quantity=1, id=1)
        self.order_item_2 = self.create_order_item(menu_item=self.menu_item_2, quantity=2, id=2)

    def create_menu_item(self, id, name, price, category=CategoryEnum.MEALS):
        return MenuItem(id=id, name=name, price=price, category=category)

    def create_order_item(self, menu_item, quantity, id):
        return OrderItem(menu_item=menu_item, quantity=quantity, id=id)

    def test_set_item_as_delivered(self):
        order = Order(table=1, status=OrderStatus.IN_PROGRESS, items=[self.order_item_1])

        order.set_item_as_delivered(1)

        self.assertTrue(self.order_item_1.is_delivered)

    def test_set_item_as_delivered_item_not_found(self):
        order = Order(table=1, status=OrderStatus.IN_PROGRESS, items=[self.order_item_1])

        with self.assertRaises(DomainException):
            order.set_item_as_delivered(999)

    def test_set_as_cancel(self):
        order = Order(table=1, status=OrderStatus.IN_PROGRESS)

        order.set_as_cancel()

        self.assertEqual(order.status, OrderStatus.CANCELLED)
        self.assertIsNotNone(order.end_at)

    def test_set_as_cancel_order_not_in_progress(self):
        order = Order(table=1, status=OrderStatus.CANCELLED)

        with self.assertRaises(DomainException):
            order.set_as_cancel()

    def test_set_as_complete(self):
        order = Order(table=1, status=OrderStatus.IN_PROGRESS)

        order.set_as_complete()

        self.assertEqual(order.status, OrderStatus.COMPLETED)
        self.assertIsNotNone(order.end_at)

    def test_set_as_complete_order_not_in_progress(self):
        order = Order(table=1, status=OrderStatus.COMPLETED)

        with self.assertRaises(DomainException):
            order.set_as_complete()

    def test_add_item(self):
        order = Order(table=1, status=OrderStatus.IN_PROGRESS)

        order.add_item(self.order_item_1)

        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.items[0].menu_item.name, "Pizza Margherita")

    def test_remove_items(self):
        order = Order(table=1, status=OrderStatus.IN_PROGRESS, items=[self.order_item_1, self.order_item_2])

        order.remove_items([1])

        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.items[0].menu_item.name, "Burger")

        with self.assertRaises(ValueError):
            order.remove_items([999])


class TestPayment(unittest.TestCase):
    def setUp(self):
        self.menu_item = MenuItem(
            id=1,
            name="Pizza Margherita",
            price=Decimal('150.00'),
            category="MEALS"
        )
        self.order_item = OrderItem(
            menu_item=self.menu_item,
            quantity=2,
            id=1
        )
        self.order = Order(table=1, status="IN_PROGRESS", items=[self.order_item])
        self.payment = Payment.init_payment(self.order)

    def test_create_payment(self):
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.payment_status, 'pending_payment')
        self.assertEqual(self.payment.sub_total, Decimal('0.00'))
        self.assertEqual(self.payment.total, Decimal('0.00'))
        self.assertEqual(self.payment.currency_type, 'MXN')

    def test_calculate_numbers(self):
        payment_item = PaymentItem(
            menu_item=self.menu_item,
            order_item=self.order_item,
            price=Decimal('150.00'),
            quantity=2
        )
        payment_item.calculate_total()

        self.payment.items.append(payment_item)
        self.payment.calculate_numbers()

        self.assertEqual(self.payment.sub_total, Decimal('300.00'))
        self.assertEqual(self.payment.vat, Decimal('48.00'))  # 300 * 0.16
        self.assertEqual(self.payment.total, Decimal('348.00'))  # 300 + 48


    def test_validate_payment_complete_success(self):
        self.payment.payment_status = 'PENDING_PAYMENT'
        result = self.payment.validate_payment_complete()
        self.assertTrue(result.is_success())

    def test_validate_payment_complete_error(self):
        self.payment.payment_status = 'CANCELLED'
        result = self.payment.validate_payment_complete()
        self.assertTrue(result.is_failure())
        self.assertEqual(result.get_error_msg(), "only pending payments can be completed")

    def test_validate_payment_cancel_success(self):
        self.payment.payment_status = 'PENDING_PAYMENT'
        result = self.payment.validate_payment_cancel()
        self.assertTrue(result.is_success())

    def test_validate_payment_cancel_error(self):
        self.payment.payment_status = 'COMPLETE'
        result = self.payment.validate_payment_cancel()
        self.assertTrue(result.is_failure())
        self.assertEqual(result.get_error_msg(), "only pending payments can be cancel")

    def test_validate_payment_method_success(self):
        result = self.payment.validate_payment_method('CARD')
        self.assertTrue(result.is_success())

    def test_validate_payment_method_error(self):
        result = self.payment.validate_payment_method('BITCOIN')
        self.assertTrue(result.is_failure())
        self.assertEqual(result.get_error_msg(), "invalid payment method")

    def test_complete_payment(self):
        self.payment.payment_status = 'PENDING_PAYMENT'
        self.payment.complete_payment('CASH')
        self.assertEqual(self.payment.payment_status, 'COMPLETED')
        self.assertEqual(self.payment.payment_method, 'CASH')
        self.assertIsNotNone(self.payment.paid_at)

    def test_validate_payment_status_invalid(self):
        with self.assertRaises(DomainException):
            self.payment.validate_payment_status('INVALID_STATUS')

    def test_set_as_complete(self):
        self.payment.set_as_complete()
        self.assertEqual(self.payment.payment_status, 'COMPLETED')

    def test_validate_pending_status_error(self):
        with self.assertRaises(ValueError):
            Payment.validate_pending_status('COMPLETE')

if __name__ == "__main__":
    unittest.main()
