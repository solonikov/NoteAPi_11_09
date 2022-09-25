import pytest
from api import db
from app import app
from config import Config
from api.models.user import UserModel


@pytest.fixture()
def application():
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE
    })
    db.create_all()
    yield app
    db.drop_all()


@pytest.fixture()
def client(application):
    return application.test_client()


def test_user_get_by_id(client):
    # Create new User
    user_data = {"username": "testUser", "password": "1234"}
    user = UserModel(**user_data)
    user.save()

    response = client.get('/users/1')
    data = response.json
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["username"] == user_data["username"]


def test_user_not_found(client):
    response = client.get('/users/2')
    assert response.status_code == 404


def test_user_create(client):
    user_data = {"username": "testUser", "password": "1234"}
    response = client.post('/users', json=user_data)
    data = response.json
    user = UserModel.query.get(1)
    assert response.status_code == 201
    assert data["id"] == 1
    assert data["username"] == user_data["username"]
    assert user is not None
    assert user.username == user_data["username"]