from schemas.order import OrderCompleted
from talepy.steps import Step

from orders.extensions import db, kafka
from orders.models.order import Order, OrderItem, OrderStatus


class CreateOrder(Step):
    def execute(self, state):
        with db.session.begin(subtransactions=True):
            order = Order(user_id=state["user_id"], status=OrderStatus.created)

            for item in state["items"]:
                order.items.append(OrderItem(product_id=item["product_id"], quantity=item["quantity"], unit_price=100))
            db.session.add(order)

        state["order"] = order
        return state

    def compensate(self, state):
        with db.session.begin(subtransactions=True):
            state["order"].status = OrderStatus.cancelled
            db.session.add(state["order"])


class CompleteOrder(Step):
    def execute(self, state):
        with db.session.begin(subtransactions=True):
            state["order"].status = OrderStatus.complete
            db.session.add(state["order"])
        return state

    def compensate(self, state):
        with db.session.begin(subtransactions=True):
            state["order"].status = OrderStatus.processing
            db.session.add(state["order"])

class SendOrderCompleted(Step):
    def execute(self, state):
        order_completed = OrderCompleted(order_id=state["order"].id)

        kafka.send("order-completed", order_completed.serialize())
        return state

    def compensate(self, state):
        pass
