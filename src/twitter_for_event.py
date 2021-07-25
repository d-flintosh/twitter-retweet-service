from TwitterAPI import TwitterAPI

from src.authentication.twitter_auth import get_credentials
from src.events.event_list import events
from src.events.search_new_tweets import SearchNewTweets


class TwitterForEvent:
    def __init__(self, attributes: dict):
        self.credentials = get_credentials()
        self.application_credentials = self.credentials.get('application_account')
        self.event = attributes.get('event')
        self.league_name = attributes.get('league_name')
        self.twitter_conditions = events.get(self.event).get(self.league_name)

    def find_retweet(self):
        twitter_api = TwitterAPI(
            consumer_key=self.application_credentials.get('consumer_key'),
            consumer_secret=self.application_credentials.get('consumer_secret'),
            access_token_key=self.application_credentials.get('access_token_key'),
            access_token_secret=self.application_credentials.get('access_token_secret'),
            api_version='2'
        )
        relevant_tweets = SearchNewTweets(
            twitter_api=twitter_api,
            twitter_conditions=self.twitter_conditions,
            event=self.event,
            league_name=self.league_name
        ).search()

        for relevant_tweet in relevant_tweets:
            print(f'The Relevant Tweet: {relevant_tweet}')
            twitter_api_v1 = TwitterAPI(
                consumer_key=self.application_credentials.get('consumer_key'),
                consumer_secret=self.application_credentials.get('consumer_secret'),
                access_token_key=self.credentials.get(relevant_tweet.get('school')).get('access_token_key'),
                access_token_secret=self.credentials.get(relevant_tweet.get('school')).get('access_token_secret'),
            )

            response = twitter_api_v1.request(
                f'statuses/retweet/:{relevant_tweet.get("tweet").get("id")}'
            )
            print(f'The response code: {response.status_code}')
            print(response.json())
