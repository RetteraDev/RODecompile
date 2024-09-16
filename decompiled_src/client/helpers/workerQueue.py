#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/workerQueue.o
import threading
import traceback, sys
import BigWorld
from callbackHelper import Functor

class SimpleWorkerQueue(object):

    def __init__(self):
        self.tasks = []
        self.results = []
        self.lock = threading.RLock()
        self.rlock = threading.RLock()
        self.event = threading.Event()
        self.thread = threading.Thread(target=self.worker)
        self.thread.start()
        self.running = True
        self.cbHandler = BigWorld.callback(1, Functor(self.fetchResult))

    def worker(self):
        while True:
            self.event.wait()
            self.event.clear()
            if not self.running:
                break
            while True:
                f = None
                callback = None
                self.lock.acquire()
                if self.tasks:
                    f, args, callback = self.tasks.pop(0)
                self.lock.release()
                if f:
                    try:
                        r = f(*args)
                        if callback:
                            self.rlock.acquire()
                            self.results.append((callback, r))
                            self.rlock.release()
                    except:
                        traceback.print_exception(*sys.exc_info())

                self.lock.acquire()
                if not self.tasks:
                    self.lock.release()
                    break
                else:
                    self.lock.release()

    def applyAsync(self, f, args = [], callback = None):
        self.lock.acquire()
        self.tasks.append((f, args, callback))
        self.lock.release()
        self.event.set()

    def fetchResult(self):
        if not self.running:
            return
        callback = None
        while True:
            self.rlock.acquire()
            if self.results:
                if self.results:
                    callback, result = self.results.pop(0)
                else:
                    self.rlock.release()
                    break
            self.rlock.release()
            if callback:
                try:
                    if result:
                        callback(result)
                    else:
                        callback()
                except:
                    traceback.print_exception(*sys.exc_info())

            self.rlock.acquire()
            if not self.results:
                self.rlock.release()
                break
            else:
                self.rlock.release()

        self.cbHandler = BigWorld.callback(0.2, Functor(self.fetchResult))

    def close(self):
        self.running = False
        self.event.set()
