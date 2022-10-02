from api import ma
from api.models.note import NoteModel
from api.schemas.user import UserSchema
from api.schemas.tag import TagSchema


#       schema        flask-restful
# object ------>  dict ----------> json

class NoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    id = ma.auto_field()
    text = ma.auto_field()
    private = ma.auto_field()
    author = ma.Nested(UserSchema())
    tags = ma.Nested(TagSchema(many=True))


class NoteCreateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel
        fields = ["text", "private"]

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
