from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class CounterfeitEntryError(Exception):
    pass

"""class to define the entry model"""
class Entry:
    entryId = 0

    def __init__(self, title, content, time):
        self.entryId = None
        self.title = title
        self.content = content
        self.time = time

    def add(self):
        entries_present = EntryView.entries

        for entry in entries_present:
            if entry['title'] == self.title:
                raise CounterfeitEntryError('Entry' + {self.title} + 'already exists')

        Entry.entryId + 1
        self.entryId = Entry.entryId

        entry_data = {
            'entryId': self.entryId,
            'title': self.title,
            'content': self.content,
            'time': self.time
        }
        entries_present.append(entry_data)

class EntryView(Resource):
    entries = []
    def get(self):
        return make_response(jsonify(
            {'entries':EntryView.entries},
            {"message": "Entries successfully fetched"}), 201)

api.add_resource(EntryView, '/api/v1/entries', methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True, port=5001)
