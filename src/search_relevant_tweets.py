import json
from datetime import datetime, timedelta
from typing import Union, Optional

from TwitterAPI import TwitterAPI, TwitterRequestError, TwitterConnectionError, TwitterResponse


class SearchRelevantTweets:
    def __init__(self, twitter_api: TwitterAPI, player: dict):
        self.twitter_api = twitter_api
        self.player = player

    def search(self) -> dict:
        query = f'{self.player.get("full_name")} -is:retweet has:videos has:media lang:en -is:reply -is:quote'
        first_pass = self.make_request(query=query)
        print(first_pass)
        second_pass = self.make_request(query=query, next_token=first_pass.get('next_token'))
        print(second_pass)
        return first_pass.get('most_shared_tweet') if first_pass.get('shares') >= second_pass.get('shares') else second_pass.get('most_shared_tweet')

    def make_request(self, query: str, next_token: Optional[str] = None):
        start_time = (datetime.now() - timedelta(hours=5)).isoformat(timespec='seconds')

        try:
            request_options = {
                'query': query,
                'tweet.fields': 'id,author_id,public_metrics',
                'start_time': f'{start_time}Z'
            }
            if next_token:
                request_options['next_token'] = next_token

            response: TwitterResponse = self.twitter_api.request(
                'tweets/search/recent', request_options
            )

            most_shared_tweet = {}
            previous_max_shares = 0
            for tweet in response:
                public_metrics = tweet.get('public_metrics', {})
                current_shares = public_metrics.get('retweet_count', 0) + public_metrics.get('reply_count', 0) + public_metrics.get('like_count', 0) + public_metrics.get('quote_count', 0)

                if current_shares >= previous_max_shares:
                    most_shared_tweet = tweet
                    previous_max_shares = current_shares

            return {
                'next_token': response.json().get('meta').get('next_token'),
                'shares': previous_max_shares,
                'most_shared_tweet': most_shared_tweet
            }

        except TwitterRequestError as e:
            print(e.status_code)
            for msg in iter(e):
                print(msg)

        except TwitterConnectionError as e:
            print(e)
