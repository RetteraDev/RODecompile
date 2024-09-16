#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpPlayoffs5v5VoteProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import random
import gametypes
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis import ui
from guis import uiUtils
from gamestrings import gameStrings
from guis.asObject import TipManager
from data import personal_zone_bonus_data as PZBD

class PvpPlayoffs5v5VoteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpPlayoffs5v5VoteProxy, self).__init__(uiAdapter)
        self.widget = None
        self.teamsInfoDict = {}
        self.randomSeed = random.randint(0, 1000)
        self.lvKey = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PVP_PLAYOFFS_5V5_VOTE, self.hide)

    def reset(self):
        self.canSetFudai = False
        self.teamDataArray = []
        self.lvKey = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PVP_PLAYOFFS_5V5_VOTE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PVP_PLAYOFFS_5V5_VOTE)

    def show(self, canSetFudai = False):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PVP_PLAYOFFS_5V5_VOTE)
        self.canSetFudai = canSetFudai

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.itemList.itemHeight = 45
        self.widget.itemList.itemRenderer = 'PvpPlayoffs5v5_Team'
        self.widget.itemList.labelFunction = self.labelFunction
        self.widget.lvBtn0.selected = False
        self.widget.lvBtn1.selected = True
        self.widget.lvBtn0.addEventListener(events.EVENT_SELECT, self.handleSelectLv, False, 0, True)
        self.widget.lvBtn1.addEventListener(events.EVENT_SELECT, self.handleSelectLv, False, 0, True)
        self.widget.refreshBtn.addEventListener(events.MOUSE_CLICK, self.refreshItemList, False, 0, True)
        if self.canSetFudai:
            self.widget.setFudaiBtn.addEventListener(events.MOUSE_CLICK, self.onSetFudai, False, 0, True)
        else:
            self.widget.setFudaiBtn.disabled = not self.canSetFudai

    def handleSelectLv(self, *args):
        self.refreshItemList()

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshItemList()

    def refreshItemList(self, *args):
        if self.widget.lvBtn0.selected == True:
            self.lvKey = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69
        else:
            self.lvKey = gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79
        self.refreshDataArray()
        ver = self.teamsInfoDict.get(self.lvKey, {}).get('ver', 0)
        BigWorld.player().base.queryArenaPlayoffsTeamVoteData(self.lvKey, ver)

    def labelFunction(self, *args):
        index = int(args[3][0].GetNumber())
        itemMc = ASObject(args[3][1])
        data = self.teamDataArray[index]
        itemMc.teamId = data[0]
        teamDetails = data[1]
        itemMc.teamName.text = teamDetails.get('teamName', '')
        itemMc.leaderName.text = teamDetails.get('members', [''])[0]
        itemMc.teamZhanli.text = teamDetails.get('combatScore', 0)
        itemMc.piaoshu.text = teamDetails.get('voteNum', 0)
        teamMembers = teamDetails.get('members', [''])[1:]
        teamMembersStr = ''
        for member in teamMembers:
            teamMembersStr = teamMembersStr + member + ' '

        TipManager.addTip(itemMc.leaderName, gameStrings.PVP_PLAYOFFS_5V5_TEAM_MEMBERS_TIP % teamMembersStr)
        itemMc.fudaiIcon.dragable = False
        if not len(teamDetails.get('luckyBag', {}).keys()):
            itemMc.fudaiIcon.visible = False
            itemMc.fudaiNumber.visible = False
            itemMc.fudaiBg.visible = False
        else:
            itemMc.fudaiIcon.visible = True
            itemMc.fudaiNumber.visible = True
            itemMc.fudaiBg.visible = True
            fudaiDetil = teamDetails.get('luckyBag', {})
            fudaiType = fudaiDetil.keys()[0]
            fudaiNumber = fudaiDetil[fudaiType]
            iconId = PZBD.data.get(fudaiType, {}).get('itemId', 0)
            itemMc.fudaiIcon.setItemSlotData(uiUtils.getGfxItemById(iconId))
            itemMc.fudaiNumber.text = fudaiNumber
        itemMc.voteBtn.addEventListener(events.MOUSE_CLICK, self.vote, False, 0, True)

    def vote(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.target
        BigWorld.player().cell.voteArenaPlayoffsTeam(self.lvKey, long(itemMc.parent.teamId), 0, 1)
        self.refreshInfo()

    @ui.checkInventoryLock()
    def onSetFudai(self, *args):
        gameglobal.rds.ui.pvpPlayoffs5v5Fudai.show()

    def teamsInfoDictToList(self):
        teamsInfoData = self.teamsInfoDict.get(self.lvKey, {}).get('data', {})
        retList = []
        for key in teamsInfoData:
            item = []
            item.append(key)
            item.append(teamsInfoData[key])
            retList.append(item)

        return retList

    def onGetVoteData(self, data):
        lvKey = data.get('lvKey', 'Undefined')
        self.teamsInfoDict[lvKey] = data
        self.refreshDataArray()

    def refreshDataArray(self):
        if not self.widget:
            return
        random.seed(self.randomSeed)
        self.teamDataArray = self.teamsInfoDictToList()
        dataArray = range(len(self.teamDataArray))
        random.shuffle(dataArray)
        self.widget.itemList.dataArray = dataArray
        self.widget.itemList.validateNow()
