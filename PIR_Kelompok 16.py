import RPi.GPIO as GPIO
import random
import json 
import time
from paho.mqtt import client as mqtt_client


GPIO.setmode(GPIO.BOARD)

GPIO_PIR = 13
GPIO_RELAY = 15

GPIO.setup(GPIO_RELAY, GPIO.OUT)
GPIO.setup(GPIO_PIR, GPIO.IN)

broker = '192.168.209.19'
port = 1883
topic_publish = "topic/objek2"
topic_subscribe = "topic/windSpeed"
client_id = 'python-mqtt'
username = ''
password = ''
id_dev = 'kel2'
tipe = 'Pir Sensor 2'
timestamp = 123456
def connect_mqtt():
    def on_connect(client, userdate, flags, rc):
        if rc == 0:
            print("connected to mqtt broker!!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publishSubscribe(client):
    msg_count = 0
while True:

        value = GPIO.input(GPIO_PIR)
        if value == 1  :
             GPIO.output(GPIO_RELAY, 1)
             status = "Ada Objek Terdeteksi"
        else:
             GPIO.output(GPIO_RELAY, 0)
             status = "Tidak Ada Objek Terdeteksi"

        objek = value
        msg = json.dumps({ "id": id_dev, "type": tipe, "value": objek, "desc": >
        result = client.publish(topic_publish, msg)
        status = result [0]
        if status == 0:
            print("send" +msg+"to topic"+topic_publish)
        else:
            print("Failed to send message to topic {topic_publish}")
        def on_message(client, userdata, msg):
            print("received" +str(msg.payload)+"from topic")
 client.subscribe(topic_subscribe)
        client.on_message = on_message
        time.sleep(2)
def run():
    client = connect_mqtt()
    client.loop_start()
    publishSubscribe(client)

if _name_ == '_main_':
    run()