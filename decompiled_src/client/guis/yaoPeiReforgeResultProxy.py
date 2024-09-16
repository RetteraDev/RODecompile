#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yaoPeiReforgeResultProxy.o
import gameglobal
import uiConst
import uiUtils
from uiProxy import SlotDataProxy
from data import prop_ref_data as PRD
from cdata import game_msg_def_data as GMDD

class YaoPeiReforgeResultProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(YaoPeiReforgeResultProxy, self).__init__(uiAdapter)
        self.bindType = 'yaoPeiReforgeResult'
        self.type = 'yaoPeiReforgeResult'
        self.modelMap = {}
        self.mediator = None
        self.item = None
        self.idx = 0
        self.oldVal = 0
        self.newVal = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_YAOPEI_REFORGE_RESULT, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_YAOPEI_REFORGE_RESULT:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YAOPEI_REFORGE_RESULT)

    def reset(self):
        self.item = None
        self.idx = 0
        self.oldVal = 0
        self.newVal = 0

    def show(self, item, idx, oldVal, newVal):
        if not item:
            return
        self.item = item
        self.idx = idx
        self.oldVal = oldVal
        self.newVal = newVal
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YAOPEI_REFORGE_RESULT)

    def refreshInfo(self):
        if self.mediator:
            info = {}
            info['itemInfo'] = uiUtils.getGfxItem(self.item)
            extraPropList = []
            maxActivatedLv = self.item.calcMaxYaoPeiLv()
            yaoPeiLv = self.item.getYaoPeiLv()
            idx = 0
            for prop in self.item.yaoPeiExtraProps:
                propInfo = {}
                propText, formatEqual = self.createPropText(prop[0], prop[1], prop[2], prop[3], prop[4], prop[5] <= maxActivatedLv, idx == self.idx)
                if idx == self.idx:
                    propText = uiUtils.toHtml(propText, '#E5C317')
                elif prop[5] <= yaoPeiLv:
                    propText = uiUtils.toHtml(propText, '#FFFFE7')
                else:
                    propText = uiUtils.toHtml(propText, '#808080')
                propInfo['propText'] = propText
                if idx == self.idx:
                    if formatEqual:
                        propInfo['valueFlag'] = ''
                        hint = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_REFORGE_RESULT_EQUAL_HINT, '')
                    elif self.oldVal < self.newVal:
                        propInfo['valueFlag'] = 'up'
                        hint = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_REFORGE_RESULT_UP_HINT, '')
                    elif self.oldVal > self.newVal:
                        propInfo['valueFlag'] = 'down'
                        hint = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_REFORGE_RESULT_DOWN_HINT, '')
                    else:
                        propInfo['valueFlag'] = ''
                        hint = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_REFORGE_RESULT_EQUAL_HINT, '')
                    info['hint'] = hint
                else:
                    propInfo['valueFlag'] = ''
                extraPropList.append(propInfo)
                idx += 1

            info['extraPropList'] = extraPropList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def createPropText(self, pId, pType, pVal, minVal, maxVal, activated, selected):
        prd = PRD.data.get(pId, {})
        propName = prd.get('name', '')
        showType = prd.get('showType', 0)
        pVal = uiUtils.formatProp(pVal, pType, showType)
        minVal = uiUtils.formatProp(minVal, pType, showType)
        maxVal = uiUtils.formatProp(maxVal, pType, showType)
        formatEqual = False
        if selected:
            if self.oldVal <= self.newVal:
                changeVal = self.newVal - self.oldVal
                formatVal = uiUtils.formatProp(changeVal, pType, showType)
                changeText = uiUtils.toHtml('+' + formatVal, '#79C725')
            else:
                changeVal = self.oldVal - self.newVal
                formatVal = uiUtils.formatProp(changeVal, pType, showType)
                changeText = uiUtils.toHtml('-' + formatVal, '#F43804')
            if formatVal == '0' or formatVal == '0.0%' or formatVal == '0.0':
                formatEqual = True
                changeText = uiUtils.toHtml('+' + formatVal, '#79C725')
            text = '%s +%s (%s-%s) %s ' % (propName,
             pVal,
             minVal,
             maxVal,
             changeText)
        elif activated:
            text = '%s +%s (%s-%s)' % (propName,
             pVal,
             minVal,
             maxVal)
        else:
            text = '%s + (%s-%s)' % (propName, minVal, maxVal)
        return (text, formatEqual)

    def onGetToolTip(self, *arg):
        return gameglobal.rds.ui.inventory.GfxToolTip(self.item)
