#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/personalZoneFriendProxy.o
import math
import BigWorld
from Scaleform import GfxValue
import gametypes
import gameglobal
import events
import utils
import const
import ui
import gameconfigCommon
import uiConst
from guis import uiUtils
from asObject import ASObject
from asObject import TipManager
from asObject import ASUtils
from callbackHelper import Functor
from helpers import pyq_interface
from gamestrings import gameStrings
from uiTab2Proxy import UITab2Proxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import personal_zone_config_data as PZCD
TAB_FRIENDS_IDX = 0
TAB_HOTSPOT_IDX = 1
TAB_YUNCHUI_FUN_IDX = 2
HOTSPOT_CUR_SERVER = 0
HOTSPOT_ALL_SERVER = 1
SHOW_MY_MOMENT = 1
SHOW_FRIEND_MOMENT = 2
OP_GET_HOME_MOMENTS_INIT = 1
OP_GET_HOME_MOMENTS_REFRESH_PAGE = 2
OP_GET_MY_MOMENTS_INIT = 3
OP_GET_MY_MOMENTS_REFRESH_PAGE = 4
OP_GET_CUR_SERVER_MOMENTS_INIT = 5
OP_GET_ALL_SERVER_MOMENTS_INIT = 6
OP_GET_CUR_SERVER_MOMENTS_REFRESH_PAGE = 7
OP_GET_ALL_SERVER_MOMENTS_REFRESH_PAGE = 8
OP_GET_TOPIC_MOMENTS_INIT = 9
OP_GET_TOPIC_MOMENTS_REFRESH_PAGE = 10
OP_FOLLOW_PYQ_OWNER = 11
OP_FOLLOW_MOMENT_USER = 12

class PersonalZoneFriendProxy(UITab2Proxy):

    def __init__(self, uiAdapter):
        super(PersonalZoneFriendProxy, self).__init__(uiAdapter)
        self.widget = None
        self.sortMenuData = [{'label': gameStrings.PERSONAL_ZONE_SORT_HOT_TXT,
          'data': 0,
          'sortType': 'hot'},
         {'label': gameStrings.PERSONAL_ZONE_SORT_NEW_TXT,
          'data': 0,
          'sortType': 'new'},
         {'label': gameStrings.PERSONAL_ZONE_SORT_IMAGE_TXT,
          'data': 0,
          'sortType': 'image'},
         {'label': gameStrings.PERSONAL_ZONE_SORT_FOLLOW_TXT,
          'data': 0,
          'sortType': 'follow'},
         {'label': gameStrings.PERSONAL_ZONE_SORT_CURSERVER_TXT,
          'data': 0,
          'sortType': 'cur_server'}]
        self.reset()

    @property
    def baseInfo(self):
        return self.uiAdapter.personalZoneSystem.baseInfo

    @property
    def isFollowing(self):
        return self.uiAdapter.personalZoneSystem.isFollowing

    @property
    def homeMomentsInfo(self):
        return self.curMomentsInfo

    @homeMomentsInfo.setter
    def homeMomentsInfo(self, value):
        self.curMomentsInfo = value

    @property
    def userMomentsInfo(self):
        return self.curMomentsInfo

    @userMomentsInfo.setter
    def userMomentsInfo(self, value):
        self.curMomentsInfo = value

    @property
    def serverHotspotInfo(self):
        return self.curMomentsInfo

    @serverHotspotInfo.setter
    def serverHotspotInfo(self, value):
        self.curMomentsInfo = value

    @baseInfo.setter
    def baseInfo(self, value):
        self.uiAdapter.personalZoneSystem.baseInfo = value

    def reset(self):
        self.showType = SHOW_MY_MOMENT
        self.curHotspotType = HOTSPOT_CUR_SERVER
        self.curMomentsInfo = {}

    def initPanel(self, widget):
        super(PersonalZoneFriendProxy, self).initPanel(widget)
        self.initUI()

    def unRegisterPanel(self):
        super(PersonalZoneFriendProxy, self).unRegisterPanel()
        self.widget = None
        self.reset()

    @property
    def baseInfo(self):
        return self.uiAdapter.personalZoneSystem.baseInfo

    @property
    def ownerGbID(self):
        return self.uiAdapter.personalZoneSystem.ownerGbID

    @property
    def hostId(self):
        return self.uiAdapter.personalZoneSystem.hostId

    def initUI(self):
        self.getNewsList()
        self.widget.emptyDesc.visible = False
        self.widget.myMoment.visible = False
        self.initCommonLayer()
        if self.isSelfZone():
            self.showLayer(SHOW_FRIEND_MOMENT, TAB_FRIENDS_IDX)
        else:
            self.showLayer(SHOW_MY_MOMENT, 0)
        self.uiAdapter.personalZoneSystem.initMainMc(self.widget.mainMc)
        self.setMainMc(self.widget.mainMc)
        self.setFuDaiIcon()

    def onTabChanged(self, newView, newTabIdx):
        super(PersonalZoneFriendProxy, self).onTabChanged(newView, newTabIdx)
        self.widget.setChildIndex(self.widget.commonLayer, 0)

    def showLayer(self, showType, subIndex):
        if not self.hasBaseData():
            return
        self.showType = showType
        if self.isSelfZone():
            if showType == SHOW_FRIEND_MOMENT:
                self.unRegisterMymomentsLayer()
                for tabInfo in self.tabList:
                    btn = getattr(self.widget, tabInfo['btnName'])
                    btn.visible = True

                self.widget.tabBtn2.visible = gameconfigCommon.enablePYQTopic()
                if self.currentView:
                    self.currentView.visible = True
                if subIndex == self.currentTabIdx:
                    self.initSubPanel(self.currentView)
                else:
                    self.selectSubTab(subIndex)
                self.widget.commonLayer.friendPyqBtn.label = gameStrings.PERSONAL_ZONE_MY_MOMENT_BTN_TXT
            elif showType == SHOW_MY_MOMENT:
                for tabInfo in self.tabList:
                    btn = getattr(self.widget, tabInfo['btnName'])
                    btn.visible = False

                if self.currentView:
                    self.currentView.visible = False
                self.initMymomentsLayer()
                self.widget.commonLayer.friendPyqBtn.label = gameStrings.PERSONAL_ZONE_FRIEND_MOMENT_BTN_TXT
        else:
            for tabInfo in self.tabList:
                btn = getattr(self.widget, tabInfo['btnName'])
                btn.visible = False

            if self.currentView:
                self.currentView.visible = False
            self.initMymomentsLayer()
            self.widget.commonLayer.friendPyqBtn.label = gameStrings.PERSONAL_ZONE_MY_MOMENT_BTN_TXT

    def refreshInfo(self):
        if not self.widget:
            return

    def refreshCurPageMoments(self, pageCount = 0):
        if not self.hasBaseData():
            return
        self.widget.emptyDesc.visible = False
        if self.showType == SHOW_FRIEND_MOMENT:
            if not pageCount:
                pageCount = self.currentView.pageCounter.count
            if self.currentTabIdx == TAB_FRIENDS_IDX:
                self.getHomeMoments(OP_GET_HOME_MOMENTS_INIT, pageCount)
            elif self.currentTabIdx == TAB_HOTSPOT_IDX:
                if self.curHotspotType == HOTSPOT_CUR_SERVER:
                    self.getCurServerMoments(OP_GET_CUR_SERVER_MOMENTS_REFRESH_PAGE, pageCount)
                elif self.curHotspotType == HOTSPOT_ALL_SERVER:
                    self.getAllServerMoments(OP_GET_ALL_SERVER_MOMENTS_REFRESH_PAGE, pageCount)
            elif self.currentTabIdx == TAB_YUNCHUI_FUN_IDX:
                sort = self.getCurTopicSort()
                topicId = self.getTopTopicId()
                serverId = 0
                if sort == 'cur_server':
                    serverId = self.uiAdapter.personalZoneSystem.getHostId()
                self.getTopicMoments(OP_GET_TOPIC_MOMENTS_REFRESH_PAGE, topicId, sort, pageCount, serverId=serverId)
        elif self.showType == SHOW_MY_MOMENT:
            if not pageCount:
                pageCount = self.widget.myMoment.pageCounter.count
            self.getUserMoments(OP_GET_MY_MOMENTS_REFRESH_PAGE, self.ownerGbID, pageCount)

    def _getTabList(self):
        return [{'tabIdx': TAB_FRIENDS_IDX,
          'btnName': 'tabBtn0',
          'clsName': 'PersonalZoneFriend_Friends',
          'pos': (35, 38)}, {'tabIdx': TAB_HOTSPOT_IDX,
          'btnName': 'tabBtn1',
          'clsName': 'PersonalZoneFriend_Hotspot',
          'pos': (35, 38)}, {'tabIdx': TAB_YUNCHUI_FUN_IDX,
          'btnName': 'tabBtn2',
          'clsName': 'PersonalZoneFriend_YunchuiFun',
          'pos': (29, 58)}]

    def initSubPanel(self, currentView):
        super(PersonalZoneFriendProxy, self).initSubPanel(currentView)
        self.widget.emptyDesc.visible = False
        if self.currentTabIdx == TAB_FRIENDS_IDX:
            self.initFriendLayer()
        elif self.currentTabIdx == TAB_HOTSPOT_IDX:
            self.initHotspotLayer()
        elif self.currentTabIdx == TAB_YUNCHUI_FUN_IDX:
            self.initYunchuiFunLayer()

    def initCommonLayer(self):
        self.widget.commonLayer.freshBtn.visible = True
        self.widget.commonLayer.friendPyqBtn.visible = True
        if self.isSelfZone():
            self.widget.commonLayer.addMomentBtn.visible = True
            self.widget.commonLayer.giftBtn.visible = False
            self.widget.commonLayer.msgBtn.visible = True
            self.widget.commonLayer.vistorListBtn.visible = True
            self.widget.commonLayer.followListBtn.visible = True
        else:
            self.widget.commonLayer.msgBtn.visible = False
            self.widget.commonLayer.addMomentBtn.visible = False
            self.widget.commonLayer.giftBtn.visible = True
            self.widget.commonLayer.vistorListBtn.visible = False
            self.widget.commonLayer.followListBtn.visible = False
        self.refreshFollowBtn()
        self.widget.commonLayer.giftBtn.gbId = self.ownerGbID
        self.widget.commonLayer.giftBtn.hostId = self.hostId
        self.widget.commonLayer.giftBtn.roleName = self.baseInfo.get('roleName', '')
        self.widget.commonLayer.followBtn.gbId = self.ownerGbID
        self.widget.commonLayer.followBtn.addEventListener(events.BUTTON_CLICK, self.handleFollowBtn, False, 0, True)
        self.widget.commonLayer.giftBtn.addEventListener(events.BUTTON_CLICK, self.handleGiftBtn, False, 0, True)
        self.widget.commonLayer.freshBtn.addEventListener(events.BUTTON_CLICK, self.handleFreshBtn, False, 0, True)
        self.widget.commonLayer.vistorListBtn.addEventListener(events.BUTTON_CLICK, self.handleVistorListBtn, False, 0, True)
        self.widget.commonLayer.msgBtn.addEventListener(events.BUTTON_CLICK, self.handleMsgBtn, False, 0, True)
        self.widget.commonLayer.addMomentBtn.addEventListener(events.BUTTON_CLICK, self.handleAddMomentBtn, False, 0, True)
        self.widget.commonLayer.followListBtn.addEventListener(events.BUTTON_CLICK, self.handleFollowListBtn, False, 0, True)
        self.widget.commonLayer.friendPyqBtn.addEventListener(events.BUTTON_CLICK, self.handleFriendPyqBtn, False, 0, True)
        if not gameconfigCommon.enableNewPYQ():
            self.widget.commonLayer.vistorListBtn.visible = False
            self.widget.commonLayer.followListBtn.visible = False

    def initFriendLayer(self):
        self.currentView.mainMc.visible = False
        self.widget.mainMc.visible = True
        self.uiAdapter.personalZoneSystem.initMainMc(self.widget.mainMc)
        self.setMainMc(self.widget.mainMc)
        self.currentView.momentsList.itemRenderer = 'PersonalZoneFriend_PYQ_Item'
        self.currentView.momentsList.labelFunction = self.momentsItemFunc
        self.currentView.momentsList.itemHeightFunction = self.momentsItemHeightFunction
        self.currentView.momentsList.dataArray = []
        self.currentView.pageCounter.enableMouseWheel = False
        self.currentView.pageCounter.count = 1
        self.currentView.pageCounter.minCount = 1
        self.currentView.pageCounter.addEventListener(events.EVENT_COUNT_CHANGE, self.handlePageChange, False, 0, True)
        self.getHomeMoments(OP_GET_HOME_MOMENTS_INIT, 1)

    def initHotspotLayer(self):
        self.curHotspotType = HOTSPOT_ALL_SERVER
        self.currentView.mainMc.visible = False
        self.widget.mainMc.visible = True
        self.uiAdapter.personalZoneSystem.initMainMc(self.widget.mainMc)
        self.setMainMc(self.widget.mainMc)
        self.currentView.curServerBtn.groupName = 'hotspotTab'
        self.currentView.allServerBtn.groupName = 'hotspotTab'
        self.currentView.momentsList.itemRenderer = 'PersonalZoneFriend_PYQ_Item'
        self.currentView.momentsList.labelFunction = self.momentsItemFunc
        self.currentView.momentsList.itemHeightFunction = self.momentsItemHeightFunction
        self.currentView.momentsList.dataArray = []
        self.currentView.pageCounter.enableMouseWheel = False
        self.currentView.pageCounter.count = 1
        self.currentView.pageCounter.minCount = 1
        self.currentView.pageCounter.addEventListener(events.EVENT_COUNT_CHANGE, self.handlePageChange, False, 0, True)
        self.currentView.curServerBtn.addEventListener(events.BUTTON_CLICK, self.handleCurServerBtn, False, 0, True)
        self.currentView.allServerBtn.addEventListener(events.BUTTON_CLICK, self.handleAllServerBtn, False, 0, True)
        if self.curHotspotType == HOTSPOT_CUR_SERVER:
            self.currentView.curServerBtn.selected = True
            self.getCurServerMoments(OP_GET_CUR_SERVER_MOMENTS_INIT, 1)
        elif self.curHotspotType == HOTSPOT_ALL_SERVER:
            self.currentView.allServerBtn.selected = True
            self.getAllServerMoments(OP_GET_ALL_SERVER_MOMENTS_INIT, 1)

    def initYunchuiFunLayer(self):
        self.widget.mainMc.visible = False
        ASUtils.setDropdownMenuData(self.currentView.sortMenu, self.sortMenuData)
        self.currentView.sortMenu.selectedIndex = 0
        self.currentView.sortMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleSortMenuItemSelected, False, 0, True)
        self.currentView.sortMenu.validateNow()
        p = BigWorld.player()
        self.currentView.topicList.listMc.itemRenderer = 'PersonalZoneFriend_TopicItem'
        self.currentView.topicList.listMc.itemHeight = 196
        self.currentView.topicList.listMc.labelFunction = self.topicItemFunc
        self.currentView.topicList.listMc.itemHeightFunction = self.topicItemHeightFunc
        self.currentView.topicList.listMc.dataArray = p.topicList
        self.currentView.topicList.listMc.validateNow()
        self.currentView.momentsList.itemRenderer = 'PersonalZoneFriend_PYQ_Item'
        self.currentView.momentsList.labelFunction = self.momentsItemFunc
        self.currentView.momentsList.itemHeightFunction = self.momentsItemHeightFunction
        self.currentView.momentsList.dataArray = []
        self.currentView.pageCounter.enableMouseWheel = False
        self.currentView.pageCounter.count = 1
        self.currentView.pageCounter.minCount = 1
        self.currentView.pageCounter.addEventListener(events.EVENT_COUNT_CHANGE, self.handlePageChange, False, 0, True)
        sort = self.getCurTopicSort()
        topicId = self.getTopTopicId()
        self.getTopicMoments(OP_GET_TOPIC_MOMENTS_INIT, topicId, sort, 1)

    def getCurTopicSort(self):
        if self.showType == SHOW_FRIEND_MOMENT:
            if self.currentTabIdx == TAB_YUNCHUI_FUN_IDX:
                dataIndex = self.currentView.sortMenu.selectedIndex
                if dataIndex < len(self.sortMenuData):
                    return self.sortMenuData[dataIndex].get('sortType', 'hot')
        return 'hot'

    def initMymomentsLayer(self):
        self.widget.emptyDesc.visible = False
        self.widget.myMoment.visible = True
        self.widget.myMoment.mainMc.visible = False
        self.widget.mainMc.visible = True
        self.uiAdapter.personalZoneSystem.initMainMc(self.widget.mainMc)
        self.setMainMc(self.widget.mainMc)
        self.widget.myMoment.momentsList.itemRenderer = 'PersonalZoneFriend_PYQ_Item'
        self.widget.myMoment.momentsList.labelFunction = self.momentsItemFunc
        self.widget.myMoment.momentsList.itemHeightFunction = self.momentsItemHeightFunction
        self.widget.myMoment.momentsList.dataArray = []
        self.widget.myMoment.pageCounter.enableMouseWheel = False
        self.widget.myMoment.pageCounter.count = 1
        self.widget.myMoment.pageCounter.minCount = 1
        self.widget.myMoment.pageCounter.addEventListener(events.EVENT_COUNT_CHANGE, self.handlePageChange, False, 0, True)
        self.getUserMoments(OP_GET_MY_MOMENTS_INIT, self.ownerGbID, 1)

    def unRegisterMymomentsLayer(self):
        self.widget.myMoment.visible = False

    def unRegisterSubPanel(self):
        super(PersonalZoneFriendProxy, self).unRegisterSubPanel()
        if self.currentTabIdx == TAB_FRIENDS_IDX:
            pass
        elif self.currentTabIdx == TAB_HOTSPOT_IDX:
            pass
        elif self.currentTabIdx == TAB_YUNCHUI_FUN_IDX:
            pass

    def setMainMc(self, mc):
        if not self.hasBaseData():
            return
        self.uiAdapter.personalZoneSystem.setMainMc(mc)

    def getMainMc(self):
        return self.widget.mainMc

    def freshTagsAddOne(self, src, new):
        pass

    def setUpdateInfo(self, needAdjustTag = False):
        if self.widget:
            mainMc = self.getMainMc()
            if mainMc:
                self.setMainMc(mainMc)
            self.setFuDaiIcon()

    def isSelfZone(self):
        return self.uiAdapter.personalZoneSystem.isSelfZone()

    def refreshFollowBtn(self):
        if not self.hasBaseData():
            return
        self.widget.commonLayer.followBtn.visible = False
        if not self.isSelfZone() and self.isFollowing != -1:
            self.widget.commonLayer.followBtn.visible = True
            if not self.isFollowing:
                self.widget.commonLayer.followBtn.label = gameStrings.PERSONAL_ZONE_FOLLOW_ADD_TXT
            else:
                self.widget.commonLayer.followBtn.label = gameStrings.PERSONAL_ZONE_FOLLOW_CANCEL_TXT

    def getHomeMoments(self, op, page):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onGetHomeMoments(rStatus, content, op, page)

        pyq_interface.getHomeMoments(_callBack, page)

    def onGetHomeMoments(self, rStatus, content, opType, page):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            if self.showType == SHOW_FRIEND_MOMENT:
                if self.currentTabIdx == TAB_FRIENDS_IDX:
                    if opType == OP_GET_HOME_MOMENTS_INIT:
                        self.setMomentListInfo(self.currentView.momentsList, self.currentView.pageCounter, self.homeMomentsInfo, content)
                    elif opType == OP_GET_HOME_MOMENTS_REFRESH_PAGE:
                        if page == self.currentView.pageCounter.count:
                            self.setMomentListInfo(self.currentView.momentsList, self.currentView.pageCounter, self.homeMomentsInfo, content)

    def getNewsList(self):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onGetNewsList(rStatus, content)

        pyq_interface.getNewsList(_callBack, 1, const.PERSONAL_ZONE_NEWS_PAGE_SIZE)

    def onGetNewsList(self, rStatus, content):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            p = BigWorld.player()
            p.getPyqNewNum()

    def getUserMoments(self, op, gbId, page):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onGetUserMoments(rStatus, content, op, page)

        pyq_interface.getUserMoments(_callBack, gbId, page)

    def onGetUserMoments(self, rStatus, content, opType, page):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            if self.showType == SHOW_MY_MOMENT:
                if opType == OP_GET_MY_MOMENTS_INIT:
                    self.setMomentListInfo(self.widget.myMoment.momentsList, self.widget.myMoment.pageCounter, self.userMomentsInfo, content)
                elif opType == OP_GET_MY_MOMENTS_REFRESH_PAGE:
                    if page == self.widget.myMoment.pageCounter.count:
                        self.setMomentListInfo(self.widget.myMoment.momentsList, self.widget.myMoment.pageCounter, self.userMomentsInfo, content)

    def getCurServerMoments(self, op, page):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onGetCurServerMoments(rStatus, content, op, page)

        pyq_interface.getCurServerHotMoments(_callBack, self.uiAdapter.personalZoneSystem.getHostId(), page)

    def onGetCurServerMoments(self, rStatus, content, opType, page):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            if self.showType == SHOW_FRIEND_MOMENT:
                if self.currentTabIdx == TAB_HOTSPOT_IDX:
                    if opType == OP_GET_CUR_SERVER_MOMENTS_INIT:
                        self.setMomentListInfo(self.currentView.momentsList, self.currentView.pageCounter, self.serverHotspotInfo, content)
                    elif opType == OP_GET_CUR_SERVER_MOMENTS_REFRESH_PAGE:
                        if page == self.currentView.pageCounter.count:
                            self.setMomentListInfo(self.currentView.momentsList, self.currentView.pageCounter, self.serverHotspotInfo, content)

    def getAllServerMoments(self, op, page):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onGetAllServerMoments(rStatus, content, op, page)

        pyq_interface.getAllServerHotMoments(_callBack, page)

    def onGetAllServerMoments(self, rStatus, content, opType, page):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            if self.showType == SHOW_FRIEND_MOMENT:
                if self.currentTabIdx == TAB_HOTSPOT_IDX:
                    if opType == OP_GET_ALL_SERVER_MOMENTS_INIT:
                        self.setMomentListInfo(self.currentView.momentsList, self.currentView.pageCounter, self.serverHotspotInfo, content)
                    elif opType == OP_GET_ALL_SERVER_MOMENTS_REFRESH_PAGE:
                        if page == self.currentView.pageCounter.count:
                            self.setMomentListInfo(self.currentView.momentsList, self.currentView.pageCounter, self.serverHotspotInfo, content)

    def getTopicMoments(self, op, topicId, sortType, page, serverId = 0):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onGetTopicMoments(rStatus, content, op, page)

        pyq_interface.getTopicMoments(_callBack, topicId, sortType, page, serverId)

    def onGetTopicMoments(self, rStatus, content, opType, page):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            if self.showType == SHOW_FRIEND_MOMENT:
                if self.currentTabIdx == TAB_YUNCHUI_FUN_IDX:
                    if opType == OP_GET_TOPIC_MOMENTS_INIT:
                        self.setMomentListInfo(self.currentView.momentsList, self.currentView.pageCounter, self.serverHotspotInfo, content)
                    elif opType == OP_GET_TOPIC_MOMENTS_REFRESH_PAGE:
                        if page == self.currentView.pageCounter.count:
                            self.setMomentListInfo(self.currentView.momentsList, self.currentView.pageCounter, self.serverHotspotInfo, content)

    def likeMoments(self, momentId, action, topicId, logInfo):
        p = BigWorld.player()
        logInfo['momentId'] = momentId

        def _callBack(rStatus, content):
            self.onLikeMoments(rStatus, content, logInfo)

        pyq_interface.likeMoments(_callBack, momentId, action)

    def onLikeMoments(self, rStatus, content, logInfo):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        p = BigWorld.player()
        if not content.get('code', 0):
            commentId = content.get('date', {}).get('id', 0)
            self.refreshCurPageMoments()
            self.uiAdapter.personalZoneMoment.refreshMoments()
            gbId = logInfo.get('gbId', 0)
            hostId = logInfo.get('hostId', 0)
            momentId = logInfo.get('momentId', 0)
            topicId = logInfo.get('topicId', 0)
            p.base.genPyqOpLog(gametypes.PERSONAL_ZONE_PYQ_OP_LIKE_MOMENT, int(gbId), int(momentId), int(commentId))
            p.base.operateMoment(int(gbId), int(hostId), gametypes.PYQ_OP_TYPE_LIKE, int(momentId), int(topicId))
        else:
            p.showGameMsg(GMDD.data.PERSONAL_ZONE_MOMENT_DELETED_TIPS, ())

    def delMoments(self, momentId, logInfo):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onDelMoments(rStatus, content, momentId, logInfo)

        func = Functor(pyq_interface.delMoments, _callBack, momentId)
        self.uiAdapter.messageBox.showYesNoMsgBox(gameStrings.PERSONAL_ZONE_MOMENT_DELETE_TXT, func)

    def onDelMoments(self, rStatus, content, momentId, logInfo):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            self.refreshCurPageMoments()
            if momentId == self.uiAdapter.personalZoneMoment.getMomentId():
                self.uiAdapter.personalZoneMoment.hide()
            likeNum = logInfo.get('likeNum', 0)
            commentNum = logInfo.get('commentNum', 0)
            forwardNum = logInfo.get('forwardNum', 0)
            topicId = logInfo.get('topicId', 0)
            srcId = logInfo.get('srcId', 0)
            hasGraph = logInfo.get('hasGraph', 0)
            p = BigWorld.player()
            p.base.genPyqMomentLog(gametypes.PERSONAL_ZONE_PYQ_OP_DEL_MOMENT, momentId, likeNum, commentNum, forwardNum, topicId, srcId, hasGraph)

    def delComment(self, commentId, logInfo):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onDelComment(rStatus, content, commentId, logInfo)

        func = Functor(pyq_interface.delComment, _callBack, commentId)
        self.uiAdapter.messageBox.showYesNoMsgBox(gameStrings.PERSONAL_ZONE_COMMENT_DELETE_TXT, func)

    def onDelComment(self, rStatus, content, commentId, logInfo):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            self.refreshCurPageMoments()
            self.uiAdapter.personalZoneMoment.refreshMomentData()
            gbId = logInfo.get('gbId', 0)
            momentId = logInfo.get('momentId', 0)
            p = BigWorld.player()
            p.base.genPyqOpLog(gametypes.PERSONAL_ZONE_PYQ_OP_DEL_COMMENT, int(gbId), int(momentId), int(commentId))

    def addFollow(self, gbId, op):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onAddFollow(rStatus, content, op)

        pyq_interface.addFollow(_callBack, gbId)

    def onAddFollow(self, rStatus, content, op):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            self.refreshCurPageMoments()
            self.uiAdapter.personalZoneSystem.getProfile(self.ownerGbID)
            self.uiAdapter.personalZoneMoment.refreshMomentData()

    def cancelFollow(self, gbId):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onCancelFollow(rStatus, content)

        pyq_interface.cancelFollow(_callBack, gbId)

    def onCancelFollow(self, rStatus, content):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            self.refreshCurPageMoments()
            self.uiAdapter.personalZoneSystem.getProfile(self.ownerGbID)
            self.uiAdapter.personalZoneMoment.refreshMomentData()

    def setMomentListInfo(self, mList, counter, mInfo, content):
        data = content.get('data', {})
        mInfo.update(data)
        listData = mInfo.get('list', [])
        self.setMomentsListData(mList, listData)
        count = mInfo.get('count', 0)
        self.setCounterData(counter, count)

    def setMomentsListData(self, listMc, listData):
        if not self.hasBaseData():
            return
        listMc.dataArray = [ {'index': i,
         'mId': v.get('id')} for i, v in enumerate(listData) ]
        listMc.validateNow()
        if not len(listMc.dataArray):
            self.widget.emptyDesc.visible = True

    def setCounterData(self, counterMc, count):
        if not counterMc:
            return
        counterMc.maxCount = max(math.ceil(count * 1.0 / const.PERSONAL_ZONE_MOMENTS_NUM_PER_PAGE), 1)

    def topicItemFunc(self, *arg):
        if not self.hasBaseData():
            return 0
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            self.setTopicItem(itemMc, info)

    def setTopicItem(self, itemMc, info):
        msg = uiUtils.toHtml(gameStrings.PERSONAL_ZONE_TOPIC_FORMAT_TXT % (info.name,), info.nameColor)
        itemMc.nameTxt.htmlText = msg
        itemMc.desc.text = info.desc
        itemMc.desc.height = itemMc.desc.textHeight + 5
        itemMc.bannerImg.fitSize = True
        itemMc.bannerImg.url = info.banner
        itemMc.applyBtn.data = info.id
        itemMc.applyBtn.addEventListener(events.BUTTON_CLICK, self.handleTopicApplyBtn, False, 0, True)
        itemMc.topicBg.height = itemMc.desc.textHeight + 50
        itemMc.applyBtn.y = itemMc.desc.y + itemMc.desc.textHeight + 10

    def topicItemHeightFunc(self, *arg):
        if not self.hasBaseData():
            return 0
        info = ASObject(arg[3][0])
        itemMc = self.widget.getInstByClsName('PersonalZoneFriend_TopicItem')
        self.setTopicItem(itemMc, info)
        return GfxValue(itemMc.height)

    def momentsItemFunc(self, *arg):
        if not self.hasBaseData():
            return 0
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            listData = self.curMomentsInfo.get('list', [])
            if listData and info.index < len(listData):
                data = listData[info.index]
                gbId = int(data.get('roleId', 0))
                roleName = data.get('roleName', '')
                p = BigWorld.player()
                data['clientDataIndex'] = info.index
                self.setMomentsItem(itemMc, data)

    def momentsItemHeightFunction(self, *arg):
        if not self.hasBaseData():
            return GfxValue(0)
        info = ASObject(arg[3][0])
        height = 0
        listData = []
        if self.showType == SHOW_FRIEND_MOMENT:
            listData = self.homeMomentsInfo.get('list', [])
        elif self.showType == SHOW_MY_MOMENT:
            listData = self.userMomentsInfo.get('list', [])
        if listData and info.index < len(listData):
            data = listData[info.index]
            mItem = self.widget.getInstByClsName('PersonalZoneFriend_PYQ_Item')
            mItem.index = info.index
            data['clientDataIndex'] = info.index
            if mItem:
                height = self.setMomentsItem(mItem, data)
        return GfxValue(height)

    def setMomentsItem(self, item, data):
        if not self.hasBaseData():
            return 0
        else:
            item.addEventListener(events.MOUSE_ROLL_OVER, self.handleItemRollOver, False, 0, True)
            item.addEventListener(events.MOUSE_ROLL_OUT, self.handleItemRollOut, False, 0, True)
            self.widget.removeAllInst(item, False)
            p = BigWorld.player()
            momentsGbId = int(data.get('roleId', 0))
            height = 8
            posY = 0
            isSelf = False
            if momentsGbId == p.gbId:
                isSelf = True
            item.momentsGbId = momentsGbId
            item.isSelf = isSelf
            hostId = data.get('serverId', 0)
            if not hostId:
                hostId = 0
            item.isCrossServer = hostId != utils.getHostId()
            momentBg = self.addMomentBg(item)
            headIcon = self.addHeadIcon(item, data)
            commonX = headIcon.x + headIcon.width
            nameTxt = self.addNameTxt(item, data, height, commonX)
            timeMc = self.addTimeMc(item, data, height)
            height = nameTxt.y + nameTxt.height
            reportBtn = self.addReportBtn(item, nameTxt, timeMc, data)
            descMc = self.addDescMc(item, data, height, commonX)
            height = descMc.y + descMc.richTxt.textFiled.textHeight
            imgList = data.get('forwardMoment', {}).get('imgList', [])
            if not imgList:
                imgList = data.get('imgList', [])
            self.addImgList(item, imgList, height, commonX, data)
            height += math.ceil(len(imgList) * 1.0 / 3) * 89
            delMomentBtn = self.addDelMomentBtn(item, data, height)
            operationMc = self.addOperationMc(item, data, height, commonX)
            height = operationMc.y + operationMc.height
            commentBg = self.widget.getInstByClsName('PersonalZoneFriend_CommentBg')
            commentBg.x = commonX
            commentBg.y = height + 5
            commentBg.width = 388
            commmentHeight = 0
            notShowComment = False
            if self.showType == SHOW_FRIEND_MOMENT:
                if self.currentTabIdx == TAB_HOTSPOT_IDX:
                    notShowComment = True
            likeListMc = None
            likeUsers = data.get('likeUsers', [])
            if likeUsers and not notShowComment:
                likeListMc = self.addLikeListMc(item, likeUsers, height, commonX)
                commmentHeight += likeListMc.height
                height = likeListMc.y + likeListMc.height
            commentMcList = []
            commentList = data.get('commentList', [])
            for commentInfo in commentList:
                if not notShowComment:
                    commentMc = self.addCommentMc(item, data, commentInfo, height, commonX)
                    commmentHeight = commentMc.y + commentMc.height - commentBg.y
                    height = commentMc.y + commentMc.height

            if (likeUsers or commentList) and not notShowComment:
                item.addChild(commentBg)
                item.setChildIndex(commentBg, 0)
            if commmentHeight:
                commentBg.alpha = 1
                commentBg.height = commmentHeight
                height = commentBg.y + commentBg.height
            dashLine = self.widget.getInstByClsName('PersonalZoneFriend_DashLine')
            dashLine.x = 0
            dashLine.y = height + 10
            dashLine.width = 443
            item.addChild(dashLine)
            height = dashLine.y + dashLine.height + 10
            momentBg.height = height
            return height

    def addMomentBg(self, item):
        momentBg = self.widget.getInstByClsName('PersonalZoneFriend_CommentBg')
        momentBg.x = 0
        momentBg.y = 0
        momentBg.width = 456
        momentBg.alpha = 0
        item.addChild(momentBg)
        return momentBg

    def addHeadIcon(self, item, data):
        headIcon = self.widget.getInstByClsName('PersonalZoneFriend_HeadIcon')
        headIcon.x = 0
        headIcon.y = 0
        item.addChild(headIcon)
        headIcon.leftFlag.visible = False
        headIcon.lvTxt.text = data.get('level', 0)
        roleName = data.get('roleName', '')
        if not roleName:
            roleName = ''
        gbId = data.get('roleId', 0)
        hostId = data.get('serverId', 0)
        if not hostId:
            hostId = 0
        headIcon.roleName = roleName
        headIcon.gbId = gbId
        headIcon.hostId = hostId
        headIcon.addEventListener(events.MOUSE_CLICK, self.handelHeadIconClick, False, 0, True)
        p = BigWorld.player()
        borderId = data.get('borderId', 1)
        if not borderId:
            borderId = SCD.data.get('defaultBorderId', 1)
        borderIcon = p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
        headIcon.headMc.borderImg.fitSize = True
        headIcon.headMc.borderImg.loadImage(borderIcon)
        headIcon.headMc.icon.setContentUnSee()
        headIcon.headMc.icon.fitSize = True
        headIcon.headMc.icon.serverId = hostId
        headIcon.headMc.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
        photo = data.get('photo', '')
        if not photo:
            school = data.get('jobId', 4)
            sex = data.get('gender', 1)
            photo = utils.getDefaultPhoto(school, sex)
            headIcon.headMc.icon.loadImage(photo)
        elif utils.isDownloadImage(photo):
            headIcon.headMc.icon.url = photo
        else:
            headIcon.headMc.icon.loadImage(photo)
        return headIcon

    def addNameTxt(self, item, data, height, commonX):
        nameTxt = self.widget.getInstByClsName('PersonalZoneFriend_NameTxtMc')
        nameTxt.name = 'nameTxt'
        nameTxt.x = commonX
        nameTxt.y = height
        item.addChild(nameTxt)
        roleName = data.get('roleName', '')
        if not roleName:
            roleName = ''
        gbId = data.get('roleId', 0)
        hostId = data.get('serverId', 0)
        if not hostId:
            hostId = 0
        roleName = uiUtils.getRoleNameWithSeverName(roleName, int(hostId))
        roleName = uiUtils.formatLinkZone(roleName, int(gbId), int(hostId), underLine=False)
        nameTxt.nameTxt.htmlText = roleName
        return nameTxt

    def addTimeMc(self, item, data, height):
        timeMc = self.widget.getInstByClsName('PersonalZoneFriend_TimeMc')
        timeMc.x = 386
        timeMc.y = height
        item.addChild(timeMc)
        time = data.get('createTime', 0) / 1000
        timeStr = utils.formatTimeAgo(time, fuzzyTime=60)
        timeMc.timeTxt.text = timeStr
        return timeMc

    def addReportBtn(self, item, nameTxt, timeMc, data):
        reportBtn = self.widget.getInstByClsName('PersonalZoneFriend_ReportBtn')
        reportBtn.name = 'reportBtn'
        reportBtn.x = timeMc.x - 18
        reportBtn.y = nameTxt.y + 4
        reportBtn.visible = False
        item.addChild(reportBtn)
        roleName = data.get('roleName', '')
        if not roleName:
            roleName = ''
        reportBtn.data = roleName
        reportBtn.addEventListener(events.BUTTON_CLICK, self.handleReportBtn, False, 0, True)
        return reportBtn

    def addDescMc(self, item, data, height, commonX):
        descMc = self.widget.getInstByClsName('PersonalZoneFriend_DescMc')
        descMc.name = 'descMc'
        descMsg = data.get('text', '')
        momentId = data.get('id', 0)
        previousForwards = data.get('previousForwards', [])
        forwardMoment = data.get('forwardMoment', {})
        if previousForwards or forwardMoment:
            descMsg += gameStrings.PERSONAL_ZONE_FORWARD_SIG_TXT
        for pfInfo in previousForwards:
            forwardText = pfInfo.get('text')
            roleInfo = pfInfo.get('roleinfo', {})
            pGbId = roleInfo.get('roleId', 0)
            pHostId = roleInfo.get('serverId', 0)
            roleName = roleInfo.get('roleName', '')
            if not roleName:
                roleName = ''
            roleName = uiUtils.getRoleNameWithSeverName(roleName, int(pHostId))
            forwardRoleName = gameStrings.PERSONAL_ZONE_AT_NAME_TXT + roleName
            descMsg += uiUtils.formatLinkZone(forwardRoleName, int(pGbId), int(pHostId)) + gameStrings.PERSONAL_ZONE_COLON_SIG_TXT + forwardText + gameStrings.PERSONAL_ZONE_FORWARD_SIG_TXT

        if forwardMoment:
            forwardMomentText = forwardMoment.get('text', '')
            pGbId = forwardMoment.get('roleId', 0)
            pHostId = forwardMoment.get('serverId', 0)
            roleName = forwardMoment.get('roleName', '')
            if not roleName:
                roleName = ''
            roleName = uiUtils.getRoleNameWithSeverName(roleName, int(pHostId))
            authorName = gameStrings.PERSONAL_ZONE_AT_NAME_TXT + roleName
            descMsg += uiUtils.formatLinkZone(authorName, int(pGbId), int(pHostId)) + gameStrings.PERSONAL_ZONE_COLON_SIG_TXT + forwardMomentText
        eventStr = 'shareMoment-%s' % (momentId,)
        descMsg = uiUtils.toHtml(descMsg, '#663517', eventStr, underLine=False)
        descMc.richTxt.text = ''
        descMc.richTxt.appandText(descMsg)
        descMc.richTxt.validateNow()
        descMc.x = commonX
        descMc.y = height
        descMc.richTxt.textFiled.height = descMc.richTxt.textFiled.textHeight + 10
        item.addChild(descMc)
        descMc.dataIndex = data.get('clientDataIndex', 0)
        return descMc

    def addImgList(self, item, imgList, height, commonX, data):
        imgHeight = 0
        forwardMoment = data.get('forwardMoment', {})
        isForward = bool(forwardMoment)
        hostId = 0
        if isForward:
            hostId = forwardMoment.get('serverId', 0)
        else:
            hostId = data.get('serverId', 0)
        for i, imgUrl in enumerate(imgList):
            imgMc = self.widget.getInstByClsName('PersonalZoneFriend_PicMc')
            imgMc.name = 'imgMc' + str(i)
            imgMc.icon.addEventListener(events.EVENT_LOAD_REMOTE_IMG_FAIL, self.handleImgLoadFailBtn, False, 0, True)
            imgMc.icon.addEventListener(events.EVENT_COMPLETE, self.handleImgLoadDone, False, 0, True)
            imgMc.x = commonX + i % 3 * (imgMc.icon.oriWidth + 3)
            imgMc.y = height + 10 + i / 3 * (imgMc.icon.oriHeight + 3)
            imgMc.gotoAndStop('zhaopian')
            item.addChild(imgMc)
            item.setChildIndex(imgMc, 0)
            imgMc.icon.scaleType = uiConst.SCALE_TYPE_FILL_FRAME
            imgMc.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
            imgMc.icon.serverId = hostId
            imgMc.icon.url = imgUrl.get('pic', '')
            imgMc.alpha = 1
            imgHeight = imgMc.icon.oriHeight
            imgMc.dataIndex = data.get('clientDataIndex', 0)
            imgMc.picIdx = i
            imgMc.canOpen = False
            touchImgMc = self.widget.getInstByClsName('PersonalZoneFriend_PicMc')
            touchImgMc.x = imgMc.x
            touchImgMc.y = imgMc.y
            touchImgMc.alpha = 0
            touchImgMc.relatedMc = imgMc
            item.addChild(touchImgMc)
            touchImgMc.addEventListener(events.MOUSE_CLICK, self.handleOpenPicture, False, 0, True)

    def addDelMomentBtn(self, item, data, height):
        momentId = data.get('id', 0)
        delMomentBtn = self.widget.getInstByClsName('PersonalZoneFriend_DelBtn')
        delMomentBtn.name = 'delMomentBtn'
        delMomentBtn.momentId = momentId
        likeCount = data.get('likeCount', 0)
        commentCount = data.get('commentCount', 0)
        forwardCount = data.get('forwardCount', 0)
        topicId = data.get('topicId', 0)
        momentId = data.get('momentId', 0)
        forwardMoment = data.get('forwardMoment', 0)
        impList = forwardMoment.get('imgList', [])
        previousForwards = data.get('previousForwards', [])
        lastForwardMomentId = 0
        if len(previousForwards):
            lastForwardMomentId = previousForwards[0].get('id', 0)
        if not lastForwardMomentId:
            lastForwardMomentId = momentId
        delMomentBtn.likeNum = likeCount
        delMomentBtn.commentNum = commentCount
        delMomentBtn.forwardNum = forwardCount
        delMomentBtn.topicId = topicId
        delMomentBtn.srcId = lastForwardMomentId
        delMomentBtn.hasGraph = bool(impList)
        delMomentBtn.x = 426
        delMomentBtn.y = height + 15
        delMomentBtn.visible = False
        delMomentBtn.addEventListener(events.BUTTON_CLICK, self.handleDelMomentBtn, False, 0, True)
        item.addChild(delMomentBtn)
        return delMomentBtn

    def addOperationMc(self, item, data, height, commonX):
        p = BigWorld.player()
        momentsGbId = int(data.get('roleId', 0))
        hostId = data.get('serverId', 0)
        roleName = data.get('roleName', '')
        momentId = data.get('id', 0)
        topicId = data.get('topicId', 0)
        clientDataIndex = data.get('clientDataIndex', 0)
        if not roleName:
            roleName = ''
        isSelf = False
        if momentsGbId == p.gbId:
            isSelf = True
        operationMc = self.widget.getInstByClsName('PersonalZoneFriend_OperationMc')
        operationMc.x = commonX
        operationMc.y = height + 10
        operationMc.transpondBtn.btn.momentId = momentId
        operationMc.transpondBtn.btn.clientDataIndex = clientDataIndex
        operationMc.transpondBtn.btn.addEventListener(events.BUTTON_CLICK, self.handleTranspondBtn, False, 0, True)
        forwardCount = data.get('forwardCount', 0)
        operationMc.transpondBtn.numTxt.text = forwardCount
        ASUtils.setHitTestDisable(operationMc.transpondBtn.numTxt, True)
        operationMc.commentBtn.btn.momentId = momentId
        operationMc.commentBtn.btn.clientDataIndex = clientDataIndex
        operationMc.commentBtn.btn.addEventListener(events.BUTTON_CLICK, self.handleCommentBtn, False, 0, True)
        commentCount = data.get('commentCount', 0)
        operationMc.commentBtn.numTxt.text = commentCount
        ASUtils.setHitTestDisable(operationMc.commentBtn.numTxt, True)
        isUserLiked = data.get('isUserLiked', 0)
        operationMc.likeBtn.btn.addEventListener(events.BUTTON_CLICK, self.handleLikeBtn, False, 0, True)
        operationMc.unlikeBtn.btn.addEventListener(events.BUTTON_CLICK, self.handleUnlikeBtn, False, 0, True)
        likeCount = data.get('likeCount', 0)
        operationMc.unlikeBtn.btn.momentId = momentId
        operationMc.likeBtn.btn.momentId = momentId
        operationMc.likeBtn.btn.topicId = topicId
        operationMc.likeBtn.btn.gbId = momentsGbId
        operationMc.likeBtn.btn.likeCount = likeCount
        operationMc.likeBtn.btn.hostId = hostId
        if isUserLiked:
            operationMc.unlikeBtn.visible = True
            operationMc.unlikeBtn.numTxt.text = likeCount
            ASUtils.setHitTestDisable(operationMc.unlikeBtn.numTxt, True)
            operationMc.likeBtn.visible = False
        else:
            operationMc.likeBtn.visible = True
            operationMc.likeBtn.numTxt.text = likeCount
            ASUtils.setHitTestDisable(operationMc.likeBtn.numTxt, True)
            operationMc.unlikeBtn.visible = False
        operationMc.giftBtn.visible = not isSelf
        operationMc.giftBtn.gbId = momentsGbId
        operationMc.giftBtn.hostId = hostId
        operationMc.giftBtn.roleName = roleName
        operationMc.giftBtn.addEventListener(events.BUTTON_CLICK, self.handleGiftBtn, False, 0, True)
        operationMc.followBtn.momentsGbId = momentsGbId
        operationMc.followBtn.addEventListener(events.BUTTON_CLICK, self.handleFollowBtn, False, 0, True)
        operationMc.followBtn.label = gameStrings.PERSONAL_ZONE_FOLLOW_TXT
        isFollowing = data.get('isFollowing', 0)
        operationMc.followBtn.visible = not isSelf and not isFollowing
        item.addChild(operationMc)
        return operationMc

    def addLikeListMc(self, item, likeUsers, height, commonX):
        likeListMc = self.widget.getInstByClsName('PersonalZoneFriend_LikeListMc')
        likeListMc.x = commonX
        likeListMc.y = height + 5
        likeListMc.likeUsersTxt.htmlText = ''
        item.addChild(likeListMc)
        likeUserStr = ''
        lastStr = ''
        for userInfo in likeUsers:
            gbId = int(userInfo.get('roleId', 0))
            hostId = userInfo.get('serverId', 0)
            if not hostId:
                hostId = 0
            roleName = userInfo.get('roleName', '')
            roleName = uiUtils.getRoleNameWithSeverName(roleName, int(hostId))
            userZoneLink = uiUtils.formatLinkZone(roleName, gbId=gbId, hostId=hostId)
            if likeUserStr:
                likeUserStr = gameStrings.PERSONAL_ZONE_COMMA_TXT.join((likeUserStr, userZoneLink))
            else:
                likeUserStr = ''.join((likeUserStr, userZoneLink))
            lastStr = likeUserStr

        if len(likeUsers) >= const.PERSONAL_ZONE_LIKE_USERS_SHOW_NUM:
            likeUserStr = likeUserStr + gameStrings.PERSONAL_ZONE_ETC_TXT
        likeListMc.likeUsersTxt.htmlText = likeUserStr
        likeListMc.likeUsersTxt.height = likeListMc.likeUsersTxt.textHeight + 5
        likeListMc.likeBg.height = likeListMc.likeUsersTxt.textHeight + 10
        return likeListMc

    def addCommentMc(self, item, data, commentInfo, height, commonX):
        roleName = commentInfo.get('roleName', '')
        if not roleName:
            roleName = ''
        momentId = data.get('id', 0)
        clientDataIndex = data.get('clientDataIndex', 0)
        commentText = commentInfo.get('text', '')
        gbId = int(commentInfo.get('roleId', 0))
        hostId = commentInfo.get('serverId', 0)
        if not hostId:
            hostId = 0
        commentId = commentInfo.get('id', 0)
        commentMc = self.widget.getInstByClsName('PersonalZoneFriend_CommentItem')
        commentMc.commentGbId = gbId
        commentMc.clientDataIndex = clientDataIndex
        commentMc.commentId = commentId
        commentMc.x = commonX + 5
        commentMc.y = height + 5
        roleNameEx = uiUtils.getRoleNameWithSeverName(roleName, int(hostId))
        commentMc.roleNameTxt.htmlText = ''
        roleNameStr = uiUtils.formatLinkZone(roleNameEx + gameStrings.PERSONAL_ZONE_COLON_SIG_TXT, gbId=gbId, hostId=hostId)
        commentMc.setChildIndex(commentMc.roleNameTxt, 0)
        commentMc.setChildIndex(commentMc.commentItemBg, 0)
        commentMc.commentTxt.x = commentMc.roleNameTxt.textWidth + 5
        commentMc.commentTxt.textFiled.width = 344 - commentMc.commentTxt.x
        commentMc.delBtn.momentId = momentId
        commentMc.delBtn.commentId = commentId
        commentMc.delBtn.gbId = gbId
        commentMc.delBtn.addEventListener(events.BUTTON_CLICK, self.handleCommentItemDel, False, 0, True)
        commentMc.delBtn.visible = False
        commentMc.reportBtn.data = roleName
        commentMc.reportBtn.addEventListener(events.BUTTON_CLICK, self.handleCommentItemReport, False, 0, True)
        commentMc.reportBtn.visible = False
        commentMc.isCrossServer = hostId != utils.getHostId()
        replyInfo = commentInfo.get('replyInfo', {})
        msg = roleNameStr
        if replyInfo:
            replyGbId = replyInfo.get('roleId', 0)
            if replyGbId:
                replyRoleName = replyInfo.get('roleName', '')
                replyServerId = replyInfo.get('serverId', 0)
                if not replyServerId:
                    replyServerId = 0
                replyRoleNameEx = uiUtils.getRoleNameWithSeverName(replyRoleName, int(replyServerId))
                msg += gameStrings.PERSONAL_ZONE_REPLY_TXT + uiUtils.formatPersonalZoneNameColor(replyRoleNameEx + gameStrings.PERSONAL_ZONE_COLON_SIG_TXT)
        msg += commentText
        commentMc.commentTxt.text = ''
        commentMc.commentTxt.appandText(msg)
        commentMc.commentTxt.validateNow()
        commentMc.commentTxt.textFiled.height = commentMc.commentTxt.textFiled.textHeight + 5
        commentMc.commentTxt.addEventListener(events.MOUSE_CLICK, self.handleReplyComment, False, 0, True)
        commentMc.dashLine.y = commentMc.commentTxt.y + commentMc.commentTxt.height + 5
        commentMc.commentItemBg.height = commentMc.dashLine.y + commentMc.dashLine.height
        commentMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleCommentItemRollOver, False, 0, True)
        commentMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleCommentItemRollOut, False, 0, True)
        item.addChild(commentMc)
        return commentMc

    def handleItemRollOver(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        if t.isSelf:
            t.delMomentBtn.visible = True
        elif not t.isCrossServer:
            t.reportBtn.visible = True

    def handleItemRollOut(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        if t.reportBtn and t.delMomentBtn:
            t.reportBtn.visible = False
            t.delMomentBtn.visible = False

    def handleCommentItemRollOver(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        p = BigWorld.player()
        if int(t.commentGbId) == int(p.gbId):
            t.delBtn.visible = True
        elif not t.isCrossServer:
            t.reportBtn.visible = True

    def handleCommentItemRollOut(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        t.reportBtn.visible = False
        t.delBtn.visible = False

    def handleDelMomentBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        logInfo = {'likeNum': t.likeNum,
         'commentNum': t.commentNum,
         'forwardNum': t.forwardNum,
         'topicId': t.topicId,
         'srcId': t.srcId,
         'hasGraph': t.hasGraph}
        self.delMoments(t.momentId, logInfo)

    def handleReportBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        gameglobal.rds.ui.prosecute.show(t.data, uiConst.MENU_PERSONAL_ZONE_PROSECUTE)

    def handleTranspondBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.openMoment(t.clientDataIndex, const.PERSONAL_ZONE_MOMENT_FORWARD)

    def handleCommentBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.openMoment(t.clientDataIndex, const.PERSONAL_ZONE_MOMENT_ADD_COMMENT)

    def handleLikeBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        logInfo = {'gbId': t.gbId,
         'momentId': t.momentId,
         'topicId': t.topicId,
         'likeCount': t.likeCount,
         'hostId': t.hostId}
        self.likeMoments(t.momentId, 'do', int(t.topicId), logInfo)

    def handleUnlikeBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target

    def handleFollowBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        opType = OP_FOLLOW_MOMENT_USER
        gbId = t.momentsGbId
        if not gbId:
            opType = OP_FOLLOW_PYQ_OWNER
            gbId = self.ownerGbID
        if self.isFollowing:
            self.cancelFollow(gbId)
        else:
            self.addFollow(gbId, opType)

    def handleGiftBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        gameglobal.rds.ui.spaceGiftGiving.show(t.gbId, t.roleName, t.hostId)

    def handlePageChange(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.refreshCurPageMoments(t.count)

    def handleCommentItemReport(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        gameglobal.rds.ui.prosecute.show(t.data, uiConst.MENU_PERSONAL_ZONE_PROSECUTE)

    def handleCommentItemDel(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        logInfo = {'momentId': t.momentId,
         'gbId': t.gbId}
        self.delComment(t.commentId, logInfo)

    def handleFreshBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.refreshCurPageMoments()

    def handleReplyComment(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        self.openMoment(t.parent.clientDataIndex, const.PERSONAL_ZONE_MOMENT_REPLY_COMMENT, t.parent.commentId)

    def handleVistorListBtn(self, *arg):
        if not self.hasBaseData():
            return
        self.uiAdapter.personalZoneVistor.show()

    def handleFollowListBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target

    def handleAddMomentBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.uiAdapter.personalZoneMood.show()

    def handleMsgBtn(self, *arg):
        if not self.hasBaseData():
            return
        gameglobal.rds.ui.personalZoneNews.show()

    def handleFollowListBtn(self, *arg):
        if not self.hasBaseData():
            return
        self.uiAdapter.personalZoneFocus.show()

    def handleFriendPyqBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        if self.isSelfZone():
            if self.showType == SHOW_FRIEND_MOMENT:
                self.showLayer(SHOW_MY_MOMENT, 0)
            elif self.showType == SHOW_MY_MOMENT:
                self.showLayer(SHOW_FRIEND_MOMENT, TAB_FRIENDS_IDX)
        else:
            self.uiAdapter.personalZoneDetail.openZoneMyself()

    def handleCurServerBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.curHotspotType = HOTSPOT_CUR_SERVER
        self.currentView.curServerBtn.selected = True
        self.refreshCurPageMoments()

    def handleAllServerBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.curHotspotType = HOTSPOT_ALL_SERVER
        self.currentView.allServerBtn.selected = True
        self.refreshCurPageMoments()

    def handleSortMenuItemSelected(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.refreshCurPageMoments()

    def handleImgLoadFailBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        if t.parent:
            t.parent.canOpen = False
            if int(e.loadStatus) == gametypes.NOS_FILE_STATUS_ILLEGAL:
                t.parent.gotoAndStop('butongguo')
            else:
                t.parent.gotoAndStop('shenghezhong')

    def handleImgLoadDone(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        if t.parent:
            t.parent.canOpen = True

    def handleOpenMoment(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget
        self.openMoment(t.dataIndex, const.PERSONAL_ZONE_MOMENT_ADD_COMMENT)

    def handleTopicApplyBtn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        self.uiAdapter.personalZoneMood.show(t.data)

    def handelHeadIconClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        roleName = str(t.roleName)
        gbId = int(t.gbId)
        hostId = int(t.hostId)
        menuId = uiConst.MENU_PERSOANL_SPACE
        if hostId != self.uiAdapter.personalZoneSystem.getHostId():
            menuId = uiConst.MENU_PERSOANL_SPACE_CROSS_SERVER
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            self.uiAdapter.showUserLinkMenu(roleName, gbId, hostId, menuId)
        else:
            self.uiAdapter.personalZoneSystem.openZoneOther(int(t.gbId), '', 0, int(t.hostId))

    def handleOpenPicture(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget.relatedMc
        p = BigWorld.player()
        if t:
            if not t.canOpen:
                p.showGameMsg(GMDD.data.PERSONAL_ZONE_PIC_AUDIT_TIPS, ())
                return None
            dataIndex = t.dataIndex
            listData = self.curMomentsInfo.get('list', [])
            data = {}
            if listData and dataIndex < len(listData):
                data = listData[dataIndex]
            imgList = data.get('forwardMoment', {}).get('imgList', [])
            if not imgList:
                imgList = data.get('imgList', [])
            picList = []
            numberIdx = 0
            for i, info in enumerate(imgList):
                pic = info.get('pic', '')
                status, _, _ = p.nosFileStatusCache.get(pic, (None, None, None))
                if status == gametypes.NOS_FILE_STATUS_APPROVED:
                    picList.append({'filePath': pic})
                    if i == int(t.picIdx):
                        numberIdx = len(picList) - 1

            if picList:
                gameglobal.rds.ui.personalZonePicture.show(picList, numberIdx)

    def openMoment(self, dataIndex, opType = const.PERSONAL_ZONE_MOMENT_ADD_COMMENT, commentId = 0):
        listData = self.curMomentsInfo.get('list', [])
        data = {}
        if listData and dataIndex < len(listData):
            data = listData[dataIndex]
        momentId = data.get('id', 0)
        rInfo = {}
        if opType == const.PERSONAL_ZONE_MOMENT_REPLY_COMMENT:
            if commentId:
                commentList = data.get('commentList', [])
                for commentInfo in commentList:
                    cId = commentInfo.get('id', 0)
                    if cId == commentId:
                        replyGbId = commentInfo.get('roleId', 0)
                        if replyGbId:
                            replyRoleName = commentInfo.get('roleName', 0)
                            replyServerId = commentInfo.get('serverId', 0)
                            rInfo = {'commentId': commentId,
                             'gbId': replyGbId,
                             'hostId': replyServerId,
                             'roleName': replyRoleName}
                        break

        self.uiAdapter.personalZoneMoment.show(momentId, data, opType, rInfo)

    def getTopTopicId(self):
        p = BigWorld.player()
        if p.topicList:
            return p.topicList[0].get('id', 0)
        return 0

    def setPrettyGirlBtn(self):
        if not self.hasBaseData():
            return
        self.widget.commonLayer.prettyGirlBtn.visible = self.baseInfo.get('missTianyu', 0) and GameDataModel.getGameConfig('enableMissTianyu')
        self.widget.commonLayer.prettyGirlBtn.addEventListener(events.MOUSE_CLICK, self.handleClickPrettyGirlBtn, False, 0, True)

    def setFuDaiIcon(self):
        if not self.hasBaseData():
            return
        if self.uiAdapter.personalZoneSystem.getFuDaiNumber() <= 0:
            self.widget.commonLayer.fuDaiShowBtn.visible = False
        else:
            self.widget.commonLayer.fuDaiShowBtn.visible = True
        TipManager.addTip(self.widget.commonLayer.fuDaiShowBtn, self.uiAdapter.personalZoneSystem.getFuDaiTips())

    def handleClickPrettyGirlBtn(self):
        if not self.hasBaseData():
            return
        self.uiAdapter.personalZoneSystem.openPrettyGirlFunc()

    def hasBaseData(self):
        if not self.widget:
            return False
        return True
