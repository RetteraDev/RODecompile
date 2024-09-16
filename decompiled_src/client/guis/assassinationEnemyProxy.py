#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/assassinationEnemyProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
import const
import ui
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
import clientUtils
from cdata import assassination_config_data as ACD

class AssassinationEnemyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AssassinationEnemyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ASSASSINATION_ENEMY, self.hide)

    def reset(self):
        self.lastEnemyMc = None
        self.enemyDataList = []
        self.findDataList = []
        self.selectedEnemyData = None
        self.hintStr = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ASSASSINATION_ENEMY:
            self.widget = widget
            self.reset()
            self.initData()
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ASSASSINATION_ENEMY)

    def initData(self):
        self.hintStr = ACD.data.get('searchEnemyHintStr', gameStrings.NEED_CONFIG_DESC)
        friendListData = gameglobal.rds.ui.friend._getFriendListData([gametypes.FRIEND_GROUP_ENEMY], gameglobal.FRIENDS_ALL)
        del self.enemyDataList[:]
        for childData in friendListData[0]['children']:
            gbId = long(childData[5])
            name = str(ui.unicode2gbk(childData[17]))
            level = int(childData[7])
            school = int(childData[6])
            isOnline = True if childData[1] == 'online' else False
            photo = str(childData[0])
            sex = int(childData[19])
            self.enemyDataList.append(self.updateInfoFormat(gbId, name, level, school, isOnline, photo, sex))

    def initUI(self):
        if self.widget:
            self.widget.defaultCloseBtn = self.widget.closeBtn
            self.initSearchInput()
            self.initScrollList()
            self.initConfirmBtn()

    def initSearchInput(self):
        self.widget.searchInputIconMc.enabled = False
        self.widget.searchInput.addEventListener(events.EVENT_CHANGE, self.handleSearchInputChange, False, 0, True)
        self.widget.searchInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleSearchKeyClick, False, 0, True)
        self.widget.searchInputIconMc.addEventListener(events.MOUSE_CLICK, self.handleSearchMouseClick, False, 0, True)
        self.widget.hintMc.htmlText = self.hintStr

    def handleSearchInputChange(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.text == '':
            self.widget.searchInputIconMc.enabled = False
            self.widget.enemyListMc.dataArray = self.enemyDataList
        else:
            self.widget.searchInputIconMc.enabled = True
            del self.findDataList[:]
            self.widget.enemyListMc.dataArray = self.findDataList
        self.selectedEnemyData = None
        self.refreshConfirmBtn()
        self.widget.enemyListMc.validateNow()

    def handleSearchKeyClick(self, *args):
        searchInputMc = ASObject(args[3][0])
        if searchInputMc.keyCode == events.KEYBOARD_CODE_ENTER or searchInputMc.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            searchInputMc.currentTarget.stage.focus = None
            searchInputMc.stopImmediatePropagation()
            self.searchEnemy()

    def handleSearchMouseClick(self, *args):
        self.searchEnemy()

    def initScrollList(self):
        listMc = self.widget.enemyListMc
        listMc.itemRenderer = 'AssassinationEnemy_Info'
        listMc.lableFunction = self.enemyListLabelFunction
        listMc.column = 1
        listMc.itemWidth = 270
        listMc.itemHeight = 83
        listMc.dataArray = self.enemyDataList
        listMc.validateNow()

    def enemyListLabelFunction(self, *args):
        enemyData = ASObject(args[3][0])
        enemyMc = ASObject(args[3][1])
        enemyMc.data = enemyData
        enemyMc.visible = True
        if enemyData.headIcon:
            enemyMc.portraitMc.headIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
            enemyMc.portraitMc.headIcon.fitSize = True
            enemyMc.portraitMc.headIcon.serverId = int(gameglobal.rds.g_serverid)
            enemyMc.portraitMc.headIcon.url = enemyData.headIcon
        else:
            enemyMc.portraitMc.headIcon.fitSize = True
            enemyMc.portraitMc.headIcon.loadImage(uiUtils.getHeadIconPath(enemyData.school, enemyData.sex))
        enemyMc.sexMc.gotoAndStop('type%d' % int(enemyData.sex))
        if not enemyData.online:
            ASUtils.setMcEffect(enemyMc.portraitMc.headIcon, 'gray')
        else:
            ASUtils.setMcEffect(enemyMc.portraitMc.headIcon)
        enemyMc.nameMc.htmlText = enemyData.name
        enemyMc.lvMc.htmlText = str(enemyData.lv)
        enemyMc.jobIconMc.gotoAndStop(enemyData.schoolDesc)
        TipManager.addTip(enemyMc.jobIconMc, enemyData.schoolName)
        enemyMc.checkRoomBtn.addEventListener(events.MOUSE_CLICK, self.handleViewZoneClick, False, 0, True)
        enemyMc.addEventListener(events.MOUSE_CLICK, self.handleEnemyMcClick, False, 0, True)
        enemyMc.selectEffect.visible = False
        enemyMc.validateNow()
        enemyMc.mouseChildren = True

    def handleViewZoneClick(self, *args):
        e = ASObject(args[3][0])
        gbId = long(e.currentTarget.parent.data.gbId)
        p = BigWorld.player()
        p.getPersonalSysProxy().openZoneOther(gbId, None, const.PERSONAL_ZONE_SRC_RECOMMEND_FRIEND)

    def handleEnemyMcClick(self, *args):
        enemyMc = ASObject(args[3][0]).currentTarget
        self.selectedEnemyData = enemyMc.data
        self.refreshConfirmBtn()
        if self.lastEnemyMc:
            self.lastEnemyMc.selectEffect.visible = False
        self.lastEnemyMc = enemyMc
        self.lastEnemyMc.selectEffect.visible = True
        enemyMc.validateNow()

    def updateEnemyDataUI(self):
        self.widget.enemyListMc.dataArray = self.findDataList
        self.widget.enemyListMc.validateNow()

    def initConfirmBtn(self):
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.refreshConfirmBtn()

    def refreshConfirmBtn(self):
        if self.selectedEnemyData:
            self.widget.confirmBtn.enabled = True
        else:
            self.widget.confirmBtn.enabled = False

    def handleConfirmBtnClick(self, *args):
        gameglobal.rds.ui.assassinationIssue.confirmToSelectEmeny(self.selectedEnemyData)
        self.hide()

    def show(self):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ASSASSINATION_ENEMY)

    def searchEnemy(self):
        playerName = self.widget.searchInput.text
        BigWorld.player().base.searchFriendByName(gametypes.SEARCH_PLAYER_FOR_FRIEND, playerName)

    def setSearchResult(self, infoList):
        if not gameglobal.rds.configData.get('enableAssassination', False):
            return
        if not self.widget:
            return
        del self.findDataList[:]
        for gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, combatScore in infoList:
            self.findDataList.append(self.updateInfoFormat(gbId, name, level, school, isOnline, photo, sex))

        self.updateEnemyDataUI()

    def updateInfoFormat(self, gbId, name, level, school, isOnline, photo, sex):
        p = BigWorld.player()
        if not photo:
            photo = p.friend.getDefaultPhoto(school, sex)
        infoMap = {'name': str(name),
         'gbId': long(gbId),
         'sex': int(sex),
         'lv': int(level),
         'online': bool(isOnline),
         'headIcon': str(photo),
         'schoolDesc': str(uiConst.SCHOOL_FRAME_DESC.get(school)),
         'schoolName': str(const.SCHOOL_DICT.get(school)),
         'school': int(school)}
        return infoMap
