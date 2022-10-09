from api import app, db
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel
import click
import json
from config import Config


@app.cli.command('createsuperuser')
def create_superuser():
    """
    Creates a user with the admin role
    """
    username = input("Username[default 'admin']:")
    password = input("Password[default 'admin']:")
    user = UserModel(username, password, role="admin")
    user.save()
    print(f"Superuser create successful! id={user.id}")


@app.cli.command('user')
@click.argument('do')  # create delete show
@click.option("--all", is_flag=True, default=False)
def user_operation(do, all):
    """
    User operations
    :create: create/show-all/delete
    """
    if do == "delete":
        if all:
            UserModel.query.delete()
            db.session.commit()
            print("Delete all users")
            return
        username = input("username: ")
        user = UserModel.query.filter_by(username=username).first()
        if user:
            user.delete()
            print("User deleted")
        else:
            print(f"User with {username} not found")

    elif do == "show-all":
        users = UserModel.query.all()
        for user in users:
            print(f"{user.username}")


@app.cli.command('fixture')
@click.argument('do')
@click.option('--fixture', help='fixture file name')  # python load_fixtures.py --fixture 'notes.json'
def load_data(do, fixture):
    """
    Load fixtures from json
    """
    if do == "load":
        models = {
            "UserModel": UserModel,
            "NoteModel": NoteModel,
            "TagModel": TagModel
        }
        with open(Config.PATH_TO_FIXTURES / fixture, "r", encoding="UTF-8") as f:
            file_data = json.load(f)
            model_name = file_data["model"]
            model = models[model_name]
            for obj_data in file_data["data"]:
                obj = model(**obj_data)
                db.session.add(obj)
            db.session.commit()
        print(f"{len(file_data['data'])} {model_name} created")
