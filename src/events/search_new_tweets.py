from datetime import datetime, timedelta
from typing import List

from TwitterAPI import TwitterAPI, TwitterRequestError, TwitterConnectionError, TwitterResponse

from src.events.decipher_school import decipher_school
from src.gcp.gcs import Gcs


class SearchNewTweets:
    def __init__(self, twitter_api: TwitterAPI, twitter_conditions: dict, event: str, league_name: str):
        self.event = event
        self.league_name = league_name
        self.twitter_api = twitter_api
        self.twitter_conditions = twitter_conditions

    def search(self) -> List:

        gcs = Gcs(bucket='special_events')
        most_recent_tweet_url = f'{self.event}_{self.league_name}.json'
        most_recent_tweet = gcs.read_as_dict(url=most_recent_tweet_url)

        try:
            query = f'(from:{" OR from:".join(self.twitter_conditions.get("twitter_accounts"))})'
            request_options = {
                'query': query,
                'tweet.fields': 'id,author_id'
            }

            most_recent_tweet_id = most_recent_tweet.get('id', None)
            print(most_recent_tweet_id)
            if most_recent_tweet_id and int(most_recent_tweet_id) > 0:
                request_options['since_id'] = most_recent_tweet.get('id')
            else:
                start_time = (datetime.now() - timedelta(hours=1)).isoformat(timespec='seconds')
                request_options['start_time'] = f'{start_time}Z'

            response: TwitterResponse = self.twitter_api.request(
                'tweets/search/recent', request_options
            )

            tweets_to_retweet = []
            max_id = '0'
            for tweet in response:
                current_id = tweet.get('id')
                max_id = current_id if int(current_id) > int(max_id) else max_id

                school = decipher_school(tweet_text=tweet.get('text'))
                if school:
                    tweets_to_retweet.append({
                        'school': school,
                        'tweet': tweet
                    })
            most_recent_tweet = {
                'id': max_id
            }
            if max_id != '0':
                gcs.write(url=most_recent_tweet_url, contents=most_recent_tweet)
            return tweets_to_retweet

        except TwitterRequestError as e:
            print(e.status_code)
            for msg in iter(e):
                print(msg)

        except TwitterConnectionError as e:
            print(e)
