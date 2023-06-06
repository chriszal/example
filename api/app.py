import falcon
import mongoengine as mongo
from falcon_multipart.middleware import MultipartMiddleware
import api.common.constants as constants
from api.common.cors import Cors
from api.resource.measurements_resource import MeasurementResource
from api.resource.clinicians_resource import CliniaciansResource
import json 
from api.rabbitmq import RabbitMQ

import logging

logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )


mongo.connect(
    constants.MONGO['DATABASE'],
    host=constants.MONGO['HOST'],
    port=constants.MONGO['PORT'],
    username=constants.MONGO['USERNAME'],
    password=constants.MONGO['PASSWORD'],
    authentication_source=constants.MONGO['DATABASE'],
    authentication_mechanism='SCRAM-SHA-256'
)


rabbitMQ_instance = RabbitMQ(
    host=constants.RABBITMQ['HOST'],
    username=constants.RABBITMQ['USERNAME'],
    password=constants.RABBITMQ['PASSWORD'],
    exchange=constants.RABBITMQ['EXCHANGE']
)



app = falcon.App(middleware=[Cors(),MultipartMiddleware()])

measurement = MeasurementResource(rabbitMQ_instance,constants.INFLUXDB,logging)
clinicians = CliniaciansResource()

app.add_route('/api/v1/clinicians', clinicians)
app.add_route('/api/v1/measurement/',measurement)


# Add health check endpoint

class HealthResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {"status": "healthy"}

health = HealthResource()
app.add_route("/api/v1/health", health)


