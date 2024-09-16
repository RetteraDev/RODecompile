#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cheerTopBarProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import events
import formula
import Avatar
from helpers import tickManager
from uiProxy import UIProxy
from asObject import TipManager
from gamestrings import gameStrings
from data import arena_mode_data as AMD
from guis.asObject import ASObject
from data import wing_world_config_data as WWCD
REFRESH_INTERVAL = 5

class CheerTopBarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CheerTopBarProxy, self).__init__(uiAdapter)
        self.widget = None
        self.tickId = 0
        self.count = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_CHEER_TOPBAR, self.hide)

    def reset(self):
        self.roundNo = 0
        self.matchNo = 0
        self.lastRefresh = True
        self.startTime = 0
        self.inPrepare = True
        self.inspireInfo = None
        self.myInspireGroupNUID = None
        self.cheerWait = False
        self.bloodColors = ['red', 'blue', 'blue']
        self.bloodColorMap = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_CHEER_TOPBAR:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def onGetServerData(self, roundNo, matchNo, inspireInfo, endTime, myInspireGroupNUID):
        self.roundNo = roundNo
        self.matchNo = matchNo
        self.inspireInfo = inspireInfo
        self.startTime = endTime
        if self.cheerWait and self.myInspireGroupNUID != myInspireGroupNUID:
            gameglobal.rds.sound.playSound(6188)
        self.myInspireGroupNUID = myInspireGroupNUID

    def clearWidget(self):
        self.widget = None
        if self.tickId:
            tickManager.stopTick(self.tickId)
            self.tickId = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_CHEER_TOPBAR)

    def show(self, roundNo, matchNo):
        self.roundNo = roundNo
        self.matchNo = matchNo
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_CHEER_TOPBAR)
        else:
            self.refreshInfo()

    def initUI(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = tickManager.addTick(1, self.refreshInfo)
        self.clearCheerInfo()
        self.widget.cheerBtn0.cheerBtn.addEventListener(events.BUTTON_CLICK, self.onCheer, False, 0, True)
        self.widget.cheerBtn1.cheerBtn.addEventListener(events.BUTTON_CLICK, self.onCheer, False, 0, True)
        TipManager.addTip(self.widget.personIcon, gameStrings.CHEER_TOP_BAR_PERSON_ICON_TIP)

    def clearCheerInfo(self):
        self.widget.teamName0.text = ''
        self.widget.teamName1.text = ''
        self.widget.cheerNum0.text = '0'
        self.widget.cheerNum1.text = '0'
        self.widget.progress.currentValue = 50
        self.widget.progress.maxValue = 100
        self.widget.personNum.text = 0
        self.widget.cheerBtn0.cheeredIcon.visible = False
        self.widget.cheerBtn1.cheeredIcon.visible = False

    def onCheer(self, *args):
        if not self.inspireInfo:
            self.queryServerData()
            return
        e = ASObject(args[3][0])
        groupNUID = long(e.currentTarget.data)
        self.cheerWait = True
        if groupNUID:
            teamName = self.inspireInfo[groupNUID][0]
            gameglobal.rds.ui.cheer.show(self.roundNo, self.matchNo, groupNUID, teamName)

    def refreshInfo(self):
        if not self.widget:
            return
        if not self.inspireInfo:
            self.queryServerData()
            return
        p = BigWorld.player()
        inspireInfo = self.inspireInfo
        nums = [10, 10]
        progress = 1.0
        if formula.spaceInWingWorldXinMoArena(formula.getAnnalSrcSceneNo(p.spaceNo)):
            self.showPlayerBlood()
        for index, groupNUID in enumerate(inspireInfo):
            self.widget.getChildByName('teamName%d' % index).text = inspireInfo[groupNUID][0]
            self.widget.getChildByName('cheerNum%d' % index).text = inspireInfo[groupNUID][1]
            self.widget.getChildByName('cheerBtn%d' % index).cheerBtn.data = groupNUID
            self.widget.getChildByName('cheerBtn%d' % index).cheeredIcon.visible = True if self.myInspireGroupNUID and self.myInspireGroupNUID == groupNUID else False
            nums[index] += int(inspireInfo[groupNUID][1])

        self.widget.progress.currentValue = 100.0 * nums[0] / (nums[0] + nums[1])
        self.widget.personNum.text = getattr(p, 'xinMoAnnalFakeCnt', 0)
        if self.inPrepare:
            timeLeft = self.startTime - utils.getNow()
            if timeLeft < 0:
                self.widget.cheerBtn0.visible = False
                self.widget.cheerBtn1.visible = False
                self.widget.timeCount.visible = False
                self.onArenaStart()
            else:
                if formula.spaceInWingWorldXinMoArena(formula.getAnnalSrcSceneNo(p.spaceNo)):
                    self.widget.cheerBtn0.visible = True
                    self.widget.cheerBtn1.visible = True
                elif formula.spaceInWingWorldXinMoArena(p.spaceNo):
                    self.widget.cheerBtn0.visible = False
                    self.widget.cheerBtn1.visible = False
                self.widget.timeCount.visible = True
                self.widget.timeCount.text = self.formateTime(timeLeft)
        else:
            timeLeft = self.getArenaLeftTime()
            if timeLeft < 0:
                self.widget.timeCount.visible = False
            else:
                self.widget.timeCount.visible = True
                self.widget.timeCount.text = self.formateTime(timeLeft)
        self.count += 1
        if self.count >= REFRESH_INTERVAL:
            self.count -= REFRESH_INTERVAL
            self.queryServerData()

    def onArenaStart(self):
        p = BigWorld.player()
        if not formula.spaceInWingWorldXinMoArena(p.spaceNo):
            return
        self.inPrepare = False

    def formateTime(self, time):
        minute = int(time / 60)
        sec = time - minute * 60
        return '%02d:%02d' % (minute, sec)

    def queryServerData(self):
        p = BigWorld.player()
        p.base.queryWingWorldXinMoInspire(self.roundNo, self.matchNo)

    def updateEnterXinMoData(self, roundNo, matchNo):
        self.roundNo = roundNo
        self.matchNo = matchNo

    def getArenaLeftTime(self):
        p = BigWorld.player()
        duration = AMD.data.get(p.getArenaMode(), {}).get('duration', 600)
        timePassing = duration - (p.getServerTime() - p.arenaReadyTime)
        return timePassing

    def showPlayerBlood(self):
        p = BigWorld.player()
        entities = BigWorld.entities.values()
        for index, groupNUID in enumerate(self.inspireInfo):
            if index >= len(self.bloodColors):
                break
            self.bloodColorMap[groupNUID] = self.bloodColors[index]

        for en in entities:
            if not isinstance(en, Avatar.Avatar) or en == p:
                continue
            if en.topLogo:
                if getattr(en, 'groupNUID', -1) in self.bloodColorMap.keys():
                    en.topLogo.xinmoColor = self.bloodColorMap[en.groupNUID]
                    en.topLogo.setBloodColor(en.topLogo.xinmoColor)
                    en.topLogo.showBlood(True)
                elif en.tempCamp == 1:
                    en.topLogo.xinmoColor = 'red'
                    en.topLogo.setBloodColor(en.topLogo.xinmoColor)
                    en.topLogo.showBlood(True)
                elif en.tempCamp == 2:
                    en.topLogo.xinmoColor = 'blue'
                    en.topLogo.setBloodColor(en.topLogo.xinmoColor)
                    en.topLogo.showBlood(True)
