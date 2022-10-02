import click
import json
from config import Config
from api import db
from api.schemas.user import UserRequestSchema

from api.models.note import NoteModel
from api.models.user import UserModel


@click.command
# @click.argument('file_name') # python load_fixtures.py 'notes.json'
@click.option('--fixture', help='fixture file name') # python load_fixtures.py --fixture 'notes.json'
def load_data(fixture):
    with open(Config.PATH_TO_FIXTURES / fixture, "r", encoding="UTF-8") as f:
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
    print(f"{len(file_data['data'])} notes created")


# path_to_fixture = "fixtures/notes.json"
# load_data(path_to_fixture)

if __name__ == "__main__":
    load_data()
