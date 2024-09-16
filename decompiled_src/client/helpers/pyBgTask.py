#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/pyBgTask.o
from __future__ import with_statement
import threading
import BigWorld
g_instance_mgr = None

class TaskCallback(object):

    def __init__(self, mgr, callback):
        self.__mgr = mgr
        self.__func = callback

    def __call__(self, *args, **kw):
        self.__mgr.add_callback(self.__func, args, kw)


class PyBgTaskMgr(object):
    lock = threading.Lock()

    def __init__(self):
        self.callback_handle = BigWorld.callback(0.1, self.process_tasks)
        self.callback_list = []

    def process_tasks(self):
        self.callback_handle = BigWorld.callback(0.1, self.process_tasks)
        callback_item = None
        with self.lock:
            if len(self.callback_list) > 0:
                callback_item = self.callback_list.pop(0)
        if callback_item:
            func, args, kw = callback_item
            func(*args, **kw)

    def stop_tasks(self):
        if self.callback_handle:
            BigWorld.cancelCallback(self.callback_handle)
            self.callback_handle = None
        with self.lock:
            self.callback_list = []

    def add_task(self, work_func, func_args):
        task_thread = threading.Thread(target=work_func, args=func_args)
        task_thread.start()

    def make_callback(self, callback):
        return TaskCallback(self, callback)

    def add_callback(self, callback, args, kw):
        with self.lock:
            self.callback_list.append((callback, args, kw))


def init():
    global g_instance_mgr
    if g_instance_mgr:
        g_instance_mgr.stop_tasks()
    g_instance_mgr = PyBgTaskMgr()


def getMgr():
    return g_instance_mgr
