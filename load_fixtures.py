from api import db
import json
from api.schemas.user import UserRequestSchema

from api.models.note import NoteModel
from api.models.user import UserModel


def load_data(path_to_fixture):
    with open(path_to_fixture, "r", encoding="UTF-8") as f:
        file_data = json.load(f)
        model_name = file_data["model"]
        if model_name == "UserModel":
            model = UserModel
        elif model_name == "NoteModel":
            model = NoteModel

        for obj_data in file_data["data"]:
            obj = model(**obj_data)
            db.session.add(obj)
        db.session.commit()
    print(f"{len(file_data['data'])} users created")


path_to_fixture = "fixtures/users.json"
load_data(path_to_fixture)
