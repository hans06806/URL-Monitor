WebMon - URL Monitoring System

📌 Background

WebMon is a URL monitoring system that periodically checks website availability, response time, and health status. 
It uses Kafka for event-driven architecture and stores monitoring results in a PostgreSQL database.

🚀 Tech Stack

## 🚀 Tech Stack

| Technology     | Description                                      |
|--------------|--------------------------------------------------|
| **Flask**     | Web API framework for managing URLs            |
| **httpx**     | Async HTTP client for fast URL checking        |
| **SQLAlchemy** | ORM for PostgreSQL database management        |
| **psycopg2**  | PostgreSQL driver for database connection      |
| **aiokafka**  | Kafka producer/consumer for event-driven processing |
| **APScheduler** | Task scheduler for periodic URL checks      |
| **Gunicorn**  | Web server for deploying Flask API             |

📖 Features

✅ Add URLs for monitoring via API.
✅ Monitor URLs asynchronously using httpx.
✅ Store monitoring results in PostgreSQL.
✅ Event-driven processing with Kafka.
✅ View monitoring results via API.

TBC