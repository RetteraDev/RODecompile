#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/missTianyuGroupTopRankProxy.o
import BigWorld
import gameglobal
import uiConst
import gametypes
import events
import utils
import random
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import ui
from guis import uiUtils
from guis.asObject import ASObject
from asObject import MenuManager
from missTianyu import MissTianyuGroupVal as PreliminaryData
from missTianyu import MissTianyuPlayoffVal as FinalsData
from cdata import personal_zone_config_data as PZCD
FORMAT_COLOR = "<font color = \'#a65b11\'>%s</font>"
TOP_HIDE_NUM = 40

class MissTianyuGroupTopRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MissTianyuGroupTopRankProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_MISS_TIANYU_GROUP_TOP_RANK, self.hide)
        self.type = gametypes.TOP_TYPE_MISS_TIANYU_GROUP
        self.updateBtnCoolDownTime = 0
        self.selectedItem = None
        self.preliminaryVersion = 0
        self.preliminaryCache = []
        self.myPreliminaryRank = -1
        self.myPreliminaryHeat = 0
        self.finalsVersion = 0
        self.finalsCache = []
        self.myFinalsRank = -1
        self.myFinalsVotes = 0

    def reset(self):
        self.type = gametypes.TOP_TYPE_MISS_TIANYU_GROUP
        self.updateBtnCoolDownTime = 0
        self.selectedItem = None
        self.preliminaryVersion = 0
        self.preliminaryCache = []
        self.myPreliminaryRank = -1
        self.myPreliminaryHeat = 0
        self.finalsVersion = 0
        self.finalsCache = []
        self.myFinalsRank = -1
        self.myFinalsVotes = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MISS_TIANYU_GROUP_TOP_RANK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            self.requestData()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MISS_TIANYU_GROUP_TOP_RANK)

    def show(self, rankType):
        self.type = rankType
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MISS_TIANYU_GROUP_TOP_RANK)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.refreshBtn.label = gameStrings.REFRESH_BTN_LABEL
        self.widget.refreshBtn.addEventListener(events.MOUSE_CLICK, self.handleRefreshBtnClick, False, 0, True)
        if self.type == gametypes.TOP_TYPE_MISS_TIANYU_GROUP:
            self.hideFinalsUI()
            self.initPreliminaryUI()
        elif self.type == gametypes.TOP_TYPE_MISS_TIANYU_PLAYOFF:
            self.hidePreliminaryUI()
            self.initFinalsUI()

    def refreshInfo(self):
        if not self.widget:
            return
        if self.type == gametypes.TOP_TYPE_MISS_TIANYU_GROUP:
            self.refreshPreliminaryUI()
        elif self.type == gametypes.TOP_TYPE_MISS_TIANYU_PLAYOFF:
            self.refreshFinalsUI()

    def requestData(self):
        if self.type == gametypes.TOP_TYPE_MISS_TIANYU_GROUP:
            self.requestPreliminaryData()
        elif self.type == gametypes.TOP_TYPE_MISS_TIANYU_PLAYOFF:
            self.requestFinalsData()

    def handleRefreshBtnClick(self, *args):
        self.startUpdateBtnCooldownTimer()
        if self.type == gametypes.TOP_TYPE_MISS_TIANYU_GROUP:
            self.requestPreliminaryData()
        else:
            self.requestFinalsData()

    def initPreliminaryUI(self):
        self.widget.title.text = gameStrings.MISS_GROUP_PRELIMINARY_TITLE
        self.widget.preliminaryList.visible = True
        self.widget.preliminaryList.list.itemRenderer = 'MissTianyuGroupTopRank_PreliminaryItem'
        self.widget.preliminaryList.list.barAlwaysVisible = True
        self.widget.preliminaryList.list.dataArray = []
        self.widget.preliminaryList.list.lableFunction = self.preliminaryListItemRenderer
        self.widget.heatInfo.visible = True
        self.widget.heatInfo.myHeat.text = ''
        self.widget.myRank.text = ''
        self.widget.rankDesc.text = PZCD.data.get('topPreliminaryRankDesc', '')
        self.widget.rulesBtn.addEventListener(events.BUTTON_CLICK, self.handlePreliminaryHelpKeyClick, False, 0, True)

    def hidePreliminaryUI(self):
        self.widget.preliminaryList.visible = False
        self.widget.heatInfo.visible = False

    def refreshPreliminaryUI(self):
        self.selectedItem = None
        if self.isInMissTianyuProcess():
            pass
        else:
            self.breakRankPreliminaryData()
        self.widget.preliminaryList.list.dataArray = self.preliminaryCache
        self.widget.myRank.text = gameStrings.MISS_GROUP_OUT_OF_RANK if self.myPreliminaryRank == -1 else str(self.myPreliminaryRank)
        self.refreshPreliminaryHeat()

    def breakRankPreliminaryData(self):
        if not self.preliminaryCache:
            return
        topHide = self.preliminaryCache[0:TOP_HIDE_NUM]
        theOthers = self.preliminaryCache[TOP_HIDE_NUM:]
        random.shuffle(topHide)
        self.preliminaryCache = topHide + theOthers

    def preliminaryListItemRenderer(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.gotoAndStop('up')
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)
        isMyself = itemData.isMyself is True
        rank = itemData.rank
        rankStr = str(int(rank))
        gbId = long(itemData.gbId)
        roleName = itemData.roleName
        school = itemData.school
        gender = itemData.gender
        hostId = itemData.hostId
        photo = itemData.photo
        borderId = itemData.borderId
        borderIcon = BigWorld.player().getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
        heat = itemData.val
        heatStr = str(int(heat))
        isInProcess = self.isInMissTianyuProcess()
        if isInProcess:
            itemMc.top3Icon.visible = rank <= 3
            if itemMc.top3Icon.visible:
                itemMc.top3Icon.gotoAndStop('top%d' % rank)
        else:
            itemMc.top3Icon.visible = False
        if isInProcess:
            if itemMc.top3Icon.visible:
                itemMc.rank.visible = False
            else:
                itemMc.rank.visible = True
                itemMc.rank.htmlText = self.__getRankTextFormat(rankStr, isMyself)
        else:
            itemMc.rank.visible = rank > TOP_HIDE_NUM
            if itemMc.rank.visible:
                itemMc.rank.htmlText = self.__getRankTextFormat(rankStr, isMyself)
        if photo:
            itemMc.headIcon.icon.fitSize = True
            itemMc.headIcon.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
            itemMc.headIcon.icon.serverId = hostId
            itemMc.headIcon.icon.url = photo
        else:
            itemMc.headIcon.icon.fitSize = True
            itemMc.headIcon.icon.loadImage(uiUtils.getHeadIconPath(school, gender))
        itemMc.headIcon.borderImg.fitSize = True
        itemMc.headIcon.borderImg.loadImage(borderIcon)
        itemMc.roleName.htmlText = self.__getRankTextFormat(roleName, isMyself)
        MenuManager.getInstance().registerMenuById(itemMc.roleName, uiConst.MENU_PERSOANL_SPACE, {'roleName': roleName,
         'gbId': gbId})
        itemMc.serverName.htmlText = self.__getRankTextFormat(utils.getServerName(hostId), isMyself)
        if isInProcess:
            itemMc.heat.htmlText = self.__getRankTextFormat(heatStr, isMyself)
        else:
            itemMc.heat.htmlText = '****' if rank <= TOP_HIDE_NUM else self.__getRankTextFormat(heatStr, isMyself)
        itemMc.homeBtn.data = (gbId, hostId)
        itemMc.homeBtn.addEventListener(events.BUTTON_CLICK, self.handleHomeBtnClick, False, 0, True)

    def refreshPreliminaryHeat(self):
        if not self.widget:
            return
        self.widget.heatInfo.myHeat.text = str(self.myPreliminaryHeat)

    def handleHomeBtnClick(self, *args):
        e = ASObject(args[3][0])
        gbId = long(e.currentTarget.data[0])
        hostId = int(e.currentTarget.data[1])
        p = BigWorld.player()
        p.getPersonalSysProxy().openZoneOther(gbId, hostId=hostId)

    def handlePreliminaryHelpKeyClick(self, *args):
        helpKey = PZCD.data.get('preliminaryHelpKey', 0)
        gameglobal.rds.ui.showHelpByKey(helpKey)

    def requestPreliminaryData(self):
        p = BigWorld.player()
        p.base.queryTopUniversal(gametypes.TOP_TYPE_MISS_TIANYU_GROUP, self.preliminaryVersion, '')
        p.base.queryGroupValMT()

    @ui.uiEvent(uiConst.WIDGET_MISS_TIANYU_GROUP_TOP_RANK, events.EVENT_MISS_TIANYU_GROUP_PRELIMINARY_DATA)
    def onPreliminaryDataUpdate(self, event):
        version = event.data.get('version', 0)
        dataList = event.data.get('data', [])
        self.preliminaryVersion = version
        self.preliminaryCache, self.myPreliminaryRank, self.myPreliminaryHeat = self.preliminaryDataProcessor(dataList)
        if self.type == gametypes.TOP_TYPE_MISS_TIANYU_GROUP:
            self.refreshInfo()

    @ui.uiEvent(uiConst.WIDGET_MISS_TIANYU_GROUP_TOP_RANK, events.EVENT_MISS_TIANYU_GROUP_PRELIMINARY_HEAT_UPDATE)
    def onPreliminaryHeatValueUpdate(self, event):
        self.myPreliminaryHeat = int(event.data.get('heat', 0))
        self.refreshPreliminaryHeat()

    def preliminaryDataProcessor(self, dataList):
        ret = []
        myRank = -1
        myHeat = 0
        for data in dataList:
            pdata = PreliminaryData()
            pdata.fromDTO(data)
            ret.append(pdata.toDict())

        ret.sort(cmp=lambda a, b: cmp(a.get('val', 0), b.get('val', 0)), reverse=True)
        p = BigWorld.player()
        for i, data in enumerate(ret):
            if data.get('gbId', None) == p.gbId:
                data['isMyself'] = True
                myRank = i + 1
                myHeat = data.get('val', 0)
            data['rank'] = i + 1

        return (ret, myRank, myHeat)

    def initFinalsUI(self):
        self.widget.title.text = gameStrings.MISS_GROUP_FINALS_TITLE
        self.widget.finalsList.visible = True
        self.widget.finalsList.list.itemRenderer = 'MissTianyuGroupTopRank_FinalsItem'
        self.widget.finalsList.list.barAlwaysVisible = True
        self.widget.finalsList.list.dataArray = []
        self.widget.finalsList.list.lableFunction = self.finalsListItemRenderer
        self.widget.voteInfo.visible = True
        self.widget.voteInfo.myVote.text = ''
        self.widget.myRank.text = ''
        self.widget.rankDesc.text = PZCD.data.get('topFinalsRankDesc', '')
        self.widget.rulesBtn.addEventListener(events.BUTTON_CLICK, self.handleFinalsHelpKeyClick, False, 0, True)

    def hideFinalsUI(self):
        self.widget.finalsList.visible = False
        self.widget.voteInfo.visible = False

    def refreshFinalsUI(self):
        self.selectedItem = None
        self.widget.finalsList.list.dataArray = self.finalsCache
        self.widget.voteInfo.myVote.text = str(self.myFinalsVotes)
        self.widget.myRank.text = gameStrings.MISS_GROUP_OUT_OF_RANK if self.myFinalsRank == -1 else str(self.myFinalsRank)

    def finalsListItemRenderer(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.gotoAndStop('up')
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)
        isMyself = itemData.isMyself is True
        rank = itemData.rank
        rankStr = str(int(rank))
        gbId = long(itemData.gbId)
        roleName = itemData.roleName
        school = itemData.school
        gender = itemData.gender
        hostId = itemData.hostId
        photo = itemData.photo
        borderId = itemData.borderId
        borderIcon = BigWorld.player().getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
        fansGbId = itemData.fansGbId
        fansName = itemData.fansRoleName
        fansSchool = itemData.fansSchool
        fansGender = itemData.fansGender
        fansPhoto = itemData.fansPhoto
        fansHostId = itemData.fansHostId
        fansBorderId = itemData.fansBorderId
        fansBorderIcon = BigWorld.player().getPhotoBorderIcon(fansBorderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
        votes = itemData.val
        votesStr = str(int(votes))
        itemMc.top3Icon.visible = rank <= 3
        if itemMc.top3Icon.visible:
            itemMc.top3Icon.gotoAndStop('top%d' % rank)
        itemMc.rank.visible = rank > 3
        if itemMc.rank.visible:
            itemMc.rank.htmlText = self.__getRankTextFormat(rankStr, isMyself)
        if photo:
            itemMc.headIcon.icon.fitSize = True
            itemMc.headIcon.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
            itemMc.headIcon.icon.serverId = hostId
            itemMc.headIcon.icon.url = photo
        else:
            itemMc.headIcon.icon.fitSize = True
            itemMc.headIcon.icon.loadImage(uiUtils.getHeadIconPath(school, gender))
        itemMc.headIcon.borderImg.fitSize = True
        itemMc.headIcon.borderImg.loadImage(borderIcon)
        itemMc.fansIcon.visible = fansGbId != 0
        if itemMc.fansIcon.visible:
            if fansPhoto:
                itemMc.fansIcon.icon.fitSize = True
                itemMc.fansIcon.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
                itemMc.fansIcon.icon.serverId = fansHostId
                itemMc.fansIcon.icon.url = fansPhoto
            else:
                itemMc.fansIcon.icon.fitSize = True
                itemMc.fansIcon.icon.loadImage(uiUtils.getHeadIconPath(fansSchool, fansGender))
        itemMc.fansIcon.borderImg.fitSize = True
        itemMc.fansIcon.borderImg.loadImage(fansBorderIcon)
        itemMc.roleName.htmlText = self.__getRankTextFormat(roleName, isMyself)
        MenuManager.getInstance().registerMenuById(itemMc.roleName, uiConst.MENU_PERSOANL_SPACE, {'roleName': roleName,
         'gbId': gbId,
         'hostId': hostId})
        itemMc.fansName.htmlText = self.__getRankTextFormat(fansName, isMyself)
        MenuManager.getInstance().registerMenuById(itemMc.fansName, uiConst.MENU_PERSOANL_SPACE, {'roleName': fansName,
         'gbId': fansGbId,
         'hostId': fansHostId})
        itemMc.serverName.htmlText = self.__getRankTextFormat(utils.getServerName(hostId), isMyself)
        itemMc.votes.htmlText = self.__getRankTextFormat(votesStr, isMyself)
        if isMyself:
            itemMc.voteBtn.enabled = False
        else:
            itemMc.voteBtn.enabled = True
            itemMc.voteBtn.data = (gbId, roleName, hostId)
            itemMc.voteBtn.addEventListener(events.BUTTON_CLICK, self.handleVoteBtnClick, False, 0, True)

    def requestFinalsData(self):
        p = BigWorld.player()
        p.base.queryTopUniversal(gametypes.TOP_TYPE_MISS_TIANYU_PLAYOFF, self.finalsVersion, '')

    @ui.uiEvent(uiConst.WIDGET_MISS_TIANYU_GROUP_TOP_RANK, events.EVENT_MISS_TIANYU_GROUP_FINALS_DATA)
    def onFinalsDataUpdate(self, event):
        version = event.data.get('version', 0)
        dataList = event.data.get('data', [])
        self.finalsVersion = version
        self.finalsCache, self.myFinalsRank, self.myFinalsVotes = self.finalsDataProcessor(dataList)
        if self.type == gametypes.TOP_TYPE_MISS_TIANYU_PLAYOFF:
            self.refreshInfo()

    def finalsDataProcessor(self, dataList):
        ret = []
        myRank = -1
        myVotes = 0
        for data in dataList:
            fdata = FinalsData()
            fdata.fromDTO(data)
            ret.append(fdata.toDict())

        ret.sort(cmp=lambda a, b: cmp(a.get('val', 0), b.get('val', 0)), reverse=True)
        p = BigWorld.player()
        for i, data in enumerate(ret):
            if data.get('gbId', None) == p.gbId:
                data['isMyself'] = True
                myRank = i + 1
                myVotes = data.get('val', 0)
            data['rank'] = i + 1

        return (ret, myRank, myVotes)

    def handleVoteBtnClick(self, *args):
        e = ASObject(args[3][0])
        gbId, roleName, hostId = e.currentTarget.data
        gameglobal.rds.ui.spaceGiftGiving.show(gbId, roleName, hostId, showType=gametypes.SPACE_GIFT_GIVING_MISS_GROUP_VOTE)

    def handleFinalsHelpKeyClick(self, *args):
        helpKey = PZCD.data.get('preliminaryHelpKey', 0)
        gameglobal.rds.ui.showHelpByKey(helpKey)

    def handleItemClick(self, *args):
        e = ASObject(args[3][0])
        if self.selectedItem:
            self.selectedItem.gotoAndStop('up')
        self.selectedItem = e.currentTarget
        e.currentTarget.gotoAndStop('down')

    def startUpdateBtnCooldownTimer(self):
        self.updateBtnCoolDownTime = 61
        BigWorld.callback(0, self.__updateBtnTimerCallback)

    def __updateBtnTimerCallback(self, *args):
        self.updateBtnCoolDownTime -= 1
        if self.updateBtnCoolDownTime > 0:
            BigWorld.callback(1, self.__updateBtnTimerCallback)
        if self.widget:
            self.widget.refreshBtn.enabled = self.updateBtnCoolDownTime == 0
            if self.updateBtnCoolDownTime > 0:
                self.widget.refreshBtn.label = gameStrings.REFRESH_BTN_LABEL_CD % self.updateBtnCoolDownTime
            else:
                self.widget.refreshBtn.label = gameStrings.REFRESH_BTN_LABEL

    def __getRankTextFormat(self, text, isMyself):
        if isMyself:
            return FORMAT_COLOR % text
        return text

    def isInMissTianyuProcess(self):
        p = BigWorld.player()
        return p.missTianyuState == gametypes.MISS_TIANYU_GROUP_PROCESS
