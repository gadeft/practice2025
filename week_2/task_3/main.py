from datetime import datetime
import sys

class Logger:
    def __init__(self, out_stream, formatter):
        self._out_stream = out_stream
        self._formatter = formatter

    def log(self, message):
        now = datetime.now()
        print("[%s] %s" % (now.strftime(self._formatter), message))

