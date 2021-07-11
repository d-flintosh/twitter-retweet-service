from dataclasses import dataclass
from typing import List
from unittest.mock import Mock, patch

import pytest
from TwitterAPI import TwitterAPI

from src.authentication.twitter_auth import get_credentials
from src.search_relevant_tweets import SearchRelevantTweets


@pytest.mark.skip(reason="this was only a test")
class TestSearchRelevantTweets:
    @dataclass
    class Params:
        mock_schedule_return: List

    @dataclass
    class Fixture:
        mock_client: Mock

    @pytest.fixture(
        ids=['No games found'],
        params=[
            Params(
                mock_schedule_return=[],
            )
        ]
    )
    def setup(self, request):
        credentials = get_credentials()
        application_credentials = credentials.get('application_account')
        twitter_api = TwitterAPI(
                consumer_key=application_credentials.get('consumer_key'),
                consumer_secret=application_credentials.get('consumer_secret'),
                access_token_key=application_credentials.get('access_token_key'),
                access_token_secret=application_credentials.get('access_token_secret'),
                api_version='2'
            )

        player = {
            'full_name': 'Francisco Lindor'
        }
        subject = SearchRelevantTweets(twitter_api=twitter_api, player=player)
        print(subject.search())

        return TestSearchRelevantTweets.Fixture(
            mock_client=Mock()
        )

    def test_foo(self, setup: Fixture):
        pass
