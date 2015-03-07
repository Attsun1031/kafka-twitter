# -*- coding: utf-8 -*-
from multiprocessing import Process
from kafka import SimpleProducer, MultiProcessConsumer, KafkaConsumer
from kafka_twitter import twitter_client, kafka_client


TRACK_TERM = '#nowplaying,#nowlistening'
topic = b'Tweets'


def produce():
    kafka_producer = SimpleProducer(kafka_client)
    tweets = twitter_client.request('statuses/filter', {'track': TRACK_TERM})

    for item in filter(lambda t: 'text' in t, tweets):
        text = item['text']
        kafka_producer.send_messages(topic, text.encode('utf8', 'replace'))


def single_consumer(name):
    """
    一つのコンシューマーがリッスン
    """
    consumer = KafkaConsumer(topic, metadata_broker_list=['localhost:9092'])
    while True:
        for message in consumer:
            print(name, message.value)


def multi_consumer_and_multi_partition():
    """
    コンシューマーグループに複数のコンシューマーを所属させて、各パーティンションをリッスンする。
    """
    consumer = MultiProcessConsumer(kafka_client, b'test-group', topic, num_procs=2,
                                    auto_commit_every_n=10)
    while True:
        for msg in consumer:
            print(msg.message.value)


if __name__ == '__main__':
    producer_process = Process(target=produce)
    producer_process.start()

    # 一つのストリームをコンシューマーグループがパーティションごとにリッスンする
    # multi_consumer_and_multi_partition()

    # 同じストリームを別々のコンシューマーがリッスンする
    consumer1 = Process(target=single_consumer, args=('p1',))
    consumer2 = Process(target=single_consumer, args=('p2',))
    consumer1.start()
    consumer2.start()

    producer_process.join()
    consumer1.join()
    consumer2.join()
