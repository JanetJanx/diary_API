from flask import Flask, jsonify, request, make_response
app = Flask(__name__)

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

@app.route('/api/v1/entries', methods=['GET'])
def get_all_entries():
    return make_response(jsonify(
        {'entries':entries},
        {"message": "Entries successfully fetched"}), 201)

@app.route('/api/v1/entries/<int:entryid>', methods=['GET'])
def get_specific_entry(entryid):
    entry = [eid for eid in entries if eid['entryId'] == entryid]
    return make_response(jsonify(
        {'entry': entry[0]},
        {"message": "Entry successfully fetched"}), 200)


if __name__ == "__main__":
    app.run(debug=True, port=5008)
