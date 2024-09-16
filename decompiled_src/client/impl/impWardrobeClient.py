#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWardrobeClient.o
import cPickle
import zlib
import BigWorld
import gamelog
import utils
import gameglobal
import const
from guis import events
from guis import wardrobeHelper
from helpers import aspectHelper
from callbackHelper import Functor
from data import item_data as ID

class ImpWardrobeClient(object):

    def openWardrobe(self, showCate = None):
        wardrobeHelper.getInstance().open(showCate)

    def closeWardrobe(self):
        wardrobeHelper.getInstance().close()

    def initWardrobeBag(self, data):
        gamelog.debug('dxk@impWardrobeClient initWardrobeBag')
        self.wardrobeBag.initInfo(data)
        self.addCheckExpireWardrobeItemsCallback(utils.getNow() + 60)
        self.wardrobeBag.requireLoveList()

    def wardrobeBagInsert(self, itemInsert, srcResKind):
        uuid = itemInsert.uuid
        self.tempInsert = itemInsert
        gamelog.debug('dxk@impWardrobeClient wardrobeBagInsert', uuid, srcResKind, itemInsert)
        self.wardrobeBag.addItem(uuid, itemInsert)
        if srcResKind != const.RES_KIND_EQUIP:
            itemCate = gameglobal.rds.ui.wardrobe.getItemCate(itemInsert.id)
            if srcResKind == const.RES_KIND_INV or srcResKind == const.RES_KIND_FASHION_BAG:
                gameglobal.rds.ui.wardrobe.scrollToUUID = uuid
                gameglobal.rds.ui.dispatchEvent(events.EVENT_WARDROBE_ITEM_CHANGED)
                self.openWardrobe(itemCate)
                wearPart = gameglobal.rds.ui.wardrobe.getWearPart(itemInsert)
                aspectHelper.getInstance().wearWardrobeItem({wearPart: uuid}, identifyStr='dyeList', callBack=Functor(gameglobal.rds.ui.wardrobe.onWearSucess, wearPart, uuid))
            else:
                gameglobal.rds.ui.dispatchEvent(events.EVENT_WARDROBE_ITEM_CHANGED)
        self.checkExpireWardrobeItem(itemInsert)

    def wardrobeBagRemove(self, itemUUID, tgtResKind):
        gamelog.debug('dxk@impWardrobeClient wardrobeBagRemove', itemUUID, tgtResKind)
        self.wardrobeBag.delItem(itemUUID)
        if tgtResKind != const.RES_KIND_EQUIP:
            gameglobal.rds.ui.dispatchEvent(events.EVENT_WARDROBE_ITEM_CHANGED)

    def wardrobeBagUpdate(self, itemUpdate):
        uuid = itemUpdate.uuid
        gamelog.debug('dxk@impWardrobeClient wardrobeBagUpdate', itemUpdate)
        self.wardrobeBag.changeItem(uuid, itemUpdate)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_WARDROBE_ITEM_CHANGED)
        self.checkExpireWardrobeItem(itemUpdate)

    def itemDyeSchemeUpdate(self, itemUpdate):
        uuid = itemUpdate.uuid
        gamelog.debug('dxk@impWardrobeClient itemDyeSchemeUpdate', itemUpdate)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_ITEM_DYE_SCHEME_CHANGED, itemUpdate)

    def getWardrobeItemWearPart(self, uuid):
        for i in xrange(len(self.equipment)):
            equip = self.equipment[i]
            if equip:
                if getattr(equip, 'uuid', '') == uuid:
                    return i

        return -1

    def checkExpireWardrobeItem(self, item):
        if not item:
            return
        if item.isExpireTTL() or not self.checkWardrobeItemValid(item):
            self.checkExpireWardrobeItems()
            return
        expireTime = item.getTTLExpireTime()
        if expireTime:
            self.addCheckExpireWardrobeItemsCallback(expireTime)

    def checkWardrobeItemValid(self, item):
        bodyType = self.physique.bodyType
        if not utils.inAllowBodyType(item.id, bodyType):
            return False
        if not utils.inAllowSex(item.id, self.physique.sex):
            return False
        return True

    def addCheckExpireWardrobeItemsCallback(self, tWhen):
        now = self.getServerTime()
        if not hasattr(self, '_nextCheckExpireWardrobeItemsTime') or self._nextCheckExpireWardrobeItemsTime <= now:
            self._nextCheckExpireWardrobeItemsTime = 0
            self._nextCheckExpireWardrobeItemsCallback = None
        if tWhen <= now - const.CLIENT_EXPIRETIME_CHECK_DELAY:
            return
        else:
            if tWhen <= now:
                tWhen = now + const.CLIENT_EXPIRETIME_CHECK_DELAY
            tWhen = tWhen + 1
            if self._nextCheckExpireWardrobeItemsTime == 0 or tWhen < self._nextCheckExpireWardrobeItemsTime:
                self._nextCheckExpireWardrobeItemsTime = tWhen
                if self._nextCheckExpireWardrobeItemsCallback:
                    BigWorld.cancelCallback(self._nextCheckExpireWardrobeItemsCallback)
                self._nextCheckExpireWardrobeItemsCallback = BigWorld.callback(tWhen - now, self.checkExpireWardrobeItems)
            return

    def checkExpireWardrobeItems(self):
        if not self.inWorld or self._isSoul():
            return
        else:
            now = self.getServerTime()
            tNext = 0
            expireItems = []
            for uuid in self.wardrobeBag.drobeItems:
                item = self.wardrobeBag.drobeItems.get(uuid, None)
                if item.isExpireTTL() or not self.checkWardrobeItemValid(item):
                    expireItems.append(uuid)
                else:
                    expireTime = item.getTTLExpireTime()
                    if expireTime > now - const.CLIENT_EXPIRETIME_CHECK_DELAY and (not tNext or expireTime < tNext):
                        tNext = expireTime

            if expireItems:
                expireItems = expireItems[:5]
                gamelog.debug('dxk@impWardrobeClient wardrobe items expire:', expireItems)
                self.base.requireRemoveWardrobeExpiredItems(expireItems)
                self.addCheckExpireWardrobeItemsCallback(now + const.CLIENT_EXPIRETIME_CHECK_DELAY)
            if tNext:
                self.addCheckExpireWardrobeItemsCallback(tNext)
            return

    def onUpdateWardrobeLoveList(self, loveList):
        buf = zlib.decompress(loveList)
        loveListInfo = cPickle.loads(buf)
        gamelog.debug('dxk@impWardrobeClient onUpdateWardrobeLoveList:', loveListInfo)
        self.wardrobeBag.updateLoveList(loveListInfo)
        gameglobal.rds.ui.wardrobe.refreshItemsInsiteInfo(True)

    def onFinishExchangeWardrobeEquip(self, extraArgs):
        gamelog.debug('dxk@impWardrobeClient onFinishExchangeWardrobeEquip:', extraArgs)
        aspectHelper.getInstance().onSucessWearCloths(extraArgs)

    def onUpdateWardrobeCustomScheme(self, customSchemeZip):
        buf = zlib.decompress(customSchemeZip)
        schemeInfo = cPickle.loads(buf)
        gamelog.debug('dxk@impWardrobeClient onUpdateWardrobeCustomScheme:', schemeInfo)
        self.wardrobeBag.updateSchemeInfo(schemeInfo)
        gameglobal.rds.ui.myCloth.refreshSchemeInfo()
