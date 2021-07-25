import json

from TwitterAPI import TwitterAPI
from dacite import from_dict

from src.authentication.twitter_auth import get_credentials
from src.player import Player
from src.search_relevant_tweets import SearchRelevantTweets


class TwitterForPlayer:
    def __init__(self, school: str, content: str):
        credentials = get_credentials()
        self.application_credentials = credentials.get('application_account')
        self.twitter_credentials = credentials.get(school)
        self.player: Player = from_dict(data_class=Player, data=json.loads(content))
        print(f'The Player: {self.player}')

    def send_tweet(self):
        print(f'Sending tweet to: {self.twitter_credentials.get("twitter_handle")}')

        twitter_api = TwitterAPI(
            consumer_key=self.application_credentials.get('consumer_key'),
            consumer_secret=self.application_credentials.get('consumer_secret'),
            access_token_key=self.application_credentials.get('access_token_key'),
            access_token_secret=self.application_credentials.get('access_token_secret'),
            api_version='2'
        )
        relevant_tweet = SearchRelevantTweets(twitter_api=twitter_api, player=self.player).search()
        print(f'The Relevant Tweet: {relevant_tweet}')
        relevant_tweet_id = relevant_tweet.get('id', None)

        if relevant_tweet_id and len(relevant_tweet_id) > 0:
            twitter_api_v1 = TwitterAPI(
                consumer_key=self.application_credentials.get('consumer_key'),
                consumer_secret=self.application_credentials.get('consumer_secret'),
                access_token_key=self.twitter_credentials.get('access_token_key'),
                access_token_secret=self.twitter_credentials.get('access_token_secret'),
            )

            response = twitter_api_v1.request(
                f'statuses/retweet/:{relevant_tweet_id}'
            )
            print(f'The response code: {response.status_code}')
            print(response.json())
