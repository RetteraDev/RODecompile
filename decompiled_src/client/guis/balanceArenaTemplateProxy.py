#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArenaTemplateProxy.o
import random
import BigWorld
import gameglobal
import gametypes
import uiConst
import events
import utils
import formula
from guis.asObject import TipManager
from guis.asObject import MenuManager
from guis.asObject import ASUtils
from guis import asObject
from data import sys_config_data as SCD
from asObject import ASObject
from uiProxy import UIProxy
from gamestrings import gameStrings
TEMPLATE_ITEM_CLS = 'BalanceArenaTemplate_TemplateItem'
RANK_ITEM_NUM = 5
SUPPORT_MOVE_X = 240
VIEW_MOVE_X = 311

class BalanceArenaTemplateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceArenaTemplateProxy, self).__init__(uiAdapter)
        self.widget = None
        self.cache = {}
        self.school = 0
        self.monthRank = []
        self.totalRank = []
        self.randomSeed = random.randint(0, 1000)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BALANCE_ARENA_TEMPLATE, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BALANCE_ARENA_TEMPLATE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BALANCE_ARENA_TEMPLATE)

    def onGetServerData(self, data):
        if data != None:
            self.cache = {}
            for key in data:
                if data[key]:
                    self.cache[key] = data[key]

            self.genMonthRankList()
            if not self.widget:
                self.uiAdapter.loadWidget(uiConst.WIDGET_BALANCE_ARENA_TEMPLATE)
            else:
                self.refreshInfo()

    def onGetTotalRankData(self, data):
        self.totalRank = []
        if data:
            for dataItem in data[1]:
                itemInfo = {}
                itemInfo['roleName'] = dataItem.get(gametypes.TOP_UNIVERSAL_ROLE_NAME, '')
                itemInfo['heatMonthly'] = dataItem.get(gametypes.TOP_UNIVERSAL_VALUE, (0, 0))[0]
                itemInfo['hostId'] = dataItem.get(gametypes.TOP_UNIVERSAL_VALUE, (0, 0))[1]
                self.totalRank.append(itemInfo)

    def useCharTempSuccess(self, tempId):
        if self.widget:
            self.refreshInfo()

    def queryServerData(self):
        p = BigWorld.player()
        p.base.queryPersonalCharTempInfo(self.school)
        p.base.queryCharTempHeat(0, str(self.school))

    def show(self, school = 0):
        if not school:
            p = BigWorld.player()
            self.school = p.school
        else:
            self.school = school
        if self.cache != None:
            if not self.widget:
                self.uiAdapter.loadWidget(uiConst.WIDGET_BALANCE_ARENA_TEMPLATE)
            else:
                self.refreshInfo()
        self.queryServerData()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.randomCkBox.visible = False
        self.widget.templateList.itemRenderer = TEMPLATE_ITEM_CLS
        self.widget.templateList.lableFunction = self.templateLableFunc
        self.widget.randomCkBox.addEventListener(events.EVENT_SELECT, self.onRandomChange, False, 0, True)
        self.widget.monthRankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick, False, 0, True)
        self.widget.totalRankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick, False, 0, True)
        self.setHelpInfo()

    def setHelpInfo(self):
        p = BigWorld.player()
        self.widget.helpIcon1.helpKey = 393
        self.widget.helpIcon2.helpKey = 394
        self.widget.helpBtn.helpKey = 395
        if formula.isBalanceArenaCrossServerML(formula.getMLGNo(p.spaceNo)):
            TipManager.addTip(self.widget.helpIcon1, SCD.data.get('balanceArenaTip1', ''))
            TipManager.addTip(self.widget.helpIcon2, SCD.data.get('balanceArenaTip2', ''))
            self.widget.helpBtn.visible = False

    def onRankBtnClick(self, *args):
        e = ASObject(args[3][0])
        self.widget.monthRankBtn.selected = False
        self.widget.totalRankBtn.selected = False
        e.target.selected = True
        if e.target == self.widget.monthRankBtn:
            self.showMonthRank()
        else:
            self.showTotalRank()

    def onRandomChange(self, *args):
        pass

    def genMonthRankList(self):
        tempList = [ self.cache[key] for key in self.cache ]
        tempList.sort(self.compRankItem)
        self.monthRank = tempList

    def compRankItem(self, x, y, key = 'heatMonthly'):
        if x.get(key, 0) < y.get(key, 0):
            return 1
        if x.get(key, 0) > y.get(key, 0):
            return -1
        return 0

    def setRankList(self, rankList):
        for i in xrange(RANK_ITEM_NUM):
            rankNumItem = self.widget.getChildByName('topNum%s' % str(i + 1))
            rankitem = self.widget.getChildByName('top%s' % str(i + 1))
            if rankitem:
                rankitem.visible = False
            if rankNumItem:
                rankNumItem.visible = False

        maxHotNum = 0
        for i, data in enumerate(rankList):
            if i >= RANK_ITEM_NUM:
                break
            rankitem = self.widget.getChildByName('top%s' % str(i + 1))
            rankNumItem = self.widget.getChildByName('topNum%s' % str(i + 1))
            hostId = data.get('hostId', 0)
            if hostId:
                playerName = '%s-%s' % (data.get('roleName', ''), utils.getServerName(hostId))
            else:
                playerName = data.get('roleName', '')
            hotNum = data.get('heatMonthly', 0)
            src = data.get('src', 0)
            if i == 0:
                maxHotNum = hotNum
            rankitem.visible = True
            rankNumItem.visible = True
            rankitem.playerName.text = playerName
            rankitem.hotNum.text = hotNum
            if src:
                rankitem.source.visible = True
                rankitem.source.gotoAndStop(str(src))
            else:
                rankitem.source.visible = False
            rankitem.hotProgress.maxValue = maxHotNum + 1
            rankitem.hotProgress.currentValue = hotNum + 1

    def showMonthRank(self):
        self.setRankList(self.monthRank)

    def showTotalRank(self):
        self.setRankList(self.totalRank)

    def isNew(self, lastCheckTime):
        return True

    def templateLableFunc(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        p = BigWorld.player()
        templateId = getattr(data, 'lastTempId', 0)
        name = '%s-%s' % (getattr(data, 'roleName', ''), utils.getServerName(getattr(data, 'hostId', 0)))
        if getattr(data, 'lastVersion', 1) == 0:
            name += '-Need To Check'
        elif getattr(data, 'lastVersion', 1) >= 2:
            name += '-Waiting to Publish:%d' % getattr(data, 'lastVersion', 0)
        useNum = long(getattr(data, 'useCount', 0L))
        supportNum = long(getattr(data, 'totalZan', 0L)) + long(getattr(data, 'zanMonthly', 0L))
        photoUrl = getattr(data, 'photo', '')
        isNew = self.isNew(getattr(data, 'lastCheckTime', 0))
        charTempId = getattr(p, 'charTempId', -1)
        playerGbId = getattr(data, 'gbID', 0)
        item.templateId = templateId
        item.gbId = str(playerGbId)
        item.hostId = str(getattr(data, 'hostId', 0))
        item.playerName.text = name
        item.useText.text = gameStrings.BALANCE_ARENA_USESTR % useNum
        item.supportText.text = gameStrings.BALANCE_ARENA_ZANSTR % supportNum
        item.photo.fitSize = True
        item.photo.imgType = uiConst.IMG_TYPE_NOS_FILE
        item.photo.serverId = getattr(data, 'hostId', 0)
        item.photo.setContentUnSee()
        item.photo.url = photoUrl
        item.isSelectIcon.visible = long(charTempId) == long(templateId)
        item.isNewIcon.visible = isNew
        item.homeBtn.addEventListener(events.BUTTON_CLICK, self.onHomeBtnClick, False, 0, True)
        item.chatBtn.addEventListener(events.BUTTON_CLICK, self.onChatBtnClick, False, 0, True)
        item.supportBtn.addEventListener(events.BUTTON_CLICK, self.onSupportBtnClick, False, 0, True)
        item.previewBtn.addEventListener(events.BUTTON_CLICK, self.onPreviewBtnClick, False, 0, True)
        item.selectBtn.addEventListener(events.BUTTON_CLICK, self.onSelectBtnClick, False, 0, True)
        if not formula.isBalanceArenaCrossServerML(formula.getMLGNo(p.spaceNo)):
            item.supportBtn.x = SUPPORT_MOVE_X
            item.previewBtn.x = VIEW_MOVE_X
            item.selectBtn.visible = False
        menuParam = {'roleName': name,
         'gbId': long(playerGbId),
         'hostId': getattr(data, 'hostId', 0)}
        MenuManager.getInstance().registerMenuById(item.photo, uiConst.MENU_BALANCE_ARENA_TEMPLATE, menuParam)

    def onHomeBtnClick(self, *args):
        e = ASObject(args[3][0])
        templateId = e.target.parent.templateId
        gbId = e.target.parent.gbId
        hostId = e.target.parent.hostId
        if gbId:
            p = BigWorld.player()
            p.getPersonalSysProxy().openZoneOther(long(gbId), hostId=long(hostId))

    def onChatBtnClick(self, *args):
        e = ASObject(args[3][0])
        templateId = e.target.parent.templateId
        gbId = e.target.parent.gbId
        hostId = e.target.parent.hostId
        if gbId:
            p = BigWorld.player()
            p.getPersonalSysProxy().openZoneOther(long(gbId), hostId=long(hostId), autoOpenChat=True)

    def onSupportBtnClick(self, *args):
        e = ASObject(args[3][0])
        gbId = e.target.parent.gbId
        p = BigWorld.player()
        p.base.zanCharTemp(long(gbId))

    def onPreviewBtnClick(self, *args):
        e = ASObject(args[3][0])
        templateId = e.target.parent.templateId
        gameglobal.rds.ui.balanceArenaPreview.show(templateId)

    def onSelectBtnClick(self, *args):
        e = ASObject(args[3][0])
        templateId = e.target.parent.templateId
        p = BigWorld.player()
        p.cell.useCharTemp(long(templateId), gametypes.CHAR_TEMP_TYPE_ARENA)

    def getUseAndZan(self, gbId):
        if self.cache.has_key(gbId):
            tempData = self.cache.get(gbId, {})
            useNum = long(tempData.get('useCount', 0L))
            supportNum = long(tempData.get('totalZan', 0L)) + long(tempData.get('zanMonthly', 0L))
            return (useNum, supportNum)
        return (0, 0)

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            random.seed(self.randomSeed)
            if self.cache != None:
                templateList = self.cache
                dataArr = []
                for key in templateList.keys():
                    dataArr.append(templateList.get(key, {}))

                random.shuffle(dataArr)
                self.sortTempList(dataArr)
                self.widget.templateList.dataArray = dataArr
                self.widget.monthRankBtn.selected = True
                self.widget.totalRankBtn.selected = False
                self.showMonthRank()
            return

    def sortTempList(self, templateList):
        templateList.sort(cmp=self.compTempItem)

    def compTempItem(self, x, y):
        p = BigWorld.player()
        if str(x.get('lastTempId', 0)) == str(getattr(p, 'charTempId', -1)):
            return -1
        if str(y.get('lastTempId', 0)) == str(getattr(p, 'charTempId', -1)):
            return 1
        return 0
