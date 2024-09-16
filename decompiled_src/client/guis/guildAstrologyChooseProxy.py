#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildAstrologyChooseProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
from uiProxy import UIProxy
from data import state_data as SD
from data import guild_astrology_data as GAD
from cdata import guild_astrology_state_reverse_data as GASRD

class GuildAstrologyChooseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildAstrologyChooseProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'cancel': self.onCancel}
        self.mediator = None
        self.isLast = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_ASTROLOGY_CHOOSE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_ASTROLOGY_CHOOSE:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_ASTROLOGY_CHOOSE)

    def reset(self):
        self.isLast = False

    def show(self, isLast):
        self.isLast = isLast
        if self.mediator:
            self.refreshInfo()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_ASTROLOGY_CHOOSE)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            if not p.astrologyId:
                self.hide()
                return
            info = {}
            if self.isLast:
                info['hint'] = gameStrings.TEXT_GUILDASTROLOGYCHOOSEPROXY_53
            else:
                info['hint'] = gameStrings.TEXT_GUILDASTROLOGYCHOOSEPROXY_55
            info['maxNum'] = p.guild._getMaxAstrologyState()
            info['lockTips'] = gameStrings.TEXT_GUILDASTROLOGYCHOOSEPROXY_57
            buffList = []
            for buffId in p.statesServerAndOwn:
                key = GASRD.data.get(buffId, ())
                if key:
                    buffData = SD.data.get(buffId, {})
                    buffInfo = {}
                    buffInfo['buffId'] = buffId
                    buffInfo['lv'] = key[0]
                    buffInfo['iconPath'] = 'state/48/%d.dds' % buffData.get('iconId', 0)
                    buffInfo['tipDesc'] = buffData.get('desc', '')
                    buffList.append(buffInfo)

            info['buffList'] = buffList
            buffId = GAD.data.get(p.astrologyId, {}).get('buffId', (0,))[0]
            buffData = SD.data.get(buffId, {})
            nowBuff = {}
            nowBuff['lv'] = p.astrologyId[0]
            nowBuff['iconPath'] = 'state/48/%d.dds' % buffData.get('iconId', 0)
            nowBuff['tipDesc'] = buffData.get('desc', '')
            info['nowBuff'] = nowBuff
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        buffId = int(arg[3][0].GetNumber())
        BigWorld.player().cell.applyGuildAstrologyAward(buffId)
        self.hide()

    def onCancel(self, *arg):
        BigWorld.player().cell.discardGuildAstrologyAward()
        self.hide()
