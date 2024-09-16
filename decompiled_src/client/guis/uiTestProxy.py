#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/uiTestProxy.o
import BigWorld
import uiConst
import events
import gameglobal
import utils
import clientUtils
import gamelog
from gamestrings import gameStrings
from uiProxy import UIProxy
from xml.dom.minidom import Document
from asObject import ASObject
from guis.asObject import ASUtils
from guis import uiUtils
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import quizzes_config_data as QCD
NORMAL_ATTRIBUTE_LIST = [{'label': 'alpha'},
 {'label': 'height'},
 {'label': 'width'},
 {'label': 'x'},
 {'label': 'y'},
 {'label': 'visible'}]
TEXT_ATTRIBUTE_LIST = [{'label': 'text'},
 {'label': 'textColor'},
 {'label': 'textWidth'},
 {'label': 'textWidth'},
 {'label': 'type'},
 {'label': 'wordWrap'},
 {'label': 'maxChars'}]
FORMAT_ATTRIBUTE_LIST = [{'label': 'align'},
 {'label': 'bold'},
 {'label': 'italic'},
 {'label': 'font'},
 {'label': 'size'},
 {'label': 'leading'},
 {'label': 'leftMargin'},
 {'label': 'rightMargin'},
 {'label': 'underline'},
 {'label': 'multiline'}]

class UiTestProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(UiTestProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_UI_TEST, self.hide)

    def reset(self):
        self.widget = None
        self.chooseWidget = None
        self.widgetList = []
        self.menuList = []
        self.curItem = None
        self.graphics = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_UI_TEST:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_UI_TEST)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_UI_TEST)
        else:
            self.initUI()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.widgetConfirmBtn.addEventListener(events.BUTTON_CLICK, self.handleWidgetBtnClick, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.graphics = self.widget.graphics

    def refreshInfo(self):
        self.clearItem(0)
        self.widget.itemChoose.menu0.selectedIndex = -1
        self.widget.attributeMenu.selectedIndex = -1
        self.widget.attriInput.text = ''
        self.widget.attriChoose.selectedIndex = -1

    def handleWidgetBtnClick(self, *args):
        self.refreshInfo()
        wid = self.widget.widgetInput.text
        self.chooseWidget = gameglobal.rds.ui.getWidgetByID(int(wid))
        numChildren = self.chooseWidget.numChildren
        menuList = []
        itemList = []
        if numChildren:
            for i in xrange(numChildren):
                item = self.chooseWidget.getChildAt(i)
                itemClass = item.constructor.toString()[7:-1]
                if itemClass != 'Shape':
                    itemLabel = {'label': item.name}
                    menuList.append(itemLabel)
                    itemList.append(item)

        gamelog.debug('yedawang### handleWidgetBtnClick wid widget', wid, menuList)
        ASUtils.setDropdownMenuData(self.widget.itemChoose.menu0, menuList)
        self.widget.itemChoose.menu0.level = 0
        self.widget.itemChoose.menu0.itemList = itemList
        self.widget.itemChoose.menu0.addEventListener(events.INDEX_CHANGE, self.handleItemMenu)

    def clearItem(self, level):
        if self.widget:
            for menu in self.menuList[level:]:
                self.widget.itemChoose.removeChild(menu)
                self.menuList.remove(menu)

    def clearAttri(self):
        self.widget.attributeMenu.selectedIndex = -1
        self.widget.attriInput.text = ''

    def handleItemMenu(self, *args):
        level = ASObject(args[3][0]).currentTarget.level
        selectedIndex = ASObject(args[3][0]).currentTarget.selectedIndex
        selectedItem = ASObject(args[3][0]).currentTarget.itemList[selectedIndex]
        self.curItem = selectedItem
        if selectedIndex == -1:
            return
        self.clearItem(level)
        numChildren = selectedItem.numChildren
        gamelog.debug('yedawang### handleItemMenu0 selectedIndex level', selectedIndex, level, selectedItem.name, numChildren)
        if numChildren:
            menuList = []
            itemList = []
            for i in xrange(numChildren):
                item = selectedItem.getChildAt(i)
                itemClass = item.constructor.toString()[7:-1]
                if itemClass != 'Shape':
                    itemLabel = {'label': item.name}
                    menuList.append(itemLabel)
                    itemList.append(item)

            if menuList and itemList:
                menu = self.widget.getInstByClsName('UITest_DefaultDropdownMenu')
                ASUtils.setDropdownMenuData(menu, menuList)
                menu.level = level + 1
                menu.itemList = itemList
                menu.y = 30 + level * 30
                menu.dropdown = 'M12_DefaultScrollingList'
                menu.itemRenderer = 'M12_DefaultListItemRenderer'
                menu.scrollBar = 'M12_DefaultScrollBar'
                menu.addEventListener(events.INDEX_CHANGE, self.handleItemMenu)
                self.widget.itemChoose.addChild(menu)
                self.menuList.append(menu)
        if self.graphics:
            self.graphics.clear()
        itemClass = selectedItem.constructor.toString()[7:-1]
        self.widget.itemType.text = itemClass
        if itemClass != 'Shape':
            self.graphics.beginFill(26316, 0.6)
            x, y = self.getItemLocation(selectedItem)
            self.graphics.drawRect(x, y, selectedItem.width, selectedItem.height)
            self.graphics.endFill()
        self.clearAttri()
        attrLabelList = self.genAttrList(selectedItem)
        attrList = []
        for label in attrLabelList:
            attrList.append(label['label'])

        gamelog.debug('yedawang### attrilist', attrList)
        self.widget.attributeMenu.selectedItem = selectedItem
        self.widget.attributeMenu.attributeList = attrList
        ASUtils.setDropdownMenuData(self.widget.attributeMenu, attrLabelList)
        self.widget.attributeMenu.addEventListener(events.INDEX_CHANGE, self.handleAttributeMenu)

    def getItemLocation(self, item):
        x = item.x
        y = item.y
        while item.parent:
            x += item.parent.x
            y += item.parent.y
            item = item.parent

        gamelog.debug('yedawang### x y', x, y)
        return (x, y)

    def genAttrList(self, item):
        attrLabelList = NORMAL_ATTRIBUTE_LIST
        cls = item.constructor.toString()[7:-1]
        if cls == 'TextField':
            attrLabelList += TEXT_ATTRIBUTE_LIST
            textFormat = item.getTextFormat()
            if textFormat:
                attrLabelList += FORMAT_ATTRIBUTE_LIST
                if item.multiline:
                    attrLabelList.append({'label': 'numLines'})
        gamelog.debug('yedawang### attrLabelList', attrLabelList)
        return attrLabelList

    def genWidgetDict(self, parent):
        numChildren = parent.numChildren
        name = parent.name
        childrenList = []
        for i in xrange(numChildren):
            item = parent.getChildAt(i)
            childrenList.append(self.getDisplayObjAttr(item))
            self.genWidgetDict(item)

        self.widgetList.append(self.genWidgetDict(parent.getChildAt(i)))

    def handleAttributeMenu(self, *args):
        selectedIndex = ASObject(args[3][0]).currentTarget.selectedIndex
        selectedItem = ASObject(args[3][0]).currentTarget.selectedItem
        selectedAttri = ASObject(args[3][0]).currentTarget.attributeList[selectedIndex]
        if selectedIndex == -1:
            return
        else:
            self.widget.attriInput.text = getattr(selectedItem, selectedAttri, None)
            self.widget.attriConfirmBtn.data = [selectedItem, selectedAttri]
            self.widget.attriConfirmBtn.addEventListener(events.BUTTON_CLICK, self.handleAttriBtnClick, False, 0, True)
            return

    def handleAttriBtnClick(self, *args):
        item = ASObject(args[3][0]).currentTarget.data[0]
        attribute = ASObject(args[3][0]).currentTarget.data[1]
        gamelog.debug('yedawang### item attribute', item, attribute)
        value = self.widget.attriInput.text
        setattr(item, attribute, value)
        self.graphics.clear()
        self.graphics.beginFill(26316, 0.6)
        x, y = self.getItemLocation(item)
        self.graphics.drawRect(x, y, item.width, item.height)
        self.graphics.endFill()

    def handleConfirmBtnClick(self, *args):
        widget = self.chooseWidget
        numChildren = widget.numChildren
        flaDoc = {}
        flaDoc['path'] = widget.root.loaderInfo.url
        flaDoc['alpha'] = widget.alpha
        flaDoc['height'] = widget.height
        flaDoc['width'] = widget.width
        flaDoc['name'] = widget.name
        flaDoc['visible'] = widget.visible
        flaDoc['x'] = widget.x
        flaDoc['y'] = widget.y
        flaDoc['class'] = widget.constructor.toString()[7:-1]
        elementList = []
        for i in xrange(numChildren):
            elementList.append(self.getDisplayObjAttr(widget.getChildAt(i)))

        flaDoc['elementList'] = elementList
        self.outputXML(flaDoc)

    def getDisplayObjAttr(self, obj):
        element = {}
        element['path'] = obj.root.loaderInfo.url
        element['alpha'] = obj.alpha
        element['height'] = obj.height
        element['width'] = obj.width
        element['name'] = obj.name
        element['visible'] = obj.visible
        element['x'] = obj.x
        element['y'] = obj.y
        element['class'] = obj.constructor.toString()[7:-1]
        if element['class'] == 'TextField' and obj.length:
            element['length'] = obj.length
            element['text'] = obj.text
            element['textHeight'] = obj.textHeight
            element['textWidth'] = obj.textWidth
            element['textColor'] = hex(obj.textColor)
            element['type'] = obj.type
            element['wordWrap'] = obj.wordWrap
            element['maxChars'] = obj.maxChars
            textFormat = obj.getTextFormat()
            if textFormat:
                element['align'] = textFormat.align
                element['bold'] = textFormat.bold
                element['italic'] = textFormat.italic
                element['font'] = textFormat.font
                element['size'] = textFormat.size
                element['indent'] = textFormat.indent
                element['leading'] = textFormat.leading
                element['leftMargin'] = textFormat.leftMargin
                element['rightMargin'] = textFormat.rightMargin
                element['underline'] = textFormat.underline
            element['multiline'] = obj.multiline
            if obj.multiline:
                element['numLines'] = obj.numLines
        if obj.numChildren:
            elementList = []
            for i in xrange(obj.numChildren):
                elementList.append(self.getDisplayObjAttr(obj.getChildAt(i)))

            element['elementList'] = elementList
        return element

    def outputXML(self, widget):
        doc = Document()
        root = doc.createElement('widget')
        doc.appendChild(root)
        for attr, value in widget.iteritems():
            if attr != 'elementList':
                gamelog.debug('yedawang### attr,value', attr, value)
                if value:
                    a = doc.createElement(attr)
                    v = doc.createTextNode(str(value))
                    a.appendChild(v)
                    root.appendChild(a)
            else:
                self.handleElementList(doc, value, root)

        f = open('E:\\pangu-res\\code\\entities\\client\\guieditor\\output.xml', 'w')
        doc.writexml(f, indent='	', newl='\n', addindent='	', encoding='utf-8')
        f.write(doc.toprettyxml(encoding='utf-8'))
        f.close()

    def handleElementList(self, doc, elementList, parent):
        elements = doc.createElement('children')
        for i in xrange(len(elementList)):
            element = doc.createElement('element')
            element.setAttribute('name', elementList[i]['name'])
            for elementAttr, elementVal in elementList[i].iteritems():
                if elementAttr != 'name':
                    if elementAttr == 'elementList':
                        self.handleElementList(doc, elementVal, element)
                    elif elementVal:
                        a = doc.createElement(elementAttr)
                        v = doc.createTextNode(str(elementVal))
                        a.appendChild(v)
                        element.appendChild(a)

            elements.appendChild(element)

        parent.appendChild(elements)

    def getTabStr(self, level):
        s = ''
        while level > 0:
            s += '	'
            level -= 1

        return s
