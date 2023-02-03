import logging
import json
import os
from confluent_kafka import Consumer, KafkaError

# Set up logging
logging.basicConfig(format='%(asctime)s %(threadName)s/%(thread)d %(levelname)s %(message)s', level=logging.INFO)

# Get the Kafka broker from the environment variable
kafka_broker = os.environ.get('KAFKA_BROKER')

# Define the Kafka consumer configuration
conf = {
    'bootstrap.servers': kafka_broker,
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

# Create the Kafka consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe(['test'])

# Continuously poll for new messages
while True:
    msg_batch = consumer.consume(num_messages=20, timeout=1.0)
    
    # Log the number of messages in the batch
    logging.info('Received %d messages in this batch', len(msg_batch))
    
    for msg in msg_batch:
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logging.info('Reached end of partition event for %s', msg.topic())
            else:
                logging.error('Error while polling for messages: %s', msg.error())
        else:
            # Log the received message
            message = json.loads(msg.value().decode('utf-8'))
            sleep_time = message['sleep_time']
            logging.info('Received message: sleep_time = %d', sleep_time)
