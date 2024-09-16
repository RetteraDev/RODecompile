#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/realNameCheckProxy.o
import BigWorld
import gameglobal
import uiConst
import ui
import const
import events
import utils
import gametypes
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from cdata import font_config_data as FCD
SLOT_XPOS_LIST = [[],
 [216],
 [158, 262],
 [112, 216, 320]]
MAX_SLOT = 3
SLOT_ID_IDX = 0
SLOT_CNT_IDX = 1

class RealNameCheckProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RealNameCheckProxy, self).__init__(uiAdapter)
        self.addEvent(events.EVENT_TYPE_SCENARIO_END, self.checkRealName, isGlobal=True)
        self.widget = None
        self.lastPushedName = None
        self.reset()

    def reset(self):
        pass

    def clearAll(self):
        self.lastPushedName = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_REALNAME_CHECK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.uiAdapter.restoreUI()
        self.widget = None
        self.releaseControl()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_REALNAME_CHECK)

    def show(self):
        p = BigWorld.player()
        if not self.widget and self.lastPushedName != p.roleName:
            self.lastPushedName = p.roleName
            self.uiAdapter.hideAllUI()
            self.uiAdapter.loadWidget(uiConst.WIDGET_REALNAME_CHECK)
            self.lockControl()

    def lockControl(self):
        p = BigWorld.player()
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI, False)

    def releaseControl(self):
        p = BigWorld.player()
        p.unlockKey(gameglobal.KEY_POS_UI)

    def initUI(self):
        self.widget.rewardHintTf.htmlText = SCD.data.get('realNameHintRewardText')
        self.widget.closeHintTf.htmlText = SCD.data.get('realNameHintCloseText')
        self.slotMcs = [self.widget.slot0, self.widget.slot1, self.widget.slot2]
        self.updateSlot()

    def updateSlot(self):
        rewardSlot = SCD.data.get('realNameHintRewardSlot', ((999, 1), (994, 2)))
        slotKindCnt = len(rewardSlot)
        slotMcsXPos = SLOT_XPOS_LIST[slotKindCnt]
        for idx in xrange(MAX_SLOT):
            if idx < slotKindCnt:
                self.updateSlotInfo(self.slotMcs[idx], slotMcsXPos[idx], rewardSlot[idx])
            else:
                self.slotMcs[idx].visible = False

    def updateSlotInfo(self, slotMc, xPos, costSlot):
        slotId = costSlot[SLOT_ID_IDX]
        count = costSlot[SLOT_CNT_IDX]
        itemInfo = uiUtils.getGfxItemById(slotId, count)
        slotMc.visible = True
        slotMc.x = xPos
        slotMc.slot.setItemSlotData(itemInfo)
        slotMc.slot.dragable = False

    def refreshInfo(self):
        if not self.widget:
            return

    @ui.callFilter(2)
    def _onConfirmBtnClick(self, e):
        self.gotoCommitRealName()

    @ui.callFilter(5)
    def _onCloseBtnClick(self, e):
        BigWorld.player().base.updateIndulgeStage()
        if gameglobal.rds.configData.get('enableForceCloseRealNameWnd', False):
            self.hide()
        else:
            self.closeBtnClick()

    @ui.callAfterTime()
    def closeBtnClick(self):
        p = BigWorld.player()
        if p.indulgeState in const.INDULGE_PERMIT_STATES:
            p.base.applyRealNameReward()
            self.hide()
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.REAL_NAME_CHECK_FAILED)
            self.uiAdapter.messageBox.showMsgBox(msg, callback=self.gotoCommitRealName)

    def gotoCommitRealName(self):
        BigWorld.openUrl(SCD.data.get('realNameWebLink', ''))

    def checkRealName(self):
        if not self.checkPlayerIndulgeState():
            self.show()

    def checkPlayerIndulgeState(self):
        if gameglobal.rds.configData.get('enableAntiIndulgenceLoginClient', False):
            if BigWorld.player().indulgeState not in const.INDULGE_PERMIT_STATES:
                return False
        return True

    def isPlayerThirdParty(self):
        p = BigWorld.player()
        return utils.getAccountType(p.roleURS) != gametypes.ACCOUNT_TYPE_URS
