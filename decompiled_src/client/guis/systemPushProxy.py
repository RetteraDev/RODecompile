#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/systemPushProxy.o
from Scaleform import GfxValue
import gameglobal
from guis import uiConst
from uiProxy import UIProxy
from guis import ui
from guis.ui import gbk2unicode
from guis import uiUtils
from data import item_data as ID
from cdata import font_config_data as FCD

class SystemPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SystemPushProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.reset()

    def reset(self):
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SYSTEM_PUSH:
            self.mediator = mediator

    def refresh(self):
        if self.mediator:
            self.mediator.Invoke('clearSystemInfo')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SYSTEM_PUSH)

    def additem(self, item, num):
        if hasattr(item, 'quality'):
            quality = item.quality
        else:
            quality = ID.data.get(item.id, {}).get('quality', 1)
        qualityColor = FCD.data.get(('item', quality), {}).get('color', '#CCCCCC')
        mwrap = ID.data.get(item.id, {}).get('mwrap', 0)
        needPile = True if mwrap > 1 else False
        iconPath = uiUtils.getItemIconFile40(item.id)
        text = "<font color=\'%s\'>%s</font>" % (qualityColor, item.name)
        self.addItemSound()
        self.setSystemInfo(iconPath, text, needPile, item.id, num)

    @ui.callFilter(1, False)
    def addItemSound(self):
        gameglobal.rds.sound.playSound(gameglobal.SD_472)

    def setSystemInfo(self, iconPath, text, needPile = False, itemId = 0, num = 0):
        if self.mediator:
            self.mediator.Invoke('setSystemInfo', (GfxValue(iconPath),
             GfxValue(gbk2unicode(text)),
             GfxValue(needPile),
             GfxValue(itemId),
             GfxValue(num)))
