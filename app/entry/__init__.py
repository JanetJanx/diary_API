from flask import Blueprint
from flask_restful import Api
from .entryapp import AddNewEntry, ModifySpecificEntry, GetAllEntries, DeleteSpecificEntry, ViewSpecificEntry

entry = Blueprint('entries', __name__)
api = Api(entry)
api.add_resource(GetAllEntries, '/api/v1/entries')
api.add_resource(AddNewEntry, '/api/v1/entries')
api.add_resource(ViewSpecificEntry, '/api/v1/entries/<int:entryid>')
api.add_resource(DeleteSpecificEntry, '/api/v1/entries/<int:entryid>')
api.add_resource(ModifySpecificEntry, '/api/v1/entries/<int:entryid>')
