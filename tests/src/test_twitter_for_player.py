import json
from dataclasses import dataclass
from typing import List
from unittest.mock import patch, Mock, call

import pytest as pytest

from src.json_encoder import EnhancedJSONEncoder
from src.player import Player
from src.twitter_for_player import TwitterForPlayer


class TestTwitterForPlayer:
    @dataclass
    class Fixture:
        player: Player
        mock_twitter_api_constructor: Mock
        mock_twitter_api: Mock
        mock_search: Mock
        expected_twitter_api_constructor_calls: List
        expected_retweet_calls: List

    @dataclass
    class Param:
        player: Player
        expected_twitter_api_constructor_calls: List
        expected_retweet_calls: List
        search_return_value: dict

    @pytest.fixture(
        ids=['found relevant tweet', 'not found relevant tweet'],
        params=[
            Param(
                player=Player(full_name="Bo", league_name="mlb", college="fsu"),
                expected_twitter_api_constructor_calls=[
                    call(
                        consumer_key='1',
                        consumer_secret='2',
                        access_token_key='3',
                        access_token_secret='4',
                        api_version='2'
                    ),
                    call(
                        consumer_key='1',
                        consumer_secret='2',
                        access_token_key='7',
                        access_token_secret='8'
                    )
                ],
                expected_retweet_calls=[
                    call('statuses/retweet/:1')
                ],
                search_return_value ={'id': '1'}
            ),
            Param(
                player=Player(full_name="Bo", league_name="mlb", college="fsu"),
                expected_twitter_api_constructor_calls=[
                    call(
                        consumer_key='1',
                        consumer_secret='2',
                        access_token_key='3',
                        access_token_secret='4',
                        api_version='2'
                    )
                ],
                expected_retweet_calls=[],
                search_return_value ={}
            )
        ]
    )
    @patch('src.twitter_for_player.SearchRelevantTweets', autospec=True)
    @patch('src.twitter_for_player.get_credentials', autospec=True)
    @patch('src.twitter_for_player.TwitterAPI', autospec=True)
    def setup(self, mock_twitter_api_constructor, mock_credentials, mock_search, request):
        mock_search.return_value.search.return_value = request.param.search_return_value
        mock_twitter_api = mock_twitter_api_constructor.return_value
        mock_credentials.return_value = {
            'application_account': {
                'consumer_key': '1',
                'consumer_secret': '2',
                'access_token_key': '3',
                'access_token_secret': '4'
            },
            'fsu': {
                'consumer_key': '5',
                'consumer_secret': '6',
                'access_token_key': '7',
                'access_token_secret': '8'
            }
        }
        TwitterForPlayer(school='fsu', content=json.dumps(request.param.player, cls=EnhancedJSONEncoder)).send_tweet()

        return TestTwitterForPlayer.Fixture(
            player=request.param.player,
            mock_twitter_api=mock_twitter_api,
            mock_twitter_api_constructor=mock_twitter_api_constructor,
            mock_search=mock_search,
            expected_twitter_api_constructor_calls=request.param.expected_twitter_api_constructor_calls,
            expected_retweet_calls=request.param.expected_retweet_calls
        )

    def test_twitter_constructor(self, setup: Fixture):
        if setup.expected_retweet_calls:
            setup.mock_twitter_api_constructor.assert_has_calls(
                setup.expected_twitter_api_constructor_calls,
                any_order=True
            )
        else:
            assert setup.mock_twitter_api_constructor.mock_calls == setup.expected_twitter_api_constructor_calls

    def test_search_constructor(self, setup: Fixture):
        setup.mock_search.assert_called_once_with(twitter_api=setup.mock_twitter_api, player=setup.player)

    def test_search_called(self, setup: Fixture):
        setup.mock_search.return_value.search.assert_called_once()

    def test_retweet(self, setup: Fixture):
        if setup.expected_retweet_calls:
            setup.mock_twitter_api.request.assert_has_calls(setup.expected_retweet_calls, any_order=True)
        else:
            assert setup.mock_twitter_api.request.mock_calls == setup.expected_retweet_calls
