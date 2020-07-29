import os
import fcntl
import threading
from time import sleep


class Lock:
    @staticmethod
    def getFileLock(fileName):
        return FileLock(fileName)


class FileLock:
    def __init__(self, fileName):
        lock_file = fileName
        lock_dir = '/tmp'
        self.file = os.path.join(lock_dir, lock_file)
        self.thread_lock = threading.Lock()
        self._fn = None

        self.release()

    def acquire(self):
        self.thread_lock.acquire()
        self._fn = open(self.file, 'a')
        fcntl.flock(self._fn.fileno(), fcntl.LOCK_EX)

    def release(self):
        if self._fn:
            try:
                self._fn.close()
                self.thread_lock.release()
            except Exception as e:
                print(e)

#