import json
from datetime import datetime, timedelta

from TwitterAPI import TwitterAPI, TwitterRequestError, TwitterConnectionError

from src.authentication.twitter_auth import get_credentials
from src.search_relevant_tweets import SearchRelevantTweets


class Twitter:
    def __init__(self, school: str):
        credentials = get_credentials()
        self.application_credentials = credentials.get('application_account')
        self.twitter_credentials = credentials.get(school)

    def send_tweet(self, content: str):
        print(f'Sending tweet to: {self.twitter_credentials.get("twitter_handle")}')
        print(f'The Content: {content}')

        twitter_api = TwitterAPI(
            consumer_key=self.application_credentials.get('consumer_key'),
            consumer_secret=self.application_credentials.get('consumer_secret'),
            access_token_key=self.application_credentials.get('access_token_key'),
            access_token_secret=self.application_credentials.get('access_token_secret'),
            api_version='2'
        )
        relevant_tweet = SearchRelevantTweets(twitter_api=twitter_api, player=json.loads(content)).search()
        print(f'The Relevant Tweet: {relevant_tweet}')
        relevant_tweet_id = relevant_tweet.get('id')

        if len(relevant_tweet_id) > 0:
            twitter_api_v1 = TwitterAPI(
                consumer_key=self.application_credentials.get('consumer_key'),
                consumer_secret=self.application_credentials.get('consumer_secret'),
                access_token_key=self.twitter_credentials.get('access_token_key'),
                access_token_secret=self.twitter_credentials.get('access_token_secret'),
            )

            response = twitter_api_v1.request('statuses/retweet', {'id': relevant_tweet_id})
            print(f'The response code: {response.status_code}')
