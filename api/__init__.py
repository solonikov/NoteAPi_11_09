import logging
from config import Config
from flask import Flask, g
from flask_restful import Api, Resource, abort, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
# from flasgger import Swagger
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

security_definitions = {
    "basicAuth": {
        "type": "basic"
    }
}

app = Flask(__name__)
app.config.from_object(Config)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Notes Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        securityDefinitions=security_definitions,
        security=[],

        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI UI of API Doc
})

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
auth = MultiAuth(basic_auth, token_auth)
docs = FlaskApiSpec(app)


# swagger = Swagger(app)


@basic_auth.verify_password
def verify_password(username, password):
    from api.models.user import UserModel
    user = UserModel.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    return user


@token_auth.verify_token
def verify_token(token):
    from api.models.user import UserModel
    user = UserModel.verify_auth_token(token)
    # print(f"{user=}")
    return user


@basic_auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()
