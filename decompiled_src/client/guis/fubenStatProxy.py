#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenStatProxy.o
from gamestrings import gameStrings
import BigWorld
import const
import gamelog
import gameglobal
import combatUtils
from Scaleform import GfxValue
from callbackHelper import Functor
from guis.uiProxy import UIProxy
from guis import uiConst, uiUtils
from fbStatistics import FubenStats
from ui import gbk2unicode
from ui import unicode2gbk
from gameStrings import gameStrings
from data import monster_data as MD
from data import skill_general_template_data as SGTD
STAT_KEY_TOTAL = -1
STAT_KEY_TIME = -2
BOSS_KEY_TOTAL = -1
BOSS_KEY_CURRENT = -2
MAX_VALUE = 99999
STAT_KEYS = (STAT_KEY_TIME,
 FubenStats.K_DAMAGE,
 FubenStats.K_DPS,
 FubenStats.K_BEDAMAGE,
 FubenStats.K_CURE,
 FubenStats.K_DEATH_CNT,
 FubenStats.K_RELIVE_HERE_CNT,
 FubenStats.K_RELIVE_NEAR_CNT,
 FubenStats.K_RELIVE_BY_SKILL_CNT)
SKILL_LIST_STAT_KEYS = (FubenStats.K_DAMAGE,
 FubenStats.K_DPS,
 FubenStats.K_CURE,
 FubenStats.K_BEDAMAGE)
SKILL_DETAIL_KYE_DICT = {FubenStats.K_DAMAGE: FubenStats.K_SKILL_DAMAGE,
 FubenStats.K_DPS: FubenStats.K_SKILL_DPS,
 FubenStats.K_CURE: FubenStats.K_SKILL_CURE,
 FubenStats.K_BEDAMAGE: FubenStats.K_SKILL_BEDAMAGE}
SPRITE_SKILL_DETAIL_KYE_DICT = {FubenStats.K_DAMAGE: FubenStats.K_SPRITE_SKILL_DAMAGE,
 FubenStats.K_DPS: FubenStats.K_SPRITE_SKILL_DPS,
 FubenStats.K_CURE: FubenStats.K_SPRITE_SKILL_HEAL,
 FubenStats.K_BEDAMAGE: FubenStats.K_SPRITE_SKILL_BEDAMAGE}
SKILL_BOSS_DETAIL_KYE_DICT = {FubenStats.K_DAMAGE: FubenStats.K_SKILL_DAMAGE,
 FubenStats.K_DPS: FubenStats.K_BOSS_COMBAT_SKILL_DPS,
 FubenStats.K_CURE: FubenStats.K_SKILL_CURE,
 FubenStats.K_BEDAMAGE: FubenStats.K_SKILL_BEDAMAGE}
SPRITE_SKILL_BOSS_DETAIL_KYE_DICT = {FubenStats.K_DAMAGE: FubenStats.K_SPRITE_SKILL_DAMAGE,
 FubenStats.K_DPS: FubenStats.K_SPRITE_BOSS_COMBAT_SKILL_DPS,
 FubenStats.K_CURE: FubenStats.K_SPRITE_SKILL_HEAL,
 FubenStats.K_BEDAMAGE: FubenStats.K_SPRITE_SKILL_BEDAMAGE}
PLAYER_TO_SPRITE_KYE_DICT = {FubenStats.K_DAMAGE: FubenStats.K_SPRITE_DAMAGE,
 FubenStats.K_DPS: FubenStats.K_SPRITE_DPS,
 FubenStats.K_CURE: FubenStats.K_SPRITE_HEAL,
 FubenStats.K_BEDAMAGE: FubenStats.K_SPRITE_BE_DAMAGE}
STAT_DICT = {STAT_KEY_TIME: gameStrings.TEXT_FUBENSTATPROXY_64,
 FubenStats.K_DAMAGE: gameStrings.TEXT_FUBENSTATPROXY_65,
 FubenStats.K_DPS: gameStrings.TEXT_FUBENSTATPROXY_66,
 FubenStats.K_BEDAMAGE: gameStrings.TEXT_FUBENSTATPROXY_67,
 FubenStats.K_CURE: gameStrings.TEXT_FUBENSTATPROXY_68,
 FubenStats.K_DEATH_CNT: gameStrings.TEXT_FUBENSTATPROXY_69,
 FubenStats.K_RELIVE_HERE_CNT: gameStrings.TEXT_FUBENSTATPROXY_70,
 FubenStats.K_RELIVE_NEAR_CNT: gameStrings.TEXT_FUBENSTATPROXY_71,
 FubenStats.K_RELIVE_BY_SKILL_CNT: gameStrings.TEXT_FUBENSTATPROXY_72}
STAT_MENU_KEY = (STAT_KEY_TOTAL,
 FubenStats.K_DAMAGE,
 FubenStats.K_DPS,
 FubenStats.K_BEDAMAGE,
 FubenStats.K_CURE,
 FubenStats.K_DEATH_CNT,
 FubenStats.K_RELIVE_HERE_CNT,
 FubenStats.K_RELIVE_NEAR_CNT,
 FubenStats.K_RELIVE_BY_SKILL_CNT)
STAT_MENU_DICT = {FubenStats.K_DAMAGE: gameStrings.TEXT_FUBENSTATPROXY_65,
 STAT_KEY_TOTAL: gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_158,
 FubenStats.K_DPS: gameStrings.TEXT_FUBENSTATPROXY_66,
 FubenStats.K_BEDAMAGE: gameStrings.TEXT_FUBENSTATPROXY_67,
 FubenStats.K_CURE: gameStrings.TEXT_FUBENSTATPROXY_68,
 FubenStats.K_DEATH_CNT: gameStrings.TEXT_FUBENSTATPROXY_69,
 FubenStats.K_RELIVE_HERE_CNT: gameStrings.TEXT_FUBENSTATPROXY_70,
 FubenStats.K_RELIVE_NEAR_CNT: gameStrings.TEXT_FUBENSTATPROXY_71,
 FubenStats.K_RELIVE_BY_SKILL_CNT: gameStrings.TEXT_FUBENSTATPROXY_72}

class FubenStatProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FubenStatProxy, self).__init__(uiAdapter)
        self.modelMap = {'initDone': self.onInitDone,
         'changeBoss': self.onChangeBoss,
         'sendToChat': self.onSendToChat,
         'changeStat': self.onChangeStatKey,
         'clearStat': self.onClearStat,
         'showSkillList': self.onShowSkillList,
         'sendSkillListToChat': self.onSendSkillListToChat,
         'changeHateBoss': self.onChangeHateBoss,
         'sendHateToChat': self.onSendHateToChat}
        self.reset()
        self.destroyOnHide = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FB_STAT:
            self.med = mediator
        else:
            if widgetId == uiConst.WIDGET_FB_STAT_SKILL_lIST:
                self.skillMed = mediator
                return uiUtils.dict2GfxDict(self.skillListData, True)
            if widgetId == uiConst.WIDGET_FB_HATE_LIST:
                self.hateMed = mediator
                self.setAllHateBoss(self.hateStatBosses, True)
                return uiUtils.dict2GfxDict(self.hateListData, True)

    def show(self, *args):
        showByUser = False
        if args and len(args):
            self.statType = args[0]
            if len(args) >= 2:
                showByUser = args[1]
        else:
            self.statType = None
        if BigWorld.player().inFuben():
            self.uiAdapter.checkStateAndLoad(uiConst.WIDGET_FB_STAT, showByUser)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FB_STAT)

    def showHateList(self, showByUser = False):
        self.uiAdapter.checkStateAndLoad(uiConst.WIDGET_FB_HATE_LIST, showByUser)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FB_STAT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FB_STAT_SKILL_lIST)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FB_HATE_LIST)
        self.med = None
        self.skillMed = None
        if self.callBack:
            BigWorld.cancelCallback(self.callBack)
        if self.dpsCallback:
            BigWorld.cancelCallback(self.dpsCallback)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_FB_STAT_SKILL_lIST:
            self.skillListData = None
            self.skillMed = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FB_STAT_SKILL_lIST)
        elif widgetId == uiConst.WIDGET_FB_HATE_LIST:
            self.hateListData = None
            self.hateMed = None
            gameglobal.rds.ui.unLoadWidget(widgetId)
        else:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FB_STAT)
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FB_STAT_SKILL_lIST)
            self.med = None
            self.skillMed = None
            if self.callBack:
                BigWorld.cancelCallback(self.callBack)
            if self.dpsCallback:
                BigWorld.cancelCallback(self.dpsCallback)
            self.med = None
            self.selectBoss = None
            self.statKey = None
            self.callBack = None
            self.timerId = None
            self.statType = None
            self.dpsValues = {}
            self.dpsCallback = None
            self.lastMainStat = None
            self.lastTotalDps = None

    def reset(self):
        self.med = None
        self.fbStatDict = {}
        self.bossStatDict = {}
        self.selectBoss = None
        self.statKey = None
        self.currentStatBoss = 0
        self.callBack = None
        self.timerId = None
        self.statType = None
        self.dpsValues = {}
        self.dpsCallback = None
        self.lastMainStat = None
        self.lastTotalDps = None
        self.skillListData = None
        self.skillMed = None
        self.needRefreshBossTitle = False
        self.hateMed = None
        self.hateListData = {}
        self.hateSelectBoss = None
        self.hateStatBosses = [0]
        self.tempStatDict = {}

    def resetAvatarCombatStats(self, spaceNo, gbIdList):
        gamelog.info('jbx:resetAvatarCombatStats', spaceNo, gbIdList)
        self._innerClearStat()

    def onInitDone(self, *args):
        if self.statType == uiConst.STAT_TYPE_ONLY_DPS:
            self.initDpsStat()
        else:
            self.refreshStatTitle()
            self.refreshBossTitle()
            self.setUISelect(BOSS_KEY_TOTAL)
            self.selectBoss = BOSS_KEY_TOTAL
            self.statKey = STAT_KEY_TOTAL
            self.lastMainStat = None
            self.lastTotalDps = None
            self.refreshContent()

    def onChangeBoss(self, *args):
        sBoss = args[3][0].GetNumber()
        if sBoss == self.selectBoss:
            return
        else:
            self.selectBoss = sBoss
            self.lastMainStat = None
            self.lastTotalDps = None
            self.refreshContent()
            return

    def onChangeStatKey(self, *args):
        sKey = args[3][0].GetNumber()
        if sKey == self.statKey or sKey == STAT_KEY_TIME:
            return
        else:
            self.statKey = sKey
            self.lastMainStat = None
            self.lastTotalDps = None
            self.refreshContent()
            return

    def onClearStat(self, *args):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_FUBENSTATPROXY_235, self._innerClearStat)

    def _innerClearStat(self):
        if self.statType == uiConst.STAT_TYPE_ONLY_DPS:
            BigWorld.player().cell.endDpsCalc()
            self.tempStatDict = {}
            self._refreshDpsContent()
        else:
            for key in self.fbStatDict.keys():
                stat = FubenStats()
                stat.record(FubenStats.K_FB_START_TIME, BigWorld.player().getServerTime())
                self.fbStatDict[key] = stat

            self.bossStatDict = {}
            self.lastMainStat = None
            self.lastTotalDps = 0
            self.refreshContent()
            BigWorld.player().cell.resetFubenStats()

    def onSendToChat(self, *args):
        msg = unicode2gbk(args[3][0].GetString())
        gameglobal.rds.ui.chat.chatToCurrentChannel(msg)

    def onSendSkillListToChat(self, *args):
        gameglobal.rds.ui.chat.chatToCurrentChannel(self._getSkillDatasStr())

    def onChangeHateBoss(self, *args):
        bossId = args[3][0].GetNumber()
        self.changeHateBoss(bossId)

    def onSendHateToChat(self, *args):
        gameglobal.rds.ui.chat.chatToCurrentChannel(self._getHateDatasStr())

    def refreshSelfDpsSkillWnd(self):
        p = BigWorld.player()
        gbId = p.gbId
        name = p.roleName
        self._refreshDpsSkillListData(gbId, name)
        if self.skillMed:
            self.skillMed.Invoke('refreshData', uiUtils.dict2GfxDict(self.skillListData, True))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FB_STAT_SKILL_lIST)

    def onShowSkillList(self, *args):
        if self.statType == uiConst.STAT_TYPE_ONLY_DPS:
            p = BigWorld.player()
            self.tempStatDict[p.gbId] = combatUtils.genDmgDpsStats(p, p.summonedSpriteInWorld)
            if not self.tempStatDict:
                return
            gbId = args[3][0].GetString()
            name = unicode2gbk(args[3][1].GetString())
            self._refreshDpsSkillListData(gbId, name)
            if self.skillMed:
                self.skillMed.Invoke('refreshData', uiUtils.dict2GfxDict(self.skillListData, True))
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FB_STAT_SKILL_lIST)
        else:
            if self.statKey not in SKILL_LIST_STAT_KEYS:
                return
            gbId = args[3][0].GetString()
            name = unicode2gbk(args[3][1].GetString())
            self._refreshSkillListData(gbId, name)
            if self.skillMed:
                self.skillMed.Invoke('refreshData', uiUtils.dict2GfxDict(self.skillListData, True))
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FB_STAT_SKILL_lIST)

    def setAllHateBoss(self, bosses, forceRefresh = False):
        if self.hateStatBosses != bosses or forceRefresh:
            self.hateStatBosses = bosses
            arr = []
            if len(self.hateStatBosses):
                for bossId in self.hateStatBosses:
                    data = {'bossId': bossId}
                    data['label'] = MD.data.get(bossId, {}).get('name', gameStrings.TEXT_FUBENSTATPROXY_311)
                    arr.append(data)

            else:
                arr.append({'label': gameStrings.TEXT_FUBENSTATPROXY_311,
                 'id': 0})
            if self.hateMed:
                self.hateMed.Invoke('setBossList', uiUtils.array2GfxAarry(arr, True))
            self.changeHateBoss(self.hateStatBosses[0] if len(self.hateStatBosses) else 0, forceRefresh)

    def changeHateBoss(self, bossId, forceRefresh = False):
        if self.hateSelectBoss != bossId or forceRefresh:
            self.hateSelectBoss = bossId
            self.refreshHateView()

    def getMembers(self):
        p = BigWorld.player()
        if p.inFightObserve():
            return p.getObservedMembers()
        else:
            return p.members

    def refreshHateView(self):
        if not self.hateMed:
            return
        else:
            p = BigWorld.player()
            self.hateListData = []
            hateValue = {}
            for gbId, stat in self.bossStatDict.get(self.hateSelectBoss, {}).items():
                hateValue[gbId] = stat.getStats(FubenStats.K_BOSS_HATE).get(self.hateSelectBoss, 0)

            keys = hateValue.keys()
            if p.gbId not in keys and not p.inFightObserve():
                keys.append(p.gbId)
            members = self.getMembers()
            if members:
                for mGbId in members:
                    if mGbId not in keys:
                        keys.append(mGbId)

            keys.sort(cmp=lambda x, y: cmp(hateValue.get(y), hateValue.get(x)))
            firstValue = None
            rank = 1
            for gbId in keys:
                hate = hateValue.get(gbId, 0)
                if firstValue == None:
                    firstValue = hate
                obj = {}
                name, school = self._getPlayerInfo(gbId)
                if not name:
                    continue
                obj['rank'] = rank
                obj['gbId'] = str(gbId)
                obj['name'] = name
                obj['school'] = school
                firstPercent = 0 if firstValue == 0 else round(1.0 * hate / firstValue, 3)
                obj['value'] = str(hate) + '(%s%%)' % str(100 * firstPercent)
                obj['percent'] = firstPercent
                self.hateListData.append(obj)
                rank += 1

            self.hateMed.Invoke('refreshHateList', uiUtils.array2GfxAarry(self.hateListData, True))
            return

    def refreshStatTitle(self):
        if self.med:
            arr = self.movie.CreateArray()
            index = 0
            for key in STAT_MENU_KEY:
                obj = self.movie.CreateObject()
                obj.SetMember('statKey', GfxValue(key))
                obj.SetMember('label', GfxValue(gbk2unicode(STAT_MENU_DICT.get(key, ''))))
                arr.SetElement(index, obj)
                index += 1

            self.med.Invoke('setStatMenuData', arr)

    def refreshBossTitle(self):
        if self.med:
            arr = self.movie.CreateArray()
            obj = self.movie.CreateObject()
            obj.SetMember('bossId', GfxValue(BOSS_KEY_CURRENT))
            obj.SetMember('label', GfxValue(gbk2unicode(gameStrings.TEXT_FUBENSTATPROXY_311)))
            arr.SetElement(0, obj)
            obj = self.movie.CreateObject()
            obj.SetMember('bossId', GfxValue(BOSS_KEY_TOTAL))
            obj.SetMember('label', GfxValue(gbk2unicode(gameStrings.TEXT_ACTIVITYFACTORY_107)))
            arr.SetElement(1, obj)
            index = 2
            for bossId in self.bossStatDict.keys():
                monsterName = MD.data.get(bossId, {}).get('name')
                if monsterName:
                    obj = self.movie.CreateObject()
                    obj.SetMember('bossId', GfxValue(bossId))
                    count = self.bossStatDict[bossId].get(BigWorld.player().gbId, FubenStats()).getStats(FubenStats.K_BOSS_COMBAT_CNT).get(bossId, 0)
                    if count > 1:
                        monsterName += '(%d)' % count
                    obj.SetMember('label', GfxValue(gbk2unicode(monsterName)))
                    arr.SetElement(index, obj)
                    index += 1

            self.med.Invoke('setBossMenuData', arr)

    def refreshContent(self):
        if self.callBack:
            BigWorld.cancelCallback(self.callBack)
            self.callBack = None
        if self.med and self.statKey != None and self.selectBoss != None:
            if self.statKey == STAT_KEY_TOTAL:
                totalStats, dps = self._getMainStat(self.selectBoss)
                if totalStats:
                    arr = self.movie.CreateArray()
                    for i in xrange(len(STAT_KEYS)):
                        obj = self.movie.CreateObject()
                        obj.SetMember('key', GfxValue(STAT_KEYS[i]))
                        value = 0
                        label = STAT_DICT.get(STAT_KEYS[i], '')
                        if STAT_KEYS[i] == STAT_KEY_TIME:
                            label = label % (gameStrings.TEXT_GROUPDETAILFACTORY_28 if self.selectBoss == BOSS_KEY_TOTAL else gameStrings.TEXT_FUBENSTATPROXY_422_1)
                            if self.selectBoss == BOSS_KEY_TOTAL:
                                startTime = totalStats.getStats(FubenStats.K_FB_START_TIME)
                                endTime = 0
                            else:
                                boss = self.currentStatBoss if self.selectBoss == BOSS_KEY_CURRENT else self.selectBoss
                                startTime = totalStats.getStats(FubenStats.K_MONSTER_ENTER_COMBAT_TIME).get(boss)
                                endTime = totalStats.getStats(FubenStats.K_MONSTER_LEAVE_COMBAT_TIME).get(boss)
                            if startTime:
                                if endTime and endTime > startTime:
                                    value = self.timeStr(endTime - startTime)
                                else:
                                    tTime = BigWorld.player().getServerTime() - startTime
                                    value = self.timeStr(tTime)
                                    self.callBack = BigWorld.callback(1, Functor(self.refreshTimeTxt, tTime))
                                    self.timerId = '%d_%d' % (self.statKey, self.selectBoss)
                                    obj.SetMember('timerId', GfxValue(self.timerId))
                        elif STAT_KEYS[i] == FubenStats.K_DPS:
                            value = dps
                        else:
                            value = totalStats.getStats(STAT_KEYS[i])
                        obj.SetMember('value', GfxValue(gbk2unicode(self._formatValue(value))))
                        obj.SetMember('label', GfxValue(gbk2unicode(label)))
                        arr.SetElement(i, obj)

                    self.med.Invoke('refreshMainContent', arr)
            else:
                totalStats, dps = self._getMainStat(self.selectBoss)
                if totalStats:
                    tempKey = self.statKey
                    if self.selectBoss != BOSS_KEY_TOTAL and self.statKey == FubenStats.K_DPS:
                        tempKey = FubenStats.K_BOSS_COMBAT_DPS
                    totalValue = totalStats.getStats(tempKey)
                    if self.selectBoss == -1:
                        statDict = self.fbStatDict
                    else:
                        bKey = self.currentStatBoss if self.selectBoss == BOSS_KEY_CURRENT else self.selectBoss
                        statDict = self.bossStatDict.get(bKey, {})
                    arr = self.movie.CreateArray()
                    i = 0
                    keys = statDict.keys()
                    p = BigWorld.player()
                    if p.gbId not in keys and not p.inFightObserve():
                        keys.append(p.gbId)
                    members = self.getMembers()
                    if members:
                        for mGbId in members:
                            if mGbId not in keys:
                                keys.append(mGbId)

                    keys.sort(cmp=lambda x, y: cmp(statDict.get(y, FubenStats()).getStats(tempKey), statDict.get(x, FubenStats()).getStats(tempKey)))
                    firstValue = None
                    for key in keys:
                        obj = self.movie.CreateObject()
                        name, school = self._getPlayerInfo(key)
                        if not name:
                            continue
                        obj.SetMember('gbId', GfxValue(str(key)))
                        obj.SetMember('name', GfxValue(gbk2unicode(name)))
                        obj.SetMember('school', GfxValue(school))
                        spriteValue = 0
                        if key in statDict.keys():
                            value = statDict[key].getStats(tempKey)
                            if tempKey in PLAYER_TO_SPRITE_KYE_DICT.keys():
                                spriteValue = statDict[key].getStats(PLAYER_TO_SPRITE_KYE_DICT[tempKey])
                        else:
                            value = 0
                        if firstValue == None:
                            firstValue = value
                        pecent = 0 if totalValue == 0 else round(1.0 * value / totalValue, 3)
                        firstPercent = 0 if firstValue == 0 else round(1.0 * value / firstValue, 3)
                        backBgPer = 0 if firstValue == 0 else round(1.0 * max(0, value - spriteValue) / firstValue, 3)
                        if tempKey == FubenStats.K_DPS or tempKey == FubenStats.K_BOSS_COMBAT_DPS:
                            obj.SetMember('value', GfxValue(value))
                            obj.SetMember('percent', GfxValue(firstPercent))
                            obj.SetMember('backBgPer', GfxValue(backBgPer))
                        else:
                            obj.SetMember('value', GfxValue(gbk2unicode(str(self._formatValue(value)) + '(%s%%)' % str(pecent * 100))))
                            obj.SetMember('percent', GfxValue(firstPercent))
                            obj.SetMember('backBgPer', GfxValue(backBgPer))
                        arr.SetElement(i, obj)
                        i += 1

                    self.med.Invoke('refreshMainContent', (arr, GfxValue(False)))

    def onEnterFuben(self, fbNo):
        self.reset()

    def setUISelect(self, selectBoss):
        if not selectBoss:
            return
        if self.med:
            self.med.Invoke('setSelectBoss', GfxValue(selectBoss))

    def refreshTimeTxt(self, time):
        if self.med:
            time += 1
            self.med.Invoke('refreshTimerText', (GfxValue(self.timerId), GfxValue(self.timeStr(time))))
            self.callBack = BigWorld.callback(1, Functor(self.refreshTimeTxt, time))

    def updateTempStat(self, gbId, fbStat, addTotal = True):
        if addTotal:
            if self.tempStatDict.has_key(gbId):
                self.tempStatDict.get(gbId).patchStats(fbStat)
            else:
                self.tempStatDict[gbId] = fbStat

    def updateFbStat(self, gbId, bossCharType, statsDict, addTotal = True):
        fbStat = FubenStats(statsDict)
        if len(fbStat.getStats(FubenStats.K_BOSS_COMBAT_CNT)) > 0:
            self.needRefreshBossTitle = True
            self.lastMainStat = None
            self.lastTotalDps = None
        if addTotal:
            if self.fbStatDict.has_key(gbId):
                self.fbStatDict.get(gbId).patchStats(fbStat)
            else:
                self.fbStatDict[gbId] = fbStat
            if self.selectBoss == BOSS_KEY_TOTAL and self.lastMainStat:
                self.lastMainStat.patchStats(fbStat)
                if statsDict.has_key(FubenStats.K_DPS):
                    self.lastTotalDps[gbId] = fbStat.getStats(FubenStats.K_DPS)
        if bossCharType > 0:
            if self.currentStatBoss != bossCharType:
                self.currentStatBoss = bossCharType
                self.lastMainStat = None
                self.lastTotalDps = None
            elif self.lastMainStat and self.getRealSelectBoss() == bossCharType:
                self.lastMainStat.patchStats(fbStat)
                if statsDict.has_key(FubenStats.K_BOSS_COMBAT_DPS):
                    self.lastTotalDps[gbId] = fbStat.getStats(FubenStats.K_BOSS_COMBAT_DPS)
            if self.bossStatDict.has_key(bossCharType):
                bossStats = self.bossStatDict.get(bossCharType)
            else:
                self.lastMainStat = None
                self.lastTotalDps = None
                self.needRefreshBossTitle = True
                bossStats = {}
                self.bossStatDict[bossCharType] = bossStats
            if bossStats.has_key(gbId):
                bossStats.get(gbId).patchStats(fbStat)
            else:
                bossStats[gbId] = FubenStats(statsDict)

    def getRealSelectBoss(self):
        if self.selectBoss == BOSS_KEY_CURRENT:
            return self.currentStatBoss
        return self.selectBoss

    def refreshView(self):
        self.refreshContent()
        if self.needRefreshBossTitle:
            self.refreshBossTitle()
            self.setUISelect(self.selectBoss)
            self.needRefreshBossTitle = False

    def resetBossStat(self, bossCharType):
        self.currentStatBoss = bossCharType
        if self.bossStatDict.has_key(bossCharType):
            num = self.bossStatDict[bossCharType].get(BigWorld.player().gbId, FubenStats()).getStats(FubenStats.K_BOSS_COMBAT_CNT)
            self.bossStatDict[bossCharType] = {}
            self.bossStatDict[bossCharType][BigWorld.player().gbId] = FubenStats({FubenStats.K_BOSS_COMBAT_CNT: num})
        self.refreshContent()
        self.refreshBossTitle()
        self.setUISelect(self.selectBoss)

    def _getMainStat(self, boss, cache = True):
        if cache and self.lastMainStat:
            return [self.lastMainStat, sum(self.lastTotalDps.values())]
        else:
            if cache:
                self.lastTotalDps = {}
            dps = 0
            if boss == BOSS_KEY_CURRENT:
                boss = self.currentStatBoss
            if boss == BOSS_KEY_TOTAL:
                statDict = self.fbStatDict
            else:
                statDict = self.bossStatDict.get(boss, None)
            totalStats = FubenStats()
            if statDict:
                for gbId, stats in statDict.items():
                    totalStats.patchStats(stats, exlude=(FubenStats.K_BOSS_COMBAT_CNT,))
                    if gbId == BigWorld.player().gbId:
                        totalStats.record(FubenStats.K_BOSS_COMBAT_CNT, stats.getStats(FubenStats.K_BOSS_COMBAT_CNT), FubenStats.RECORD_TYPE_SET)
                    if boss == BOSS_KEY_TOTAL:
                        tempDps = stats.getStats(FubenStats.K_DPS)
                    else:
                        tempDps = stats.getStats(FubenStats.K_BOSS_COMBAT_DPS)
                    if cache:
                        self.lastTotalDps[gbId] = tempDps
                    dps += tempDps

            if cache:
                self.lastMainStat = totalStats
            else:
                self.lastMainStat = None
                self.lastTotalDps = None
            return [totalStats, dps]

    def _getPlayerInfo(self, gbId):
        p = BigWorld.player()
        if gbId == p.gbId:
            return (p.realRoleName, p.school)
        members = self.getMembers()
        name = members.get(gbId, {}).get('roleName', '')
        school = members.get(gbId, {}).get('school', 0)
        return (name, school)

    def timeStr(self, time):
        h = str(int(time / 3600))
        m = str(int(time % 3600 / 60))
        s = str(int(time % 60))
        if len(h) < 2:
            h = '0' + h
        if len(m) < 2:
            m = '0' + m
        if len(s) < 2:
            s = '0' + s
        return '%s:%s:%s' % (h, m, s)

    def initDpsStat(self):
        if self.med:
            p = BigWorld.player()
            arr = self.movie.CreateArray()
            obj = self.movie.CreateObject()
            obj.SetMember('statKey', GfxValue(FubenStats.K_DPS))
            obj.SetMember('label', GfxValue(gbk2unicode(STAT_MENU_DICT.get(FubenStats.K_DPS, ''))))
            arr.SetElement(0, obj)
            self.med.Invoke('setStatMenuData', arr)
            self._refreshDpsContent()
            self.setUISelect(BOSS_KEY_CURRENT)

    def _refreshDpsContent(self):
        if not self.med:
            return
        else:
            p = BigWorld.player()
            target = BigWorld.entities.get(p.dmgTarget)
            if not target:
                self.hide()
                return
            arr = self.movie.CreateArray()
            obj = self.movie.CreateObject()
            obj.SetMember('bossId', GfxValue(BOSS_KEY_CURRENT))
            label = MD.data.get(target.charType, {}).get('name', gameStrings.TEXT_FUBENSTATPROXY_673)
            obj.SetMember('label', GfxValue(gbk2unicode(label)))
            arr.SetElement(0, obj)
            self.med.Invoke('setBossMenuData', arr)
            self.dpsValues = {}
            self.dpsValues[p.gbId] = (self.getDpsValue(p), self.getDpsValue(p.getSpriteInWorld()))
            members = self.getMembers()
            if members:
                for mGbId in members:
                    if mGbId not in self.dpsValues.keys():
                        mId = members.get(mGbId, {}).get('id', 0)
                        mEn = BigWorld.entities.get(mId)
                        if mEn:
                            self.dpsValues[mGbId] = (self.getDpsValue(mEn), self.getDpsValue(mEn.getSpriteInWorld()))
                        else:
                            self.dpsValues[mGbId] = (0, -1)

            keys = self.dpsValues.keys()
            keys.sort(cmp=lambda x, y: cmp(sum(self.dpsValues.get(y, (0, 0))), sum(self.dpsValues.get(x, (0, 0)))))
            firstValue = None
            arr = self.movie.CreateArray()
            i = 0
            for key in keys:
                obj = self.movie.CreateObject()
                name, school = self._getPlayerInfo(key)
                if not name:
                    continue
                obj.SetMember('name', GfxValue(gbk2unicode(name)))
                obj.SetMember('school', GfxValue(school))
                obj.SetMember('gbId', GfxValue(str(key)))
                values = self.dpsValues.get(key, (0, 0))
                value = sum(values)
                if firstValue == None:
                    firstValue = value
                firstPercent = 0 if firstValue == 0 else round(1.0 * value / firstValue, 3)
                backBgPer = 0 if firstValue == 0 else round(1.0 * values[0] / firstValue, 3)
                s = '%s+%s' % values
                if values[1] == -1:
                    s = values[0]
                obj.SetMember('value', GfxValue(s))
                obj.SetMember('percent', GfxValue(firstPercent))
                obj.SetMember('backBgPer', GfxValue(backBgPer))
                arr.SetElement(i, obj)
                i += 1

            self.med.Invoke('refreshMainContent', (arr, GfxValue(False)))
            self.dpsCallback = BigWorld.callback(1, self._refreshDpsContent)
            return

    def getDpsValue(self, en):
        if not en:
            return -1
        if en and hasattr(en, 'dmgTotal'):
            now = en.dmgEndTime if en.dmgEndTime else int(BigWorld.player().getServerTime())
            if en.dmgStartTime and now - en.dmgStartTime:
                return int(en.dmgTotal / (now - en.dmgStartTime))
            return en.dmgTotal
        return 0

    def _refreshDpsSkillListData(self, gbId, name):
        if self.statType == uiConst.STAT_TYPE_ONLY_DPS:
            statKey = FubenStats.K_DPS
            self.skillListData = {'tabName': STAT_DICT.get(statKey, '') + gameStrings.TEXT_FUBENSTATPROXY_732 + name}
            self.skillListData['skillData'] = []
            statDict = self.tempStatDict
            if not statDict:
                return
            totalStats = statDict.get(long(gbId))
            skillDetailData = []
            keyDict = SKILL_DETAIL_KYE_DICT
            spriteKeyDict = SPRITE_SKILL_DETAIL_KYE_DICT
            if totalStats:
                playerSkillDict = totalStats.getStats(keyDict.get(statKey))
                spriteSkillDict = totalStats.getStats(spriteKeyDict.get(statKey)).copy()
                skillDict = {}
                saveFirstKey = None
                for skill, value in spriteSkillDict.iteritems():
                    skillCategory = SGTD.data.get(skill, {}).get('skillCategory', '')
                    spriteKey = '1_%s' % skill
                    if skillCategory == const.SKILL_CATEGORY_SPRITE_AUTO:
                        if not saveFirstKey:
                            saveFirstKey = spriteKey
                        if saveFirstKey and saveFirstKey in skillDict.keys():
                            preVal = skillDict[saveFirstKey]
                            skillDict[saveFirstKey] = value + preVal
                        else:
                            skillDict[spriteKey] = value
                    else:
                        skillDict[spriteKey] = value

                skillDict.update(playerSkillDict)
                keys = skillDict.keys()
                keys.sort(cmp=lambda x, y: cmp(skillDict.get(y, 0), skillDict.get(x, 0)))
                rank = 0
                totalDamage = sum(skillDict.values())
                for skillId in keys:
                    isSprite = skillId not in playerSkillDict
                    realSkillId = int(skillId.split('_')[1]) if isSprite else skillId
                    name = SGTD.data.get(realSkillId, {}).get('name', '')
                    if isSprite:
                        name = gameStrings.SPRITE_FUBEN_STAT_NAME % name
                    if self.statKey == FubenStats.K_BEDAMAGE:
                        cntKey = FubenStats.K_SPRITE_SKILL_BEHIT_COUNT if isSprite else FubenStats.K_SKILL_BEHIT_COUNT
                        count = totalStats.getStats(cntKey).get(realSkillId, 0)
                    else:
                        cntKey = FubenStats.K_SPRITE_SKILL_HIT_COUNT if isSprite else FubenStats.K_SKILL_HIT_COUNT
                        count = totalStats.getStats(cntKey).get(realSkillId, 0)
                    damage = skillDict.get(skillId, 0)
                    rank += 1
                    if not totalDamage:
                        percent = 0
                    else:
                        percent = damage * 1.0 / totalDamage
                    skillDetailData.append({'rank': rank,
                     'skillName': name,
                     'count': count,
                     'percent': round(percent, 3),
                     'damage': self._formatValue(damage),
                     'percentStr': str(round(percent * 100.0, 1)) + '%'})

            self.skillListData['skillData'] = skillDetailData

    def _refreshSkillListData(self, gbId, name):
        if self.statKey in SKILL_LIST_STAT_KEYS:
            self.skillListData = {'tabName': STAT_DICT.get(self.statKey, '') + gameStrings.TEXT_FUBENSTATPROXY_732 + name}
            if self.selectBoss == BOSS_KEY_CURRENT:
                boss = self.currentStatBoss
            else:
                boss = self.selectBoss
            if boss == BOSS_KEY_TOTAL:
                statDict = self.fbStatDict
                keyDict = SKILL_DETAIL_KYE_DICT
                spriteKeyDict = SPRITE_SKILL_DETAIL_KYE_DICT
            else:
                statDict = self.bossStatDict.get(boss, None)
                keyDict = SKILL_BOSS_DETAIL_KYE_DICT
                spriteKeyDict = SPRITE_SKILL_BOSS_DETAIL_KYE_DICT
            if not statDict:
                return
            totalStats = statDict.get(long(gbId))
            skillDetailData = []
            if totalStats:
                playerSkillDict = totalStats.getStats(keyDict.get(self.statKey))
                spriteSkillDict = totalStats.getStats(spriteKeyDict.get(self.statKey)).copy()
                skillDict = {}
                saveFirstKey = None
                for skill, value in spriteSkillDict.iteritems():
                    skillCategory = SGTD.data.get(skill, {}).get('skillCategory', '')
                    spriteKey = '1_%s' % skill
                    if skillCategory == const.SKILL_CATEGORY_SPRITE_AUTO:
                        if not saveFirstKey:
                            saveFirstKey = spriteKey
                        if saveFirstKey and saveFirstKey in skillDict.keys():
                            preVal = skillDict[saveFirstKey]
                            skillDict[saveFirstKey] = value + preVal
                        else:
                            skillDict[spriteKey] = value
                    else:
                        skillDict[spriteKey] = value

                skillDict.update(playerSkillDict)
                keys = skillDict.keys()
                keys.sort(cmp=lambda x, y: cmp(skillDict.get(y, 0), skillDict.get(x, 0)))
                rank = 0
                totalDamage = sum(skillDict.values())
                for skillId in keys:
                    isSprite = skillId not in playerSkillDict
                    realSkillId = int(skillId.split('_')[1]) if isSprite else skillId
                    name = SGTD.data.get(realSkillId, {}).get('name', '')
                    if isSprite:
                        name = gameStrings.SPRITE_FUBEN_STAT_NAME % name
                    if self.statKey == FubenStats.K_BEDAMAGE:
                        cntKey = FubenStats.K_SPRITE_SKILL_BEHIT_COUNT if isSprite else FubenStats.K_SKILL_BEHIT_COUNT
                        count = totalStats.getStats(cntKey).get(realSkillId, 0)
                    else:
                        cntKey = FubenStats.K_SPRITE_SKILL_HIT_COUNT if isSprite else FubenStats.K_SKILL_HIT_COUNT
                        count = totalStats.getStats(cntKey).get(realSkillId, 0)
                    damage = skillDict.get(skillId, 0)
                    rank += 1
                    if not totalDamage:
                        percent = 0
                    else:
                        percent = damage * 1.0 / totalDamage
                    skillDetailData.append({'rank': rank,
                     'skillName': name,
                     'count': count,
                     'percent': round(percent, 3),
                     'damage': self._formatValue(damage),
                     'percentStr': str(round(percent * 100.0, 1)) + '%'})

            self.skillListData['skillData'] = skillDetailData

    def _getSkillDatasStr(self):
        if self.skillListData:
            skillMsg = self.skillListData.get('tabName')
            for item in self.skillListData.get('skillData', []):
                skillMsg += '\n%s %s %s %s %s' % (item.get('rank', 0),
                 item.get('skillName', ''),
                 item.get('count', ''),
                 self._formatValue(item.get('damage', '')),
                 str(item.get('percent', 0) * 100) + '%')

        return skillMsg

    def _getHateDatasStr(self):
        msg = gameStrings.TEXT_FUBENSTATPROXY_872 % MD.data.get(self.hateSelectBoss, {}).get('name', '')
        for item in self.hateListData:
            msg += '\n%s%s %s' % (item.get('rank'), item.get('name'), item.get('value'))

        return msg

    def _formatValue(self, value):
        if isinstance(value, int) or isinstance(value, long):
            if value > MAX_VALUE:
                return str(round(value * 1.0 / 10000, 2)) + gameStrings.TEXT_CBGMAINPROXY_273
        return str(value)
