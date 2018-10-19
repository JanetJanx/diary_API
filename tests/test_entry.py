import unittest
import re
from datetime import datetime
from app.entryapp import app, get_timestamp
from app.models import Entry

class TestEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)
        self.entry = Entry("open bank account", "used DFCU, registered with nation ID", "2018-09-27 08:44:01")

    def test_add_entry_successfully_with_post(self):
        entry_data = Entry.json(self.entry)
        post_url = self.client.post('api/v1/entries',data=entry_data,content_type='application/json')
        self.assertEqual(post_url.status_code, 201)

        if self.entry.title.strip() == "" or len(self.entry.title.strip()) < 3:
            self.assertEqual(post_url.json, [{"message": "Enter a valid tiltle please"}])

        if re.compile('[!@#$%^&*:;?><.0-9]').match(self.entry.title):
            self.assertEqual(post_url.json, [{"message": "Title contains Invalid characters"}])

        for x in self.entry.title:
            if x.isdigit():
                self.assertEqual(post_url.json, [{"message": "Title contains numbers"}])

        entries = []
        for entry in entries:
            if entry['title'] == entries['title']:
                self.assertEqual(post_url.json, [{"message": "Entry with the same title already exists "}])

    def test_get_all_entries(self):
        get_url = self.client.get('api/v1/entries')
        self.assertEqual(get_url.status_code, 200)

    def test_get_timestamp(self):
        self.assertEqual(get_timestamp(), datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))

    def test_get_specific_entry(self):
        self.entry.entryId = 1
        specific_get_url = self.client.get('api/v1/entries/{}'.format(self.entry.entryId))
        self.assertEqual(specific_get_url.status_code, 200)

    def test_modify_entry_with_put_successfully(self):
        entry_data = Entry.json(self.entry)
        self.entry.entryId = 1
        put_url = self.client.put('api/v1/entries/{}'.format(self.entry.entryId),data=entry_data,content_type='application/json')
        self.assertEqual(put_url.status_code, 200)

    def test_delete_entry_with_delete_successfully(self):
        entry_data = Entry.json(self.entry)
        self.entry.entryId = 1
        delete_url = self.client.delete('api/v1/entries/{}'.format(self.entry.entryId),data=entry_data,content_type='application/json')
        self.assertEqual(delete_url.status_code, 200)
        self.assertIsNotNone(delete_url.json)

if __name__ == "__main__":
    unittest.main()