from collections import namedtuple
import csv
import os

import tweepy

from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_SECRET

DEST_DIR = 'data'
EXT = 'csv'
NUM_TWEETS = 100

Tweet = namedtuple('Tweet', 'id_str, created_at, text')


class UserTweets(object):

    def __init__(self, handle, max_id=None):
        '''Construct the UserTweets object for the given handle'''
        self._handle = handle
        self._max_id = max_id
        self.output_file = os.path.join(DEST_DIR, self._handle + "." + EXT)

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self._api = tweepy.API(auth)

        self._tweets = list(self._get_tweets())
        self._save_to_csv()

    def _get_tweets(self):
        '''Get tweets for this user via the Twitter API'''
        last_hundred = self._api.user_timeline(self._handle,
                                               max_id=self._max_id,
                                               count=NUM_TWEETS)

        for status in last_hundred:
            yield Tweet(status.id_str, status.created_at, status.text)

    def _save_to_csv(self):
        '''Save tweets for this user to DEST_DIR/{handle}.csv'''
        with open(self.output_file, "w") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(Tweet._fields)
            writer.writerows(self)

    def __len__(self):
        return len(self._tweets)

    def __getitem__(self, i):
        return self._tweets[i]


if __name__ == "__main__":

    for handle in ('pybites', 'techmoneykids', 'bbelderbos'):
        print('--- {} ---'.format(handle))
        user = UserTweets(handle)
        for tw in user[:5]:
            print(tw)
        print()
