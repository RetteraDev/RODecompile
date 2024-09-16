#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/duelMatchTimeProxy.o
from gamestrings import gameStrings
from Scaleform import GfxValue
import utils
import formula
import gamelog
import const
from uiProxy import DataProxy
from guis import uiConst
from ui import gbk2unicode
from guis import uiUtils
from data import battle_field_data as BFD
from data import arena_mode_data as AMD
from data import fame_data as FD

class DuelMatchTimeProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(DuelMatchTimeProxy, self).__init__(uiAdapter)
        self.bindType = 'duelMatchTime'
        self.mediator = None
        self.modelMap = {'getDuelMatchInfo': self.onGetDuelMatchInfo,
         'getExtraReward': self.onGetExtraReward}
        self.duelMatchMap = {}

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DUEL_MATCH_TIME:
            self.mediator = mediator

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_DUEL_MATCH_TIME)

    def clearWidget(self):
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DUEL_MATCH_TIME)

    def onGetDuelMatchInfo(self, *arg):
        ret = self.movie.CreateArray()
        for index, val in enumerate(self.duelMatchMap.values()):
            obj = self.movie.CreateObject()
            obj.SetMember('fbNo', GfxValue(val.fbNo))
            obj.SetMember('duration', GfxValue(val.getDurantionTime()))
            obj.SetMember('titleDesc', GfxValue(gbk2unicode(val.getTitleDesc())))
            if val.hasExtraReward():
                obj.SetMember('hasExtraReward', GfxValue(True))
                obj.SetMember('rewardTxt', GfxValue(gbk2unicode(val.getExtraRewardTxt())))
            ret.SetElement(index, obj)

        return ret

    def onGetExtraReward(self, *arg):
        fbNo = int(arg[3][0].GetNumber())
        val = self.duelMatchMap.get(fbNo)
        if val and val.hasExtraReward():
            return GfxValue(gbk2unicode(val.getExtraRewardTxt()))

    def addMatchTimeItem(self, fbNo):
        gamelog.debug('@hjx matchTime#addMatchTimeItem:', fbNo)
        if not self.duelMatchMap.has_key(fbNo):
            if formula.inBattleField(fbNo):
                self.duelMatchMap[fbNo] = BFMatchTimeItem(fbNo)
            else:
                self.duelMatchMap[fbNo] = ArenaMatchTimeItem(fbNo)
        self.refreshDuelMatch()

    def removeMatchTimeItem(self, fbNo):
        gamelog.debug('@hjx matchTime#removeMatchTimeItem:', fbNo)
        self.duelMatchMap.pop(fbNo, None)
        if len(self.duelMatchMap) == 0:
            self.hide()
        else:
            self.refreshDuelMatch()

    def refreshDuelMatch(self):
        if self.mediator:
            self.mediator.Invoke('refreshMatchingTime')
        else:
            self.show()

    def resetDuelMatch(self):
        self.duelMatchMap.clear()
        self.hide()


class IDuelMatchTimeItem(object):

    def __init__(self, fbNo):
        self.fbNo = fbNo
        self.startTimeStamp = utils.getNow()
        self.titleDesc = ''

    def getDurantionTime(self):
        return int(utils.getNow() - self.startTimeStamp)

    def getTitleDesc(self):
        return self.titleDesc

    def hasExtraReward(self):
        return False


class ArenaMatchTimeItem(IDuelMatchTimeItem):

    def __init__(self, arenaMode):
        super(ArenaMatchTimeItem, self).__init__(arenaMode)
        self.titleDesc = gameStrings.TEXT_DUELMATCHTIMEPROXY_110 + AMD.data.get(arenaMode, {}).get('name', '') + gameStrings.TEXT_DUELMATCHTIMEPROXY_110_1


class BFMatchTimeItem(IDuelMatchTimeItem):

    def __init__(self, fbNo):
        super(BFMatchTimeItem, self).__init__(fbNo)
        self.titleDesc = gameStrings.TEXT_DUELMATCHTIMEPROXY_115 + BFD.data.get(fbNo, {}).get('name', '') + gameStrings.TEXT_DUELMATCHTIMEPROXY_110_1

    def hasExtraReward(self):
        if formula.inHookBattleField(self.fbNo) or formula.inHuntBattleField(self.fbNo):
            return False
        else:
            return True

    def getExtraReward(self):
        cnt = utils.calcBattleFieldWaitRewardJunzi(self.startTimeStamp, utils.getNow())
        return (const.JUN_ZI_FAME_ID, cnt)

    def getExtraRewardTxt(self):
        fameId, cnt = self.getExtraReward()
        fameName = FD.data.get(fameId, {}).get('name', '')
        rewardTxt = '%s %s' % (uiUtils.toHtml(cnt, '#29B1CC'), uiUtils.toHtml(fameName, '#FFFFFF'))
        return rewardTxt
