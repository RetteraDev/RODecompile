#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServiceFubenRaceProxy.o
import BigWorld
import utils
import uiUtils
import const
import events
import gametypes
import clientUtils
import commNewServerActivity
from uiProxy import UIProxy
from asObject import ASObject
from gamestrings import gameStrings
from callbackHelper import Functor
from data import new_server_activity_data as NSAD
from data import mail_template_data as MTD
MAX_FUBEN_TAB_NUM = 2
RANK_ITEM_TEXT_NUM = 4

class NewServiceFubenRaceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServiceFubenRaceProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rankData = {}
        self.reset()

    def clearAll(self):
        self.rankData = {}

    def reset(self):
        self.selFbTab = None
        self.selRankItem = None
        self.needSelectSelfItem = False
        self.isRaceEnd = {}

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        self.initContentList()
        self.initFubenTabBtns()
        self.widget.mainMc.contentMc.myRankBtn.addEventListener(events.MOUSE_CLICK, self.handleMRankClick, False, 0, True)

    def canOpenTab(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_FUBEN_RACE):
            return False
        for fbId in NSAD.data.get('jingSuFubens', {}).keys():
            if self._checkRaceInDisplayTime(fbId):
                return True

        return False

    def handleMRankClick(self, *args):
        curTarget = ASObject(args[3][0]).currentTarget
        contentList = curTarget.parent.list
        myRank = self.rankData.get(self.selFbTab.fbId, {}).get('myRank', 0)
        if not myRank:
            return
        offsetY = contentList.itemHeight * (myRank - 1)
        contentList.scrollTo(offsetY)
        itemMc = contentList.canvas.getChildByName('item_%d' % (myRank - 1))
        if itemMc:
            self.selectRankItemByMc(itemMc)
        else:
            self.needSelectSelfItem = True

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshContentList()

    def initFubenTabBtns(self):
        mainMc = self.widget.mainMc
        fbIds = NSAD.data.get('jingSuFubens', {}).keys()
        for i in xrange(MAX_FUBEN_TAB_NUM):
            rewardBtn = getattr(mainMc, 'rBtn_%d' % i)
            rewardBtn.visible = False
            rewardBtn.fbId = fbIds[i]
            rewardBtn.addEventListener(events.MOUSE_CLICK, self.handleRewardBtnClick, False, 0, True)
            fbBtn = getattr(mainMc, 'fBtn_%d' % i)
            fbBtn.reward = rewardBtn
            if i < len(fbIds) and self._checkRaceInDisplayTime(fbIds[i]):
                fbBtn.timeTxt.visible = True
                fbBtn.enabled = True
                fbBtn.fbId = fbIds[i]
                timeStr = self.getFubenRaceRestTimeStr(fbIds[i])
                fbBtn.timeTxt.text = gameStrings.NEW_SERVICE_FUBEN_RACE_REST_TIME % timeStr if timeStr else gameStrings.NEW_SERVICE_FUBEN_RACE_END
                fbBtn.addEventListener(events.MOUSE_CLICK, self.handleFubenTabBtnClick, False, 0, True)
                not self.selFbTab and self.selectFubenTabByMc(fbBtn)
            else:
                fbBtn.timeTxt.visible = False
                fbBtn.enabled = False
                fbBtn.validateNow()
                if self._checkRaceActivityOpenButEnd(fbIds[i]) and getattr(fbBtn, 'lockMc'):
                    fbBtn.lockMc.disabledDesc.text = gameStrings.NEW_SERVICE_FUBEN_RACE_ACTIVITY_END

    def handleRewardBtnClick(self, *args):
        curTarget = ASObject(args[3][0]).currentTarget
        fbId = curTarget.fbId
        if not fbId:
            return
        self.uiAdapter.ranking.openRewardPanel(0, 0, useNewAwardPanel=True, awardInfoFunc=Functor(self.rankAwardInfoFunc, fbId))

    def _checkRaceInDisplayTime(self, fbId):
        return commNewServerActivity.checkNSJingSuInDisPlayTime(fbId)

    def getFubenRaceRestTimeStr(self, fbId):
        msId, activityOpenDay, _ = NSAD.data['jingSuFubens'][fbId]
        if msId:
            startTime = BigWorld.player().getServerProgressFinishTime(msId)
        else:
            startTime = utils.getServerOpenTime()
        restTime = utils.getDaySecond(startTime) + activityOpenDay * const.TIME_INTERVAL_DAY - utils.getNow()
        if restTime > 0:
            d = restTime / const.TIME_INTERVAL_DAY
            h = restTime % const.TIME_INTERVAL_DAY / const.TIME_INTERVAL_HOUR
            self.isRaceEnd[fbId] = gametypes.GROUP_FB_QUERY_TYPE_DATA_DEFAULT
            return str(d) + gameStrings.COMMON_DAY + str(h) + gameStrings.COMMON_HOUR
        else:
            self.isRaceEnd[fbId] = gametypes.GROUP_FB_QUERY_TYPE_DATA_BAK
            return ''

    def initContentList(self):
        rankList = self.widget.mainMc.contentMc.list
        rankList.itemRenderer = 'NewServiceFubenRace_CommonRankItem'
        rankList.itemHeight = 35
        rankList.labelFunction = self.rankItemLabelFunc

    def refreshContentList(self):
        if not self.selFbTab:
            return
        fbId = self.selFbTab.fbId
        contentMc = self.widget.mainMc.contentMc
        rData = self.rankData.get(fbId, {})
        myRank = rData.get('myRank', 0)
        contentMc.myRankBtn.enabled = bool(myRank)
        contentMc.myRank.text = myRank if myRank else gameStrings.NEW_SERVER_NOT_IN_RANK_1
        dataLength = len(rData.get('data', []))
        contentMc.list.dataArray = [ idx for idx in xrange(dataLength) ]
        contentMc.list.validateNow()

    def rankItemLabelFunc(self, *args):
        index = int(args[3][0].GetNumber())
        itemMc = ASObject(args[3][1])
        fbId = self.selFbTab.fbId
        itemData = self.rankData[fbId]['data'][index]
        itemMc.nuid = itemData.get('nuid', 0)
        itemMc.tName = itemData.get('teamName', 0)
        itemMc.name = 'item_%d' % index
        topIconVisible = index < 3
        itemMc.rank.visible = not topIconVisible
        itemMc.top3Icon.visible = topIconVisible
        if topIconVisible:
            itemMc.top3Icon.gotoAndPlay('rank_%d' % (index + 1))
            self.ricon = itemMc.top3Icon
        else:
            itemMc.rank.text = str(index + 1)
        dataKeys = ('teamName', 'guildName', 'costTime', 'score')
        for i in xrange(RANK_ITEM_TEXT_NUM):
            textFiled = getattr(itemMc, 'text%d' % i)
            if i < len(dataKeys):
                textFiled.text = itemData.get(dataKeys[i], '')
            else:
                textFiled.text = ''

        if self.needSelectSelfItem and index + 1 == self.rankData[fbId]['myRank']:
            self.needSelectSelfItem = False
            self.selectRankItemByMc(itemMc)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleRankItemRollOver, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleRankItemRollOut, False, 0, True)
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleRankItemClick, False, 0, True)

    def handleRankItemRollOver(self, *args):
        curTarget = ASObject(args[3][0]).currentTarget
        if curTarget.selected:
            return
        curTarget.gotoAndPlay('over')

    def handleRankItemRollOut(self, *args):
        curTarget = ASObject(args[3][0]).currentTarget
        if curTarget.selected:
            return
        curTarget.gotoAndPlay('up')

    def handleRankItemClick(self, *args):
        curTarget = ASObject(args[3][0]).currentTarget
        self.selectRankItemByMc(curTarget)

    def handleFubenTabBtnClick(self, *args):
        curTarget = ASObject(args[3][0]).currentTarget
        self.selectFubenTabByMc(curTarget)

    def selectFubenTabByMc(self, mc):
        if self.selFbTab:
            self.selFbTab.selected = False
            self.selFbTab.reward.visible = False
        mc.selected = True
        mc.reward.visible = True
        self.selFbTab = mc
        self.refreshInfo()
        fbId = mc.fbId
        self.queryRaceRankData(fbId)

    def selectRankItemByMc(self, mc):
        if not mc.enabled:
            return
        if self.selRankItem and self.selRankItem.selected:
            self.selRankItem.gotoAndPlay('up')
            self.selRankItem.selected = False
        self.selRankItem = mc
        mc.selected = True
        mc.gotoAndPlay('down')
        fbId = self.selFbTab.fbId
        if fbId in self.isRaceEnd:
            self.uiAdapter.ranking.saveTeamUuid(mc.nuid, long(mc.nuid))
            self.uiAdapter.ranking.openTeamDetail(fbId, mc.nuid, mc.tName, self.isRaceEnd[fbId])

    def updateTeamData(self, version, data, fbNo, isBak = False):
        if fbNo not in NSAD.data.get('jingSuFubens', {}):
            return
        data, mRank = self.getRankListData(data, isBak)
        self.rankData[fbNo] = {'version': version,
         'data': data,
         'myRank': mRank}
        self.selFbTab and self.selFbTab.fbId == fbNo and self.refreshInfo()

    def getRankListData(self, data, isBak):
        listData = []
        myRank = 0
        if isBak:
            data.sort(key=lambda ret: ret['rank'])
        else:
            data.sort(key=lambda ret: (ret['finishTime'], -ret['score'], ret['fTimestamp']))
        for idx, val in enumerate(data):
            finishTime = val.get('finishTime', 0)
            combinedName = val.get('combinedName', '-').split('-')
            guildName = combinedName[1] if len(combinedName) > 1 else ''
            captainName = combinedName[2] if len(combinedName) > 2 else ''
            realTeamName = gameStrings.TEAM_DEFAULT_TEAM_NAME % captainName if captainName else ''
            hasMe = val.get('hasMe', False)
            itemData = {'nuid': val.get('nuid', 0),
             'teamName': realTeamName,
             'guildName': guildName,
             'score': val.get('score', 0),
             'costTime': utils.formatTimeStr(finishTime, 'h:m:s', True, 2, 2, 2),
             'hasMe': hasMe}
            if hasMe and not myRank:
                myRank = idx + 1
            listData.append(itemData)

        return (listData, myRank)

    def rankAwardInfoFunc(self, fbId):
        fbInfo = NSAD.data.get('jingSuFubens', {}).get(fbId, [])
        awardList = []
        if fbInfo and len(fbInfo) > 2 and isinstance(fbInfo[2], tuple):
            oldMailId = None
            oldIdx = None
            mailTampIds = list(fbInfo[2])
            mailTampIds.append(-1)
            for idx, mailId in enumerate(mailTampIds):
                if oldMailId is None:
                    oldIdx, oldMailId = idx, mailId
                    continue
                elif oldMailId != mailId:
                    up = idx
                    down = oldIdx + 1
                    rankDesc = '%d~%d' % (down, up) if up != down else str(up)
                    desc = gameStrings.NEW_SERVICE_FUBEN_RACE_AWARD_RANK % rankDesc
                    bonusId = MTD.data.get(oldMailId, {}).get('bonusId', 0)
                    items = clientUtils.genItemBonus(bonusId)
                    if not items:
                        items = ()
                    itemList = []
                    for item in items:
                        iconPath = uiUtils.getItemIconFile64(item[0])
                        color = uiUtils.getItemColor(item[0])
                        itemList.append([iconPath,
                         item[1],
                         color,
                         item[0]])

                    awardList.append([desc, '', itemList])
                    oldIdx, oldMailId = idx, mailId

        ret = [0,
         False,
         [],
         '',
         awardList,
         0,
         gametypes.TOP_TYPE_NEW_SERVICE_FUBEN_RACE,
         gameStrings.NEW_SERVICE_FUBEN_RACE_AWARD_DESC]
        return ret

    def queryRaceRankData(self, fbId):
        if fbId in self.isRaceEnd:
            version = self.rankData.get(fbId, {}).get('version', 0)
            if self.isRaceEnd[fbId] == gametypes.GROUP_FB_QUERY_TYPE_DATA_BAK and version == -1:
                return
            BigWorld.player().base.queryNSJingSuData(fbId, version, self.isRaceEnd[fbId])

    def _checkRaceActivityOpenButEnd(self, fbId):
        fbData = NSAD.data.get('jingSuFubens', {}).get(fbId, ())
        if not fbData:
            return False
        msId, activityOpenDay, _ = fbData
        if msId:
            if not BigWorld.player().isServerProgressFinished(msId):
                return False
            tMsFinish = BigWorld.player().getServerProgressFinishTime(msId)
            openDay = utils.getDaysByTime(tMsFinish)
        else:
            openDay = utils.getServerOpenDays()
        displayDay = NSAD.data.get('jingSuRewardOpenDay', 0)
        if openDay + 1 > activityOpenDay + displayDay:
            return True
        return False
