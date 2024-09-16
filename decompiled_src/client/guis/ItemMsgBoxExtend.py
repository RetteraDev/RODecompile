#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ItemMsgBoxExtend.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import uiUtils
from data import item_data as ID
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import fashion_convert_data as FCD

class FashionExtend(object):

    def __init__(self, proxy):
        self.proxy = proxy
        self.convertMap = {}

    def initData(self):
        if self.convertMap:
            return
        for fashionSetVals in FCD.data.itervalues():
            for fashionSetVal in fashionSetVals.itervalues():
                newSet = [ uiUtils.getParentId(itemId) for itemId in fashionSetVal ]
                for itemId in newSet:
                    self.convertMap[itemId] = newSet

    def show(self):
        title = SCD.data.get('ITEM_MSG_BOX_FASHION_EXTEND_TITLE', '')
        msg = SCD.data.get('ITEM_MSG_BOX_FASHION_EXTEND_MSG', '')
        slotNum = SCD.data.get('ITEM_MSG_BOX_FASHION_EXTEND_SLOT_NUM', 1)
        self.initData()
        self.proxy.show(title=title, msg=msg, slotNum=slotNum, yesCallback=self.yesCallback, noCallback=self.noCallback, escCallBack=self.noCallback, itemDisabledFunc=self.itemDisabledFunc, checkSetItemFunc=self.checkSetItemFunc, findEmptyPosFunc=self.findEmptyPosFunc)

    def yesCallback(self):
        if len(self.proxy.itemIdList) == 0:
            return
        p = BigWorld.player()
        remainingList = self.getRemainingList(self.proxy.itemIdList)
        if len(remainingList) > 0:
            itemName = ''
            for itemId in remainingList:
                if itemName != '':
                    itemName += gameStrings.TEXT_ACTIVITYFACTORY_280
                itemName += ID.data.get(itemId, {}).get('name', '')

            p.showGameMsg(GMDD.data.FASHION_EXHANGE_LOSE_ITEM, (itemName,))
            return
        pageList = []
        posList = []
        for value in self.proxy.posMap.values():
            pageList.append(value[1])
            posList.append(value[2])

        if gameglobal.rds.configData.get('enableWardrobeMultiDyeScheme', False):
            p.cell.fashionEquipExchangeMultiScheme(const.RES_KIND_INV, pageList, posList, False)
        else:
            p.cell.fashionEquipExchange(const.RES_KIND_INV, pageList, posList)
        self.proxy.hide()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def noCallback(self):
        self.proxy.hide()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.hide()

    def itemDisabledFunc(self, kind, page, pos, item):
        if kind == const.RES_KIND_INV:
            if not item.isFashionEquip():
                return True
            if ID.data.get(item.id).has_key('ttl'):
                return True
            itemId = uiUtils.getParentId(item.id)
            if itemId not in self.convertMap:
                return True
            if (kind, page, pos) in self.proxy.posMap.values():
                return True
            p = BigWorld.player()
            if item.checkPlayerCondition(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, needLvCheck=False):
                return True
            if len(self.proxy.itemIdList) > 0:
                remainingList = self.getRemainingList(self.proxy.itemIdList)
                if itemId not in remainingList:
                    return True
            return False
        return True

    def getRemainingList(self, resItemIdList):
        itemIdList = [ uiUtils.getParentId(itemId) for itemId in resItemIdList ]
        fashionSet = self.convertMap.get(itemIdList[0])
        if fashionSet:
            remainingList = [ itemId for itemId in fashionSet if itemId not in itemIdList ]
        else:
            remainingList = []
        return remainingList

    def checkSetItemFunc(self, item):
        if item.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return False
        return True

    def findEmptyPosFunc(self):
        for pos in xrange(self.proxy.slotNum):
            if pos not in self.proxy.posMap:
                return pos

        return 0
