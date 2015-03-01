# -*- coding: utf-8 -*-
from kafka import SimpleProducer, KafkaConsumer, KafkaClient

cli = KafkaClient('localhost:9092')

def produce():
    producer = SimpleProducer(cli)
    producer.send_messages('my-replicated-topic', b'from python', b'multi message')


def consume():
    consumer = KafkaConsumer('my-replicated-topic', metadata_broker_list=[b'localhost:9092'])
    for m in consumer:
        print(m.value)
