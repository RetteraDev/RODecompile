#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ransackProxy.o
import BigWorld
import uiConst
import events
import gamelog
import formula
import utils
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import ui
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis import uiUtils
RANK_LEN = 10
MIN_PAGE_NUM = 1
SELF_TXT_COLOR = '#FFC961'
from data import sky_wing_challenge_config_data as SWCCD

class RansackProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RansackProxy, self).__init__(uiAdapter)
        self.widget = None
        self.clearAll()
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANSACK_POINT, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RANSACK_POINT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearAll(self):
        self.rankData = {}
        self.version = 0
        self.selfRank = 1
        self.queryStartRank = 1
        self.queryEndRank = 1
        self.protectDic = {}

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RANSACK_POINT)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_RANSACK_POINT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        ransackTips = SWCCD.data.get('ransackTips', ('', '', ''))
        self.widget.txtDesc0.htmlText = ransackTips[0]
        self.widget.txtDesc1.htmlText = ransackTips[1]
        self.widget.txtDesc2.htmlText = ransackTips[2]
        self.widget.helpIcon.helpKey = SWCCD.data.get('ransackHelpIconKey', 0)
        self.widget.scrollWndList.itemRenderer = 'Ransack_ItemRender'
        self.widget.scrollWndList.lableFunction = self.lableFunction
        self.widget.scrollWndList.itemHeight = 35
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshBtnClick, False, 0, True)
        self.refreshTimer()

    def refreshTimer(self):
        if not self.widget:
            return
        for itemMc in self.widget.scrollWndList.items:
            self.updateItemSansack(itemMc, int(itemMc.gbId))

        BigWorld.callback(1, self.refreshTimer)

    def lableFunction(self, *args):
        rankKey = int(args[3][0].GetNumber())
        itemMc = ASObject(args[3][1])
        itemData = self.rankData.get(rankKey, None)
        gamelog.info('jbx:lableFunction', rankKey, itemData)
        if not itemData:
            return
        else:
            isSelf = itemData['isSelf']
            itemMc.gbId = itemData['gbId']
            itemMc.txtRank.htmlText = str(itemData['rank']) if not isSelf else uiUtils.toHtml(str(itemData['rank']), SELF_TXT_COLOR)
            itemMc.txtName.htmlText = str(itemData['name']) if not isSelf else uiUtils.toHtml(str(itemData['name']), SELF_TXT_COLOR)
            itemMc.jobIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC[itemData['school']])
            itemMc.rank = rankKey
            if isSelf:
                itemMc.state.visible = False
            if itemData['isReduce']:
                itemMc.state.visible = True
                itemMc.state.gotoAndStop('shuai')
                TipManager.addTip(itemMc.state, SWCCD.data.get('shuai', ''))
            elif itemData['isEnmey']:
                itemMc.state.visible = True
                itemMc.state.gotoAndStop('chou')
                TipManager.addTip(itemMc.state, SWCCD.data.get('chou', ''))
            elif itemData['isFriend']:
                itemMc.state.visible = True
                itemMc.state.gotoAndStop('you')
                TipManager.addTip(itemMc.state, SWCCD.data.get('you', ''))
            else:
                itemMc.state.visible = False
            itemMc.txtGuildName.htmlText = itemData['guildName'] if not isSelf else uiUtils.toHtml(itemData['guildName'], SELF_TXT_COLOR)
            itemMc.txtPoint.htmlText = itemData['value'] if not isSelf else uiUtils.toHtml(itemData['value'], SELF_TXT_COLOR)
            self.updateItemSansack(itemMc, itemData['gbId'])
            if itemData['sameGuild']:
                itemMc.sansackBtn.visible = False
                itemMc.txtGuild.visible = True
                if isSelf:
                    itemMc.txtGuild.htmlText = uiUtils.toHtml(itemMc.txtGuild.text, SELF_TXT_COLOR)
                else:
                    itemMc.txtGuild.htmlText = itemMc.txtGuild.text
            else:
                itemMc.sansackBtn.visible = True
                itemMc.txtGuild.visible = False
                itemMc.sansackBtn.addEventListener(events.BUTTON_CLICK, self.handleRansackBtnClick, False, 0, True)
            return

    def updateItemSansack(self, itemMc, gbId):
        timeStamp = self.protectDic.get(gbId, 0)
        passTime = utils.getNow() - timeStamp
        cd = SWCCD.data.get('beRobCD', 180)
        if passTime >= cd:
            itemMc.sansackBtn.enabled = True
            itemMc.sansackBtn.label = gameStrings.BAIDI_SHILIAN_ROB_LABEL
        else:
            itemMc.sansackBtn.enabled = False
            itemMc.sansackBtn.label = gameStrings.BAIDI_SHILIAN_ROB_LABEL_CD % (cd - passTime)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshRank(True)

    @ui.callInCD(1.5)
    def sendRefreshRank(self):
        BigWorld.player().base.getTopSkyWingRob(self.version)
        gamelog.info('jbx:getTopSkyWingRob', self.version)

    def onReceiveRankData(self, data):
        gamelog.info('jbx:onReceiveRankData', data)
        p = BigWorld.player()
        mData, selfRank, queryStartRank, enemyList, reduceList, protectList, self.version = data
        beRobCD = SWCCD.data.get('beRobCD', 180)
        self.protectDic = {}
        for gbId, cd in protectList:
            self.protectDic[gbId] = utils.getNow() - (beRobCD - cd)

        self.selfRank = selfRank
        self.queryStartRank = queryStartRank
        self.rankData.clear()
        for index, dataInfo in enumerate(mData):
            gbId, name, school, value, timeStamp, guildNuid, guildName = dataInfo
            info = {}
            info['isSelf'] = gbId == p.gbId
            info['rank'] = queryStartRank + index
            info['school'] = school
            info['name'] = name
            info['value'] = value
            info['isEnmey'] = gbId in enemyList
            info['isFriend'] = p.friend.isFriend(gbId)
            info['isReduce'] = gbId in reduceList
            info['guildName'] = guildName
            info['guildNuid'] = guildNuid
            info['gbId'] = gbId
            info['sameGuild'] = guildNuid == p.guildNUID
            self.rankData[queryStartRank + index] = info
            self.queryEndRank = queryStartRank + index

        self.refreshRank()

    def refreshRank(self, force = False):
        if not self.widget:
            return
        else:
            rankKeyList = []
            for index in range(self.queryStartRank, self.queryEndRank + 1):
                rankData = self.rankData.get(index, None)
                rankData and rankKeyList.append(index)

            self.widget.scrollWndList.dataArray = rankKeyList
            self.widget.scrollWndList.validateNow()
            subValue = self.queryEndRank - self.queryStartRank
            if subValue > 0:
                self.widget.scrollWndList.scrollbar.position = 733 * ((self.selfRank - self.queryStartRank) * 1.0 / (self.queryEndRank - self.queryStartRank))
            if not len(rankKeyList) or force:
                self.sendRefreshRank()
            return

    def handleRansackBtnClick(self, *args):
        e = ASObject(args[3][0])
        rankKey = int(e.currentTarget.parent.rank)
        rankData = self.rankData.get(rankKey, None)
        gamelog.info('jbx:handleRansackBtnClick', rankKey, rankData)
        if not rankData:
            return
        else:
            rank = rankData['rank']
            score = rankData['value']
            p = BigWorld.player()
            p.cell.applySkyWingRob(rankData['gbId'], rankData['name'], rankData['guildNuid'], rankData['guildName'])
            fbNo = formula.getFubenNo(p.spaceNo)
            if formula.inSkyWingChallengeFuben(fbNo) or formula.inSkyWingRobFuben(fbNo):
                self.hide()
                self.uiAdapter.baiDiShiLian.hide()
            gamelog.info('jbx:applySkyWingRob', rankData['gbId'], rankData['name'], rankData['guildNuid'], rankData['guildName'])
            return

    def handleRefreshBtnClick(self, *args):
        gamelog.info('jbx:handleRefreshBtnClick')
        self.refreshRank(True)
