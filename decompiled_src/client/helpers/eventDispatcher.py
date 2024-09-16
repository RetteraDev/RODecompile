#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/eventDispatcher.o
import inspect
import gamelog

class EventDispatcher(object):

    def __init__(self):
        self.events = {}

    def addEvent(self, event, call, priority = 0):
        if not event or not call or not callable(call):
            return
        eventFuns = self.events.get(event, [])
        for funcAndPrioriy in eventFuns:
            if funcAndPrioriy[0] == call:
                funcAndPrioriy[1] = priority
                eventFuns.sort(cmp=lambda a, b: cmp(a[1], b[1]), reverse=True)
                return

        eventFuns.append([call, priority])
        eventFuns.sort(cmp=lambda a, b: cmp(a[1], b[1]), reverse=True)
        if event not in self.events.keys():
            self.events[event] = eventFuns

    def delEvent(self, event, call):
        if not event or not call or not callable(call):
            return
        eventFuncs = self.events.get(event, [])
        if eventFuncs:
            removeEvents = []
            for item in eventFuncs:
                if item[0] == call:
                    removeEvents.append(item)

            for item in removeEvents:
                eventFuncs.remove(item)

            if not eventFuncs:
                self.events.pop(event)

    def delAllEvent(self, event):
        if event in self.events.keys():
            self.events.pop(event)

    def dispatchEvent(self, event, data = None):
        eventObj = None
        if isinstance(event, str):
            eventObj = Event(event)
        elif isinstance(event, Event):
            eventObj = event
            eventObj.handled = False
        if eventObj:
            if not eventObj.data and data:
                eventObj.data = data
            eventFuncs = self.events.get(eventObj.name, [])
            for i in reversed(xrange(len(eventFuncs))):
                try:
                    func = eventFuncs[i][0]
                    arginfo = inspect.getargspec(func)
                    if len(arginfo.args) > 1:
                        func(eventObj)
                    else:
                        func()
                    if eventObj.handled:
                        return
                except Exception as e:
                    gamelog.error('@zhp event handle error:', e.message)


class Event(object):

    def __init__(self, name, data = None, priority = 0):
        self.name = name
        self.data = data
        self.handled = False
        self.priority = priority

    def stop(self):
        self.handled = True

    def clone(self):
        e = Event(self.name, self.data, self.priority)
        e.handled = self.handled
        return e
