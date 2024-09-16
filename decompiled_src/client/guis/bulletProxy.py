#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bulletProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
from guis import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy
from data import consume_state_data as CSD

class BulletProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BulletProxy, self).__init__(uiAdapter)
        self.modelMap = {'getToolTips': self.onGetToolTips}
        self.mediator = None
        self.isShow = False
        self.maxAmmoNum = 1
        self.ammoType = None
        self.desc = ''
        self.hasState = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BULLET:
            self.mediator = mediator
            if BigWorld.player().life == gametypes.LIFE_DEAD:
                self.setVisible(False)
            elif gameglobal.rds.ui.isHideAllUI():
                self.setVisible(False)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_BULLET, True)

    def onGetToolTips(self, *arg):
        return GfxValue(gbk2unicode(self.desc))

    def show(self):
        self.hasState = False
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BULLET)
        self.isShow = True
        self.checkAvatarState()

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BULLET)
        self.isShow = False

    def reset(self):
        self.mediator = None

    def setVisible(self, visible):
        if self.mediator:
            self.mediator.Invoke('setVisible', GfxValue(visible))

    def _setBulletIcon(self, state):
        csd = CSD.data.get((BigWorld.player().ammoType, state), {})
        icon = csd.get('icon', None)
        path = 'skill/icon/' + str(icon) + '.dds'
        self.desc = csd.get('desc', None)
        if self.mediator != None:
            self.mediator.Invoke('setBulletIcon', (GfxValue(path), GfxValue(BigWorld.player().ammoNum)))

    def setBulletNum(self):
        if self.mediator != None:
            self.mediator.Invoke('setBulletNum', GfxValue(BigWorld.player().ammoNum))

    def checkAvatarState(self):
        gameStrings.TEXT_BULLETPROXY_70
        if gameglobal.rds.ui.isHideAllUI():
            return
        gameStrings.TEXT_BULLETPROXY_74
        self.setVisible(not gameglobal.rds.ui.skill.inAirBattleState())
