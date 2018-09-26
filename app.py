from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
import json

from datetime import datetime

app = Flask(__name__)
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

"""class to define the entry model and its operations"""   
class Entry(dict):
    def __init__(self, entryId, title, content, time):
        self.entryId = entryId
        self.title = title
        self.content = content
        self.time = time
    def json(self):
        return json.dumps({
            'entryId': self.entryId,
            'title': self.title,
            'content': self.content,
            'time': self.time
        })


class EntryView(Resource):
    entries = []
    def get(self):
        return make_response(jsonify(
            {'entries':EntryView.entries},
            {"message": "Entries successfully fetched"}), 201)

    def post(self):
        try:
            entrydata = request.get_json()
            title = entrydata.get('title')
            content = entrydata.get('content')
            
            new_entry = Entry(increment_entryId(), title, content, get_timestamp())
            entry = json.loads(new_entry.json())
            EntryView.entries.append(entry)

            return make_response(jsonify(
                {'entries': EntryView.entries},
                {'message': "Entry successfully added"}), 200)

        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"}), 400)

class SpecificEntry(Resource):
    """get specific entry"""
    def get(self, entryid):
        entries = EntryView.entries
        entry = [eid for eid in entries if eid['entryId'] == entryid]
        return make_response(jsonify(
            {'entry': entry[0]},
            {"message": "Entry successfully fetched"}), 200)
    
    """delete a specify entry"""
    def delete(self, entryid):
        entry = [eid for eid in EntryView.entries if eid['entryId'] == entryid]
        EntryView.entries.remove(entry[0])
        return make_response(jsonify(
            {'entry': entry[0]},
            {"message": "Entry successfully removed"}), 200)

    """modify a specific entry"""
    def put(self, entryid):
        entry = [entry for entry in EntryView.entries if entry['entryId'] == entryid]
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


api.add_resource(SpecificEntry, '/api/v1/entries/<int:entryid>', methods=['PUT', 'GET', 'DELETE'])

api.add_resource(EntryView, '/api/v1/entries', methods=['POST', 'GET'] ) 


if __name__ == "__main__":
    app.run(debug=True, port=5000)
