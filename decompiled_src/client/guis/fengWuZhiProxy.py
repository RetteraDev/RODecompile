#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fengWuZhiProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import clientUtils
import ui
import gamelog
from uiProxy import UIProxy
from Scaleform import GfxValue
from data import qiren_clue_data as QCD
from data import fengwuzhi_item_data as FID
from data import fengwuzhi_area_data as FAD
from data import fengwuzhi_area_overview_data as FAOD
from data import fengwuzhi_group_data as FGD
from cdata import game_msg_def_data as GMDD
IDX_AREA_PANEL = 1
IDX_OVERVIEW_PANEL = 2
IDX_DETAIL_PANEL = 3
IDX_AWARD_PANEL = 4
IDX_PANDECT_PANEL = 5
SECOND_IDX_DETAIL_PANEL_DESC = 1
SECOND_IDX_DETAIL_PANEL_CLUE = 2
MAP_TYPE_YUNCHUI = 0
MAP_TYPE_YISHIJIE = 1

class FengWuZhiProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FengWuZhiProxy, self).__init__(uiAdapter)
        self.modelMap = {'getAreaBaseInfo': self.onGetAreaBaseInfo,
         'getAreaInfo': self.onGetAreaInfo,
         'getOverviewTabInfo': self.onGetOverviewTabInfo,
         'getOverviewDetailInfo': self.onGetOverviewDetailInfo,
         'getDetailInfo': self.onGetDetailInfo,
         'getDetailResearchInfo': self.onGetDetailResearchInfo,
         'getAwardInfo': self.onGetAwardInfo,
         'getPandectInfo': self.onGetPandectInfo,
         'getBonus': self.onGetBonus,
         'getMapType': self.onGetMapType}
        self.mediator = None
        self.mapType = 0
        self.clueToItem = {}
        self.itemToArea = {}
        self.curPanelIdx = 0
        self.curPanelArg = 0
        self.curPanelSecondIdx = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FENG_WU_ZHI, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FENG_WU_ZHI:
            self.mediator = mediator
            info = {'curPanelIdx': self.curPanelIdx,
             'curPanelArg': self.curPanelArg,
             'curPanelSecondIdx': self.curPanelSecondIdx}
            return uiUtils.dict2GfxDict(info, True)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FENG_WU_ZHI)

    def reset(self):
        self.curPanelIdx = 0
        self.curPanelArg = 0
        self.curPanelSecondIdx = 0

    def showDetailDescPanel(self, itemId):
        self.show(IDX_DETAIL_PANEL, itemId, SECOND_IDX_DETAIL_PANEL_DESC)

    def showDetailCluePanel(self, itemId):
        self.show(IDX_DETAIL_PANEL, itemId, SECOND_IDX_DETAIL_PANEL_CLUE)

    def show(self, curPanelIdx = IDX_AREA_PANEL, curPanelArg = 0, curPanelSecondIdx = 0):
        if not gameglobal.rds.configData.get('enableFengWuZhi', False):
            return
        self.curPanelIdx = curPanelIdx
        self.curPanelArg = curPanelArg
        self.curPanelSecondIdx = curPanelSecondIdx
        self.initBaseData()
        if self.mediator:
            if self.curPanelIdx == IDX_DETAIL_PANEL:
                self.mediator.Invoke('showDetailPanel', (GfxValue(self.curPanelArg), GfxValue(self.curPanelSecondIdx)))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FENG_WU_ZHI)

    def onGetAreaBaseInfo(self, *arg):
        areaList = []
        self.mapType = self.getMapType()
        for areaId, value in FAD.data.iteritems():
            if value.get('mapType', 0) != self.mapType:
                continue
            areaInfo = {}
            areaInfo['areaId'] = areaId
            areaInfo['name'] = value.get('name', '')
            pos = value.get('pos')
            if not pos:
                continue
            areaInfo['x'] = pos[0]
            areaInfo['y'] = pos[1]
            areaList.append(areaInfo)

        return uiUtils.array2GfxAarry(areaList, True)

    def onGetAreaInfo(self, *arg):
        self.curPanelIdx = IDX_AREA_PANEL
        self.curPanelArg = 0
        self.refreshAreaInfo()

    def _isItemCompleted(self, itemId):
        clueIdList = FID.data.get(itemId, {}).get('clueIdList', ())
        if not clueIdList:
            return False
        p = BigWorld.player()
        return all([ p.getClueFlag(cid) for cid in clueIdList ])

    def refreshAreaInfo(self):
        if self.curPanelIdx != IDX_AREA_PANEL:
            return
        if self.mediator:
            info = {}
            self.mapType = self.getMapType()
            for areaId, value in FAD.data.iteritems():
                if value.get('mapType', 0) != self.mapType:
                    continue
                areaInfo = {}
                areaInfo['curValue'] = self.getCurAreaNum(areaId)
                areaInfo['maxValue'] = self.getMaxAreaNum(areaId)
                info[areaId] = areaInfo

            self.mediator.Invoke('refreshAreaInfo', uiUtils.dict2GfxDict(info, True))

    def onGetOverviewTabInfo(self, *arg):
        areaId = int(arg[3][0].GetNumber())
        overviewId = int(arg[3][1].GetNumber())
        self.curPanelIdx = IDX_OVERVIEW_PANEL
        self.curPanelArg = 0
        self.refreshOverviewTabInfo(areaId, overviewId)

    def refreshOverviewTabInfo(self, areaId, overviewId):
        if self.mediator:
            info = {}
            info['overviewId'] = overviewId
            overviewList = []
            overviewIdList = FAD.data.get(areaId, {}).get('overviewIdList')
            if overviewIdList:
                for overviewId in overviewIdList:
                    maxItemNum = 0
                    curItemNum = 0
                    faod = FAOD.data.get(overviewId, {})
                    overviewInfo = {}
                    overviewInfo['overviewId'] = overviewId
                    overviewList.append(overviewInfo)
                    itemIdList = faod.get('itemIdList', ())
                    maxItemNum = len(itemIdList)
                    for itemId in itemIdList:
                        if self._isItemCompleted(itemId):
                            curItemNum = curItemNum + 1

                    overviewInfo['name'] = '%s(%d/%d)' % (faod.get('name', ''), curItemNum, maxItemNum)

            info['overviewList'] = overviewList
            self.mediator.Invoke('refreshOverviewTabInfo', uiUtils.dict2GfxDict(info, True))

    def onGetOverviewDetailInfo(self, *arg):
        overviewId = int(arg[3][0].GetNumber())
        self.curPanelIdx = IDX_OVERVIEW_PANEL
        self.curPanelArg = overviewId
        self.refreshOverviewDetailInfo(overviewId)

    def refreshOverviewDetailInfo(self, overviewId):
        if self.curPanelIdx != IDX_OVERVIEW_PANEL or self.curPanelArg != overviewId:
            return
        if self.mediator:
            itemList = []
            itemIdList = FAOD.data.get(overviewId, {}).get('itemIdList', ())
            if itemIdList:
                for itemId in itemIdList:
                    fid = FID.data.get(itemId, {})
                    if not fid:
                        continue
                    itemInfo = {}
                    itemInfo['itemId'] = itemId
                    itemInfo['name'] = fid.get('name', '')
                    if self._isItemCompleted(itemId):
                        itemInfo['iconPath'] = 'fengwuzhi/110/color/%d.dds' % fid.get('icon', 0)
                    else:
                        itemInfo['iconPath'] = 'fengwuzhi/110/gray/%d.dds' % fid.get('icon', 0)
                    itemInfo['rarity'] = 'rarity%d' % fid.get('rarity', 0)
                    itemInfo['newTipVisible'] = fid.get('newTip', 0)
                    itemList.append(itemInfo)

            self.mediator.Invoke('refreshOverviewDetailInfo', uiUtils.array2GfxAarry(itemList, True))

    def onGetDetailInfo(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        self.curPanelIdx = IDX_DETAIL_PANEL
        self.curPanelArg = itemId
        self.curPanelSecondIdx = SECOND_IDX_DETAIL_PANEL_DESC
        self.refreshDetailInfo(itemId)

    def refreshDetailInfo(self, itemId):
        if self.curPanelIdx != IDX_DETAIL_PANEL or self.curPanelArg != itemId or self.curPanelSecondIdx != SECOND_IDX_DETAIL_PANEL_DESC:
            return
        if self.mediator:
            info = {}
            fid = FID.data.get(itemId, {})
            info['itemId'] = itemId
            if self._isItemCompleted(itemId):
                info['iconPath'] = 'fengwuzhi/200/color/%d.dds' % fid.get('icon', 0)
                info['collectFlagVisible'] = True
            else:
                info['iconPath'] = 'fengwuzhi/200/gray/%d.dds' % fid.get('icon', 0)
                info['collectFlagVisible'] = False
            info['name'] = fid.get('name', '')
            info['desc'] = fid.get('desc', '')
            info['areaId'], info['overviewId'] = self.itemToArea.get(itemId, (0, 0))
            self.mediator.Invoke('refreshDetailInfo', uiUtils.dict2GfxDict(info, True))

    def onGetDetailResearchInfo(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        self.curPanelIdx = IDX_DETAIL_PANEL
        self.curPanelArg = itemId
        self.curPanelSecondIdx = SECOND_IDX_DETAIL_PANEL_CLUE
        self.refreshDetailResearchInfo(itemId)

    def refreshDetailResearchInfo(self, itemId):
        if self.curPanelIdx != IDX_DETAIL_PANEL or self.curPanelArg != itemId or self.curPanelSecondIdx != SECOND_IDX_DETAIL_PANEL_CLUE:
            return
        if self.mediator:
            p = BigWorld.player()
            info = {}
            fid = FID.data.get(itemId, {})
            info['itemId'] = itemId
            if self._isItemCompleted(itemId):
                info['iconPath'] = 'fengwuzhi/200/color/%d.dds' % fid.get('icon', 0)
                info['collectFlagVisible'] = True
            else:
                info['iconPath'] = 'fengwuzhi/200/gray/%d.dds' % fid.get('icon', 0)
                info['collectFlagVisible'] = False
            researchList = []
            clueIdList = FID.data.get(itemId, {}).get('clueIdList', ())
            if clueIdList:
                for clueId in clueIdList:
                    qcd = QCD.data.get(clueId, {})
                    if not qcd:
                        continue
                    researchInfo = {}
                    if clueId and p.getClueFlag(clueId):
                        researchInfo['state'] = 'finish'
                    else:
                        researchInfo['state'] = 'going'
                    researchInfo['stepNum'] = qcd.get('stepNum', 0)
                    desc = qcd.get('desc', '')
                    preClueIdList = qcd.get('preClueIdList', ())
                    if preClueIdList:
                        for preClueId in preClueIdList:
                            if preClueId and not p.getClueFlag(preClueId):
                                desc = uiUtils.getTextFromGMD(GMDD.data.FENG_WU_ZHI_UNKNOWN_CLUE, gameStrings.TEXT_FENGWUZHIPROXY_278)
                                break

                    researchInfo['desc'] = desc
                    researchList.append(researchInfo)

            info['researchList'] = researchList
            info['areaId'], info['overviewId'] = self.itemToArea.get(itemId, (0, 0))
            self.mediator.Invoke('refreshDetailResearchInfo', uiUtils.dict2GfxDict(info, True))

    def onGetAwardInfo(self, *arg):
        areaId = int(arg[3][0].GetNumber())
        self.curPanelIdx = IDX_AWARD_PANEL
        self.curPanelArg = areaId
        self.refreshAwardInfo(areaId)

    def refreshAwardInfo(self, areaId):
        if self.curPanelIdx != IDX_AWARD_PANEL or self.curPanelArg != areaId:
            return
        if self.mediator:
            p = BigWorld.player()
            info = {}
            fad = FAD.data.get(areaId, {})
            if not fad:
                return
            fengwuzhiBonusFlag = p.fengwuzhiBonusFlags.get(areaId, {})
            info['areaName'] = fad.get('name', '')
            info['curValue'] = self.getCurAreaNum(areaId)
            info['maxValue'] = self.getMaxAreaNum(areaId)
            bounsList = []
            gainBonusNumList = fad.get('gainBonusNumList', ())
            bonusIdList = fad.get('bonusIdList', ())
            if gainBonusNumList and bonusIdList:
                bonusLen = min(len(gainBonusNumList), len(bonusIdList))
                for i in xrange(bonusLen):
                    bounsId = bonusIdList[i]
                    itemBonus = clientUtils.genItemBonus(bounsId)
                    if len(itemBonus) < 1:
                        continue
                    itemId, _ = itemBonus[0]
                    bounsInfo = uiUtils.getGfxItemById(itemId)
                    bounsInfo['areaId'] = areaId
                    gainNum = gainBonusNumList[i]
                    bounsInfo['gainNum'] = gainNum
                    bounsInfo['condition'] = gameStrings.TEXT_FENGWUZHIPROXY_327 % gainNum
                    if info['curValue'] >= gainNum:
                        bounsInfo['state'] = 'finish'
                        if gainNum in fengwuzhiBonusFlag:
                            bounsInfo['btnLabel'] = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
                            bounsInfo['btnEnabled'] = False
                        else:
                            bounsInfo['btnLabel'] = gameStrings.TEXT_FENGWUZHIPROXY_334
                            bounsInfo['btnEnabled'] = True
                    else:
                        bounsInfo['state'] = 'going'
                        bounsInfo['btnLabel'] = gameStrings.TEXT_FENGWUZHIPROXY_334
                        bounsInfo['btnEnabled'] = False
                    bounsList.append(bounsInfo)

            info['bounsList'] = bounsList
            self.mediator.Invoke('refreshAwardInfo', uiUtils.dict2GfxDict(info, True))

    def onGetPandectInfo(self, *arg):
        self.curPanelIdx = IDX_PANDECT_PANEL
        self.refreshPandectInfo()

    def refreshPandectInfo(self):
        if self.curPanelIdx != IDX_PANDECT_PANEL:
            return
        if self.mediator:
            p = BigWorld.player()
            itemList = []
            for value in FGD.data.itervalues():
                itemInfo = {}
                itemInfo['groupName'] = value.get('name', '')
                itemInfo['sortIdx'] = value.get('sortIdx', 0)
                curNum = 0
                slotList = []
                itemIdList = value.get('itemIdList', ())
                if itemIdList:
                    for itemId in itemIdList:
                        fid = FID.data.get(itemId, {})
                        if not fid:
                            continue
                        slotInfo = {}
                        slotInfo['name'] = fid.get('name', '')
                        if self._isItemCompleted(itemId):
                            slotInfo['iconPath'] = 'fengwuzhi/110/color/%d.dds' % fid.get('icon', 0)
                            curNum += 1
                        else:
                            slotInfo['iconPath'] = 'fengwuzhi/110/gray/%d.dds' % fid.get('icon', 0)
                        slotInfo['rarity'] = 'rarity%d' % fid.get('rarity', 0)
                        slotList.append(slotInfo)

                itemInfo['slotList'] = slotList
                itemInfo['groupNum'] = '%d/%d' % (curNum, len(slotList))
                itemList.append(itemInfo)

            itemList.sort(key=lambda x: x['sortIdx'], reverse=True)
            self.mediator.Invoke('refreshPandectInfo', uiUtils.array2GfxAarry(itemList, True))

    def initBaseData(self):
        if self.clueToItem:
            return
        self.mapType = self.getMapType()
        for areaId, value in FAD.data.iteritems():
            if value.get('mapType', 0) != self.mapType:
                continue
            overviewIdList = value.get('overviewIdList')
            if not overviewIdList:
                continue
            for overviewId in overviewIdList:
                itemIdList = FAOD.data.get(overviewId, {}).get('itemIdList', ())
                if not itemIdList:
                    continue
                for itemId in itemIdList:
                    clueIdList = FID.data.get(itemId, {}).get('clueIdList', ())
                    if not clueIdList:
                        continue
                    self.itemToArea[itemId] = (areaId, overviewId)
                    for clueId in clueIdList:
                        self.clueToItem[clueId] = itemId

    def getCurAreaNum(self, areaId):
        curNum = 0
        overviewIdList = FAD.data.get(areaId, {}).get('overviewIdList')
        if overviewIdList:
            for overviewId in overviewIdList:
                itemIdList = FAOD.data.get(overviewId, {}).get('itemIdList', ())
                if not itemIdList:
                    continue
                for itemId in itemIdList:
                    if self._isItemCompleted(itemId):
                        curNum += 1

        return curNum

    def getMaxAreaNum(self, areaId):
        maxNum = 0
        overviewIdList = FAD.data.get(areaId, {}).get('overviewIdList')
        if overviewIdList:
            for overviewId in overviewIdList:
                itemIdList = FAOD.data.get(overviewId, {}).get('itemIdList', ())
                if not itemIdList:
                    continue
                maxNum += len(itemIdList)

        return maxNum

    def onGetBonus(self, *arg):
        areaId = int(arg[3][0].GetNumber())
        gainNum = int(arg[3][1].GetNumber())
        BigWorld.player().base.getFengwuzhiBonus(areaId, gainNum)

    def onGetMapType(self, *arg):
        self.mapType = self.getMapType()
        return GfxValue(self.mapType)

    @ui.scenarioCallFilter()
    def onClueInfoUpdate(self, newClues):
        if not newClues:
            return
        self.initBaseData()
        cid = newClues[-1]
        if QCD.data.get(cid, {}).get('clueType', 0) != uiConst.CLUE_TYPE_FENG_WU_ZHI:
            return
        itemId = self.clueToItem.get(cid, 0)
        if self._isItemCompleted(itemId):
            gameglobal.rds.ui.fengWuZhiItemPush.show(itemId)
            if self.curPanelIdx == IDX_AREA_PANEL:
                self.refreshAreaInfo()
            elif self.curPanelIdx == IDX_OVERVIEW_PANEL:
                self.refreshOverviewDetailInfo(self.curPanelArg)
            elif self.curPanelIdx == IDX_DETAIL_PANEL:
                self.refreshDetailInfo(itemId)
                self.refreshDetailResearchInfo(itemId)
            elif self.curPanelIdx == IDX_AWARD_PANEL:
                self.refreshAwardInfo(self.curPanelArg)
            elif self.curPanelIdx == IDX_PANDECT_PANEL:
                self.refreshPandectInfo()
        else:
            gameglobal.rds.ui.fengWuZhiCluePush.show(itemId)
            self.refreshDetailInfo(itemId)
            self.refreshDetailResearchInfo(itemId)

    def getMapType(self):
        if gameglobal.rds.configData.get('enableWingWorldFengWuZhi', False):
            p = BigWorld.player()
            if p.inWingCity():
                return MAP_TYPE_YISHIJIE
        return MAP_TYPE_YUNCHUI
