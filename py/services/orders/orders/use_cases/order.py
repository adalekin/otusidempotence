from talepy import run_transaction

from orders.sagas.billing import CreatePayment, GetAccount
from orders.sagas.order import CompleteOrder, CreateOrder, SendOrderCompleted


def create_order_use_case(user_id, items):
    state = run_transaction(
        steps=[CreateOrder(), GetAccount(), CreatePayment(), CompleteOrder(), SendOrderCompleted()],
        starting_state={"user_id": user_id, "items": items},
    )

    return state["order"]
