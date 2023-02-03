import logging
import json
import os
import time
import threading
from confluent_kafka import Consumer, KafkaError


def process_msg(msg):
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            logging.info('Reached end of partition event for %s', msg.topic())
        else:
            logging.error('Error while polling for messages: %s', msg.error())
    else:
        # Log the received message
        message = json.loads(msg.value().decode('utf-8'))
        sleep_time = message['sleep_time']
        logging.info('Going to sleep for %d s', sleep_time)
        # Sleep for sleep_time seconds
        time.sleep(sleep_time)


def consume_messages(config,topic,size,multi_thread):
    # Create the Kafka consumer instance
    consumer = Consumer(config)

    # Subscribe to the topic
    consumer.subscribe([topic]) 
    
    # Set a batch number to track batches
    batch_num  = 0
    
    # Continuously poll for new messages
    while True:
        logging.info('Number of threads currently running: %d', len(threading.enumerate()))
        msg_batch = consumer.consume(num_messages=size, timeout=1.0)
        # Log the number of messages in the batch
        logging.info('Received %d messages in this batch', len(msg_batch))
        if len(msg_batch) == 0:
            logging.info('No Messages to process')
            continue
        
        start_time = time.time()
        
        if multi_thread == 'true':
            threads = []
            for msg in msg_batch:
                t = threading.Thread(target=process_msg, args=(msg,))
                threads.append(t)
                t.start()
                
            for t in threads:
                t.join()
                
        else:
            for msg in msg_batch:
                process_msg(msg)
                
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info("Batch %d processing time: %s seconds",  batch_num, elapsed_time)
        logging.info('Committing offsets for batch: %d', batch_num)
        # Commit the offset of the last message in the batch
        consumer.commit(msg_batch[-1])
        # Increment batch number
        batch_num += 1


if __name__ == '__main__':
    # Get the Kafka broker from an environment variable
    kafka_broker = os.environ.get('KAFKA_BROKER')

    # Get the recommended batch size from an environment variable
    batch_size = int(os.environ.get('BATCH_SIZE'))
    
    # Get topic name from environment variable
    topic = os.getenv('KAFKA_TOPIC', 'test')

    # Check if multithreading is enabled
    multi_thread = os.environ.get('MULTI_THREAD')
    
    # Create a consumer group name based on threads used
    if multi_thread == 'true':
        consumer_group = 'single-threaded-group'
    else:
        consumer_group = 'multi-threaded-group'

    # Set up logging
    logging.basicConfig(
        format='%(asctime)s %(threadName)s/%(thread)d %(levelname)s %(message)s',
        level=logging.INFO
    )
    
    # Define the Kafka consumer configuration
    conf = {
        'bootstrap.servers': kafka_broker,
        'group.id': 'my-group',
        'auto.offset.reset': 'earliest'
    }
    
    consume_messages(conf,topic,batch_size,multi_thread)
    
    
