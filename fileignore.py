from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse
import re
from datetime import datetime

app = Flask(__name__)
api = Api(app)

users = [
            {
                'firstname':'Janet',
                'lastname':'Namutebi',
                'email':'janet@gmail.com',
                'password':'123'
            },
            {
                'firstname':'Aine',
                'lastname':'Mbabazi',
                'email':'aine@gmail.com',
                'password':'453'
            }
        ]

entries = [
            {
                'title':'dictionary function',
                'content':'using comprehenion',
                'time':'2018-09-14 11:31:09.318212',
                'email':'janet@gmail.com'
                
            },
            {
                'title':'bankaccount class',
                'content':'class implementation corresponding to the provided tests',
                'time':'2018-09-21 10:1:09.318212',
                'email':'aine@gmail.com'
            }
        ]
def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    
parser = reqparse.RequestParser()
class User:
    """User representation"""
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def json(self):
        return json.dumps({
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'password': self.password
        })

class Entry:
    def __init__(self, entry_id, title, content, time):
        self.entry_id = entry_id
        self.title = title
        self.content = content
        self.time = datetime.datetime.now()

    def json(self):
        return json.dumps({
            'entry_id': self.entry_id,
            'title': self.title,
            'content': self.content,
            'time': self.time
        })
          

class UserLogin(Resource):
    def post(self):
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        args = parser.parser_args()
        email = args['email']
        password = args['password']

        for user in users:
            if email == user['email'] and password == user['password']:
                return make_response(jsonify({"message": "User logged in successfully"}), 201)
            return make_response(jsonify({"message": "wrong credentials"}), 401)

class AddUser(Resource):
    def get(self):
        return users

    def post(self):
        """Allow new users to signup"""
        parser.add_argument('firstname', type=str)
        parser.add_argument('lastname', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

        args = parser.parser_args()
        firstname = args['firstname']
        lastname = args['lastname']
        email = args['email']
        password = args['password']

        if password.strip() == "" or len(password.strip()) < 8:
            return make_response(jsonify({"message": "password too short or left empty, re-enter valid password"}), 401)
        
        if lastname.strip() == "" or len(lastname.strip()) < 2:
            return make_response(jsonify({"message": "lastname too short or left empty, re-enter lastname"}), 401)
        
        if firstname.strip() == "" or len(firstname.strip()) < 2:
            return make_response(jsonify({"message": "firstname too short or left empty, re-enter lastname"}), 401)
        
        if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
            return make_response(jsonify({"message": "Enter valid email"}), 401)

        if re.compile('[!@#$%^&*:;?><.0-9]').match(lastname):
            return make_response(jsonify({"message": "Invalid characters not allowed, re-enter lastname"}), 401)

        if re.compile('[!@#$%^&*:;?><.0-9]').match(firstname):
            return make_response(jsonify({"message": "Invalid characters not allowed, re-enter firstname"}), 401)
        
        new_user = User(firstname, lastname, email, password)

        for user in users:
            if email == users['email']:
                return make_response(jsonify({"message": "user with this email already in use"}), 401)

        users.append(json.loads(new_user.json()))
        return make_response(jsonify({'message': 'User successfully created', 'email': new_user.email}), 201)

class AddEntry(Resource):
        def post(self):
            """Allow authenticated users to add entries"""
            parser.add_argument('title', type=str)
            parser.add_argument('content', type=str)
            parser.add_argument('email', type=str, location=True)
            parser.add_argument('time', type=str, get_timestamp())

            args = parser.parser_args()
            title = args['title']
            content = args['content']
            time = args['time']

            if not args['email']:
                return make_response(jsonify({"message": "Not logged in"}), 400)
            
            for user in users:
                if user['email'] == args['email']:
                    if title.strip() == "" or len(title.strip()) < 2:
                        return make_response(jsonify({"message": "Title should be more than 2 letters"}), 400)

                    if re.compile('[!@#$%^&*:;?><.0-9]').match(title):
                        return make_response(jsonify({"message": "Invalid characters not allowed"}), 400)

                    new_entry = Entry(email, title, content, time)
                    
                    for entry in entries:
                        if title == entry['title']:
                            return make_response(jsonify({"message": 'entry title already exists'}), 400)

                    entry = json.loads(new_entry.json())
                    entries.append(entry)
                    return make_response(jsonify({
                    'message': 'entry successfully saved',
                    'status': 'ok'},), 201)
                return make_response(jsonify({"message": "Doesn't exist, signup please"}), 401)

api.add_resource(UserLogin, '/v1/login')   
api.add_resource(AddUser, '/v1')

if __name__ == "__main__":
    app.run(debug=True, port=5000)


@app.route('/api/v1/entry/<int:entryid>', methods=['PUT'])


if __name__ == "__main__":
    app.run(debug=True, port=5000)




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

class SpecificEntry(Resource):
    def get(self, entryid):
        entry = [eid for eid in entries if eid['entryId'] == entryid]
        return make_response(jsonify(
            {'entry': entry[0]},
            {"message": "Entry successfully fetched"}), 200)

    def delete(self, entryid):
        entry = [eid for eid in entries if eid['entryId'] == entryid]
        entries.remove(entry[0])
        return make_response(jsonify(
            {'entry': entry[0]},
            {"message": "Entry successfully removed"}), 200)



api.add_resource(EntryView, '/api/v1/entries', methods=['GET'])
api.add_resource(SpecificEntry, '/api/v1/entries/<int:entryid>', methods=['GET'])

def add(self):
        entries_present = EntryView.entries

        for entry in entries_present:
            if entry['title'] == self.title:
                raise CounterfeitEntryError('Entry' + {self.title} + 'already exists')

        entry_data = {
            'entryId': self.entryId,
            'title': self.title,
            'content': self.content,
            'time': self.time
        }
        entries_present.append(entry_data)
        return make_response(jsonify(
            {'entries':entries_present},
            {"message": "Entries successfully created"}), 201)

def test_get_specific_entry(self):
        entryId = 1
        entry_data = Entry.json(self.entry)
        specific_get_url = self.client.get('api/v1/entries/{}'.format(entryId))
        self.assertEqual(specific_get_url.status_code, 200)

    def test_modify_entry_with_put_successfully(self):
        entryId = 1
        entry_data = Entry.json(self.entry)
        put_url = self.client.put('api/v1/entries/{}'.format(entryId),
                               data=entry_data,
                                content_type='application/json')
        self.assertEqual(put_url.status_code, 201)

    def test_delete_specific_entry(self):
        entryId = 1
        specific_get_url = self.client.delete('api/v1/entries/{}'.format(entryId))
        self.assertEqual(specific_get_url.status_code, 200)