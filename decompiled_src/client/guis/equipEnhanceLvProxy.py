#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/equipEnhanceLvProxy.o
from Scaleform import GfxValue
import gameglobal
from guis import uiConst
from guis import uiUtils
from guis.uiProxy import UIProxy
from data import equip_enhance_refining_data as EERD

class EquipEnhanceLvProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipEnhanceLvProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.closeWidget,
         'refreshPanel': self.refreshPanel,
         'selectItem': self.selectItem}
        self.mediator = None
        self.isShow = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_ENHANCE_LV, self.clearWidget)

    def closeWidget(self, *args):
        self.clearWidget()

    def clearWidget(self):
        self.mediator = None
        self.isShow = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_ENHANCE_LV)

    def show(self):
        self.isShow = True
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_ENHANCE_LV)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_ENHANCE_LV:
            self.mediator = mediator

    def refreshLvInfo(self):
        dataList = []
        if self.mediator:
            maxLv = gameglobal.rds.ui.equipEnhance.getMaxRefineLv()
            currentLv = gameglobal.rds.ui.equipEnhance.getEnhanceLv()
            self.mediator.Invoke('setMaxRefineLv', GfxValue(maxLv))
            self.mediator.Invoke('setSelectPos', GfxValue(currentLv))
            item = gameglobal.rds.ui.equipEnhance.getEnhanceItem()
            if item:
                if hasattr(item, 'enhanceRefining'):
                    equipRefining = item.enhanceRefining
                    maxLv = getattr(item, 'maxEnhlv', 0)
                    maxUse = maxLv + 1
                    firstOut = False
                    for i in xrange(1, maxUse):
                        data = {}
                        data2 = EERD.data.get(i, {})
                        min = 0
                        max = 0
                        progressList = data2.get('enhEffects', 0)
                        colorDiv = int(data2.get('colorDiv', 0) * 100)
                        for it in progressList:
                            if it[0] > max:
                                max = it[0]
                            if it[0] < min or min == 0:
                                min = it[0]

                        min = int(min * 100)
                        max = int(max * 100)
                        if equipRefining.has_key(i):
                            value = round(equipRefining[i] * 100)
                            canClick = True
                            if value <= colorDiv:
                                color = '#FB0000'
                            elif int(value) == max:
                                color = '#79C725'
                            else:
                                color = '#e5c317'
                            data['refinePer'] = "<font color=\'%s\'>%d%%</font>" % (color, round(value))
                        else:
                            if firstOut == False:
                                color = '#FFFFE7'
                                firstOut = True
                            else:
                                color = '#808080'
                            data['refinePer'] = "<font color=\'%s\'>?%%</font>" % color
                            canClick = True
                        data['lvTxt'] = "<font color=\'%s\'>Lv%d</font>" % (color, i)
                        data['lv'] = i
                        data['refineRange'] = "<font color=\'%s\'>%d%%~%d%%</font>" % (color, min, max)
                        data['index'] = i
                        data['canClick'] = canClick
                        dataList.append(data)

                    ret = uiUtils.array2GfxAarry(dataList, True)
                    self.mediator.Invoke('setNowInfo', (ret, GfxValue(item.enhLv)))

    def toggle(self):
        if self.isShow == False:
            self.show()
        else:
            self.clearWidget()

    def refreshPanel(self, *args):
        self.refreshLvInfo()

    def selectItem(self, *args):
        index = int(args[3][0].GetNumber())
        gameglobal.rds.ui.equipEnhance.setNowRefineLv(index)
        gameglobal.rds.ui.equipEnhance.refreshContent()
