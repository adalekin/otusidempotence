from dataclasses import dataclass

from dataclasses_avroschema import AvroModel


@dataclass
class OrderCompleted(AvroModel):
    "An OrderCompleted event"
    order_id: int

    class Meta:
        namespace = "OrderCompleted.v1"
        aliases = ["order-completed-v1"]
