import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from restaurant.services.domain.ingredient import Ingredient
from restaurant.services.domain.table import Table
from restaurant.services.domain.reservation import Reservation
from restaurant.tests.factories.model_factories import TableFactory, ReservationFactory
from restaurant.mappers.reservation_mappers import ReservationMapper

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
        self.table.mark_unavailable()
        initial_updated_at = self.table.updated_at

        self.table.mark_available()

        self.assertTrue(self.table.is_available)
        self.assertGreater(self.table.updated_at, initial_updated_at)

    def test_str_representation(self):
        self.assertEqual(str(self.table), "Table 1 (Capacity: 4)")


class TestReservation(unittest.TestCase):
    def setUp(self):
        self.future_date = datetime.now() + timedelta(days=10)

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

    def test_cancel_reservation(self):
        reservation = ReservationFactory()
        domain_reservation = ReservationMapper.to_domain(reservation)

        domain_reservation.cancel()
        self.assertEqual(domain_reservation.status, Reservation.Status.CANCELLED)
        self.assertIsNotNone(domain_reservation.cancelled_at)

        with self.assertRaises(ValueError):
            domain_reservation.cancel()

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
            table=Table(number=self.table.number, capacity=self.table.capacity)
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
            table=Table(number=self.table.number, capacity=self.table.capacity)
        )
        result = reservation.validate_customer_limit()
        self.assertTrue(result.is_failure())
        self.assertEqual(result.get_error_msg(), "Reservation can't be above 8 customers")
