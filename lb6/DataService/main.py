import asyncio
import json

from aiokafka import AIOKafkaConsumer

from database import (
    create_project, create_task
)

KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
KAFKA_TOPIC = "data_commands"


async def consume_commands():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    await consumer.start()
    try:
        async for msg in consumer:
            command = msg.value["command"]
            data = msg.value["data"]

            if command == "create_project":
                result = create_project(data)
                print(f"Project completed: {result}")

            elif command == "create_task":
                result = create_task(data)
                print(f"Task completed: {result}")

    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_commands())
