#Embedded file name: /WORKSPACE/data/entities/common/callbackhelper.o
import BigWorld
import sys
import traceback
import gamelog

class Functor(object):

    def __init__(self, fn, *args):
        self.fn = fn
        self.args = args

    def __call__(self, *args):
        try:
            return self.fn(*(self.args + args))
        except Exception as e:
            self.catchException(args, e)

    def catchException(self, args, e):
        if BigWorld.component not in 'client':
            return
        p = BigWorld.player()
        if p and p.__class__.__name__ == 'PlayerAvatar':
            msg = 'callback functor error %s, %s, %s, %s, %s' % (str(self.fn)[:60],
             str(self.args)[:100],
             str(args)[:100],
             str(e.__class__.__name__)[:20],
             str(e.message)[:100])
            tp, val, exc_tb = sys.exc_info()
            tbStrList = []
            for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
                fName = filename.split('/')[-1]
                tbStrList.append('\n%s:%s in %s()' % (fName, linenum, funcname))

            s = ''.join(tbStrList)[:350]
            msg = msg + s
            gamelog.error('jbx:callbackException', msg)
            p.reportClientException(1, [msg], 0, {})
        else:
            gamelog.error('jbx:raceback.format_exc():\n' + traceback.format_exc())


class StateFunctor(Functor):

    def __init__(self, state, fn, *args):
        self.__old_state = state.get()
        self.__state = state
        super(StateFunctor, self).__init__(fn, args)

    def __call__(self, *args):
        if self.__state.get() == self.__old_state:
            super(StateFunctor, self).__call__(args)


class State(object):

    def __init__(self):
        self.__id = 0

    def change(self):
        self.__id += 1

    def get(self):
        return self.__id

    def set(self, _id):
        self.__id = _id

    def functor(self, state, fn, *args):
        return StateFunctor(self, fn, args)


class CallbackSyncer(object):
    __callbackMap = {}

    @classmethod
    def removeCallback(cls, owner):
        oid = id(owner)
        cls.__callbackMap.pop(oid, None)

    def __init__(self, owner, fn, *args, **kw):
        super(CallbackSyncer, self).__init__()
        self.__callbackMap[id(owner)] = id(self)
        self.__owner = owner
        self.__fn = fn
        self.__args = args
        self.__kw = kw

    def __call__(self, *args, **kw):
        oid = id(self.__owner)
        if self.__fn and self.__callbackMap.get(oid) == id(self):
            del self.__callbackMap[oid]
            fn = self.__fn
            call_args = list(args)
            call_args.extend(self.__args)
            call_kw = self.__kw
            call_kw.update(kw)
            self.__fn = None
            return fn(*call_args, **call_kw)

    def __del__(self):
        oid = id(self.__owner)
        if self.__callbackMap.get(oid) == id(self):
            del self.__callbackMap[oid]
