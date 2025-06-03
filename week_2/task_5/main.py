import my_logger
import sys
from datetime import datetime

class StdoutHandler(my_logger.IHandler):
    def log(self, formatter, message):
        now = datetime.now()
        now = now.strftime(formatter)
        sys.stdout.write("Stdout [%s] %s\n" % (now, message))

class StderrHandler(my_logger.IHandler):
    def log(self, formatter, message):
        now = datetime.now()
        now = now.strftime(formatter)
        sys.stderr.write("Stderr [%s] %s\n" % (now, message))

class FileHandler(my_logger.IHandler):
    def __init__(self, filename):
        self.filename = filename

    def log(self, formatter, message):
        now = datetime.now()
        now = now.strftime(formatter)
        with open(self.filename, 'a') as file:
            file.write("[%s] %s\n" % (now, message))

stdout_handler = StdoutHandler()
stderr_handler = StderrHandler()
file_handler = FileHandler("out")

logger = my_logger.Logger()
logger.add_handler(stdout_handler)
logger.add_handler(stderr_handler)
logger.add_handler(file_handler)
logger.log("Hello world!!!")

logger.del_handler(stdout_handler)
logger.log("Another \"Hello world\"")
