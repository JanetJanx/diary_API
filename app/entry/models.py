import json  

class Entry:
    def __init__(self, entryId, title, content, time):
        self.entryId = entryId
        self.title = title
        self.content = content
        self.time = time
    def json(self):
        return json.dumps({
            'entryId': self.entryId,
            'title': self.title,
            'content': self.content,
            'time': self.time
        })