import pytest
from app import app as flask_app
from flask_login import login_user, logout_user, current_user, UserMixin
import mongomock
from bson.objectid import ObjectId

class TestUser(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password
        self.active = True

    @property
    def is_active(self):
        return self.active

@pytest.fixture
def app():
    app = flask_app
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test_secret",
        "MONGO_URI": "mongomock://localhost",
        "MONGO_DBNAME": "mockdb"
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def mock_db(mocker, app):
    mocker.patch('pymongo.MongoClient', mongomock.MongoClient)
    db = mongomock.MongoClient()[app.config['MONGO_DBNAME']]
    return db

@pytest.fixture
def user_id():
    return ObjectId()

@pytest.fixture
def logged_in_user(client, mocker, app):
    with app.app_context():
        user_id = str(ObjectId())
        user = TestUser(user_id, 'testuser', 'password')
        mocker.patch('pymongo.collection.Collection.find_one', return_value={
            '_id': user.id, 'username': user.username, 'password': user.password
        })
        with client:
            with client.session_transaction() as sess:
                sess['user_id'] = user.id
            login_user(user, remember=True)
            yield user
            logout_user()



@pytest.fixture
def task_id():
    return ObjectId()

def test_login_success(client, mocker):
    test_user = {'_id': ObjectId(), 'username': 'test', 'password': 'test'}
    mocker.patch('pymongo.collection.Collection.find_one', return_value=test_user)
    response = client.post('/login', data={'username': 'test', 'password': 'test'})
    assert response.status_code == 302
    assert '/home' in response.headers['Location']

def test_login_failure(client, mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value=None)
    response = client.post('/login', data={'username': 'wrong', 'password': 'wrong'})
    assert response.status_code == 200
    assert b"Incorrect password entered" in response.data

def test_register_new_user(client, mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value=None)
    mocker.patch('pymongo.collection.Collection.insert_one')
    response = client.post('/register', data={'username': 'newuser', 'password': 'newpass'})
    assert response.status_code == 302

def test_register_existing_user(client, mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value=True)
    response = client.post('/register', data={'username': 'existuser', 'password': 'password'})
    assert response.status_code == 200
    assert b"Username already exists!" in response.data

def test_add_task(client, logged_in_user, mocker):
    mocker.patch('pymongo.collection.Collection.update_one')
    mocker.patch('pymongo.collection.Collection.find_one', return_value={'_id': logged_in_user.id, 'username': 'testuser', 'tasks': []})
    response = client.post('/add', data={'title': 'New Task', 'course': 'Math', 'date': '2024-04-30'}, follow_redirects=True)
    assert response.status_code == 200, f"Failed with status {response.status_code}, expected 200"

def test_edit_task(client, logged_in_user, task_id, mocker):
    mocker.patch('pymongo.collection.Collection.update_one')
    response = client.post(f'/edit/{logged_in_user.id}/{task_id}', data={'title': 'Updated Task', 'course': 'Science', 'date': '2024-05-01'})
    assert response.status_code == 302
    assert '/home' in response.headers['Location']

def test_delete_task(client, logged_in_user, task_id, mocker):
    mocker.patch('pymongo.collection.Collection.update_one')
    response = client.post(f'/delete/{logged_in_user.id}/{task_id}')
    assert response.status_code == 302
    assert '/home' in response.headers['Location']
