from aiokafka import AIOKafkaConsumer
import asyncio

async def consume():
    consumer = AIOKafkaConsumer(
        "url_status",
        bootstrap_servers="localhost:9092",
        group_id="webmon",
        auto_offset_reset="earliest"
    )
    await consumer.start()

    try:
        async for msg in consumer:
            print(f"Consumed message: {msg.value.decode('utf-8')}")
    finally:
        await consumer.stop()

asyncio.run(consume())