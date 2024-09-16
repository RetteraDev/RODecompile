#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArena2PersonRequireProxy.o
import gameglobal
import gamelog
from guis import events
from guis import uiUtils
from gamestrings import gameStrings
from data import duel_config_data as DCD

class BalanceArena2PersonRequireProxy(object):

    def __init__(self):
        super(BalanceArena2PersonRequireProxy, self).__init__()
        self.widget = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        self.widget.goBtn.addEventListener(events.BUTTON_CLICK, self.onSeekBtnClick, False, 0, True)
        self.initStepAndRequire()
        self.initTips()

    def onSeekBtnClick(self, *args):
        gamelog.debug('dxk@balanceArena2PersonProxy Seek to the npc by seeker id', DCD.data.get('doubleArenaSeekId', 0))
        uiUtils.findPosById(DCD.data.get('doubleArenaSeekId', 0))

    def initTips(self):
        tips = DCD.data.get('doubleArenaRequireTips', gameStrings.DOUBLEARENA_REQUIRE_TIPS)
        self.widget.tip0.text = tips[0]
        self.widget.tip1.text = tips[1]

    def initStepAndRequire(self):
        steps = DCD.data.get('doubleArenaSteps', gameStrings.DOBULEARENA_STEPS)
        requires = DCD.data.get('doubleArenaReqires', gameStrings.DOBULEARENA_REQUIRES)
        for i in xrange(len(steps)):
            stepMc = self.widget.getChildByName('step%s' % str(i))
            if stepMc:
                stepMc.textField.text = steps[i]
                stepMc.finishMc.visible = False

        for i in xrange(len(requires)):
            requireMc = self.widget.getChildByName('require%s' % str(i))
            if requireMc:
                requireMc.textField.text = requires[i]
                requireMc.finishMc.visible = False

    def refreshInfo(self):
        pass
