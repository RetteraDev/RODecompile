#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/buffNoticeProxy.o
import BigWorld
import uiUtils
from guis import uiConst
from uiProxy import DataProxy
from data import state_data as SD
statePath = 'state/icon/'

class BuffNoticeProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(BuffNoticeProxy, self).__init__(uiAdapter)
        self.bindType = 'notice'
        self.modelMap = {}
        self.mediator = None
        self.dMediator = None
        self.oldState = []

    def _registerMediator(self, widgetId, mediator):
        p = BigWorld.player()
        if widgetId == uiConst.WIDGET_BUFF_NOTICE:
            self.mediator = mediator
            p.addPlayerAllStateIcon()
        elif widgetId == uiConst.WIDGET_DEBUFF_NOTICE:
            self.dMediator = mediator
            p.addPlayerAllStateIcon()

    def getValue(self, key):
        pass

    def matchState(self, buffId, srcId, stateId, stateSrc):
        data = SD.data.get(int(buffId), None)
        separateShow = data.get('separateShow', 0)
        if separateShow:
            return int(buffId) == stateId and int(srcId) == stateSrc
        else:
            return int(buffId) == stateId

    def changeStateIcon(self, addData, delData, stateType):
        if stateType == 1:
            if self.dMediator:
                self.dMediator.Invoke('changeState', (uiUtils.array2GfxAarry(addData), uiUtils.array2GfxAarry(delData)))
        elif stateType == 2:
            if self.mediator:
                self.mediator.Invoke('changeState', (uiUtils.array2GfxAarry(addData), uiUtils.array2GfxAarry(delData)))

    def clearStateIcon(self):
        if self.mediator:
            self.mediator.Invoke('clearBuff')
        if self.dMediator:
            self.dMediator.Invoke('clearBuff')

    def reset(self):
        self.mediator = None
        self.dMediator = None
