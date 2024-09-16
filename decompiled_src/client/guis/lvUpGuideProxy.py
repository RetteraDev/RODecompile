#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/lvUpGuideProxy.o
from Scaleform import GfxValue
import gameglobal
import uiConst
from uiProxy import UIProxy
from ui import gbk2unicode
from data import lv_up_guide_activity_data as LUGAD
from data import play_recomm_data as PRD
ICON_IMAGE_RES = 'lvUpGuide/'

class LvUpGuideProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LvUpGuideProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'getInitData': self.onGetInitData,
         'clickItem': self.onClickItem}
        self.mediator = None
        self.lv = 0
        self.skillList = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_LV_UP_GUIDE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_LV_UP_GUIDE:
            self.mediator = mediator

    def onClickClose(self, *arg):
        self.hide(True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LV_UP_GUIDE)

    def reset(self):
        super(self.__class__, self).reset()
        self.lv = 0
        self.skillList = []

    def onClickItem(self, *arg):
        lv = int(arg[3][0].GetNumber())
        index = int(arg[3][1].GetString())
        data = LUGAD.data.get(lv, {}).get('activityData', ())[index]
        if len(data) < 5:
            return
        playRecommId = data[4]
        page = PRD.data.get(playRecommId, {}).get('type')[0]
        gameglobal.rds.ui.playRecomm.setInitPage(page, playRecommId)
        gameglobal.rds.ui.playRecomm.show()

    def onGetInitData(self, *arg):
        lvUpGuideObj = self.movie.CreateObject()
        activityArray = self.movie.CreateArray()
        if self.lv in LUGAD.data:
            lvUpGuideObj.SetMember('lv', GfxValue(self.lv))
            activityData = LUGAD.data[self.lv].get('activityData', ())
            for i, item in enumerate(activityData):
                activityObj = self.movie.CreateObject()
                activityObj.SetMember('name', GfxValue(gbk2unicode(item[0])))
                activityObj.SetMember('type', GfxValue(item[1]))
                activityObj.SetMember('imagePath', GfxValue(ICON_IMAGE_RES + str(item[2]) + '.dds'))
                activityObj.SetMember('desc', GfxValue(gbk2unicode(item[3])))
                activityArray.SetElement(i, activityObj)

            lvUpGuideObj.SetMember('activityArray', activityArray)
        return lvUpGuideObj

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        id = int(key[14:])
        return gameglobal.rds.ui.skill.formatTooltip(self.skillList[id])

    def show(self):
        if self.mediator:
            return
        if self.lv:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LV_UP_GUIDE)

    def refresh(self):
        pass
