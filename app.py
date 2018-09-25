from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

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


class EntryView(Resource):
    def get(self):
        return make_response(jsonify(
            {'entries':entries},
            {"message": "Entries successfully fetched"}), 201)

api.add_resource(EntryView, '/api/v1/entries', methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True, port=5001)
