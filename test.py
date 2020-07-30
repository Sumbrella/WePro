from WePro.until.User import User
from WePro.until.Date import Date
from WePro.tool.saveClockDescription import saveClockDescription
from WePro.until.Lock import Lock

import threading

lock = Lock.getFileLock('description')
user = User("oF7S25CRBHEe_iOoVwJ7ntQPpo5o")
date = Date(2020, 7, 30)


class TestThreading(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        saveClockDescription(lock, user, date, 'jpg')

