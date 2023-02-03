import json
import logging
import os
import random
import time

from confluent_kafka import Producer


def delivery_report(err, msg):
    if err is not None:
        logging.error('Message delivery failed: {}'.format(err))
    else:
        logging.info('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def produce_loop(producer):
    topic = "test"
    while True:
        sleep_time = random.randint(1, 10)
        payload = {'sleep_time': sleep_time}
        producer.produce(topic, value=json.dumps(payload).encode('utf-8'), callback=delivery_report)
        producer.poll(0)
        time.sleep(1)


if __name__ == '__main__':
    broker = os.getenv('KAFKA_BROKER', 'localhost:9092')

    conf = {
        'bootstrap.servers': broker,
        'client.id': 'python_producer'
    }

    logging.basicConfig(
        format='%(asctime)s %(threadName)s/%(thread)d %(levelname)s %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger('python_producer')

    producer = Producer(conf)

    produce_loop(producer)

