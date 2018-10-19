import json
import re
from datetime import datetime

from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

from app.models import Entry


app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class GetAllEntries(Resource):
    entries = []
    @classmethod
    def get(self):
        return make_response(jsonify({'entries':GetAllEntries.entries},{"message": "Entries successfully fetched"}), 200)

class AddNewEntry(Resource):
    @classmethod
    def post(self):

        entrydata = request.get_json()
        title = entrydata.get('title')
        content = entrydata.get('content')

        #validation of entries
        if title.strip() == "" or len(title.strip()) < 3:
            return make_response(jsonify({"message": "Enter a valid tiltle please"}), 400)

        if re.compile('[!@#$%^&*:;?><.0-9]').match(title):
            return make_response(jsonify({"message": "Title contains Invalid characters"}), 400)

        for i in title:
            if i.isdigit():
                return make_response(jsonify({"message": "Title contains numbers"}), 400)

        if content.strip() == "" or len(content.strip()) < 10:
            return make_response(jsonify({"message": "Enter valid content please, with atleast 10 characters"}), 400)

        for entry in GetAllEntries.entries:
            if entry['title'] == title:
                return make_response(jsonify({"message": "Entry with the same title already exists "}), 406)

        new_entry = Entry(title, content, get_timestamp())
        entry = json.loads(new_entry.json())
        GetAllEntries.entries.append(entry)

        return make_response(jsonify({'entries': entry},{'message': "Entry successfully added"}), 201)


class ViewSpecificEntry(Resource):
    """get specific entry"""
    @classmethod
    def get(self, entryid):
        entries = GetAllEntries.entries
        for eid in entries:
            if eid['entryId'] == entryid:
                return make_response(jsonify({'entry': eid},{"message": "Entry successfully fetched"}), 200)

class DeleteSpecificEntry(Resource):
    """delete a specify entry"""
    @classmethod
    def delete(self, entryid):
        for eid in GetAllEntries.entries:
            if eid['entryId'] == entryid:
                GetAllEntries.entries.remove(eid)
        return make_response(jsonify({'entry': eid},{"message": "Entry successfully removed"}), 200)

class ModifySpecificEntry(Resource):
    """modify a specific entry"""
    @classmethod
    def put(self, entryid):
        #entry = [entry for entry in GetAllEntries.entries if entry['entryId'] == entryid]
        for entry in GetAllEntries.entries:
            if entry['entryId'] == entryid:
                entrydata = request.get_json()
                title = entrydata.get('title')
                content = entrydata.get('content')

                entry['title'] = title
                entry['content'] = content
                entry['time'] = get_timestamp()

                return make_response(jsonify(
                    {'entry':entry[0]},
                    {'message': "Entry successfully updated"}), 200)


api.add_resource(GetAllEntries, '/api/v1/entries', methods=['GET'])
api.add_resource(AddNewEntry, '/api/v1/entries', methods=['POST'])
api.add_resource(ViewSpecificEntry, '/api/v1/entries/<int:entryid>', methods=['GET'])
api.add_resource(DeleteSpecificEntry, '/api/v1/entries/<int:entryid>', methods=['DELETE'])
api.add_resource(ModifySpecificEntry, '/api/v1/entries/<int:entryid>', methods=['PUT'])