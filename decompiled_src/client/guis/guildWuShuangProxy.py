#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildWuShuangProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiUtils
import uiConst
import const
import gametypes
import skillDataInfo
import commGuild
from uiProxy import UIProxy
from callbackHelper import Functor
from data import guild_config_data as GCD
from data import skill_general_template_data as SGTD
from data import ws_daoheng_data as WDD
from cdata import ws_skill_lvup_data as WSLD
from cdata import game_msg_def_data as GMDD

class GuildWuShuangProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildWuShuangProxy, self).__init__(uiAdapter)
        self.modelMap = {'getTabInfo': self.onGetTabInfo,
         'getXinDeInfo': self.onGetXinDeInfo,
         'getDaoHengInfo': self.onGetDaoHengInfo,
         'select': self.onSelect,
         'start': self.onStart}
        self.mediator = None
        self.tabIdx = 0
        self.idxMap = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_WUSHUANG, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_WUSHUANG:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_WUSHUANG)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.idxMap = {}
        if gameglobal.rds.ui.guildWuShuangSelect.mediator:
            gameglobal.rds.ui.guildWuShuangSelect.hide()

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_WUSHUANG)

    def onGetTabInfo(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableGuildWSDaoheng', False))

    def onGetXinDeInfo(self, *arg):
        self.tabIdx = uiConst.GUILD_WUSHUANG_XINDE
        self.refreshXinDeInfo()

    def onGetDaoHengInfo(self, *arg):
        self.tabIdx = uiConst.GUILD_WUSHUNAG_DAOHENG
        self.refreshDaoHengInfo()

    def refreshXinDeInfo(self):
        if self.tabIdx != uiConst.GUILD_WUSHUANG_XINDE:
            return
        else:
            if self.mediator:
                p = BigWorld.player()
                guild = p.guild
                if not guild:
                    return
                markerId = commGuild.getMarkerIdByBuildingId(guild, gametypes.GUILD_BUILDING_GROWTH_ID)
                marker = guild.marker.get(markerId)
                buildValue = guild.building.get(marker.buildingNUID)
                buildLv = buildValue.level if buildValue else 0
                info = {}
                info['openNum'] = GCD.data.get('wsGuildPracticeOpenNum', const.GUILD_WS_PRACTICE_OPEN_NUM)
                if self.tabIdx not in self.idxMap:
                    self.idxMap[self.tabIdx] = {}
                skillMap = self.idxMap[self.tabIdx]
                skillList = []
                wsPracticeNum = GCD.data.get('wsPracticeNum', const.GUILD_WS_PRACTICE_NUM)
                wsPracticeContrib = GCD.data.get('wsPracticeContrib', const.GUILD_WS_PRACTICE_CONTRIB)
                for i in xrange(const.GUILD_WS_PRACTICE_MAX_NUM):
                    itemInfo = {}
                    if i >= len(p.guildWSPractice):
                        wsVal = None
                    else:
                        wsVal = p.guildWSPractice[i]
                    if wsPracticeNum[i] <= buildLv:
                        itemInfo['state'] = 'canUse'
                        skillId = skillMap[i] if i in skillMap else 0
                        if wsVal and wsVal.skillId != 0:
                            skillId = wsVal.skillId
                        if skillId != 0:
                            itemInfo['state'] = 'normal'
                            sd = skillDataInfo.ClientSkillInfo(skillId)
                            icon = sd.getSkillData('icon', None)
                            skInfoVal = p.wsSkills.get(skillId, None)
                            lv = skInfoVal.level if skInfoVal else 1
                            skillInfo = p.getSkillInfo(skillId, lv)
                            itemInfo['slotData'] = {'iconPath': 'skill/icon64/' + str(icon) + '.dds'}
                            itemInfo['skillId'] = skillId
                            itemInfo['skillName'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_109
                            itemInfo['valueAmount'] = '%d/%d' % (lv, gametypes.WUSHUANG_LV_MAX)
                            itemInfo['detailTitle'] = skillInfo.getSkillData('name', '')
                            itemInfo['detailType'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_113
                            lvUpData = WSLD.data.get((skillId, lv), {})
                            exp = 0
                            for val in skInfoVal.proficiency.values():
                                exp += val

                            needExp = lvUpData.get('maxXd', 0)
                            itemInfo['expText'] = '%s/%s' % (format(exp, '.2f') if int(exp) != exp else str(int(exp)), str(needExp))
                            currentValue = 100.0
                            if exp <= needExp and needExp != 0:
                                currentValue = currentValue * exp / needExp
                            itemInfo['currentValue'] = currentValue
                            detailDesc = gameStrings.TEXT_GUILDWUSHUANGPROXY_127 % uiUtils.formatTime(const.GUILD_WS_PRACTICE_DURATION)
                            detailDesc += gameStrings.TEXT_GUILDWUSHUANGPROXY_128 % uiUtils.formatTime(skillInfo.getSkillData('wsPracticeInterval', const.GUILD_WS_PRACTICE_INTERVAL))
                            detailDesc += gameStrings.TEXT_GUILDWUSHUANGPROXY_129 % lvUpData.get('useAddXd', 0)
                            itemInfo['detailDesc'] = detailDesc
                            itemInfo['isBusy'] = wsVal.isBusy() if wsVal else False
                            if itemInfo['isBusy']:
                                itemInfo['contrib'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_134 % uiUtils.formatTime(wsVal.duration - wsVal.tCost)
                            else:
                                itemInfo['contrib'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_136 % wsPracticeContrib[i]
                        else:
                            itemInfo['state'] = 'canUse'
                            itemInfo['skillName'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_139
                            itemInfo['detailTitle'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_140
                            itemInfo['contrib'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_136 % wsPracticeContrib[i]
                    else:
                        itemInfo['state'] = 'useless'
                        itemInfo['detailTitle'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_144 % wsPracticeNum[i]
                    skillList.append(itemInfo)

                info['skillList'] = skillList
                self.mediator.Invoke('refreshXinDeInfo', uiUtils.dict2GfxDict(info, True))
            return

    def refreshDaoHengInfo(self):
        if self.tabIdx != uiConst.GUILD_WUSHUNAG_DAOHENG:
            return
        else:
            if self.mediator:
                p = BigWorld.player()
                guild = p.guild
                if not guild:
                    return
                markerId = commGuild.getMarkerIdByBuildingId(guild, gametypes.GUILD_BUILDING_GROWTH_ID)
                marker = guild.marker.get(markerId)
                buildValue = guild.building.get(marker.buildingNUID)
                buildLv = buildValue.level if buildValue else 0
                info = {}
                info['openNum'] = const.GUILD_WS_DAOHENG_OPEN_NUM
                if self.tabIdx not in self.idxMap:
                    self.idxMap[self.tabIdx] = {}
                skillMap = self.idxMap[self.tabIdx]
                skillList = []
                wsDaohengNum = GCD.data.get('wsDaohengNum', const.GUILD_WS_DAOHENG_NUM)
                wsDaohengContrib = GCD.data.get('wsDaohengContrib', const.GUILD_WS_DAOHENG_CONTRIB)
                for i in xrange(const.GUILD_WS_DAOHENG_MAX_NUM):
                    itemInfo = {}
                    if i >= len(p.guildWSDaoheng):
                        wsVal = None
                    else:
                        wsVal = p.guildWSDaoheng[i]
                    if wsDaohengNum[i] <= buildLv:
                        itemInfo['state'] = 'canUse'
                        skillId = skillMap[i] if i in skillMap else 0
                        if wsVal and wsVal.skillId != 0:
                            skillId = wsVal.skillId
                        if skillId != 0:
                            itemInfo['state'] = 'normal'
                            sd = skillDataInfo.ClientSkillInfo(skillId)
                            icon = sd.getSkillData('icon', None)
                            skInfoVal = p.wsSkills.get(skillId, None)
                            lv = skInfoVal.level if skInfoVal else 1
                            skillInfo = p.getSkillInfo(skillId, lv)
                            itemInfo['slotData'] = {'iconPath': 'skill/icon64/' + str(icon) + '.dds'}
                            itemInfo['skillId'] = skillId
                            itemInfo['skillName'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_109
                            itemInfo['valueAmount'] = '%d/%d' % (lv, gametypes.WUSHUANG_LV_MAX)
                            itemInfo['detailTitle'] = skillInfo.getSkillData('name', '')
                            itemInfo['detailType'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_198
                            slotNum = len(skInfoVal.slots) if skInfoVal.slots else 0
                            daoHengData = WDD.data.get((skillId, slotNum + 1), {})
                            addVal, maxVal = daoHengData.get('daohengGuild', const.GUILD_WS_DAOHENG_ADD_DEFAULT)
                            daoHengInfo = gameglobal.rds.ui.skill._genDirectionInfo(skillId)
                            exp = daoHengInfo['value']
                            needExp = daoHengInfo['maxValue']
                            itemInfo['expText'] = '%s/%s' % (format(exp, '.2f') if int(exp) != exp else str(int(exp)), str(needExp))
                            currentValue = 100.0
                            if exp <= needExp and needExp != 0:
                                currentValue = currentValue * exp / needExp
                            itemInfo['currentValue'] = currentValue
                            if slotNum >= len(daoHengInfo['daohang']):
                                itemInfo['expText'] = '0/0'
                                itemInfo['currentValue'] = 100.0
                                detailDesc = uiUtils.getTextFromGMD(GMDD.data.GUILD_WS_DAOHENG_FULL)
                            elif daoHengInfo['daohang'][slotNum][0] == uiConst.DAOHENG_LOCK:
                                detailDesc = uiUtils.getTextFromGMD(GMDD.data.GUILD_WS_DAOHENG_JINJIE_LIMIT, '%s') % daoHengInfo['daohang'][slotNum][1]
                            else:
                                detailDesc = gameStrings.TEXT_GUILDWUSHUANGPROXY_127 % uiUtils.formatTime(const.GUILD_WS_DAOHENG_DURATION)
                                detailDesc += gameStrings.TEXT_GUILDWUSHUANGPROXY_128 % uiUtils.formatTime(skillInfo.getSkillData('wsDaohengInterval', const.GUILD_WS_DAOHENG_INTERVAL))
                                detailDesc += gameStrings.TEXT_GUILDWUSHUANGPROXY_223 % addVal
                                detailDesc += gameStrings.TEXT_GUILDWUSHUANGPROXY_224 % (getattr(skInfoVal, 'daoHeng', {}).get('guild', 0), maxVal)
                            itemInfo['detailDesc'] = detailDesc
                            itemInfo['isBusy'] = wsVal.isBusy() if wsVal else False
                            if itemInfo['isBusy']:
                                itemInfo['contrib'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_134 % uiUtils.formatTime(wsVal.duration - wsVal.tCost)
                            else:
                                itemInfo['contrib'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_136 % wsDaohengContrib[i]
                        else:
                            itemInfo['state'] = 'canUse'
                            itemInfo['skillName'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_139
                            itemInfo['detailTitle'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_140
                            itemInfo['contrib'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_136 % wsDaohengContrib[i]
                    else:
                        itemInfo['state'] = 'useless'
                        itemInfo['detailTitle'] = gameStrings.TEXT_GUILDWUSHUANGPROXY_144 % wsDaohengNum[i]
                    skillList.append(itemInfo)

                info['skillList'] = skillList
                self.mediator.Invoke('refreshDaoHengInfo', uiUtils.dict2GfxDict(info, True))
            return

    def selectSkill(self, tabIdx, idx, skillId):
        if tabIdx not in self.idxMap:
            self.idxMap[tabIdx] = {}
        skillMap = self.idxMap[tabIdx]
        for i in skillMap:
            if skillMap[i] == skillId:
                skillMap.pop(i)
                break

        skillMap[idx] = skillId
        if tabIdx == uiConst.GUILD_WUSHUANG_XINDE:
            self.refreshXinDeInfo()
        elif tabIdx == uiConst.GUILD_WUSHUNAG_DAOHENG:
            self.refreshDaoHengInfo()

    def onSelect(self, *arg):
        idx = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if self.tabIdx == uiConst.GUILD_WUSHUANG_XINDE:
            for wsVal in p.guildWSPractice:
                if not wsVal or wsVal.idx != idx:
                    continue
                if wsVal.isBusy():
                    p.showGameMsg(GMDD.data.GUILD_WS_PRACTICE_BUSY, ())
                    return
                if not wsVal.isAvailToday():
                    p.showGameMsg(GMDD.data.GUILD_WS_PRACTICE_DAILY, ())
                    return

        elif self.tabIdx == uiConst.GUILD_WUSHUNAG_DAOHENG:
            for wsVal in p.guildWSDaoheng:
                if not wsVal or wsVal.idx != idx:
                    continue
                if wsVal.isBusy():
                    p.showGameMsg(GMDD.data.GUILD_WS_DAOHENG_BUSY, ())
                    return
                if not wsVal.isAvailToday():
                    p.showGameMsg(GMDD.data.GUILD_WS_DAOHENG_DAILY, ())
                    return

        else:
            return
        gameglobal.rds.ui.guildWuShuangSelect.show(self.tabIdx, idx)

    def onStart(self, *arg):
        idx = int(arg[3][0].GetNumber())
        if self.tabIdx not in self.idxMap:
            return
        else:
            skillId = self.idxMap[self.tabIdx].get(idx, 0)
            p = BigWorld.player()
            skInfoVal = p.wsSkills.get(skillId, None)
            if not skInfoVal:
                return
            lv = skInfoVal.level if skInfoVal else 1
            if self.tabIdx == uiConst.GUILD_WUSHUANG_XINDE:
                exp = 0
                for val in skInfoVal.proficiency.values():
                    exp += val

                needExp = WSLD.data.get((skillId, lv), {}).get('maxXd', 0)
                if exp >= needExp:
                    p.showGameMsg(GMDD.data.GUILD_WS_PRACTICE_FULL, ())
                    return
                msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_WS_PRACTICE_START_CHECK, '%s') % SGTD.data.get(skillId, {}).get('name', '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.startGuildWSPractice, idx, skillId))
            elif self.tabIdx == uiConst.GUILD_WUSHUNAG_DAOHENG:
                daoHengInfo = gameglobal.rds.ui.skill._genDirectionInfo(skillId)
                if daoHengInfo['value'] >= daoHengInfo['maxValue']:
                    p.showGameMsg(GMDD.data.GUILD_WS_DAOHENG_FULL, ())
                    return
                msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_WS_DAOHENG_START_CHECK, '%s') % SGTD.data.get(skillId, {}).get('name', '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.startGuildWSDaoheng, idx, skillId))
            return
