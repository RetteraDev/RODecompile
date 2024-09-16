#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipEnhanceResultProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import itemToolTipUtils
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from data import prop_ref_data as PRD

class EquipEnhanceResultProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipEnhanceResultProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.closeWidget,
         'refreshPanel': self.refreshPanel}
        self.type = 'equipEnhanceResult'
        self.bindType = 'equipEnhanceResult'
        self.mediator = None
        self.isShow = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_ENHANCE_RESULT, self.clearWidget)

    def closeWidget(self, *args):
        self.clearWidget()

    def clearWidget(self):
        self.mediator = None
        self.isShow = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_ENHANCE_RESULT)

    def show(self):
        if not self.isShow:
            self.isShow = True
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_ENHANCE_RESULT, True)
        else:
            self.refreshResultInfo()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_ENHANCE_RESULT:
            self.mediator = mediator

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[12:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'equipEResult%d.slot%d' % (bar, slot)

    def refreshResultInfo(self):
        nowItem = gameglobal.rds.ui.equipEnhance.getEnhanceItem()
        preItem = gameglobal.rds.ui.equipEnhance.enhanceBeforeItem
        if not nowItem:
            pagePos = gameglobal.rds.ui.equipEnhance.enhanceBeforeItemPos
            nowItem = BigWorld.player().inv.getQuickVal(pagePos[0], pagePos[1])
        key = self._getKey(0, 0)
        self.bindingData[key] = preItem
        key = self._getKey(0, 1)
        self.bindingData[key] = nowItem
        preLv = getattr(preItem, 'enhLv', 0)
        nowLv = getattr(nowItem, 'enhLv', 0)
        isUpdate = False
        targetLv = nowLv
        if preLv < nowLv:
            isUpdate = True
            gameglobal.rds.ui.equipEnhance.updateItemAfterEnhance(nowItem)
        else:
            preLv = gameglobal.rds.ui.equipEnhance.enhanceTargetLv
            targetLv = gameglobal.rds.ui.equipEnhance.enhanceTargetLv
            gameglobal.rds.ui.equipEnhance.updateItemAfterEnhance(nowItem, False)
        if isUpdate == False:
            fromEnhanceProgress = round(getattr(preItem, 'enhanceRefining', {}).get(targetLv, 0) * 100)
        else:
            fromEnhanceProgress = 0
        toEnhanceProgress = round(getattr(nowItem, 'enhanceRefining', {}).get(targetLv, 0) * 100)
        fromEnhanceRefining = getattr(preItem, 'enhanceRefining', {})
        toEnhanceRefining = getattr(nowItem, 'enhanceRefining', {})
        totalFrom = 0
        for key in fromEnhanceRefining:
            totalFrom += round(fromEnhanceRefining[key] * 100)

        totalTo = 0
        for key in toEnhanceRefining:
            totalTo += round(toEnhanceRefining[key] * 100)

        color = uiUtils.getItemColorByItem(preItem)
        preIconPath = uiUtils.getItemIconFile64(preItem.id)
        preData = {'iconPath': preIconPath,
         'color': color}
        nowIconPath = uiUtils.getItemIconFile64(preItem.id)
        nowData = {'iconPath': nowIconPath,
         'color': color}
        str2 = ''
        contentStrList = []
        if isUpdate == False:
            contentStrList.append([gameStrings.TEXT_EQUIPENHANCERESULTPROXY_107, '+%d%%' % fromEnhanceProgress, "<font color=\'#79C725\'>+%d%%</font>" % toEnhanceProgress])
        else:
            preJueXingData = getattr(preItem, 'enhJuexingData', {})
            nowJueXingData = getattr(nowItem, 'enhJuexingData', {})
            if len(preJueXingData) < len(nowJueXingData):
                for key in nowJueXingData:
                    if key not in preJueXingData:
                        juexingDataList = nowJueXingData[key]
                        basicProp = ''
                        for juexingData in juexingDataList:
                            info = PRD.data[juexingData[0]]
                            jueXingNum = juexingData[2]
                            if juexingData[0] in itemToolTipUtils.PROPS_SHOW_SHRINK:
                                jueXingNum = round(juexingData[2] / 100.0, 1)
                            basicProp += info['name'] + '  '
                            if info['showType'] == 0:
                                basicProp += str(itemToolTipUtils.float2Int(jueXingNum))
                            elif info['showType'] == 2:
                                basicProp += str(round(jueXingNum, 1))
                            else:
                                basicProp += str(round(jueXingNum * 100, 1)) + '%'
                            basicProp += '\n'

                        if basicProp:
                            str2 += "<font color= \'#79C725\'>" + basicProp + '</font>'

            enhList = [None, None]
            _, _, enhList[0], _, _ = itemToolTipUtils.calAttrVal(preItem)
            _, _, enhList[1], _, _ = itemToolTipUtils.calAttrVal(nowItem)
            contentList = {}
            for i in xrange(0, 2):
                for item in enhList[i]:
                    if not contentList.has_key(item[0]):
                        contentList[item[0]] = [(item[0], 3, 0), (item[0], 3, 0)]
                    contentList[item[0]][i] = item

            contentStrList = []
            content = ''
            contentTo = ''
            title = ''
            for key in contentList:
                if key == 118 and contentList.has_key(119):
                    content = '+%d-%d(+%d%%)' % (contentList[118][0][2], contentList[119][0][2], totalFrom)
                    title = gameStrings.TEXT_EQUIPENHANCERESULTPROXY_157
                    contentTo = "<font color = \'#79C725\'>+%d-%d(+%d%%)</font>" % (contentList[118][1][2], contentList[119][1][2], totalTo)
                elif key == 120 and contentList.has_key(121):
                    content = '+%d-%d(+%d%%)' % (contentList[120][0][2], contentList[121][0][2], totalFrom)
                    title = gameStrings.TEXT_EQUIPCHANGESTARLVUPPROXY_324
                    contentTo = "<font color = \'#79C725\'>+%d-%d(+%d%%)</font>" % (contentList[120][1][2], contentList[121][1][2], totalTo)

            if content != '':
                contentStrList.append([title, content, contentTo])
            for key in contentList:
                content = ''
                contentTo = ''
                if key not in (118, 119, 120, 121):
                    info = PRD.data[key]
                    title = info['name'] + '   '
                    typeUse = ''
                    if info['type'] == 2:
                        typeUse += '+'
                    elif info['type'] == 1:
                        typeUse += '-'
                    if info['showType'] == 0:
                        enhProp = str(itemToolTipUtils.float2Int(contentList[key][0][2]))
                        enhProp1 = str(itemToolTipUtils.float2Int(contentList[key][1][2]))
                        content = '%s%s(+%d%%)' % (typeUse, enhProp, totalFrom)
                        contentTo = "<font color = \'#79C725\'>%s%s(+%d%%)</font>" % (typeUse, enhProp1, totalTo)
                    elif info['showType'] == 2:
                        enhProp = str(round(contentList[key][0][2], 1))
                        enhProp1 = str(round(contentList[key][1][2], 1))
                        content = '%s%s(+%d%%)' % (typeUse, enhProp, totalFrom)
                        contentTo = "<font color = \'#79C725\'>%s%s(+%d%%)</font>" % (typeUse, enhProp1, totalTo)
                    else:
                        enhProp = str(round(contentList[key][0][2] * 100, 1))
                        enhProp1 = str(round(contentList[key][1][2] * 100, 1))
                        content = "%s%s%%   <font color = \'#79C725\'>%s%s%%(+%d%%)</font>" % (typeUse, enhProp, totalFrom)
                        contentTo = "<font color = \'#79C725\'>%s%s%%(+%d%%)</font>" % (typeUse, enhProp1, totalTo)
                    if content:
                        contentStrList.append([title, content, contentTo])

        inputDict = {'fromLv': preLv,
         'toLv': targetLv,
         'fromItem': preData,
         'toItem': nowData,
         'result1': contentStrList,
         'result3': str2}
        if self.mediator != None:
            self.mediator.Invoke('setInfo', uiUtils.dict2GfxDict(inputDict, True))

    def toggle(self):
        if self.isShow == False:
            self.show()
        else:
            self.clearWidget()

    def refreshPanel(self, *args):
        self.refreshResultInfo()

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')
