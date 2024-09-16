#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildResidentUpdateTiredProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import const
from uiProxy import UIProxy
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD

class GuildResidentUpdateTiredProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildResidentUpdateTiredProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.entityId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RESIDENT_UPDATE_TIRED, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_RESIDENT_UPDATE_TIRED:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_RESIDENT_UPDATE_TIRED)

    def show(self, entityId):
        p = BigWorld.player()
        noItem = True
        residentUpdateTiredList = GCD.data.get('residentUpdateTiredList', ())
        for itemId in residentUpdateTiredList:
            num = p.questBag.countItemInPages(itemId)
            if num > 0:
                noItem = False
                break

        if noItem:
            p.showGameMsg(GMDD.data.GUILD_RESIDENT_UPDATE_TIRED_NOITEM, ())
            return
        self.entityId = entityId
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_RESIDENT_UPDATE_TIRED)

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            itemList = []
            residentUpdateTiredList = GCD.data.get('residentUpdateTiredList', ())
            for itemId in residentUpdateTiredList:
                num = p.questBag.countItemInPages(itemId)
                if num <= 0:
                    continue
                itemInfo = uiUtils.getGfxItemById(itemId)
                itemList.append(itemInfo)

            info['itemList'] = itemList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        pg, ps = p.questBag.findItemInPages(itemId)
        if pg != const.CONT_NO_PAGE and ps != const.CONT_NO_POS and self.entityId:
            p.cell.useQuestItemWithTarget(pg, ps, self.entityId)
        self.hide()
