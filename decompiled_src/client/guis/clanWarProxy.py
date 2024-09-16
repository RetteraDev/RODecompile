#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/clanWarProxy.o
from gamestrings import gameStrings
import BigWorld
import Scaleform
import copy
import gametypes
import gameglobal
import gameconfigCommon
import const
import formula
import sMath
import utils
from guis import ui
from guis import uiUtils, uiConst
from uiProxy import UIProxy
from callbackHelper import Functor
from ui import unicode2gbk
from guis import pinyinConvert
from data import clan_war_fort_data as CWFD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import clanwar_guild_kill_award_data as CGKAD
from data import bonus_data as BD
from data import item_data as ID
from data import region_server_config_data as RSCD
from data import cross_clan_war_config_data as CCWCD
REFRESH_DATA_CD = 5
MAX_RANK_NUM = 20
STOP_WAR_CD = 30
DECLARE_WAR_CD = SCD.data.get('declareWarInterval', 30)
GET_DECLARE_WAR_DATA_CD = 5
GUILD_SCORE_RANK = 11
PLAYER_KILL_TAB_IDX = 12
PLAYER_DAMAGE_TAB_IDX = 13
PLAYER_CURE_TAB_IDX = 14
GUILD_KILL_RANK = 15

class ClanWarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClanWarProxy, self).__init__(uiAdapter)
        self.modelMap = {'changeTab': self.onChangeTab,
         'clanWarStoneShield': self.onClanWarStoneShield,
         'clanWarTeleport': self.onClanWarTeleport,
         'clanWarZhancheInfo': self.onClanWarZhancheInfo,
         'teleportToFort': self.onTeleportToFort,
         'declareWar': self.onDeclareWar,
         'checkCanDeclareWar': self.onCheckCanDeclareWar,
         'wantStopWar': self.onWantStopWar,
         'showGuildList': self.onShowGuildList,
         'getGuildList': self.onGetGuildList,
         'processScore': self.onProcessScore,
         'getClanWarScoreTip': self.onGetClanWarScoreTip}
        self.keyDatas = {}
        self.reset()
        self.lastStopWarTimeStamp = 0
        self.lastDeclareWarTimeStamp = 0
        self.lastGetWarDataTimeStamp = 0
        self.currentTabIdx = 0
        self.isCrossClanWar = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLAN_WAR_RANK, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLAN_WAR_RESULT, self.hideResult)
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_LIST, self.hideGuildList)

    def reset(self):
        self.rankMediator = None
        self.guildMed = None
        self.resultMeditor = None
        self.currentProxyKey = None
        self.warListVer = -1
        self.declareWarList = []
        self.guildList = None
        self.currentTabIdx = 0
        self.rankJumpIndex = -1
        self.clanWarTgtHostId = utils.getHostId()

    def _registerMediator(self, widgetId, mediator):
        p = BigWorld.player()
        if widgetId == uiConst.WIDGET_CLAN_WAR_RANK:
            self.rankMediator = mediator
            jumpIndex = self.rankJumpIndex
            self.rankJumpIndex = -1
            return uiUtils.array2GfxAarry([BigWorld.player().guildNUID > 0, jumpIndex])
        elif widgetId == uiConst.WIDGET_CLAN_WAR_RESULT:
            self.resultMeditor = mediator
            fortGfxInfo = {}
            clanWar = BigWorld.player().clanWar if not self.isCrossClanWar else BigWorld.player().crossClanWar
            for fortId, fortVal in clanWar.fort.items():
                fortData = CWFD.data.get(fortId, '')
                if fortData and fortData.get('digongFort'):
                    continue
                guildIcon, color = uiUtils.getGuildFlag(fortVal.ownerGuildFlag)
                icon = uiUtils.getGuildIconPath(guildIcon)
                if uiUtils.isDownloadImage(guildIcon) and not p.isDownloadNOSFileCompleted(guildIcon):
                    if fortVal.fromHostId != utils.getHostId():
                        p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, guildIcon, fortVal.fromHostId, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                    else:
                        p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, guildIcon, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                fortGfxInfo[fortId] = {'name': fortData.get('showName', ''),
                 'ownerGuildName': fortVal.ownerGuildName if fortVal.ownerGuildName else gameStrings.TEXT_CLANWARPROXY_111,
                 'ownerGuildFlag': icon,
                 'color': color,
                 'ownerGuildNUID': str(fortVal.ownerGuildNUID),
                 'myGuildId': str(BigWorld.player().guildNUID)}

            BigWorld.player().cell.getClanWarResult()
            fortGfxInfo['isCrossClanWar'] = self.isCrossClanWar
            return uiUtils.dict2GfxDict(fortGfxInfo, True)
        else:
            if widgetId == uiConst.WIDGET_GUILD_LIST:
                self.guildMed = mediator
                BigWorld.player().cell.queryDeclareWarAllGuild()
            return None

    def onDownloadGuildIcon(self, *args):
        pass

    def clearWidget(self):
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CLAN_WAR_RANK)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_LIST)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CLAN_WAR_RESULT)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_CLAN_WAR_RANK:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CLAN_WAR_RANK)
            self.rankMediator = None
            self.currentProxyKey = None
            self.currentTabIdx = 0
            self.rankJumpIndex = -1
        elif widgetId == uiConst.WIDGET_CLAN_WAR_RESULT:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CLAN_WAR_RESULT)
            self.resultMeditor = None
        elif widgetId == uiConst.WIDGET_GUILD_LIST:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_LIST)
            self.guildMed = None

    def hideResult(self):
        self._asWidgetClose(uiConst.WIDGET_CLAN_WAR_RESULT, 0)

    def hideGuildList(self):
        self._asWidgetClose(uiConst.WIDGET_GUILD_LIST, 0)

    def showRankList(self, jumpIndex = -1, targetHostId = None):
        if not targetHostId:
            targetHostId = utils.getHostId()
        self.clanWarTgtHostId = targetHostId
        if self.rankMediator:
            if jumpIndex >= 0:
                self.rankMediator.Invoke('setTabIndex', Scaleform.GfxValue(jumpIndex))
        else:
            self.rankJumpIndex = jumpIndex
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CLAN_WAR_RANK)

    def showClanWarResult(self, isCrossClanWar = False):
        self.isCrossClanWar = isCrossClanWar
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CLAN_WAR_RESULT)

    def onChangeTab(self, *args):
        tabIndex = args[3][0].GetNumber()
        if tabIndex in (GUILD_KILL_RANK, GUILD_SCORE_RANK):
            self.currentTabIdx = tabIndex
            self.getClanWarGuildRank()
        elif tabIndex in (12, 13, 14):
            self.currentTabIdx = tabIndex
            self.getClanWarPlayerRank()
        elif tabIndex == 2:
            self.currentTabIdx = tabIndex
            self.getClanWarPlayerInfo()
        elif tabIndex == 0:
            self.currentTabIdx = tabIndex
            self.refreshFortInfo()
        elif tabIndex == 3:
            self.currentTabIdx = tabIndex
            self.setDeclareWarList(self.warListVer, [], False)
            self.refreshDeclareWar()

    def onProcessScore(self, *args):
        score = int(float(args[3][0].GetString()))
        score = self.uiAdapter.crossClanWarRank.processScore(score)
        return Scaleform.GfxValue(ui.gbk2unicode(score))

    def onGetClanWarScoreTip(self, *args):
        totalScore = long(args[3][0].GetNumber())
        killScore = long(args[3][1].GetNumber())
        tips = CCWCD.data.get('crossClanWarScoreTips', 'crossClanWarScoreTips') % (killScore, totalScore - killScore)
        return Scaleform.GfxValue(ui.gbk2unicode(tips))

    def onClanWarStoneShield(self, *args):
        if self._checkInClanWar():
            p = BigWorld.player()
            if not p.guild:
                p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
                return
            now = p.getServerTime()
            guildSkill = p.guild.skills.get(gametypes.GUILD_SKILL_STONE_SHIELD)
            nextTime = guildSkill and guildSkill.nextTime or 0
            if nextTime < now:
                nextTime = 0
            msg = uiUtils.getTextFromGMD(GMDD.data.USE_ZULONG_CONFIRM, '%s, %s')
            if not nextTime:
                msg = msg % (guildSkill.duration, gameStrings.TEXT_CLANWARPROXY_214)
            else:
                msg = msg % (guildSkill.duration, gameStrings.TEXT_CLANWARPROXY_216 % utils.formatTime(nextTime - now))
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self._confirmClanWarStoneShield, yesBtnText=gameStrings.TEXT_CLANWARPROXY_217)

    def _confirmClanWarStoneShield(self):
        BigWorld.player().cell.clanWarStoneShield()

    def onClanWarTeleport(self, *args):
        if self._checkInClanWar():
            p = BigWorld.player()
            if not p.guild:
                p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
                return
            nfort = len([ k for k, v in self.getClanWar().fort.iteritems() if p.guildNUID and p.guildNUID == v.ownerGuildNUID ])
            if not nfort:
                p.showGameMsg(GMDD.data.CLAN_WAR_TELEPORT_NO_STONE, ())
                return
            if nfort > 1:
                self._confirmClanWarTeleport()
                return
            now = p.getServerTime()
            guildSkill = p.guildSkills.get(gametypes.GUILD_SKILL_TELEPORT)
            nextTime = guildSkill and guildSkill.nextTime or 0
            if nextTime < now:
                nextTime = 0
            msg = gameStrings.TEXT_CLANWARPROXY_240
            if not nextTime:
                msg = msg % gameStrings.TEXT_CLANWARPROXY_214
            else:
                msg = msg % (gameStrings.TEXT_CLANWARPROXY_216 % utils.formatTime(nextTime - now))
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self._confirmClanWarTeleport, yesBtnText=gameStrings.TEXT_CLANWARPROXY_217)

    def _confirmClanWarTeleport(self):
        BigWorld.player().cell.clanWarTeleport()

    def onTeleportToFort(self, *args):
        fortId = args[3][0].GetNumber()
        fortName = unicode2gbk(args[3][1].GetString())
        p = BigWorld.player()
        now = p.getServerTime()
        guildSkill = p.guildSkills.get(gametypes.GUILD_SKILL_TELEPORT)
        nextTime = guildSkill and guildSkill.nextTime or 0
        if nextTime < now:
            nextTime = 0
        msg = gameStrings.TEXT_CLANWARPROXY_261
        if not nextTime:
            msg = msg % (fortName, gameStrings.TEXT_CLANWARPROXY_214)
        else:
            msg = msg % (fortName, gameStrings.TEXT_CLANWARPROXY_216 % utils.formatTime(nextTime - now))
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda fortId = fortId: self._confirmClanWarTeleportToFort(fortId), yesBtnText=gameStrings.TEXT_CLANWARPROXY_217)

    def _confirmClanWarTeleportToFort(self, fortId):
        self._teleportToFort(fortId)

    def onDeclareWar(self, *args):
        nuid = args[3][0].GetString()
        if nuid:
            BigWorld.player().cell.declareWar(long(nuid))
            self.hideGuildList()

    def onClanWarZhancheInfo(self, *args):
        gameglobal.rds.ui.zhancheInfo.show()

    def onCheckCanDeclareWar(self, *args):
        result = {'canDeclare': gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_DECLARE_WAR),
         'stopWarCD': self.lastStopWarTimeStamp + STOP_WAR_CD - BigWorld.player().getServerTime(),
         'declareWarCD': self.lastDeclareWarTimeStamp + DECLARE_WAR_CD - BigWorld.player().getServerTime(),
         'effectBase': SCD.data.get('declareWarEffectBase', const.DECLARE_WAR_EFFECT_BASE),
         'effectSegment': SCD.data.get('declareWarEffectSegment', const.DECLARE_WAR_EFFECT_SEGMENT),
         'guildName': BigWorld.player().guildName}
        return uiUtils.dict2GfxDict(result, True)

    def onShowGuildList(self, *args):
        if self._checkInClanWar():
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_LIST)

    def onGetGuildList(self, *args):
        name = unicode2gbk(args[3][0].GetString())
        if not self.guildList:
            return uiUtils.array2GfxAarry([], True)
        if not name:
            return uiUtils.array2GfxAarry(self.guildList, True)
        ret = []
        name = name.lower()
        isPinyinAndHanzi = utils.isPinyinAndHanzi(name)
        if isPinyinAndHanzi == const.STR_HANZI_PINYIN:
            return uiUtils.array2GfxAarry(ret, True)
        for guild in self.guildList:
            itemName = guild[1]
            if isPinyinAndHanzi == const.STR_ONLY_PINYIN:
                pinyin = pinyinConvert.strPinyinFirst(itemName)
                isFind = pinyin.find(name) != -1
            else:
                isFind = itemName.find(name) != -1
            if isFind:
                ret.append(guild)

        return uiUtils.array2GfxAarry(ret, True)

    def _checkInClanWar(self):
        if not BigWorld.player().clanWarStatus:
            BigWorld.player().showGameMsg(GMDD.data.DECLARE_WAR_NOT_IN_CLAN_WAR, ())
            return False
        return True

    def onWantStopWar(self, *args):
        guildNuid = args[3][0].GetString()
        tip = gameStrings.TEXT_CLANWARPROXY_328
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(tip, Functor(self.applyStopWar, guildNuid))

    def applyStopWar(self, guildNuid):
        BigWorld.player().cell.cancelDeclareWar(long(guildNuid))

    def _teleportToFort(self, fortId):
        BigWorld.player().cell.clanWarTeleportToSelectedStone(fortId)

    def getClanWarGuildRank(self):
        self.currentProxyKey = const.PROXY_KEY_TOP_CLANWAR_GUILD
        if self.keyDatas.has_key(self.currentProxyKey):
            self.setClanWarGuildRank(self.keyDatas[self.currentProxyKey][0], False)
        if self.currentTabIdx == GUILD_SCORE_RANK:
            BigWorld.player().cell.getClanWarGuildRecordScoreRank()
        else:
            BigWorld.player().cell.getClanWarGuildRank()

    def setClanWarGuildRank(self, rankData, cacheData = True):
        if cacheData:
            self.keyDatas[const.PROXY_KEY_TOP_CLANWAR_GUILD] = (rankData, BigWorld.player().getServerTime())
        if self.currentProxyKey == const.PROXY_KEY_TOP_CLANWAR_GUILD and self.rankMediator:
            enableClanWarZaijuReward = gameglobal.rds.configData.get('enableClanWarTopGuildMemberAward', False)
            p = BigWorld.player()
            if self.currentTabIdx == GUILD_SCORE_RANK:
                rankData = getattr(p, 'crossClanWarRecordRank', [])
                rankData.sort(cmp=lambda x, y: cmp((y[2], y[4]), (x[2], x[4])))
                rankData = self._addRankToList(rankData, const.TOP_CLAN_NUM)
            elif self.currentTabIdx == GUILD_KILL_RANK:
                rankData = getattr(p, 'clanWarGuildRank', [])
                rankData.sort(cmp=lambda x, y: cmp(y[5], x[5]))
                rankData = self._addRankToList(rankData, const.TOP_CLAN_NUM)
            if len(rankData) > const.TOP_CLAN_NUM:
                gfxData = {'allRank': rankData[0:const.TOP_CLAN_NUM],
                 'selfRank': rankData[const.TOP_CLAN_NUM],
                 'myClanRankNum': gameStrings.TEXT_CLANWARPROXY_367,
                 'enableClanWarZaijuReward': enableClanWarZaijuReward}
            else:
                gfxData = {'allRank': rankData,
                 'myClanRankNum': gameStrings.TEXT_CLANWARPROXY_367,
                 'enableClanWarZaijuReward': enableClanWarZaijuReward}
                myGuildName = BigWorld.player().guildName
                if myGuildName:
                    for index, item in enumerate(rankData):
                        if item and myGuildName == item[0]:
                            gfxData['selfRank'] = item
                            gfxData['myClanRankNum'] = str(index + 1)
                            break

            self.rankMediator.Invoke('setClanWarGuildRank', uiUtils.dict2GfxDict(gfxData, True))

    def getClanWarPlayerRank(self):
        self.currentProxyKey = const.PROXY_KEY_TOP_CLANWAR_PLAYER
        if self.keyDatas.has_key(self.currentProxyKey):
            self.setClanWarPlayerRank(self.keyDatas[self.currentProxyKey][0], False)
        if not self.checkDataOutCd(self.currentProxyKey):
            return
        BigWorld.player().cell.getClanWarPlayerRank()

    def setClanWarPlayerRank(self, rankData, cacheData = True):
        if cacheData:
            self.keyDatas[const.PROXY_KEY_TOP_CLANWAR_PLAYER] = (rankData, BigWorld.player().getServerTime())
        if self.currentProxyKey == const.PROXY_KEY_TOP_CLANWAR_PLAYER and self.rankMediator:
            rankData = rankData.get(self.currentTabIdx + 1 - PLAYER_KILL_TAB_IDX)
            if self.currentTabIdx == PLAYER_KILL_TAB_IDX:
                rankData.sort(cmp=lambda x, y: cmp(y[1], x[1]))
            elif self.currentTabIdx == PLAYER_DAMAGE_TAB_IDX:
                rankData.sort(cmp=lambda x, y: cmp(y[3], x[3]))
            elif self.currentTabIdx == PLAYER_CURE_TAB_IDX:
                rankData.sort(cmp=lambda x, y: cmp(y[4], x[4]))
            rankData = self._addRankToList(rankData, const.TOP_CLAN_MEMBER_NUM)
            if len(rankData) > const.TOP_CLAN_MEMBER_NUM:
                gfxData = {'allRank': rankData[0:const.TOP_CLAN_MEMBER_NUM]}
            else:
                gfxData = {'allRank': rankData}
            myRoleName = BigWorld.player().realRoleName
            for item in rankData:
                if myRoleName == item[0]:
                    gfxData['selfRank'] = item
                    break

            self.rankMediator.Invoke('setClanWarPlayerRank', uiUtils.dict2GfxDict(gfxData, True))

    def getClanWarPlayerInfo(self):
        self.currentProxyKey = const.PROXY_KEY_CLANWAR_PLAYER_INFO
        if self.keyDatas.has_key(self.currentProxyKey):
            self.setClanWarPlayerInfo(self.keyDatas[self.currentProxyKey][0], False)
        if not self.checkDataOutCd(self.currentProxyKey):
            return
        playerInfo = {'allRank': [],
         'myClanRankNum': gameStrings.TEXT_CLANWARPROXY_421,
         'myInWorldRankNum': gameStrings.TEXT_CLANWARPROXY_421,
         'fort': ''}
        dis = 0
        fortId = 0
        for key, item in CWFD.data.items():
            if item.get('digongFort'):
                continue
            tmpDis = sMath.distance3D(BigWorld.player().position, item.get('fortIconPos', (0, 0, 0)))
            if not dis or dis > tmpDis:
                fortId = key
                dis = tmpDis

        if fortId:
            playerInfo['fort'] = CWFD.data.get(fortId, {}).get('showName', '')
            playerInfo['icon'] = uiConst.FORT_ICON_64 + '%s.dds' % fortId
        playerInfo['guildName'] = BigWorld.player().guildName
        playerInfo['clanName'] = BigWorld.player().clanName
        playerInfo['ownBuilding'] = ''
        playerInfo['ownFort'] = ''
        playerInfo['totalKill'] = ''
        playerInfo['awarText'] = ''
        playerInfo['zhancheNumber'] = ''
        self.rankMediator.Invoke('setClanWarPlayerInfo', uiUtils.dict2GfxDict(playerInfo, True))
        BigWorld.player().cell.getClanWarPlayerInfo(self.clanWarTgtHostId)
        BigWorld.player().cell.getGuildZaijuUsedList(0)

    def setClanWarPlayerInfo(self, rankList, cacheData = True):
        p = BigWorld.player()
        if cacheData:
            self.keyDatas[const.PROXY_KEY_CLANWAR_PLAYER_INFO] = (rankList, BigWorld.player().getServerTime())
        if self.currentProxyKey == const.PROXY_KEY_CLANWAR_PLAYER_INFO and self.rankMediator:
            rankList[1].sort(cmp=lambda x, y: cmp(y[6], x[6]))
            playerInfo = {'allRank': [],
             'myClanRankNum': str(rankList[0][0]) if rankList[0][0] else gameStrings.TEXT_CLANWARPROXY_421,
             'myInWorldRankNum': str(rankList[0][1]) if rankList[0][1] else gameStrings.TEXT_CLANWARPROXY_421,
             'fort': '',
             'awarText': ''}
            dis = 0
            fortId = 0
            for key, item in CWFD.data.items():
                if item.get('digongFort'):
                    continue
                tmpDis = sMath.distance3D(p.position, item.get('fortIconPos', (0, 0, 0)))
                if not dis or dis > tmpDis:
                    fortId = key
                    dis = tmpDis

            if fortId:
                playerInfo['fort'] = CWFD.data.get(fortId, {}).get('showName', '')
                playerInfo['icon'] = uiConst.FORT_ICON_64 + '%s.dds' % fortId
            if p.guildNUID > 0:
                playerInfo['guildName'] = p.guildName
                playerInfo['myRankInGuild'] = gameStrings.TEXT_CLANWARPROXY_421
                icon, color = self.getGuildPathAndClolor(p.guildFlag)
                playerInfo['guildIcon'] = icon
                playerInfo['color'] = color
                totalKillNum = 0
                players = []
                for index, item in enumerate(rankList[1]):
                    if item[0] == BigWorld.player().roleName:
                        playerInfo['playerData'] = item
                        playerInfo['myRankInGuild'] = index + 1
                    totalKillNum += item[2]
                    tmpItem = list(item) + [index + 1]
                    tmpItem[1] = gametypes.GUILD_ROLE_DICT.get(item[1], '')
                    tmpItem[7] = formula.whatSchoolName(item[7])
                    players.append(tmpItem)

                playerInfo['allRank'] = players
                playerInfo['totalKill'] = totalKillNum
                playerInfo['clanName'] = p.clanName
                zhanchenNum = gameglobal.rds.ui.zhancheInfo.getzhancheNumber()
                playerInfo['zhancheNumber'] = '%d / %d' % (zhanchenNum[0], zhanchenNum[1])
                killNum, itemName = self._getAwardItemByKillNum(totalKillNum)
                if itemName:
                    playerInfo['awarText'] = gameStrings.TEXT_CLANWARPROXY_496 % (killNum, itemName)
            ownFort = []
            ownBuilding = []
            fort = BigWorld.player().clanWar.fort
            for fortId, fortVal in fort.items():
                if fortVal.ownerGuildNUID == p.guildNUID:
                    fortData = CWFD.data.get(fortId, '')
                    if fortData and fortData.get('digongFort'):
                        continue
                    if fortData:
                        if fortData.get('parentId'):
                            ownBuilding.append(fortData.get('showName'))
                        else:
                            ownFort.append(fortData.get('showName'))

            playerInfo['ownBuilding'] = ','.join(ownBuilding) if len(ownBuilding) else gameStrings.TEXT_BATTLEFIELDPROXY_1605
            playerInfo['ownFort'] = ','.join(ownFort) if len(ownFort) else gameStrings.TEXT_BATTLEFIELDPROXY_1605
            self.rankMediator.Invoke('setClanWarPlayerInfo', uiUtils.dict2GfxDict(playerInfo, True))

    def updateZhancheNum(self, useNumber, totalNumber):
        if self.currentProxyKey == const.PROXY_KEY_CLANWAR_PLAYER_INFO:
            zhanchenNum = '%d / %d' % (useNumber, totalNumber)
            self.rankMediator.Invoke('refreshzhancheNumber', Scaleform.GfxValue(zhanchenNum))

    def _getAwardItemByKillNum(self, killNum):
        awardKeys = copy.deepcopy(CGKAD.data.keys())
        awardKeys.sort()
        awardKey = awardKeys[-1]
        itemName = ''
        for key in awardKeys:
            if key > killNum:
                awardKey = key
                break

        bonusId = CGKAD.data.get(awardKey, {}).get('bonusId', 0)
        if bonusId:
            fixedBonus = BD.data[bonusId].get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            if fixedBonus:
                itemId = fixedBonus[0][1]
            else:
                itemId = 0
            if itemId:
                itemName = ID.data.get(itemId, {}).get('name', '')
        return (awardKey, itemName)

    def refreshFortInfo(self):
        if not self.rankMediator:
            return None
        else:
            p = BigWorld.player()
            fort = p.clanWar.fort
            fortGfxInfo = {}
            for fortId, fortVal in fort.items():
                fortData = CWFD.data.get(fortId, '')
                if not fortData or fortData.get('digongFort'):
                    continue
                if not fortData.get('parentId'):
                    data = fortGfxInfo.get(fortId)
                    if fortVal.ownerGuildName:
                        guildIcon, color = uiUtils.getGuildFlag(fortVal.ownerGuildFlag)
                        icon, color = self.getGuildPathAndClolor(fortVal.ownerGuildFlag)
                        if uiUtils.isDownloadImage(guildIcon) and not p.isDownloadNOSFileCompleted(guildIcon):
                            if fortVal.fromHostId != utils.getHostId():
                                p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, guildIcon, fortVal.fromHostId, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                            else:
                                p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, guildIcon, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                    else:
                        icon = uiConst.FORT_ICON_64 + '%s.dds' % fortId
                        color = 0
                    if not data:
                        fortGfxInfo[fortId] = {'name': fortData.get('showName', ''),
                         'ownerGuildName': fortVal.ownerGuildName if fortVal.ownerGuildName else gameStrings.TEXT_CLANWARPROXY_111,
                         'buildings': [],
                         'icon': icon,
                         'color': color}
                    else:
                        data['name'] = fortData.get('showName', '')
                        data['ownerGuildName'] = fortVal.ownerGuildName if fortVal.ownerGuildName else gameStrings.TEXT_CLANWARPROXY_111
                        data['icon'] = icon
                        data['color'] = color
                else:
                    parentId = fortData.get('parentId')
                    data = fortGfxInfo.get(parentId)
                    if not data:
                        data = {'buildings': []}
                        fortGfxInfo[parentId] = data
                    if fortVal.ownerGuildName:
                        guildIcon, color = uiUtils.getGuildFlag(fortVal.ownerGuildFlag)
                        icon, color = self.getGuildPathAndClolor(fortVal.ownerGuildFlag)
                        if uiUtils.isDownloadImage(guildIcon) and not p.isDownloadNOSFileCompleted(guildIcon):
                            if fortVal.fromHostId != utils.getHostId():
                                p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, guildIcon, fortVal.fromHostId, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                            else:
                                p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, guildIcon, gametypes.NOS_FILE_PICTURE, self.onDownloadGuildIcon, (None,))
                    else:
                        icon = uiConst.FORT_ICON_32 + '%s.dds' % fortId
                        color = 0
                    data['buildings'].append({'name': fortData.get('showName', ''),
                     'ownerGuildName': fortVal.ownerGuildName if fortVal.ownerGuildName else gameStrings.TEXT_CLANWARPROXY_111,
                     'icon': icon,
                     'color': color})

            self.rankMediator.Invoke('setFortInfo', uiUtils.array2GfxAarry(fortGfxInfo.values(), True))
            return None

    def setDeclareWarList(self, ver, warList, cacheData = True):
        if cacheData:
            self.warListVer = ver
            self.declareWarList = warList
        if self.rankMediator:
            obj = {'warList': warList,
             'stopWarCD': self.lastStopWarTimeStamp + STOP_WAR_CD - BigWorld.player().getServerTime(),
             'declareWarCD': self.lastDeclareWarTimeStamp + DECLARE_WAR_CD - BigWorld.player().getServerTime()}
            self.rankMediator.Invoke('setWarList', uiUtils.dict2GfxDict(obj, True))

    def setClanAllGuildList(self, guildList):
        if self.guildMed:
            guilds = []
            for guild in guildList:
                if guild[0] != BigWorld.player().guildNUID:
                    guilds.append(guild)

            self.guildList = guilds
            self.guildMed.Invoke('setGuildList', uiUtils.array2GfxAarry(guilds, True))

    def checkDataOutCd(self, proxyKey):
        if self.keyDatas and self.keyDatas.has_key(proxyKey) and BigWorld.player().getServerTime() - self.keyDatas[proxyKey][1] <= REFRESH_DATA_CD:
            return False
        return True

    def clanWarEnd(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CLAN_WAR_RESULT)

    def onResultPushClick(self):
        self.showClanWarResult()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_CLAN_WAR_RESULT)

    def setClanWorResult(self, result):
        if self.resultMeditor:
            resultGfxDict = {'kill': result[0],
             'damage': result[1],
             'cure': result[2],
             'guildKill': result[3],
             'guildRank': result[4] if result[4] else gameStrings.TEXT_CLANWARPROXY_421}
            self.resultMeditor.Invoke('setWarData', uiUtils.dict2GfxDict(resultGfxDict, True))

    def _addRankToList(self, rankList, maxCnt):

        def mapFun(rankData, index, maxCnt):
            if index <= maxCnt:
                return list(rankData) + [index]
            else:
                return list(rankData) + [gameStrings.TEXT_CLANWARPROXY_421]

        result = map(mapFun, rankList, [ x + 1 for x in xrange(len(rankList)) ], [maxCnt] * len(rankList))
        for info in result:
            if self.currentTabIdx == GUILD_KILL_RANK:
                info[5] = RSCD.data.get(info[6], {}).get('serverName', '')
            else:
                info[5] = RSCD.data.get(info[5], {}).get('serverName', '')

        return result

    def getGuildPathAndClolor(self, flag):
        icon, color = uiUtils.getGuildFlag(flag)
        return (uiUtils.getGuildIconPath(icon), color)

    def getClanWar(self):
        p = BigWorld.player()
        return p.clanWar

    def showSelectStoneToTeleport(self):
        p = BigWorld.player()
        forts = []
        for fortId, fort in self.getClanWar().fort.items():
            if fort.ownerGuildNUID == p.guildNUID:
                fortName = CWFD.data.get(fortId, {}).get('showName', '')
                forts.append((fortName, fortId))

        if forts and self.rankMediator:
            self.rankMediator.Invoke('showTeleportStone', uiUtils.array2GfxAarry(forts, True))

    def refreshDeclareWar(self, force = False):
        if self.rankMediator:
            if force or self.lastGetWarDataTimeStamp + GET_DECLARE_WAR_DATA_CD <= BigWorld.player().getServerTime():
                self.lastGetWarDataTimeStamp = BigWorld.player().getServerTime()
                BigWorld.player().cell.queryDeclareWar(-1)
            else:
                self.setDeclareWarList(self.warListVer, self.declareWarList)

    def declareToSucc(self, guildNUID, guildName):
        self.lastDeclareWarTimeStamp = BigWorld.player().getServerTime()
        self.refreshDeclareWar(True)

    def onCancelDeclareWar(self, guildNUID, guildName):
        self.lastStopWarTimeStamp = BigWorld.player().getServerTime()
        guilds = [ guild for guild in self.declareWarList if guild[0] != guildNUID ]
        self.setDeclareWarList(self.warListVer, guilds)
