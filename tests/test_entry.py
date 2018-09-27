import unittest
import json
import requests
import codecs
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app import app_config, app
from flask import Flask, jsonify, request
from app.entry.entryapp import AddNewEntry, GetAllEntries, ViewSpecificEntry, DeleteSpecificEntry, ViewSpecificEntry


class TestEndpoint(unittest.TestCase):
    def create_app(self):
        app.config.from_object(app_config["testing"])
        return app

    def setUp(self):
        self.client = app.test_client(self)

    def tearDown(self):
        GetAllEntries.entries[:] = []    

    def post_entry(self, entryId, title, content, time):
        return self.client.post(
            'api/v1/entries',
            data=json.dumps(dict(
                entryId=entryId,
                title=title,
                content=content,
                time=time
             ) 
             ),
            content_type='application/json'
        )  
    def get_entries(self):
        return self.client.get('api/v1/entries')
    
    def get_specific_entry(self,entryid):
        return self.client.get('api/v1/entries/{}'.format(entryid))
    
    def put_entry(self, entryid, title, content, time):
        return self.client.put('api/v1/users/requests/{}'.format(entryid),
                               data=json.dumps(dict(
                                   entryId=entryid,
                                    title=title,
                                    content=content,
                                    time=time)),
                                content_type='application/json')
        
    def test_add_entry_successfully_with_post(self):
        with self.client:
            id = 1
            reader = codecs.getreader("utf-8")
            response = self.post_entry(id, "bank acount", "using oop python implementing", "2018-09-27 08:44:01")
            data = json.load(reader(response.data))
            self.assertEqual(data.status_code, 200)
            #self.assertEqual(entry_data.get('message'), "Entry successfully added")

    
    
if __name__ == "__main__":
    unittest.main()