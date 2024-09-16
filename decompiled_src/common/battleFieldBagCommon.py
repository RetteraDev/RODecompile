#Embedded file name: I:/bag/tmp/tw2/res/entities\common/battleFieldBagCommon.o
from userDictType import UserDictType
import const
from item import Item

class BattleFieldBagCommon(UserDictType):

    def __init__(self):
        super(BattleFieldBagCommon, self).__init__()
        self.version = 0
        self.freeze = 0
        self.suit = {}
        self.opstr = ''
        self.locker = 0
        self.state = 0

    def _lateReload(self):
        super(BattleFieldBagCommon, self)._lateReload()
        for val in self.itervalues():
            if val:
                val.reloadScript()

    def searchBestInPages(self, itemId, amount, src = None):
        if amount > Item.maxWrap(itemId):
            return (const.CONT_NO_PAGE, const.CONT_NO_POS)
        if not src:
            src = Item(itemId, cwrap=amount, genRandProp=False)
        if src.canWrap():
            for pos in self.iterkeys():
                dst = self[pos]
                if dst == const.CONT_EMPTY_VAL:
                    continue
                if dst.id != src.id:
                    continue
                if dst.overBear(amount):
                    continue
                if not src.canMerge(src, dst):
                    continue
                return (1, pos)

        for pos in xrange(const.BATTLE_FIELD_BAG_MAX_NUM):
            if not self.has_key(pos):
                return (1, pos)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)
