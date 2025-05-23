from reservations.domain.entities.table import Table
from orders.infrastructure.models.table_model import TableModel

class TableMappers:
    @staticmethod
    def to_model(table: Table):
        return TableModel(
            id=table.id,
            number=table.number,
            capacity=table.capacity,
            is_available=table.is_available
        )

    @staticmethod
    def to_domain(model: TableModel):
        return Table(
            id=model.id,
            number=model.number,
            capacity=model.capacity,
            is_available=model.is_available
        )

