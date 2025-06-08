"""
Context manager for working with JSON files.
Opens a json file, parses its contents into the variable content and returns it.
When closing, writes everything from the variable content to the file and closes it.
"""

import json

class JsonContextManager:
    def __init__(self, filename, params: str):
        self.filename = filename
        self.params = params
        self.content = None

    def __enter__(self):
        self.file = open(self.filename, self.params)
        self.content = json.load(self.file)
        return self.content

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.params not in ['r', 'rb']:
            self.file.seek(0)
            self.file.truncate(0)
            self.file.write(json.dumps(self.content))
        self.file.close()