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

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

@app.route('/api/v1/entries', methods=['GET'])
def get_all_entries():
    return make_response(jsonify(
        {'entries':entries},
        {"message": "Entries successfully fetched"}), 201)

<<<<<<< Updated upstream

if __name__ == "__main__":
    app.run(debug=True, port=5000)
=======
@app.route('/api/v1/entries/<int:entryid>', methods=['GET'])
def get_specific_entry(entryid):
    entry = [eid for eid in entries if eid['entryId'] == entryid]
    return make_response(jsonify(
        {'entry': entry[0]},
        {"message": "Entry successfully fetched"}), 200)

@app.route('/api/v1/entries', methods=['POST'])
def add_entry():
    entrycontent = {
        'entryId':entries[-1]['entryId'] + 1,
        'title': request.json['title'],
        'content':request.json['content'],
        'time':get_timestamp()
        }
    entries.append(entrycontent)

    return make_response(jsonify(
        {'entrycontent': entrycontent},
        {'message': "Entry successfully added"}), 200)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
>>>>>>> Stashed changes
