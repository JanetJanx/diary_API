from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

from datetime import datetime

app = Flask(__name__)
api = Api(app)

entries = [
    {
        'entryId':1,
        'title':'dictionary function',
        'content':'using comprehenion',
        'time':'2018-09-14 11:31:09.318212'
        
    },
    {
        'entryId':2,
        'title':'bankaccount class',
        'content':'class implementation corresponding to the provided tests',
        'time':'2018-09-21 10:1:09.318212'
    }
        ]

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

class EntryView(Resource):
    def get(self):
        return make_response(jsonify(
            {'entries':entries},
            {"message": "Entries successfully fetched"}), 201)

    def post(self):
        try:
            entrydata = request.get_json()
            title = entrydata.get('title')
            content = entrydata.get('content')

            entrycontent = {
                "entryId":entries[-1]['entryId'] + 1,
                "title": title,
                "content":content,
                "time":get_timestamp()
                }

            entries.append(entrycontent)

            return make_response(jsonify(
                {'entrycontent': entrycontent},
                {'message': "Entry successfully added"}), 200)

        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"}), 400)


class SpecificEntry(Resource):
    def get(self, entryid):
        entry = [eid for eid in entries if eid['entryId'] == entryid]
        return make_response(jsonify(
            {'entry': entry[0]},
            {"message": "Entry successfully fetched"}), 200)


api.add_resource(EntryView, '/api/v1/entries', methods=['GET', 'POST'])
api.add_resource(SpecificEntry, '/api/v1/entries/<int:entryid>', methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True, port=5004)
