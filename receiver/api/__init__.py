import logging
import mongoengine as mongo
from api.enum import EnvironmentVariables
from api.rabbitmq import RabbitMQReceiver
import threading
import json


def load_credentials(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def create_rabbitmq_receiver(name, user, password,exchange, queue_name, token, org_name, bucket_name, routing_keys):
    return RabbitMQReceiver(
        host=name,
        username=user,
        password=password,
        exchange=exchange,
        routing_keys=routing_keys,
        queue=queue_name,
        influx_name=EnvironmentVariables.INFLUXDB_NAME.get_env(),
        influx_port=8086,
        influx_token=token,
        influx_org=org_name,
        influx_bucket=bucket_name
    )


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    mongo_credentials = load_credentials('/var/mongo_credentials.json')
    mongo_db_user = mongo_credentials.get("user")
    mongo_db_password = mongo_credentials.get("password")
    mongo_db_name = mongo_credentials.get("databases")[0].get("name")

    mongo.connect(
        mongo_db_name,
        host="mongodb",
        port=27017,
        username=mongo_db_user,
        password=mongo_db_password,
        authentication_source=mongo_db_name,
        authentication_mechanism='SCRAM-SHA-256'
    )

    influx_credentials = load_credentials('/var/influx_credentials.json')
    token = influx_credentials.get("api_token")
    bucket_name = influx_credentials.get("bucket").get("name")
    org_name = influx_credentials.get("org").get("name")

    rabbitmq_credentials = load_credentials('/var/rabbitmq_credentials.json')
    rabbit_name = rabbitmq_credentials.get("name")
    rabbit_user = rabbitmq_credentials.get("user")
    rabbit_password = rabbitmq_credentials.get("password")

    receiver_bites = create_rabbitmq_receiver(
        rabbit_name, rabbit_user, rabbit_password, "exchange_test",
        "bites_queue", token, org_name, bucket_name,
        ['smartwatch.accelerometer', 'smartwatch.gyroscope']
    )

    receiver_steps = create_rabbitmq_receiver(
        rabbit_name, rabbit_user, rabbit_password,"exchange_test",
        "steps_queue", token, org_name, bucket_name,
        ['*.accelerometer']
    )

    thread1 = threading.Thread(target=receiver_bites.get_messages)
    thread2 = threading.Thread(target=receiver_steps.get_messages)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()