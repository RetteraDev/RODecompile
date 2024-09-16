#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/interactiveActionBarProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from guis import hotkeyProxy
import hotkey as HK
from data import interactive_data as IAD
from data import interactive_action_data as IAAD
from data import interactive_data as ID
from data import interactive_expend_action_data as IEAD
CALLBACK_TIME = 0.1

class InteractiveActionBarProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(InteractiveActionBarProxy, self).__init__(uiAdapter)
        self.mediator = None
        self.modelMap = {'closeWidget': self.onClose,
         'getKeyText': self.onGetKeyText,
         'notifySlotUse': self.onNotifySlotUse,
         'getActionNormalTips': self.onGetActionNormalTips,
         'exitInteractive': self.onExitInteractive,
         'getSlotData': self.onGetSlotData}
        self.type = 'interactiveActionBar'
        self.bindType = 'interactiveActionBar'
        self.actions = [[0, 0]] * 5
        self.binding = {}
        self.bindIdx = -1
        self.playActionCD = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INTERACTIVE_ACTION_BAR:
            self.mediator = mediator

    def getSlotID(self, key):
        _idCon, idItem = key.split('.')
        return (0, int(idItem[4:]))

    def onGetKeyText(self, *arg):
        keyArr = self._createKeyText()
        keyArr.append(hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_LEAVE_ZAIJU))
        return uiUtils.array2GfxAarry(keyArr, True)

    def onGetActionNormalTips(self, *arg):
        tips = []
        for action in self.actions:
            name = IAAD.data.get(action[0], {}).get('desc', '')
            tip = IAAD.data.get(action[0], {}).get('tip', name)
            tips.append(tip)

        return uiUtils.array2GfxAarry(tips, True)

    def onExitInteractive(self, *arg):
        BigWorld.player().quitInteractiveObj()

    def _createKeyText(self):
        keyArr = hotkeyProxy.getInstance().shortKey.getKeyDescArray()[0:5]
        return keyArr

    def onNotifySlotUse(self, *arg):
        key = arg[3][0].GetString()
        _, slotId = self.getSlotID(key)
        actionId = self.actions[slotId][0]
        BigWorld.player().playInteractiveAction(actionId)

    def setCoolDown(self):
        if self.mediator:
            self.mediator.Invoke('setCoolDown', GfxValue(self.playActionCD * 1000))

    def useSkill(self, bar, slotId, isDown = False):
        if isDown:
            if slotId >= len(self.actions):
                return
            actionId = self.actions[slotId][0]
            BigWorld.player().playInteractiveAction(actionId)

    def getSlotValue(self, movie, idItem, idCon):
        return None

    def refreshActionBar(self):
        p = BigWorld.player()
        if not p.inInteractiveObject():
            return
        else:
            interObj = BigWorld.entities.get(p.interactiveObjectEntId, None)
            if not interObj or not interObj.inWorld:
                return
            basicActionExpendId = IAD.data.get(interObj.objectId, {}).get('basicActionExpendId', None)
            interactiveActions = []
            interactiveActionsExpend = IEAD.data.get(basicActionExpendId, {}).get('interactiveActions', None)
            if interactiveActionsExpend and self.bindIdx > -1 and self.bindIdx < len(interactiveActionsExpend):
                interactiveActions = interactiveActionsExpend[self.bindIdx]
            else:
                interactiveActions = IAD.data.get(interObj.objectId, {}).get('interactiveActions', [])
            self.playActionCD = IAD.data.get(interObj.objectId, {}).get('playActionCD', 0)
            self.actions = []
            for action in interactiveActions:
                self.actions.append([action, 0])

            if len(self.actions) < 5:
                for _ in xrange(5 - len(self.actions)):
                    self.actions.append([0, 0])

            if self.mediator:
                self.mediator.Invoke('refreshActionBar')
            return

    def getActionIcon(self, actionId, level = 1):
        if actionId == 0:
            return 'notFound'
        else:
            icon = IAAD.data.get(actionId, {}).get('icon', None)
            if icon != None:
                return 'skill/icon/' + str(icon) + '.dds'
            return 'notFound'

    def show(self, bindIdx = -1):
        if BigWorld.player().inInteractiveObj():
            objId = gameglobal.rds.ui.interactiveObjMounts.getInteractiveObjId()
            if objId != 0 and ID.data.get(objId, {}).get('hideActionBar', 0):
                BigWorld.player().showZaijuUI(showType=uiConst.ZAIJU_SHOW_TYPE_EXIT)
                return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INTERACTIVE_ACTION_BAR)
        if self.mediator:
            self.mediator.Invoke('show')
        self.bindIdx = bindIdx
        self.refreshActionBar()
        self.hideOtherWidget()

    def hideOtherWidget(self):
        gameglobal.rds.ui.actionbar.refreshSkillActionBarOpacity()
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ACTION_BARS, False)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WUSHUANG_BARS, False)
        gameglobal.rds.ui.bullet.setVisible(False)
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.SetVisible(False)

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.playActionCD = 0
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INTERACTIVE_ACTION_BAR)
        BigWorld.player().hideZaijuUI(uiConst.ZAIJU_SHOW_TYPE_EXIT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXIT_ZAIJU)
        if not gameglobal.rds.ui.isHideAllUI():
            gameglobal.rds.ui.actionbar.refreshSkillActionBarOpacity()
        else:
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ACTION_BARS, True)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_WUSHUANG_BARS, True)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ZAIJU, False)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ZAIJU_V2, False)
        gameglobal.rds.ui.actionbar.updateSlots()
        gameglobal.rds.ui.bullet.setVisible(True)
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.Invoke('forceVisibleByOther')
        if gameglobal.rds.ui.guildBusinessBag.mediator:
            gameglobal.rds.ui.guildBusinessBag.hide()

    def onGetSlotData(self, *args):
        ret = []
        for action in self.actions:
            iconPath = self.getActionIcon(action[0], action[1])
            ret.append({'name': iconPath,
             'iconPath': iconPath})

        return uiUtils.array2GfxAarry(ret, True)
