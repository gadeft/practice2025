from datetime import datetime
import sys

class Logger:
    def __init__(self, out_stream = sys.stdout, formatter = "%Y.%m.%d %H:%M:%S"):
        self._out_stream = out_stream
        self._formatter = formatter

    def log(self, message):
        now = datetime.now()
        now = now.strftime(self._formatter)
        print("[%s] %s" % (now, message), file = self._out_stream)
