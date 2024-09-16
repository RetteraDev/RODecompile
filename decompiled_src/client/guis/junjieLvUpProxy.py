#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/junjieLvUpProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from data import item_data as ID
from cdata import font_config_data as FCD
from data import junjie_config_data as JCD

class JunjieLvUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(JunjieLvUpProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInitData': self.onGetInitData,
         'close': self.onClose,
         'confirm': self.onConfirm}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_JUNJIE_LVUP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_JUNJIE_LVUP:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_JUNJIE_LVUP)

    def show(self):
        if self.mediator == None:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_JUNJIE_LVUP)

    def onGetInitData(self, *arg):
        p = BigWorld.player()
        itemId = JCD.data.get(p.junJieLv, {}).get('needItem', 0)
        data = ID.data.get(itemId, {})
        itemInfo = {}
        itemInfo['id'] = itemId
        itemInfo['iconPath'] = uiUtils.getItemIconFile40(itemId)
        ownNum = p.inv.countItemInPages(itemId)
        needNum = 1
        if ownNum < needNum:
            itemInfo['count'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
            itemInfo['confirmEnable'] = False
        else:
            itemInfo['count'] = '%d/%d' % (ownNum, needNum)
            itemInfo['confirmEnable'] = True
        quality = data.get('quality', 1)
        qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        itemInfo['qualitycolor'] = qualitycolor
        return uiUtils.dict2GfxDict(itemInfo, True)

    def onClose(self, *arg):
        self.hide()

    def onConfirm(self, *arg):
        BigWorld.player().cell.junJieLvUp()
        self.hide()
