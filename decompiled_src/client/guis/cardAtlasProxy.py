#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardAtlasProxy.o
import BigWorld
import events
import gameglobal
import uiConst
import uiUtils
from asObject import ASUtils
from asObject import ASObject
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import card_atlas_data as CAD
from data import prop_ref_data as PRD
DROP_DOWN_ROW_MAX = 5
PROP_HEIGHT = 25
NORMAL_FONT_SIZE = 12
MIN_FONT_SIZE = 11

class CardAtlasProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardAtlasProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CARD_ATLAS, self.hide)

    def reset(self):
        self.verAtlasData = []
        self.allAtlasPropDict = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CARD_ATLAS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CARD_ATLAS)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CARD_ATLAS)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.setMenu()
        self.widget.leftList.column = 3
        self.widget.leftList.itemHeight = 157
        self.widget.leftList.itemWidth = 180
        self.widget.leftList.itemRenderer = 'CardAtlas_ListItem'
        self.widget.leftList.labelFunction = self.leftListFunction
        self.widget.leftList.dataArray = []
        self.setLeftList()
        self.widget.rightList.itemHeight = 25
        self.widget.rightList.itemWidth = 150
        self.widget.rightList.itemRenderer = 'CardAtlas_PropertyItem'
        self.widget.rightList.labelFunction = self.rightListFunction
        self.widget.rightList.dataArray = []
        self.setRightList()
        self.widget.hideFullAtlasBox.addEventListener(events.EVENT_SELECT, self.handleHideFullAtlasBoxSelected, False, 0, True)

    def setLeftList(self):
        if not self.hasBaseData():
            return
        dataList = self.getLeftListData()
        self.widget.leftList.dataArray = dataList
        self.widget.leftList.validateNow()

    def getLeftListData(self):
        vaData = self.uiAdapter.cardSystem.getVersionAtlasData()
        self.verAtlasData = vaData
        lData = []
        propType = 0
        pMenu = getattr(self.widget, 'propMenu', None)
        if pMenu and self.uiAdapter.cardSystem.propMenuData:
            propType = self.uiAdapter.cardSystem.propMenuData[pMenu.selectedIndex].get('data', '')
        ver = 0
        vMenu = getattr(self.widget, 'versionMenu', None)
        if vMenu and self.uiAdapter.cardSystem.versionMenuData:
            ver = self.uiAdapter.cardSystem.versionMenuData[vMenu.selectedIndex].get('data', '')
        for k, v in CAD.data.iteritems():
            if ver and k != ver:
                continue
            pType = self.verAtlasData.get(k, {}).get('propType', 0)
            if propType and pType != propType:
                continue
            activedNum = self.uiAdapter.cardSystem.getAtlasActivedNumData(k)
            conMax = self.uiAdapter.cardSystem.getAtlasConMax(k)
            if self.widget.hideFullAtlasBox.selected and activedNum >= conMax:
                continue
            lData.append(k)

        return lData

    def leftListFunction(self, *arg):
        verId = int(arg[3][0].GetNumber())
        itemMc = ASObject(arg[3][1])
        if itemMc and verId:
            name = CAD.data.get(verId, {}).get('version', '')
            itemMc.nameTxt.text = gameStrings.CARD_ATLAS_COLON % (name,)
            activedNum = self.uiAdapter.cardSystem.getAtlasActivedNumData(verId)
            conMax = self.uiAdapter.cardSystem.getAtlasConMax(verId)
            numStr = uiUtils.convertNumStr(activedNum, conMax, enoughColor='', notEnoughColor='')
            itemMc.numTxt.text = numStr
            propArr = []
            atlasData = CAD.data.get(verId, {})
            for num in xrange(1, uiConst.CARD_ATLAS_PROP_NUM_MAX):
                cond = atlasData.get('cond' + str(num), 0)
                if cond:
                    pArr = atlasData.get('prop' + str(num), ((0, 0),))
                    pDesc = atlasData.get('propdec' + str(num), '')
                    for propId, propVal in pArr:
                        pItem = ((propId,
                          propVal,
                          cond,
                          pDesc),)
                        propArr += pItem
                        if pDesc:
                            break

            self.widget.removeAllInst(itemMc.canvas)
            for i, (propId, propVal, cond, pDesc) in enumerate(propArr):
                pText = ''
                if not pDesc:
                    propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal, 'shortName')
                    pText = self.uiAdapter.cardSystem.formatPropStr(propertyName, propVal, separator='', titleColor=uiConst.CARD_PROP_PRE_COLOR, valColor=uiConst.CARD_PROP_SUF_COLOR)
                else:
                    pText = pDesc
                pText = gameStrings.CARD_ATLAS_NUM % (cond,) + pText
                propItem = self.widget.getInstByClsName('CardAtlas_PropertyItem')
                propItem.contentTxt.htmlText = pText
                ASUtils.autoSizeWithFont(propItem.contentTxt, NORMAL_FONT_SIZE, propItem.contentTxt.width, MIN_FONT_SIZE)
                propItem.y = i * PROP_HEIGHT
                if activedNum < cond:
                    ASUtils.setMcEffect(propItem, 'gray')
                else:
                    ASUtils.setMcEffect(propItem, '')
                itemMc.canvas.addChild(propItem)

    def setRightList(self):
        if not self.hasBaseData():
            return
        dataList = self.getRightListData()
        self.widget.rightList.dataArray = dataList
        self.widget.rightList.validateNow()

    def getRightListData(self):
        self.allAtlasPropDict, curAtlasPropDict = self.uiAdapter.cardSystem.getAllAtlasProp()
        return self.allAtlasPropDict.keys()

    def rightListFunction(self, *arg):
        propId = int(arg[3][0].GetNumber())
        itemMc = ASObject(arg[3][1])
        if itemMc and propId:
            propVal = self.allAtlasPropDict.get(propId, 0)
            propertyName, propVal = self.uiAdapter.cardSystem.transPropVal(propId, propVal, 'shortName')
            pText = self.uiAdapter.cardSystem.formatPropStr(propertyName, propVal, separator='', titleColor=uiConst.CARD_PROP_PRE_COLOR, valColor=uiConst.CARD_PROP_SUF_COLOR)
            itemMc.contentTxt.htmlText = pText

    def refreshInfo(self):
        if not self.widget:
            return

    def setMenu(self):
        pMenu = getattr(self.widget, 'propMenu', None)
        if pMenu:
            ASUtils.setDropdownMenuData(pMenu, self.uiAdapter.cardSystem.propMenuData)
            pMenu.selectedIndex = 0
            pMenu.menuRowCount = min(len(self.uiAdapter.cardSystem.propMenuData), DROP_DOWN_ROW_MAX)
            pMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handlePropMenuItemSelected, False, 0, True)
        vMenu = getattr(self.widget, 'versionMenu', None)
        if vMenu:
            ASUtils.setDropdownMenuData(vMenu, self.uiAdapter.cardSystem.versionMenuData)
            vMenu.selectedIndex = 0
            vMenu.menuRowCount = min(len(self.uiAdapter.cardSystem.versionMenuData), DROP_DOWN_ROW_MAX)
            vMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleVersionMenuItemSelected, False, 0, True)

    def handlePropMenuItemSelected(self, *args):
        if not self.hasBaseData():
            return
        self.setLeftList()

    def handleVersionMenuItemSelected(self, *args):
        if not self.hasBaseData():
            return
        self.setLeftList()

    def handleHideFullAtlasBoxSelected(self, *args):
        if not self.hasBaseData():
            return
        self.setLeftList()

    def hasBaseData(self):
        if not self.widget:
            return False
        return True
