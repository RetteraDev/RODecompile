#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildScaleUpgradeProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from data import guild_scale_data as GSCD

class GuildScaleUpgradeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildScaleUpgradeProxy, self).__init__(uiAdapter)
        self.modelMap = {'close': self.onClose,
         'upgrade': self.onUpgrade}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_SCALE_UPGRADE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_SCALE_UPGRADE:
            self.mediator = mediator
            self.refresh()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_SCALE_UPGRADE)

    def show(self):
        if self.mediator:
            self.refresh()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_SCALE_UPGRADE)

    def refresh(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            info = {}
            info['nowScaleIcon'] = 'guildScale/%d.dds' % guild.scale
            info['nowScaleName'] = GSCD.data.get(guild.scale, {}).get('name', '')
            info['nextScaleIcon'] = 'guildScale/%d.dds' % (guild.scale + 1)
            info['nextScaleName'] = GSCD.data.get(guild.scale + 1, {}).get('name', '')
            canUpgrade = True
            costItemList = []
            costItems = GSCD.data.get(guild.scale + 1, {}).get('costItems', None)
            if costItems:
                for itemId, needNum in costItems:
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
                    ownNum = guild.otherRes.get(itemId, 0)
                    itemInfo['itemNum'] = uiUtils.convertNumStr(ownNum, needNum, needThousand=True)
                    if ownNum < needNum:
                        canUpgrade = False
                    costItemList.append(itemInfo)

            info['costItemList'] = costItemList
            info['canUpgrade'] = canUpgrade
            self.mediator.Invoke('refresh', uiUtils.dict2GfxDict(info, True))

    def onClose(self, *arg):
        self.hide()

    def onUpgrade(self, *arg):
        BigWorld.player().cell.upgradeGuildScale()
        self.hide()
