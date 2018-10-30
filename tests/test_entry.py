import unittest
import re
from datetime import datetime
from app.entryapp import app, get_timestamp, ViewSpecificEntry
from app.models import Entry

class TestEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)
        self.entry = Entry("open bank account", "used DFCU, registered with nation ID", "2018-09-27 08:44:01")
        self.entries = []

    def test_add_entry_successfully_with_post(self):
        entry_data = Entry.json(self.entry)
        post_url = self.client.post('api/v1/entries',data=entry_data,content_type='application/json')
        self.assertEqual(post_url.status_code, 201)

    def test_whether_title_is_valid(self):
        self.ent = Entry("qr", "used DFCU, registered with nation ID", "2018-09-27 08:44:01")
        entry_data = Entry.json(self.ent)
        post_url = self.client.post('api/v1/entries',data=entry_data,content_type='application/json')
        title = str(self.ent.title).strip()
        if not title or len(title) < 3:
            self.assertEqual(post_url.json, {"message": "Enter a valid tiltle please"})

    def test_whether_content_is_valid(self):
        self.ent = Entry("open account", "used DFCU", "2018-09-27 08:44:01")
        entry_data = Entry.json(self.ent)
        post_url = self.client.post('api/v1/entries',data=entry_data,content_type='application/json')
        content = str(self.ent.content).strip()
        if not content or len(content) < 10:
            self.assertEqual(post_url.json, {"message": "Enter valid content please, with atleast 10 characters"})

    def test_whether_title_contains_invalid_chars(self):
        self.ent = Entry("qr3w#", "used DFCU, registered with nation ID", "2018-09-27 08:44:01")
        entry_data = Entry.json(self.ent)
        post_url = self.client.post('api/v1/entries',data=entry_data,content_type='application/json')
        if re.compile('[!@#$%^&*:;?><.0-9]').search(self.ent.title):
            self.assertEqual(post_url.json, {"message": "Title contains Invalid characters"})

    def test_whether_title_is_unique(self):
        entry_data = Entry.json(self.entry)
        post_url = self.client.post('api/v1/entries',data=entry_data,content_type='application/json')
        for entry in self.entries:
            if entry['title'] == entry_data.title:
                self.assertEqual(post_url.status_code, 400)
                self.assertEqual(post_url.json, {"message": "Entry with the same title already exists "})

    def test_get_all_entries(self):
        get_url = self.client.get('api/v1/entries')
        self.assertEqual(get_url.status_code, 200)

    def test_get_timestamp(self):
        self.assertEqual(get_timestamp(), datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))

    def test_get_specific_entry(self):
        for entry in self.entries:
            if entry['entryId'] == 1:
                specific_get_url = self.client.get('api/v1/entries/{}'.format(entry['entryId']))
                self.assertEqual(specific_get_url.json, {"message": "Entry successfully fetched"})
                self.assertEqual(specific_get_url.status_code, 200)
            self.assertEqual(specific_get_url.json, {"message": "Entry doesn't exists "})

    def test_modify_entry_with_put_successfully(self):
        for entry in self.entries:
            if entry['entryId'] == 1:
                entry['title'] = "bank account"
                entry['content'] = "used DFCU, registered with nation ID"
                entry['time'] = get_timestamp()
                put_url = self.client.put('api/v1/entries/{}'.format(entry['entryId']),data=entry,content_type='application/json')
                self.assertEqual(put_url.json, {'message': "Entry successfully updated"})
                self.assertEqual(put_url.status_code, 200)
            self.assertEqual(put_url.json, {"message": "Entry doesn't exists "})

    def test_delete_entry_with_delete_successfully(self):
        for entry in self.entries:
            if entry['entryId'] == 1:
                self.entries.remove(entry)
                delete_url = self.client.delete('api/v1/entries/{}'.format(entry['entryId']))
                self.assertEqual(delete_url.json, {"message": "Entry successfully removed"})
                self.assertEqual(delete_url.status_code, 200)
            self.assertEqual(put_url.json, {"message": "Entry with specified ID not found"})

if __name__ == "__main__":
    unittest.main()