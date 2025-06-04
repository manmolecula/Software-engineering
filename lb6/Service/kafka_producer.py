import json

from aiokafka import AIOKafkaProducer

KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
KAFKA_TOPIC = "data_commands"


class KafkaProducer:
    def __init__(self):
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_command(self, command: str, data: dict):
        if not self.producer:
            raise RuntimeError("Producer not started")

        message = {
            "command": command,
            "data": data
        }
        await self.producer.send_and_wait(KAFKA_TOPIC, message)


kafka_producer = KafkaProducer()
