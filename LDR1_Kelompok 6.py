import random
import time
import json
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client

broker = '192.168.155.19'
port = 1883
topic_publish = "ldr1/topic"
client_id = 'python-mqtt'
username = ''
password = ''
id_dev = 'kel6'
tipe = 'LDR Sensor'
timestamp = 123456

ldr = 7
in1 = 15 
in2 = 18
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ldr, GPIO.IN)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

GPIO.output(in1, False)
GPIO.output(in2, False)

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
		print(GPIO.input(ldr))
		if GPIO.input(ldr)==1:
			print("Tirai Terbuka")
			GPIO.output(in1, True)
			GPIO.output(in2, False)
			msg = json.dumps({ "id":id_dev,"type":tipe,"value":1,"desc":"ON","timestamp":timestamp})
			result = client.publish(topic_publish, msg)
			time.sleep(2)
		else:
			print("Tirai Tertutup")
			GPIO.output(in1, False)
			GPIO.output(in2, True)
			msg = json.dumps({ "id":id_dev,"type":tipe,"value":0,"desc":"OFF","timestamp":timestamp})
			result = client.publish(topic_publish, msg)
			time.sleep(2)     
   
	status = result[0]
	if status == 0:
		print("Send "+msg+" to topic {topic_publish}")
	else:
		print("Failed to send message to topic {topic_publish}")
	
	def on_message(client, userdata, msg):
		print("Received "+str(msg.payload)+" from topic")
	client.on_message = on_message
	time.sleep(1)

def run():
    client = connect_mqtt()
    client.loop_start()
    publishSubscribe(client)

if __name__== '__main__':
    run()