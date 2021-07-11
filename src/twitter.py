from TwitterAPI import TwitterAPI

from src.authentication.twitter_auth import get_credentials


class Twitter:
    def __init__(self, school: str):
        credentials = get_credentials()
        self.application_credentials = credentials.get('application_account')
        self.twitter_credentials = credentials.get(school)

    def send_tweet(self, content: str):
        self._send_tweet(
            application_credentials=self.application_credentials,
            twitter_credentials=self.twitter_credentials,
            content=content
        )

    def _send_tweet(self, application_credentials: dict, twitter_credentials: dict, content: str):
        print(f'Sending tweet to: {twitter_credentials.get("twitter_handle")}')
        twitter_api = TwitterAPI(
            consumer_key=application_credentials.get('consumer_key'),
            consumer_secret=application_credentials.get('consumer_secret'),
            access_token_key=twitter_credentials.get('access_token_key'),
            access_token_secret=twitter_credentials.get('access_token_secret')
        )

        print(content)
        # response = twitter_api.request('statuses/update', {'status': tweet})
        # print(f'The response code: {response.status_code}')

