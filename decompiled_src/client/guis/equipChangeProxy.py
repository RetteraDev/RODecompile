#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeProxy.o
import BigWorld
import gameglobal
import gameconfigCommon
import gametypes
import uiUtils
import uiConst
import events
import ui
from gamestrings import gameStrings
from Scaleform import GfxValue
from uiProxy import UIProxy
from guis import equipChangeJuexingStrengthProxy
from guis.asObject import ASObject
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
SUBTAB_JUEXINGREBUILD = 0
SUBTAB_PREFIXREBUILD = 1
SUBTAB_PREFIXTRANSFER = 2
SUBTAB_JUEXINGSTRENGTH = 3

class EquipChangeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeProxy, self).__init__(uiAdapter)
        self.modelMap = {'close': self.onClose,
         'changeTabIndex': self.onChangeTabIndex,
         'getTabInfo': self.onGetTabInfo,
         'checkSubTabBtnVisible': self.onCheckSubTabBtnVisible,
         'getSubTabRedPointVisible': self.onGetSubTabRedPointVisible,
         'setSubTabRedPointVisible': self.onSetSubTabRedPointVisible,
         'registerEquipChangeGem': self.onRegisterEquipChangeGem,
         'unRegisterEquipChangeGem': self.onUnRegisterEquipChangeGem,
         'registerRefining': self.onRegisterRefining,
         'unRegisterRefining': self.onUnRegisterRefining,
         'enableEquipChangeRefine': self.onEnableEquipChangeRefine}
        self.mediator = None
        self.tabIdx = uiConst.EQUIPCHANGE_TAB_ENHANCE
        self.subTabIdx = 0
        self.useDiKou = True
        self.showRedPoint = False
        self.gemRedPointClicked = False
        self.runeRedPointClicked = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_CHANGE, self.checkAndHide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_CHANGE:
            self.mediator = mediator
            return uiUtils.array2GfxAarry([self.tabIdx, self.subTabIdx])

    def clearWidget(self):
        self.mediator = None
        self.showRedPoint = False
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_EQUIP_CHANGE)

    def reset(self):
        self.tabIdx = uiConst.EQUIPCHANGE_TAB_ENHANCE
        self.subTabIdx = 0

    def clearAll(self):
        self.useDiKou = True

    def show(self, tabIdx, subTabIdx = 0):
        p = BigWorld.player()
        if p._isSchoolSwitch():
            p.showGameMsg(GMDD.data.FORBIDEN_EQUIP_CHANGE_IN_SCHOOL_SWITCH, ())
            return
        if tabIdx == uiConst.EQUIPCHANGE_TAB_ENHANCE:
            if not gameglobal.rds.configData.get('enableEquipChangeEnhance', False):
                p.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
                return
        elif tabIdx == uiConst.EQUIPCHANGE_TAB_REFORGE:
            if not gameglobal.rds.configData.get('enableEquipChangeReforge', False):
                p.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
                return
            needLv = SCD.data.get('equipChangeReforgeOpenLv', 0)
            if p.lv < needLv:
                p.showGameMsg(GMDD.data.CBG_PLACE_CASH_FAILED_LV, (needLv,))
                return
        elif tabIdx == uiConst.EQUIPCHANGE_TAB_STAR:
            if not gameglobal.rds.configData.get('enableEquipChangeStar', False):
                p.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
                return
            needLv = SCD.data.get('equipChangeStarOpenLv', 0)
            if p.lv < needLv:
                p.showGameMsg(GMDD.data.CBG_PLACE_CASH_FAILED_LV, (needLv,))
                return
        elif tabIdx == uiConst.EQUIPCHANGE_TAB_SUIT:
            if not gameglobal.rds.configData.get('enableEquipChangeSuit', False):
                p.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
                return
            needLv = SCD.data.get('equipChangeSuitOpenLv', 0)
            if p.lv < needLv:
                p.showGameMsg(GMDD.data.CBG_PLACE_CASH_FAILED_LV, (needLv,))
                return
        elif tabIdx == uiConst.EQUIPCHANGE_TAB_GEM:
            if not gameglobal.rds.configData.get('enableEquipChangeGem', False):
                p.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
                return
            needLv = SCD.data.get('equipChangeGemOpenLv', 0)
            if p.lv < needLv:
                p.showGameMsg(GMDD.data.CBG_PLACE_CASH_FAILED_LV, (needLv,))
                return
        if not self.mediator:
            self.tabIdx = tabIdx
            self.subTabIdx = subTabIdx
            self.uiAdapter.loadWidget(uiConst.WIDGET_EQUIP_CHANGE)
        else:
            self.realSetTabIndex(tabIdx, subTabIdx)
        if self.uiAdapter.mail.mediator:
            self.uiAdapter.mail.hide()

    def onClose(self, *arg):
        self.checkAndHide()

    def checkAndHide(self):
        self.hide()

    def onChangeTabIndex(self, *arg):
        tabIdx = int(arg[3][0].GetNumber())
        subTabIdx = int(arg[3][1].GetNumber())
        self.realSetTabIndex(tabIdx, subTabIdx)

    def realSetTabIndex(self, tabIdx, subTabIdx):
        if self.mediator:
            self.tabIdx = tabIdx
            self.subTabIdx = subTabIdx
            if tabIdx == uiConst.EQUIPCHANGE_TAB_GEM:
                self.gemRedPointClicked = True
            elif tabIdx == uiConst.EQUIPCHANGE_TAB_RUNE:
                self.runeRedPointClicked = True
            self.mediator.Invoke('realSetTabIndex', (GfxValue(self.tabIdx), GfxValue(self.subTabIdx)))
            self.mediator.Invoke('relayoutTab')

    def refreshInfo(self):
        if self.mediator:
            info = {}
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    @ui.uiEvent(uiConst.WIDGET_EQUIP_CHANGE, events.EVENT_ROLE_SET_LV)
    def refreshTabInfo(self):
        if self.mediator:
            self.mediator.Invoke('relayoutTab')

    def onGetTabInfo(self, *arg):
        lv = BigWorld.player().lv
        info = {}
        info['visibleEnhanceBtn'] = gameglobal.rds.configData.get('enableEquipChangeEnhance', False)
        info['visibleReforgeBtn'] = gameglobal.rds.configData.get('enableEquipChangeReforge', False)
        needLv = SCD.data.get('equipChangeReforgeOpenLv', 0)
        info['enabledReforgeBtn'] = lv >= needLv
        info['reforgeBtnTip'] = gameStrings.WELFARE_ENABLE_LV % needLv
        info['visibleStarBtn'] = gameglobal.rds.configData.get('enableEquipChangeStar', False)
        needLv = SCD.data.get('equipChangeStarOpenLv', 0)
        info['enabledStarBtn'] = lv >= needLv
        info['starBtnTip'] = gameStrings.WELFARE_ENABLE_LV % needLv
        info['visibleSuitBtn'] = gameglobal.rds.configData.get('enableEquipChangeSuit', False)
        needLv = SCD.data.get('equipChangeSuitOpenLv', 0)
        info['enabledSuitBtn'] = lv >= needLv
        info['suitBtnTip'] = gameStrings.WELFARE_ENABLE_LV % needLv
        info['visibleGemBtn'] = gameglobal.rds.configData.get('enableEquipChangeGem', False)
        needLv = SCD.data.get('equipChangeGemOpenLv', 0)
        info['enabledGemBtn'] = lv >= needLv
        info['gemBtnTip'] = gameStrings.WELFARE_ENABLE_LV % needLv
        info['gemRedPointVisible'] = self.showRedPoint and not self.gemRedPointClicked
        p = BigWorld.player()
        canOpenRune = p.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_HIEROGRAM)
        info['visibleRuneBtn'] = gameglobal.rds.configData.get('enableEquipChangeRune', False)
        openRuneLv = SCD.data.get('OPENRUNELV', 30)
        info['enabledRuneBtn'] = canOpenRune
        info['runeBtnTip'] = gameStrings.WELFARE_ENABLE_LV % openRuneLv
        info['runeRedPointVisible'] = self.showRedPoint and not self.runeRedPointClicked
        return uiUtils.dict2GfxDict(info, True)

    def onCheckSubTabBtnVisible(self, *args):
        tabIdx = int(args[3][0].GetNumber())
        if tabIdx == SUBTAB_JUEXINGSTRENGTH:
            return GfxValue(equipChangeJuexingStrengthProxy.checkTabVisible())
        return GfxValue(True)

    def onGetSubTabRedPointVisible(self, *args):
        name = args[3][0].GetString()
        return GfxValue(self.getSubTabRedPointVisible(name))

    def getSubTabRedPointVisible(self, name):
        if name == 'gemLvUp':
            return self.showRedPoint and not self.uiAdapter.equipChangeGemLvUp.gemLvUpClicked
        if name == 'runeLvUp':
            return self.showRedPoint and not self.uiAdapter.equipChangeRuneLvUp.runeLvUpClicked
        return False

    def onSetSubTabRedPointVisible(self, *args):
        name = args[3][0].GetString()
        self.setSubTabRedPointVisible(name)

    def setSubTabRedPointVisible(self, name):
        if name == 'gemLvUp':
            self.uiAdapter.equipChangeGemLvUp.gemLvUpClicked = True
        elif name == 'runeLvUp':
            self.uiAdapter.equipChangeRuneLvUp.runeLvUpClicked = True

    def onRegisterEquipChangeGem(self, *args):
        widget = ASObject(args[3][0])
        self.uiAdapter.equipChangeGem.registerEquipChangeGem(widget)

    def onUnRegisterEquipChangeGem(self, *args):
        self.uiAdapter.equipChangeGem.unRegisterEquipChangeGem()

    def onRegisterRefining(self, *args):
        widget = ASObject(args[3][0])
        self.uiAdapter.equipChangeRefining.registerPanel(widget)

    def onUnRegisterRefining(self, *args):
        self.uiAdapter.equipChangeRefining.unRegisterPanel()

    def onEnableEquipChangeRefine(self, *args):
        return GfxValue(gameconfigCommon.enableRefineManualEquipment() and BigWorld.player().lv >= SCD.data.get('refineManualEquipmentLvlimt', 59))
