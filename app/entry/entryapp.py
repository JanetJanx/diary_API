from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
import json
from datetime import datetime
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from entry.models import Entry
app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

count = 0
def increment_entryId():
    global count
    count = count + 1
    return count

class CounterfeitEntryError(Exception):
    pass

class GetAllEntries(Resource):
    entries = []
    @classmethod
    def get(self):
        return make_response(jsonify(
            {'entries':GetAllEntries.entries},
            {"message": "Entries successfully fetched"}), 200)

class AddNewEntry(Resource):
    @classmethod
    def post(self):
        try:
            entrydata = request.get_json()
            title = entrydata.get('title')
            content = entrydata.get('content')
            new_entry = Entry(increment_entryId(), title, content, get_timestamp())
            entry = json.loads(new_entry.json())
            GetAllEntries.entries.append(entry)

            return make_response(jsonify(
                {'entries': GetAllEntries.entries},
                {'message': "Entry successfully added"}), 200)

        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"}), 400)

class ViewSpecificEntry(Resource):
    """get specific entry"""
    @classmethod
    def get(self, entryid):
        entries = GetAllEntries.entries
        entry = [eid for eid in entries if eid['entryId'] == entryid]
        return make_response(jsonify(
            {'entry': entry[0]},
            {"message": "Entry successfully fetched"}), 200)

class DeleteSpecificEntry(Resource):
    """delete a specify entry"""
    @classmethod
    def delete(self, entryid):
        entry = [eid for eid in GetAllEntries.entries if eid['entryId'] == entryid]
        GetAllEntries.entries.remove(entry[0])
        return make_response(jsonify(
            {'entry': entry[0]},
            {"message": "Entry successfully removed"}), 200)

class ModifySpecificEntry(Resource):
    """modify a specific entry"""
    @classmethod
    def put(self, entryid):
        entry = [entry for entry in GetAllEntries.entries if entry['entryId'] == entryid]
        try:
            entrydata = request.get_json()
            title = entrydata.get('title')
            content = entrydata.get('content')

            entry[0]['title'] = title
            entry[0]['content'] = content
            entry[0]['time'] = get_timestamp()

            return make_response(jsonify(
                {'entry':entry[0]},
                {'message': "Entry successfully updated"}), 201)

        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"}), 401)

api.add_resource(GetAllEntries, '/api/v1/entries', methods=['GET'])
api.add_resource(AddNewEntry, '/api/v1/entries', methods=['POST'])
api.add_resource(ViewSpecificEntry, '/api/v1/entries/<int:entryid>', methods=['GET'])
api.add_resource(DeleteSpecificEntry, '/api/v1/entries/<int:entryid>', methods=['DELETE'])
api.add_resource(ModifySpecificEntry, '/api/v1/entries/<int:entryid>', methods=['PUT'])

if __name__ == "__main__":
    app.run(port 5004)
