import json
from dataclasses import dataclass

import pytest as pytest

from src.twitter import Twitter


@pytest.mark.skip(reason="this was only a test")
class TestTwitter:
    @dataclass
    class Fixture:
        temp: bool

    @pytest.fixture
    def setup(self):
        test_tweet = {
            'full_name': 'Francisco Lindor'
        }
        Twitter(school='connecticut').send_tweet(content=json.dumps(test_tweet))

        return TestTwitter.Fixture(
            temp=True
        )

    def test_twitter_constructor(self, setup: Fixture):
        pass
