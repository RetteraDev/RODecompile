#Embedded file name: /WORKSPACE/data/entities/common/miniutils.o
"""
\xd7\xa8\xb8\xf8info\xc0\xe0\xd3\xc3\xb5\xc4utils
info\xc0\xe0\xb2\xbb\xd3\xc3utils\xca\xc7\xd2\xf2\xce\xaautils\xd3\xd0\xcc\xab\xb6\xe0\xb6\xab\xce\xf7
\xb1\xc8\xc8\xe7 db\xca\xb9\xd3\xc3Netease\xd2\xfd\xc6\xf0\xb1\xa8\xb4\xed
"""
import time
import BigWorld
from cPickle import loads

def getNow(isInt = True):
    if BigWorld.component in ('cell', 'base'):
        current = time.time()
    elif BigWorld.component in 'client':
        p = BigWorld.player()
        if hasattr(p, 'getServerTime'):
            current = BigWorld.player().getServerTime()
        else:
            current = time.time()
    if not isInt:
        return current
    return int(current)


def createItemObjFromDict(dict):
    return doCreateItemObjFromDict(dict)


def doCreateItemObjFromDict(d, doLoad = True, doConsistant = False):
    from item import Item, GemSlot
    it = Item(d['id'], cwrap=d['cwrap'], isNew=False)
    it.uuid = d['uuid']
    it.uutime = d['uutime']
    it.__dict__.update(doLoad and loads(d['minutia']) or d)
    for idx, slotDict in enumerate(getattr(it, 'yangSlots', ())):
        if type(slotDict) == dict:
            it.yangSlots[idx] = GemSlot.slotWithSavedData(slotDict)

    for idx, slotDict in enumerate(getattr(it, 'yinSlots', ())):
        if type(slotDict) == dict:
            it.yinSlots[idx] = GemSlot.slotWithSavedData(slotDict)

    if doConsistant:
        it.consistent()
    return it


def getItemSaveData_X(part, it):
    if not it:
        return {}
    itData = getItemSaveData(it)
    if not itData:
        return {}
    res = {'part': part}
    res.update(itData)
    return res


def getItemSaveData(it):
    from item import Item
    if not it:
        return {}
    try:
        if it.__dict__.has_key('yangSlots'):
            yangSlotsBak = list(it.yangSlots)
            for idx, sVal in enumerate(yangSlotsBak):
                it.yangSlots[idx] = sVal.getGemData(Item.GEM_TYPE_YANG)

        if it.__dict__.has_key('yinSlots'):
            yinSlotsBak = list(it.yinSlots)
            for idx, sVal in enumerate(yinSlotsBak):
                it.yinSlots[idx] = sVal.getGemData(Item.GEM_TYPE_YIN)

        res = {'uuid': it.uuid,
         'uutime': it.uutime,
         'id': it.id,
         'cwrap': it.cwrap,
         'minutia': it.dumpProp()}
        if it.__dict__.has_key('yangSlots'):
            for idx, sVal in enumerate(yangSlotsBak):
                it.yangSlots[idx] = yangSlotsBak[idx]

        if it.__dict__.has_key('yinSlots'):
            for idx, sVal in enumerate(yinSlotsBak):
                it.yinSlots[idx] = yinSlotsBak[idx]

    except Exception as e:
        import gamelog
        gamelog.error('getItemSaveData', getattr(it, 'id', 0), getattr(it, 'uuid', ''), e.message)
        return {}

    return res
