#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/baoDianProxy.o
import BigWorld
from Scaleform import GfxValue
import keys
import gameglobal
import appSetting
import uiConst
import uiUtils
import utils
from uiProxy import UIProxy
from guis import events
from guis.asObject import ASObject
from data import baodian_menu_data as BMD
from data import baodian_content_data as BCD

class BaoDianProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BaoDianProxy, self).__init__(uiAdapter)
        self.modelMap = {'close': self.onClose,
         'getData': self.onGetData,
         'getPointSubPage': self.onGetPointSubPage}
        self.mediator = None
        self.widget = None
        self.introType = uiConst.BAODIAN_TYPE_DEFAULT
        uiAdapter.registerEscFunc(uiConst.WIDGET_BAODIAN, self.hide)
        self.pointPage = [0, 0, 0]

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BAODIAN:
            self.mediator = mediator
            self.widget = ASObject(self.mediator).getWidget()
            self.refreshCheck()

    def reset(self):
        self.pointPage = [0, 0, 0]

    def getMainIdByIntroType(self, introType):
        for mainId in BMD.data:
            if BMD.data.get(mainId, {}).get('type', 0) == introType:
                return mainId

        return 0

    def getBaodianIdx(self, mainId, subId, resId):
        mainKeys = BMD.data.keys()
        mainKeys.sort()
        if mainId in mainKeys:
            mainIdx = mainKeys.index(mainId)
        else:
            mainIdx = 0
        subKeys = BMD.data.get(mainId, {}).get('list', [])
        if subId in subKeys:
            subIdx = subKeys.index(subId)
        else:
            subIdx = 0
        pictures = BCD.data.get(subId, {}).get('picture', [])
        if resId in pictures:
            pageIdx = pictures.index(resId)
        else:
            pageIdx = 0
        return (mainIdx, subIdx, pageIdx)

    def show(self, page = [0, 0, 0], introType = uiConst.BAODIAN_TYPE_DEFAULT):
        needRefresh = self.introType != introType
        self.introType = introType
        if utils.isInternationalVersion():
            self.uiAdapter.help.show()
            return
        if page != [0, 0, 0]:
            page = self.getBaodianIdx(page[0], page[1], page[2])
        elif introType != uiConst.BAODIAN_TYPE_DEFAULT:
            page = self.getBaodianIdx(self.getMainIdByIntroType(introType), 0, 0)
        self.pointPage = page
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BAODIAN)
            gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_BAODIAN)
        elif needRefresh:
            self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            self.refreshCheck()
            self.mediator.Invoke('gotoSubItem', GfxValue(self.pointPage[0], self.pointPage[1], self.pointPage[2]))

    def refreshCheck(self):
        if self.widget:
            self.widget.notShowCheck.visible = self.introType in uiConst.SHOW_CHECK_TYPES
            if self.widget.notShowCheck.visible:
                self.widget.notShowCheck.removeEventListener(events.EVENT_SELECT, self.onNotShowSelectChange)
                self.widget.notShowCheck.selected = self.getNoPushSetting(self.introType)
                self.widget.notShowCheck.addEventListener(events.EVENT_SELECT, self.onNotShowSelectChange)

    def onNotShowSelectChange(self, *args):
        e = ASObject(args[3][0])
        notShowAgain = e.currentTarget.selected
        self.saveNoPushSetting(self.introType, notShowAgain)

    def saveNoPushSetting(self, introId, value):
        saveKey = keys.SET_INTRO_NO_PUSH % (str(introId),)
        appSetting.Obj[saveKey] = 1 if value else 0
        appSetting.Obj.save()

    def getNoPushSetting(self, introId):
        saveKey = keys.SET_INTRO_NO_PUSH % (str(introId),)
        autoPush = appSetting.Obj.get(saveKey, 0)
        return bool(autoPush)

    def isShow(self):
        return self.mediator != None

    def clearWidget(self):
        self.mediator = None
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BAODIAN)

    def onClose(self, *arg):
        self.hide()

    def onGetData(self, *arg):
        data = []
        index = 0
        for menu in BMD.data.items():
            menuData = {}
            if menu[1].get('gameconfig', ''):
                if gameglobal.rds.configData.get(menu[1]['gameconfig']):
                    continue
            menuData['index'] = index
            menuData['label'] = menu[1]['name']
            subMenu = []
            for contentID in menu[1]['list']:
                subMenuContent = {}
                content = BCD.data.get(contentID, {})
                subMenuContent['label'] = content['name']
                subMenuContent['page'] = map(lambda x: 'widgets/baodian/' + str(x) + '.swf', content['picture'])
                subMenu.append(subMenuContent)

            menuData['subItem'] = subMenu
            index += 1
            data.append(menuData)

        return uiUtils.array2GfxAarry(data, True)

    def autoShowIntro(self, introType):
        if utils.isInternationalVersion():
            return
        isNoPush = self.getNoPushSetting(introType)
        if not isNoPush:
            self.show(introType=introType)

    def onGetPointSubPage(self, *arg):
        return uiUtils.array2GfxAarry(self.pointPage)
