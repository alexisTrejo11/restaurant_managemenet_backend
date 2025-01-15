import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from faker import Faker
from datetime import datetime
from restaurant.models import MenuItemModel, MenuExtraModel, TableModel, ReservationModel, IngredientModel, StockModel, StockTransactionModel, PaymentModel, OrderItemModel, OrderModel, PaymentItemModel, UserModel
import pytz
from decimal import Decimal 
from django.utils.timezone import make_aware


fake = Faker()

class TableFactory(DjangoModelFactory):
    class Meta:
        model = TableModel

    number = factory.Sequence(lambda n: n + 1)
    capacity = factory.Iterator([2, 4, 6, 8]) 
    is_available = True
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class MenuItemFactory(DjangoModelFactory):
    class Meta:
        model = MenuItemModel

    name = factory.Faker('word')
    price = factory.Faker('random_number', digits=2)
    description = factory.Faker('sentence', nb_words=10)
    category = factory.Iterator(MenuItemModel.CATEGORY_CHOICES, getter=lambda c: c[0])
    created_at = factory.LazyFunction(lambda: timezone.make_aware(datetime.now()))
    updated_at = factory.LazyFunction(lambda: timezone.make_aware(datetime.now()))



class MenuExtraFactory(DjangoModelFactory):
    class Meta:
        model = MenuExtraModel

    name = factory.Faker('word')
    price = factory.Faker("random_number", digits=2)
    description = factory.Faker("sentence")
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = ReservationModel

    name = factory.Faker('name')
    phone_number = factory.Faker('phone_number')
    customer_number = factory.Faker('random_int', min=1, max=10)
    email = factory.Faker('email')
    table = factory.SubFactory(TableFactory) 
    reservation_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=2))
    status = factory.Iterator(['BOOKED'])
    cancelled_at = factory.LazyAttribute(lambda x: None if x.status != 'CANCELLED' else timezone.now())
    created_at = factory.LazyFunction(timezone.now)


class IngredientFactory(DjangoModelFactory):
    class Meta:
        model = IngredientModel

    name = factory.Faker('word')
    unit = factory.Faker('word', ext_word_list=['kg', 'g', 'oz', 'ml', 'l'])
    menu_item = factory.SubFactory(MenuItemFactory)
    created_at = factory.LazyFunction(lambda: fake.date_this_century())
    updated_at = factory.LazyFunction(lambda: fake.date_this_century())


class StockFactory(DjangoModelFactory):
    class Meta:
        model = StockModel

    ingredient = factory.SubFactory(IngredientFactory)
    total_stock = factory.Faker('random_int', min=1, max=100)  
    optimal_stock_quantity = factory.Faker('random_int', min=1, max=50)
    created_at = factory.LazyFunction(lambda: fake.date_this_century())
    updated_at = factory.LazyFunction(lambda: fake.date_this_century())


class StockTransactionFactory(DjangoModelFactory):
    class Meta:
        model = StockTransactionModel

    ingredient_quantity = factory.Faker('random_int', min=1, max=10)
    stock = factory.SubFactory(StockFactory) 
    transaction_type = factory.Faker('random_element', elements=['IN', 'OUT'])
    date = factory.LazyFunction(fake.date_this_century)
    expires_at = factory.LazyFunction(fake.future_date)
    employee_name = factory.Faker('name')


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = OrderModel

    table = factory.SubFactory(TableFactory)
    status = factory.Faker('random_element', elements=['IN_PROGRESS', 'COMPLETED', 'CANCELLED'])
    created_at = factory.LazyFunction(timezone.now)
    end_at = factory.LazyAttribute(
        lambda o: make_aware(fake.date_time_this_century(), pytz.UTC) if o.status == 'COMPLETED' else None
    )    


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItemModel

    order = factory.SubFactory(OrderFactory)
    menu_item = factory.SubFactory(MenuItemFactory)
    added_at = factory.LazyFunction(fake.date_this_century)
    is_delivered = factory.Faker('boolean')


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = PaymentModel

    order = factory.SubFactory(OrderFactory) 
    payment_method = factory.Faker('random_element', elements=['CASH', 'CARD', 'TRANSACTION'])
    payment_status = factory.Faker('random_element', elements=['PENDING', 'COMPLETED', 'CANCELLED'])
    sub_total = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    discount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    vat_rate = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    vat = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    currency_type = factory.Faker('random_element', elements=['MXN', 'USD', 'EUR'])
    total = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    created_at = factory.LazyFunction(timezone.now)
    paid_at = factory.LazyAttribute(lambda o: make_aware(fake.date_time_this_century(), pytz.UTC)if o.payment_status == 'COMPLETED' else None)


class PaymentItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentItemModel

    payment = factory.SubFactory(PaymentFactory)
    order_item = factory.SubFactory(OrderItemFactory) 
    menu_item = factory.SubFactory(MenuItemFactory) 
    menu_item_extra = factory.SubFactory(MenuExtraFactory) 
    price = factory.Faker('random_number', digits=5)
    quantity = factory.Faker('random_int', min=1, max=10)
    extras_charges = Decimal('0.00')
    total = factory.LazyAttribute(lambda o: o.price * o.quantity + o.extras_charges)


from django.contrib.auth import get_user_model

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    gender = factory.Faker('random_element', elements=['Male', 'Female', 'Other'])
    email = factory.Faker('email')
    password = factory.Faker('password')
    birth_date = factory.Faker('date_of_birth')
    role = factory.Faker('random_element', elements=['Admin', 'User', 'Manager'])
    phone_number = factory.LazyAttribute(lambda _: fake.phone_number()[:20])
    username = factory.LazyAttribute(lambda x: fake.user_name())