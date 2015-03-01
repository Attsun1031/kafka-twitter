# -*- coding: utf-8 -*-
import os
from TwitterAPI import TwitterAPI
from kafka import KafkaClient


kafka_client = KafkaClient('localhost:9092')

twitter_client = TwitterAPI(os.environ.get('TWITTER_CONSUMER_KEY'),
                            os.environ.get('TWITTER_CONSUMER_SECRET'),
                            os.environ.get('TWITTER_ACCESS_KEY'),
                            os.environ.get('TWITTER_ACCESS_SECRET'))
