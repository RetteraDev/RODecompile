#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTopVoteProxy.o
import BigWorld
import copy
import gamelog
import utils
import gametypes
from gamestrings import gameStrings
import uiConst
import events
from guis import uiUtils
from guis.asObject import ASObject
from uiProxy import UIProxy
from data import school_top_config_data as STCD
from cdata import game_msg_def_data as GMDD

class SchoolTopVoteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTopVoteProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TOP_VOTE, self.hide)

    def reset(self):
        self.selectedItemMc = None
        self.selfIdx = -1
        self.autoJump = True

    @property
    def selfData(self):
        p = BigWorld.player()
        return p.getSelfCandidateData()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TOP_VOTE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TOP_VOTE)

    def show(self):
        p = BigWorld.player()
        if not getattr(p, 'schoolTopStage', {}).get(p.school, None) == gametypes.SCHOOL_TOP_STAGE_CAMPAIGN:
            p.showGameMsg(GMDD.data.NOT_IN_SCHOOL_TOP_STAGE_CAMPAIGN, ())
            return
        else:
            if not self.widget:
                self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TOP_VOTE)
            p.base.querySchoolTopCandidates()
            return

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.declareBtn.addEventListener(events.BUTTON_CLICK, self.handleDeclareBtnClick, False, 0, True)
        self.widget.addGiftBtn.addEventListener(events.BUTTON_CLICK, self.handleAddGiftBtnClick, False, 0, True)
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshBtnClick, False, 0, True)
        self.widget.scrollWndList.itemRenderer = 'SchoolTopVote_Item'
        self.widget.scrollWndList.labelFunction = self.labelFunction
        endTime = utils.getNextCrontabTime(STCD.data.get('matchStartTime', '15 19 * * 5'))
        if not utils.isSameWeek(endTime, utils.getNow()):
            endTime = utils.getPreCrontabTime(STCD.data.get('matchStartTime', '15 19 * * 5'))
        self.widget.txtEndTime.text = gameStrings.SCHOOL_TOP_COMPAIGN_END_TIME % utils.formatDate(endTime)

    def getInfo(self):
        dataInfo = {}
        dataList = []
        p = BigWorld.player()
        schoolTopCandidates = getattr(p, 'schoolTopCandidates', {})
        rankList = [ (gbId, schoolTopCandidates[gbId]['ticketCnt'], schoolTopCandidates[gbId]['rank']) for gbId in schoolTopCandidates ]
        rankList.sort(cmp=lambda x, y: cmp((x[1], y[2]), (y[1], x[2])), reverse=True)
        selfIdx = -1
        for index, rankInfo in enumerate(rankList):
            gbId, tickCnt, r = rankInfo
            copyData = copy.deepcopy(schoolTopCandidates[gbId])
            copyData['rank'] = index + 1
            dataList.append((gbId, copyData))
            itemId = 0
            itemCnt = 0
            luckBag = copyData.get('luckyBag', {})
            if luckBag.get(1, 0):
                itemId = STCD.data.get('luckyBagItems', {}).get(1, 999)
                itemCnt = luckBag[1]
            elif luckBag.get(2, 0):
                itemId = STCD.data.get('luckyBagItems', {}).get(2, 999)
                itemCnt = luckBag[2]
            elif luckBag.get(3, 0):
                itemId = STCD.data.get('luckyBagItems', {}).get(3, 999)
                itemCnt = luckBag[3]
            copyData['itemId'] = itemId
            copyData['itemCnt'] = itemCnt
            if gbId == p.gbId:
                selfIdx = index

        dataInfo['selfIdx'] = selfIdx
        dataInfo['dataList'] = dataList
        return dataInfo

    def getVoteCntInfo(self):
        import random
        return (3, random.randint(0, 3))

    def refreshInfo(self):
        if not self.widget:
            return
        dataInfo = self.getInfo()
        selfIdx = dataInfo['selfIdx']
        dataList = dataInfo['dataList']
        self.selfIdx = selfIdx
        self.widget.scrollWndList.dataArray = dataList
        self.widget.scrollWndList.validateNow()
        if self.autoJump and selfIdx >= 0 and dataList:
            pos = max(0, selfIdx - 3) * self.widget.scrollWndList.itemHeight
            self.widget.scrollWndList.scrollbar.position = pos
            self.autoJump = False
        self.widget.declareBtn.enabled = bool(self.selfData)
        self.widget.addGiftBtn.enabled = bool(self.selfData)

    def handleDeclareBtnClick(self, *args):
        self.uiAdapter.schoolTopDeclare.show()

    def handleAddGiftBtnClick(self, *args):
        self.uiAdapter.schoolTopSetGift.show()

    def labelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.button.validateNow()
        itemMc.button.addEventListener(events.BUTTON_CLICK, self.handleItemClick, False, 0, True)
        if self.selfIdx + 1 == int(itemData[1].rank):
            if self.selectedItemMc:
                self.selectedItemMc.button.selected = False
            self.selectedItemMc = itemMc
            self.selectedItemMc.button.selected = True
        else:
            itemMc.button.selected = False
        itemMc.itemData = itemData
        if itemData[1].rank == 1:
            itemMc.qualificationIcon.visible = True
        else:
            itemMc.qualificationIcon.visible = False
        itemMc.button.txtPlayerName.text = itemData[1].roleName
        itemMc.button.txtGuildName.text = itemData[1].guildName
        itemMc.button.txtCnt.text = itemData[1].ticketCnt
        itemMc.item.dragable = False
        if int(itemData[1].itemCnt):
            itemMc.item.setItemSlotData(uiUtils.getGfxItemById(int(itemData[1].itemId), int(itemData[1].itemCnt)))
            itemMc.item.visible = True
        else:
            itemMc.item.visible = False
        itemMc.voteBtn.data = itemData
        itemMc.voteBtn.addEventListener(events.BUTTON_CLICK, self.handleVoteBtnClick, False, 0, True)

    def handleVoteBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemData = e.currentTarget.data
        p = BigWorld.player()
        gamelog.info('jbx:handleVoteBtnClick, gbId', int(itemData[0]))
        p.cell.schoolTopVotePlayer(int(itemData[0]))

    def handleItemClick(self, *args):
        e = ASObject(args[3][0])
        if self.selectedItemMc:
            self.selectedItemMc.button.selected = False
        self.selectedItemMc = e.currentTarget.parent
        self.selectedItemMc.button.selected = True
        self.selfIdx = int(e.currentTarget.parent.itemData[1].rank) - 1

    def handleRefreshBtnClick(self, *args):
        BigWorld.player().base.querySchoolTopCandidates()
