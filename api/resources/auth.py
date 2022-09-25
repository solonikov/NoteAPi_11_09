from api import Resource, multi_auth


class TokenResource(Resource):
    @multi_auth.login_required
    def get(self):
        user = multi_auth.current_user()
        token = user.generate_auth_token()
        return {'token': token}
