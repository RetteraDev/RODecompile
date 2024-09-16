#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildFindStarProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import random
import uiUtils
import uiConst
from uiProxy import UIProxy
from data import state_data as SD
from data import guild_astrology_data as GAD
from data import guild_config_data as GCD
from data import guild_technology_data as GTD
from cdata import guild_astrology_state_reverse_data as GASRD
from cdata import guild_astrology_tech_reverse_data as GATRD
from cdata import game_msg_def_data as GMDD
from cdata import guild_func_prop_def_data as GFNPDD
BUFF_MAP = {0: 22,
 1: 23,
 2: 0,
 3: 1,
 4: 2,
 5: 3,
 6: 4,
 7: 5,
 8: 18,
 9: 19,
 10: 20,
 11: 21,
 12: 10,
 13: 11,
 14: 12,
 15: 13,
 16: 14,
 17: 15,
 18: 16,
 19: 17,
 20: 6,
 21: 7,
 22: 8,
 23: 9}

class GuildFindStarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildFindStarProxy, self).__init__(uiAdapter)
        self.modelMap = {'close': self.onClose,
         'clickManager': self.onClickManager,
         'beginFindStar': self.onBeginFindStar,
         'setCloseMsgBox': self.onSetCloseMsgBox,
         'getItem': self.onGetItem}
        self.mediator = None
        self.markerId = 0
        self.buildLv = 0
        self.buffList = []
        self.contrib = 0
        self.needCloseMsgBox = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_FIND_STAR, self.close)

    def show(self, markerId):
        self.markerId = markerId
        if not self.mediator:
            gameglobal.rds.ui.guild.hideAllGuildBuilding()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_FIND_STAR)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_FIND_STAR:
            self.mediator = mediator
            self.refreshInitData()
            self.refreshTimeInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_FIND_STAR)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.markerId = 0
        self.buildLv = 0
        self.buffList = []
        self.contrib = 0
        self.needCloseMsgBox = False
        gameglobal.rds.sound.stopSound(gameglobal.SD_498)

    def refreshInitData(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID)
            self.buildLv = buildValue.level if buildValue else 0
            info = {}
            info['level'] = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % self.buildLv
            astrologyBuff = guild._getAstrologyBuff()
            buffList = []
            idx = 0
            for lv, stype, locked in astrologyBuff:
                baseData = GAD.data.get((lv, stype), {})
                buffData = SD.data.get(baseData.get('buffId', (0,))[0], {})
                buffInfo = {}
                buffInfo['idx'] = BUFF_MAP.get(idx, 0)
                buffInfo['lv'] = lv
                buffInfo['iconPath'] = 'state/48/%d.dds' % buffData.get('iconId', 0)
                buffInfo['tipDesc'] = '%s<br>%s' % (buffData.get('name', ''), buffData.get('desc', ''))
                buffInfo['locked'] = locked
                techId = GATRD.data.get(stype, 0)
                buffInfo['techTips'] = gameStrings.TEXT_GUILDFACTORYPROXY_127 % GTD.data.get(techId, {}).get('name', '')
                buffList.append(buffInfo)
                idx += 1

            info['buffList'] = buffList
            self.mediator.Invoke('refreshInitData', uiUtils.dict2GfxDict(info, True))

    def refreshTimeInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            info['timeNum'] = gameStrings.TEXT_GUILDFINDSTARPROXY_110 % (p.dailyAstrologyCount, GCD.data.get('dailyAstrologyLimit', const.GUILD_DAILY_ASTROLOGY_LIMIT))
            astrologyConsumeContrib = GCD.data.get('astrologyConsumeContrib', None)
            if astrologyConsumeContrib and len(astrologyConsumeContrib) >= self.buildLv:
                consumeContrib = astrologyConsumeContrib[self.buildLv - 1]
            else:
                consumeContrib = const.GUILD_DAILY_ASTROLOGY_CONTRIB
            self.contrib = 0
            if p.dailyAstrologyCount < len(consumeContrib):
                self.contrib = consumeContrib[p.dailyAstrologyCount]
            else:
                self.contrib = consumeContrib[-1]
            self.contrib = int(self.contrib * 1.0 / (1 + p.guild.getAbility(GFNPDD.data.ASTROLOGY_REDUCE_CONTRIB)))
            if self.contrib > p.guildContrib:
                contrib = uiUtils.toHtml(str(self.contrib), '#F43804')
            else:
                contrib = uiUtils.toHtml(str(self.contrib), '#4D4339')
            info['contrib'] = contrib
            self.mediator.Invoke('refreshTimeInfo', uiUtils.dict2GfxDict(info, True))

    def beginFindStar(self, num):
        self.refreshTimeInfo()
        if self.mediator:
            idx = BUFF_MAP.get(num, 0)
            index = random.choice([idx + 3, idx + 27])
            gameglobal.rds.sound.playSound(gameglobal.SD_498)
            self.mediator.Invoke('rotate', GfxValue(index))

    def onGetItem(self, *arg):
        p = BigWorld.player()
        buffNum = 0
        for buffId in p.statesServerAndOwn:
            key = GASRD.data.get(buffId, ())
            if key:
                buffNum += 1

        if buffNum < p.guild._getMaxAstrologyState():
            p.cell.applyGuildAstrologyAward(0)
        else:
            gameglobal.rds.ui.guildAstrologyChoose.show(False)

    def onClose(self, *arg):
        self.close()

    def close(self):
        if self.needCloseMsgBox:
            msg = gameStrings.TEXT_GUILDFINDSTARPROXY_157
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.hide)
        else:
            self.hide()

    def onClickManager(self, *arg):
        gameglobal.rds.ui.guildResidentManager.showOrHide(self.markerId)

    def onBeginFindStar(self, *arg):
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        p = BigWorld.player()
        if p.astrologyId:
            gameglobal.rds.ui.guildAstrologyChoose.show(True)
            return GfxValue(True)
        elif self.contrib > p.guildContrib:
            p.showGameMsg(GMDD.data.GUILD_NOT_ENOUGH_CONTRIB, ())
            return GfxValue(True)
        else:
            BigWorld.player().cell.guildAstrology()
            return GfxValue(False)

    def onSetCloseMsgBox(self, *arg):
        self.needCloseMsgBox = arg[3][0].GetBool()
        if not self.needCloseMsgBox:
            gameglobal.rds.sound.stopSound(gameglobal.SD_498)

    def astrologyFailed(self):
        if self.mediator:
            if BigWorld.player().dailyAstrologyCount >= GCD.data.get('dailyAstrologyLimit', const.GUILD_DAILY_ASTROLOGY_LIMIT):
                self.needCloseMsgBox = False
            else:
                self.mediator.Invoke('astrologyFailed')
