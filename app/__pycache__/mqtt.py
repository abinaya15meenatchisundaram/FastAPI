# main_async.py
from fastapi import FastAPI
import asyncio
from asyncio_mqtt import Client

app = FastAPI()

BROKER = "test.mosquitto.org"
TOPIC = "fastapi/async"

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(mqtt_subscriber())

async def mqtt_subscriber():
    async with Client(BROKER) as client:
        async with client.messages() as messages:
            await client.subscribe(TOPIC)
            async for message in messages:
                print(f"📩 Async Received: {message.topic} -> {message.payload.decode()}")

@app.post("/publish/{message}")
async def publish(message: str):
    async with Client(BROKER) as client:
        await client.publish(TOPIC, message.encode())
    return {"status": "sent", "message": message}
