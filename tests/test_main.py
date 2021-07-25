import base64
import json
from dataclasses import dataclass
from unittest.mock import patch, Mock

import pytest

from main import entrypoint


class TestMain:
    @dataclass
    class Fixture:
        mock_twitter_for_player_constructor: Mock
        input_data: dict

    @dataclass
    class Param:
        input_data: dict

    @pytest.fixture(
        ids=['found relevant tweet'],
        params=[
            Param(
                input_data={},
            )
        ]
    )
    @patch('main.TwitterForPlayer', autospec=True)
    def setup(self, mock_twitter_for_player_constructor, request):
        mock_event = {
            'data': base64.b64encode(json.dumps(request.param.input_data).encode('utf-8')),
            'attributes': {
                'school': 'someSchool'
            }
        }
        entrypoint(event=mock_event, context={})

        return TestMain.Fixture(
            input_data=request.param.input_data,
            mock_twitter_for_player_constructor=mock_twitter_for_player_constructor
        )

    def test_twitter_for_player_constructor(self, setup: Fixture):
        setup.mock_twitter_for_player_constructor.assert_called_once_with(school='someSchool', content=json.dumps(setup.input_data))