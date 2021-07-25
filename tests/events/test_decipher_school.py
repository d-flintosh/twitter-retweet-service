from dataclasses import dataclass
from typing import Union

import pytest as pytest

from src.events.decipher_school import decipher_school


class TestDecipherSchool:
    @dataclass
    class Fixture:
        actual: Union[None, str]
        expected: Union[None, str]

    @dataclass
    class Param:
        expected: Union[None, str]
        input_string: str

    @pytest.fixture(
        ids=['none', 'fsu', 'found with mismatched case'],
        params=[
            Param(
                input_string='falalalallala words do not match',
                expected=None
            ),
            Param(
                input_string='some words fsu more words',
                expected='fsu'
            ),
            Param(
                input_string='some words @FSUHoops more words',
                expected='fsu'
            )
        ]
    )
    def setup(self, request):
        return TestDecipherSchool.Fixture(
            actual=decipher_school(tweet_text=request.param.input_string),
            expected=request.param.expected
        )

    def test_decipher_school(self, setup: Fixture):
        assert setup.expected == setup.actual

