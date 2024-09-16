#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/roleInformationQumoProxy.o
import BigWorld
import gameglobal
import gametypes
import uiConst
import uiUtils
import const
import utils
import clientUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import MenuManager
from guis import events
from uiProxy import UIProxy
from guis import activityFactory
from gameStrings import gameStrings
from data import qumo_lv_data as QLD
from data import seeker_data as SEEKD
from data import npc_data as ND
from data import sys_config_data as SCD
from data import bonus_data as BD
from data import item_data as ID
from data import activity_state_config_data as ASCD
from data import stats_target_data as STD
from data import activity_basic_data as ABD
MAX_REWARD_NUM = 5
INIT_ACT_X = 0
INIT_ACT_Y = 0
ACT_Y_OFFSET = 28
ACTIVITY_ITEM = 'RoleInformationQumo_Act_Item'

class RoleInformationQumoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RoleInformationQumoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.nextQumoReward = {}
        self.weeklyQumoScore = 0
        self.weeklyMaxQumoScore = 0
        self.gongxianPoint = []
        self.qumoData = {}
        self.nextQumoData = {}
        self.nextRewardTip = None
        self.actFactory = activityFactory.getInstance()
        self.sortedAct = sorted(ABD.data.iteritems(), key=lambda d: d[1]['sortedId'])

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.nextRewardTip = None

    def initUI(self):
        self.widget.questPanel.visible = False
        p = BigWorld.player()
        qumoLv = p.qumoLv
        self.qumoData = QLD.data.get(qumoLv, {})
        title = self.qumoData.get('name', gameStrings.NO_QU_MO_TITLE)
        self.widget.panel.title.text = title
        self.setQumoScore()
        exchangeNpcID = self.qumoData.get('exchangeNpc', 10040)
        npcId = SEEKD.data.get(exchangeNpcID, {}).get('npcId', 0)
        if npcId == 0:
            exchangeNpcName = SEEKD.data.get(exchangeNpcID, {}).get('name', gameStrings.OTHER)
        else:
            exchangeNpcName = ND.data.get(npcId, {}).get('name', gameStrings.OTHER)
            budNpcLink = 'seek:%d' % exchangeNpcID
        self.widget.panel.nulinScoreNpc.htmlText = gameStrings.NUL_IN_SCORE_NPC % (budNpcLink, exchangeNpcName)
        self.widget.panel.nulinScoreNpc.width = self.widget.panel.nulinScoreNpc.textWidth + 5
        self.widget.panel.findNpc.addEventListener(events.MOUSE_CLICK, self.handleFindNpc)
        self.widget.panel.findNpc.data = exchangeNpcID
        self.widget.panel.findNpc.x = self.widget.panel.nulinScoreNpc.x + self.widget.panel.nulinScoreNpc.textWidth + 5
        nextQumoLv = p.qumoLv + 1
        self.nextQumoData = QLD.data.get(nextQumoLv, {})
        self.initNextQumoInfo()
        self.initNextQumoReward()
        self.initWeekReward()
        self.widget.panel.nextRewardTip.visible = False
        self.nextRewardTip = self.widget.panel.nextRewardTip
        self.widget.panel.nextQumoReward.addEventListener(events.MOUSE_CLICK, self.handleClickNextReward)
        self.widget.panel.weekQumoActivity.addEventListener(events.MOUSE_CLICK, self.handleClickWeekQumoActivity)

    def setQumoScore(self):
        p = BigWorld.player()
        self.widget.panel.qumoExpWeek.text = gameStrings.WEEK_SCORE_QU_MO % self.weeklyQumoScore
        self.widget.panel.qumoExpWeekLimit.text = gameStrings.WEEK_LIMIT_SCORE_QU_MO % self.weeklyMaxQumoScore
        qumoFameId = SCD.data.get('fameNulinID', 0)
        self.widget.panel.qumoExp.text = p.fame.get(qumoFameId)
        self.widget.panel.doubleQumo.text = gameStrings.DOUBLE_SCORE_QU_MO % getattr(p, 'doubleQumo', 0)

    def initWeekReward(self):
        if not self.widget:
            return
        p = BigWorld.player()
        gongxianData = SCD.data.get('pointsToFame', [])
        gotGongxian = p.weeklyQumoCollectPoints if p.weeklyQumoCollectPoints else []
        bonus = self.qumoData.get('bonusSet', {500: 0,
         850: 0,
         1000: 0})
        bonus = sorted(bonus.iteritems(), key=lambda e: e[0])
        self.widget.panel.getBtn.addEventListener(events.MOUSE_CLICK, self.handleClickGetBtn)
        getEnabled = False
        self.gongxianPoint = [180, 300, 560]
        if len(gongxianData) > 0:
            self.gongxianPoint[0] = gongxianData[0][0]
            self.gongxianPoint[1] = gongxianData[1][0]
            self.gongxianPoint[2] = gongxianData[2][0]
        if len(self.gongxianPoint) == len(bonus):
            for i in xrange(len(self.gongxianPoint)):
                itemBonus = clientUtils.genItemBonus(bonus[i][1])
                if len(itemBonus) <= 0:
                    continue
                itemInfo = uiUtils.getGfxItemById(itemBonus[0][0], itemBonus[0][1])
                itemInfo['state'] = uiConst.ITEM_GRAY
                state = gameStrings.WEEK_QUMO_WEEK_REWARD_TXT % self.gongxianPoint[i]
                arrowState = 'dislight'
                if p.weeklyQumoPoints >= self.gongxianPoint[i]:
                    itemInfo['state'] = uiConst.ITEM_NORMAL
                    if i != 0:
                        arrowState = 'light'
                    if len(gotGongxian) <= i:
                        getEnabled = True
                    else:
                        state = gameStrings.WEEK_REWARD_GETTED
                elif i > 0 and p.weeklyQumoPoints > self.gongxianPoint[i - 1]:
                    arrowState = 'half'
                if i != 0:
                    self.widget.panel.getChildByName('arrow%d' % i).gotoAndStop(arrowState)
                reward = self.widget.panel.getChildByName('reward%d' % i)
                reward.slot.setItemSlotData(itemInfo)
                reward.state.text = state

        self.widget.panel.getBtn.enabled = getEnabled
        self.setExtraReward()
        basicFameVal = self.qumoData.get('basicFameVal', 0)
        percentArr = [0.5, 0.5, 0.2]
        if len(gongxianData) > 0:
            percentArr[0] = gongxianData[0][1]
            percentArr[1] = gongxianData[1][1]
            percentArr[2] = gongxianData[2][1]
        famePercent = self.qumoData.get('famePercent', percentArr)
        maxYunchui = basicFameVal * famePercent[0] + basicFameVal * famePercent[1] + basicFameVal * famePercent[2]
        self.widget.panel.maxYunchui.text = maxYunchui
        self.widget.panel.weekQumoPoint.text = gameStrings.WEEK_QUMO_POINT % p.weeklyQumoPoints
        TipManager.addTip(self.widget.panel.maxYunchui, gameStrings.WEEK_YUN_CHUI_SCORE_TIP)

    def initNextQumoInfo(self):
        p = BigWorld.player()
        canLvUp = True
        reqLv = self.nextQumoData.get('reqLv', 0)
        if p.lv >= reqLv:
            self.widget.panel.levelRequire.gotoAndStop('lvgou')
        else:
            canLvUp = False
            self.widget.panel.levelRequire.gotoAndStop('wenzi')
            self.widget.panel.levelRequire.txt.text = '(%d/%d)' % (p.lv, reqLv)
        if p.statsInfo.has_key(const.QUMO_STATS_VAR_FBSSS):
            curFb = p.statsInfo[const.QUMO_STATS_VAR_FBSSS]
        else:
            curFb = 0
        reqFb = self.nextQumoData.get('reqFb', 0)
        flag = QLD.data.get(p.qumoLv, {}).get('MaxQuMoLv', False)
        if not flag:
            if curFb >= reqFb:
                self.widget.panel.fubenRequire.gotoAndStop('lvgou')
            else:
                canLvUp = False
                self.widget.panel.fubenRequire.gotoAndStop('wenzi')
                self.widget.panel.fubenRequire.txt.text = '(%d/%d)' % (curFb, reqFb)
            self.widget.panel.levelRequireLabel.text = gameStrings.NEXT_QU_MO_LV % reqLv
            self.widget.panel.fubenRequireLabel.text = gameStrings.NEXT_QU_MO_FUBEN_TIMES % reqFb
        else:
            self.widget.panel.levelRequireLabel.text = SCD.data.get('nextQuMoLvMax', '')
            self.widget.panel.fubenRequireLabel.text = ''
            self.widget.panel.fubenRequire.visible = False
            self.widget.panel.levelRequire.visible = False
            self.widget.panel.quxiaodian.visible = False
            self.widget.panel.lvupBtn.visible = False
        nextQumoName = self.nextQumoData.get('name', gameStrings.NO_QU_MO_TITLE)
        self.qumoName = nextQumoName
        self.qumoNameV = gameStrings.NEXT_QUMO_LV_NAME
        self.widget.panel.nextQumoTitle.text = nextQumoName
        lvupNpcID = self.qumoData.get('lvupNpc', 10040)
        self.widget.panel.lvupBtn.data = lvupNpcID
        self.widget.panel.lvupBtn.addEventListener(events.MOUSE_CLICK, self.handleFindNpc)
        if not canLvUp:
            self.widget.panel.lvupBtn.enabled = False
        else:
            self.widget.panel.lvupBtn.enabled = True

    def setExtraReward(self):
        bonusBtnEnabled = False
        qumoActId = self.getQumoActivityId()
        p = BigWorld.player()
        if qumoActId:
            activityTips = SCD.data.get('QUMO_ACTIVITY_TIPS', gameStrings.QU_MO_EXTRA_REWARD)
            qmDataList = ASCD.data.get(qumoActId, {}).get('pointsToFame', {})
            bonusAwardIdList = []
            coverBonus = []
            for qmData in qmDataList:
                qmBonusItem = {}
                qmBonusItem['actBonusGongxianNeed'] = qmData[0]
                if qmBonusItem['actBonusGongxianNeed'] <= p.weeklyQumoPoints:
                    coverBonus.append(qmBonusItem['actBonusGongxianNeed'])
                qmBonusItem['actBonusPercent'] = qmData[1]
                bonusAwardIdList.append(qmBonusItem)

            if len(coverBonus):
                bonusBtnEnabled = False
                weeklyQumoCollectPointsForActivity = p.weeklyQumoCollectPointsForActivity
                for canGetPoint in coverBonus:
                    canGet = True
                    for wcItem in weeklyQumoCollectPointsForActivity:
                        getedPoint = wcItem[0]
                        if getedPoint == canGetPoint:
                            canGet = False

                    if canGet:
                        bonusBtnEnabled = True
                        break

            else:
                bonusBtnEnabled = False
        else:
            activityTips = SCD.data.get('QUMO_ACTIVITY_NO_TIPS', gameStrings.QU_MO_WITHOUT_EXTRA_REWARD)
        self.widget.panel.bonusBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBonusBtn)
        self.widget.panel.bonusBtn.enabled = bonusBtnEnabled
        TipManager.addTip(self.widget.panel.bonusBtn, activityTips)

    def updateQumoFame(self, value, nWeek, mWeek, extraLimit):
        self.weeklyQumoScore = nWeek
        self.weeklyMaxQumoScore = mWeek
        self.qumoScoreExtraLimit = extraLimit

    def getQumoActivityId(self):
        p = BigWorld.player()
        if not hasattr(p, 'qumoActivityId'):
            return 0
        else:
            return p.qumoActivityId

    def getQumoActList(self, levelReq):
        p = BigWorld.player()
        ret = []
        for key, _ in self.sortedAct:
            actIns = self.actFactory.actIns.get(key, None)
            if actIns.getShowInQumo() == 0:
                continue
            if not hasattr(actIns, 'erefId'):
                continue
            if levelReq and (p.realLv < actIns.getMinLv() or p.realLv > actIns.getMaxLv()):
                continue
            nowErefId = actIns.erefId[0]
            item = STD.data.get(nowErefId, {})
            actItem = {}
            actItem['actId'] = actIns.id
            actItem['actName'] = actIns.getDesc()
            actItem['sortedId'] = actIns.getSortedId()
            actItem['value'] = item.get('rewardQumo', 0)
            actItem['playRecommPage'] = item.get('playRecommPage', 0)
            actItem['playRecommItemId'] = item.get('playRecommItemId', 0)
            actItem['playRecommLocateType'] = item.get('playRecommLocateType', 0)
            actItem['process'] = [actIns.getStatsInfoValue(item.get('property', '')), item.get('finishNum', 0)]
            ret.append(actItem)

        ret.sort(key=lambda x: x['sortedId'])
        return ret

    def refreshActivityPanel(self):
        self.widget.questPanel.actCloseBtn.addEventListener(events.MOUSE_CLICK, self.handleClickActClose)
        lvReq = self.widget.questPanel.lvAvaliable.selected
        actList = self.getQumoActList(lvReq)
        questPanel = self.widget.questPanel
        posY = INIT_ACT_Y
        length = len(actList)
        for i in xrange(0, length):
            item = questPanel.itemArea.getChildByName('item%d' % i)
            if not item:
                item = self.widget.getInstByClsName(ACTIVITY_ITEM)
                questPanel.itemArea.addChild(item)
                item.y = posY
                item.x = INIT_ACT_X
            item.check.data = {'playRecommPage': actList[i].get('playRecommPage', ''),
             'playRecommItemId': actList[i].get('playRecommItemId', ''),
             'playRecommLocateType': actList[i].get('playRecommLocateType', '')}
            item.check.addEventListener(events.MOUSE_CLICK, self.handleClickCheck)
            item.actName.text = actList[i].get('actName', '')
            item.score.text = actList[i].get('value', '')
            if actList[i].get('process', (0, 0))[0] >= actList[i].get('process', (0, 0))[1]:
                item.progress.gotoAndStop('lvgou')
            else:
                item.progress.gotoAndStop('wenzi')
                item.progress.txt.text = '%d/%d' % (actList[i].get('process', (0, 0))[0], actList[i].get('process', (0, 0))[1])
            posY += ACT_Y_OFFSET

        while length < questPanel.itemArea.numChildren:
            questPanel.itemArea.removeChildAt(length)

    def initNextQumoReward(self):
        p = BigWorld.player()
        percentArr = [0.5, 0.5, 0.2]
        nextQumoLv = p.qumoLv + 1
        basicFameVal = self.nextQumoData.get('basicFameVal', 1200)
        nowBasicFameVal = self.qumoData.get('basicFameVal', 1200)
        famePercent = self.nextQumoData.get('famePercent', percentArr)
        nowFamePercent = self.qumoData.get('famePercent', percentArr)
        self.nextQumoReward['nextMaxFame'] = basicFameVal * (famePercent[0] + famePercent[1] + famePercent[2])
        self.nextQumoReward['nowMaxFame'] = nowBasicFameVal * (nowFamePercent[0] + nowFamePercent[1] + nowFamePercent[2])
        nextRewardItems = self.nextQumoData.get('rewardItems', [])
        self.nextQumoReward['nextRewardItems'] = self.getItemsInfo(nextRewardItems)
        nextJunziItems = self.nextQumoData.get('junziItems', [])
        self.nextQumoReward['nextJunziItems'] = self.getItemsInfo(nextJunziItems)

    def initNextRewardTip(self):
        for i in xrange(0, MAX_REWARD_NUM):
            rewardItem = self.widget.panel.nextRewardTip.getChildByName('rewardItem%d' % i)
            if i >= len(self.nextQumoReward['nextRewardItems']):
                rewardItem.visible = False
                continue
            rewardItem.setItemSlotData(self.nextQumoReward['nextRewardItems'][i])

        for i in xrange(0, MAX_REWARD_NUM):
            junziItem = self.widget.panel.nextRewardTip.getChildByName('junziItem%d' % i)
            if i >= len(self.nextQumoReward['nextJunziItems']):
                junziItem.visible = False
                continue
            junziItem.setItemSlotData(self.nextQumoReward['nextJunziItems'][i])

        self.widget.panel.nextRewardTip.cashNow.text = self.nextQumoReward['nowMaxFame']
        self.widget.panel.nextRewardTip.cashNext.text = self.nextQumoReward['nextMaxFame']

    def getItemsInfo(self, itemArr):
        info = []
        for item in itemArr:
            if item != None:
                itemId = item[0]
                itemCount = item[1]
                itemInfo = uiUtils.getGfxItemById(itemId, itemCount)
                info.append(itemInfo)

        return info

    def handleFindNpc(self, *args):
        target = ASObject(args[3][0]).currentTarget
        seekId = int(target.data)
        uiUtils.gotoTrack(seekId)
        gameglobal.rds.uiLog.addFlyLog(seekId)

    def handleClickNextReward(self, *args):
        target = ASObject(args[3][0]).currentTarget
        MenuManager.getInstance().showMenu(target, self.nextRewardTip, None, False)
        self.initNextRewardTip()

    def handleClickWeekQumoActivity(self, *args):
        self.widget.questPanel.visible = not self.widget.questPanel.visible
        self.refreshActivityPanel()

    def handleClickGetBtn(self, *args):
        p = BigWorld.player()
        p.cell.getQumoFameFromWeeklyPoints()

    def handleClickBonusBtn(self, *args):
        BigWorld.player().cell.getQumoFameFromWeeklyPointsFromActivity()

    def handleClickActClose(self, *args):
        self.widget.questPanel.visible = False

    def handleClickCheck(self, *args):
        target = ASObject(args[3][0]).currentTarget
        gameglobal.rds.ui.playRecomm.showInPage(page=target.data.playRecommPage, selectedId=target.data.playRecommItemId, locateType=target.data.playRecommLocateType)
