from api import Resource, abort, reqparse, auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from api.schemas.user import UserSchema, UserRequestSchema


# parameters:
# 1. path
# 2. body
# 3. query
@doc(tags=['Users'])
class UserResource(MethodResource):
    @doc(summary="Get user by id", description="Returns user")
    @doc(responses={404: {"description": 'User not found'}})
    @marshal_with(UserSchema, code=200)
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if user is None:
            abort(404, error=f"User with id={user_id} not found")
        return user, 200

    @auth.login_required(role="admin")
    @doc(description='Edit user by id')
    @marshal_with(UserSchema)
    # @use_kwargs({"username": fields.Str()})
    @doc(security=[{"basicAuth": []}])
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        user_data = parser.parse_args()
        user = UserModel.query.get(user_id)
        user.username = user_data["username"]
        user.save()
        return user, 200

    # @auth.login_required
    def delete(self, user_id):
        raise NotImplemented  # не реализовано!


@doc(tags=['Users'])
class UsersListResource(MethodResource):
    @marshal_with(UserSchema(many=True), code=200)
    def get(self):
        users = UserModel.query.all()
        return users, 200

    @doc(summary="Create new User", description="Подробное описание метода POST")
    @use_kwargs(UserRequestSchema, location='json')
    @marshal_with(UserSchema, code=201)
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user, 201

# Сериализация: obj --> dict --> str
# Десериализация: str --> dict --> obj
