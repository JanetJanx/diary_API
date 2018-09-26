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
    def __repr__(self):
        entry_def = '{} {} {} {}'.format(self.entryId, self.title, self.content, self.time)
        return json.dumps(entry_def)


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
            
            EntryView.entries.append(Entry(increment_entryId(), title, content, get_timestamp()))

            return make_response(jsonify(
                {'entries': EntryView.entries},
                {'message': "Entry successfully added"}), 200)

        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"}), 400)

class SpecificEntry(Resource):
    def get(self, entryid):
        entries = EntryView.entries
        entry = [eid for eid in entries if eid['entryId'] == entryid]
        return make_response(jsonify(
            {'entry': entry[0]},
            {"message": "Entry successfully fetched"}), 200)
    

api.add_resource(EntryView, '/api/v1/entries', methods=['GET', 'POST'])
api.add_resource(SpecificEntry, '/api/v1/entries/<int:entryid>', methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True, port=5004)
