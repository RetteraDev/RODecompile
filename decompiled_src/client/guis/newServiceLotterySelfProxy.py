#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServiceLotterySelfProxy.o
import BigWorld
import uiConst
import events
import time
import utils
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import lottery_data as LD
from data import new_server_activity_data as NSAD

class NewServiceLotterySelfProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServiceLotterySelfProxy, self).__init__(uiAdapter)
        self.widget = None
        self.allLotteryInfo = {}
        self.lotteryInfo = {}
        self.nsLotteryInfo = {}
        self.globalLotteryInfo = {}
        self.typeList = []
        self.isGotoFinal = False
        self.lotteryId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_NEW_SERVICE_LOTTERY_SELF, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_NEW_SERVICE_LOTTERY_SELF:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NEW_SERVICE_LOTTERY_SELF)

    def reset(self):
        self.typeList = []
        self.lotteryInfo = {}
        self.isGotoFinal = False
        self.lotteryId = 0

    def setLotteryId(self, id):
        self.lotteryId = id

    def show(self, isGotoFinal = False):
        self.isGotoFinal = isGotoFinal
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_NEW_SERVICE_LOTTERY_SELF)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.playerItemList.itemRenderer = 'NewServiceLotterySelf_playerItem'
        self.widget.playerItemList.barAlwaysVisible = True
        self.widget.playerItemList.dataArray = []
        self.widget.playerItemList.lableFunction = self.itemFunction
        self.widget.dropDown.addEventListener(events.INDEX_CHANGE, self.handleStageChange, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        nsLotteryId = NSAD.data.get('lotteryId', 0)
        globalLotteryId = NSAD.data.get('globalLotteryId', 0)
        if self.lotteryId == nsLotteryId:
            self.allLotteryInfo = self.nsLotteryInfo
        elif self.lotteryId == globalLotteryId:
            self.allLotteryInfo = self.globalLotteryInfo
        allLotteryKeys = self.allLotteryInfo.keys()
        allLotteryKeys.sort()
        finalNum = max(0, len(allLotteryKeys) - 1)
        finalKeyTime = allLotteryKeys[finalNum] if len(allLotteryKeys) > finalNum else 0
        finalLotteryInfo = self.allLotteryInfo.get(finalKeyTime, {})
        finalLotteryTime = finalLotteryInfo.get('lotteryTime', 0)
        if not self.lotteryInfo or self.lotteryInfo.get('lotteryId') != self.lotteryId:
            self.lotteryInfo = finalLotteryInfo
        lotteryId = self.lotteryInfo.get('lotteryId', 0)
        version = self.lotteryInfo.get('version', 0)
        lotteryTime = LD.data.get(lotteryId, {}).get('lotteryTime', '')
        lotteryInterval = LD.data.get(lotteryId, {}).get('lotteryInterval', 0)
        firstLotteryTime = utils.getTimeSecondFromStr(lotteryTime)
        sumDays = 0
        alteTime = firstLotteryTime
        while alteTime and finalLotteryTime and alteTime <= finalLotteryTime:
            alteTime += lotteryInterval
            sumDays += 1

        self.typeList = []
        for i in xrange(sumDays):
            stageTime = firstLotteryTime + lotteryInterval * i
            typeInfo = {}
            typeInfo['label'] = gameStrings.NEW_SERVICE_LOTTERY_SELF_STAGE_TIME % time.strftime('%Y/%m/%d', utils.localtimeEx(stageTime))
            typeInfo['stageTime'] = stageTime
            typeInfo['lotteryId'] = lotteryId
            typeInfo['version'] = version
            typeInfo['typeIndex'] = i
            self.typeList.append(typeInfo)

        ASUtils.setDropdownMenuData(self.widget.dropDown, self.typeList)
        self.widget.dropDown.menuRowCount = len(self.typeList)
        if self.widget.dropDown.selectedIndex == -1 or self.isGotoFinal:
            self.widget.dropDown.selectedIndex = len(self.typeList) - 1
            if self.typeList:
                itemInfo = self.typeList[len(self.typeList) - 1]
                curStageTime = itemInfo.get('stageTime', 0)
                self.lotteryInfo = self.allLotteryInfo.get(curStageTime, {})
        self.updateLotteryNumber()

    def handleStageChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        self.isGotoFinal = False
        p = BigWorld.player()
        itemInfo = self.typeList[itemMc.selectedIndex]
        lotteryId = itemInfo.get('lotteryId', 0)
        curStageTime = itemInfo.get('stageTime', 0)
        version = itemInfo.get('version', 0)
        p.base.queryNSLotterySelfData(lotteryId, curStageTime, version)
        self.lotteryInfo = self.allLotteryInfo.get(curStageTime, {})
        self.updateLotteryNumber()

    def updateLotteryNumber(self):
        now = utils.getNow()
        curStateLotteryTime = self.lotteryInfo.get('lotteryTime', 0)
        dataArr = []
        data = self.lotteryInfo.get('data', {})
        for i, nuid in enumerate(data):
            state = data.get(nuid, 0)
            if state == 0:
                if now > curStateLotteryTime:
                    stateStr = gameStrings.NEW_SERVICE_LOTTERY_SELF_NOT_WINNING
                else:
                    stateStr = gameStrings.NEW_SERVICE_LOTTERY_SELF_WAIT_PRIZE
            else:
                stateStr = gameStrings.NEW_SERVICE_LOTTERY_SELF_WINNING
            dataArr.append({'nuid': nuid,
             'stateStr': stateStr})

        self.widget.playerItemList.dataArray = dataArr
        self.widget.noneLotteryDesc.visible = not data

    def onGetNewServiceLotteryData(self, lotteryInfo):
        lotteryTime = lotteryInfo.get('lotteryTime', 0)
        lotteryId = lotteryInfo.get('lotteryId', 0)
        self.lotteryInfo = lotteryInfo
        nsLotteryId = NSAD.data.get('lotteryId', 0)
        globalLotteryId = NSAD.data.get('globalLotteryId', 0)
        if lotteryId == nsLotteryId:
            self.nsLotteryInfo[lotteryTime] = lotteryInfo
        elif lotteryId == globalLotteryId:
            self.globalLotteryInfo[lotteryTime] = lotteryInfo
        if self.widget:
            self.refreshInfo()
        else:
            self.show()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.nuidText.text = itemData.nuid
        itemMc.stateText.text = itemData.stateStr

    def getEndLotteryTimeVersion(self):
        if not self.allLotteryInfo:
            return 0
        allLotteryKeys = self.allLotteryInfo.keys()
        allLotteryKeys.sort()
        endNum = max(0, len(allLotteryKeys) - 1)
        endKeyTime = allLotteryKeys[endNum]
        lotteryInfo = self.allLotteryInfo.get(endKeyTime, {})
        version = lotteryInfo.get('version', 0)
        return version
