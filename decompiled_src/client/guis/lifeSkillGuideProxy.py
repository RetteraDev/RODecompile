#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/lifeSkillGuideProxy.o
from Scaleform import GfxValue
import gameglobal
import uiConst
from uiProxy import UIProxy
FISHING_GUIDE_PAGES = 10
EXPLORE_GUIDE_PAGES = 10
SPECIAL_SKILL_GUIDE_PAGES = 10
NORMAL_SKILL_GUIDE_PAGES = 7
FISHING_GAME_GUIDE_PAGES = 1

class LifeSkillGuideProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LifeSkillGuideProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'gotoPage': self.onGotoPage,
         'getMaxPage': self.onGetMaxPage}
        self.mediator = None
        self.guideType = uiConst.GUIDE_TYPE_FISHING
        uiAdapter.registerEscFunc(uiConst.WIDGET_LIFE_SKILL_GUIDE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_LIFE_SKILL_GUIDE:
            self.mediator = mediator

    def show(self, guideType = uiConst.GUIDE_TYPE_FISHING):
        self.guideType = guideType
        if self.mediator:
            self.setPanel()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LIFE_SKILL_GUIDE)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LIFE_SKILL_GUIDE)

    def _getMaxPages(self):
        ret = 1
        if self.guideType == uiConst.GUIDE_TYPE_FISHING:
            ret = FISHING_GUIDE_PAGES
        elif self.guideType == uiConst.GUIDE_TYPE_EXPLORE:
            ret = EXPLORE_GUIDE_PAGES
        elif self.guideType == uiConst.GUIDE_TYPE_NORMAL_SKILL:
            ret = NORMAL_SKILL_GUIDE_PAGES
        elif self.guideType == uiConst.GUIDE_TYPE_SPECIAL_SKILL:
            ret = SPECIAL_SKILL_GUIDE_PAGES
        elif self.guideType == uiConst.GUIDE_TYPE_FISHING_GAME:
            ret = FISHING_GAME_GUIDE_PAGES
        return ret

    def setPanel(self):
        if self.mediator != None:
            ret = self._getMaxPages()
            self.mediator.Invoke('setPanel', GfxValue(ret))

    def onClosePanel(self, *arg):
        self.hide()

    def onGotoPage(self, *arg):
        page = int(arg[3][0].GetNumber())
        path = 'lifeSkillGuide/%d/%d.dds' % (self.guideType, page)
        if self.mediator != None:
            self.mediator.Invoke('loadImage', GfxValue(path))

    def onGetMaxPage(self, *arg):
        ret = self._getMaxPages()
        return GfxValue(ret)
