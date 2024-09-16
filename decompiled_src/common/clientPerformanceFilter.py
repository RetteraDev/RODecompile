#Embedded file name: I:/bag/tmp/tw2/res/entities\common/clientPerformanceFilter.o
from userSoleType import UserSoleType
from userDictType import UserDictType

class ClientPerformanceFilterVal(UserSoleType):

    def __init__(self, id, name, condition, interval, prob, gbId, urs):
        self.id = id
        self.name = name
        self.condition = condition
        self.interval = interval
        self.prob = prob
        self.gbId = gbId
        self.urs = urs

    def _lateReload(self):
        super(ClientPerformanceFilterVal, self)._lateReload()

    def listFilter(self):
        return {'condition': self.condition,
         'interval': self.interval,
         'prob': self.prob}

    def listAllFilter(self):
        return {'name': self.name,
         'condition': self.condition,
         'interval': self.interval,
         'prob': self.prob,
         'gbId': self.gbId,
         'urs': self.urs}


class ClientPerformanceFilterInfo(UserDictType):

    def __init__(self):
        super(ClientPerformanceFilterInfo, self).__init__()

    def _lateReload(self):
        super(ClientPerformanceFilterInfo, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def addFilter(self, id, name, condition, interval, prob, gbId, urs):
        filter = ClientPerformanceFilterVal(id, name, condition, interval, prob, gbId, urs)
        self[filter.id] = filter

    def delFilterById(self, id):
        if not self.has_key(id):
            return False
        self.pop(id, None)
        return True

    def checkFilterName(self, name):
        for id, info in self.iteritems():
            if info.name == name:
                return False

        return True

    def delFilterByName(self, name):
        delId = 0
        for id, info in self.iteritems():
            if info.name == name:
                delId = id
                break

        self.pop(delId, None)
        return delId

    def listAllFilter(self):
        info = {}
        for id, value in self.iteritems():
            info[id] = {'name': value.name,
             'condition': value.condition,
             'interval': value.interval,
             'prob': value.prob,
             'gbId': value.gbId,
             'urs': value.urs}

        return info

    def listFilterById(self, id):
        if not self.has_key(id):
            return {}
        return {'name': self[id].name,
         'condition': self[id].condition,
         'interval': self[id].interval,
         'prob': self[id].prob,
         'gbId': self[id].gbId,
         'urs': self[id].urs}

    def listFilterByName(self, name):
        for id, info in self.iteritems():
            if info.name == name:
                return self.listFilterById(id)

        return {}

    def getFilterVal(self, name):
        for id, info in self.iteritems():
            if info.name == name:
                return info
