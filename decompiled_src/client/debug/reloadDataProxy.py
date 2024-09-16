#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/reloadDataProxy.o
import sys
import BigWorld
import cacheBDB
import copy
import gamelog
import game
import const
import gametypes
from guis import uiConst
from guis import events
from guis.uiProxy import UIProxy
from guis.asObject import ASObject
from helpers import charRes

class ReloadDataProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ReloadDataProxy, self).__init__(uiAdapter)
        self._resetData()
        uiAdapter.registerEscFunc(uiConst.WIDGET_RELOAD_DATA, self.hide)

    def _resetData(self):
        self.widget = None
        self.loadedDataName = ''
        self.loadedData = {}
        self.idData = {}
        self.dataName = ''
        self.id = 0
        self.propertyEditorList = []
        self.selectedProperty = ''
        self.cfg = None
        self.cfgIdx = -1
        self.cfgDataNameList = []

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self._initUI()
        self.refreshFrame()

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_RELOAD_DATA)

    def clearWidget(self):
        self._resetData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RELOAD_DATA)

    def refreshFrame(self):
        if not self.widget:
            return

    def _initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.onCloseClick, False, 0, True)
        self.widget.txtDataName.addEventListener(events.EVENT_CHANGE, self.onDataNameChange, False, 0, True)
        self.widget.importDataBtn.addEventListener(events.MOUSE_CLICK, self.onImportDataBtnClick, False, 0, True)
        self.widget.relaodBtn.addEventListener(events.MOUSE_CLICK, self.onReloadBtnClick, False, 0, True)
        self.widget.txtId.textField.restrict = '0-9'
        self.widget.txtId.addEventListener(events.EVENT_CHANGE, self.onTxtIdChange, False, 0, True)
        self.widget.chooseId.addEventListener(events.MOUSE_CLICK, self.onChooseIdClick, False, 0, True)
        self.widget.txtAddProperty.restrict = 'a-zA-Z0-9'
        self.widget.txtAddProperty.addEventListener(events.EVENT_CHANGE, self.onAddPropertyChange, False, 0, True)
        self.widget.addBtn.addEventListener(events.MOUSE_CLICK, self.onAddBtnClick, False, 0, True)
        self.widget.delBtn.addEventListener(events.MOUSE_CLICK, self.onDelBtnClick, False, 0, True)
        self.widget.scrollList.itemRenderer = 'ReloadData_ItemRender'
        self.widget.scrollList.lableFunction = self.labelFunction
        self.widget.saveChangeBtn.addEventListener(events.MOUSE_CLICK, self.onSaveChangeBtnClick, False, 0, True)

    def onReloadBtnClick(self, *args):
        game.reloadAllData()

    def onAddPropertyChange(self, *args):
        e = ASObject(args[3][0])
        self.selectedProperty = e.currentTarget.text

    def onSaveChangeBtnClick(self, *args):
        if not self.idData:
            return
        newData = copy.deepcopy(self.idData)
        for info in self.propertyEditorList:
            newValue = self.changeType(info['oldValue'], info['newValue'])
            newData[info['property']] = newValue
            self.changeTypeEx(info['property'], newValue)
            gamelog.info('@jbx:setProperty', type(info['oldValue']), self.id, info['property'], info['newValue'])

        data = {}
        data[self.id] = newData
        cacheBDB.hotfix_update(self.loadedData, data)
        BigWorld.player().reloadModel()

    def changeTypeEx(self, propertyName, newValue):
        gamelog.info('jbx:propertyName', propertyName, newValue)
        p = BigWorld.player()
        if self.dataName == 'equip_data':
            if propertyName == 'dyeList':
                for i in p.equipment:
                    if i == None:
                        continue
                    if getattr(i, 'id', 0) == self.id:
                        parts = i.whereEquip()
                        for part in parts:
                            self.changeDyeList(part, newValue)

                        return

    def changeDyeList(self, part, value):
        p = BigWorld.player()
        dyeList = list(value)
        gamelog.info('@jbx:oldDyeList', p.aspect.dyeLists[part])
        for index, item in enumerate(value):
            if index >= const.DYES_INDEX_COLOR and index < const.DYES_INDEX_TEXTURE or index >= const.DYES_INDEX_DUAL_COLOR and index < const.DYES_INDEX_PBR_TEXTURE_DEGREE:
                dyeList[index] = p.aspect.colorStr2Int(item)
            else:
                dyeList[index] = str(item)

        p.aspect.dyeLists[part] = dyeList
        gamelog.info('@jbx:newDyeList', p.aspect.dyeLists[part])

    def changeType(self, oldValue, newValue):
        if isinstance(oldValue, int):
            return int(newValue)
        elif isinstance(oldValue, float):
            return float(newValue)
        elif isinstance(oldValue, str):
            return newValue
        else:
            return eval(newValue)

    def onChooseIdClick(self, *args):
        if not self.loadedData:
            return
        self.idData = self.loadedData.get(self.id, {})
        self.propertyEditorList = []
        self.refreshScrollList()

    def refreshScrollList(self):
        self.widget.scrollList.dataArray = self.propertyEditorList
        self.widget.scrollList.validateNow()

    def labelFunction(self, *args):
        info = ASObject(args[3][0])
        mc = ASObject(args[3][1])
        mc.removeEventListener(events.EVENT_CHANGE, self.onNewValueChange)
        mc.txtOldValue.text = info.property
        mc.txtNewValue.validateNow()
        mc.txtNewValue.text = str(info.newValue)
        mc.name = str(int(info.dataIndex))
        mc.txtNewValue.addEventListener(events.EVENT_CHANGE, self.onNewValueChange, False, 0, True)

    def onNewValueChange(self, *args):
        currentTarget = ASObject(args[3][0]).currentTarget
        index = int(currentTarget.parent.name)
        newValue = currentTarget.text
        if index < len(self.propertyEditorList):
            self.propertyEditorList[index]['newValue'] = newValue

    def onDelBtnClick(self, *args):
        for info in self.propertyEditorList:
            if info['property'] == self.selectedProperty:
                self.propertyEditorList.remove(info)
                break

        self.refreshScrollList()

    def onAddBtnClick(self, *args):
        if not self.selectedProperty:
            return
        if not self.isContainedProperty(self.selectedProperty):
            info = {}
            info['dataIndex'] = len(self.propertyEditorList)
            info['property'] = self.selectedProperty
            info['oldValue'] = self.idData.get(self.selectedProperty, '')
            info['newValue'] = str(info['oldValue'])
            self.propertyEditorList.append(info)
        self.refreshScrollList()

    def isContainedProperty(self, propertyName):
        for _, info in enumerate(self.propertyEditorList):
            if info['property'] == propertyName:
                return True

        return False

    def onImportDataBtnClick(self, *args):
        self.importData(self.dataName)

    def importData(self, dataName):
        if self.loadedData:
            return
        moduleName = 'data.%s' % dataName
        if moduleName not in sys.modules:
            raise Exception('%s not exised' % moduleName)
        module = sys.modules['data.%s' % dataName]
        self.loadedData = module.data

    def onTxtIdChange(self, *args):
        e = ASObject(args[3][0])
        text = e.currentTarget.textField.text
        self.id = int(text) if text else 0

    def onDataNameChange(self, *args):
        e = ASObject(args[3][0])
        self.dataName = e.currentTarget.text

    def onCloseClick(self, *args):
        self.hide()
