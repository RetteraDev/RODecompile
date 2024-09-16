#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServerTopRankCombatScoreAndLvProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import events
import utils
import const
import uiUtils
import uiConst
from uiProxy import UIProxy
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis.asObject import MenuManager
from gamestrings import gameStrings
from cdata import ns_guild_prestige_act_bonus_data as NGPABD
from data import bonus_data as BD
PRIVIEGE_DAY_TO_SECOND = 86400

class NewServerTopRankCombatScoreAndLvProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServerTopRankCombatScoreAndLvProxy, self).__init__(uiAdapter)
        self.widget = None

    def reset(self):
        pass

    def setType(self, panelType):
        self.panelType = panelType
        self.widget.panelNode.ruleNode.selectedIndex = -1
        p = BigWorld.player()
        if self.panelType == const.NEW_SERVICE_TOP_RANK_COMBAT_SCORE:
            self.topType = gametypes.TOP_TYPE_COMBAT_SCORE
            self.stage = utils.getNewServerPropertyRankActStageClient(self.topType, p.combatScoreList[const.COMBAT_SCORE])
            if self.stage <= 0:
                self.stage = 0
            p.base.getNSCombatScorePropertyRank(self.stage)
        elif self.panelType == const.NEW_SERVICE_TOP_RANK_COMBAT_LV:
            self.topType = gametypes.TOP_TYPE_LEVEL
            self.stage = utils.getNewServerPropertyRankActStageClient(self.topType, (p.lv, utils.getTotalSkillEnhancePoint(p)))
            if self.stage <= 0:
                self.stage = 0
            p.base.getNSLevelPropertyRank(self.stage)
        self.rankData = self.lvRankData or self.combatRankData
        self.initUI()

    def initPanel(self, widget):
        self.widget = widget
        self.topType = None
        self.rankData = None
        self.panelType = None
        self.stage = 0
        self.timer = None
        self.lvRankData = None
        self.combatRankData = None
        self.topLen = None
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.topType = None
        self.rankData = None
        self.panelType = None
        self.topLen = None
        self.cleanTimer()

    def setDataAndRefresh(self, topType, topLen, data):
        self.rankData = data
        self.topLen = topLen
        if topType == gametypes.TOP_TYPE_LEVEL:
            self.lvRankData = self.rankData
            gameglobal.rds.ui.newServiceActivities.updateActiviesTabLevelRedPot()
        elif topType == gametypes.TOP_TYPE_COMBAT_SCORE:
            self.combatRankData = self.rankData
            gameglobal.rds.ui.newServiceActivities.updateActiviesTabCombatRedPot()
        self.initUI()

    def initUI(self):
        if self.rankData == None or not self.panelType:
            return
        else:
            self.initEvent()
            self.initDropDown()
            self.initListProp()
            self.initTopHead()
            self.initMyRank()
            self.updateTimer()
            return

    def initEvent(self):
        self.widget.panelNode.getRewardBtn.addEventListener(events.BUTTON_CLICK, self.onGetRewardClick, False, 0, True)

    def onGetRewardClick(self, *args):
        p = BigWorld.player()
        p.base.applyNSActivityReward(self.topType, self.stage)

    def initMyRank(self):
        p = BigWorld.player()
        myAvatarInfo = None
        for avatarInfo in self.rankData:
            if avatarInfo[5] == p.gbId and avatarInfo[0] != 0:
                myAvatarInfo = avatarInfo

        if myAvatarInfo:
            if not gameglobal.rds.ui.newServiceActivities.checkCombatAndLvOpen(self.topType):
                self.widget.panelNode.getRewardBtn.visible = False
            else:
                self.widget.panelNode.getRewardBtn.visible = True
                self.widget.panelNode.getRewardBtn.label = gameStrings.NEW_SERVER_TOP_LV_REWARD_GET_LABEL
            if myAvatarInfo[2]:
                self.widget.panelNode.getRewardBtn.enabled = False
                self.widget.panelNode.getRewardBtn.label = gameStrings.NEW_SERVER_TOP_LV_REWARD_HAS_GET_LABEL
            else:
                self.widget.panelNode.getRewardBtn.enabled = True
            self.widget.panelNode.myRank.text = gameStrings.NEW_SERVER_MY_RANK % myAvatarInfo[0]
        else:
            self.widget.panelNode.myRank.text = gameStrings.NEW_SERVER_MY_RANK % gameStrings.NEW_SERVER_NOT_IN_RANK_1
            self.widget.panelNode.getRewardBtn.visible = False

    def initDropDown(self):
        self.typeList = []
        allData = utils.getNSPropertyRankActData(self.topType)
        openStage = utils.getEnableNewServerPropertyRankActStages(self.topType)
        if self.topType == gametypes.TOP_TYPE_LEVEL:
            for i in range(max(openStage) + 1, 3):
                openStage.append(i)

        openStage = sorted(openStage)
        for stage in openStage:
            value = allData[stage]
            propertyTarget = value.get('propertyTarget', None)
            if not propertyTarget:
                continue
            if self.topType == gametypes.TOP_TYPE_LEVEL:
                self.typeList.append({'label': gameStrings.NEW_SERVER_LV_LABEL % propertyTarget[0],
                 'index': stage})
            else:
                self.typeList.append({'label': gameStrings.NEW_SERVER_COMBATSCORE_LABEL % propertyTarget,
                 'index': stage})

        self.widget.panelNode.ruleNode.menuRowCount = len(self.typeList)
        ASUtils.setDropdownMenuData(self.widget.panelNode.ruleNode, sorted(self.typeList))
        self.widget.panelNode.ruleNode.addEventListener(events.INDEX_CHANGE, self.handleListChange)
        selectedIndex = 0
        for i, value in enumerate(self.typeList):
            if value['index'] == self.stage:
                selectedIndex = i
                break

        if self.widget.panelNode.ruleNode.selectedIndex != selectedIndex:
            self.widget.panelNode.ruleNode.selectedIndex = selectedIndex
            self.widget.panelNode.ruleNode.validateNow()
            self.handleListChange()

    def initListProp(self):
        allData = self.getBonus()
        for i in range(8):
            item = getattr(self.widget.panelNode, 'line%s' % i)
            if i >= len(allData):
                item.visible = False
            else:
                data = allData[i]
                self.itemFunc(data, item)

    def getBonus(self):
        bonusList = []
        data = utils.getNSPropertyRankActData(self.topType)
        if self.stage > len(data) - 1:
            return []
        rankBonus = data[self.stage].get('rankBonus', {})
        for k, v in rankBonus.items():
            bonusList.append((k, v))

        return sorted(bonusList, key=lambda value: value[0][0])

    def itemFunc(self, data, item):
        item.leftText.visible = True
        item.leftLabel.visible = True
        item.leftLabel.text = gameStrings.NEW_SERVER_LEFT_NUM
        if data[0][0] == data[0][1]:
            item.rankText.text = gameStrings.NEW_SERVER_TOP_RANK % data[0][0]
            if self.topLen != None:
                if data[0][0] <= self.topLen:
                    item.leftText.visible = False
                    item.leftLabel.text = gameStrings.NEW_SERVER_EMPTY
                else:
                    item.leftText.text = 1
        elif data[0][0] == self.getBonus()[len(self.getBonus()) - 1][0][0]:
            item.leftText.visible = False
            item.leftLabel.visible = False
            item.rankText.text = gameStrings.NEW_SERVER_ALL_PEOPLE_REWARD
        else:
            item.rankText.text = gameStrings.NEW_SERVER_TOP_RANK % (str(data[0][0]) + '-' + str(data[0][1]))
            if self.topLen != None:
                if data[0][0] <= self.topLen < data[0][1]:
                    item.leftText.text = data[0][1] - self.topLen
                elif self.topLen >= data[0][1]:
                    item.leftText.visible = False
                    item.leftLabel.text = gameStrings.NEW_SERVER_EMPTY
                elif self.topLen < data[0][0]:
                    item.leftText.text = data[0][1] - data[0][0] + 1
        fixedBonus = BD.data.get(data[1], {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        for i in range(0, 10):
            itemNode = getattr(item, 'item%s' % i)
            if itemNode:
                itemNode.slot.dragable = False
                if i + 1 > len(fixedBonus):
                    itemNode.visible = False
                else:
                    itemNode.slot.visible = True
                    itemId = fixedBonus[i][1]
                    itemCount = fixedBonus[i][2] if len(fixedBonus[i]) > 2 else 1
                    info = uiUtils.getGfxItemById(itemId, count=itemCount)
                    itemNode.slot.setItemSlotData(info)

    def getItemByBonusId(self, bonusId):
        itemList = []
        bonusInfo = NGPABD.data.get(bonusId)
        if not bonusInfo:
            return itemList
        for value in bonusInfo:
            if value.get('bonusId'):
                itemList.append(value.get('bonusId'))

        return itemList

    def handleListChange(self, *args):
        p = BigWorld.player()
        self.stage = self.typeList[self.widget.panelNode.ruleNode.selectedIndex]['index']
        if self.topType == gametypes.TOP_TYPE_COMBAT_SCORE:
            if self.stage <= 0:
                self.stage = 0
            p.base.getNSCombatScorePropertyRank(self.stage)
        elif self.topType == gametypes.TOP_TYPE_LEVEL:
            if self.stage <= 0:
                self.stage = 0
            p.base.getNSLevelPropertyRank(self.stage)

    def updateTimer(self):
        configData = utils.getNSPropertyRankActData(self.topType)
        if self.stage > len(configData) - 1:
            self.cleanTimer()
            return
        else:
            enableTime = configData[self.stage].get('enableTime', None)
            if not enableTime:
                self.cleanTimer()
                return
            periodType, nWeeksOffset, nLastWeeks = enableTime
            tStart, tEnd = utils.calcTimeDuration(periodType, utils.getServerOpenTime(), nWeeksOffset, nLastWeeks)
            if tStart <= utils.getNow() <= tEnd:
                leftTime = tEnd - utils.getNow()
            elif utils.getNow() < tStart:
                leftTime = -1
            else:
                leftTime = 0
            if leftTime > PRIVIEGE_DAY_TO_SECOND:
                timeText = utils.formatTimeStr(leftTime, formatStr=gameStrings.TEXT_NEWSERVERTOPRANKCOMBATSCOREANDLVPROXY_262)
            elif leftTime <= PRIVIEGE_DAY_TO_SECOND and leftTime >= 3600:
                timeText = utils.formatTimeStr(leftTime, formatStr=gameStrings.TEXT_NEWSERVERTOPRANKCOMBATSCOREANDLVPROXY_265)
            else:
                timeText = utils.formatTimeStr(leftTime, formatStr=gameStrings.TEXT_NEWSERVERTOPRANKCOMBATSCOREANDLVPROXY_267)
            if self.widget:
                if leftTime == 0:
                    self.widget.panelNode.timeText.text = gameStrings.NEW_SERVER_TOP_RANK_END
                elif leftTime == -1:
                    self.widget.panelNode.timeText.text = gameStrings.NEW_SERVER_TOP_RANK_NOT_START
                else:
                    self.widget.panelNode.timeText.text = gameStrings.LEFT_TIME % timeText
            if leftTime > 0:
                self.timer = BigWorld.callback(1, self.updateTimer)
            else:
                self.cleanTimer()
            return

    def cleanTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def initTopHead(self):
        configData = utils.getNSPropertyRankActData(self.topType)
        propertyTarget = configData[self.stage].get('propertyTarget', None)
        if propertyTarget:
            if self.topType == gametypes.TOP_TYPE_COMBAT_SCORE:
                self.widget.panelNode.titleNode.gotoAndPlay('zhanli')
                subStr = gameStrings.NEW_SERVER_COMBATSCORE_LABEL % propertyTarget
                self.widget.panelNode.titleNode.titleText.text = str(propertyTarget / 10000) + 'W'
            elif self.topType == gametypes.TOP_TYPE_LEVEL:
                if int(propertyTarget[1]) <= 0:
                    self.widget.panelNode.titleNode.gotoAndPlay('mubiao')
                    self.widget.panelNode.titleNode.titleText.text = str(propertyTarget[0])
                else:
                    self.widget.panelNode.titleNode.gotoAndPlay('xiu')
                    self.widget.panelNode.titleNode.titleText.text = str(propertyTarget[0])
                    self.widget.panelNode.titleNode.xiuText.text = str(propertyTarget[1])
        for i in range(1, 4):
            topNode = getattr(self.widget.panelNode, 'top%s' % i)
            topNode.headIcon.url = ''
            topNode.headIcon.loadImage('')
            topNode.headIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
            topNode.headIcon.fitSize = True
            findValue = None
            for value in self.rankData:
                if value[0] == i:
                    findValue = value

            if findValue:
                topNode.headIcon.url = findValue[4]
                topNode.roleName.text = findValue[3]
                menuParam = {'roleName': findValue[3],
                 'gbId': long(findValue[5])}
                MenuManager.getInstance().registerMenuById(topNode, uiConst.MENU_ACHIEVEMENT_TOPRANK, menuParam, events.RIGHT_BUTTON)
            else:
                topNode.headIcon.url = ''
                topNode.roleName.text = gameStrings.NEW_SERVER_NOT_IN_RANK_2
