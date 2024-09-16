#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yaBiaoProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import formula
import const
import gameglobal
import gametypes
import utils
import ui
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from guis import events
from data import yabiao_data as YBD
from data import yabiao_config_data as YBCD
from data import npc_yabiao_data as NYD
from data import empty_zaiju_data as EZD
from cdata import game_msg_def_data as GMDD

class YaBiaoProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(YaBiaoProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirmAccept': self.onConfirmAccept,
         'teleportToZaiju': self.onTeleportToZaiju,
         'completeFailYabiao': self.onCompleteFailYabiao}
        uiAdapter.registerEscFunc(uiConst.WIDGET_YA_BIAO_ACCEPT, self.hideYaBiaoAccept)
        uiAdapter.registerEscFunc(uiConst.WIDGET_YA_BIAO, self.hideYaBiaoInfo)
        self.nextTeleportTime = 0
        self.reset()
        self.addEvent(events.EVENT_PLAYER_SPACE_NO_CHANGED, self.onSpaceNoChanged, 0, True)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_YA_BIAO_ACCEPT:
            self.yabiaoAcceptMed = mediator
            ybTypeData = YBCD.data.get('yabiaoTypeData', {}).get(self.yabiaoType, {})
            initData = {'title': ybTypeData.get('name', ''),
             'desc': ybTypeData.get('desc', ''),
             'tip': ybTypeData.get('tip', ''),
             'helpTxt': YBCD.data.get('yabiaoHelpTxt', ''),
             'guideTip': YBCD.data.get('guideTip', ''),
             'hasGuideEffect': BigWorld.player().hasYabiaoGuideEffect()}
            if self.yabiaoType == gametypes.YABIAO_TYPE_DANGER:
                initData['defaultItemTip'] = YBCD.data.get('acceptYaobiaoItemTip', '')
            else:
                initData['defaultItemTip'] = YBCD.data.get('acceptYaobiaoNormolTip', '')
            bonusData = self.getBonusItemData()
            initData.update(bonusData)
            self.uiAdapter.inventory.show()
            return uiUtils.dict2GfxDict(initData, True)
        if widgetId == uiConst.WIDGET_YA_BIAO:
            self.yabiaoMed = mediator
            initData = self.getYabiaoData()
            return uiUtils.dict2GfxDict(initData, True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_YA_BIAO:
            self.hideYaBiaoInfo()
        elif widgetId == uiConst.WIDGET_YA_BIAO_ACCEPT:
            self.hideYaBiaoAccept()

    def show(self):
        if self.enableYaBiao():
            self.uiAdapter.loadWidget(uiConst.WIDGET_YA_BIAO)

    def showYaBiaoAccept(self, yabiaoType, npcId):
        if self.enableYaBiao():
            self.yabiaoType = yabiaoType
            self.yabiaoNpcId = npcId
            self.uiAdapter.loadWidget(uiConst.WIDGET_YA_BIAO_ACCEPT)

    def clearWidget(self):
        self.hideYaBiaoAccept()
        self.hideYaBiaoInfo()

    def reset(self):
        self.yabiaoMed = None
        self.yabiaoAcceptMed = None
        self.yabiaoType = 0
        self.yabiaoNpcId = 0
        self.yabiaoItem = None

    def hideYaBiaoAccept(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_YA_BIAO_ACCEPT)
        self.yabiaoAcceptMed = None
        self.yabiaoItem = None
        self.uiAdapter.inventory.hide()

    def hideYaBiaoInfo(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_YA_BIAO)
        self.yabiaoMed = None

    def enableYaBiao(self):
        return gameglobal.rds.configData.get('enableYabiao', False)

    def onTriggerNpc(self, npcEntityId, npcId, yabiaoType):
        npcType = NYD.data.get(npcId, {}).get('type')
        if npcType == gametypes.NPC_YABIAO_MARKER:
            npc = BigWorld.entities.get(npcEntityId)
            if npc:
                npc.cell.triggerYabiao()
                self.uiAdapter.funcNpc.close()
        elif npcType == gametypes.NPC_YABIAO_ACCEPT:
            p = BigWorld.player()
            if p._isSoul():
                p.showGameMsg(GMDD.data.SOUL_CANNOT_ACCEPT_YABIAO, ())
                self.uiAdapter.funcNpc.onDefaultState()
            else:
                self.showYaBiaoAccept(yabiaoType, npcEntityId)
        elif npcType == gametypes.NPC_YABIAO_COMPLETE:
            npc = BigWorld.entities.get(npcEntityId)
            if npc:
                if yabiaoType:
                    npc.cell.completeFailedYabiao()
                else:
                    npc.cell.completeYabiao()
                self.uiAdapter.funcNpc.close()
        elif npcType == gametypes.NPC_YABIAO_UPGRADE:
            npc = BigWorld.entities.get(npcEntityId)
            if npc:
                npc.cell.upgradeYabiao()
                self.uiAdapter.funcNpc.close()

    def onAcceptYaBiao(self, ybId, res):
        if res:
            self.hideYaBiaoAccept()
            if BigWorld.player().yabiaoData:
                self.show()
                self.uiAdapter.topBar.refreshTopBarWidgets()
                self.uiAdapter.questTrack.hideTrackPanel(True)

    def onTriggerYabiao(self, res):
        if res == gametypes.MARKER_TRIGGER_SUC:
            self.refreshYabiaoView()
            self.uiAdapter.funcNpc.close()
        msgIdName = 'MARKER_TRIGGER_MSG_%s' % res
        BigWorld.player().showGameMsg(getattr(GMDD.data, msgIdName, 0), ())

    def onCompleteYabiao(self, res, isFailedYabiao):
        if isFailedYabiao:
            msgIdName = 'YABIAO_FAIL_COMP_MSG_%s' % res
        else:
            msgIdName = 'YABIAO_COMP_MSG_%s' % res
        BigWorld.player().showGameMsg(getattr(GMDD.data, msgIdName, 0), ())
        if res == gametypes.YABIAO_COMP_SUC or res == gametypes.YABIAO_FAIL_COMP_SUC:
            self.hide()

    def onUpgradeYabiao(self, res, oldZaijuNo, newZaijuNo):
        msgIdName = 'YABIAO_UPGRADE_MSG_%s' % res
        if res in (gametypes.YABIAO_UPGRADE_SUC, gametypes.YABIAO_UPGRADE_SUC_MATE):
            data = (EZD.data.get(newZaijuNo, {}).get('name', ''),)
        else:
            data = ()
        BigWorld.player().showGameMsg(getattr(GMDD.data, msgIdName, 0), data)

    def onTeleportToYabiao(self, res):
        if res:
            self.nextTeleportTime = utils.getNow() + YBCD.data.get('teleportCD', 30)
            if self.yabiaoMed:
                self.yabiaoMed.Invoke('refreshTranBtnCd', GfxValue(self.nextTeleportTime))

    def getBonusItemData(self):
        ybId, yabiaoData = self.getCurrentYabiaoData()
        result = {}
        if yabiaoData:
            headerReward = yabiaoData.get('headerReward')
            if headerReward:
                rewardId, cnt = headerReward[0]
                result['extraItem'] = uiUtils.getGfxItemById(rewardId, cnt, appendInfo={'itemName': uiUtils.getItemColorName(rewardId)})
            bonusItem = []
            zaijuNo = yabiaoData.get('zaijuInfo', ((0, 0),))[0][0]
            compRewardItems = YBCD.data.get('compRewardItems', {0: 0}).get(zaijuNo)
            if compRewardItems:
                for reward in compRewardItems:
                    cRwardId, cnt = reward
                    cnt = int(self.getTotalRate(ybId, True) * cnt)
                    if cnt:
                        bonusItem.append(uiUtils.getGfxItemById(cRwardId, cnt, appendInfo={'itemName': uiUtils.getItemColorName(cRwardId)}))

            rate = self.getServerStarAdjustRate(ybId, False)
            failBonusIitem = []
            compRewardItems = YBCD.data.get('compFailedRewardItems', {0: 0}).get(zaijuNo)
            if compRewardItems:
                for reward in compRewardItems:
                    cRwardId, cnt = reward
                    cnt = int(self.getTotalRate(ybId, False) * cnt)
                    if cnt:
                        failBonusIitem.append(uiUtils.getGfxItemById(cRwardId, cnt, appendInfo={'itemName': uiUtils.getItemColorName(cRwardId)}))

            result['bonusItem'] = bonusItem
            result['failBonusIitem'] = failBonusIitem
            result['rate'] = (rate,)
            result['rateMsg'] = (YBCD.data.get('rateMsg', '%s') % int(round((rate - 1) * 100)),)
            promiseCash = yabiaoData.get('promiseCash', 0)
            if promiseCash:
                result['needCash'] = uiUtils.convertNumStr(BigWorld.player().cash, promiseCash, False)
                result['canAccept'] = BigWorld.player().cash >= promiseCash and self.yabiaoItem != None
            else:
                result['canAccept'] = self.yabiaoItem != None
        return result

    def getCurrentYabiaoData(self):
        for key, data in YBD.data.items():
            if data.get('type') == self.yabiaoType:
                if self.yabiaoItem:
                    if data.get('itemId') == self.yabiaoItem.getParentId():
                        return (key, data)
                else:
                    return (key, data)

    @ui.uiEvent(uiConst.WIDGET_YA_BIAO_ACCEPT, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nPos = event.data['pos']
        if i == None:
            return
        else:
            self.setYaoBiaoItem(i)
            self.uiAdapter.inventory.updateSlotState(nPage, nPos)
            return

    def onSpaceNoChanged(self):
        p = BigWorld.player()
        if p.yabiaoData and formula.inWorldWar(p.spaceNo):
            self.show()
        if not formula.inWorldWar(p.spaceNo):
            self.hide()

    def setYaoBiaoItem(self, item):
        if self.yabiaoAcceptMed:
            self.yabiaoItem = item
            itemData = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
            itemData['count'] = '%s/1' % item.cwrap
            self.yabiaoAcceptMed.Invoke('setYaoBiaoItem', uiUtils.dict2GfxDict(itemData, True))
            self.yabiaoAcceptMed.Invoke('refreshBonous', uiUtils.dict2GfxDict(self.getBonusItemData(), True))

    def isItemDisabled(self, kind, page, pos, item):
        if kind == const.RES_KIND_INV:
            if self.yabiaoAcceptMed:
                itemIds = []
                for val in YBD.data.values():
                    if val.get('type') == self.yabiaoType:
                        itemIds.append(val.get('itemId', 0))

                return item.getParentId() not in itemIds or self.yabiaoItem == item
        return False

    def getYabiaoData(self):
        p = BigWorld.player()
        yabiaoData = p.yabiaoData
        ybId = yabiaoData[gametypes.YABIAO_ID]
        acTime = yabiaoData[gametypes.YABIAO_BEGIN_TIME]
        zaijuNo = yabiaoData[gametypes.YABIAO_ZAIJU_NO]
        markInfo = yabiaoData[gametypes.YABIAO_MARKER_INFO]
        seq = yabiaoData[gametypes.YABIAO_MARKER_SEQ]
        headerName = yabiaoData[gametypes.YABIAO_HEADER_NAME]
        ybCfgData = YBD.data.get(ybId, {})
        ybType = ybCfgData.get('type', {})
        rate = self.getServerStarAdjustRate(ybId, False)
        bonusItem = []
        for itemId, cnt in YBCD.data.get('compRewardItems', {}).get(zaijuNo, ()):
            cnt = int(self.getTotalRate(ybId, True) * cnt)
            if cnt > 0:
                bonusItem.append(uiUtils.getGfxItemById(itemId, cnt))

        failBonusIitem = []
        for itemId, cnt in YBCD.data.get('compFailedRewardItems', {}).get(zaijuNo, ()):
            cnt = int(self.getTotalRate(ybId, False) * cnt)
            if cnt > 0:
                failBonusIitem.append(uiUtils.getGfxItemById(itemId, cnt))

        currentStep = seq + 1
        for _, res in markInfo.values():
            if res:
                currentStep += 1

        data = {'bonusItem': bonusItem,
         'failBonusIitem': failBonusIitem,
         'rate': rate,
         'rateMsg': YBCD.data.get('rateMsg', '%s') % int(round((rate - 1) * 100)),
         'title': YBCD.data.get('yabiaoTypeData', {}).get(ybType, {}).get('name', ''),
         'zaijuMax': p.yabiaoZaijuInfo[1],
         'zaijuCurrent': p.yabiaoZaijuInfo[0],
         'zaijuBroken': not yabiaoData[gametypes.YABIAO_WHOLE],
         'zaijuBrokenDes': YBCD.data.get('zaijuBrokenDes', ''),
         'transCost': YBCD.data.get('teleportCost', 0),
         'leftTime': acTime + ybCfgData.get('timeLimit', 0) - utils.getNow(),
         'yabiaoStep': currentStep,
         'stepTips': YBCD.data.get('stepTips', ()),
         'stepSeekIds': YBCD.data.get('stepSeekIds', ()),
         'stepNames': YBCD.data.get('stepNames', ()),
         'headerName': headerName,
         'zaiju': uiUtils.getGfxItemById(EZD.data.get(zaijuNo, {}).get('refItem', 999)),
         'guideTip': YBCD.data.get('guideTip', ''),
         'hasGuideEffect': p.hasYabiaoGuideEffect(),
         'transEnableTime': self.nextTeleportTime}
        headerReward = ybCfgData.get('headerReward', ())
        if headerReward:
            reWardId, cnt = headerReward[0]
            data['headerItem'] = uiUtils.getGfxItemById(reWardId, cnt)
        return data

    def refreshYabiaoView(self):
        if not self.enableYaBiao():
            return
        if self.yabiaoMed:
            if BigWorld.player().yabiaoData:
                self.yabiaoMed.Invoke('refresh', uiUtils.dict2GfxDict(self.getYabiaoData(), True))
            else:
                self.hideYaBiaoInfo()

    def refreshYabiaoZaijuBar(self):
        if self.yabiaoMed:
            self.yabiaoMed.Invoke('refreshBar', uiUtils.array2GfxAarry(BigWorld.player().yabiaoZaijuInfo))

    @ui.callFilter(1, True)
    def onConfirmAccept(self, *args):
        p = BigWorld.player()
        if not p.groupNUID:
            msg = YBCD.data.get('singleAcceptYabiaoMsg', '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.confirmAcceptYabiao, gameStrings.TEXT_YABIAOPROXY_345, self.cancelAcceptYabiao, gameStrings.TEXT_YABIAOPROXY_347)
        else:
            self.confirmAcceptYabiao()

    def confirmAcceptYabiao(self):
        npc = BigWorld.entities.get(self.yabiaoNpcId)
        if npc and self.yabiaoItem:
            for key, data in YBD.data.items():
                if data.get('type') == self.yabiaoType and data.get('itemId') == self.yabiaoItem.getParentId():
                    npc.cell.acceptYabiao(key)
                    self.uiAdapter.funcNpc.close()
                    break

    def cancelAcceptYabiao(self):
        self.uiAdapter.funcNpc.close()

    @ui.callFilter(1, True)
    def onTeleportToZaiju(self, *args):
        BigWorld.player().cell.teleportToYabiao()

    def onCompleteFailYabiao(self, *args):
        BigWorld.player().cell.completeFailedYabiao()

    def getTotalRate(self, ybId, suc):
        rate = self.getServerStarAdjustRate(ybId, suc)
        if BigWorld.player().hasYabiaoGuideEffect():
            rate *= YBCD.data.get('guideRewardRate', 1)
        return rate

    def getServerStarAdjustRate(self, ybId, suc):
        ybd = YBD.data.get(ybId, {})
        if ybd.has_key('sucStarRates') and suc:
            rates = ybd['sucStarRates']
        elif ybd.has_key('failStarRates') and not suc:
            rates = ybd['failStarRates']
        else:
            return 1
        ww = BigWorld.player().worldWar
        questStarLv, enemyQuestStarLv = ww.calcQuestStarLv(ww.getCountry().enemyHostId)
        starLvMargin = enemyQuestStarLv - questStarLv
        for lvMargin, rate in rates:
            if starLvMargin >= lvMargin:
                return rate
        else:
            return 1
