import base64
import json
from dataclasses import dataclass
from typing import List
from unittest.mock import patch, Mock, call

import pytest

from main import entrypoint


class TestMain:
    @dataclass
    class Fixture:
        mock_twitter_for_player_constructor: Mock
        mock_twitter_for_event_constructor: Mock
        input_data: dict
        expected_twitter_for_player_calls: List
        expected_twitter_for_event_calls: List

    @dataclass
    class Param:
        input_data: dict
        input_attributes: dict
        expected_twitter_for_player_calls: List
        expected_twitter_for_event_calls: List

    @pytest.fixture(
        ids=['twitter for player', 'twitter for special event'],
        params=[
            Param(
                input_data={},
                input_attributes={
                    'school': 'someSchool'
                },
                expected_twitter_for_player_calls=[
                    call(school='someSchool', content=json.dumps({})),
                    call().send_tweet()
                ],
                expected_twitter_for_event_calls=[]
            ),
            Param(
                input_data={},
                input_attributes={
                    'event': 'someEvent'
                },
                expected_twitter_for_player_calls=[],
                expected_twitter_for_event_calls=[
                    call(attributes={'event': 'someEvent'}),
                    call().find_retweet()
                ]
            )
        ]
    )
    @patch('main.TwitterForEvent', autospec=True)
    @patch('main.TwitterForPlayer', autospec=True)
    def setup(self, mock_twitter_for_player_constructor, mock_twitter_for_event_constructor, request):
        mock_event = {
            'data': base64.b64encode(json.dumps(request.param.input_data).encode('utf-8')),
            'attributes': request.param.input_attributes
        }
        entrypoint(event=mock_event, context={})

        return TestMain.Fixture(
            input_data=request.param.input_data,
            mock_twitter_for_player_constructor=mock_twitter_for_player_constructor,
            mock_twitter_for_event_constructor=mock_twitter_for_event_constructor,
            expected_twitter_for_player_calls=request.param.expected_twitter_for_player_calls,
            expected_twitter_for_event_calls=request.param.expected_twitter_for_event_calls
        )

    def test_twitter_for_player_constructor(self, setup: Fixture):
        assert setup.mock_twitter_for_player_constructor.mock_calls == setup.expected_twitter_for_player_calls

    def test_twitter_for_event_constructor(self, setup: Fixture):
        assert setup.mock_twitter_for_event_constructor.mock_calls == setup.expected_twitter_for_event_calls
