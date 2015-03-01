# -*- coding: utf-8 -*-
import os
from TwitterAPI import TwitterAPI


TRACK_TERM = '#nowplaying,#nowlistening'

CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.environ.get('TWITTER_ACCESS_KEY')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')


if __name__ == '__main__':
    api = TwitterAPI(CONSUMER_KEY,
                     CONSUMER_SECRET,
                     ACCESS_TOKEN_KEY,
                     ACCESS_TOKEN_SECRET)

    r = api.request('statuses/filter', {'track': TRACK_TERM})

    for item in r:
        print(item['text'] if 'text' in item else item)
