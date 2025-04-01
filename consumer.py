from aiokafka import AIOKafkaConsumer # An async Kafka consumer to read messages from Kafka Topics
import asyncio # Python's standard library for writing async code

async def consume(): # define an async function, which continuously listens for incoming messages from Kafka
    consumer = AIOKafkaConsumer(
        "url_status", # Listens specifically to the "url_status" topic
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

# The consumer script (consumer.py) complements your producer logic in monitor.py, 
# forming a complete Kafka-based event-driven architecture.

# Allows your system to process monitoring results in real-time as they are generated, 
# supporting future extension for database storage, logging, or alerting.

# A Kafka Consumer is an application or process that reads (consumes) messages from one or more Kafka topics. 
# Kafka maintains messages in a queue-like structure, where messages remain stored until consumed 
# (or until retention policies remove them).

# A Kafka topic is a logical channel used to organize and categorize messages.