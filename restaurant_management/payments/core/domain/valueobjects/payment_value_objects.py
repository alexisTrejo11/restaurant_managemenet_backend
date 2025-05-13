from enum import Enum

class PaymentMethod(str, Enum):
    CASH = 'CASH'
    CARD = 'CARD'
    TRANSACTION = 'TRANSACTION'

    @staticmethod
    def get_methods():
        return [PaymentMethod.CARD.__str__, PaymentMethod.CASH.__str__, PaymentMethod.TRANSACTION.__str__]

class PaymentStatus(str, Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

    @staticmethod
    def get_all_staus():
        return [PaymentStatus.PENDING.__str__, PaymentStatus.COMPLETED.__str__, PaymentStatus.CANCELLED.__str__]

class CurrencyType(str, Enum):
    MXN = 'MXN'
    USD = 'USD'
    EUR = 'EUR'
