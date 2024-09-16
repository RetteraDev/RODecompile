#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/baiDiShiLianProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import utils
import gamelog
import formula
import const
from gamestrings import gameStrings
import gametypes
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import MenuManager
from guis import ui
from guis import uiUtils
from data import sky_wing_challenge_config_data as SWCCD
from cdata import sky_wing_challenge_scheduler_data as SWCSD
from cdata import game_msg_def_data as GMDD
PROGRESS_STAGE_ONE = 1
PROGRESS_STATE_TWO = 2
PROGRESS_STAGE_THREE = 3
PROGRESS_STAGE_CNT = 3
RANK_TOTAL = 1
RANK_SCHOOL = 2
RANK_GUILD = 3
RANK_COLOR_SELF = '#C3A160'
RANK_MAX_LEN = 200
LOG_LIST_MAX_LEN = 50
CHALLENGE_BTN_CD = 60
RANSACK_BTN_CD = 45
REFRESH_BTN_CD = 5
PROGRESSBAR_LINE_POS_RANGE = (38, 557)
STAGE_TITLE_POS_RANGE = (417, 936)
FIRST_PLACE = 1
SECOND_PLACE = 2
THIRD_PLACE = 3
RANK_MAX_LEN = 30

class BaiDiShiLianProxy(UIProxy):

    def __init__(self, uiAdapter):
        global RANSACK_BTN_CD
        global CHALLENGE_BTN_CD
        super(BaiDiShiLianProxy, self).__init__(uiAdapter)
        self.widget = None
        self.skyWingPassTime = -1
        self.startTime = 0
        self.rankData = {}
        self.selfRankInfo = {}
        self.rankVerData = {}
        self.logList = []
        self.selfLogList = []
        self.isOnlyShowSelfLog = False
        self.lastChallengeTime = 0
        self.lastRansackTime = 0
        self.lastRefreshTime = 0
        self.isEnd = False
        self.selfScore = 0
        self.reset()
        CHALLENGE_BTN_CD = SWCCD.data.get('challengeCD', 180)
        RANSACK_BTN_CD = SWCCD.data.get('robCD', 180)
        uiAdapter.registerEscFunc(uiConst.WIDGET_BAIDI_SHILIAN, self.hide)

    def reset(self):
        self.timer = None
        self.selectedRank = RANK_TOTAL
        self.isSelectedLowLv = True
        self.stageTimes = []

    def clearAll(self):
        self.lastRansackTime = 0
        self.startTime = 0
        self.skyWingPassTime = -1
        self.lastRefreshTime = 0
        self.logList = []
        self.selfLogList = []
        self.selfScore = 0
        self.rankData = {}
        self.selfRankInfo = {}
        self.rankVerData = {}
        self.logList = []
        self.selfLogList = []
        self.isOnlyShowSelfLog = False
        self.lastChallengeTime = 0
        self.isEnd = False
        self.selfScore = 0

    def onSkyWingStart(self):
        self.startTime = 0
        self.rankData = {}
        self.selfRankInfo = {}
        self.rankVerData = {}
        self.logList = []
        self.selfLogList = []
        self.isOnlyShowSelfLog = False
        self.lastChallengeTime = 0
        self.lastRansackTime = 0
        self.lastRefreshTime = 0
        self.isEnd = False
        self.selfScore = 0
        self.refreshInfo()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BAIDI_SHILIAN:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BAIDI_SHILIAN)

    def show(self):
        if not gameglobal.rds.configData.get('enableSkyWingChallenge', False):
            return
        p = BigWorld.player()
        if p._isSoul():
            p.showGameMsg(GMDD.data.BAIDISHILIAN_SOUL, ())
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BAIDI_SHILIAN)
            lowLv = gametypes.LV_1_69_RANGE
            self.isSelectedLowLv = p.lv <= lowLv[1]

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.helpIcon.helpKey = SWCCD.data.get('skyWingHelpKey', 0)
        self.widget.lowLvBtn.label = 'Lv.%d~%d' % SWCCD.data.get('rankLowLv', gametypes.LV_1_69_RANGE)
        rankHighLv = SWCCD.data.get('rankHighLv', gametypes.LV_70_79_RANGE)
        if gameglobal.rds.configData.get('enableTopRankNewLv89', False):
            rankHighLv = list(rankHighLv)
            rankHighLv[1] = 89
            rankHighLv = tuple(rankHighLv)
        self.widget.highLvBtn.label = 'Lv.%d~%d' % rankHighLv
        self.widget.rankTotalBtn.addEventListener(events.BUTTON_CLICK, self.handleRankTotalBtnClick, False, 0, True)
        self.widget.rankSchoolBtn.addEventListener(events.BUTTON_CLICK, self.handleRankSchoolBtnClick, False, 0, True)
        self.widget.rankGuildBtn.addEventListener(events.BUTTON_CLICK, self.handleRankGuildBtnClick, False, 0, True)
        self.widget.lowLvBtn.addEventListener(events.BUTTON_CLICK, self.handleLowLvBtnClick, False, 0, True)
        self.widget.highLvBtn.addEventListener(events.BUTTON_CLICK, self.handleHighLvBtnClick, False, 0, True)
        self.widget.challengeBtn.addEventListener(events.BUTTON_CLICK, self.handleChannlengeBtnClick, False, 0, True)
        self.widget.ransackBtn.addEventListener(events.BUTTON_CLICK, self.handleRansackBtnClick, False, 0, True)
        self.widget.scrollWndList.lableFunction = self.rankLableFuncition
        self.widget.onlySelfChk.selected = self.isOnlyShowSelfLog
        self.widget.txtDesc.text = SWCCD.data.get('tipsDesc', '')
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshBtnClick, False, 0, True)
        self.widget.onlySelfChk.addEventListener(events.BUTTON_CLICK, self.handleOnlySelfChkClick, False, 0, True)
        self.stageTimes = []
        self.stageTimes.append(0)
        self.stageTimes.append(SWCSD.data.get(PROGRESS_STAGE_THREE, {}).get('nextSchedules', {}).get(PROGRESS_STAGE_THREE + 1, 60))
        self.stageTimes.append(SWCSD.data.get(PROGRESS_STATE_TWO, {}).get('nextSchedules', {}).get(PROGRESS_STAGE_THREE, 60))
        self.stageTimes.append(SWCSD.data.get(PROGRESS_STAGE_ONE, {}).get('nextSchedules', {}).get(PROGRESS_STATE_TWO, 60))
        self.refreshTimeProgress()

    def relayoutProgressBar(self):
        offsetTime = 0
        totalTimes = sum(self.stageTimes)
        for i in range(1, PROGRESS_STAGE_CNT):
            lineMc = self.widget.progressBar.getChildByName('line%d' % (i - 1))
            offsetTime += self.stageTimes[i]
            lineMc.x = PROGRESSBAR_LINE_POS_RANGE[0] + offsetTime * 1.0 / totalTimes * (PROGRESSBAR_LINE_POS_RANGE[1] - PROGRESSBAR_LINE_POS_RANGE[0])

        offsetTime = 0
        for i in range(PROGRESS_STAGE_CNT):
            titleMc = self.widget.getChildByName('progress%d' % i)
            offsetTime += self.stageTimes[i]
            titleMc.x = STAGE_TITLE_POS_RANGE[0] + (offsetTime + self.stageTimes[i + 1] / 2) * 1.0 / totalTimes * (STAGE_TITLE_POS_RANGE[1] - STAGE_TITLE_POS_RANGE[0]) - titleMc.width / 2

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshRank(refreshForece=True)
        self.refreshLogList()

    def setFuBenCD(self, challengeCD = 0, ransackCD = 0):
        gamelog.info('jbx:setFuBenCD', challengeCD, ransackCD, utils.getNow(), CHALLENGE_BTN_CD)
        if challengeCD:
            self.lastChallengeTime = utils.getNow() - (CHALLENGE_BTN_CD - challengeCD)
        if ransackCD:
            self.lastRansackTime = utils.getNow() - (RANSACK_BTN_CD - ransackCD)

    def refreshTimeProgress(self):
        if not self.widget:
            return
        else:
            leftTime, totalTime = self.getTime()
            currentValue = leftTime * 1.0 / totalTime * 100
            self.widget.progressBar.currentValue = currentValue
            for i in xrange(PROGRESS_STAGE_CNT):
                progressMc = getattr(self.widget, 'progress%d' % i, None)
                currentValue = min(99, currentValue)
                start = sum(self.stageTimes[:i + 1]) * 1.0 / totalTime * 100
                end = (sum(self.stageTimes[:i + 1]) + self.stageTimes[i + 1]) * 1.0 / totalTime * 100
                if currentValue > end:
                    progressMc.gotoAndStop('frame3')
                elif currentValue < start:
                    progressMc.gotoAndStop('frame1')
                else:
                    progressMc.gotoAndStop('frame2')

            self.widget.txtLeftTime.text = utils.formatTimeStr(int(leftTime), 'm:s', True, 2, 2)
            if utils.getNow() - self.lastChallengeTime < CHALLENGE_BTN_CD:
                self.widget.challengeBtn.enabled = False
                self.widget.challengeBtn.label = gameStrings.BAIDI_SHILIAN_CHALLENGE_IN_CD % (self.lastChallengeTime + CHALLENGE_BTN_CD - utils.getNow())
            else:
                self.widget.challengeBtn.enabled = True
                self.widget.challengeBtn.label = gameStrings.BAIDI_SHILIAN_CHALLENGE
            if utils.getNow() - self.lastRansackTime < RANSACK_BTN_CD:
                self.widget.ransackBtn.enabled = False
                self.widget.ransackBtn.label = gameStrings.BAIDI_SHILIAN_RANSACK_IN_CD % (self.lastRansackTime + RANSACK_BTN_CD - utils.getNow())
            else:
                self.widget.ransackBtn.enabled = True
                self.widget.ransackBtn.label = gameStrings.BAIDI_SHILIAN_RANSACK
            if utils.getNow() - self.lastRefreshTime < REFRESH_BTN_CD:
                self.widget.refreshBtn.enabled = False
                self.widget.refreshBtn.label = gameStrings.BAIDI_SHILIAN_REFRESH_IN_CD % (self.lastRefreshTime + REFRESH_BTN_CD - utils.getNow())
            else:
                self.widget.refreshBtn.enabled = True
                self.widget.refreshBtn.label = gameStrings.BAIDI_SHILIAN_REFRESH
            self.relayoutProgressBar()
            self.timer = BigWorld.callback(1, self.refreshTimeProgress)
            return

    @ui.callInCD(1)
    def refreshRank(self, rankType = None, isLowLv = None, refreshForece = False):
        if not self.widget:
            return
        else:
            if rankType == None:
                rankType = self.selectedRank
            if isLowLv == None:
                isLowLv = self.isSelectedLowLv
            p = BigWorld.player()
            if not refreshForece and rankType == self.selectedRank and isLowLv == self.isSelectedLowLv:
                return
            self.selectedRank = rankType
            self.isSelectedLowLv = isLowLv
            self.widget.lowLvBtn.visible = rankType == RANK_SCHOOL
            self.widget.highLvBtn.visible = rankType == RANK_SCHOOL
            if isLowLv:
                lvRange = gametypes.LV_1_69_RANGE
            else:
                lvRange = gametypes.LV_70_79_RANGE
            if rankType == RANK_TOTAL:
                key = gametypes.ALL_LV_TOP_RANK_KEY
                p.cell.getTopSkyWing(self.rankVerData.get(RANK_TOTAL, 0), key)
                gamelog.info('jbx:getTopSkyWing', self.rankVerData.get(RANK_TOTAL, 0), key)
            elif rankType == RANK_SCHOOL:
                key = '%d_%d_%d' % (lvRange[0], lvRange[1], p.school)
                p.cell.getTopSkyWing(self.rankVerData.get((True, isLowLv), 0), key)
                gamelog.info('jbx:getTopSkyWing', self.rankVerData.get((True, isLowLv), 0), key)
            else:
                p.cell.getTopSkyWingGuild(self.rankVerData.get(RANK_GUILD, 0))
                gamelog.info('jbx:getTopSkyWingGuild', self.rankVerData.get(RANK_GUILD, 0))
            self.refreshRankScrollWndListView()
            return

    def getDataList(self):
        if self.selectedRank in (RANK_TOTAL, RANK_SCHOOL):
            isSelfSchool = self.selectedRank == RANK_SCHOOL
            if self.selectedRank == RANK_TOTAL:
                dataList = self.rankData.get(RANK_TOTAL, [])
            else:
                dataList = self.rankData.get((isSelfSchool, self.isSelectedLowLv), [])
            if self.selectedRank == RANK_SCHOOL:
                dataList = dataList[:10]
        else:
            dataList = self.rankData.get(RANK_GUILD, [])
        dataList = dataList[:RANK_MAX_LEN]
        return dataList

    def getRankInfo(self):
        if self.selectedRank == RANK_TOTAL:
            rankInfo = self.selfRankInfo.get(RANK_TOTAL, (0, 2000))
        elif self.selectedRank == RANK_SCHOOL:
            isSelfSchool = self.selectedRank == RANK_SCHOOL
            rankInfo = self.selfRankInfo.get((isSelfSchool, self.isSelectedLowLv), (0, 2000))
        else:
            rankInfo = self.selfRankInfo.get(RANK_GUILD, (0, 2000))
        return rankInfo

    def getDataByIndex(self, index):
        dataList = self.getDataList()
        if index < len(dataList):
            return dataList[index]
        else:
            return None

    def refreshRankScrollWndListView(self):
        if not self.widget:
            return
        self.widget.rankTotalBtn.selected = self.selectedRank == RANK_TOTAL
        self.widget.rankSchoolBtn.selected = self.selectedRank == RANK_SCHOOL
        self.widget.rankGuildBtn.selected = self.selectedRank == RANK_GUILD
        self.widget.lowLvBtn.selected = self.isSelectedLowLv
        self.widget.highLvBtn.selected = not self.isSelectedLowLv
        if self.selectedRank == RANK_GUILD:
            self.widget.txtGuildProp.visible = True
            self.widget.txtProp0.visible = False
            self.widget.txtProp1.visible = False
        else:
            self.widget.txtGuildProp.visible = False
            self.widget.txtProp0.visible = True
            self.widget.txtProp1.visible = True
        if self.selectedRank in (RANK_TOTAL, RANK_SCHOOL):
            self.widget.scrollWndList.itemRenderer = 'BaiDiShiLian_ItemRender'
            dataList = self.getDataList()
            self.widget.scrollWndList.dataArray = range(len(dataList))
        else:
            self.widget.scrollWndList.itemRenderer = 'BaiDiShiLian_GuildItemRender'
            dataList = self.getDataList()
            self.widget.scrollWndList.dataArray = range(len(dataList))
        self.refreshSelfRankInfo()

    def refreshItemRenderProp(self, rankIndex, isSelf, itemData, itemMc):
        desList = []
        desList.append(str(rankIndex))
        for value in itemData:
            desList.append(str(value))

        itemMc.gotoAndStop('normal')
        if self.selectedRank == RANK_TOTAL and rankIndex in (FIRST_PLACE, SECOND_PLACE, THIRD_PLACE):
            itemMc.gotoAndStop('qian3')
            if rankIndex == FIRST_PLACE:
                itemMc.cup.gotoAndStop('jin')
            elif rankIndex == SECOND_PLACE:
                itemMc.cup.gotoAndStop('ying')
            elif rankIndex == THIRD_PLACE:
                itemMc.cup.gotoAndStop('tong')
        for descIndex, des in enumerate(desList):
            txt = getattr(itemMc, 'txt%d' % descIndex, None)
            if txt:
                txt.htmlText = des if not isSelf else uiUtils.toHtml(des, RANK_COLOR_SELF)

    def rankLableFuncition(self, *args):
        rankIndex = int(args[3][0].GetNumber())
        itemMc = ASObject(args[3][1])
        itemMc.rankIndex = rankIndex
        itemData = self.getDataByIndex(rankIndex)
        gamelog.info('jbx:rankLableFuncition', rankIndex, itemData)
        rankIndex += 1
        p = BigWorld.player()
        if not itemData:
            return
        if self.selectedRank != RANK_GUILD:
            isSelf = p.gbId == itemData[0]
            self.refreshItemRenderProp(rankIndex, isSelf, itemData[1:], itemMc)
            MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_RANK, {'roleName': itemData[1],
             'gbId': itemData[0]})
        else:
            isSelf = p.guildNUID == itemData[0]
            self.refreshItemRenderProp(rankIndex, isSelf, itemData[1:], itemMc)

    def getTime(self):
        if not self.startTime:
            if self.skyWingPassTime >= 0:
                self.startTime = utils.getNow() - self.skyWingPassTime
            else:
                return (0, 100)
        endTime = self.startTime + SWCCD.data.get('duration', 720)
        leftTime = max(0, endTime - utils.getNow())
        return (leftTime, endTime - self.startTime)

    def onProxyDataSend(self, proxyId, data):
        gamelog.info('jbx:onProxyDataSend', proxyId, data)
        if proxyId == const.PROXY_KEY_TOP_SKY_WING_CHALLENGE:
            self.processAvatarData(data)
        elif proxyId == const.PROXY_KEY_TOP_GUILD_SKY_WING_CHALLENGE:
            self.processGuildData(data)

    def processAvatarData(self, data):
        p = BigWorld.player()
        infoList = []
        ver, dataList, myScore, key = data
        strs = key.split('_')
        isRankAll = key == gametypes.ALL_LV_TOP_RANK_KEY
        if isRankAll:
            lvRange = (1, 79)
            school = 0
        else:
            lvRange = (int(strs[0]), int(strs[1]))
            school = int(strs[2])
        isLowLvRange = gametypes.LV_1_69_RANGE == lvRange
        isSelfSchool = p.school == school
        if isRankAll:
            self.rankData[RANK_TOTAL] = infoList
            self.rankVerData[RANK_TOTAL] = ver
        else:
            self.rankData[isSelfSchool, isLowLvRange] = infoList
            self.rankVerData[isSelfSchool, isLowLvRange] = ver
        for gbId, name, school, val, timeStamp in dataList:
            roleName, guildName = utils.getNameAndGuildNameFromStr(name)
            infoList.append((gbId,
             roleName,
             guildName,
             val,
             timeStamp))

        infoList.sort(cmp=self.sortCmp)
        isInRank = False
        for index, info in enumerate(infoList):
            if info[0] == p.gbId:
                isInRank = True
                if isRankAll:
                    self.selfRankInfo[RANK_TOTAL] = (info[3], index + 1)
                else:
                    self.selfRankInfo[isSelfSchool, isLowLvRange] = (info[3], index + 1)
                break

        if not isInRank:
            if isRankAll:
                self.selfRankInfo[RANK_TOTAL] = (myScore, RANK_MAX_LEN + 1)
            else:
                self.selfRankInfo[isSelfSchool, isLowLvRange] = (myScore, RANK_MAX_LEN + 1)
        self.refreshRankScrollWndListView()

    def sortCmp(self, infoA, infoB):
        if infoA[3] != infoB[3]:
            return cmp(infoB[3], infoA[3])
        return cmp(infoA[4], infoB[4])

    def guildSortCmp(self, infoA, infoB):
        if infoA[2] != infoB[2]:
            return cmp(infoB[2], infoA[2])
        return cmp(infoA[3], infoB[3])

    def processGuildData(self, data):
        p = BigWorld.player()
        infoList = []
        version, dataList, guildScore, key = data
        for guildNuid, name, school, val, timeStamp in dataList:
            infoList.append((guildNuid,
             name,
             val,
             timeStamp))

        infoList.sort(cmp=self.guildSortCmp)
        isInRank = False
        for index, info in enumerate(infoList):
            if info[0] == p.guildNUID:
                isInRank = True
                self.selfRankInfo[RANK_GUILD] = (info[2], index + 1)
                break

        if not isInRank:
            self.selfRankInfo[RANK_GUILD] = (guildScore, RANK_MAX_LEN + 1)
        self.rankData[RANK_GUILD] = infoList
        self.rankVerData[RANK_GUILD] = version
        self.refreshRankScrollWndListView()

    def refreshSelfRankInfo(self):
        gamelog.info('jbx:refreshSelfRankInfo')
        if not self.widget:
            return
        selfRankInfo = self.getRankInfo()
        if not selfRankInfo[1] or selfRankInfo[1] > RANK_MAX_LEN:
            rankDesc = gameStrings.BAIDI_SHILIAN_SELF_NOT_IN_RANK
        else:
            rankDesc = str(selfRankInfo[1])
        myscore = selfRankInfo[0]
        if self.selectedRank == RANK_TOTAL:
            self.widget.descScore.text = gameStrings.BAIDI_SHILIAN_RANK_TOTAL_DESC_SCORE
            self.widget.descRank.text = gameStrings.BAIDI_SHILIAN_RANK_TOTAL_DESC_RANK
            self.widget.txtRankValue.text = gameStrings.BAIDI_SHILIAN_RANK_TOTAL_TXT % rankDesc
            myscore = self.selfScore if self.selfScore else myscore
        elif self.selectedRank == RANK_SCHOOL:
            self.widget.descScore.text = gameStrings.BAIDI_SHILIAN_RANK_TOTAL_DESC_SCORE
            self.widget.descRank.text = gameStrings.BAIDI_SHILIAN_RANK_TOTAL_DESC_RANK
            self.widget.txtRankValue.text = gameStrings.BAIDI_SHILIAN_RANK_SCHOOL_TXT % rankDesc
            myscore = self.selfScore if self.selfScore else myscore
        else:
            self.widget.descScore.text = gameStrings.BAIDI_SHILIAN_RANK_GUILD_DESC_SCORE
            self.widget.descRank.text = gameStrings.BAIDI_SHILIAN_RANK_GUILD_DESC_RANK
            self.widget.txtRankValue.text = '%s' % rankDesc
        self.widget.txtPoint.text = str(myscore)

    def addLogList(self, logType, *logData):
        gamelog.info('jbx:addLogList', logType, logData)
        while len(self.logList) > LOG_LIST_MAX_LEN:
            self.logList.pop(0)

        time = utils.getNow()
        gbId = logData[0]
        logData = (logType, time, logData)
        self.logList.append(logData)
        gbId == BigWorld.player().gbId and self.selfLogList.append(logData)
        self.refreshLogList()

    @ui.callInCD(1)
    def refreshLogList(self):
        if not self.widget:
            return
        if self.isOnlyShowSelfLog:
            dataArray = self.selfLogList
        else:
            dataArray = self.logList
        textOffset = 2
        startPos = 0
        self.widget.removeAllInst(self.widget.logList.canvas, True)
        for itemData in dataArray:
            itemMc = self.widget.getInstByClsName('BaiDiShiLian_LogItemRender')
            self.widget.logList.canvas.addChild(itemMc)
            self.logItemlabelFunction(itemData, itemMc)
            itemMc.y = startPos
            startPos += itemMc.txtDesc.textHeight + textOffset

        self.widget.logList.refreshHeight(startPos + 10)
        self.widget.logList.scrollToEnd()

    def logItemlabelFunction(self, itemData, itemMc):
        logType, time, logData = int(itemData[0]), int(itemData[1]), itemData[2]
        timeDesc = utils.formatTimeStr(time, 'm:s', False, 2, 2)
        isSelf = False
        desc = ''
        logListDesc = SWCCD.data.get('logListDesc', {})
        if logType == uiConst.LOG_TYPE_CHALLENGE:
            memberGbId = int(logData[0])
            memberName = logData[1]
            score = int(logData[2])
            isSelf = memberGbId == BigWorld.player().gbId
            if isSelf:
                desc = logListDesc.get('selfChallenge', '%d') % score
            else:
                desc = logListDesc.get('challenge', '%s%d') % (memberName, score)
        elif logType == uiConst.LOG_TYPE_RANSACK:
            memberGbId = int(logData[0])
            memberName = logData[1]
            tName = logData[4]
            robscore = int(logData[7])
            isSelf = memberGbId == BigWorld.player().gbId
            if isSelf:
                desc = logListDesc.get('selfRansack', '%s%d') % (tName, robscore)
            else:
                desc = logListDesc.get('ransack', '%s%s%d') % (memberName, tName, robscore)
        else:
            memberGbId = int(logData[0])
            memberName = logData[1]
            sName = logData[4]
            robscore = int(logData[7])
            isSelf = memberGbId == BigWorld.player().gbId
            if isSelf:
                desc = logListDesc.get('selfBeRansack', '%s%d') % (sName, robscore)
            else:
                desc = logListDesc.get('beRansack', '%s%s%d') % (memberName, sName, robscore)
        itemMc.txtTime.text = timeDesc
        itemMc.txtDesc.text = desc

    def handleRankTotalBtnClick(self, *args):
        gamelog.info('jbx:handleRankToTotalBtnClick')
        self.refreshRank(rankType=RANK_TOTAL)

    def handleRankSchoolBtnClick(self, *args):
        gamelog.info('jbx:handleRankSchoolBtnClick')
        self.refreshRank(RANK_SCHOOL)

    def handleRankGuildBtnClick(self, *args):
        gamelog.info('jbx:handleRankGuildBtnClick')
        self.refreshRank(RANK_GUILD)

    def handleLowLvBtnClick(self, *args):
        gamelog.info('jbx:handleLowBtnClick')
        self.refreshRank(isLowLv=True)

    def handleHighLvBtnClick(self, *args):
        gamelog.info('jbx:handleHighLvBtnClick')
        self.refreshRank(isLowLv=False)

    def handleRefreshBtnClick(self, *args):
        gamelog.info('jbx:handleRefreshBtnClick')
        if utils.getNow() - self.lastRefreshTime < REFRESH_BTN_CD:
            return
        self.lastRefreshTime = utils.getNow()
        self.refreshRank(refreshForece=True)

    def handleOnlySelfChkClick(self, *args):
        gamelog.info('jbx:handleOnlySelfChkClick')
        self.isOnlyShowSelfLog = not self.isOnlyShowSelfLog
        self.refreshLogList()

    def handleChannlengeBtnClick(self, *args):
        gamelog.info('jbx:handleChannlengeBtnClick')
        if utils.getNow() - self.lastChallengeTime < CHALLENGE_BTN_CD:
            return
        p = BigWorld.player()
        p.cell.applySkyWingChallenge()
        if formula.inSkyWingFubenSpace(p.spaceNo):
            self.hide()

    def handleRansackBtnClick(self, *args):
        gamelog.info('jbx:handleRansackBtnClick')
        if utils.getNow() - self.lastRansackTime < RANSACK_BTN_CD:
            return
        gameglobal.rds.ui.ransack.show()
