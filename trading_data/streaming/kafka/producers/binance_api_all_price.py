import os
import json
import logging
import asyncio
from aiokafka import AIOKafkaProducer
from utils.kafka_utils.binance_api import producer_stream_api_book_price

TOPIC = 'binance-api-all-price'
FREQUENCY = 1.0
KEY = 'symbol'
URL = "https://fapi.binance.com/fapi/v1/ticker/price"

"""
kafka-topics.sh --create \
  --bootstrap-server kafka:9092 \
  --topic binance-api-all-price \
  --partitions 12 \
  --replication-factor 1

kafka-topics.sh --bootstrap-server kafka:9092 --delete --topic binance-api-all-price
"""

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s")


async def main():
    producer = AIOKafkaProducer(
        bootstrap_servers=os.getenv("BOOTSTRAP_SERVER"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8")
    )
    await producer.start()
    logging.log(logging.INFO, f"{TOPIC}: Started streaming")
    try:
        await producer_stream_api_book_price(
            producer=producer,
            topic=TOPIC,
            key=KEY,
            url=URL,
            frequency=FREQUENCY
        )
    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(main())
