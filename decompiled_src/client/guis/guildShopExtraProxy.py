#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildShopExtraProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
from uiProxy import UIProxy
from data import guild_shop_refresh_data as GSRD

class GuildShopExtraProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildShopExtraProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickConfirm': self.onClickConfirm}
        self.mediator = None
        self.shopType = 0
        self.buildLv = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_SHOP_EXTRA, self.hide)

    def show(self, shopType, buildLv):
        self.shopType = shopType
        self.buildLv = buildLv
        if self.mediator:
            self.refreshInfo()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_SHOP_EXTRA)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_SHOP_EXTRA:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_SHOP_EXTRA)

    def onClickConfirm(self, *arg):
        BigWorld.player().cell.refreshGuildShop(self.shopType)
        self.hide()

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            info = {}
            enabledState = True
            if self.shopType == gametypes.GUILD_SHOP_TYPE_TREASURE:
                info['shopType'] = 'treasure'
                curRefreshCnt = p.guildMemberShopRefreshCnt + 1
                info['contrib'] = guild.getMemberShopRefreshContrib(curRefreshCnt)
                info['contribHave'] = p.guildContrib
                if info['contrib'] > info['contribHave']:
                    info['contribHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['contribHaveColor'] = '0xFFFFE7'
                info['shopRefreshCnt'] = gameStrings.TEXT_GUILDSHOPEXTRAPROXY_65 % curRefreshCnt
            else:
                info['shopType'] = 'normal'
                baseData = GSRD.data.get((self.shopType, self.buildLv), {})
                info['cash'] = baseData.get('bindCash', 0)
                info['cashHave'] = guild.bindCash
                if info['cash'] > info['cashHave']:
                    info['cashHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['cashHaveColor'] = '0xFFFFE7'
                info['wood'] = baseData.get('wood', 0)
                info['woodHave'] = guild.wood
                if info['wood'] > info['woodHave']:
                    info['woodHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['woodHaveColor'] = '0xFFFFE7'
                info['mojing'] = baseData.get('mojing', 0)
                info['mojingHave'] = guild.mojing
                if info['mojing'] > info['mojingHave']:
                    info['mojingHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['mojingHaveColor'] = '0xFFFFE7'
                info['xirang'] = baseData.get('xirang', 0)
                info['xirangHave'] = guild.xirang
                if info['xirang'] > info['xirangHave']:
                    info['xirangHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['xirangHaveColor'] = '0xFFFFE7'
            info['enabledState'] = enabledState
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
