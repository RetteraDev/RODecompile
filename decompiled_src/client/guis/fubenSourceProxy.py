#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenSourceProxy.o
import BigWorld
import gameglobal
import gametypes
import uiUtils
import uiConst
import events
import const
from gamestrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis import groupDetailFactory
from uiProxy import UIProxy
from cdata import group_fb_menu_data as GFMD
from data import fb_data as FD
from cdata import game_msg_def_data as GMDD
SUCCESS = 1
FAILED = 2

class FubenSourceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FubenSourceProxy, self).__init__(uiAdapter)
        self.widget = None
        self.itemId = 0
        self.fubenItems = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_FUBEN_SOURCE, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()
        self.refreshPanel()
        self.initLayout()

    def initLayout(self):
        if gameglobal.rds.ui.itemSourceInfor.widget:
            itemSourceInfor = gameglobal.rds.ui.itemSourceInfor.widget
            x = itemSourceInfor.x + itemSourceInfor.width
            y = itemSourceInfor.y
            ASUtils.dragWidgetTo(self.widget, x, y)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.fubenArea.lableFunction = self.itemFunction
        self.widget.fubenArea.itemRenderer = 'FubenSource_Fuben_Item'
        self.widget.fubenArea.dataArray = self.fubenItems

    def refreshPanel(self):
        self.widget.slot.setItemSlotData(uiUtils.getGfxItemById(self.itemId))
        self.widget.slot.dragable = False

    def itemFunction(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        item.itemPanel.fubenName.text = data.fubenName
        item.teamBtn.data = data.fubenArgs[0]
        item.teleportBtn.data = data.fubenArgs[1]
        item.teamBtn.addEventListener(events.MOUSE_CLICK, self.handleClickTeamBtn)
        item.teleportBtn.addEventListener(events.MOUSE_CLICK, self.handleClickTeleportBtn)
        TipManager.addTip(item.teleportBtn, gameStrings.FUBEN_SOURCE_SEEK_PATH)
        TipManager.addTip(item.teamBtn, gameStrings.FUBEN_SOURCE_TEAM)

    def handleClickTeleportBtn(self, *arg):
        seekId = int(ASObject(arg[3][0]).currentTarget.data)
        gameglobal.rds.ui.itemSourceInfor.findPath(seekId)

    def handleClickTeamBtn(self, *arg):
        self.closeQuestPanel()
        p = BigWorld.player()
        fubenNo = int(ASObject(arg[3][0]).currentTarget.data)
        lvMin = FD.data.get(fubenNo).get('lvMin', 0)
        lvMax = FD.data.get(fubenNo).get('lvMax', const.MAX_CURRENT_LEVEL)
        if p.lv < lvMin or p.lv > lvMax:
            p.showGameMsg(GMDD.data.FUBEN_TEAM_LV_FAIL, ())
            return
        gameglobal.rds.ui.team.openTeamWithType(fubenNo, const.GROUP_GOAL_FB)

    def getFubenArgsFromName(self, fubenName):
        for fubenItem in self.fubenItems:
            if fubenItem['fubenName'] == fubenName:
                return fubenItem.get('fubenArgs', ())

        return ()

    def show(self, itemId, fubenItems):
        self.itemId = itemId
        self.fubenItems = fubenItems
        if self.widget:
            self.refreshPanel()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_SOURCE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FUBEN_SOURCE)
        self.widget = None
        self.itemId = 0
        self.fubenItems = []

    def closeQuestPanel(self):
        if gameglobal.rds.ui.quest.isShow or gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.funcNpc.closeByInv()
