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

def test_register_page(client):

    response = client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data

def test_register_post(client):
    response = client.post("/register", data={
        "username":"hello",
        "password":"123",
    })
    assert response.status_code == 200

def test_login_page(client):

    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data

def test_login_post(client):
    response = client.post("/login", data={
        "username":"hello",
        "password":"123",
    })
    assert response.status_code == 302

def test_home_page(client):

    auth = client.post("/login", data={
    "username":"hello",
    "password":"123",
    })
    response = client.get("/home")
    assert response.status_code == 200
    assert b"My Tasks" in response.data
    
def test_add_page(client):

    response = client.get("/add")
    assert response.status_code == 200
    assert b"Add a Task" in response.data

def test_add_task(client):

    auth = client.post("/login", data={
    "username":"hello",
    "password":"123",
    })
    response = client.post("/add", data={
        "_id":ObjectId(),
        "title":"Title",
        "course":"Course",
        "date":"01/01/2024"                    
    })
    assert response.status_code == 302

def test_search_page(client):

    response = client.get("/search")
    assert response.status_code == 200
    assert b"Search Tasks" in response.data

def test_search_for_task(client):

    auth = client.post("/login", data={
    "username":"hello",
    "password":"123",
    })
    response = client.post("/search", data={
        "_id":ObjectId(),
        "course":"Course",                   
    })
    assert response.status_code == 200
    assert b"Tasks for" in response.data