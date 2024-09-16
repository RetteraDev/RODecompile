#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/guildShootUpRankProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import gametypes
import time
import clientUtils
from uiProxy import UIProxy
from data import guild_config_data as GCD
from data import novice_boost_score_type_data as NBSTD

class GuildShootUpRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildShootUpRankProxy, self).__init__(uiAdapter)
        self.modelMap = {'getProgressInfo': self.onGetProgressInfo,
         'getFinishInfo': self.onGetFinishInfo,
         'query': self.onQuery,
         'award': self.onAward}
        self.mediator = None
        self.currentTabIndex = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_SHOOT_UP_RANK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_SHOOT_UP_RANK:
            self.mediator = mediator
            self.queryInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_SHOOT_UP_RANK)

    def reset(self):
        self.currentTabIndex = 0

    def show(self):
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo()
            self.queryInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_SHOOT_UP_RANK)

    def queryInfo(self):
        p = BigWorld.player()
        if not p.guild:
            return
        p.cell.queryGuildNoviceBoost(p.guild.noviceBoostVer)

    def onGetProgressInfo(self, *arg):
        self.currentTabIndex = uiConst.GUILD_SHOOT_UP_TAB_GOING
        self.refreshProgressInfo()

    def onGetFinishInfo(self, *arg):
        self.currentTabIndex = uiConst.GUILD_SHOOT_UP_TAB_AWARD
        self.refreshFinishInfo()

    def refreshInfo(self):
        if self.currentTabIndex == uiConst.GUILD_SHOOT_UP_TAB_GOING:
            self.refreshProgressInfo()
        elif self.currentTabIndex == uiConst.GUILD_SHOOT_UP_TAB_AWARD:
            self.refreshFinishInfo()

    def refreshProgressInfo(self):
        if self.mediator:
            p = BigWorld.player()
            if not p.guild:
                return
            info = {}
            info['title'] = GCD.data.get('shootUpRankProgressTitle', '')
            itemList = []
            for gbId, score in p.guild.noviceBoosting.iteritems():
                memberInfo = p.guild.member.get(gbId)
                if memberInfo is None:
                    continue
                typeId, fineScore = (0, 0)
                lv = memberInfo.level
                for key, v in NBSTD.data.iteritems():
                    minLv, maxLv = v.get('minLv', 0), v.get('maxLv', 0)
                    if minLv <= lv and lv < maxLv:
                        typeId = key
                        fineScore = v.get('fineScore', 0)
                        break

                itemInfo = {}
                itemInfo['typeId'] = typeId
                itemInfo['nameField'] = memberInfo.role
                itemInfo['score'] = '%s/%s' % (format(score, ','), format(fineScore, ','))
                itemInfo['gbId'] = str(gbId)
                if not memberInfo.online:
                    itemInfo['nameField'] = uiUtils.toHtml(itemInfo['nameField'], '#808080')
                    itemInfo['score'] = uiUtils.toHtml(itemInfo['score'], '#808080')
                itemList.append(itemInfo)

            info['itemList'] = itemList
            self.mediator.Invoke('refreshProgressInfo', uiUtils.dict2GfxDict(info, True))

    def refreshFinishInfo(self):
        if self.mediator:
            p = BigWorld.player()
            if not p.guild:
                return
            info = {}
            info['title'] = GCD.data.get('shootUpRankFinishTitle', '')
            info['subTitle'] = GCD.data.get('shootUpRankFinishSubTitle', '')
            itemList = []
            for key, value in p.guild.noviceBoosted.iteritems():
                itemInfo = {}
                itemInfo['nameField'] = value.name
                itemInfo['timeField'] = time.strftime('%Y-%m-%d', time.localtime(value.tWhen))
                itemInfo['actId'] = value.actId
                itemInfo['gbId'] = str(key[0])
                itemBonus = clientUtils.genItemBonus(value.getBonusId())
                itemId, _ = itemBonus[0]
                itemInfo['bonusInfo'] = uiUtils.getGfxItemById(itemId)
                if value.state == gametypes.GUILD_NOVICE_BOOST_REWARD_NO:
                    itemInfo['btnLabel'] = '无法领取'
                    itemInfo['btnEnabled'] = False
                elif value.state == gametypes.GUILD_NOVICE_BOOST_REWARD_READY:
                    itemInfo['btnLabel'] = '领取奖励'
                    itemInfo['btnEnabled'] = True
                elif value.state == gametypes.GUILD_NOVICE_BOOST_REWARD_DONE:
                    itemInfo['btnLabel'] = '已领取'
                    itemInfo['btnEnabled'] = False
                itemList.append(itemInfo)

            info['itemList'] = itemList
            self.mediator.Invoke('refreshFinishInfo', uiUtils.dict2GfxDict(info, True))

    def onQuery(self, *arg):
        typeId = int(arg[3][0].GetNumber())
        gbId = int(arg[3][1].GetString())
        gameglobal.rds.ui.newbieGuideExam.setOtherType(typeId)
        BigWorld.player().cell.queryOtherPlayerNoviceBoost(gbId)

    def onAward(self, *arg):
        actId = int(arg[3][0].GetNumber())
        gbId = int(arg[3][1].GetString())
        guild = BigWorld.player().guild
        if not guild:
            return
        val = guild.noviceBoosted.get((gbId, actId))
        if not val:
            return
        BigWorld.player().cell.applyGuildNoviceBoostReward(gbId, actId, val.bPerfect)
