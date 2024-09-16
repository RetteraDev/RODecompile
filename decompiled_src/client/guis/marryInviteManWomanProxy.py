#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryInviteManWomanProxy.o
import BigWorld
from Scaleform import GfxValue
import math
import gameglobal
import gametypes
import uiConst
import utils
import uiUtils
import const
import pinyinConvert
import events
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from asObject import ASUtils
from callbackHelper import Functor
from data import marriage_config_data as MCD
from data import marriage_package_data as MPD
from cdata import game_msg_def_data as GMDD
MAN_LIMIT_NUM = 3
WOMAN_LIMIT_NUM = 3
FRIEND_NUM_PER_PAGE = 7

class MarryInviteManWomanProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryInviteManWomanProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.tempMan = []
        self.tempWoman = []
        self.friendList = []

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        self.reset()
        manMap, womanMap = self.uiAdapter.marrySettingBg.getCurServerManAndWomanMap()
        self.tempMan, self.tempWoman = manMap.keys(), womanMap.keys()
        self.refreshFriendListData()

    def initState(self):
        self.widget.mainMc.descList.itemRenderer = 'MarryInviteManWoman_DescItem'
        self.widget.mainMc.descList.lableFunction = self.descListItemFunction
        self.widget.mainMc.descList.itemHeightFunction = self.descListItemHeightFunction
        self.widget.mainMc.descList.dataArray = self.getDescData()
        self.widget.mainMc.rightList.itemRenderer = 'MarryInviteManWoman_RightFiendItem'
        self.widget.mainMc.rightList.lableFunction = self.rightListItemFunction
        self.widget.mainMc.rightList.itemHeight = 44
        self.widget.mainMc.rightList.dataArray = []
        self.widget.mainMc.searchFriend.maxchars = 30
        self.widget.mainMc.searchFriend.addEventListener(events.EVENT_CHANGE, self.handleSearchFriendChange, False, 0, True)
        self.widget.mainMc.saveBtn.addEventListener(events.BUTTON_CLICK, self.handleSaveBtnClick, False, 0, True)
        self.widget.mainMc.noFriendTxt.htmlText = gameStrings.MARRIAGE_ADD_FRIEND_HTML
        self.widget.mainMc.countPage.minCount = 1
        self.refreshCountMc()
        self.widget.mainMc.countPage.enableMouseWheel = False
        self.widget.mainMc.countPage.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCountChange, False, 0, True)

    def refreshInfo(self):
        if self.hasBaseData():
            self.refreshRightList()
            self.refreshManWoman()

    def refreshRightList(self):
        if self.hasBaseData():
            self.refreshFriendListData(searchName=self.widget.mainMc.searchFriend.text)
            self.refreshCountMc()
            self.getRightListData()

    def receiveRightListData(self, dataList):
        if self.hasBaseData():
            self.widget.mainMc.rightList.dataArray = dataList
            self.widget.mainMc.noFriendTxt.visible = False if len(dataList) or self.widget.mainMc.searchFriend.text else True

    def refreshManWoman(self):
        if self.hasBaseData():
            limitNum = self.getLimitNum()
            for i in xrange(0, MAN_LIMIT_NUM):
                manMc = getattr(self.widget.mainMc, 'manMc' + str(i))
                if manMc:
                    if i < limitNum:
                        manMc.visible = True
                        if i < len(self.tempMan):
                            gbId = self.tempMan[i]
                            self.setLeftItem(manMc, gbId, False)
                        else:
                            self.setLeftItem(manMc, 0, True)
                    else:
                        manMc.visible = False

            for i in xrange(0, WOMAN_LIMIT_NUM):
                womanMc = getattr(self.widget.mainMc, 'womanMc' + str(i))
                if womanMc:
                    if i < limitNum:
                        womanMc.visible = True
                        if i < len(self.tempWoman):
                            gbId = self.tempWoman[i]
                            self.setLeftItem(womanMc, gbId, False)
                        else:
                            self.setLeftItem(womanMc, 0, True)
                    else:
                        womanMc.visible = False

    def setLeftItem(self, mc, gbId, isEmpty):
        if not mc:
            return
        p = BigWorld.player()
        fInfo = self.getFriendInfo(gbId)
        if not fInfo:
            isEmpty = True
        if not isEmpty:
            if fInfo:
                mc.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
                mc.icon.fitSize = True
                mc.icon.url = self.getFriendPhoto(fInfo)
                roleName = utils.preRenameString(fInfo.get('roleName')) if utils.isRenameString(fInfo.get('roleName')) else fInfo.get('roleName')
                mc.roleName.text = roleName
                mc.icon.visible = True
                mc.roleName.visible = True
                mc.removeBtn.visible = False
                mc.addEventListener(events.MOUSE_ROLL_OUT, self.handleLeftItemRollOut, False, 0, True)
                mc.addEventListener(events.MOUSE_ROLL_OVER, self.handleLeftItemRollOver, False, 0, True)
                mc.gbId = fInfo.get('gbId')
                mc.removeBtn.addEventListener(events.BUTTON_CLICK, self.handleRemoveClick, False, 0, True)
        else:
            mc.icon.visible = False
            mc.roleName.visible = False
            mc.removeBtn.visible = False
            mc.removeEventListener(events.MOUSE_ROLL_OUT, self.handleLeftItemRollOut)
            mc.removeEventListener(events.MOUSE_ROLL_OVER, self.handleLeftItemRollOver)

    def getDescData(self):
        dArray = []
        mType, subType = self.uiAdapter.marrySettingBg.getCurServerMarriageType()
        descData = MPD.data.get((mType, subType), {}).get('inviteManWomanDesc', ())
        for i, desc in enumerate(descData):
            info = {'desc': desc,
             'index': i}
            dArray.append(info)

        return dArray

    def descListItemFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if info and itemMc:
            itemMc.descTxt.htmlText = info.desc

    def descListItemHeightFunction(self, *arg):
        if self.hasBaseData():
            info = ASObject(arg[3][0])
            descItem = self.widget.getInstByClsName('MarryInviteManWoman_DescItem')
            descItem.descTxt.htmlText = info.desc
            return GfxValue(descItem.descTxt.textHeight)

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def rightListItemFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            p = BigWorld.player()
            itemMc.roleName.text = info.name
            itemMc.intimacy.visible = info.hasIntimacyTgt
            if info.hasIntimacyTgt:
                ASUtils.setMcEffect(itemMc.icon, 'gray')
            else:
                ASUtils.setMcEffect(itemMc.icon, '')
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
                serverList.append(utils.getHostId())
            elif not needPatchData:
                fInfo = self.getFriendInfo(gbId)
                if fInfo:
                    rightGuest.append(fInfo)

        if needPatchData:
            self.widget.mainMc.noFriendTxt.visible = False
            p.queryMarriageUnitInfoEx(gametypes.MARRIAGE_QUERY_TYPE_INVITE_MAN_PAGE, serverList, needPatchData)
        if len(rightGuest) == len(rightGuestGbId):
            self.receiveRightListData(rightGuest)

    def getFriendPhoto(self, friendInfo):
        return self.uiAdapter.marrySettingBg.getFriendPhoto(friendInfo)

    def handleRightItemRollOver(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.currentTarget
            t.gotoAndStop('over')
            t.inviteBtn.visible = not t.intimacy.visible
            t.inviteBtn.addEventListener(events.BUTTON_CLICK, self.handleInviteBtnClick, False, 0, True)

    def handleRightItemRollOut(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.currentTarget
            t.gotoAndStop('up')

    def handleInviteBtnClick(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            p = BigWorld.player()
            limitNum = self.getLimitNum()
            fVal = p.friend.get(int(e.target.parent.gbId))
            if fVal and fVal.sex == const.SEX_MALE:
                if len(self.tempMan) < limitNum and int(e.target.parent.gbId) not in self.tempMan:
                    self.tempMan.append(int(e.target.parent.gbId))
                else:
                    p.showGameMsg(GMDD.data.MARRIAGE_INVITE_MAN_FULL, ())
            elif len(self.tempWoman) < limitNum and int(e.target.parent.gbId) not in self.tempWoman:
                self.tempWoman.append(int(e.target.parent.gbId))
            else:
                p.showGameMsg(GMDD.data.MARRIAGE_INVITE_WOMAN_FULL, ())
            self.refreshInfo()

    def handleSearchFriendChange(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            self.refreshRightList()

    def handleLeftItemRollOver(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.currentTarget
            t.removeBtn.visible = True

    def handleLeftItemRollOut(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.currentTarget
            t.removeBtn.visible = False

    def handleRemoveClick(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.target
            if int(t.parent.gbId) in self.tempMan:
                self.tempMan.remove(int(t.parent.gbId))
            if int(t.parent.gbId) in self.tempWoman:
                self.tempWoman.remove(int(t.parent.gbId))
            self.refreshInfo()

    def handleSaveBtnClick(self, *arg):
        p = BigWorld.player()
        addBridesmaidServerList = []
        addBridesmaidList = []
        delBridesmaidList = []
        addBestmanServerList = []
        addBestmanList = []
        delBestmanList = []
        manMap, womanMap = self.uiAdapter.marrySettingBg.getCurServerManAndWomanMap()
        for item in self.tempMan:
            if item not in manMap.keys():
                addBestmanList.append(item)
                fVal = self.getFriendInfo(item)
                addBestmanServerList.append(fVal.get('serverId', 0))

        for item in self.tempWoman:
            if item not in womanMap.keys():
                addBridesmaidList.append(item)
                fVal = self.getFriendInfo(item)
                addBridesmaidServerList.append(fVal.get('serverId', 0))

        delBestmanList = list(set(manMap.keys()) - set(self.tempMan))
        delBridesmaidList = list(set(womanMap.keys()) - set(self.tempWoman))
        _msg = MCD.data.get('marriageInviteConfirm', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(_msg, yesCallback=Functor(p.cell.setMarriageMaids, addBridesmaidServerList, addBridesmaidList, delBridesmaidList, addBestmanServerList, addBestmanList, delBestmanList), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)

    def getLimitNum(self):
        mType, subType = self.uiAdapter.marrySettingBg.getCurServerMarriageType()
        maxMaidCount = MPD.data.get((mType, subType)).get('maxMaidCount', 0)
        return maxMaidCount

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
        p = BigWorld.player()
        for k, fVal in p.friend.iteritems():
            if fVal.acknowledge and fVal.gbId not in self.tempMan and fVal.gbId not in self.tempWoman and fVal.gbId not in member:
                if searchName:
                    if uiUtils.filterPinYin(searchName, fVal.name):
                        rightGuest.append(fVal.gbId)
                else:
                    rightGuest.append(fVal.gbId)

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
