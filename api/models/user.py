from api import db, Config, ma
from passlib.apps import custom_app_context as pwd_context
# Документация itsdangerous: https://itsdangerous.palletsprojects.com/en/2.1.x/
from itsdangerous import URLSafeSerializer
from itsdangerous import BadSignature

from sqlalchemy.exc import IntegrityError


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.relationship('NoteModel', backref='author', lazy='dynamic')
    is_staff = db.Column(db.Boolean(), default=False, server_default="false", nullable=False)
    role = db.Column(db.String(32), nullable=False, server_default="simple_user", default="simple_user")

    def __init__(self, username, password, role="simple_user"):
        self.username = username
        self.hash_password(password)
        self.role = role

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self):
        s = URLSafeSerializer(Config.SECRET_KEY)
        return s.dumps({'id': self.id})

    def get_roles(self):
        return [self.role]

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:  # Обработка ошибки "создание пользователя с НЕ уникальным именем"
            db.session.rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def verify_auth_token(token):
        s = URLSafeSerializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except BadSignature:
            return None  # invalid token
        user = UserModel.query.get(data['id'])
        return user
