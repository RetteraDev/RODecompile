#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/propSchemeResumeProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import uiUtils
import time
import const
import gametypes
from gameStrings import gameStrings
from ui import gbk2unicode
from uiProxy import UIProxy
from data import sys_config_data as SCD
from cdata import item_fame_score_cost_data as IFSCD
from cdata import item_parentId_data as IPD
USE_FOR_PROP = 0
USE_FOR_SKILL = 1

class PropSchemeResumeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PropSchemeResumeProxy, self).__init__(uiAdapter)
        self.modelMap = {'dismiss': self.onDismiss,
         'commit': self.onCommit,
         'getCurrentNeedItem': self.onGetCurrentNeedItem,
         'getCurrentAddTime': self.onGetCurrentAddTime,
         'getCurrentTimeText': self.onGetCurrentTimeText,
         'getTitle': self.onGetTitle,
         'getCurrentTimeTextByState': self.onGetCurrentTimeTextByState}
        self.mediator = None
        self.resetMediator = None
        self.schemeNo = -1
        self.totalCost = 0
        self.funcType = USE_FOR_PROP
        uiAdapter.registerEscFunc(uiConst.WIDGET_PROP_SCHEME_RESUME, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def onDismiss(self, *args):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PROP_SCHEME_RESUME)

    def clearWidget(self):
        self.mediator.Invoke('cancel', ())

    def onCommit(self, *args):
        state = int(args[3][0].GetNumber())
        if self.funcType == USE_FOR_PROP:
            scheme = BigWorld.player().getPropSchemeById(self.schemeNo)
            if not scheme:
                BigWorld.player().cell.enablePropScheme(self.schemeNo, '', state)
            else:
                BigWorld.player().cell.resetPropSchemeExpire(self.schemeNo, state)
        else:
            scheme = BigWorld.player().getSkillSchemeConvertById(self.schemeNo)
            if not scheme:
                BigWorld.player().cell.enableSkillScheme(self.schemeNo, True, state)
            else:
                BigWorld.player().cell.enableSkillScheme(self.schemeNo, False, state)
        if self.funcType == USE_FOR_PROP:
            if not scheme:
                data = SCD.data.get('enablePropSchemeData')
            else:
                data = SCD.data.get('resetPropSchemeExpireData')
        elif not scheme:
            data = SCD.data.get('enableSkillSchemeData')
        else:
            data = SCD.data.get('resetSkillSchemeExpireData')
        itemId = 0
        if data.get(state):
            itemId = int(self.getCanShowItemId(data.get(state)[0]))
        if not itemId:
            return
        else:
            p = BigWorld.player()
            needNum = 1
            allNum = 0
            allList = p.inv.findAllItemInPages(itemId, gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, True, False, False, False)
            for pg, ps in allList:
                cit = p.inv.getQuickVal(pg, ps)
                if not cit.isExpireTTL() and not cit.hasLatch():
                    allNum += cit.cwrap

            if allNum >= needNum or p.fame.get(const.YUN_CHUI_JI_FEN_FAME_ID, 0) >= self.totalCost:
                self.onDismiss(None)
            return

    def onGetTitle(self, *args):
        if self.funcType == USE_FOR_PROP:
            scheme = BigWorld.player().getPropSchemeById(self.schemeNo)
        else:
            scheme = BigWorld.player().getSkillSchemeConvertById(self.schemeNo)
        if scheme:
            title = gameStrings.TEXT_PROPSCHEMERESUMEPROXY_103
        else:
            title = gameStrings.TEXT_PROPSCHEMERESUMEPROXY_105
        return GfxValue(gbk2unicode(title))

    def onGetCurrentTimeTextByState(self, *args):
        if self.funcType == USE_FOR_PROP:
            scheme = BigWorld.player().getPropSchemeById(self.schemeNo)
            if not scheme:
                data = SCD.data.get('enablePropSchemeData')
            else:
                data = SCD.data.get('resetPropSchemeExpireData')
        else:
            scheme = BigWorld.player().getSkillSchemeConvertById(self.schemeNo)
            if not scheme:
                data = SCD.data.get('enableSkillSchemeData')
            else:
                data = SCD.data.get('resetSkillSchemeExpireData')
        state = int(args[3][0].GetNumber())
        day = data.get(state)[1] / 86400
        if scheme:
            timeText = gameStrings.TEXT_PROPSCHEMERESUMEPROXY_124 % day
        else:
            timeText = gameStrings.TEXT_PROPSCHEMERESUMEPROXY_126 % day
        return GfxValue(gbk2unicode(timeText))

    def onGetCurrentTimeText(self, *args):
        if self.funcType == USE_FOR_PROP:
            scheme = BigWorld.player().getPropSchemeById(self.schemeNo)
            if not scheme:
                data = SCD.data.get('enablePropSchemeData')
            else:
                data = SCD.data.get('resetPropSchemeExpireData')
        else:
            scheme = BigWorld.player().getSkillSchemeConvertById(self.schemeNo)
            if not scheme:
                data = SCD.data.get('enableSkillSchemeData')
            else:
                data = SCD.data.get('resetSkillSchemeExpireData')
        textArray = []
        for i in (1, 2):
            day = data.get(i)[1] / 86400
            scheme = BigWorld.player().getPropSchemeById(self.schemeNo)
            if scheme:
                timeText = gameStrings.TEXT_PROPSCHEMERESUMEPROXY_148 % day
            else:
                timeText = gameStrings.TEXT_PROPSCHEMERESUMEPROXY_150 % day
            textArray.append(timeText)

        return uiUtils.array2GfxAarry(textArray, True)

    def onGetCurrentNeedItem(self, *args):
        if self.funcType == USE_FOR_PROP:
            scheme = BigWorld.player().getPropSchemeById(self.schemeNo)
            if not scheme:
                data = SCD.data.get('enablePropSchemeData')
            else:
                data = SCD.data.get('resetPropSchemeExpireData')
        else:
            scheme = BigWorld.player().getSkillSchemeConvertById(self.schemeNo)
            if not scheme:
                data = SCD.data.get('enableSkillSchemeData')
            else:
                data = SCD.data.get('resetSkillSchemeExpireData')
        state = int(args[3][0].GetNumber())
        itemId = 0
        if data.get(state):
            itemId = int(self.getCanShowItemId(data.get(state)[0]))
        if not itemId:
            return
        p = BigWorld.player()
        needNum = 1
        allNum = 0
        allList = p.inv.findAllItemInPages(itemId, gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, True, False, False, False)
        for pg, ps in allList:
            cit = p.inv.getQuickVal(pg, ps)
            if not cit.isExpireTTL() and not cit.hasLatch():
                allNum += cit.cwrap

        itemInfo = uiUtils.getGfxItemById(itemId, uiUtils.convertNumStr(allNum, needNum))
        if allNum < needNum:
            itemInfo['state'] = uiConst.COMPLETE_ITEM_LEAKED
        else:
            itemInfo['state'] = uiConst.ITEM_NORMAL
        deltaNum = needNum - allNum
        itemFameTxt = {}
        if deltaNum > 0 and gameglobal.rds.configData.get('enableYunChuiScoreDikou', False):
            itemIds = IPD.data.get(itemId, [])
            for id in itemIds:
                if IFSCD.data.has_key(id):
                    itemFameData = IFSCD.data.get(id, {})
                    itemCost = itemFameData.get(const.YUN_CHUI_JI_FEN_FAME_ID, 0)

            totalCost = deltaNum * itemCost
            self.totalCost = totalCost
            itemFameTxt['line1'] = gameStrings.ITEM_FAME_INSTANTLY_PURCHASE_1
            itemFameTxt['line2'] = gameStrings.ITEM_FAME_INSTANTLY_PURCHASE_2 % totalCost
        self.setItemFameCost(itemFameTxt)
        return uiUtils.dict2GfxDict(itemInfo, True)

    def setItemFameCost(self, costTxt):
        self.mediator.Invoke('setItemFameCost', uiUtils.dict2GfxDict(costTxt, True))

    def getCanShowItemId(self, itemList):
        canUseItemId = None
        p = BigWorld.player()
        for itemId in itemList:
            needNum = 1
            allNum = 0
            allList = p.inv.findAllItemInPages(int(itemId), gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, True, False, False, False)
            for pg, ps in allList:
                cit = p.inv.getQuickVal(pg, ps)
                if not cit.isExpireTTL() and not cit.hasLatch():
                    allNum += cit.cwrap

            if allNum >= needNum:
                canUseItemId = itemId
                break

        if canUseItemId == None:
            canUseItemId = itemList[0]
        return canUseItemId

    def onGetCurrentAddTime(self, *args):
        state = int(args[3][0].GetNumber())
        if self.funcType == USE_FOR_PROP:
            data = SCD.data.get('enablePropSchemeData')
            addTime = data.get(state)[1]
            scheme = BigWorld.player().getPropSchemeById(self.schemeNo)
        else:
            data = SCD.data.get('enableSkillSchemeData')
            addTime = data.get(state)[1]
            scheme = BigWorld.player().getSkillSchemeConvertById(self.schemeNo)
        if scheme and scheme['expireTime'] > BigWorld.player().getServerTime():
            finalTime = addTime + scheme['expireTime']
            finalStr = gameStrings.TEXT_PROPSCHEMERESUMEPROXY_240 % scheme['schemeName'] + time.strftime('%Y.%m.%d  %H:%M', time.localtime(finalTime))
        else:
            finalTime = BigWorld.player().getServerTime() + addTime
            if self.funcType == USE_FOR_PROP:
                finalStr = gameStrings.TEXT_PROPSCHEMERESUMEPROXY_244 % BigWorld.player().getSchemeDefaultName(self.schemeNo) + time.strftime('%Y.%m.%d  %H:%M', time.localtime(finalTime))
            else:
                finalStr = gameStrings.TEXT_PROPSCHEMERESUMEPROXY_244 % BigWorld.player().getSkillSchemeName(self.schemeNo) + time.strftime('%Y.%m.%d  %H:%M', time.localtime(finalTime))
        return GfxValue(gbk2unicode(finalStr))

    def show(self, schemeNo, funcType = USE_FOR_PROP):
        if self.mediator:
            return
        self.funcType = funcType
        self.schemeNo = schemeNo
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PROP_SCHEME_RESUME)
