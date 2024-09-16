#Embedded file name: I:/bag/tmp/tw2/res/entities\common/pickledItem.o
import copy
from cPickle import loads
import item
from userSoleType import UserSoleType
from data import item_data as ID

class PickledItem(UserSoleType):

    def __init__(self, id, cwrap, uuid, uutime, minutia):
        d = self.__dict__
        d['id'] = id
        d['cwrap'] = cwrap
        d['uuid'] = uuid
        d['uutime'] = uutime
        d['minutia'] = minutia

    def copyDict(self):
        return copy.deepcopy(self.__dict__)

    def dumpProp(self):
        return self.__dict__['minutia']

    def getType(self):
        try:
            tp = ID.data.get(self.id, {})['type']
            return tp
        except:
            return item.Item.PROPERTY_CHART['type']

    def isRuneEquip(self):
        return self.getType() == self.BASETYPE_RUNE_EQUIP

    def isHieroEquip(self):
        return self.getType() == self.BASETYPE_HIEROGRAM_EQUIP

    def getRuneData(self):
        self.changeToItem()
        return self.getRuneData()

    def updateProp(self, d):
        self.__dict__.update(d)
        return self

    def changeToItem(self):
        object.__setattr__(self, '__class__', item.Item)
        minutia = self.__dict__.pop('minutia')
        item.Item.__init__(self, self.__dict__['id'], self.__dict__['cwrap'], isNew=False)
        self.__dict__.update(loads(minutia))
        self.__dict__['cwrap'] = int(self.__dict__['cwrap'])
        for idx, slotDict in enumerate(self.__dict__.get('yangSlots', ())):
            if type(slotDict) == dict:
                self.__dict__['yangSlots'][idx] = item.GemSlot.slotWithSavedData(slotDict)

        for idx, slotDict in enumerate(self.__dict__.get('yinSlots', ())):
            if type(slotDict) == dict:
                self.__dict__['yinSlots'][idx] = item.GemSlot.slotWithSavedData(slotDict)

    def __getattr__(self, name):
        self.changeToItem()
        return getattr(self, name)

    def __setattr__(self, name, value):
        if name == '__class__':
            return object.__setattr__(self, '__class__', value)
        self.changeToItem()
        return setattr(self, name, value)

    def __delattr__(self, name):
        self.changeToItem()
        return delattr(self, name)

    def __getnewargs__(self):
        return (self.__dict__,)

    def __getstate__(self):
        return (self.__dict__,)

    def __setstate__(self, st):
        self.__dict__.update(st[0])

    def __str__(self):
        return 'PickledItem'
