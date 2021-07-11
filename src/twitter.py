import json
from datetime import datetime, timedelta

from TwitterAPI import TwitterAPI, TwitterRequestError, TwitterConnectionError

from src.authentication.twitter_auth import get_credentials


class Twitter:
    def __init__(self, school: str):
        credentials = get_credentials()
        self.application_credentials = credentials.get('application_account')
        self.twitter_credentials = credentials.get(school)

    def send_tweet(self, content: str):
        print(f'Sending tweet to: {self.twitter_credentials.get("twitter_handle")}')
        print(content)
        # twitter_api = TwitterAPI(
        #     consumer_key=self.application_credentials.get('consumer_key'),
        #     consumer_secret=self.application_credentials.get('consumer_secret'),
        #     access_token_key=self.application_credentials.get('access_token_key'),
        #     access_token_secret=self.application_credentials.get('access_token_secret'),
        #     api_version='2'
        # )
        # player_object = json.loads(content)
        #
        # start_time = (datetime.now() - timedelta(hours=5)).isoformat(timespec='seconds')

        # try:
        #     # r = twitter_api.request(
        #     #     'tweets/search/recent', {
        #     #         'query': player_object.get('full_name'),
        #     #         'tweet.fields': 'author_id,public_metrics',
        #     #         'expansions': 'author_id,referenced_tweets.id',
        #     #         'start_time': f'{start_time}Z'
        #     #     }
        #     # )
        #     ids = ','.join(['1414287019388383236'])
        #
        #     r = twitter_api.request(
        #         'tweets', {
        #             'ids': ids,
        #             'tweet.fields': 'author_id,public_metrics',
        #             'expansions': 'author_id,referenced_tweets.id',
        #             'user.fields': 'public_metrics'
        #         }
        #     )
        #
        #     for item in r:
        #         print(item)
        #
        #     print('\nINCLUDES')
        #     print(r.json()['includes'])
        #
        #     print('\nQUOTA')
        #     print(r.get_quota())
        #
        # except TwitterRequestError as e:
        #     print(e.status_code)
        #     for msg in iter(e):
        #         print(msg)
        #
        # except TwitterConnectionError as e:
        #     print(e)
        #
        # except Exception as e:
        #     print(e)
