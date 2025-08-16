from fastapi import FastAPI
import paho.mqtt.client as mqtt

app = FastAPI()

# MQTT Broker details
broker = "test.mosquitto.org"
port = 1883
topic = "fastapi/test"

# Initialize MQTT client
client = mqtt.Client()
client.connect(broker, port, 60)
client.loop_start()

@app.post("/publish/{message}")
async def publish_message(message: str):
    client.publish(topic, message)
    return {"status": "Message published", "message": message}
