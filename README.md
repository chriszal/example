# Example component relevium test

This example contains a simple falcon wsgi gunicorn REST API that has access to mongodb and influxdb. With the bellow endpoints we can list clinicians from mongo and we can post gzipped data to influx. While posting new sensor/ singal data to influx the rabbitmq producer is triggered which will start the rabbitmq process pipeline which we have more information on the relevium-test repo. This example also contains all receiver codes needed.

### Endpoints

Below is a list of the available endpoints in the API:

1. List clinicians

    `GET /api/v1/clinicians`
2. Post a measurement 

    `POST /api/v1/measurement/`

    ```
    --form file='@g_s_RELEVIUM-01-02_20230526_15.gz'
    ```