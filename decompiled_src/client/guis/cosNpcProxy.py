#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cosNpcProxy.o
import BigWorld
import gamelog
import uiConst
import commNpcFavor
from guis import events
from guis.asObject import ASObject
from uiProxy import UIProxy
from data import state_data as SD

class CosNpcProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CosNpcProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_COS_NPC, self.hide)

    def reset(self):
        self.npcId = 0
        self.selectedBuffId = 0
        self.lastSelectedMc = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_COS_NPC:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_COS_NPC)

    def show(self, npcId):
        self.npcId = npcId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_COS_NPC)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.sureBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBtnClick, False, 0, True)
        self.widget.scrollWndList.itemRenderer = 'CosNpc_ItemRender'
        self.widget.scrollWndList.column = 2
        self.widget.scrollWndList.labelFunction = self.labelFunction

    def labelFunction(self, *args):
        npcInfo = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.txtName.text = npcInfo[1]
        buffId = int(npcInfo[0])
        buffPath = 'state/40/%d.dds' % SD.data.get(buffId, {}).get('iconId', '')
        itemMc.head.icon.fitSize = True
        itemMc.head.icon.loadImage(buffPath)
        itemMc.data = buffId
        if buffId == self.selectedBuffId:
            if self.lastSelectedMc:
                self.lastSelectedMc.selected = False
            self.lastSelectedMc = itemMc
            self.lastSelectedMc.selected = True
        itemMc.addEventListener(events.BUTTON_CLICK, self.handleBuffClick, False, 0, True)

    def handleBuffClick(self, *args):
        e = ASObject(args[3][0])
        buffId = int(e.currentTarget.data)
        if buffId == self.selectedBuffId:
            return
        self.selectedBuffId = buffId
        if self.lastSelectedMc:
            self.lastSelectedMc.selected = False
        self.lastSelectedMc = e.currentTarget
        self.lastSelectedMc.selected = True

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.scrollWndList.dataArray = BigWorld.player().npcFavor.getNpcCosList(self.npcId)

    def handleSureBtnClick(self, *args):
        if not self.selectedBuffId:
            return
        gamelog.info('jbx:actorRoleNF', commNpcFavor.getNpcPId(self.npcId), self.selectedBuffId)
        BigWorld.player().base.actorRoleNF(commNpcFavor.getNpcPId(self.npcId), self.selectedBuffId)
