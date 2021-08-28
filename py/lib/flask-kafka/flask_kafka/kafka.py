from kafka import KafkaProducer
from kafka.errors import KafkaError


class Kafka:
    def __init__(self, app=None):
        self.app = app
        self.config = None

        self.producer = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.config = app.config

        bootstrap_servers = self.config.get("KAFKA_BOOTSTRAP_SERVERS")

        if bootstrap_servers:
            self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def send(self, topic, value=None, key=None, headers=None, partition=None, timestamp_ms=None):
        if self.producer:
            return self.producer.send(
                topic=topic, value=value, key=key, headers=headers, partition=partition, timestamp_ms=timestamp_ms
            )
