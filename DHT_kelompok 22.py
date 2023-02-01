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
led = 10
temp = sensor.temperature
humidity = sensor.humidity

GPIO.setup(led, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

broker = '192.168.183.187'
port = 1883
topic_publish = "topic/objek"
client_id = 'python-mqtt'
username = 'rikiyoga'
password = 'tupainakal'
id_dev = 'kel23'
tipe = 'sensor.humadity'
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
		try:
			print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))

			if humidity < 80 :
				GPIO.output(buzzer,1)
				GPIO.output(led,0)
				status = "hidup"
			else:
				GPIO.output(buzzer,0)
				GPIO.output(led,1)
				status = "mati"

		except RuntimeError as error:
			print(error.args[0])
			time.sleep(2.0)
			continue
		except Exception as error:
			dhtDevice.exit()
			raise error
			time.sleep(2.0)
		objek = humidity
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

if __name__ == '__main__':
    run()