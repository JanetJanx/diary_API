from flask import Flask, Blueprint
from flask_restful import Api
from .entryapp import AddNewEntry, ModifySpecificEntry, GetAllEntries, DeleteSpecificEntry, ViewSpecificEntry
from config import app_config

def create_app():
    # Initialize flask app
    app_ = Flask(__name__, instance_relative_config=True)

    return app_


app = create_app()

entry = Blueprint('entries', __name__)
api = Api(entry)
api.add_resource(GetAllEntries, '/api/v1/entries')
api.add_resource(AddNewEntry, '/api/v1/entries')
api.add_resource(ViewSpecificEntry, '/api/v1/entries/<int:entryid>')
api.add_resource(DeleteSpecificEntry, '/api/v1/entries/<int:entryid>')
api.add_resource(ModifySpecificEntry, '/api/v1/entries/<int:entryid>')