import pytest
from base64 import b64encode
from api import db
from app import app
from config import Config
from api.models.note import NoteModel
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


def auth():
    user_data = {"username": "testUser", "password": "1234"}
    headers = {
        'Authorization': 'Basic ' + b64encode(
            f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
    }
    return headers


def test_note_get_by_id(client):
    # Create new User
    user_data = {"username": "testUser", "password": "1234"}
    user = UserModel(**user_data)
    user.save()

    note_data = {"author_id": user.id, "text": "Note for testUser"}
    user = NoteModel(**note_data)
    user.save()

    headers = auth()
    response = client.get('/notes/1', headers=headers)
    data = response.json
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["text"] == note_data["text"]
    assert data["author"]["id"] == 1