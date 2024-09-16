#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/introducerProxy.o
"""
Created on Oct 17, 2013
\xe8\xa1\xa8\xe6\x83\x85\xe7\xae\xa1\xe7\x90\x86
@author: Administrator
"""
from Scaleform import GfxValue
import gameglobal
from guis import uiConst
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy

class IntroducerProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(IntroducerProxy, self).__init__(uiAdapter)
        self.bindType = 'introducer'
        self.modelMap = {'getData': self.onGetData,
         'closeIntroducer': self.closeIntroducer}
        self.mediator = None
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INTRODUCER:
            self.mediator = mediator

    def reset(self):
        self.stepArgs = None

    def show(self, stepArgs):
        self.stepArgs = stepArgs
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INTRODUCER)

    def hideIntroducer(self):
        if self.mediator:
            self.mediator.Invoke('playCloseAnimation')

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INTRODUCER)

    def onGetData(self, *arg):
        ret = self.movie.CreateObject()
        if self.stepArgs:
            ret.SetMember('roleName', GfxValue(gbk2unicode(self.stepArgs[0])))
        return ret

    def closeIntroducer(self, *arg):
        self.clearWidget()

    def onCloseClick(self, *arg):
        pass
