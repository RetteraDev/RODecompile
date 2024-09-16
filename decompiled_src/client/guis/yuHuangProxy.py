#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yuHuangProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import utils
import const
from helpers import tickManager
from helpers import wingWorld
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from data import wing_world_config_data as WWCD

class YuHuangProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YuHuangProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.tickId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_YUHUANG, self.hide)

    def reset(self):
        self.activityState = -1
        self.endTime = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_YUHUANG:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            gameglobal.rds.sound.playSound(gameglobal.SD_4)

    def clearWidget(self):
        self.widget = None
        if self.tickId:
            tickManager.stopTick(self.tickId)
            self.tickId = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_YUHUANG)

    def show(self, activityState = -1, endTime = 0):
        self.activityState = activityState
        self.endTime = endTime
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_YUHUANG)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = tickManager.addTick(1, self.refreshInfo)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirmBtnClick, False, 0, True)
        self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick, False, 0, True)

    def onRankBtnClick(self, *args):
        e = ASObject(args[3][0])
        btn = e.currentTarget
        if btn.label == gameStrings.WING_WORLD_XINMO_NORMAL_BTN0_LABEL:
            gameglobal.rds.ui.teamRankingList.show()
        elif btn.label == gameStrings.WING_WORLD_XINMO_PREPARE_BTN0_LABEL:
            p = BigWorld.player()
            p.cell.applyWingWorldXinMoArenaML()
            self.hide()

    def onConfirmBtnClick(self, *args):
        e = ASObject(args[3][0])
        btn = e.currentTarget
        if btn.label == gameStrings.WING_WORLD_XINMO_NORMAL_BTN1_LABEL:
            self.gotoXinmoEntry()
        elif btn.label == gameStrings.WING_WORLD_XINMO_PREPARE_BTN1_LABEL:
            self.hide()

    def gotoXinmoEntry(self):
        r = wingWorld.getNearestXinmoEntryPos(2)
        if r:
            pos, spaceNo = r
            p = BigWorld.player()
            if p.canPathFindingWingWorld(spaceNo, includeSameSpace=True):
                wingWorld.pathFinding(pos + (spaceNo,))

    def refreshInfo(self):
        if not self.widget:
            return
        if self.activityState == const.WING_WORLD_XINMO_STATE_NORMAL_BOSS:
            self.widget.titleName.textField.text = gameStrings.WING_WORLD_XINMO_NORMAL_TITLE
            leftTime = self.endTime - utils.getNow()
            if leftTime < 0:
                return
            self.widget.restTime.text = self.formateTime(leftTime)
            self.widget.confirmInfo.text = WWCD.data.get('xinmoNormalBossTip', '')
            self.widget.rankBtn.label = gameStrings.WING_WORLD_XINMO_NORMAL_BTN0_LABEL
            self.widget.confirmBtn.label = gameStrings.WING_WORLD_XINMO_NORMAL_BTN1_LABEL
            self.widget.helpIcon.visible = True
            self.widget.helpIcon.helpKey = WWCD.data.get('xinmoNormalBossHelpId', 0)
        elif self.activityState == const.WING_WORLD_XINMO_STATE_CLIENT_PREPARE or self.activityState == const.WING_WORLD_XINMO_STATE_ENTER_ML:
            self.widget.titleName.textField.text = gameStrings.WING_WORLD_XINMO_PREPARE_TITLE
            leftTime = max(0, self.endTime - utils.getNow())
            self.widget.restTime.text = self.formateTime(leftTime)
            self.widget.confirmInfo.text = WWCD.data.get('xinmoPrepareDesc', '')
            self.widget.rankBtn.label = gameStrings.WING_WORLD_XINMO_PREPARE_BTN0_LABEL
            self.widget.confirmBtn.label = gameStrings.WING_WORLD_XINMO_PREPARE_BTN1_LABEL
            self.widget.helpIcon.visible = True
            self.widget.helpIcon.helpKey = WWCD.data.get('xinmoPrepareHelpId', 0)
        elif self.activityState == const.WING_WORLD_XINMO_STATE_PRE_END:
            self.widget.titleName.textField.text = gameStrings.WING_WORLD_XINMO_PRE_END_TITLE
            leftTime = max(0, self.endTime - utils.getNow())
            self.widget.restTime.text = self.formateTime(leftTime)
            self.widget.confirmInfo.text = WWCD.data.get('xinmoPreEndDesc', '')
            self.widget.rankBtn.label = gameStrings.WING_WORLD_XINMO_NORMAL_BTN0_LABEL
            self.widget.confirmBtn.label = gameStrings.WING_WORLD_XINMO_PREPARE_BTN1_LABEL
            self.widget.helpIcon.visible = False

    def formateTime(self, time):
        minute = int(time / 60)
        sec = time - minute * 60
        return gameStrings.WING_WORLD_XIMO_YUHUANG_REST_TIME % (minute, sec)
