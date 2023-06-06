import logging
import json
import pika
from api.services.data_processor import DataProcessor
# import subprocess

class RabbitMQReceiver():
    """
    Consumer component that will receive messages and handle
    connection and channel interactions with RabbitMQ.
    """

    def __init__(
        self,
        host,
        username,
        password,
        routing_keys,
        queue,
        exchange='',
        influx_name='',
        influx_port='',
        influx_token='',
        influx_org='',
        influx_bucket=''
    ):
        self._routing_keys = routing_keys
        self.queue_name = queue
        self._host = host
        self._exchange = exchange
        self._username = username
        self._password = password
        self.data_processor = DataProcessor(influx_name,influx_port, influx_token, influx_org, influx_bucket)
        self.start_server()

    def start_server(self):
        self.create_channel()
        self.create_exchange()
        self.create_bind()
        logging.info("Receiver Channel created...")

    def create_channel(self):
        credentials = pika.PlainCredentials(username=self._username, password=self._password)
        parameters = pika.ConnectionParameters(self._host, credentials=credentials ,heartbeat=0)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    def create_exchange(self):
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type='topic',  
            passive=False,
            durable=True,
            auto_delete=False
        )

    def create_bind(self):
        self._channel.queue_declare(queue=self.queue_name, exclusive=False, durable=True)
        logging.info(f"Queue created: {self.queue_name}")
        for routing_key in self._routing_keys: 
            self._channel.queue_bind(
                exchange=self._exchange,
                queue=self.queue_name,
                routing_key=routing_key
            )


    
    def callback(self, channel, method, properties, body):
        try:
            message = json.loads(body.decode())
            logging.info(f'Queue: {self.queue_name} received message: {message}')

            sensor_type = message.get('type')
            chunk_id = message.get('chunk_id')
            if self.queue_name=="bites_queue":
                self.data_processor.process_bites(sensor_type, chunk_id, channel, method)
            elif self.queue_name=="steps_queue":
                self.data_processor.process_steps(chunk_id, channel, method)

        except Exception as e:
            logging.error(f'Error while processing message of {self.queue_name}: {e}')
   

    def get_messages(self):
        try:
            logging.info(f'Starting the {self.queue_name} receiver...')
            self._channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.callback,  
                auto_ack=False
            )
            self._channel.start_consuming()
        except Exception as e:
            logging.debug(f'Exception: {e}')
