#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/npcSlotProxy.o
import BigWorld
import gameglobal
import uiConst
import gamelog
from ui import callFilter
from uiProxy import UIProxy
from guis import uiUtils

class NpcSlotProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NpcSlotProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerNpcSlot': self.onRegisterNpcSlot,
         'getIconPath': self.onGetIconPath,
         'clickIcon': self.onClickIcon}
        self.mc = None
        self.path = None
        self.params = None
        self.isShow = False
        self.type = None

    def onRegisterNpcSlot(self, *arg):
        self.mc = arg[3][0]

    def onGetIconPath(self, *arg):
        gamelog.debug('jjh@npcSlot.onGetIconPath ', self.path)
        ret = [self.path, self.params[1], self.params[2]]
        return uiUtils.array2GfxAarry(ret, True)

    def show(self, path, type = uiConst.SLOT_FROM_MARK_NPC, params = {}):
        if not params or path is None:
            gamelog.error('@szh: ERROR NpcSlot.show', path, params)
        self.path = path
        self.params = params
        self.isShow = True
        self.type = type
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NPC_SLOT)

    def hide(self, destroy = True):
        if self.isShow:
            self._realClose()

    def _realClose(self):
        self.mc = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NPC_SLOT)
        self.isShow = False
        self.type = None
        self.params = None

    @callFilter(uiConst.SERVER_CALL_ABANDONTASK, False)
    def onClickIcon(self, *arg):
        p = BigWorld.player()
        if self.type == uiConst.SLOT_FROM_MARK_NPC:
            if self.params:
                p.useMarkerNpc(self.params[0])
        elif self.type == uiConst.SLOT_FROM_MONSTER:
            itemId = self.params[0]
            page, pos = p.questBag.findItemInPages(itemId, includeExpired=True, includeLatch=True, includeShihun=True)
            BigWorld.player().useQuestItem(page, pos)
        elif self.type == uiConst.SLOT_FROM_CLAN_WAR_CREATION:
            entId = self.params[0]
            p.useClanWarItem(entId)
        elif self.type == uiConst.SLOT_FROM_GUILD_BUILDING:
            entId = self.params[0]
            p.createGuildBuilding(entId)
