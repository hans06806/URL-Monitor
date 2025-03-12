import asyncio
import httpx
from aiokafka import AIOKafkaProducer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import SessionLocal
from models import URL, URLStatus
from datetime import datetime

async def send_kafka_message(status):
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()
    await producer.send_and_wait("url_status", bytes(str(status), "utf-8"))
    await producer.stop()

async def check_url(url_obj):
    async with httpx.AsyncClient() as client:
        try:
            start = datetime.now()
            response = await client.get(url_obj.url, timeout=10)
            response_time = (datetime.now() - start).microseconds / 1000
            status = URLStatus(url_id=url_obj.id, status_code=response.status_code, response_time=response_time, is_up=response.status_code == 200)
        except Exception:
            status = URLStatus(url_id=url_obj.id, status_code=0, response_time=0, is_up=False)

    db = SessionLocal()
    db.add(status)
    db.commit()
    db.close()

    await send_kafka_message(f"URL {url_obj.url} is {'UP' if status.is_up else 'DOWN'}, status: {status.status_code}")

async def monitor_urls():
    while True:
        db = SessionLocal()
        urls = db.query(URL).all()
        tasks = [check_url(url) for url in urls]
        await asyncio.gather(*tasks)
        db.close()
        await asyncio.sleep(60)

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(monitor_urls, "interval", seconds=60)
    scheduler.start()

    # Keep the event loop alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())  # Ensures it runs inside an async event loop