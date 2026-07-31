#!/usr/bin/env python3

"""Tests for `bed2ucsc`"""

import pytest

from bed2ucsc import bed2ucsc


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/engineervix/cookiecutter-pyproject')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


class TestBed2ucsc():
    """Tests the bed2ucsc module"""

    @staticmethod
    def test_addition():
        """tests for addition"""
        assert bed2ucsc.add(2, 2) == 4  # nosec

    @staticmethod
    def test_subtraction():
        """tests for subtraction"""
        assert bed2ucsc.subtract(4, 2) == 2  # nosec
