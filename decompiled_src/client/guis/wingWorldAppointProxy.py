#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldAppointProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
import math
import utils
import gametypes
import uiUtils
import const
import wingWorldUtils
from uiProxy import UIProxy
from guis.asObject import ASUtils
from guis import ui
from guis.asObject import ASObject
from gamestrings import gameStrings
MAX_PAGE_NUM = 5
MAX_PLAYER_PER_PAGE = 8
LEADER_MGR_POST_NUM = 12
GENERAL_MGR_POST_NUM = 9

class WingWorldAppointProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldAppointProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_APPOINT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_APPOINT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def reset(self):
        self.widget = None
        self.appointList = {}
        self.appointedList = []
        self.appointedListBefore = []
        self.appointingList = []
        self.pageNo = 1
        self.playerNum = 0
        self.appointedNum = 0
        self.appointingNum = 0
        self.selectedAppointBtn = 0
        self.maxAppointNum = 0
        self.mgrPostName = ''
        self.mgrPostIds = 0

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleCloseClick, False, 0, True)
        self.widget.submitBtn.addEventListener(events.MOUSE_CLICK, self.handleSubmitClick, False, 0, True)
        self.widget.pageMc.minBtn.addEventListener(events.BUTTON_CLICK, self.handleMinBtnClick, False, 0, True)
        self.widget.pageMc.maxBtn.addEventListener(events.BUTTON_CLICK, self.handleMaxBtnClick, False, 0, True)
        self.widget.submitBtn.enabled = False
        self.widget.pageMc.stepper.labelFunction = self.optionStepperLableFunction
        self.widget.pageMc.stepper.addEventListener(events.INDEX_CHANGE, self.handleIndexChange, False, 0, True)
        self.widget.input.addEventListener(events.EVENT_CHANGE, self.handleInputChange, False, 0, True)
        self.widget.searchBtn.enabled = False
        self.widget.searchBtn.addEventListener(events.BUTTON_CLICK, self.handleSearchClick, False, 0, True)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_APPOINT)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_APPOINT)

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            mgrPostIds = p.wingWorld.getArmyByGbId(p.gbId).mgrPostIds
            armyData = wingWorldUtils.getWingArmyData()
            if p.isWingWorldCampArmy():
                if p.wingWorldPostId == wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID:
                    self.maxAppointNum = LEADER_MGR_POST_NUM
                    for id in mgrPostIds:
                        if id in wingWorldUtils.wingPostIdData.ARMY_SPECIAL_POST_ID:
                            continue
                        else:
                            self.mgrPostIds = id

                else:
                    self.maxAppointNum = GENERAL_MGR_POST_NUM
                    for id in mgrPostIds:
                        self.mgrPostIds = id

            elif p.wingWorldPostId == wingWorldUtils.wingPostIdData.ARMY_LEADER_POST_ID:
                self.maxAppointNum = LEADER_MGR_POST_NUM
                for id in mgrPostIds:
                    if id in wingWorldUtils.wingPostIdData.ARMY_SPECIAL_POST_ID:
                        continue
                    else:
                        self.mgrPostIds = id

            else:
                self.maxAppointNum = GENERAL_MGR_POST_NUM
                for id in mgrPostIds:
                    self.mgrPostIds = id

            self.mgrPostName = armyData.get(self.mgrPostIds, {}).get('name')
            self.appointedListBefore = gameglobal.rds.ui.wingWorld.getAppointData()
            self.appointedNum = len(self.appointedListBefore)
            if self.maxAppointNum == GENERAL_MGR_POST_NUM:
                self.appointedList = self.appointedListBefore + [None] * (self.maxAppointNum - len(self.appointedListBefore))
            else:
                specialPost = [None] * 3
                normalPost = []
                for player in self.appointedListBefore:
                    gbId = player['gbId']
                    postId = p.wingWorld.getArmyByGbId(gbId).postId
                    if postId in wingWorldUtils.wingPostIdData.ARMY_SPECIAL_POST_ID:
                        if postId == wingWorldUtils.wingPostIdData.ARMY_ASSIST1_POST_ID:
                            specialPost[0] = player
                        elif postId == wingWorldUtils.wingPostIdData.ARMY_ASSIST2_POST_ID:
                            specialPost[1] = player
                        elif postId == wingWorldUtils.wingPostIdData.ARMY_ASSIST3_POST_ID:
                            specialPost[2] = player
                    else:
                        startIndex = self.appointedListBefore.index(player)
                        normalPost = self.appointedListBefore[startIndex:]
                        break

                self.appointedList = specialPost + normalPost + [None] * (self.maxAppointNum - len(normalPost) - 3)
            p.cell.queryRecommendSoldierInGuild()
            for i in xrange(self.maxAppointNum):
                if not self.appointedList[i]:
                    self.selectedAppointBtn = i
                    break

            self.refreshAppointedPanel()
            return

    def handleCloseClick(self, *args):
        self.hide()

    def handleSubmitClick(self, *args):
        self.appointArmy()

    def handleIndexChange(self, *args):
        self.pageNo = int(self.widget.pageMc.stepper.selectedIndex + 1)
        self.refreshAppointingPanel()

    def optionStepperLableFunction(self, *args):
        pageNo = int(args[3][0].GetNumber())
        return GfxValue(ui.gbk2unicode(str(pageNo + 1)))

    def handleMinBtnClick(self, *args):
        self.widget.pageMc.stepper.selectedIndex = 0

    def handleMaxBtnClick(self, *args):
        self.widget.pageMc.stepper.selectedIndex = MAX_PAGE_NUM - 1

    def handleInputChange(self, *args):
        self.widget.searchBtn.enabled = not utils.isEmpty(self.widget.input.text)
        if utils.isEmpty(self.widget.input.text) and not len(self.widget.input.text):
            self.widget.pageMc.stepper.selectedIndex = 0
            BigWorld.player().cell.queryRecommendSoldierInGuild()

    def handleSearchClick(self, *args):
        txt = self.widget.input.text
        BigWorld.player().base.searchFriendByName(gametypes.SEARCH_PLAYER_FOR_ARMY_APPOINT, txt)

    def refreshAppointingPanel(self):
        if not self.widget:
            return
        else:
            self.appointingNum = len(self.appointingList) if self.appointingList else 0
            pages = int(math.ceil(self.appointingNum / float(MAX_PLAYER_PER_PAGE)))
            ASUtils.setDropdownMenuData(self.widget.pageMc.stepper, range(0, pages))
            self.widget.pageMc.minBtn.disabled = self.pageNo == 1
            self.widget.pageMc.stepper.prevBtn.disabled = self.pageNo == 1
            self.widget.pageMc.maxBtn.disabled = self.pageNo == pages
            self.widget.pageMc.stepper.nextBtn.disabled = self.pageNo == pages
            for i in xrange(MAX_PLAYER_PER_PAGE):
                playerItem = self.widget.appointingList.canvas.getChildByName('player%d' % i)
                index = (self.pageNo - 1) * MAX_PLAYER_PER_PAGE + i
                if index < self.appointingNum:
                    player = self.appointingList[index]
                    playerItem.visible = True
                    playerItem.playerName.text = player['name']
                    playerItem.combatScore.text = gameStrings.TEXT_WINGWORLDAPPOINTPROXY_185 + str(player['combatScore'])
                    if player['photo']:
                        photo = player['photo']
                    else:
                        photo = 'headIcon/%s.dds' % str(player['school'] * 10 + player['sex'])
                    if uiUtils.isDownloadImage(photo):
                        BigWorld.player().downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, None, (None,))
                        photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
                    playerItem.playerIcon.fitSize = True
                    playerItem.playerIcon.loadImage(photo)
                    playerItem.index = index
                    army = BigWorld.player().wingWorld.getArmyByGbId(player['gbId'])
                    if army or player in self.appointedList:
                        playerItem.addBtn.enabled = False
                    else:
                        playerItem.addBtn.enabled = True
                        playerItem.addBtn.addEventListener(events.BUTTON_CLICK, self.addAppointingPlayer)
                else:
                    playerItem.visible = False

            return

    def refreshAppointedPanel(self):
        if not self.widget:
            return
        armyData = wingWorldUtils.getWingArmyData()
        self.widget.titleText.text = gameStrings.WING_WORLD_APPOINT_TITLE_TEXT % (self.appointedNum, self.maxAppointNum)
        if self.appointedNum <= len(self.appointedListBefore):
            self.widget.submitBtn.enabled = False
        else:
            self.widget.submitBtn.enabled = True
        for i in xrange(self.maxAppointNum):
            playerItem = self.widget.appointedList.getChildByName('player%d' % i)
            playerItem.addEventListener(events.MOUSE_CLICK, self.selectAppointBtn)
            playerItem.index = i
            playerItem.visible = True
            showNameString = self.mgrPostName
            if self.maxAppointNum == LEADER_MGR_POST_NUM:
                if i == 0:
                    showNameString = armyData.get(wingWorldUtils.wingPostIdData.ARMY_ASSIST1_POST_ID, {}).get('name')
                elif i == 1:
                    showNameString = armyData.get(wingWorldUtils.wingPostIdData.ARMY_ASSIST2_POST_ID, {}).get('name')
                elif i == 2:
                    showNameString = armyData.get(wingWorldUtils.wingPostIdData.ARMY_ASSIST3_POST_ID, {}).get('name')
            playerItem.title.textField.text = showNameString
            if self.appointedList[i]:
                playerItem.gotoAndStop('appointed')
                player = self.appointedList[i]
                if player in self.appointedListBefore:
                    playerItem.closeBtn.visible = False
                else:
                    playerItem.closeBtn.visible = True
                    playerItem.closeBtn.addEventListener(events.MOUSE_CLICK, self.removeAppointedPlayer)
                playerItem.btn1.label = player['name']
            else:
                playerItem.gotoAndStop('unappointed')
                playerItem.btn0.label = gameStrings.WING_WORLD_APPOINT_BTN_STATUS1

    def removeAppointedPlayer(self, *args):
        index = ASObject(args[3][0]).target.parent.index
        player = self.appointedList[index]
        self.appointedList[index] = None
        if player not in self.appointingList:
            self.appointingList.append(player)
        self.appointedNum = self.appointedNum - 1
        self.refreshAppointingPanel()
        self.refreshAppointedPanel()

    def addAppointingPlayer(self, *args):
        index = ASObject(args[3][0]).target.parent.index
        player = self.appointingList[index]
        self.appointingList.remove(player)
        appointedPlayer = self.appointedList[self.selectedAppointBtn]
        if appointedPlayer and appointedPlayer not in self.appointingList:
            self.appointingList.append(appointedPlayer)
        else:
            self.appointedNum = self.appointedNum + 1
        self.appointedList[self.selectedAppointBtn] = player
        self.refreshAppointingPanel()
        self.refreshAppointedPanel()

    def selectAppointBtn(self, *args):
        lastItem = self.widget.appointedList.getChildByName('player%d' % self.selectedAppointBtn)
        if lastItem.currentLabel == 'unappointed':
            lastItem.btn0.selected = False
        elif lastItem.currentLabel == 'appointed':
            lastItem.btn1.selected = False
        item = ASObject(args[3][0]).currentTarget
        index = item.index
        if self.appointedList[index] in self.appointedListBefore:
            return
        if item.currentLabel == 'unappointed':
            item.btn0.selected = True
        elif item.currentLabel == 'appointed':
            item.btn1.selected = True
        self.selectedAppointBtn = index
        self.refreshAppointedPanel()

    def appointArmy(self):
        p = BigWorld.player()
        sendGbIds = []
        sendPostIds = []
        for i in xrange(self.maxAppointNum):
            player = self.appointedList[i]
            if not player:
                continue
            gbId = player.get('gbId')
            army = p.wingWorld.getArmyByGbId(gbId)
            if not army:
                sendGbIds.append(gbId)
                if self.maxAppointNum == LEADER_MGR_POST_NUM:
                    if i == 0:
                        sendPostIds.append(wingWorldUtils.wingPostIdData.ARMY_ASSIST1_POST_ID)
                    elif i == 1:
                        sendPostIds.append(wingWorldUtils.wingPostIdData.ARMY_ASSIST2_POST_ID)
                    elif i == 2:
                        sendPostIds.append(wingWorldUtils.wingPostIdData.ARMY_ASSIST3_POST_ID)
                    else:
                        sendPostIds.append(self.mgrPostIds)
                else:
                    sendPostIds.append(self.mgrPostIds)

        BigWorld.player().cell.appointWingWorldMultiArmyPost(sendGbIds, sendPostIds)

    def setPlayerList(self, infoList):
        if self.widget != None:
            info = []
            for gbId, name, level, spaceNo, areaId, school, isOnline, photo, sex, combatScore in infoList:
                info.append({'gbId': gbId,
                 'photo': photo,
                 'combatScore': combatScore,
                 'name': name,
                 'school': school,
                 'sex': sex})

            self.appointingList = []
            self.appointingList = info
            self.refreshAppointingPanel()

    def onAppointWingWorldArmyPostOK(self, gbId, dto, armyVer):
        p = BigWorld.player()
        p.wingWorld.refreshArmy(gbId, dto)
        p.wingWorld.armyVer = armyVer
        self.refreshInfo()
        gameglobal.rds.ui.wingWorldArmy.refreshMarshalPanel()
