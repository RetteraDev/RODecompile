#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryInviteFriendProxy.o
import BigWorld
from Scaleform import GfxValue
import math
import gameglobal
import gametypes
import uiConst
import utils
import uiUtils
import pinyinConvert
import events
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from data import marriage_config_data as MCD
from data import marriage_package_data as MPD
from cdata import game_msg_def_data as GMDD
from cdata import marriage_extend_guest_data as MEGD
FRIEND_NUM_PER_PAGE = 7
FRIEND_NORMAL_TYPE = 0
FRIEND_GLOBAL_TYPE = 1

class MarryInviteFriendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryInviteFriendProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.needRefresh = False
        self.friendList = []

    def initPanel(self, widget):
        self.widget = widget
        self.tempInviteGuest = self.uiAdapter.marrySettingBg.getCurServerGuestMap().keys()
        self.setFriendIndex(0)

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        self.initData()
        self.initState()
        self.refreshInfo()

    def initData(self):
        self.reset()
        self.refreshFriendListData()

    def initState(self):
        self.widget.mainMc.descList.itemRenderer = 'MarryInviteFriend_DescItem'
        self.widget.mainMc.descList.lableFunction = self.descListItemFunction
        self.widget.mainMc.descList.itemHeightFunction = self.descListItemHeightFunction
        self.widget.mainMc.descList.dataArray = self.getDescData()
        self.widget.mainMc.rightList.itemRenderer = 'MarryInviteFriend_RightFiendItem'
        self.widget.mainMc.rightList.lableFunction = self.rightListItemFunction
        self.widget.mainMc.rightList.itemHeight = 44
        self.widget.mainMc.rightList.dataArray = []
        self.widget.mainMc.leftList.itemRenderer = 'MarryInviteFriend_LeftFriendItem'
        self.widget.mainMc.leftList.lableFunction = self.leftListItemFunction
        self.widget.mainMc.leftList.column = 2
        self.widget.mainMc.leftList.itemHeight = 28
        self.widget.mainMc.leftList.itemWidth = 232
        self.widget.mainMc.leftList.dataArray = []
        self.widget.mainMc.searchFriend.maxChars = 30
        self.widget.mainMc.customMessage.maxChars = 18
        for i in xrange(0, 2):
            tab = getattr(self.widget.mainMc, 'tab%s' % i)
            tab.index = i
            if tab:
                tab.addEventListener(events.BUTTON_CLICK, self.handleTabClick, False, 0, True)

        customMessageDefault = MCD.data.get('customMessageDefault', '')
        self.widget.mainMc.customMessage.defaultText = customMessageDefault
        self.widget.mainMc.searchFriend.addEventListener(events.EVENT_CHANGE, self.handleSearchFriendChange, False, 0, True)
        self.widget.mainMc.saveBtn.addEventListener(events.BUTTON_CLICK, self.handleSaveBtnClick, False, 0, True)
        self.widget.mainMc.freeNumDesc.visible = gameglobal.rds.configData.get('enableMarriageGuestExtend', False)
        self.widget.mainMc.noFriendTxt.htmlText = gameStrings.MARRIAGE_ADD_FRIEND_HTML
        self.widget.mainMc.countPage.minCount = 1
        self.refreshCountMc()
        self.widget.mainMc.countPage.enableMouseWheel = False
        self.widget.mainMc.countPage.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCountChange, False, 0, True)
        tabKF = self.widget.mainMc.tab1
        p = BigWorld.player()
        if p.marriageType == gametypes.MARRIAGE_TYPE_GREAT:
            tabKF.visible = True
        else:
            tabKF.visible = False

    def handleTabClick(self, *args):
        e = ASObject(args[3][0])
        self.setFriendIndex(e.currentTarget.index)

    def setFriendIndex(self, index):
        p = BigWorld.player()
        for i in xrange(0, 2):
            tab = getattr(self.widget.mainMc, 'tab%s' % i)
            if tab:
                tab.selected = False

        selectTab = getattr(self.widget.mainMc, 'tab%s' % index)
        if selectTab:
            selectTab.selected = True
        if index == 0:
            self.friendData = p.friend
        else:
            self.friendData = p.globalFriends.friends
        self.friendIndex = index
        self.initUI()
        self.refreshInfo()

    def getDescData(self):
        dArray = []
        mType, subType = self.uiAdapter.marrySettingBg.getCurServerMarriageType()
        descData = MPD.data.get((mType, subType), {}).get('inviteFriendDesc', ())
        for i, desc in enumerate(descData):
            info = {'desc': desc,
             'index': i}
            dArray.append(info)

        return dArray

    def refreshInfo(self):
        if self.hasBaseData():
            self.refreshLeftList()
            self.refreshRightList()
            curInviteNum = self.getCurInviteNum()
            self.widget.mainMc.leftTitle.text = gameStrings.MARRY_INVITE_GUEST_NUM % (curInviteNum, self.getCurInviteNumLimit())
            self.widget.mainMc.freeNumDesc.text = gameStrings.YUNCUI_BUY_INVITE_FRIEND_LABEL % self.getCurInviteNumLimit()

    def getCurInviteNum(self):
        return len(self.tempInviteGuest)

    def getCurInviteNumLimit(self):
        return self.uiAdapter.marrySettingBg.getCurServerAllowGuest()

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def leftListItemFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            itemMc.gbId = info.gbId
            roleName = utils.preRenameString(info.name) if utils.isRenameString(info.name) else info.name
            itemMc.roleName.text = '%s-%s' % (roleName, utils.getServerName(info.serverId))
            itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleLeftItemRollOut, False, 0, True)
            itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleLeftItemRollOver, False, 0, True)

    def rightListItemFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            p = BigWorld.player()
            itemMc.roleName.text = info.name
            itemMc.intimacy.visible = False
            itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleRightItemRollOut, False, 0, True)
            itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleRightItemRollOver, False, 0, True)
            itemMc.icon.headIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
            itemMc.icon.headIcon.fitSize = True
            itemMc.icon.headIcon.url = self.getFriendPhoto(info)
            itemMc.gbId = info.gbId

    def getRightListData(self):
        p = BigWorld.player()
        rightGuestGbId = self.getPagedData()
        needPatchData = []
        rightGuest = []
        serverList = []
        for gbId in rightGuestGbId:
            if self.needPatchGbId(gbId, needPatchData):
                needPatchData.append(gbId)
                if self.getFriendType() == FRIEND_GLOBAL_TYPE:
                    serverList.append(self.friendData[gbId].server)
                else:
                    serverList.append(utils.getHostId())
            elif not needPatchData:
                fInfo = self.getFriendInfo(gbId)
                if fInfo:
                    rightGuest.append(fInfo)

        if needPatchData:
            self.widget.mainMc.noFriendTxt.visible = False
            p.queryMarriageUnitInfoEx(gametypes.MARRIAGE_QUERY_TYPE_INVITE_FRIEND_PAGE, serverList, needPatchData)
        if len(rightGuest) == len(rightGuestGbId):
            self.receiveRightListData(rightGuest)

    def getLeftListData(self):
        leftGuest = []
        for gbId in self.tempInviteGuest:
            fInfo = self.getFriendInfo(gbId)
            if fInfo:
                leftGuest.append(fInfo)

        return leftGuest

    def refreshLeftList(self):
        if self.hasBaseData():
            dataList = self.getLeftListData()
            self.widget.mainMc.leftList.dataArray = dataList

    def refreshRightList(self):
        if self.hasBaseData():
            self.refreshFriendListData(searchName=self.widget.mainMc.searchFriend.text)
            self.refreshCountMc()
            self.getRightListData()

    def receiveRightListData(self, dataList):
        if self.hasBaseData():
            self.widget.mainMc.rightList.dataArray = dataList
            curInviteNum = self.getCurInviteNum()
            self.widget.mainMc.noFriendTxt.visible = False if len(dataList) or not len(dataList) and curInviteNum >= self.getCurInviteNumLimit() or self.widget.mainMc.searchFriend.text else True

    def handleRightItemRollOver(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.currentTarget
            t.gotoAndStop('over')
            t.inviteBtn.addEventListener(events.BUTTON_CLICK, self.handleInviteBtnClick, False, 0, True)

    def handleRightItemRollOut(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.currentTarget
            t.gotoAndStop('up')

    def handleInviteBtnClick(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            if int(e.target.parent.gbId) in self.tempInviteGuest:
                return
            if len(self.tempInviteGuest) < self.getCurInviteNumLimit():
                self.tempInviteGuest.append(int(e.target.parent.gbId))
            elif gameglobal.rds.configData.get('enableMarriageGuestExtend', False):
                self.extandGuestGbid = int(e.target.parent.gbId)
                mType, subType = self.uiAdapter.marrySettingBg.getCurServerMarriageType()
                maxGuestCount = MPD.data.get((mType, subType), {}).get('maxGuestCount', 0)
                deltaCnt = len(self.tempInviteGuest) + 1 - maxGuestCount
                needYunChui = 0
                for guestCntRange in MEGD.data.keys():
                    if utils.inRange(guestCntRange, deltaCnt):
                        needYunChui = MEGD.data[guestCntRange]['yunChuiNeed']
                        break

                if needYunChui:
                    inviteFriend = gameStrings.YUNCUI_BUY_INVITE_FRIEND % needYunChui
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(inviteFriend, yesCallback=self.applyExtendMarriageGuest)
            self.refreshInfo()

    def applyExtendMarriageGuest(self):
        p = BigWorld.player()
        p.cell.applyExtendMarriageGuest()

    def refreshExtendGuest(self):
        if getattr(self, 'extandGuestGbid', None):
            self.tempInviteGuest.append(self.extandGuestGbid)
            self.extandGuestGbid = None
        self.refreshInfo()

    def getFriendPhoto(self, friendInfo):
        return self.uiAdapter.marrySettingBg.getFriendPhoto(friendInfo)

    def handleLeftItemRollOver(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.currentTarget
            t.gotoAndStop('over')
            if long(t.gbId) not in self.uiAdapter.marrySettingBg.getCurServerGuestMap().keys():
                t.removeBtn.visible = True
                t.alreadyInviteMc.visible = False
                t.removeBtn.addEventListener(events.BUTTON_CLICK, self.handleRemoveBtnClick, False, 0, True)
            else:
                t.removeBtn.visible = False
                t.alreadyInviteMc.visible = True

    def handleLeftItemRollOut(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.currentTarget
            t.gotoAndStop('up')

    def handleRemoveBtnClick(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            if int(e.target.parent.gbId) in self.tempInviteGuest:
                self.tempInviteGuest.remove(int(e.target.parent.gbId))
            self.refreshInfo()

    def handleSearchFriendChange(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            self.refreshRightList()

    def descListItemFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if info and itemMc:
            itemMc.descTxt.htmlText = info.desc

    def descListItemHeightFunction(self, *arg):
        if self.hasBaseData():
            info = ASObject(arg[3][0])
            descItem = self.widget.getInstByClsName('MarryInviteFriend_DescItem')
            descItem.descTxt.htmlText = info.desc
            return GfxValue(descItem.descTxt.textHeight)

    def handleSaveBtnClick(self, *arg):
        p = BigWorld.player()
        msg = self.getCustomMessage()
        if not self.uiAdapter.marrySettingBg.tabooCheck(msg):
            p.showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
            return
        addGuestList = []
        delGuestList = []
        addServerList = []
        oData = self.uiAdapter.marrySettingBg.getCurServerGuestMap().keys()
        allGuestSet = set(oData) | set(self.tempInviteGuest)
        if len(allGuestSet) > self.getCurInviteNumLimit():
            p.showGameMsg(GMDD.data.MARRIAGE_INVITE_GUEST_FULL, ())
            self.needRefresh = True
            self.weakRefresh()
            return
        if allGuestSet == set(oData):
            return
        for item in self.tempInviteGuest:
            if item not in oData:
                addGuestList.append(item)
                fVal = self.getFriendInfo(item)
                addServerList.append(fVal.get('serverId', 0))

        p.cell.setMarriageGuests(addServerList, addGuestList, delGuestList, msg)
        self.needRefresh = True

    def weakRefresh(self):
        if self.needRefresh:
            self.tempInviteGuest = self.uiAdapter.marrySettingBg.getCurServerGuestMap().keys()
            self.refreshInfo()
            self.needRefresh = False

    def getCustomMessage(self):
        if not self.hasBaseData():
            return ''
        if self.widget.mainMc.customMessage.text:
            return self.widget.mainMc.customMessage.text
        return self.widget.mainMc.customMessage.defaultText

    def getFriendInfo(self, gbId):
        return self.uiAdapter.marrySettingBg.getFriendInfo(gbId)

    def getCurPage(self):
        if self.hasBaseData():
            return self.widget.mainMc.countPage.count
        return 0

    def getPagedData(self):
        idx1 = (self.getCurPage() - 1) * FRIEND_NUM_PER_PAGE
        idx2 = self.getCurPage() * FRIEND_NUM_PER_PAGE
        return self.friendList[idx1:idx2]

    def refreshFriendListData(self, searchName = ''):
        rightGuest = []
        member = self.uiAdapter.marrySettingBg.getCurServerMember()
        for k, fVal in self.friendData.iteritems():
            name = ''
            if self.getFriendType() == FRIEND_NORMAL_TYPE:
                acknowledge = fVal.acknowledge
                name = fVal.name
            else:
                acknowledge = True
                fVal = self.getFriendInfo(k)
                name = fVal.get('name', '')
            if acknowledge and k not in self.tempInviteGuest and k not in member:
                if searchName:
                    if uiUtils.filterPinYin(searchName, name):
                        rightGuest.append(k)
                else:
                    rightGuest.append(k)

        self.friendList = rightGuest

    def handleCountChange(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.target
            self.refreshRightList()

    def refreshCountMc(self):
        if self.hasBaseData():
            lastMaxCount = self.widget.mainMc.countPage.maxCount
            self.widget.mainMc.countPage.maxCount = math.ceil(len(self.friendList) * 1.0 / FRIEND_NUM_PER_PAGE)

    def needPatchGbId(self, gbId, needPatchData):
        return self.uiAdapter.marrySettingBg.needPatchGbId(gbId, needPatchData)

    def getFriendType(self):
        return self.friendIndex
