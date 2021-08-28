from dataclasses import dataclass

from dataclasses_avroschema import AvroModel


@dataclass
class UserRegistered(AvroModel):
    "A UserRegistered event"
    user_id: int

    class Meta:
        namespace = "UserRegistered.v1"
        aliases = ["user-registered-v1"]
