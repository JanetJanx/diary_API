import json

class Entry:
    count = 0
    def __init__(self, title, content, time):
        self.entryId = None
        self.title = title
        self.content = content
        self.time = time

    def json(self):
        Entry.count += 1
        self.entryId = Entry.count
        return json.dumps({
            'entryId': self.entryId,
            'title': self.title,
            'content': self.content,
            'time': self.time
        })