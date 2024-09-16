#Embedded file name: /WORKSPACE/data/entities/common/container.o
import zlib
import cPickle
import BigWorld
import gametypes
import const
import utils
import gamelog
import commonDecorator
from item import Item
from const import CONT_EMPTY_VAL
from userSoleType import UserSoleType
from pickledItem import PickledItem
if BigWorld.component in ('base', 'cell'):
    from data import equip_data as ED

class Container(UserSoleType):

    def __init__(self, pageCount, width, height):
        super(Container, self).__init__()
        self.pageCount = pageCount
        self.width = width
        self.height = height
        self.posCount = width * height
        self.pages = []
        for pg in xrange(self.pageCount):
            self.pages.append([ CONT_EMPTY_VAL for ps in xrange(self.posCount) ])

        self.cacheItemCntDic = {}

    def refreshContainer(self, slotCount, width, height, needKeep = False):
        self.width = width
        self.height = height
        self.posCount = width * height
        if slotCount % self.posCount:
            self.pageCount = slotCount / self.posCount + 1
        else:
            self.pageCount = slotCount / self.posCount
        if needKeep == False:
            self.pages = []
            for pg in xrange(self.pageCount):
                self.pages.append([ CONT_EMPTY_VAL for ps in xrange(self.posCount) ])

        else:
            pageTemp = self.pages
            self.pages = []
            for pg in xrange(self.pageCount):
                if pg < len(pageTemp):
                    self.pages.append(pageTemp[pg])
                else:
                    self.pages.append([ CONT_EMPTY_VAL for ps in xrange(self.posCount) ])

    def _lateReload(self):
        super(Container, self)._lateReload()
        for page in self.pages:
            for it in page:
                if it != CONT_EMPTY_VAL:
                    it.reloadScript()

    def _isValidPos(self, pos):
        if pos < 0 or pos >= self.posCount:
            return False
        return True

    def _isValidPage(self, page):
        if page < 0 or page >= self.pageCount:
            return False
        return True

    def _isValid(self, page, pos):
        if self._isValidPage(page) and self._isValidPos(pos):
            return True
        else:
            return False

    def consistent(self, packSlot = None):
        if not hasattr(self, 'version'):
            return False
        currVer = Item.TIMESTAMP
        if self.version == currVer:
            return False
        for pg in self.getPageTuple():
            for ps in self.getPosTuple(pg):
                obj = self.getQuickVal(pg, ps)
                if obj == CONT_EMPTY_VAL:
                    continue
                obj.consistent()

        if packSlot:
            for obj in packSlot:
                if obj == CONT_EMPTY_VAL:
                    continue
                obj.consistent()

        self.version = currVer
        return True

    def transfer(self, owner, resKind, barSlot = None, barResKind = None):
        for pg in xrange(self.pageCount):
            for ps in xrange(self.posCount):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                owner.client.resInsert(resKind, it, pg, ps)

        if barSlot:
            for k, v in enumerate(barSlot):
                if v == const.CONT_EMPTY_VAL:
                    continue
                owner.client.resInsert(barResKind, v, 0, k)

    def isInvalid(self, page, pos):
        return not self._isValid(page, pos)

    def isSame(self, src, dst):
        if src == dst:
            return True
        return False

    def isEmpty(self, page, pos):
        return self.getQuickVal(page, pos) == CONT_EMPTY_VAL

    def isFill(self, page, pos):
        return self.getQuickVal(page, pos) != CONT_EMPTY_VAL

    def isFull(self, page, pos):
        obj = self.getQuickVal(page, pos)
        if obj == CONT_EMPTY_VAL:
            return False
        if obj.cwrap != obj.mwrap:
            return False
        return True

    def isEnough(self, page, pos, amount):
        obj = self.getQuickVal(page, pos)
        if obj == CONT_EMPTY_VAL:
            return False
        if obj.cwrap != amount:
            return False
        return True

    def areEmpty(self, page):
        for ps in xrange(self.posCount):
            if self.getQuickVal(page, ps) != CONT_EMPTY_VAL:
                return False

        return True

    def areAllEmpty(self):
        for pg in xrange(len(self.pages)):
            for ps in xrange(self.posCount):
                if self.getQuickVal(pg, ps) != CONT_EMPTY_VAL:
                    return False

        return True

    def areFill(self, page):
        for ps in xrange(self.posCount):
            if self.getQuickVal(page, ps) == CONT_EMPTY_VAL:
                return False

        return True

    def areFull(self, page):
        for ps in xrange(self.posCount):
            if self.getQuickVal(page, ps) == CONT_EMPTY_VAL:
                return False
            obj = self.getQuickVal(page, ps)
            if obj.cwrap != obj.mwrap:
                return False

        return True

    def getPageTuple(self):
        return range(self.pageCount)

    def getPosTuple(self, page):
        if not self._isValidPage(page):
            return ()
        return range(self.posCount)

    def getQuickVal(self, page, pos, changeToItem = True):
        if page == const.CONT_NO_PAGE and pos == const.CONT_NO_POS:
            return CONT_EMPTY_VAL
        elif page < len(self.pages) and pos < len(self.pages[page]):
            it = self.pages[page][pos]
            if it.__class__ is PickledItem and changeToItem:
                it.changeToItem()
            return it
        else:
            return CONT_EMPTY_VAL

    def setQuickVal(self, obj, page, pos):
        self.updateCountCache(obj, page, pos)
        self.pages[page][pos] = obj

    def updateCountCache(self, obj, page, pos):
        oldObj = self.pages[page][pos]
        oldParentId, oldCnt = (oldObj.getParentId(), oldObj.cwrap) if oldObj and not oldObj.hasLatch() else (0, 0)
        newParentId, newCnt = (obj.getParentId(), obj.cwrap) if obj and not obj.hasLatch() else (0, 0)
        if newParentId == oldParentId:
            self.cacheItemCntDic[oldParentId] = self.cacheItemCntDic.get(oldParentId, 0) + newCnt - oldCnt
        else:
            self.cacheItemCntDic[oldParentId] = self.cacheItemCntDic.get(oldParentId, 0) - oldCnt
            self.cacheItemCntDic[newParentId] = self.cacheItemCntDic.get(newParentId, 0) + newCnt

    def updateWarpCountCache(self, obj, count):
        parentId = obj.getParentId()
        self.cacheItemCntDic[parentId] = self.cacheItemCntDic.get(parentId, 0) + count - obj.cwrap

    def countItemCntFromCache(self, itemId):
        return self.cacheItemCntDic.get(Item.parentId(itemId), 0)

    def getSaveList(self):
        slist = []
        for i, page in enumerate(self.pages):
            for j, it in enumerate(page):
                if not it:
                    continue
                prop = utils.getItemSaveData_XY(i, j, it)
                if not prop:
                    continue
                slist.append(prop)

        return slist

    def getStreamList(self):
        slist = []
        for i, page in enumerate(self.pages):
            for j, it in enumerate(page):
                if not it:
                    continue
                prop = utils.getItemStreamData_XY(i, j, it)
                if not prop:
                    continue
                slist.append(prop)

        return slist

    def _reportCritical(self, page, pos, obj):
        if BigWorld.component in ('base', 'cell'):
            import gameengine
            gameengine.reportCritical('Error: Verify in Container(%d,%d):%d(%s,%s),%d(%d)' % (page,
             pos,
             obj.id,
             obj.name,
             obj.guid(),
             obj.cwrap,
             obj.mwrap))

    def verifyObj(self, page, pos):
        obj = self.getQuickVal(page, pos)
        if not obj:
            return
        if obj.cwrap <= 0 or obj.cwrap > obj.mwrap:
            self._reportCritical(page, pos, obj)

    def setObj(self, obj, page, pos):
        self.setQuickVal(obj, page, pos)
        self.verifyObj(page, pos)

    def insertObj(self, obj, page, pos, logInfo = None):
        self.setQuickVal(obj, page, pos)
        self.verifyObj(page, pos)

    @commonDecorator.assetReturnValueNotEquals(False)
    def removeObj(self, page, pos, logInfo = None):
        if self.getQuickVal(page, pos) == CONT_EMPTY_VAL:
            return False
        self.setQuickVal(CONT_EMPTY_VAL, page, pos)

    def searchByID(self, objID, page, startPos = 0):
        if not self._isValid(page, startPos):
            return const.CONT_NO_POS
        posCount = self.getPosCount(page)
        for dstPos in xrange(startPos, posCount):
            obj = self.getQuickVal(page, dstPos)
            if obj == CONT_EMPTY_VAL:
                continue
            if obj.id != objID:
                continue
            else:
                return dstPos

        return const.CONT_NO_POS

    def searchByIDList(self, objIDList, page, startPos = 0):
        if not self._isValid(page, startPos):
            return const.CONT_NO_POS
        posCount = self.getPosCount(page)
        for dstPos in xrange(startPos, posCount):
            obj = self.getQuickVal(page, dstPos)
            if obj == CONT_EMPTY_VAL:
                continue
            if obj.id not in objIDList:
                continue
            else:
                return dstPos

        return const.CONT_NO_POS

    def findItemById(self, id):
        pages = self.getPageTuple()
        for pg in pages:
            ps = self.searchByID(id, pg, 0)
            if ps != const.CONT_NO_POS:
                return (pg, ps)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def findItemByUUID(self, uuid):
        pages = self.getPageTuple()
        for pg in pages:
            for ps in self.getPosTuple(pg):
                obj = self.getQuickVal(pg, ps)
                if obj == const.CONT_EMPTY_VAL:
                    continue
                if hasattr(obj, 'uuid') and obj.uuid == uuid:
                    return (obj, pg, ps)

        return (const.CONT_EMPTY_VAL, const.CONT_NO_PAGE, const.CONT_NO_POS)

    def searchByParentId(self, parentId, page, startPos = 0):
        if not self._isValid(page, startPos):
            return const.CONT_NO_POS
        posCount = self.getPosCount(page)
        for dstPos in xrange(startPos, posCount):
            obj = self.getQuickVal(page, dstPos)
            if obj == CONT_EMPTY_VAL:
                continue
            if obj.getParentId() != parentId:
                continue
            else:
                return dstPos

        return const.CONT_NO_POS

    def searchByParentList(self, parentList, page, startPos = 0):
        if not self._isValid(page, startPos):
            return const.CONT_NO_POS
        posCount = self.getPosCount(page)
        for dstPos in xrange(startPos, posCount):
            obj = self.getQuickVal(page, dstPos)
            if obj == CONT_EMPTY_VAL:
                continue
            if obj.getParentId() not in parentList:
                continue
            else:
                return dstPos

        return const.CONT_NO_POS

    def searchAllByID(self, objID, page):
        if not self._isValid(page, 0):
            return []
        all = []
        pos = 0
        while True:
            dstPos = self.searchByID(objID, page, pos)
            if dstPos == const.CONT_NO_POS:
                break
            all.append((page, dstPos))
            pos = dstPos + 1

        return all

    def searchEmpty(self, page, startPos = 0):
        if not self._isValid(page, startPos):
            return const.CONT_NO_POS
        posCount = self.getPosCount(page)
        for ps in xrange(startPos, posCount):
            if not self.getQuickVal(page, ps):
                return ps
        else:
            return const.CONT_NO_POS

    def countBlank(self, page, startPos = 0):
        if not self._isValid(page, startPos):
            return 0
        cnt = 0
        pos = startPos
        total = self.getPosCount(page)
        while True:
            if pos >= total:
                break
            if self.getQuickVal(page, pos) == CONT_EMPTY_VAL:
                cnt += 1
            pos += 1

        return cnt

    def shiftObj(self, page, pos, amount):
        obj = self.getQuickVal(page, pos)
        if obj:
            self.updateWarpCountCache(obj, amount)
            obj.setWrap(amount)
            self.verifyObj(page, pos)

    def wrapObj(self, page, pos, amount, logInfo = None):
        obj = self.getQuickVal(page, pos)
        if obj:
            totalWrap = obj.cwrap + amount
            if totalWrap == 0:
                self.removeObj(page, pos, logInfo)
            elif totalWrap > 0:
                self.updateWarpCountCache(obj, totalWrap)
                obj.setWrap(totalWrap)
            elif totalWrap < 0:
                self.verifyObj(page, pos)
                gamelog.error('Error:wrap obj invalid', page, pos, obj.id, obj.mwrap, obj.cwrap)
                self.removeObj(page, pos, logInfo)
            self.verifyObj(page, pos)

    def moveObj(self, srcPage, srcPos, dstPage, dstPos):
        obj = self.getQuickVal(srcPage, srcPos)
        self.removeObj(srcPage, srcPos, None)
        self.insertObj(obj, dstPage, dstPos, None)
        self.verifyObj(srcPage, srcPos)
        self.verifyObj(dstPage, dstPos)

    def exchangeObj(self, srcPage, srcPos, dstPage, dstPos):
        obj = self.getQuickVal(srcPage, srcPos)
        it2 = self.getQuickVal(dstPage, dstPos)
        self.insertObj(obj, dstPage, dstPos, None)
        self.insertObj(it2, srcPage, srcPos, None)
        self.verifyObj(srcPage, srcPos)
        self.verifyObj(dstPage, dstPos)

    def cleanPage(self, page):
        if not self._isValidPage(page):
            return
        for ps in xrange(self.posCount):
            self.updateCountCache(None, page, ps)

        self.pages[page] = [ CONT_EMPTY_VAL for ps in xrange(self.posCount) ]

    def updateObj(self, uuid, page, pos, props):
        obj = self.getQuickVal(page, pos)
        if obj and obj.uuid == uuid:
            obj.updateAttribute(props)
            self.verifyObj(page, pos)

    def searchEmptyInAllPage(self, exclude = ()):
        blanks = []
        for pg in self.getPageTuple():
            if pg in exclude:
                continue
            for ps in self.getPosTuple(pg):
                if not self.pages[pg][ps]:
                    blanks.append((pg, ps))

        return blanks

    def getPosCount(self, page):
        return self.posCount

    def grepBest(self, src):
        pages = self.getPageTuple()
        if src.canWrap():
            for pg in pages:
                posCount = self.getPosCount(pg)
                for ps in xrange(posCount):
                    dst = self.getQuickVal(pg, ps)
                    if dst == const.CONT_EMPTY_VAL:
                        continue
                    if dst.id != src.id:
                        continue
                    if dst.beMax():
                        continue
                    if not src.canMerge(src, dst):
                        continue
                    return (pg, ps)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def searchByName(self, name, findFunc, page, startPos = 0):
        ret = []
        if not self._isValid(page, startPos):
            return ret
        posCount = self.getPosCount(page)
        for dstPos in xrange(startPos, posCount):
            obj = self.getQuickVal(page, dstPos)
            if obj == CONT_EMPTY_VAL:
                continue
            find = findFunc(obj.name, name)
            if not find:
                continue
            else:
                ret.append((page, dstPos, obj.uuid))

        return ret

    def searchAllByName(self, name, findFunc):
        all = []
        for pg in xrange(self.pageCount):
            findItems = self.searchByName(name, findFunc, pg)
            all.append(findItems)

        return all

    def searchUnbindItem(self, exclude = ()):
        for page in self.pages:
            for it in page:
                if not it:
                    continue
                if it.id in exclude:
                    continue
                if not it.isForeverBind():
                    return it.id

        return 0

    def checkItemUnbindTimes(self):
        for page in self.pages:
            for it in page:
                if it and ED.data.get(it.id, {}).get('unbindTimes', 0) > 0:
                    return False

        return True

    def resetItemUnbindTimes(self):
        for page in self.pages:
            for it in page:
                if not it:
                    continue
                unbindTimes = ED.data.get(it.id, {}).get('unbindTimes', 0)
                if unbindTimes == 0:
                    continue
                if it.isManualEquip() or it.isExtendedEquip():
                    it.unbindTimes = unbindTimes
                    dumpit = it.getItemAfterIdentify()
                    if dumpit:
                        dumpit.unbindTimes = unbindTimes
                        it.dumpAfterIdentify = zlib.compress(cPickle.dumps(utils.getItemSaveData(dumpit)))
                else:
                    it.unbindTimes = unbindTimes
                it.bindItem()

    def getBagItemCount(self, itemId, bindPolicy = gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False, filterFunc = None):
        cnt = 0
        for pg in self.getPageTuple():
            for ps in self.getPosTuple(pg):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.getParentId() != itemId if enableParentCheck else it.id != itemId:
                    continue
                if not self._checkBindPolicy(bindPolicy, it):
                    continue
                if not includeExpired and it.isExpireTTL():
                    continue
                if not includeLatch and it.hasLatch():
                    continue
                if not includeShihun and it.isShihun():
                    continue
                if filterFunc and not filterFunc(it):
                    continue
                cnt += it.cwrap

        return cnt

    def getMaterialBagItemCount(self, itemId, bindPolicy = gametypes.ITEM_REMOVE_POLICY_UNBIND_FIRST, enableParentCheck = False, includeExpired = False, includeLatch = False, includeShihun = False, filterFunc = None):
        num = 0
        p = BigWorld.player()
        posCountDict = getattr(p.materialBag, 'posCountDict', {})
        for page in posCountDict:
            for i in xrange(posCountDict[page]):
                it = p.materialBag.getQuickVal(page, i)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.getParentId() != itemId if enableParentCheck else it.id != itemId:
                    continue
                if not self._checkBindPolicy(bindPolicy, it):
                    continue
                if not includeExpired and it.isExpireTTL():
                    continue
                if not includeLatch and it.hasLatch():
                    continue
                if not includeShihun and it.isShihun():
                    continue
                if filterFunc and not filterFunc(it):
                    continue
                num += it.cwrap

        return num

    def _checkBindPolicy(self, bindPolicy, item):
        if bindPolicy in gametypes.ITEM_REMOVE_POLICY_ALL:
            return True
        elif bindPolicy == gametypes.ITEM_REMOVE_POLICY_BIND_ONLY:
            return item.isForeverBind()
        else:
            return not item.isForeverBind()

    def hasItem(self, assosiateItemIds):
        for pg in self.getPageTuple():
            for ps in self.getPosTuple(pg):
                it = self.getQuickVal(pg, ps)
                if it and it.id in assosiateItemIds:
                    return True

        return False
