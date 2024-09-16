#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achievementScoreProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import utils
import gametypes
import gameglobal
from item import Item
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from guis import tipUtils
from cdata import achieve_score_data as ASD
from cdata import achieve_score_award_data as ASAD
from data import item_data as ID
from cdata import font_config_data as FCD
from data import achievement_data as AD
from data import bonus_data as BD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class AchievementScoreProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(AchievementScoreProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'achievementScore'
        self.type = 'achievementScore'
        self.modelMap = {'init': self.onInit,
         'getAwardScore': self.onGetAwardScore,
         'gotoAchieve': self.onGotoAchieve,
         'getAwardItem': self.onGetAwardItem,
         'getItemScoreFlag': self.onGetItemScoreFlag}
        self.mediator = None
        self.awardNum = 6
        self.sumScore = 0
        self.awardData = {}
        self.awardScores = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACHIEVEMENT_SCORE, self.hide)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACHIEVEMENT_SCORE)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ACHIEVEMENT_SCORE:
            self.mediator = mediator

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ACHIEVEMENT_SCORE)

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.sumScore = 0
        self.awardData = {}
        self.awardScores = []

    def onInit(self, *arg):
        self.initDesc()
        self.initAward()
        self.initProgressBar()
        self.initAchievement()
        self._checkLock()

    def _checkLock(self):
        nowTime = int(BigWorld.player().getServerTime())
        lockTime = SCD.data.get('lockTime', 0)
        if nowTime > lockTime and self.mediator:
            self.mediator.Invoke('showLock')

    def onGetAwardItem(self, *arg):
        name = arg[3][0].GetString()
        index = self.getIndex(name)
        BigWorld.player().cell.applyAchieveScoreAward(ASAD.data.keys()[index])

    def onGetAwardScore(self, *arg):
        name = arg[3][0].GetString()
        index = self.getIndex(name)
        return GfxValue(self.awardScores[index])

    def onGotoAchieve(self, *arg):
        pass

    def updateSumScore(self, score):
        if self.mediator:
            self.mediator.Invoke('updateSumScore', GfxValue(score))

    def updateItemScore(self, score):
        if self.mediator:
            self.mediator.Invoke('updateItemScore', GfxValue(score))

    def initDesc(self):
        self.mediator.Invoke('initDesc', GfxValue(gbk2unicode(GMD.data.get(GMDD.data.ACHIEVEMENT_SCORE_DESC, {}).get('text', gameStrings.TEXT_ACHIEVEMENTSCOREPROXY_105))))

    def initProgressBar(self):
        if self.mediator:
            for i in xrange(len(self.awardScores)):
                if i == 0:
                    self.mediator.Invoke('setProgressBarMax', (GfxValue(i), GfxValue(self.awardScores[i])))
                else:
                    self.mediator.Invoke('setProgressBarMax', (GfxValue(i), GfxValue(self.awardScores[i] - self.awardScores[i - 1])))

            precent = '0/' + str(self.awardScores[len(self.awardScores) - 1])
            self.mediator.Invoke('setProgressText', GfxValue(precent))

    def initAward(self):
        awardItem = self.movie.CreateArray()
        keys = ASAD.data.keys()
        for i in xrange(len(ASAD.data)):
            obj = self.movie.CreateObject()
            achieveScoreAward = BigWorld.player().achieveScoreAward
            if keys[i] in achieveScoreAward:
                obj.SetMember('status', GfxValue(achieveScoreAward[keys[i]]))
            else:
                obj.SetMember('status', GfxValue(-1))
            awardItem.SetElement(i, obj)

        if self.mediator:
            self.mediator.Invoke('initAwardStatus', awardItem)
        i = 0
        self.awardData = ASAD.data
        for key in self.awardData.keys():
            self.awardScores.append(self.awardData[key].get('score', 0))

        for index in ASAD.data.keys():
            key = self._getKey(i)
            bonusId = ASAD.data[index].get('bonusId', '')
            fixedBonus = BD.data[bonusId].get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            if fixedBonus:
                itemId = fixedBonus[0][1]
            else:
                continue
            item = Item(itemId)
            data = self.uiAdapter.movie.CreateObject()
            icon = uiUtils.getItemIconFile64(item.id)
            idNum = GfxValue(item.id)
            name = GfxValue('item')
            iconPath = GfxValue(icon)
            count = GfxValue(item.cwrap)
            data.SetMember('id', idNum)
            data.SetMember('name', name)
            data.SetMember('iconPath', iconPath)
            data.SetMember('count', count)
            if hasattr(item, 'quality'):
                quality = item.quality
            else:
                quality = ID.data.get(item.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            if self.binding.has_key(key):
                self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
                self.binding[key][1].InvokeSelf(data)
            i += 1

    def _getKey(self, pos):
        return 'achievementScore.awardItem%d' % pos

    def initAchievement(self):
        achievementItem = self.movie.CreateArray()
        i = 0
        self.updateSumScore(BigWorld.player().achieveScore)
        self.updateItemScore(BigWorld.player().itemAchieveScore)
        self.setProgressBar(BigWorld.player().achieveScore)
        keys = [ k[0] for k in sorted(ASD.data.items(), key=lambda d: d[1]['sortId']) ]
        for key in keys:
            obj = self.movie.CreateObject()
            record = AD.data[key]
            obj.SetMember('score', GfxValue(ASD.data[key].get('score', 0)))
            obj.SetMember('detail', GfxValue(gbk2unicode(record.get('name', ''))))
            obj.SetMember('detailContent', GfxValue(gbk2unicode(AD.data[key].get('desc', ''))))
            obj.SetMember('achieveId', GfxValue(key))
            if hasattr(BigWorld.player(), 'achieveScores') and key in BigWorld.player().achieveScores:
                obj.SetMember('status', GfxValue(1))
            else:
                obj.SetMember('status', GfxValue(0))
            achievementItem.SetElement(i, obj)
            i += 1

        if self.mediator:
            self.mediator.Invoke('initAchievement', achievementItem)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        itemId = self.getItemId(key)
        if not itemId:
            return
        return tipUtils.getItemTipById(itemId)

    def getItemId(self, key):
        i = int(key[-1:])
        index = ASAD.data.keys()[i]
        bonusId = ASAD.data[index].get('bonusId', '')
        fixedBonus = BD.data[bonusId].get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        if fixedBonus:
            itemId = fixedBonus[0][1]
        else:
            itemId = 0
        return itemId

    def getIndex(self, name):
        index = int(name[-1:])
        return index

    def setProgressBar(self, score):
        if self.mediator:
            for index in xrange(len(self.awardScores)):
                if score < self.awardScores[index]:
                    if index == 0:
                        self.mediator.Invoke('setProgressBar', (GfxValue(index), GfxValue(score), GfxValue(True)))
                    else:
                        self.mediator.Invoke('setProgressBar', (GfxValue(index), GfxValue(score - self.awardScores[index - 1]), GfxValue(True)))
                elif score >= self.awardScores[index]:
                    if index == 0:
                        self.mediator.Invoke('setProgressBar', (GfxValue(index), GfxValue(self.awardScores[index]), GfxValue(False)))
                    else:
                        self.mediator.Invoke('setProgressBar', (GfxValue(index), GfxValue(self.awardScores[index] - self.awardScores[index - 1]), GfxValue(False)))

            precent = str(score) + '/' + str(self.awardScores[len(self.awardScores) - 1])
            self.mediator.Invoke('setProgressText', GfxValue(precent))
        else:
            return

    def updateAchieveStatus(self, achieveId):
        self.updateSumScore(BigWorld.player().achieveScore)
        self.updateItemScore(BigWorld.player().itemAchieveScore)
        self.setProgressBar(BigWorld.player().achieveScore)
        for index in xrange(len(ASD.data.keys())):
            if achieveId == ASD.data.keys()[index]:
                obj = self.movie.CreateObject()
                if achieveId in BigWorld.player().achieveScores:
                    obj.SetMember('status', GfxValue(1))
                else:
                    obj.SetMember('status', GfxValue(0))
                if self.mediator:
                    self.mediator.Invoke('updateAchieveStatus', (GfxValue(achieveId), obj))
                break

    def updateAwardStatus(self, awardId):
        keys = ASAD.data.keys()
        for i in xrange(len(ASAD.data)):
            if awardId == keys[i]:
                obj = self.movie.CreateObject()
                achieveScoreAward = BigWorld.player().achieveScoreAward
                if keys[i] in achieveScoreAward:
                    obj.SetMember('status', GfxValue(achieveScoreAward[keys[i]]))
                else:
                    obj.SetMember('status', GfxValue(-1))
                if self.mediator:
                    self.mediator.Invoke('updateAwardStatus', (GfxValue(i), obj))
                break

    def onGetItemScoreFlag(self, *args):
        return GfxValue(SCD.data.get('ShowAchievementItemScore', False))
