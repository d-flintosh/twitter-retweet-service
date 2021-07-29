from dataclasses import dataclass
from datetime import datetime
from typing import List, Callable
from unittest.mock import Mock, patch, MagicMock

import pytest as pytest
from TwitterAPI import TwitterAPI, TwitterResponse

from src.events.search_new_tweets import SearchNewTweets


def decipher_school_side_effect(tweet_text: str):
    if tweet_text == 'some other text':
        return 'someSchool'
    else:
        return None


def decipher_school_side_effect_none(tweet_text: str):
    return None


class TestSearchNewTweets:
    @dataclass
    class Fixture:
        actual: List
        mock_twitter_api: Mock
        mock_gcs_constructor: Mock
        mock_gcs: Mock
        expected_options: dict
        expected: List

    @dataclass
    class Param:
        read_as_dict: dict
        mock_twitter_conditions: dict
        expected_options: dict
        decipher_school_side_effect: Callable
        expected: List

    @staticmethod
    def twitter_request_side_effect():
        return iter([
            {
                'id': '100',
                'text': 'some other text'
            },
            {
                'id': '2',
                'text': 'some text'
            }
        ])

    @pytest.fixture(
        ids=['no previous tweet', 'no valid previous tweet', 'has previous tweet', 'found school', 'multiple twitter accounts'],
        params=[
            Param(
                read_as_dict={'id': '0'},
                mock_twitter_conditions={
                    'twitter_accounts': ['someTwitterHandle']
                },
                expected_options={'query': '(from:someTwitterHandle)', 'tweet.fields': 'id,author_id', 'start_time': '2021-06-30T23:00:00Z'},
                decipher_school_side_effect=decipher_school_side_effect_none,
                expected=[]
            ),
            Param(
                read_as_dict={},
                mock_twitter_conditions={
                    'twitter_accounts': ['someTwitterHandle']
                },
                expected_options={'query': '(from:someTwitterHandle)', 'tweet.fields': 'id,author_id', 'start_time': '2021-06-30T23:00:00Z'},
                decipher_school_side_effect=decipher_school_side_effect_none,
                expected=[]
            ),
            Param(
                read_as_dict={'id': '2'},
                mock_twitter_conditions={
                    'twitter_accounts': ['someTwitterHandle']
                },
                expected_options={'query': '(from:someTwitterHandle)', 'tweet.fields': 'id,author_id', 'since_id': '2'},
                decipher_school_side_effect=decipher_school_side_effect_none,
                expected=[]
            ),
            Param(
                read_as_dict={'id': '2'},
                mock_twitter_conditions={
                    'twitter_accounts': ['someTwitterHandle']
                },
                expected_options={'query': '(from:someTwitterHandle)', 'tweet.fields': 'id,author_id', 'since_id': '2'},
                decipher_school_side_effect=decipher_school_side_effect,
                expected=[{'school': 'someSchool', 'tweet': {'id': '100', 'text': 'some other text'}}]
            ),
            Param(
                read_as_dict={},
                mock_twitter_conditions={
                    'twitter_accounts': ['someTwitterHandle', 'anotherTwitterHandle']
                },
                expected_options={'query': '(from:someTwitterHandle OR from:anotherTwitterHandle)', 'tweet.fields': 'id,author_id', 'start_time': '2021-06-30T23:00:00Z'},
                decipher_school_side_effect=decipher_school_side_effect,
                expected=[{'school': 'someSchool', 'tweet': {'id': '100', 'text': 'some other text'}}]
            )
        ]
    )
    @patch('src.events.search_new_tweets.decipher_school', autospec=True)
    @patch('src.events.search_new_tweets.Gcs', autospec=True)
    @patch('src.events.search_new_tweets.datetime', autospec=True)
    def setup(self, mock_datetime_now, mock_gcs_constructor, mock_decipher_school, request):
        mock_datetime_now.now.return_value = datetime(2021, 7, 1)
        mock_gcs = mock_gcs_constructor.return_value
        mock_gcs.read_as_dict.return_value = request.param.read_as_dict
        mock_decipher_school.side_effect = request.param.decipher_school_side_effect

        mock_twitter_response = MagicMock(spec=TwitterResponse)
        mock_twitter_response.__iter__.side_effect = TestSearchNewTweets.twitter_request_side_effect
        mock_twitter_api = Mock(spec=TwitterAPI)
        mock_twitter_api.request.return_value = mock_twitter_response

        mock_twitter_conditions = request.param.mock_twitter_conditions

        actual = SearchNewTweets(
            twitter_api=mock_twitter_api,
            twitter_conditions=mock_twitter_conditions,
            event='some_event',
            league_name='some_league'
        ).search()

        return TestSearchNewTweets.Fixture(
            actual=actual,
            mock_twitter_api=mock_twitter_api,
            mock_gcs_constructor=mock_gcs_constructor,
            mock_gcs=mock_gcs,
            expected_options=request.param.expected_options,
            expected=request.param.expected
        )

    def test_gcs_constructor(self, setup: Fixture):
        setup.mock_gcs_constructor.assert_called_once_with(bucket='special_events')

    def test_gcs_read(self, setup: Fixture):
        setup.mock_gcs.read_as_dict.assert_called_once_with(url='some_event_some_league.json')

    def test_gcs_write(self, setup: Fixture):
        setup.mock_gcs.write.assert_called_once_with(url='some_event_some_league.json', contents={'id': '100'})

    def test_twitter_api_request(self, setup: Fixture):
        setup.mock_twitter_api.request.assert_called_once_with(
            'tweets/search/recent', setup.expected_options
        )

    def test_response(self, setup: Fixture):
        assert setup.actual == setup.expected
