#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldWarLvChooseProxy.o
import BigWorld
import gameglobal
import gametypes
import const
from guis import events
from guis import uiConst
from guis.asObject import ASObject
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASUtils
from guis.asObject import TipManager
from gameStrings import gameStrings
from data import world_war_config_data as WWCD
from cdata import game_msg_def_data as GMDD

class WorldWarLvChooseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WorldWarLvChooseProxy, self).__init__(uiAdapter)
        self.widget = None
        self.wwType = -1
        self.selectedWWType = -1
        self.wwName = ''
        self.wwNameOld = ''
        self.wwNameYoung = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_WORLD_WAR_LV_CHOOSE, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        p = BigWorld.player()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.cancelBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCancel)
        ASUtils.setHitTestDisable(self.widget.titlePic, True)
        ASUtils.setHitTestDisable(self.widget.title, True)
        wwState = WWCD.data.get('wwState', ())
        if self.wwType == gametypes.WORLD_WAR_TYPE_BATTLE:
            wwStateOld = ''
            wwStateYoung = ''
            battleStateOld = p.worldWar.battleStateDict[gametypes.WORLD_WAR_TYPE_BATTLE]
            battleStateYoung = p.worldWar.battleStateDict[gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG]
            if battleStateOld == gametypes.WORLD_WAR_BATTLE_STATE_APPLY:
                wwStateOld = wwState[0]
            elif battleStateOld == gametypes.WORLD_WAR_BATTLE_STATE_OPEN:
                wwStateOld = wwState[1]
            elif battleStateOld == gametypes.WORLD_WAR_BATTLE_STATE_CLOSE:
                wwStateOld = wwState[2]
            if battleStateYoung == gametypes.WORLD_WAR_BATTLE_STATE_APPLY:
                wwStateYoung = wwState[0]
            elif battleStateYoung == gametypes.WORLD_WAR_BATTLE_STATE_OPEN:
                wwStateYoung = wwState[1]
            elif battleStateYoung == gametypes.WORLD_WAR_BATTLE_STATE_CLOSE:
                wwStateYoung = wwState[2]
            self.wwName = WWCD.data.get('wwBattleName', '')
            self.wwNameOld = self.wwName % wwStateOld
            self.wwNameYoung = self.wwName % wwStateYoung
            self.widget.oldTeam.wwName.text = self.wwNameOld
            self.widget.youngTeam.wwName.text = self.wwNameYoung
            self.widget.oldTeam.data = gametypes.WORLD_WAR_TYPE_BATTLE
            self.widget.youngTeam.data = gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG
        elif self.wwType == gametypes.WORLD_WAR_TYPE_ROB:
            wwStateOld = ''
            wwStateYoung = ''
            robStateOld = p.worldWar.robStateDict[gametypes.WORLD_WAR_TYPE_ROB]
            robStateYoung = p.worldWar.robStateDict[gametypes.WORLD_WAR_TYPE_ROB_YOUNG]
            if robStateOld in gametypes.WW_ROB_STATE_APPLY_STATES:
                wwStateOld = wwState[0]
            elif robStateOld not in gametypes.WW_ROB_STATE_NOT_OPEN:
                wwStateOld = wwState[1]
            else:
                wwStateOld = wwState[2]
            if robStateYoung in gametypes.WW_ROB_STATE_APPLY_STATES:
                wwStateYoung = wwState[0]
            elif robStateYoung not in gametypes.WW_ROB_STATE_NOT_OPEN:
                wwStateYoung = wwState[1]
            else:
                wwStateYoung = wwState[2]
            self.wwName = WWCD.data.get('wwRobName', '')
            self.wwNameOld = self.wwName % wwStateOld
            self.wwNameYoung = self.wwName % wwStateYoung
            self.widget.oldTeam.wwName.text = self.wwNameOld
            self.widget.youngTeam.wwName.text = self.wwNameYoung
            self.widget.oldTeam.data = gametypes.WORLD_WAR_TYPE_ROB
            self.widget.youngTeam.data = gametypes.WORLD_WAR_TYPE_ROB_YOUNG
        self.widget.oldTeam.label = WWCD.data.get('wwOldLvTxt', '')
        self.widget.youngTeam.label = WWCD.data.get('wwYoungLvTxt', '')
        self.widget.oldTeam.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleDealWithName)
        self.widget.youngTeam.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleDealWithName)
        self.widget.oldTeam.addEventListener(events.MOUSE_CLICK, self.handleClickTeam)
        self.widget.youngTeam.addEventListener(events.MOUSE_CLICK, self.handleClickTeam)
        self.widget.notShow.addEventListener(events.MOUSE_CLICK, self.handleClickNotShow)
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirm)
        oldTeamTip = WWCD.data.get('worldWarChooseTips', [])[gametypes.WW_ARMY_GROUP_TYPE_QINGLONG]
        youngTeamTip = WWCD.data.get('worldWarChooseTips', [])[gametypes.WW_ARMY_GROUP_TYPE_BAIHU]
        if self.wwType == gametypes.WORLD_WAR_TYPE_ROB:
            oldTeamTip = oldTeamTip % gameStrings.WW_ROB_NAME
            youngTeamTip = youngTeamTip % gameStrings.WW_ROB_NAME
        else:
            oldTeamTip = oldTeamTip % gameStrings.WW_BATTLE_NAME
            youngTeamTip = youngTeamTip % gameStrings.WW_BATTLE_NAME
        TipManager.addTip(self.widget.oldTeam, oldTeamTip)
        TipManager.addTip(self.widget.youngTeam, youngTeamTip)
        if p.lv > const.WORLD_WAR_ARMY_MINLV and not p.checkRobStartPrivilege(gametypes.WORLD_WAR_TYPE_ROB_YOUNG):
            self.widget.notShow.visible = True
            self.selectTeam(True)
            self.widget.youngTeam.enabled = False
        else:
            self.widget.notShow.visible = False
            self.selectTeam(False)

    def selectTeam(self, isOldTeam):
        if self.widget:
            if isOldTeam:
                self.widget.oldTeam.selected = True
                self.widget.youngTeam.selected = False
                self.selectedWWType = int(self.widget.oldTeam.data)
            else:
                self.widget.oldTeam.selected = False
                self.widget.youngTeam.selected = True
                self.selectedWWType = int(self.widget.youngTeam.data)

    def handleClickCancel(self, *args):
        self.clearWidget()

    def handleClickTeam(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.name == 'oldTeam':
            self.selectTeam(True)
        else:
            self.selectTeam(False)

    def handleClickNotShow(self, *args):
        pass

    def handleClickConfirm(self, *args):
        p = BigWorld.player()
        if self.widget.notShow.visible:
            p.base.saveWWQLBHSelection(self.wwType, self.widget.notShow.selected)
            self.chooseWWmode()
        else:
            if self.wwType == gametypes.WORLD_WAR_TYPE_ROB:
                if p.worldWar.robStateDict[self.selectedWWType] in gametypes.WW_ROB_STATE_APPLY_STATES:
                    self.chooseWWmode()
                    return
            elif self.wwType == gametypes.WORLD_WAR_TYPE_BATTLE:
                if p.worldWar.battleStateDict[self.selectedWWType] == gametypes.WORLD_WAR_BATTLE_STATE_APPLY:
                    self.chooseWWmode()
                    return
            msg = uiUtils.getTextFromGMD(GMDD.data.WW_MODE_CHOOSE_CONFIRM)
            groupOld = gametypes.QINGLONG_GROUP
            groupYoung = gametypes.BAIHU_GROUP
            groupName = gametypes.WORLD_WAR_TYPE_GROUP_TXT[self.selectedWWType]
            if groupName == groupOld:
                otherGroupName = groupYoung
            else:
                otherGroupName = groupOld
            wwName = ''
            if self.wwType == gametypes.WORLD_WAR_TYPE_BATTLE:
                wwName = WWCD.data.get('wwBattleName', '') % ''
            else:
                wwName = WWCD.data.get('wwRobName', '') % ''
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg % (groupName,
             wwName,
             groupName,
             wwName,
             otherGroupName,
             wwName), self.chooseWWmode)

    def chooseWWmode(self):
        p = BigWorld.player()
        p.cell.enterWorldWarEvent(self.selectedWWType)
        gameglobal.rds.ui.worldWar.hide()
        self.clearWidget()

    def handleDealWithName(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.name == 'youngTeam':
            target.wwName.text = self.wwNameYoung
        else:
            target.wwName.text = self.wwNameOld

    def show(self, wwType):
        self.wwType = wwType
        if not self.widget:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WORLD_WAR_LV_CHOOSE)

    def clearWidget(self):
        self.wwType = -1
        self.widget = None
        self.selectedWWType = -1
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WORLD_WAR_LV_CHOOSE)
