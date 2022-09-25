from api import Resource, auth


class TokenResource(Resource):
    @auth.login_required
    def get(self):
        user = auth.current_user()
        token = user.generate_auth_token()
        return {'token': token}
