import connexion
from orders.exception import AccessDenied
from orders.models.order import order_schema
from orders.use_cases.order import create_order_use_case

from . import utils


def create(order):
    _, payload = utils.jwt_read_from_header(request=connexion.request)
    AccessDenied.require_condition(payload, "Access denied")

    order_ = create_order_use_case(user_id=payload["user_id"], **order)

    return order_schema.dump(order_), 201
