#Embedded file name: /WORKSPACE/data/entities/client/guis/aspecthelper.o
import BigWorld
import copy
import utils
import gameglobal
from guis import uiUtils
from cdata import game_msg_def_data as GMDD

class AspectHeleper(object):

    def __init__(self):
        super(AspectHeleper, self).__init__()

    def resetAspect(self):
        p = BigWorld.player()
        p.signal = p.signalOld
        temp = copy.deepcopy(p.aspect)
        p.aspect = copy.deepcopy(p.aspectOld)
        p.aspectOld = copy.deepcopy(temp)
        p.set_aspect(None)

    def wearCloth(self, item):
        p = BigWorld.player()
        bodyType = p.physique.bodyType
        if not utils.inAllowBodyType(item.id, bodyType):
            p.showGameMsg(GMDD.data.ITEM_USE_BODYTYPE_ERROR, ())
            return
        p.signal = 8
        parts = list(item.whereEquip())
        parts.extend(uiUtils.getAspectParts(item.id))
        for part in parts:
            p.aspect.set(part, item.id, getattr(item, 'dyeList', []), getattr(item, 'enhLv', 0), getattr(item, 'rongGuang', []))

        p.refreshAspectClient()


aspcetHelperIns = None

def getInstance():
    global aspcetHelperIns
    if not aspcetHelperIns:
        aspcetHelperIns = AspectHeleper()
    return aspcetHelperIns
