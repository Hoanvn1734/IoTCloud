import paho.mqtt.client as mqtt
import pika

mosquitto_cf = open("/configbroker/configure.cfg", "r")
data = mosquitto_cf.readlines()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(data[10].replace('\n', ''))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	# Connection rabbitMQ server
	connection = pika.BlockingConnection(pika.ConnectionParameters(host = data[13].replace('\n', '')))
	channel = connection.channel()

	# Create exchange type direct
	channel.exchange_declare(exchange = data[16].replace('\n', ''), exchange_type = 'direct')

	# get para 1 if para number > 2
	routing_key = data[19].replace('\n', '')

	# get from para 2 to the end or 'Hello World' 

	message = msg.payload

	print(message)

	channel.basic_publish(exchange = data[16].replace('\n', ''), routing_key = routing_key, body = message)

	# print(" [x] Sent %r:%r" % (routing_key, message))

	connection.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(data[1].replace('\n', ''), int(data[4].replace('\n', '')), int(data[7].replace('\n', '')))

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
