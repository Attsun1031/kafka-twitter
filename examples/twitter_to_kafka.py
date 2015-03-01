# -*- coding: utf-8 -*-
from multiprocessing import Process
from kafka import SimpleProducer, MultiProcessConsumer
from kafka_twitter import twitter_client, kafka_client


TRACK_TERM = '#nowplaying,#nowlistening'
topic = b'test-tweets'


def produce():
    kafka_producer = SimpleProducer(kafka_client)
    tweets = twitter_client.request('statuses/filter', {'track': TRACK_TERM})

    for item in filter(lambda t: 'text' in t, tweets):
        text = item['text']
        print('Input: {}'.format(text))
        kafka_producer.send_messages(topic, text.encode('utf8', 'replace'))


def multi_consumer_and_multi_partition():
    """
    コンシューマーグループに複数のコンシューマーを所属させて、各パーティンションをリッスンする。
    """
    consumer = MultiProcessConsumer(kafka_client, b'test-group', topic, num_procs=2)
    while True:
        # TODO: 最初のoffsetが毎回同じ。前回読んだものは読まないようにしたい。
        for msg in consumer:
            print(msg.message.value)


if __name__ == '__main__':
    producer_process = Process(target=produce)
    producer_process.start()
    multi_consumer_and_multi_partition()
