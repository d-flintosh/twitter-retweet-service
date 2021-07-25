from dataclasses import dataclass
from datetime import datetime
from unittest.mock import Mock, call, patch, MagicMock

import pytest as pytest
from TwitterAPI import TwitterAPI, TwitterResponse

from src.player import Player
from src.search_relevant_tweets import SearchRelevantTweets


class TestSearchRelevantTweets:
    @dataclass
    class Fixture:
        actual: dict
        mock_twitter_api: Mock
        expected_time_search: str

    @dataclass
    class Param:
        player: Player
        expected_time_search: str

    @staticmethod
    def twitter_request_side_effect():
        return iter([
            {
                'id': '1',
                'public_metrics': {
                    'retweet_count': 3,
                    'reply_count': 3,
                    'like_count': 1,
                    'quote_count': 0
                }
            },
            {
                'id': '2',
                'public_metrics': {
                    'retweet_count': 3,
                    'reply_count': 3,
                    'like_count': 1,
                    'quote_count': 10
                }
            }
        ])

    @pytest.fixture(
        ids=['mlb', 'lpga'],
        params=[
            Param(
                player=Player(full_name="Bo", league_name="mlb", college="fsu"),
                expected_time_search='2021-06-30T19:00:00Z'
            ),
            Param(
                player=Player(full_name="Bo", league_name="lpga", college="fsu"),
                expected_time_search='2021-06-30T06:00:00Z'
            )
        ]
    )
    @patch('src.search_relevant_tweets.datetime', autospec=True)
    def setup(self, mock_datetime_now, request):
        mock_datetime_now.now.return_value = datetime(2021, 7, 1)
        mock_twitter_response = MagicMock(spec=TwitterResponse)
        mock_twitter_response.json.return_value = {
            'meta': {
                'next_token': '1234'
            }
        }
        mock_twitter_response.__iter__.side_effect = TestSearchRelevantTweets.twitter_request_side_effect
        mock_twitter_api = Mock(spec=TwitterAPI)
        mock_twitter_api.request.return_value = mock_twitter_response
        player = request.param.player

        return TestSearchRelevantTweets.Fixture(
            actual=SearchRelevantTweets(twitter_api=mock_twitter_api, player=player).search(),
            mock_twitter_api=mock_twitter_api,
            expected_time_search=request.param.expected_time_search
        )

    def test_twitter_request(self, setup: Fixture):
        setup.mock_twitter_api.request.assert_has_calls([
            call('tweets/search/recent', {
                'query': 'Bo -is:retweet has:videos has:media lang:en -is:reply -is:quote',
                'tweet.fields': 'id,author_id,public_metrics',
                'start_time': setup.expected_time_search
            }),
            call('tweets/search/recent', {
                'query': 'Bo -is:retweet has:videos has:media lang:en -is:reply -is:quote',
                'tweet.fields': 'id,author_id,public_metrics',
                'start_time': setup.expected_time_search,
                'next_token': '1234'
            })
        ], any_order=True)

    def test_return_value(self, setup: Fixture):
        assert setup.actual == {
            'id': '2',
            'public_metrics': {'like_count': 1,
                               'quote_count': 10,
                               'reply_count': 3,
                               'retweet_count': 3}
        }
