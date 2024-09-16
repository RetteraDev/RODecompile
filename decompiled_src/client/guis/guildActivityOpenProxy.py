#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildActivityOpenProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import gametypes
from uiProxy import UIProxy
from data import guild_activity_data as GAD

class GuildActivityOpenProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildActivityOpenProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.activityId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_ACTIVITY_OPEN, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_ACTIVITY_OPEN:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_ACTIVITY_OPEN)

    def show(self, activityId):
        self.activityId = activityId
        if self.mediator:
            self.refreshInfo()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_ACTIVITY_OPEN)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            info = {}
            activityData = GAD.data.get(self.activityId, {})
            enabledState = True
            info['cash'] = activityData.get('bindCash', 0)
            info['cashHave'] = guild.bindCash
            if info['cash'] > info['cashHave']:
                info['cashHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['cashHaveColor'] = '0xFFFFE7'
            info['wood'] = activityData.get('wood', 0)
            info['woodHave'] = guild.wood
            if info['wood'] > info['woodHave']:
                info['woodHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['woodHaveColor'] = '0xFFFFE7'
            info['mojing'] = activityData.get('mojing', 0)
            info['mojingHave'] = guild.mojing
            if info['mojing'] > info['mojingHave']:
                info['mojingHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['mojingHaveColor'] = '0xFFFFE7'
            info['xirang'] = activityData.get('xirang', 0)
            info['xirangHave'] = guild.xirang
            if info['xirang'] > info['xirangHave']:
                info['xirangHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['xirangHaveColor'] = '0xFFFFE7'
            costItemList = []
            consumeItems = activityData.get('consumeItems', None)
            if consumeItems:
                for itemId, needNum in consumeItems:
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
                    ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
                    itemInfo['itemNum'] = uiUtils.convertNumStr(ownNum, needNum, needThousand=True)
                    if ownNum < needNum:
                        enabledState = False
                    costItemList.append(itemInfo)

            info['costItemList'] = costItemList
            info['enabledState'] = enabledState
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        p = BigWorld.player()
        if self.activityId == gametypes.GUILD_ACTIVITY_MATCH:
            p.cell.startGuildMatch()
        elif self.activityId == gametypes.GUILD_ACTIVITY_MONSTER:
            p.cell.startGuildActivity(self.activityId)
        self.hide()
