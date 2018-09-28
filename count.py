from datetime import datetime
count = 0
def increment_entryId():
    global count
    count = count + 1
    return count

print(increment_entryId())

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

print(get_timestamp())

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))