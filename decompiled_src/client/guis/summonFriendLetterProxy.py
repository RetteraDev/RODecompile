#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendLetterProxy.o
import BigWorld
import uiConst
import events
from uiProxy import UIProxy
from guis.asObject import ASObject
from data import sys_config_data as SCD
MAX_BTN_NUM = 5

class SummonFriendLetterProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonFriendLetterProxy, self).__init__(uiAdapter)
        self.widget = None
        self.curSelectIdx = 0
        self.curSelectBtn = None
        self.recallGbId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMON_FRIEND_LETTER, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMON_FRIEND_LETTER:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMON_FRIEND_LETTER)

    def reset(self):
        self.curSelectIdx = 0
        self.curSelectBtn = None
        self.recallGbId = 0

    def show(self, recallGbId):
        self.recallGbId = int(recallGbId)
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMON_FRIEND_LETTER, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        summonFriendLetterDict1 = SCD.data.get('summonFriendLetterDict1', {})
        for i in xrange(MAX_BTN_NUM):
            contentBtn = self.widget.getChildByName('contentBtn%d' % i)
            contentBtn.label = summonFriendLetterDict1.get(i, '')
            contentBtn.addEventListener(events.MOUSE_CLICK, self.handleSelectBtnClick, False, 0, True)
            contentBtn.idx = i
            contentBtn.selectState.visible = False
            if not self.curSelectBtn:
                self.curSelectBtn = contentBtn
                self.curSelectIdx = i
                contentBtn.selectState.visible = True

    def _onSendBtnClick(self, e):
        p = BigWorld.player()
        fVal = p.getFValByGbId(self.recallGbId)
        if not fVal:
            return
        summonFriendLetterDict2 = SCD.data.get('summonFriendLetterDict2', {})
        msg = summonFriendLetterDict2.get(self.curSelectIdx, '%s%s') % (fVal.name, p.realRoleName)
        p.base.sendFriendRecallInvitation(self.recallGbId, fVal.name, msg)
        self.hide()

    def _onCancelBtnClick(self, e):
        self.hide()

    def handleSelectBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.idx == self.curSelectIdx:
            return
        self.curSelectBtn.selectState.visible = False
        target.selectState.visible = True
        self.curSelectBtn = target
        self.curSelectIdx = target.idx
