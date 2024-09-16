#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldBossBuffProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis import events
from guis import worldBossHelper
from guis.asObject import TipManager
from gamestrings import gameStrings
from data import state_data as SD
BUFF_NUM = 3

class WorldBossBuffProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WorldBossBuffProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.currChooseBuffId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_WORLD_BOSS_BUFF, self.hide)

    def reset(self):
        self.currChooseBuffId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WORLD_BOSS_BUFF:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WORLD_BOSS_BUFF)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WORLD_BOSS_BUFF)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.state2.quitBtn.addEventListener(events.BUTTON_CLICK, self.onQuitBuffBtnClick)
        self.widget.state1.chooseBtn.addEventListener(events.BUTTON_CLICK, self.onChooseBtnClick)

    def onChooseBtnClick(self, *args):
        p = BigWorld.player()
        if self.currChooseBuffId:
            p.base.worldBossChooseBuff(self.currChooseBuffId)

    def onQuitBuffBtnClick(self, *args):
        msg = gameStrings.WORLD_BOSS_BUFF_QUIT_CONFIRM
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.conformDropBuff)

    def conformDropBuff(self):
        p = BigWorld.player()
        p.base.dropWorldBossBuff()

    def setBuffIcon(self, slot, buffId):
        cfg = SD.data.get(buffId, {})
        iconId = cfg.get('iconId', 'notFound')
        iconPath = 'state/40/%s.dds' % iconId
        slot.fitSize = True
        slot.dragable = False
        slot.loadImage(iconPath)
        buffText = cfg.get('desc', '')
        TipManager.addTip(slot, buffText)

    def refreshInfo(self):
        if not self.widget:
            return
        inSelectState = worldBossHelper.getInstance().inSelectBuffState()
        self.widget.state1.visible = False
        self.widget.state2.visible = False
        if inSelectState:
            self.widget.state1.visible = True
            buffList = worldBossHelper.getInstance().getSelectBuffList()
            if self.currChooseBuffId not in buffList:
                self.currChooseBuffId = buffList[0]
            for i in xrange(0, BUFF_NUM):
                buffMc = self.widget.state1.getChildByName('buff%d' % i)
                if i < len(buffList):
                    buffMc.visible = True
                    buffId = buffList[i]
                    cfg = SD.data.get(buffId, {})
                    self.setBuffIcon(buffMc.slot, buffId)
                    buffMc.checkBox.visible = False
                    buffMc.checkBox.label = cfg.get('name', '')
                    buffMc.checkBox.buffId = buffId
                    buffMc.desc.text = cfg.get('name', '')
                else:
                    buffMc.visible = False

            self.refreshCheckState()
        else:
            chooseBuff = worldBossHelper.getInstance().getChooseBuff()
            self.widget.state2.visible = True
            cfg = SD.data.get(chooseBuff, {})
            self.setBuffIcon(self.widget.state2.slot, chooseBuff)
            self.widget.state2.buffName.text = cfg.get('name', '')

    def refreshCheckState(self):
        for i in xrange(0, BUFF_NUM):
            buffMc = self.widget.state1.getChildByName('buff%d' % i)
            buffId = buffMc.checkBox.buffId
            buffMc.checkBox.removeEventListener(events.EVENT_SELECT, self.onCheckBoxCheck)
            if self.currChooseBuffId == buffId:
                buffMc.checkBox.selected = True
            else:
                buffMc.checkBox.selected = False
            buffMc.checkBox.addEventListener(events.EVENT_SELECT, self.onCheckBoxCheck)

    def onCheckBoxCheck(self, *args):
        e = ASObject(args[3][0])
        if not e.currentTarget.selected:
            return
        buffId = e.currentTarget.buffId
        self.currChooseBuffId = buffId
        self.refreshCheckState()
