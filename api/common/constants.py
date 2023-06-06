# constants.py
import os
import json

def load_credentials(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

mongo_credentials = load_credentials('/var/mongo_credentials.json')
mongo_db_user = mongo_credentials.get("user")
mongo_db_password = mongo_credentials.get("password")
mongo_db_name = mongo_credentials.get("databases")[0].get("name")

MONGO = {
    'DATABASE': mongo_db_name,
    'HOST': 'mongodb',
    'PORT': 27017,
    'USERNAME': mongo_db_user,
    'PASSWORD': mongo_db_password
}

rabbitmq_credentials = load_credentials('/var/rabbitmq_credentials.json')
rabbit_name = rabbitmq_credentials.get("name")
rabbit_user = rabbitmq_credentials.get("user")
rabbit_password = rabbitmq_credentials.get("password")

RABBITMQ = {
    'USERNAME': rabbit_user,
    'PASSWORD': rabbit_password,
    'HOST': rabbit_name,
    'EXCHANGE': 'exchange_test'
}

influx_credentials = load_credentials('/var/influx_credentials.json')
token = influx_credentials.get("api_token")
bucket_name = influx_credentials.get("bucket").get("name")
org_name = influx_credentials.get("org").get("name")

INFLUXDB = {
    'HOST': os.environ.get('INFLUXDB_NAME'),
    'PORT': 8086,
    'ADMIN_TOKEN': token,
    'ORG': org_name,
    'BUCKET': bucket_name
}

