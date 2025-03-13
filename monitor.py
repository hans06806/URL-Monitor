import asyncio
import httpx
from aiokafka import AIOKafkaProducer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import SessionLocal
from models import URL, URLStatus
from datetime import datetime
import logging
from asyncio import Lock

monitor_lock = Lock()  # Prevents multiple jobs from running at the same time

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug("[Monitor] Starting monitoring script...")


async def send_kafka_message(status):
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()
    await producer.send_and_wait("url_status", bytes(str(status), "utf-8"))
    await producer.stop()

async def check_url(url_obj):
    logging.debug(f"[Monitor] Checking URL: {url_obj.url}")
    async with httpx.AsyncClient() as client:
        try:
            start = datetime.now()
            response = await client.get(url_obj.url, timeout=10)
            response_time = (datetime.now() - start).total_seconds() * 1000
            status = URLStatus(
                url_id=url_obj.id,
                status_code=response.status_code,
                response_time=response_time,
                is_up=response.status_code == 200
            )
            logging.info(f"[Monitor] URL {url_obj.url} is UP, status: {status.status_code}, response time: {response_time:.2f} ms")
        except Exception as e:
            logging.error(f"[Monitor] Error checking {url_obj.url}: {e}")
            status = URLStatus(url_id=url_obj.id, status_code=0, response_time=0, is_up=False)
    
    kafka_message = f"URL {url_obj.url} is {'UP' if status.is_up else 'DOWN'}, status: {status.status_code}"
    
    db = SessionLocal()
    db.add(status)
    db.commit()
    db.close()

    await send_kafka_message(kafka_message)

async def monitor_urls_once():
    async with monitor_lock:  # Prevent duplicate execution
        logging.debug("[Monitor] Fetching URLs from database...")
        db = SessionLocal()
        urls = db.query(URL).all()
        db.close()

        if not urls:
            logging.warning("[Monitor] No URLs found in database.")
            return

        logging.debug(f"[Monitor] Found {len(urls)} URLs to check.")
        tasks = [check_url(url) for url in urls]
        await asyncio.gather(*tasks)

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(monitor_urls_once, "interval", seconds=60)
    scheduler.start()

    # Keep the event loop alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())  # Ensures it runs inside an async event loop