from api import auth, abort, Resource, reqparse, db
from api.models.note import NoteModel
from api.models.note import TagModel
from api.schemas.note import NoteSchema, NoteCreateSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields


@doc(tags=['Notes'])
class NoteResource(MethodResource):
    @auth.login_required
    @doc(summary="Get note by id", security=[{"basicAuth": []}])
    @marshal_with(NoteSchema)
    def get(self, note_id):
        """
        Пользователь может получить ТОЛЬКО свою заметку
        """
        author = auth.current_user()
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        return note, 200

    @auth.login_required
    @doc(summary="Edit note by id", security=[{"basicAuth": []}])
    @marshal_with(NoteSchema)
    def put(self, note_id):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = auth.current_user()
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        parser.add_argument("private", type=bool)
        note_data = parser.parse_args()
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.text = note_data["text"]

        note.private = note_data.get("private") or note.private

        note.save()
        return note, 200

    @auth.login_required
    @doc(description='Delete note by id', security=[{"basicAuth": []}])
    @doc(responses={401: {"description": "Not authorization"}})
    @doc(responses={404: {"description": "Not found"}})
    def delete(self, note_id):
        """
        Пользователь может удалять ТОЛЬКО свои заметки
        """
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        note.delete()
        return "", 204


@doc(tags=['Notes'])
class NotesListResource(MethodResource):
    @auth.login_required
    @doc(summary="Get notes list", security=[{"basicAuth": []}])
    @marshal_with(NoteSchema(many=True), code=200)
    def get(self):
        author = auth.current_user()
        notes = NoteModel.query.join(NoteModel.author).filter_by(username=author.username).all()
        return notes, 200

    @auth.login_required
    @doc(summary="Create note", security=[{"basicAuth": []}])
    @marshal_with(NoteSchema, code=201)
    @use_kwargs(NoteCreateSchema)
    def post(self, **kwargs):
        author = auth.current_user()
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        # TODO: Получить все теги по id одним запросом!
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            note.tags.append(tag)
        db.session.commit()
        return note, 200


@doc(tags=['Notes'])
class NotesFilterResource(MethodResource):
    # GET: /notes/filter?tag_name="..."
    @doc(summary="Get notes with filters")
    @marshal_with(NoteSchema(many=True))
    @use_kwargs({"tag_name": fields.Str()}, location="query")
    def get(self, **kwargs):
        notes = NoteModel.query.join(NoteModel.tags).filter_by(name=kwargs["tag_name"]).all()
        return notes