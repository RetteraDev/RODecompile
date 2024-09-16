#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/holidayMessageBoxProxy.o
from gamestrings import gameStrings
from Scaleform import GfxValue
import uiConst
import gameglobal
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
from guis import uiUtils
from ui import gbk2unicode

class HolidayMessageBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HolidayMessageBoxProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickConfirm': self.onClickConfirm,
         'getInitData': self.onGetInitData}
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_HOLIDAY_MESSAGEBOX:
            self.mediator = mediator

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_HOLIDAY_MESSAGEBOX)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_HOLIDAY_MESSAGEBOX)

    def reset(self):
        self.mediator = None

    def onClickConfirm(self, *arg):
        gameglobal.rds.ui.characterCreate.enterGame(isHoliday=True)
        self.clearWidget()

    def onGetInitData(self, *arg):
        describeStr = uiUtils.getTextFromGMD(GMDD.data.HOLIDAY_DESCRIBE_TEXT, gameStrings.TEXT_HOLIDAYMESSAGEBOXPROXY_44)
        return GfxValue(gbk2unicode(describeStr))
