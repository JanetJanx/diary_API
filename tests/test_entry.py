import unittest
from datetime import datetime
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.entry.entryapp import app, get_timestamp
from app.entry.models import Entry

class TestEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)
        self.entry = Entry(1, "open bank account", "used DFCU, registered with nation ID", "2018-09-27 08:44:01")

    def test_add_entry_successfully_with_post(self):
        entry_data = Entry.json(self.entry)
        post_url = self.client.post('api/v1/entries',data=entry_data,content_type='application/json')  
        self.assertEqual(post_url.status_code, 200)

    def test_get_all_entries(self):
        get_url = self.client.get('api/v1/entries')
        self.assertEqual(get_url.status_code, 200)

    def test_get_timestamp(self):
        self.assertEqual(get_timestamp(), datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))

if __name__ == "__main__":
    unittest.main()