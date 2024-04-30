import pytest
import os

from app import *
from app import app

@pytest.fixture
def client():
    app.config.update({
        "TESTING" : True,
    })
    with app.test_client() as client:
        yield client

def test_sanity_check(client):

    expected = True
    actual = True
    assert actual == expected

def test_sanity_check2(client):

    expected = True
    actual = True
    assert actual == expected

def test_reglog_page(client):

    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome Back to School Tasks Manager" in response.data

def test_login_page(client):

    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    