import pytest
from api import db
from app import app
from config import Config


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
   response = client.get('/users/1')
   assert response.status_code == 200
   # assert response.json ??? ← это немного позднее