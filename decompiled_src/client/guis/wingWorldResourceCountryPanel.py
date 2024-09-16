#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldResourceCountryPanel.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import gamelog
import utils
import events
import time
import math
import gametypes
import wingWorldUtils
import formula
import const
from helpers import tickManager
from helpers import wingWorld
from helpers import navigator
from gameStrings import gameStrings
from asObject import TipManager
from asObject import ASObject
from guis import uiUtils
from asObject import ASUtils
from data import wing_world_config_data as WWCfD
from data import wing_city_resource_data as WCRD
from data import region_server_config_data as RSCD
from cdata import game_msg_def_data as GMDD
POINT_COUNT = 5
WHITE_FONT = "<font color=\'#FFFFFF\'>%s</font>"
RED_FONT = "<font color=\'#FF0000\'>%s</font>"
GREEN_FONT = "<font color=\'#74c424\'>%s</font>"
POINT_DROPDOWN_RES = 1
POINT_DROPDOWN_CITY = 2
POINT_DATA_INDEX_RESTYPE = 0
POINT_DATA_INDEX_RESNAME = 1
POINT_DATA_INDEX_CITYNAME = 2
POINT_DATA_INDEX_GUILDNAME = 3
POINT_DATA_INDEX_OCCUPYTIME = 4
POINT_DATA_INDEX_POINTNAME = 5
POINT_DATA_INDEX_STATE = 6
POINT_DATA_INDEX_ROLENAME = 7
POINT_DATA_INDEX_POINTID = 8

class WingWorldResourceCountryPanel(object):

    def __init__(self):
        super(WingWorldResourceCountryPanel, self).__init__()
        self.panel = None
        self.widget = None
        self.pointListData = []
        self.curPage = -1
        self.timerId = -1
        self.destroyed = False
        self.cityDropdownSelect = 0
        self.resDropdownSelect = 0
        self.cityDropdownData = []
        self.resDropdownData = []
        self.pointDisplayNum = 0
        self.requestTimerId = -1
        self.isInvalid = False
        self.displayPointData = []

    def initPanel(self, panel, widget):
        self.panel = panel
        self.widget = widget
        self.panel.addEventListener(events.EVENT_ENTER_FRAME, self.handleEnterFrame, False, 0, True)
        self.panel.pointSubPanel.page.minCount = 1
        self.panel.pointSubPanel.page.enableMouseWheel = False
        self.panel.pointSubPanel.page.addEventListener(events.EVENT_COUNT_CHANGE, self.handleChangePage, False, 0, True)
        self.panel.recordSubPanel.recordList.itemRenderer = 'WingWorldResourc_RecordItem'
        self.panel.recordSubPanel.recordList.labelFunction = self.recordLabelFunction
        self.panel.recordSubPanel.recordList.itemHeightFunction = self.recordItemHeightFunction
        self.panel.resName1.text = WWCfD.data.get('restype1', '')
        self.panel.resName2.text = WWCfD.data.get('restype2', '')
        self.panel.resName3.text = WWCfD.data.get('restype3', '')
        self.panel.rankBtn.addEventListener(events.BUTTON_CLICK, self.handleRankClick, False, 0, True)
        self.visibleCountryResource(False)
        resDropdownData = [gameStrings.WING_WORLD_RES_DROPDOWN_1]
        cityDropdownData = [gameStrings.WING_WORLD_RES_DROPDOWN_2]
        for i in xrange(0, gametypes.WING_RESOURCE_TYPE_COUNT):
            resDropdownData.append(WWCfD.data.get('restype%d' % (i + 1), ''))

        self.setDropdownInfo(POINT_DROPDOWN_RES, resDropdownData)
        self.setDropdownInfo(POINT_DROPDOWN_CITY, cityDropdownData)
        self.panel.pointSubPanel.dropDownMenu1.addEventListener(events.INDEX_CHANGE, self.handleDropdownChange, False, 0, True)
        self.panel.pointSubPanel.dropDownMenu2.addEventListener(events.INDEX_CHANGE, self.handleDropdownChange, False, 0, True)
        self.curPage = 0
        self.cityDropdownSelect = 0
        self.resDropdownSelect = 0
        self.pointListData = []
        self.isInvalid = True
        self.displayPointData = []
        if self.timerId != -1:
            tickManager.getInstance().stopTick(self.timerId)
        self.timerId = tickManager.getInstance().addTick(1, self.timerLeftTime, [])
        if self.requestTimerId != -1:
            tickManager.getInstance().stopTick(self.requestTimerId)
        self.requestTimerId = tickManager.getInstance().addTick(30, self.timerRequest, [])
        for i in xrange(0, POINT_COUNT):
            point = getattr(self.panel.pointSubPanel.points, 'point%d' % (i + 1))
            point.listBtn5.data = i
            point.listBtn5.addEventListener(events.MOUSE_CLICK, self.handleGotoPoint, False, 0, True)
            point.leftTime.visible = False
            point.leftTime.time.text = ''
            point.state.visible = False

        self.panel.yabiao.slot.dragable = False
        self.panel.yabiao.slot.setItemSlotData(uiUtils.getGfxItemById(WWCfD.data.get('yaBiaoIconId', 999)))
        self.panel.yabiao.funcBtn.addEventListener(events.BUTTON_CLICK, self.handleYaBiaoClick, False, 0, True)
        self.panel.yabiao.funcBtn.label = gameStrings.WING_WORLD_YABIAO
        self.panel.yabiao.txt0.visible = False
        self.panel.yabiao.funcBtn.linkText = WWCfD.data.get('yaBiaoLinkText', '')
        self.panel.ronglu.slot.dragable = False
        self.panel.ronglu.slot.setItemSlotData(uiUtils.getGfxItemById(WWCfD.data.get('rongluInterfaceDispalyItem', 999)))
        self.panel.ronglu.funcBtn.addEventListener(events.BUTTON_CLICK, self.handleRongluClick, False, 0, True)
        self.panel.ronglu.funcBtn.label = gameStrings.WING_WORLD_RONGLU_GOTO_BTN
        self.panel.ronglu.txt0.htmlText = gameStrings.WING_WORLD_RONGLU_TIME_LABLE % (0, 0)
        self.panel.ronglu.txtYaBiao.visible = False
        self.refreshInfo()

    def refreshInfo(self):
        if not self.panel or self.panel.visible == False:
            return
        self.refreshYaBiao()

    def refreshYaBiao(self):
        if not self.panel or not self.panel.visible:
            return
        p = BigWorld.player()
        self.panel.yabiao.funcBtn.enabled = False
        self.panel.yabiao.txtYaBiao.text = ''
        if not p.guild:
            self.panel.yabiao.funcBtn.enabled = False
            self.panel.yabiao.txtYaBiao.text = gameStrings.WING_WORLD_NO_GUILD
        elif hasattr(p, 'wingWorldYabiaoData') and p.wingWorldYabiaoData.isYabiaoRunning():
            self.panel.yabiao.funcBtn.enabled = False
            self.panel.yabiao.txtYaBiao.text = gameStrings.WING_WORLD_IN_YABIAO
        elif getattr(p, 'isWingWorldYabiaoDoneWeekly', False):
            self.panel.yabiao.funcBtn.enabled = False
            self.panel.yabiao.txtYaBiao.text = gameStrings.WING_WORLD_YABIAO_DONE
        else:
            self.panel.yabiao.funcBtn.enabled = True
            self.panel.yabiao.txtYaBiao.text = gameStrings.WING_WORLD_NOT_YABIAO

    def refreshRongluInfo(self):
        p = BigWorld.player()
        if not self.widget or not hasattr(p, 'wingWorldForgeData'):
            return
        weekTime = p.wingWorldForgeData.genTimesWeekly
        gameglobal.rds.ui.wingWorldResource.panelCache['rongluInfo'] = (weekTime,)
        self.updateRongluInfo(weekTime)

    def updateRongluInfo(self, weekTime):
        weekLimit = WWCfD.data.get('rongluResLimit', 10)
        self.panel.ronglu.txt0.htmlText = gameStrings.WING_WORLD_RONGLU_TIME_LABLE % (weekTime, weekLimit)

    def unRegisterPanel(self):
        self.destroyed = True
        if self.timerId != -1:
            tickManager.getInstance().stopTick(self.timerId)
            self.timerId = -1
        if self.requestTimerId != -1:
            tickManager.getInstance().stopTick(self.requestTimerId)
            self.requestTimerId = -1
        self.panel = None
        self.widget = None
        self.pointListData = []
        self.curPage = -1
        self.destroyed = False
        self.cityDropdownSelect = 0
        self.resDropdownSelect = 0
        self.cityDropdownData = []
        self.resDropdownData = []
        self.pointDisplayNum = 0
        self.isInvalid = False
        self.displayPointData = []

    def onShow(self):
        gamelog.debug('ypc@WingWorldResourceCountryPanel onshow')
        self.widget.timeDesc.text = WWCfD.data.get('wingWorldResCountryTimeDesc', '')
        p = BigWorld.player()
        p.cell.queryWingWorldResource(True)
        p.base.getWingWorldForgeData()
        p.cell.statsTriggerFromClient('loadWidgetTrigger', (uiConst.FAKE_WIDGET_ID_RESOURCE_COUNTRY,))
        cache = gameglobal.rds.ui.wingWorldResource.panelCache
        cacheResList = cache.get('resList', [0] * gametypes.WING_RESOURCE_TYPE_COUNT)
        cacheRecords = cache.get('records', [])
        cacheGuildInfo = cache.get('guildInfo', [0] * gametypes.WING_RESOURCE_TYPE_COUNT)
        cacheRongluInfo = cache.get('rongluInfo', (0, 0))
        self.updateResourceStateInfo(cacheResList)
        self.updateRecords(cacheRecords)
        self.updatePoints()
        self.updateGuildInfo(cacheGuildInfo)
        self.updateRongluInfo(cacheRongluInfo[0])

    def handleRankClick(self, *args):
        gamelog.debug('ypc@handleRankClick')
        p = BigWorld.player()
        if p._isSoul():
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.WING_WORLD_RESOURCE_CAN_NOT_OPEN_RANK)
            return
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_WING_RESOURCE_GUILD_SUBMIT)

    def handleChangePage(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        self.curPage = itemMc.count - 1
        self.isInvalid = True

    def handleYaBiaoClick(self, *args):
        gamelog.info('handleYaBiaoClick')
        p = BigWorld.player()
        p.applyYabiao()

    def handleRongluClick(self, *args):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WING_WORLD_RONGLU)

    def handleDropdownChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if e.currentTarget.name == 'dropDownMenu1':
            self.resDropdownSelect = itemMc.selectedIndex
            self.isInvalid = True
        elif e.currentTarget.name == 'dropDownMenu2':
            self.cityDropdownSelect = itemMc.selectedIndex
            self.isInvalid = True

    def handleEnterFrame(self, *args):
        if self.isInvalid:
            self.isInvalid = False
            self.refreshPoints()

    def handleGotoPoint(self, *args):
        e = ASObject(args[3][0])
        index = int(e.currentTarget.data)
        if not self.displayPointData or index not in range(len(self.displayPointData)):
            return
        else:
            p = BigWorld.player()
            if not p.inWingPeaceCity() and not p.inWingCityOrBornIsland():
                p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.WING_WORLD_PATH_NOT_IN_WING_CITY)
                return
            gamelog.debug('ypc@ handleGotoPoint cityData = ', self.displayPointData[index])
            pointId = self.displayPointData[index][POINT_DATA_INDEX_POINTID]
            targetPos = wingWorldUtils.getResourcePointPosition(pointId)
            cityId = WCRD.data.get(pointId, {}).get('cityId', -1)
            if targetPos == (0, 0, 0) or cityId == -1:
                gamelog.debug('ypc@ targetPos = ', targetPos)
                return
            isBornlandPoint = pointId in (1, 2, 3)
            if isBornlandPoint:
                if p.inWingPeaceCity() or p.inWingWarCity():
                    p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.WING_WORLD_PATH_CAN_NOT_GOTO_BORNLAND)
                    return
                if p.inWingBornIsland():
                    navigator.getNav().pathFinding(targetPos + (p.spaceNo,), None, None, True, 0.5)
                    return
            groupId = p.getWingWorldGroupId()
            cityType = const.WING_CITY_TYPE_PEACE
            gamelog.debug('ypc@ pointId, groupId, cityType', pointId, groupId, cityType)
            targetSpaceNo = formula.getWingCitySpaceNo(groupId, cityType, cityId)
            if targetSpaceNo == -1:
                return
            gamelog.debug('ypc@ targetPos, targetSpaceNo', targetPos, targetSpaceNo)
            if p.canPathFindingWingWorld(targetSpaceNo, True):
                try:
                    wingWorld.pathFinding(targetPos + (targetSpaceNo,), showMsg=True, failedCallback=self.onPathFindingFailed)
                except:
                    self.onPathFindingFailed()

            return

    def onPathFindingFailed(self):
        gamelog.debug('ypc@ onPathFindingFailed !!!')
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.WING_WORLD_PATH_FAILED)

    def setPointListData(self, pointListData):
        self.pointListData = pointListData
        self.isInvalid = True

    def refreshWorldInfo(self, resList, records):
        if not self.panel:
            return
        gameglobal.rds.ui.wingWorldResource.panelCache['resList'] = resList
        gameglobal.rds.ui.wingWorldResource.panelCache['records'] = records
        self.updateResourceStateInfo(resList)
        self.updateRecords(records)
        self.updatePoints()

    def updateResourceStateInfo(self, resList):
        p = BigWorld.player()
        if len(resList) != gametypes.WING_RESOURCE_TYPE_COUNT:
            return
        for i in xrange(0, gametypes.WING_RESOURCE_TYPE_COUNT):
            try:
                if not p.guildNUID:
                    guildResCount = 0
                    guildRate = 1.0
                else:
                    guildResCount = p.wingWorld.country.getOwn().resourcePointMap.getResourceCountByGuild(p.guildNUID, i)
                    guildRate = wingWorldUtils.getResCollectRatioGuild(guildResCount)
                countryResCount = p.wingWorld.country.getOwn().resourcePointMap.getResourceCount(i)
                countryRate = wingWorldUtils.getResCollectRatioCountry(countryResCount)
            except:
                guildResCount = 0
                guildRate = 1.0
                countryResCount = 0
                countryRate = 1.0

            strPointTxt = gameStrings.WING_WORLD_RES_OCCUPY_COUNT % countryResCount
            strPointTxt = WHITE_FONT % strPointTxt if countryResCount > 0 else RED_FONT % strPointTxt
            self.panel.getChildByName('pointTxt%d' % (i + 1)).htmlText = strPointTxt
            self.visibleCountryResource(False)
            effTxt = self.panel.getChildByName('effTxt%d' % (i + 1))
            effTxt.text = gameStrings.WING_WORLD_RES_COLLECT_RATE % (guildRate * countryRate)
            addtionGuildRate = max(guildRate - 1.0, 0.0) * 100.0
            addtionCountryRate = max(countryRate - 1.0, 0.0) * 100.0
            TipManager.removeTip(effTxt)
            TipManager.addTip(effTxt, gameStrings.WING_WORLD_RES_RATE_TIP % (addtionGuildRate, addtionCountryRate))

    def updateRecords(self, records):
        dataArray = []
        for record in records:
            sec = record[0]
            type = record[1]
            timeStr = time.strftime('%y.%m.%d', time.localtime(sec))
            content = ''
            if type == gametypes.WING_RESOURCE_RECORD_TYPE_OCCUPY_GUILD:
                name = record[3]
                cityName = wingWorldUtils.getResourcePointCityName(record[4])
                resStr = wingWorldUtils.getResourcePointResName(record[4])
                content = gameStrings.WING_WORLD_RES_RECORD_OCCUPY_GUILD % (GREEN_FONT % name, cityName, resStr)
            elif type == gametypes.WING_RESOURCE_RECORD_TYPE_OCCUPY_PLAYER:
                name = record[3]
                cityName = wingWorldUtils.getResourcePointCityName(record[4])
                resStr = wingWorldUtils.getResourcePointResName(record[4])
                serverName, playerName = self.getServerNameFromRoloName(name)
                content = gameStrings.WING_WORLD_RES_RECORD_OCCUPY % (GREEN_FONT % playerName, cityName, resStr)
            elif type == gametypes.WING_RESOURCE_RECORD_TYPE_LOSE:
                name = record[3]
                hostId = record[2]
                serverName = RSCD.data.get(hostId, {}).get('serverName', '')
                cityName = wingWorldUtils.getResourcePointCityName(record[4])
                resStr = wingWorldUtils.getResourcePointResName(record[4])
                if not name:
                    content = gameStrings.WING_WORLD_RES_RECORD_LOSE % (RED_FONT % serverName,
                     RED_FONT % name,
                     cityName,
                     resStr)
                else:
                    content = gameStrings.WING_WORLD_RES_RECORD_LOSE_GUILD % (RED_FONT % serverName,
                     RED_FONT % name,
                     cityName,
                     resStr)
            else:
                continue
            dataArray.append(timeStr + gameStrings.TEXT_HELPPROXY_512 + content)

        dataArray.reverse()
        self.panel.recordSubPanel.recordList.dataArray = dataArray

    def updatePoints(self):
        p = BigWorld.player()
        pointListData = []
        dropdownData = [gameStrings.WING_WORLD_RES_DROPDOWN_2]
        try:
            resPointMap = p.wingWorld.country.getOwn().resourcePointMap
        except:
            return

        for pointId, detail in resPointMap.items():
            resType = wingWorldUtils.getResourcePointType(pointId)
            resName = wingWorldUtils.getResourcePointResName(pointId)
            cityName = wingWorldUtils.getResourcePointCityName(pointId)
            occupyTime = detail.occupyTime
            pointName = wingWorldUtils.getResourcePointName(pointId)
            guildName = detail.guildName
            state = detail.state
            roleName = detail.roleName
            pointData = (resType,
             resName,
             cityName,
             guildName,
             occupyTime,
             pointName,
             state,
             roleName,
             pointId)
            pointListData.append(pointData)
            if cityName not in dropdownData:
                dropdownData.append(cityName)

        self.setDropdownInfo(POINT_DROPDOWN_CITY, dropdownData)
        self.setPointListData(pointListData)

    def setDropdownInfo(self, index, dropdownContents):
        dropdownMc = None
        if index == POINT_DROPDOWN_CITY:
            self.cityDropdownSelect = 0
            self.cityDropdownData = dropdownContents
            dropdownMc = self.panel.pointSubPanel.getChildByName('dropDownMenu%d' % POINT_DROPDOWN_CITY)
        elif index == POINT_DROPDOWN_RES:
            self.resDropdownSelect = 0
            self.resDropdownData = dropdownContents
            dropdownMc = self.panel.pointSubPanel.getChildByName('dropDownMenu%d' % POINT_DROPDOWN_RES)
        if dropdownMc:
            dropdownData = []
            for i in range(0, len(dropdownContents)):
                dropdownData.append({'label': dropdownContents[i],
                 'typeIndex': i})

            ASUtils.setDropdownMenuData(dropdownMc, dropdownData)
            dropdownMc.menuRowCount = len(dropdownContents)
            dropdownMc.selectedIndex = 0

    def refreshPoints(self):
        if not self.panel or not self.panel.getChildByName('pointSubPanel'):
            return
        curPointData = []
        if self.cityDropdownSelect != 0 or self.resDropdownSelect != 0 and self.cityDropdownSelect in range(0, len(self.cityDropdownData)) and self.resDropdownSelect in range(0, len(self.resDropdownData)):
            tmpData = []
            for pointData in self.pointListData:
                resName = pointData[POINT_DATA_INDEX_RESNAME]
                cityName = pointData[POINT_DATA_INDEX_CITYNAME]
                if self.cityDropdownSelect != 0 and cityName != self.cityDropdownData[self.cityDropdownSelect]:
                    continue
                if self.resDropdownSelect != 0 and resName != self.resDropdownData[self.resDropdownSelect]:
                    continue
                tmpData.append(pointData)

            curPointData = tmpData
        else:
            curPointData = self.pointListData
        if self.pointDisplayNum != len(curPointData):
            self.pointDisplayNum = len(curPointData)
            self.panel.pointSubPanel.page.maxCount = int(math.ceil(float(self.pointDisplayNum) / POINT_COUNT))
        start = self.curPage * POINT_COUNT
        end = start + POINT_COUNT - 1
        latest = len(curPointData) - 1
        if latest < start:
            curPointData = []
        elif latest < end:
            curPointData = curPointData[start:latest + 1]
        else:
            curPointData = curPointData[start:end + 1]
        self.displayPointData = curPointData
        for i in range(0, POINT_COUNT):
            point = getattr(self.panel.pointSubPanel.points, 'point%d' % (i + 1))
            if not point:
                continue
            if i > len(curPointData) - 1:
                point.visible = False
            else:
                point.visible = True
                point.icon.gotoAndStop('res%d' % curPointData[i][POINT_DATA_INDEX_RESTYPE])
                point.pointName.text = curPointData[i][POINT_DATA_INDEX_POINTNAME]
                point.resName.text = curPointData[i][POINT_DATA_INDEX_RESNAME]
                guildName = curPointData[i][POINT_DATA_INDEX_GUILDNAME]
                pointId = curPointData[i][POINT_DATA_INDEX_POINTID]
                point.guildName.text = gameStrings.WING_WORLD_RES_POINT_GUILD_OCCUPY % guildName if guildName else gameStrings.WING_WORLD_RES_POINT_GUILD_OCCUPY_NONE
                nowTime = utils.getNow()
                occupyTime = curPointData[i][POINT_DATA_INDEX_OCCUPYTIME]
                if nowTime >= occupyTime and nowTime < occupyTime + WWCfD.data.get('wingWorldPointProtectTime', 7200):
                    point.leftTime.visible = True
                    leftTime = int(occupyTime + WWCfD.data.get('wingWorldPointProtectTime', 7200) - nowTime)
                    point.leftTime.time.text = self.getFormatLeftTime(leftTime)
                    point.leftTime.data = leftTime
                else:
                    point.leftTime.visible = False
                    point.leftTime.data = 0
                if point.leftTime.visible:
                    point.state.visible = False
                else:
                    point.state.visible = curPointData[i][POINT_DATA_INDEX_STATE] == gametypes.WING_RESOURCE_POINT_STATE_FIGHTING
                    point.state.txt.htmlText = RED_FONT % gameStrings.WING_WORLD_RES_POINT_IN_WAR
                roleName = curPointData[i][POINT_DATA_INDEX_ROLENAME]
                if roleName:
                    TipManager.addTip(point.guildName, roleName)

    def refreshGuildInfo(self, resList):
        if not self.panel:
            return
        gameglobal.rds.ui.wingWorldResource.panelCache['guildInfo'] = resList
        self.updateGuildInfo(resList)

    def updateGuildInfo(self, resList):
        if len(resList) != gametypes.WING_RESOURCE_TYPE_COUNT:
            return
        p = BigWorld.player()
        if not p.guild:
            resList = [0, 0, 0]
        for type in range(0, gametypes.WING_RESOURCE_TYPE_COUNT):
            txtName = 'gresTxt%s' % (gametypes.WING_RESOURCE_TYPE_OBSIDIAN + type + 1)
            txtMc = self.panel.getChildByName(txtName)
            if txtMc:
                txtMc.text = ASUtils.convertMoneyStr(resList[type])

    def recordLabelFunction(self, *args):
        data = args[3][0]
        itemMc = ASObject(args[3][1])
        itemMc.recordTxt.htmlText = data
        itemMc.recordTxt.wordWrap = True
        itemMc.recordTxt.height = itemMc.recordTxt.textHeight + 10

    def recordItemHeightFunction(self, *args):
        if not self.widget:
            return GfxValue(20)
        text = args[3][0]
        tmpText = self.widget.getInstByClsName('WingWorldResourc_RecordItem')
        tmpText.recordTxt.htmlText = text
        tmpText.recordTxt.wordWrap = True
        return GfxValue(tmpText.recordTxt.textHeight + 5)

    def timerLeftTime(self, *args):
        if self.destroyed:
            return
        for i in range(0, POINT_COUNT):
            point = getattr(self.panel.pointSubPanel.points, 'point%d' % (i + 1))
            if point:
                if point.leftTime.data > 0:
                    point.leftTime.visible = True
                    point.leftTime.time.text = self.getFormatLeftTime(int(point.leftTime.data))
                    point.leftTime.data -= 1
                else:
                    point.leftTime.visible = False
                    point.leftTime.time.text = ''
                    point.leftTime.data = 0

    def timerRequest(self, *args):
        p = BigWorld.player()
        p.cell.queryWingWorldResource(False)

    def visibleCountryResource(self, visible):
        if not self.panel:
            return
        self.panel.countryResTitle.visible = visible
        for i in xrange(3):
            self.panel.getChildByName('wresTxt%d' % (i + 1)).visible = visible

    def getFormatLeftTime(self, seconds):
        leftTime = seconds
        hours = int(leftTime / 3600)
        leftTime = leftTime % 3600
        minutes = int(leftTime / 60)
        leftTime = leftTime % 60
        seconds = int(leftTime)
        s = ''
        s += '%02d:' % hours
        s += '%02d:' % minutes
        s += '%02d' % seconds
        return s

    def getServerNameFromRoloName(self, roleName):
        namelist = roleName.split('-')
        if len(namelist) > 1:
            serverName = namelist[-1]
            for sdata in RSCD.data.values():
                if serverName == sdata.get('serverName', ''):
                    return (serverName, '-'.join(namelist[0:-1]))

        return ('', roleName)
