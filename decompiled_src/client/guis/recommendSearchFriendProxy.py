#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/recommendSearchFriendProxy.o
from gamestrings import gameStrings
import random
import BigWorld
import gameglobal
import uiConst
import events
import math
import const
import gametypes
import utils
import uiUtils
from guis.asObject import ASUtils
from gameStrings import gameStrings
from guis.asObject import ASObject
from uiProxy import UIProxy
from callbackHelper import Functor
from guis import ui
RECOMMEND_OR_SEARCH_NUM = 4
RECOMMEND_REFRESH_CD = 30

class RecommendSearchFriendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RecommendSearchFriendProxy, self).__init__(uiAdapter)
        self.widget = None
        self.totalPage = 1
        self.currPage = 1
        self.searchHostId = 0
        self.searchResultList = []
        self.recommendList = []
        self.tQueryRecommend = 0
        self.inRecommend = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_RECOMM_SEARCH_FRIEND, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RECOMM_SEARCH_FRIEND:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self):
        if not gameglobal.rds.configData.get('enableRecommendFriend', False):
            return
        if gameglobal.rds.configData.get('enableGlobalFriend', False):
            BigWorld.player().base.queryCrossServerProgressIds(gameglobal.rds.ui.yunchuiji.crossMsIdsVer)
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RECOMM_SEARCH_FRIEND)

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RECOMM_SEARCH_FRIEND)

    def reset(self):
        self.currPage = 1
        self.totalPage = 1
        self.searchHostId = 0
        self.searchResultList = []
        self.inRecommend = False

    def clearAll(self):
        self.reset()
        self.tQueryRecommend = 0
        self.recommendList = []

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        ASUtils.setHitTestDisable(self.widget.playerNameTitle, True)
        self.widget.playerName.addEventListener(events.EVENT_CHANGE, self.handleTextChange, False, 0, True)
        self.widget.playerName.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyUp, False, 0, True)
        self.widget.playerName.textField.addEventListener(events.FOCUS_EVENT_FOCUS_IN, self.handleInputFocusIn, False, 0, True)
        self.widget.playerName.textField.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.handleInputFocusOut, False, 0, True)
        self.widget.enterBtn.addEventListener(events.MOUSE_CLICK, self.handleClickExectSearch, False, 0, True)
        self.widget.clearBtn.addEventListener(events.MOUSE_CLICK, self.handleClearPlayerName, False, 0, True)
        self.widget.serverChooseBtn.addEventListener(events.MOUSE_CLICK, self.handleChooseServer, False, 0, True)
        self.widget.addFriend.addEventListener(events.MOUSE_CLICK, self.handleClickApplyFriendList, False, 0, True)
        self.widget.changeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickChangeFriend, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.searchHostId = int(gameglobal.rds.g_serverid)
        self.widget.serverName.text = gameglobal.rds.loginManager.titleName()
        self.updateRecommendFriend()

    def handleClickExectSearch(self, *args):
        self.clickExectSearch()

    def clickExectSearch(self):
        playerName = self.widget.playerName.text
        if self.isSearchSameSever():
            BigWorld.player().base.searchFriendByName(gametypes.SEARCH_PLAYER_FOR_FRIEND, playerName)
        else:
            BigWorld.player().base.queryGlobalFriendByName(self.searchHostId, playerName)

    def handleClearPlayerName(self, *args):
        self.widget.playerName.text = ''
        self.widget.clearBtn.enabled = False
        self.widget.enterBtn.enabled = False

    def handleChooseServer(self, *args):
        self.uiAdapter.migrateServer.showServerList(uiConst.CHOOSE_SERVER_TYPE_ALL, self.changeServer)

    def handleTextChange(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.text == '':
            self.widget.clearBtn.enabled = False
            self.widget.enterBtn.enabled = False
        else:
            self.widget.clearBtn.enabled = True
            self.widget.enterBtn.enabled = True

    def handleInputFocusIn(self, *args):
        if not self.widget:
            return
        self.widget.playerNameTitle.visible = False

    def handleInputFocusOut(self, *args):
        if not self.widget:
            return
        self.widget.playerNameTitle.visible = self.widget.playerName.text == ''

    def handleKeyUp(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == events.KEYBOARD_CODE_ENTER or e.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            e.currentTarget.stage.focus = None
            e.stopImmediatePropagation()
            self.clickExectSearch()

    def handlePrevBtnClick(self, *args):
        if self.currPage > 1:
            self.currPage = self.currPage - 1
            self.updateSearchResultItem()
            self.updatePageStepper()

    def handleNextBtnClick(self, *args):
        if self.currPage < self.totalPage:
            self.currPage = self.currPage + 1
            self.updateSearchResultItem()
            self.updatePageStepper()

    def handleClickChangeFriend(self, *args):
        e = ASObject(args[3][0])
        szLabel = e.currentTarget.label
        if szLabel == gameStrings.RECOMMEND_FRIEND_CHANGE_BTN_LABTL:
            p = BigWorld.player()
            if utils.getNow() - self.tQueryRecommend <= RECOMMEND_REFRESH_CD:
                random.shuffle(self.recommendList)
                self.setRecommendResult(self.recommendList, bRefresh=False)
            else:
                p.base.queryRecommendFriends()
        elif szLabel == gameStrings.RECOMMEND_FRIEND_TITLE:
            self.updateRecommendFriend()

    def handleClickApplyFriendList(self, *args):
        if gameglobal.rds.ui.friendRequest.checkNewFriendRequest():
            gameglobal.rds.ui.friendRequest.show()

    def handleClickRecommFriend(self, *args):
        e = ASObject(args[3][0])
        btnName = e.target.name
        data = e.currentTarget.data
        roleName = data.get('name', '')
        gbId = int(data.get('gbId', 0))
        p = BigWorld.player()
        if btnName == 'addFriend':
            group = p.friend.defaultGroup if p.friend.defaultGroup else gametypes.FRIEND_GROUP_FRIEND
            srcId = const.FRIEND_SRC_RECOMMEND_FRIEND
            p.base.addContactByGbId(gbId, group, srcId)
        else:
            self.updateBtnClickFriend(btnName, roleName, gbId)
            p.base.viewFriendProfile(gbId, 0, const.FRIEND_SRC_RECOMMEND_FRIEND)

    def handleClickSearchFriend(self, *args):
        e = ASObject(args[3][0])
        btnName = e.target.name
        data = e.currentTarget.data
        roleName = data.get('name', '')
        gbId = int(data.get('gbId', 0))
        p = BigWorld.player()
        if btnName == 'addFriend':
            if p.friend.isEnemy(gbId):
                fVal = p.getFValByGbId(gbId)
                msg = gameStrings.ENEMY_TO_FRIEND % fVal.name
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.addToFriendAccept, gbId))
            else:
                self.addToFriendAccept(gbId)
        else:
            self.updateBtnClickFriend(btnName, roleName, gbId)

    def addToFriendAccept(self, gbId):
        p = BigWorld.player()
        if p.friend.isEnemy(gbId):
            p.base.deleteEnemy(gbId, True)
        elif not self.isSearchSameSever():
            p.base.addRemoteFriendRequest(self.searchHostId, gbId)
        else:
            group = p.friend.defaultGroup if p.friend.defaultGroup else gametypes.FRIEND_GROUP_FRIEND
            p.base.addContactByGbId(gbId, group, const.FRIEND_SRC_SEARCH_FRIEND)

    def updateBtnClickFriend(self, btnName, roleName, gbId):
        p = BigWorld.player()
        if btnName == 'beginTochat':
            if p.friend.isFriend(gbId):
                gameglobal.rds.ui.friend.beginChat(gbId)
            else:
                gameglobal.rds.ui.chat.updateChatTarge(roleName)
                gameglobal.rds.ui.chat.setCurChannel(const.CHAT_CHANNEL_SINGLE, '', True)
        elif btnName == 'viewRoleInfo':
            p.getPersonalSysProxy().openZoneOther(gbId, None, const.PERSONAL_ZONE_SRC_RECOMMEND_FRIEND)
            if self.inRecommend:
                p.getPersonalSysProxy().friendSrcId = const.FRIEND_SRC_RECOMMEND_FRIEND

    def updateRecommendFriend(self):
        self.widget.playerNameTitle.visible = True
        self.widget.playerName.text = ''
        self.widget.clearBtn.enabled = False
        self.widget.enterBtn.enabled = False
        self.widget.pageControl.visible = False
        self.widget.titleText.text = gameStrings.RECOMMEND_FRIEND_TITLE
        self.widget.addFriend.label = gameStrings.APPLY_FRIEND_BTN_LABEL
        self.widget.changeBtn.label = gameStrings.RECOMMEND_FRIEND_CHANGE_BTN_LABTL
        self.updatefriendRequentListBtn()
        if utils.getNow() - self.tQueryRecommend <= RECOMMEND_REFRESH_CD:
            self.setRecommendResult(self.recommendList, bRefresh=False)
        else:
            self.setRecommendResult([])
        p = BigWorld.player()
        p.base.queryRecommendFriends()

    def updatefriendRequentListBtn(self):
        if not self.widget:
            return
        num = gameglobal.rds.ui.friendRequest.getFriendRequestNum()
        if num > 0:
            self.widget.addFriend.enabled = True
        else:
            self.widget.addFriend.enabled = False

    def setRecommendResult(self, infoList, bRefresh = True):
        if not self.widget:
            return
        info = []
        for gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, text in infoList:
            info.append(self.updateInfoFormat(gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, text))

        self.recommendList = infoList
        if bRefresh:
            self.tQueryRecommend = utils.getNow()
        self.inRecommend = True
        self.updateRecommendResultItem(info)
        gbIds = [ x[0] for x in infoList[:RECOMMEND_OR_SEARCH_NUM] ]
        if gbIds:
            BigWorld.player().base.genRecommendFriendListLog(gbIds)

    def updateRecommendResultItem(self, recommendInfo):
        if not self.widget.friendItemLiist:
            return
        for i in range(RECOMMEND_OR_SEARCH_NUM):
            itemMc = self.widget.friendItemLiist.getChildByName('item%d' % i)
            itemMc.opBtns.removeEventListener(events.MOUSE_CLICK, self.handleClickSearchFriend)
            if i < len(recommendInfo):
                tInfo = recommendInfo[i]
                itemMc.visible = True
                itemMc.headIcon.icon.imgType = 2
                itemMc.headIcon.icon.fitSize = True
                itemMc.headIcon.icon.serverId = self.searchHostId
                itemMc.headIcon.icon.url = tInfo.get('headIcon', '')
                itemMc.headIcon.sex.gotoAndStop('type%d' % int(tInfo.get('sex', 1)))
                if not tInfo.get('online', False):
                    ASUtils.setMcEffect(itemMc.headIcon, 'gray')
                else:
                    ASUtils.setMcEffect(itemMc.headIcon)
                itemMc.nameTxt.htmlText = tInfo.get('name', '')
                itemMc.lvTxt.htmlText = tInfo.get('lv', 0)
                itemMc.schoolIcon.gotoAndStop(tInfo.get('schoolDesc', ''))
                itemMc.msg.htmlText = tInfo.get('signText', '')
                itemMc.opBtns.data = tInfo
                itemMc.opBtns.addEventListener(events.MOUSE_CLICK, self.handleClickRecommFriend, False, 0, True)
                itemMc.focusable = False
                itemMc.validateNow()
                itemMc.mouseChildren = True
            else:
                itemMc.visible = False

    def changeServer(self, serverId, serverName):
        self.searchHostId = int(serverId)
        if not self.widget:
            return
        self.widget.serverName.text = serverName
        self.setSearchResult([])

    def setSearchResult(self, infoList):
        if not self.widget:
            return
        info = []
        for gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, combatScore in infoList:
            info.append(self.updateInfoFormat(gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, ''))

        self.inRecommend = False
        self.updateSearchResult(info)

    def updateInfoFormat(self, gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, text):
        p = BigWorld.player()
        if not photo:
            photo = p.friend.getDefaultPhoto(school, sex)
        infoMap = {'name': name,
         'gbId': str(gbId),
         'sex': sex,
         'lv': 'Lv.%s' % level,
         'online': isOnline,
         'headIcon': photo,
         'onlineTxt': gameStrings.TEXT_FRIENDPROXY_293_1 if isOnline else gameStrings.TEXT_UIUTILS_1414,
         'schoolDesc': uiConst.SCHOOL_FRAME_DESC.get(school),
         'signText': text}
        return infoMap

    def updateSearchResult(self, info):
        self.widget.titleText.text = gameStrings.SEARCH_FRIEND_TITLE
        self.widget.pageControl.visible = True
        self.widget.changeBtn.label = gameStrings.RECOMMEND_FRIEND_TITLE
        self.widget.pageControl.prevBtn.addEventListener(events.BUTTON_CLICK, self.handlePrevBtnClick, False, 0, True)
        self.widget.pageControl.nextBtn.addEventListener(events.BUTTON_CLICK, self.handleNextBtnClick, False, 0, True)
        self.searchResultList = info
        self.totalPage = max(int(math.ceil(len(info) * 1.0 / RECOMMEND_OR_SEARCH_NUM)), 1)
        self.currPage = 1
        self.updateSearchResultItem()
        self.updatePageStepper()

    def updatePageStepper(self):
        self.widget.pageControl.textField.text = '%d/%d' % (self.currPage, self.totalPage)
        self.widget.pageControl.prevBtn.enabled = self.currPage > 1 and self.totalPage != 1
        self.widget.pageControl.nextBtn.enabled = self.currPage < self.totalPage and self.totalPage != 1

    def isSearchSameSever(self):
        return int(self.searchHostId) == int(gameglobal.rds.g_serverid)

    def updateSearchResultItem(self):
        startIdx = max(0, (self.currPage - 1) * RECOMMEND_OR_SEARCH_NUM)
        endIdx = self.currPage * RECOMMEND_OR_SEARCH_NUM
        nIndex = 0
        for i in range(startIdx, endIdx):
            itemMc = self.widget.friendItemLiist.getChildByName('item%d' % nIndex)
            itemMc.opBtns.removeEventListener(events.MOUSE_CLICK, self.handleClickRecommFriend)
            if i < len(self.searchResultList):
                tInfo = self.searchResultList[i]
                itemMc.visible = True
                itemMc.headIcon.icon.imgType = 2
                itemMc.headIcon.icon.fitSize = True
                itemMc.headIcon.icon.serverId = self.searchHostId
                itemMc.headIcon.icon.url = tInfo.get('headIcon', '')
                itemMc.headIcon.sex.gotoAndStop('type%d' % int(tInfo.get('sex', 1)))
                if not tInfo.get('online', False):
                    ASUtils.setMcEffect(itemMc.headIcon, 'gray')
                else:
                    ASUtils.setMcEffect(itemMc.headIcon)
                itemMc.nameTxt.htmlText = tInfo.get('name', '')
                itemMc.lvTxt.htmlText = tInfo.get('lv', 0)
                itemMc.schoolIcon.gotoAndStop(tInfo.get('schoolDesc', ''))
                itemMc.msg.htmlText = tInfo.get('signText', '')
                itemMc.opBtns.data = tInfo
                itemMc.opBtns.addEventListener(events.MOUSE_CLICK, self.handleClickSearchFriend, False, 0, True)
                itemMc.focusable = False
                itemMc.validateNow()
                itemMc.mouseChildren = True
            else:
                itemMc.visible = False
            nIndex = nIndex + 1

    def showRecommendSearchFriendPush(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_RECOMMEND_SEARCH_FRIEND)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_RECOMMEND_SEARCH_FRIEND, {'click': self.show})
