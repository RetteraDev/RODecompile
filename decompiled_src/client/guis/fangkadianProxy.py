#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fangkadianProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import hotkey as HK
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy

class FangkadianProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FangkadianProxy, self).__init__(uiAdapter)
        self.modelMap = {'fangkadian': self.onFangkadian,
         'hide': self.onHide,
         'opera': self.onOpera,
         'armor': self.onArmor,
         'getBrief': self.onGetBrief,
         'getInitData': self.onGetInitData}
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FANGKADIAN:
            self.mediator = mediator

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FANGKADIAN)

    def onFangkadian(self, *arg):
        BigWorld.player().fangKaDian()

    def onHide(self, *arg):
        BigWorld.player().hidePlayerAndMonster(True)

    def onOpera(self, *arg):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NEW_GUIDER_OPERATION)

    def onArmor(self, *arg):
        selected = arg[3][0].GetBool()
        if not BigWorld.player().stateMachine.checkStatus(const.CT_CLAN_WAR_ARMOR):
            return
        BigWorld.player().operation['commonSetting'][17] = 1 if selected else 0
        BigWorld.player().sendOperation()
        uiUtils.setClanWarArmorMode()
        self.setArmorBtnSelect(selected)

    def onGetInitData(self, *arg):
        self.updateHideMode()

    def updateHideMode(self):
        if self.mediator:
            modeMap = {gameglobal.HIDE_MODE0: 'mode0',
             gameglobal.HIDE_MODE1: 'mode1',
             gameglobal.HIDE_MODE2: 'mode2',
             gameglobal.HIDE_MODE3: 'mode3',
             gameglobal.HIDE_MODE4: 'mode4',
             gameglobal.HIDE_MODE5: 'mode5',
             gameglobal.HIDE_MODE6: 'mode5'}
            self.mediator.Invoke('updateHideMode', GfxValue(modeMap[gameglobal.gHideMode]))

    def onGetBrief(self, *arg):
        detial = HK.HKM[HK.KEY_HIDE_PLAYER_MONSTER]
        if detial.getBrief() != '':
            return GfxValue(detial.getBrief())
        elif detial.getBrief(2) != '':
            return GfxValue(detial.getBrief(2))
        else:
            return GfxValue('')

    def setArmorBtnVisible(self, visible):
        if self.mediator:
            self.mediator.Invoke('setArmorBtnVisible', GfxValue(visible))
        if visible:
            if hasattr(BigWorld.player(), 'operation'):
                self.setArmorBtnSelect(BigWorld.player().operation['commonSetting'][17])

    def setArmorBtnSelect(self, select):
        if self.mediator:
            self.mediator.Invoke('setArmorBtnSelect', GfxValue(select))
