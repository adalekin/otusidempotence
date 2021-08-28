import enum

from marshmallow import fields
from marshmallow_enum import EnumField
from sqlalchemy.sql import func

from orders.extensions import db, marshmallow


class OrderStatus(enum.Enum):
    created = "created"
    processing = "processing"
    complete = "complete"
    cancelled = "cancelled"
    refunded = "refunded"


class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), index=True)
    items = db.relationship("OrderItem")
    status = db.Column(db.Enum(OrderStatus))

    updated_at = db.Column(db.DateTime, server_default=func.now())
    created_at = db.Column(db.DateTime, server_onupdate=func.now())

    def __repr__(self):
        return f"<Order {self.id}>"

    @property
    def amount(self):
        return sum(map(lambda item: item.quantity * item.unit_price, self.items))


class OrderItem(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer(), index=True)
    unit_price = db.Column(db.Integer())
    quantity = db.Column(db.Integer())

    def __repr__(self):
        return f"<OrderItem {self.id}>"


class OrderItemSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        exclude = ("id", "order_id")


class OrderSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        exclude = ("user_id",)
        include_fk = True

    items = fields.Nested(OrderItemSchema, many=True)
    status = EnumField(OrderStatus, by_value=True)
    amount = fields.Integer()


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
