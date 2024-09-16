#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/uiProxy.o
import weakref
import gameglobal
from guis import uiConst
from guis import ui
from guis.asObject import ASObject
from data import ui_location_data as ULD

class UIProxy(object):

    def __init__(self, uiAdapter):
        self.uiAdapter = weakref.proxy(uiAdapter)
        self.movie = uiAdapter.movie
        self.uiAdapter.proxies.append(weakref.proxy(self))
        self.modelMap = {}
        self.destroyOnHide = True
        self.basicFunMap = {'onRegister': self.onASMediatorRegister,
         'onClose': self.onASWidgetClose,
         'onRemove': self.onASMediatorRemoved}
        self.interestEvents = []
        self.widEvents = {}

    def initDataModel(self, dataModel, whichModel):
        try:
            useWeakref = gameglobal.rds.configData.get('useWeakrefUIInterface', False)
            if not useWeakref:
                for key in self.modelMap.keys():
                    try:
                        if dataModel.GetMember(key):
                            dataModel.SetMember(key, self.movie.CreateFunction(self.modelMap[key]))
                    except:
                        continue

                for key in self.basicFunMap.keys():
                    if dataModel.GetMember(key):
                        dataModel.SetMember(key, self.movie.CreateFunction(self.basicFunMap[key]))

            else:
                for key in self.modelMap.keys():
                    try:
                        if dataModel.GetMember(key):
                            dataModel.SetMember(key, self.movie.CreateFunction(weakref.proxy(self.modelMap[key])))
                    except:
                        continue

                for key in self.basicFunMap.keys():
                    if dataModel.GetMember(key):
                        dataModel.SetMember(key, self.movie.CreateFunction(weakref.proxy(self.basicFunMap[key])))

        except:
            print 'hjx avatar error#dataModel:', whichModel, key

    def clear(self):
        for k in dir(self):
            val = getattr(self, k)
            if val.__class__.__name__ == 'GfxValue':
                setattr(self, k, None)

    def __del__(self):
        pass

    def fini(self):
        del self.basicFunMap
        del self.modelMap
        del self

    def onASMediatorRegister(self, *arg):
        wid = int(arg[3][0].GetNumber())
        self._initWidEvents(wid)
        isWidgetEx = arg[3][2].GetBool()
        if isWidgetEx:
            widget = ASObject(arg[3][3])
            self.commonPreProcess(wid, widget)
            return self._registerASWidget(wid, widget)
        else:
            return self._registerMediator(wid, arg[3][1])

    def commonPreProcess(self, widgetId, widget):
        if widget.helpIcon and ULD.data.get(widgetId, {}).get('helpKey', 0):
            widget.helpIcon.helpKey = ULD.data[widgetId]['helpKey']

    def onASWidgetClose(self, *arg):
        widgetId = arg[3][0].GetNumber()
        multiID = arg[3][1].GetNumber()
        closedBySys = arg[3][2].GetBool()
        self._beforeWidgetClose(widgetId, multiID, closedBySys)
        self._asWidgetClose(widgetId, multiID)

    def onASMediatorRemoved(self, *arg):
        widgetId = arg[3][0].GetNumber()
        if widgetId in self.widEvents.keys():
            events = self.widEvents.get(widgetId, [])
            for event, call in events:
                self.delEvent(event, call)

            self.widEvents.pop(widgetId)

    def _registerMediator(self, widgetId, mediator):
        pass

    def _registerASWidget(self, widgetId, widget):
        pass

    def _beforeWidgetClose(self, widgetId, multiID, closedBySys):
        if widgetId in uiConst.SAVE_WIDGET_STATE_AFTER_CLOSE and not closedBySys:
            pos = self.uiAdapter.getWidgetPos(widgetId)
            self.uiAdapter.saveWidgetState(widgetId, pos)

    def _asWidgetClose(self, widgetId, multiID):
        self.hide(self.destroyOnHide)

    def _initWidEvents(self, wid):
        events = ui.widEvent.get(wid, [])
        for e, funcModule, funcName, p in events:
            if funcModule == self.__module__ and getattr(self, funcName):
                self.addEventToWidget(wid, e, getattr(self, funcName), p)

    def _delWidEvents(self, wid):
        if wid in self.widEvents.keys():
            for event, func in self.widEvents.get(wid, []):
                self.delEvent(event, func)

            self.widEvents.pop(wid)

    def show(self, *args):
        pass

    def hide(self, destroy = True):
        self.clearWidget()
        if destroy:
            self.delAllEvent()
            self.reset()

    def clearWidget(self):
        pass

    def reset(self):
        pass

    def clearAll(self):
        pass

    def addEvent(self, event, call, priority = 0, isGlobal = False):
        self.uiAdapter.addEvent(event, call, priority)
        if not isGlobal and (event, call) not in self.interestEvents:
            self.interestEvents.append((event, call))

    def delEvent(self, event, call):
        if (event, call) in self.interestEvents:
            self.interestEvents.remove((event, call))
        self.uiAdapter.delEvent(event, call)

    def delAllEvent(self, filters = []):
        for event, call in self.interestEvents:
            if event not in filters:
                self.uiAdapter.delEvent(event, call)

        self.interestEvents = []
        self.widEvents = {}

    def dispatchEvent(self, event, data = None):
        self.uiAdapter.dispatchEvent(event, data)

    def addEventToWidget(self, wid, event, call, priority = 0):
        self.addEvent(event, call, priority)
        self.widEvents.setdefault(wid, []).append((event, call))

    def runTestCase(self, funcName = '', args = None):
        moduleName = self.__class__.__name__[:-5]
        className = moduleName + 'TestCase'
        fileName = className[0].lower() + className[1:]
        module = __import__('tests.guis.' + fileName, fromlist=[className])
        testCaseObj = getattr(module, className)()
        if funcName == '':
            testCaseObj.run()
        else:
            func = getattr(testCaseObj, funcName)
            if func:
                if args:
                    func(*args)
                else:
                    func()


class DataProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DataProxy, self).__init__(uiAdapter)
        self.uiAdapter.dataProxies.append(weakref.proxy(self))
        self.bindingData = {}
        self.binding = {}
        self.bindType = 'data'

    def onCreateBinding(self, *arg):
        key = arg[3][0].GetString()
        obj = arg[3][2]
        handler = arg[3][1]
        self.binding[key] = [obj, handler]
        data = self.getValue(key)
        if data != None:
            handler.InvokeSelf(data)

    def onDeleteBinding(self, *arg):
        key = arg[3][0].GetString()
        if self.binding.has_key(key):
            self.binding.pop(key)

    def getValue(self, key):
        pass

    def isType(self, key):
        if key.find(self.bindType) != -1:
            return True
        return False


class SlotDataProxy(DataProxy):

    def onCreateBinding(self, *arg):
        key = arg[3][0].GetString()
        movie = arg[0]
        obj = arg[3][2]
        handler = arg[3][1]
        self.binding[key] = [obj, handler]
        idCon, idItem = self.getSlotID(key)
        data = self.getSlotValue(movie, idItem, idCon)
        if data != None:
            handler.InvokeSelf(data)

    def getSlotID(self, key):
        return (None, None)

    def getSlotValue(self, movie, idItem, idCon):
        return None
