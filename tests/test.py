import pytest
import os

from app import *
from app import app

@pytest.fixture

def test_sanity_check(client):

    expected = True
    actual = True
    assert actual == expected, "Expected True to be equal to True!"

def test_sanity_check2(client):

    expected = True
    actual = True
    assert actual == expected, "Expected True to be equal to True!"