import RPi.GPIO as GPIO
import time
import board
import adafruit_dht
import psutil
import json
import random
from paho.mqtt import client as mqtt_client

for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D23)
in1 = 15

temp = sensor.temperature
humidity = sensor.humidity

GPIO.setup(in1, GPIO.OUT)

broker = '192.168.155.19'
port = 1883
topic_publish = "dht/topic"
topic_subscribe = "dht/topic2"
client_id = 'python-mqtt'
username = ''
password = ''
id_dev = 'kel21'
tipe = 'DHT Sensor'
timestamp = 123456

def connect_mqtt() :
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect,return code %d\n", rc)            
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username,password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publishSubscribe(client):
    msg_count = 0
    while True:
        try:
            print("Temperature: {}*C    ".format(temp))
            
     
            if temp > 28 :
                GPIO.output(in1,1)
                status = "hidup"
            else:
                GPIO.output(in1,0)
                status = "mati"       
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(1.0)
            continue
        except Exception as error:
            sensor.exit()
            raise error
        time.sleep(2.0)
        objek = temp
        msg = json.dumps({ "id": id_dev, "type": tipe, "value": objek, "desc": status, "timestamp": timestamp })
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