#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fightForLoveLinesProxy.o
import BigWorld
import events
import gametypes
import utils
from asObject import ASObject
from asObject import ASUtils
from gamestrings import gameStrings
import gamelog
import uiConst
from asObject import MenuManager
from uiProxy import UIProxy
from callbackHelper import Functor
from data import fight_for_love_config_data as FFLCD

class FightForLoveLinesProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FightForLoveLinesProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FIGHT_FOR_LOVE_LINES, self.hide)

    def reset(self):
        self.fflInfo = {}
        self.curSelectedActId = None
        self.curSelectedItem = None
        self.hotStageIdList = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FIGHT_FOR_LOVE_LINES:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FIGHT_FOR_LOVE_LINES)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FIGHT_FOR_LOVE_LINES)

    def initUI(self):
        p = BigWorld.player()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.lineView.itemRenderer = 'FightForLoveLines_StageItem'
        self.widget.lineView.labelFunction = self.stageListFunction
        self.widget.lineView.dataArray = []
        self.widget.lineView.validateNow()
        self.widget.playerList.itemRenderer = 'FightForLoveLines_PlayerItem'
        self.widget.playerList.labelFunction = self.playerListFunction
        self.widget.playerList.dataArray = []
        self.widget.playerList.validateNow()
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshBtnClick, False, 0, True)
        p.cell.queryFightForLoveTotalInfo()
        self.refreshInfo()

    def stageListFunction(self, *arg):
        itemData = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and itemData:
            itemMc.activityNUID = itemData.activityNUID
            if long(itemData.activityNUID) in self.hotStageIdList:
                itemMc.hot.visible = True
            else:
                itemMc.hot.visible = False
            itemMc.participator = itemData.participator
            itemMc.phase = itemData.phase
            itemMc.item.available.visible = True
            if itemData.phase == gametypes.FIGHT_FOR_LOVE_PHASE_RUNNING:
                itemMc.item.available.text = gameStrings.FIGHT_FOR_LOVE_OBSERVE_AVAILABLE
            elif itemData.phase == gametypes.FIGHT_FOR_LOVE_PHASE_PREPARE:
                itemMc.item.available.text = gameStrings.FIGHT_FOR_LOVE_APPLY_AVAILABLE
            else:
                itemMc.item.available.visible = False
            itemMc.tOccupy = itemData.tOccupy
            itemMc.createrName = itemData.createrName
            ASUtils.setHitTestDisable(itemMc.hot, True)
            ASUtils.setHitTestDisable(itemMc.item.schoolIcon, True)
            ASUtils.setHitTestDisable(itemMc.item.playerName, True)
            ASUtils.setHitTestDisable(itemMc.item.available, True)
            itemMc.item.chooseBtn.addEventListener(events.BUTTON_CLICK, self.handleLineBtnClick, False, 0, True)
            itemMc.item.chooseBtn.selected = False
            if itemData.activityNUID == self.curSelectedActId:
                itemMc.item.chooseBtn.selected = True
            itemMc.item.playerName.text = gameStrings.FIGHT_FOR_LOVE_STAGE_NAME % itemData.createrName
            itemMc.item.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC[itemData.createrSchool])

    def playerListFunction(self, *arg):
        itemData = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and itemData:
            itemMc.gbId = itemData.gbId
            itemMc.playerName.text = itemData.name
            itemMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC[itemData.school])
            menuParam = {'roleName': itemData.name,
             'gbId': itemData.gbId}
            MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_CHAT, menuParam)

    def refreshInfo(self):
        if not self.hasBasedata():
            return False
        self.refreshSelectedState()

    def refreshListData(self, fflInfo):
        if not self.hasBasedata():
            return
        else:
            self.fflInfo = fflInfo
            fflRoomList = []
            activityNUIDList = []
            maxPlayerNum = 0
            for i in xrange(len(fflInfo)):
                fflitem = fflInfo[i]
                roomInfo = {}
                roomInfo['activityNUID'] = fflitem[0]
                roomInfo['createrGbId'] = fflitem[1]
                roomInfo['createrName'] = fflitem[2]
                roomInfo['createrSchool'] = fflitem[3]
                roomInfo['phase'] = fflitem[4]
                roomInfo['tOccupy'] = fflitem[5]
                roomInfo['participator'] = fflitem[6]
                roomInfo['participatorNum'] = len(fflitem[6])
                playerNum = len(fflitem[6])
                if playerNum >= maxPlayerNum:
                    maxPlayerNum = playerNum
                fflRoomList.append(roomInfo)
                activityNUIDList.append(fflitem[0])

            for i in xrange(len(fflInfo)):
                fflitem = fflInfo[i]
                if len(fflitem[6]) == maxPlayerNum:
                    self.hotStageIdList.append(fflitem[0])

            fflRoomList = sorted(fflRoomList, cmp=self.sortRoom, reverse=True)
            self.widget.lineView.dataArray = fflRoomList
            self.widget.lineView.validateNow()
            if fflInfo:
                if not self.curSelectedActId or self.curSelectedActId not in activityNUIDList:
                    self.curSelectedActId = fflInfo[0][0]
                self.setSelectItem(self.curSelectedActId)
                self.refreshPlayerList()
            else:
                self.curSelectedActId = None
                self.curSelectedItem = None
                self.refreshPlayerList()
            return

    def sortRoom(self, a, b):
        if self.hotStageIdList:
            if a['activityNUID'] in self.hotStageIdList and b['activityNUID'] in self.hotStageIdList:
                return a['tOccupy'] > b['tOccupy']
            elif a['activityNUID'] in self.hotStageIdList:
                return 1
            elif b['activityNUID'] in self.hotStageIdList:
                return -1
            else:
                return a['tOccupy'] > b['tOccupy']

    def refreshSelectedState(self):
        if not self.hasBasedata():
            return
        self.widget.confirmBtn.visible = False
        if self.curSelectedActId and self.curSelectedItem:
            phase = self.curSelectedItem.phase
            self.widget.confirmBtn.visible = True
            if phase == gametypes.FIGHT_FOR_LOVE_PHASE_RUNNING:
                self.widget.confirmBtn.label = gameStrings.FIGHT_FOR_LOVE_OBSERVE
            elif phase == gametypes.FIGHT_FOR_LOVE_PHASE_PREPARE:
                self.widget.confirmBtn.label = gameStrings.FIGHT_FOR_LOVE_APPLY
            else:
                self.widget.confirmBtn.visible = False

    def handleLineBtnClick(self, *arg):
        if not self.hasBasedata():
            return False
        e = ASObject(arg[3][0])
        target = e.target
        activityNUID = long(target.parent.parent.activityNUID)
        self.setSelectItem(activityNUID)
        self.refreshPlayerList()

    def setSelectItem(self, activityNUID):
        if not self.hasBasedata():
            return False
        else:
            newId = activityNUID
            oldId = self.curSelectedActId
            oldItem = None
            newItem = None
            items = self.widget.lineView.items
            for item in items:
                if newId == long(item.activityNUID):
                    newItem = item
                if oldId == long(item.activityNUID):
                    oldItem = item

            if oldItem:
                oldItem.item.chooseBtn.selected = False
            self.curSelectedActId = activityNUID
            self.curSelectedItem = newItem
            if newItem:
                newItem.item.chooseBtn.selected = True
            self.refreshSelectedState()
            return

    def refreshPlayerList(self):
        if self.curSelectedActId and self.curSelectedItem:
            participator = self.curSelectedItem.participator
            participatorList = []
            for i in xrange(len(participator)):
                participatorItem = participator[i]
                participatorInfo = {}
                participatorInfo['gbId'] = participatorItem[0]
                participatorInfo['name'] = participatorItem[1]
                participatorInfo['school'] = participatorItem[2]
                participatorList.append(participatorInfo)

            self.widget.playerList.dataArray = participatorList
            self.widget.playerList.validateNow()
        else:
            self.widget.playerList.dataArray = []
            self.widget.playerList.validateNow()

    def hasBasedata(self):
        if not self.widget:
            return False
        return True

    def handleRefreshBtnClick(self, *args):
        self.getFightForLoveListData()

    def handleConfirmBtnClick(self, *args):
        if not self.curSelectedActId:
            return
        p = BigWorld.player()
        if self.curSelectedActId and self.curSelectedItem:
            phase = self.curSelectedItem.phase
            createrName = self.curSelectedItem.createrName
            tOccupy = self.curSelectedItem.tOccupy
            startTime = int(tOccupy) + FFLCD.data.get('readyTime', 600)
            startTimeStr = gameStrings.FIGHT_FOR_LOVE_START_TIME % tuple(utils.formatDatetime(startTime).split()[1].split(':'))
            if phase == gametypes.FIGHT_FOR_LOVE_PHASE_RUNNING:
                p.cell.observeFightForLove(self.curSelectedActId)
            elif phase == gametypes.FIGHT_FOR_LOVE_PHASE_PREPARE:
                msg = FFLCD.data.get('applyConfirmMsg', '') % (createrName, startTimeStr)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.cell.applyFightForLove, self.curSelectedActId), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)

    def getFightForLoveListData(self):
        p = BigWorld.player()
        p.cell.queryFightForLoveTotalInfo()
