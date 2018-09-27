import unittest
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app import app_config, app
from flask import json, request
from app.entry.entryapp import AddNewEntry, GetAllEntries, ViewSpecificEntry, DeleteSpecificEntry, ViewSpecificEntry


class TestEndpoint(unittest.TestCase):
    def create_app(self):
        app.config.from_object(app_config["testing"])
        return app

    def setUp(self):
        self.client = app.test_client(self)
        self.entry = json.dumps({
            "entryId":1,
            "title": "open bank account",
            "content": "used DFCU, registered with nation ID",
            "time":"2018-09-27 08:44:01"
        })

    def tearDown(self):
        GetAllEntries.entries[:] = []    

    def test_add_entry_successfully_with_post(self):
        
        post_url = self.client.post('api/v1/entries',
                                    data=json.loads(self.entry),
                                    content_type='application/json'
                                )  
        self.assertEqual(post_url.status_code, 200)

    def test_get_all_entries(self):
        get_url = self.client.get('api/v1/entries')
        self.assertEqual(get_url.status_code, 200)
    
    def test_get_specific_entry(self):
        specific_get_url = self.client.get('api/v1/entries/{}'.format(self.entry[1]))
        self.assertEqual(specific_get_url.status_code, 200)

    def test_delete_specific_entry(self):
        specific_get_url = self.client.delete('api/v1/entries/{}'.format(self.entry[1]))
        self.assertEqual(specific_get_url.status_code, 200)

    
    def test_modify_entry_with_put_successfully(self):
        put_url = self.client.put('api/v1/entries/{}'.format(self.entry[1]),
                               data=json.loads(self.entry),
                                content_type='application/json')
        self.assertEqual(put_url.status_code, 200)
 
    
if __name__ == "__main__":
    unittest.main()