import random
import time
import json
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client

broker = '192.168.155.84'
port = 1883
topic_publish = "topic/keran"
client_id = 'python-mqtt'
username = ''
password = ''
GPIO.setwarnings(False)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

#set GPIO Pins
GPIO_TRIGGER = 7
GPIO_ECHO = 11
BUZZER = 13

#set GPIO direction (IN / OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed  to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publishSubscribe(client):
    msg_count = 0
    while True:
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(2)
        GPIO.output(GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        if distance < 10  :
             GPIO.output(BUZZER, True)
             status = "Keran menyala"
        else:
             GPIO.output(BUZZER, False)
             status = "Keran mati"
        jarak = str(distance)
        msg = json.dumps({"jarak": jarak, "status_Keran": status})
        result = client.publish(topic_publish, msg)
        status = result[0]
        if status == 0:
            print("send "+msg+" to topic "+topic_publish)
        else:
            print("Failed to send message to topic {topic_publish}")
    def on_message(client, userdata, msg):
        print("Received"+str(msg.payload)+"from topic")
    client_subscribe(topic_subscribe)
    client.on_message = on_message
    time.sleep(1)

def run():
    client = connect_mqtt()
    client.loop_start()
    publishSubscribe(client)

if _name_ == '_main_':
    run()