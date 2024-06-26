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
        "date":"2024-01-01"                    
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

def test_edit_task_page(client):

    auth = client.post("/login", data={
    "username":"hello",
    "password":"123",
    })
    user_id = ObjectId(current_user.id)
    user = db.users.find_one({'_id': user_id})
    add = client.post("/add", data={
        "_id":ObjectId(),
        "title":"Title",
        "course":"Course",
        "date":"2024-01-01"
    })
    tasks = user['tasks']
    print(user_id)
    task_id = tasks[0]["_id"]
    print(task_id)
    response = client.get('/edit/6631d62dabefdc3dc9d3d2cb/6631d62dabefdc3dc9d3d2cd')
    assert response.status_code == 200
    assert b"Edit Task" in response.data

def test_edit_task(client):

    auth = client.post("/login", data={
    "username":"hello",
    "password":"123",
    })
    user_id = ObjectId(current_user.id)
    user = db.users.find_one({'_id': user_id})
    add = client.post("/add", data={
        "_id":ObjectId(),
        "title":"Title",
        "course":"Course",
        "date":"2024-01-01"
    })
    tasks = user['tasks']
    response = client.post('/edit/6631d62dabefdc3dc9d3d2cb/6631d62dabefdc3dc9d3d2cd', data={
        "title":tasks[0]['title'],
        "course":tasks[0]['course'],
        "date":tasks[0]['date']
    })
    assert response.status_code == 302

def test_delete_task_page(client):

    auth = client.post("/login", data={
    "username":"hello",
    "password":"123",
    })
    user_id = ObjectId(current_user.id)
    user = db.users.find_one({'_id': user_id})
    add = client.post("/add", data={
        "_id":ObjectId(),
        "title":"Title",
        "course":"Course",
        "date":"2024-01-01"
    })
    tasks = user['tasks']
    print(user_id)
    task_id = tasks[0]["_id"]
    print(task_id)
    response = client.get('/delete/6631d62dabefdc3dc9d3d2cb/6631d62dabefdc3dc9d3d2cd')
    assert response.status_code == 200
    assert b"Delete Task" in response.data

def test_delete_task(client):

    auth = client.post("/login", data={
    "username":"hello",
    "password":"123",
    })
    user_id = ObjectId(current_user.id)
    user = db.users.find_one({'_id': user_id})
    add = client.post("/add", data={
        "_id":ObjectId(),
        "title":"Title",
        "course":"Course",
        "date":"2024-01-01"
    })
    tasks = user['tasks']
    response = client.post('/delete/6631d62dabefdc3dc9d3d2cb/6631d62dabefdc3dc9d3d2cd', data={
        "title":tasks[0]['title'],
        "course":tasks[0]['course'],
        "date":tasks[0]['date']
    })
    assert response.status_code == 302