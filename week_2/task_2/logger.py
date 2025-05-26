import sys
from datetime import datetime

def log(message):
    now = datetime.now()
    sys.stderr.write(now.strftime("[%Y.%m.%d %H:%M:%S]"))
    sys.stderr.write(f" {message}\n")

log('The test message')
