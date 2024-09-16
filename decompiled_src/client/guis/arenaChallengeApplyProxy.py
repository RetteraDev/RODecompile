#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaChallengeApplyProxy.o
import BigWorld
import const
import events
import uiConst
import utils
import gametypes
from helpers import taboo
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import uiUtils
from guis.asObject import TipManager
from guis.asObject import ASUtils
from guis.asObject import ASObject
from data import arena_mode_data as AMD
from data import duel_config_data as DCD
from data import sys_config_data as SCD
from cdata import font_config_data as FCD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
WORD_DEF_MAX_COUNT = 60
SLOT_ID_IDX = 0
SLOT_CNT_IDX = 1
COST_CASH_FORMODE = [ AMD.data.get(modeId, {}).get('needBindCash', 0) for modeId in const.ARENA_CHALLENDE_MODE_LIST ]
COST_SLOT_FORMODE = [ AMD.data.get(modeId, {}).get('needItems', 0) for modeId in const.ARENA_CHALLENDE_MODE_LIST ]
SLOT_XPOS = [59, 120, 180]
MAX_SLOT = 3
WND_OFFSET_INPUT = 80
WND_OFFSET_SLOT = 50

class ArenaChallengeApplyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaChallengeApplyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENACHALLENGE_APPLY, self.hide)

    def reset(self):
        self.needBroadcast = True

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ARENACHALLENGE_APPLY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENACHALLENGE_APPLY)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENACHALLENGE_APPLY)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.enabled = False
        self.initAboutText()
        self.initScrollList()
        self.slotMcs = [self.widget.slot0, self.widget.slot1, self.widget.slot2]
        self.updateCost()
        self.updateServerSelect(utils.getHostId(), utils.getServerName(utils.getHostId()))
        self.widget.broadcastCheckBox.selected = self.needBroadcast
        self.widget.enemyNameInputMc.addEventListener(events.EVENT_CHANGE, self.handleNameInputChange)
        self.widget.declartionInput.addEventListener(events.EVENT_CHANGE, self.handleDeclarationInputChange)
        self.widget.declartionInput.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleDeclartionInputStateChange)
        self.widget.selectModeScrollList.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleScrollListChange, False, 0, True)
        self.widget.broadcastCheckBox.addEventListener(events.EVENT_SELECT, self.handleCheckBoxSelected, False, 0, True)

    def initAboutText(self):
        self.declarationInputMax = WORD_DEF_MAX_COUNT
        self.widget.declartionInput.maxChars = self.declarationInputMax
        self.widget.declartionInput.defaultText = DCD.data.get('declartionDefaultText')
        self.widget.wordCountTextField.visible = False
        self.challengeMsg = self.widget.declartionInput.defaultText

    def initScrollList(self):
        ASUtils.setDropdownMenuData(self.widget.selectModeScrollList, gameStrings.ARENA_CHALLENGEMODE_LABELS)
        self.widget.selectModeScrollList.selectedIndex = 0
        self.widget.selectModeScrollList.validateNow()

    def handleScrollListChange(self, *args):
        self.updateCost()

    def updateCost(self):
        modeSelect = self.widget.selectModeScrollList.selectedIndex
        self.widget.cashCostTextField.text = COST_CASH_FORMODE[modeSelect]
        if not self.needBroadcast:
            for slot in self.slotMcs:
                slot.visible = False

        else:
            p = BigWorld.player()
            costSlots = COST_SLOT_FORMODE[modeSelect]
            hasSlotsCnt = [ p.inv.countItemInPages(costSlot[SLOT_ID_IDX]) for costSlot in costSlots ]
            slotKindCnt = len(costSlots)
            for idx in xrange(MAX_SLOT):
                if idx < slotKindCnt:
                    self.updateSlotInfo(self.slotMcs[idx], SLOT_XPOS[idx], costSlots[idx], hasSlotsCnt[idx])
                else:
                    self.slotMcs[idx].visible = False

    def updateSlotInfo(self, slotMc, xPos, costSlot, hasSlotCnt):
        slotId = costSlot[SLOT_ID_IDX]
        slotCnt = costSlot[SLOT_CNT_IDX]
        iconPath = uiUtils.getItemIconFile40(slotId)
        color = FCD.data.get(('item', ID.data.get(slotId, {}).get('quality', 1)), {}).get('color', '#CCCCCC')
        itemInfo = {'iconPath': iconPath,
         'color': color}
        slotMc.visible = True
        slotMc.x = xPos
        slotMc.slot.setItemSlotData(itemInfo)
        slotMc.slot.validateNow()
        slotMc.slot.dragable = False
        TipManager.addItemTipById(slotMc.slot, slotId)
        slotMc.slotCnt.htmlText = '%d/%d' % (hasSlotCnt, slotCnt)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onChangeServerBtnClick(self, e):
        self.uiAdapter.migrateServer.showServerList(uiConst.CHOOSE_SERVER_TYPE_ARENACHALLENGE, self.updateServerSelect)

    def updateServerSelect(self, serverId, serverName):
        if not self.widget:
            return
        self.widget.serverNameTextField.text = serverName
        self.serverHostId = serverId

    def _onConfirmBtnClick(self, e):
        p = BigWorld.player()
        needCash = COST_CASH_FORMODE[self.widget.selectModeScrollList.selectedIndex]
        p.payBindCashNotify(needCash, GMDD.data.ARENA_CHALLENGE_APPLY_CASH_NOT_ENOUGH, self.applyFunction)

    def applyFunction(self):
        hostId = self.serverHostId
        tgtRoleName = self.widget.enemyNameInputMc.text
        challengeMode = const.ARENA_CHALLENDE_MODE_LIST[self.widget.selectModeScrollList.selectedIndex]
        result, _ = taboo.checkNameDisWord(self.challengeMsg)
        if not result:
            self.uiAdapter.messageBox.showMsgBox(SCD.data.get('jieQiNicknameTabooWord'))
        else:
            BigWorld.player().cell.applyArenaChallenge(hostId, tgtRoleName, challengeMode, self.challengeMsg, self.needBroadcast)
            self.hide()

    def _onCancelBtnClick(self, e):
        self.hide()

    def handleNameInputChange(self, *args):
        self.widget.confirmBtn.enabled = self.isMatchCondition()

    def handleDeclarationInputChange(self, *args):
        self.widget.confirmBtn.enabled = self.isMatchCondition()
        e = ASObject(args[3][0])
        curWordCount = e.currentTarget.textField.length
        self.widget.wordCountTextField.htmlText = '%d/%d' % (curWordCount, self.declarationInputMax)

    def handleDeclartionInputStateChange(self, *args):
        if self.widget.declartionInput.defaultState == 'default' and self.widget.declartionInput.text == '':
            self.widget.wordCountTextField.visible = False
            self.challengeMsg = self.widget.declartionInput.defaultText
        else:
            self.widget.wordCountTextField.visible = True
            textLength = self.widget.declartionInput.textField.length
            self.widget.wordCountTextField.htmlText = '%d/%d' % (textLength, self.declarationInputMax)
            self.challengeMsg = self.widget.declartionInput.text

    def isMatchCondition(self):
        if self.widget.enemyNameInputMc.text == '':
            return False
        if not self.isSlotsEnough(self.widget.selectModeScrollList.selectedIndex):
            return False
        return True

    def isSlotsEnough(self, modeSelect):
        if not self.needBroadcast:
            return True
        p = BigWorld.player()
        costSlots = COST_SLOT_FORMODE[modeSelect]
        for costSlot in costSlots:
            costSlotCnt = costSlot[SLOT_CNT_IDX]
            hasSlotsCnt = p.inv.countItemInPages(costSlot[SLOT_ID_IDX], enableParentCheck=True)
            if costSlotCnt > hasSlotsCnt:
                return False

        return True

    def handleCheckBoxSelected(self, *args):
        e = ASObject(args[3][0])
        self.needBroadcast = e.currentTarget.selected
        self.widget.confirmBtn.enabled = self.isMatchCondition()
        self.relayout()

    def relayout(self):
        offset = WND_OFFSET_INPUT if self.needBroadcast else -WND_OFFSET_INPUT
        self.widget.broadcastCheckBox.y += offset
        self.widget.cashCostTextField.y += offset
        self.widget.costCashTitle.y += offset
        self.widget.costBonusMc.y += offset
        self.widget.declartionInputTitle.visible = self.needBroadcast
        self.widget.declartionInput.visible = self.needBroadcast
        self.widget.wordCountTextField.visible = self.needBroadcast and self.widget.declartionInput.text != ''
        offset = WND_OFFSET_SLOT + WND_OFFSET_INPUT if self.needBroadcast else -(WND_OFFSET_SLOT + WND_OFFSET_INPUT)
        self.widget.hit.height += offset
        self.widget.line2.y += offset
        self.widget.confirmBtn.y += offset
        self.widget.cancelBtn.y += offset
        self.updateCost()

    def checkApplyRequest(self):
        p = BigWorld.player()
        if p.arenaChallengeStatus != gametypes.CROSS_ARENA_CHALLENGE_STATUS_DEFAULT:
            p.showGameMsgEx(GMDD.data.APPLY_IN_CHALLENGE_NOTIFY, ())
        else:
            self.show()
