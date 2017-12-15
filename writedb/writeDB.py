import pika
import sys
import argparse
import json

from influxdb import InfluxDBClient

file = open("/configwdb/configure.cfg", "r")
data = file.readlines()

# Connection rabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host = data[1].replace('\n', '')))
channel = connection.channel()

def getData(channel):
	# Create exchange type direct
	channel.exchange_declare(exchange = data[7].replace('\n', ''), exchange_type = 'direct')

	# Create queue
	channel.queue_declare(queue = data[10].replace('\n', ''))

	# Link exchange to queue with routing_key
	routing_keys = [data[4].replace('\n', '')]
	for routing_key in routing_keys:
		channel.queue_bind(
			exchange = data[7].replace('\n', ''),
			queue = data[10].replace('\n', ''),
			routing_key = routing_key
		)

	print(' [*] Waiting for logs. To exit press CTRL+C')

	def callback(ch, method, properties, body):
		# print(body)
		writeDB(body)
		
	channel.basic_consume(callback, queue = data[10].replace('\n', ''), no_ack = True)
	channel.start_consuming()

def writeDB(body):
	def main(host = data[13].replace('\n', ''), port = data[16].replace('\n', '')):
	    """Instantiate a connection to the InfluxDB."""
	    user = data[19].replace('\n', '')
	    password = data[22].replace('\n', '')
	    dbname = data[25].replace('\n', '')
	    # dbuser = data[28].replace('\n', '')
	    # dbuser_password = data[31].replace('\n', '')
	    query = 'SELECT * FROM "temperature"'
	    json_body = json.loads(body)

	    client = InfluxDBClient(host, port, user, password, dbname)

	    # print("Drop user: " + dbuser)
	    # client.drop_user(dbuser)

	    # print("Drop database: " + dbname)
	    # client.drop_database(dbname)

	    # print("Create database: " + dbname)
	    client.create_database(dbname)

	    # print("Create a retention policy")
		# client.create_retention_policy('awesome_policy', '3d', 3, default=True)

	    # print("Create user: " + dbuser)
	    # client.create_user(dbuser, dbuser_password)

	    # print("Switch user: " + dbuser)
	    # client.switch_user(dbuser, dbuser_password)

	    # print("Write points: {0}".format(json_body))
	    client.write_points(json_body)

	    # print("Querying data: " + query)
	    result = client.query(query)

	    print("Result: {0}".format(result))

	    # print("Switch user: " + user)
	    # client.switch_user(user, password)

	    # print("Drop database: " + dbname)
	    # client.drop_database(dbname)


	def parse_args():
	    """Parse the args."""
	    parser = argparse.ArgumentParser(
	        description='example code to play with InfluxDB')
	    parser.add_argument('--host', type=str, required=False,
	                        default=data[13].replace('\n', ''),
	                        help='hostname of InfluxDB http API')
	    parser.add_argument('--port', type=int, required=False, default=data[16].replace('\n', ''),
	                        help='port of InfluxDB http API')
	    return parser.parse_args()


	if __name__ == '__main__':
	    args = parse_args()
	    main(host=args.host, port=args.port)

getData(channel)
