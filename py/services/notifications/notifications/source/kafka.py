import logging

from aiokafka import AIOKafkaConsumer
from schemas.user import UserRegistered

from notifications import settings

from .adapters import WelcomeEmail

LOG = logging.getLogger(__name__)


class KafkaNotificationSource:
    topic_schema_map = {settings.KAFKA_TOPIC_USER_REGISTERED: UserRegistered}
    event_notifications_map = {UserRegistered: [WelcomeEmail]}

    async def run(self):
        consumer = AIOKafkaConsumer(
            settings.KAFKA_TOPIC_USER_REGISTERED,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=settings.KAFKA_GROUP_ID,
        )

        await consumer.start()

        try:
            async for msg in consumer:
                schema_class = self.topic_schema_map.get(msg.topic)

                if not schema_class:
                    continue

                for notification in self._event_to_notifications(schema_class.deserialize(msg.value)):
                    LOG.info(notification)
        finally:
            await consumer.stop()

    def _event_to_notifications(self, event):
        notificaiton_classes = self.event_notifications_map.get(event.__class__, [])
        return list(map(lambda nc: nc(event), notificaiton_classes))
