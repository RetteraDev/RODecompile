#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/assassinationTombstoneProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gamelog
import uiConst
import events
import gametypes
import const
import ui
import utils
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
from guis.asObject import MenuManager
from assassination import AssassinationTomb
from assassination import AssassinationTombMsg
from helpers import taboo
import clientUtils
from cdata import assassination_config_data as ACD
from cdata import game_msg_def_data as GMDD

class AssassinationTombstoneProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AssassinationTombstoneProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ASSASSINATION_TOMBSTONE, self.hide)

    def reset(self):
        self.tombEntityId = 0
        self.deadData = {}
        self.enemyData = {}
        self.commentDataList = []
        self.commentDataIndexList = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ASSASSINATION_TOMBSTONE:
            self.widget = widget
            self.refreshUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ASSASSINATION_TOMBSTONE)

    def show(self, tombEntityId):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        self.removeNewUpdateMsg()
        if tombEntityId:
            self.tombEntityId = tombEntityId
            if not self.widget:
                self.uiAdapter.loadWidget(uiConst.WIDGET_ASSASSINATION_TOMBSTONE)
            self.requestAllTombDataByTombId(self.tombEntityId)
        elif self.widget:
            self.hide()

    def refreshAll(self, allData):
        self.refreshData(allData)
        self.refreshUI()

    def refreshData(self, allData):
        if allData:
            tombData = AssassinationTomb().fromDTO(allData)
            self.deadData.clear()
            self.enemyData.clear()
            del self.commentDataList[:]
            del self.commentDataIndexList[:]
            self.getEnemyData(tombData)
            self.getDeadData(tombData)
            self.getAllCommentData(tombData)
        else:
            self.deadData.clear()
            self.enemyData.clear()
            del self.commentDataList[:]
            del self.commentDataIndexList[:]

    def refreshUI(self):
        if not self.widget:
            return
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.refreshCommentInput()
        self.refreshCommentList()
        self.refreshMainContent()

    def requestAllTombDataByTombId(self, tombId):
        if tombId:
            BigWorld.player().base.queryAssassinationTomb(self.tombEntityId)
        elif self.widget:
            self.hide()

    def requestComment(self):
        msg = str(self.widget.commentInput.text)
        if self.tombEntityId:
            if self.checkCommentValid(msg):
                self.widget.commentInput.text = ''
                self.widget.commentBtn.enabled = False
                BigWorld.player().base.commentAssassinationTomb(self.tombEntityId, msg)
                self.requestAllTombDataByTombId(self.tombEntityId)
        elif self.widget:
            self.hide()

    def refreshCommentInput(self):
        self.widget.commentBtn.enabled = False
        self.widget.commentBtn.label = gameStrings.ASSASSINATION_TOMB_COMMENT_ZERO_HINT
        self.widget.commentInput.addEventListener(events.EVENT_CHANGE, self.handleCommentInputChange, False, 0, True)
        self.widget.commentInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleCommentInputEnterKeyClick, False, 0, True)
        self.widget.commentBtn.addEventListener(events.MOUSE_CLICK, self.handleCommentSubmitBtnClick, False, 0, True)

    def handleCommentInputChange(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.text == '':
            self.widget.commentBtn.enabled = False
        else:
            self.widget.commentBtn.enabled = True

    def handleCommentInputEnterKeyClick(self, *args):
        commentInputMc = ASObject(args[3][0])
        if commentInputMc.keyCode == events.KEYBOARD_CODE_ENTER or commentInputMc.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            commentInputMc.currentTarget.stage.focus = None
            commentInputMc.stopImmediatePropagation()
            self.requestComment()

    def handleCommentSubmitBtnClick(self, *args):
        self.requestComment()

    def refreshCommentList(self):
        if len(self.commentDataIndexList) <= 0:
            self.widget.comment.text = gameStrings.ASSASSINATION_TOMB_COMMENT_ZERO_HINT
        else:
            self.widget.comment.text = gameStrings.ASSASSINATION_TOMB_COMMENT_HINT % len(self.commentDataIndexList)
        listMc = self.widget.commentList
        listMc.itemRenderer = 'AssassinationTombstone_commentItem'
        listMc.lableFunction = self.commentListLabelFunction
        listMc.column = 1
        listMc.itemWidth = 265
        listMc.itemHeight = 45
        listMc.dataArray = self.commentDataIndexList
        listMc.validateNow()

    def commentListLabelFunction(self, *args):
        assTombMsgIndex = int(args[3][0].GetNumber())
        assTombMsgData = self.commentDataList[assTombMsgIndex]
        commentMc = ASObject(args[3][1])
        commentMc.headIconMc.headIcon.fitSize = True
        if assTombMsgData.photo:
            commentMc.headIconMc.headIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
            commentMc.headIconMc.headIcon.serverId = int(gameglobal.rds.g_serverid)
            commentMc.headIconMc.headIcon.url = assTombMsgData.photo
        else:
            commentMc.headIconMc.headIcon.loadImage(uiUtils.getHeadIconPath(int(assTombMsgData.school), int(assTombMsgData.sex)))
        menuParam = {'roleName': assTombMsgData.roleName,
         'gbId': assTombMsgData.gbId}
        MenuManager.getInstance().registerMenuById(commentMc, uiConst.MENU_CHAT, menuParam)
        commentMc.nameMc.text = assTombMsgData.roleName
        commentMc.contentMc.text = assTombMsgData.msg

    def refreshMainContent(self):
        self.refreshDeadContent()
        self.refreshEnemyContet()

    def refreshDeadContent(self):
        self.widget.deadName.text = str(self.deadName)
        portraitMc = self.widget.deadHeadIconMc
        if self.deadHeadIcon:
            portraitMc.headIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
            portraitMc.headIcon.fitSize = True
            portraitMc.headIcon.serverId = int(gameglobal.rds.g_serverid)
            portraitMc.headIcon.url = self.deadHeadIcon
        else:
            portraitMc.headIcon.fitSize = True
            portraitMc.headIcon.loadImage(uiUtils.getHeadIconPath(int(self.deadSchool), int(self.deadSex)))
        menuParam = {'roleName': self.deadName,
         'gbId': self.deadGbId}
        MenuManager.getInstance().registerMenuById(portraitMc, uiConst.MENU_CHAT, menuParam)
        MenuManager.getInstance().registerMenuById(self.widget.deadName, uiConst.MENU_CHAT, menuParam)
        self.widget.deadLvMc.text = str(self.deadLv)

    def refreshEnemyContet(self):
        self.widget.enemyName.text = gameStrings.ASSASSINATION_TOMB_ENEMY_NAME % self.enemyName
        if self.enemyGbId:
            menuParam = {'roleName': self.enemyName,
             'gbId': self.enemyGbId}
            MenuManager.getInstance().registerMenuById(self.widget.enemyName, uiConst.MENU_CHAT, menuParam)
        leaveContentTxtDict = ACD.data.get('assassinationMsgDict', {})
        self.widget.leaveBook.defaultText = leaveContentTxtDict.get(self.enemyLeaveBookId)
        self.widget.leaveBook.mouseChildren = False

    def pushNewUpdateMsg(self, tombEntId):
        if gameglobal.rds.configData.get('enableAssEmployerPush', False):
            if self.employerPushId:
                gameglobal.rds.ui.pushMessage.addPushMsg(self.employerPushId, {'data': tombEntId})

    def removeNewUpdateMsg(self):
        if self.employerPushId:
            gameglobal.rds.ui.pushMessage.removePushMsg(self.employerPushId)

    def setNewUpdateMsgCallBack(self):
        if gameglobal.rds.configData.get('enableAssEmployerPush', False):
            if self.employerPushId:
                gameglobal.rds.ui.pushMessage.setCallBack(self.employerPushId, {'click': self.pushNewUpdateCallBack})

    def pushNewUpdateCallBack(self):
        tombEntId = gameglobal.rds.ui.pushMessage.getLastData(self.employerPushId).get('data', 0)
        if tombEntId:
            gameglobal.rds.ui.assassinationTombstone.show(tombEntId)

    def getEnemyData(self, assTombData):
        self.enemyData['name'] = str(assTombData.ownerName)
        self.enemyData['gbId'] = str(assTombData.ownerGbId)
        self.enemyData['leaveId'] = int(assTombData.msg)

    @property
    def employerPushId(self):
        pushId = ACD.data.get('assassinationEmployerPushId', 0)
        return pushId

    @property
    def enemyName(self):
        return self.enemyData.get('name', gameStrings.TEXT_ASSASSINATIONTOMBSTONEPROXY_264)

    @property
    def enemyGbId(self):
        return self.enemyData.get('gbId', 0)

    @property
    def enemyLeaveBookId(self):
        return self.enemyData.get('leaveId', 1)

    def getDeadData(self, assTombData):
        self.deadData['name'] = str(assTombData.roleName)
        self.deadData['gbId'] = str(assTombData.gbId)
        self.deadData['headIcon'] = assTombData.photo
        self.deadData['lv'] = assTombData.lv
        self.deadData['school'] = assTombData.school
        self.deadData['sex'] = assTombData.sex

    @property
    def deadName(self):
        return self.deadData.get('name', '')

    @property
    def deadHeadIcon(self):
        return self.deadData.get('headIcon', '')

    @property
    def deadLv(self):
        return self.deadData.get('lv', 0)

    @property
    def deadGbId(self):
        return self.deadData.get('gbId', 0)

    @property
    def deadSchool(self):
        return self.deadData.get('school', 0)

    @property
    def deadSex(self):
        return self.deadData.get('sex', 0)

    def getAllCommentData(self, assTombData):
        self.commentDataList.extend(assTombData.comment)
        self.commentDataList.sort(cmp=lambda assTombDataA, assTombDataB: assTombDataB.stamp - assTombDataA.stamp)
        for index in xrange(len(self.commentDataList)):
            self.commentDataIndexList.append(index)

    def checkCommentValid(self, comment):
        p = BigWorld.player()
        maxLength = ACD.data.get('assassinationTombCommentMsgMaxLength', 15)
        commentUni = self.gbk2Unicode(comment, comment)
        if comment is None or len(comment) <= 0 or len(commentUni) <= 0:
            p.showGameMsg(GMDD.data.ASSASSINATION_TOMB_COMMENT_NOT_ZERO, ())
            return False
        elif len(commentUni) > maxLength:
            p.showGameMsg(GMDD.data.ASSASSINATION_TOMB_COMMENT_MAX_LIMIT, ())
            return False
        isNormal, newComment = taboo.checkBWorld(comment)
        if not isNormal:
            p.showGameMsg(GMDD.data.ASSASSINATION_TOMB_COMMENT_TABOO, ())
            return False
        else:
            return True

    def gbk2Unicode(self, str, default = ''):
        try:
            return str.decode(utils.defaultEncoding())
        except:
            gamelog.error('AssassinationLeaveBoolProxy gbk2unicode error', str)
            return default
