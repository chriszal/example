import pandas as pd
# from api.model.accel_processed import AccelProcessed
import requests
import logging
import os

class DataProcessor:
    def __init__(self, influx_name,influx_port, influx_token, influx_org, influx_bucket):
        self._influx_name = influx_name
        self._influx_port = influx_port
        self._influx_token = influx_token
        self._influx_org = influx_org
        self._influx_bucket = influx_bucket

    def process_steps(self, chunk_id,channel,method):
        response = self.fetch_data(chunk_id)
        
        if response.status_code == 200:
            if response.headers.get('Content-Encoding', '') == 'gzip':
                try:
                    with open(f'{chunk_id}.csv', 'wb') as f:
                        f.write(response.content)

                    if os.stat(f'{chunk_id}.csv').st_size == 0:
                        logging.info(f'File {chunk_id}.csv is empty.')
                    else:
                        df = pd.read_csv(f'{chunk_id}.csv')
                        df = df.pivot(index='_time', columns='_field', values='_value')
                        logging.info(df.head())
                        # Now i can access 'x', 'y', and 'z' as columns directly
                        x_values = df['x']
                        y_values = df['y']
                        z_values = df['z']

                         # Convert the '_time' index to datetime
                        df.index = pd.to_datetime(df.index, errors='coerce')

                        # Get the start and end dates
                        start_date = df.index.min()
                        end_date = df.index.max()

                        # accel_processed = AccelProcessed(chunk_id=chunk_id, start_date=start_date, end_date=end_date)
                        # accel_processed.save()
                except Exception as e: 
                    logging.error(f'Failed to process data for chunk_id: {e}')


            else:
               logging.info(f'The chunk_id: {chunk_id}, was not found in InfluxDB.')

        else:
            logging.error('Failed to fetch data from InfluxDB')
        channel.basic_ack(delivery_tag=method.delivery_tag)


    def process_bites(self, sensor_type, chunk_id, channel, method):
        
        # Replace 'a' with 'g' and vice versa in the chunk_id
        other_type = 'a' if sensor_type == 'g' else 'g'
        other_chunk_id = other_type + chunk_id[1:]

        # Fetch data for the corresponding other chunk_id
        other_data_response = self.fetch_data(other_chunk_id)
        
        if other_data_response.status_code == 200 and other_data_response.headers.get('Content-Encoding', '') == 'gzip':
            logging.info(f'Found corresponding <<{other_type}>> type of data for {chunk_id}. Proceed to process bites.')
            # process the bite
        else:
            logging.info(f'Corresponding <<{other_type}>> type of data for {chunk_id} was not found. Waiting for the data to arrive.')
        channel.basic_ack(delivery_tag=method.delivery_tag)
    
    def fetch_data(self, chunk_id):
        data = f'from(bucket:"{self._influx_bucket}") |> range(start:-1000000h) |> filter(fn: (r) => r.chunk_id == "{chunk_id}")'
        response = requests.post(
            f'http://{self._influx_name}:{self._influx_port}/api/v2/query?org={self._influx_org}',
            headers={
                'Authorization': f'Token {self._influx_token}',
                'Accept': 'application/csv',
                'Accept-Encoding': 'gzip',
                'Content-type': 'application/vnd.flux'
            },
            data=data
        )
        return response