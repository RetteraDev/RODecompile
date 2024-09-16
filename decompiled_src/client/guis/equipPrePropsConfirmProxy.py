#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/equipPrePropsConfirmProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from guis import ui
from callbackHelper import Functor
from ui import gbk2unicode
from data import item_data as ID
from cdata import font_config_data as FCD
from cdata import game_msg_def_data as GMDD
from data import equip_prefix_prop_data as EPPD
from cdata import equip_star_factor_data as ESFCD
from cdata import equip_quality_factor_data as EQFD

class EquipPrePropsConfirmProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipPrePropsConfirmProxy, self).__init__(uiAdapter)
        self.modelMap = {'refreshContent': self.refreshContent,
         'confirmRebuild': self.confirmRebuild}
        self.mediator = None
        self.type = 'equipPrePropsConfirm'
        self.bindType = 'equipPrePropsConfirm'
        self.isShow = False
        self.itemPage = const.CONT_NO_PAGE
        self.itemPos = const.CONT_NO_POS
        self.currentItem = None
        self.newItem = None
        self.npcEntId = None
        self.triggerId = None

    def confirmRebuild(self, *args):
        txt = uiUtils.getTextFromGMD(GMDD.data.OLD_PREP_PROPS_MISS_CONFIRM)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.trueConfirm, self.itemPage, self.itemPos))

    def trueConfirm(self, page, pos):
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            return
        BigWorld.player().cell.confirmResetEquipPrefix(self.npcEntId, self.itemPage, self.itemPos, True)
        self.closeThis()

    def closeThis(self):
        self.mediator = None
        self.isShow = False
        self.itemPage = const.CONT_NO_PAGE
        self.itemPos = const.CONT_NO_POS
        self.currentItem = None
        self.newItem = None
        self.npcEntId = None
        self.triggerId = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_PREP_PROPS_CONFIRM)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    @ui.callFilter(1)
    def clearWidget(self):
        txt = uiUtils.getTextFromGMD(GMDD.data.NEW_PREP_PROPS_MISS_CONFIRM)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.trueClear, self.itemPage, self.itemPos))

    def trueClear(self, page, pos):
        if not self.isShow:
            return
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            return
        BigWorld.player().cell.confirmResetEquipPrefix(self.npcEntId, self.itemPage, self.itemPos, False)
        self.closeThis()

    def show(self, page, pos, newItem, npcEntId, triggerId):
        self.itemPage = page
        self.itemPos = pos
        self.newItem = newItem
        self.npcEntId = npcEntId
        self.triggerId = triggerId
        self.currentItem = BigWorld.player().inv.getQuickVal(page, pos)
        if not self.isShow:
            self.isShow = True
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_PREP_PROPS_CONFIRM, True)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_PREP_PROPS_CONFIRM:
            self.mediator = mediator

    def refreshContent(self, *args):
        if not self.currentItem:
            return
        self.fixNewItemScore()
        key = self._getKey(0, 0)
        self.bindingData[key] = self.currentItem
        key2 = self._getKey(0, 1)
        self.bindingData[key2] = self.newItem
        iconPath = uiUtils.getItemIconFile64(self.currentItem.id)
        data = {'iconPath': iconPath}
        self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        self.binding[key2][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        if hasattr(self.currentItem, 'quality'):
            quality = self.currentItem.quality
        else:
            quality = ID.data.get(self.currentItem.id, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
        self.binding[key2][0].Invoke('setSlotColor', GfxValue(color))
        strCurrent = "<font color= \'#79C725\'>" + uiUtils.getItemPreprops(self.currentItem) + '</font>'
        strAfter = "<font color= \'#79C725\'>" + uiUtils.getItemPreprops(self.newItem) + '</font>'
        self.mediator.Invoke('setContentInfo', (GfxValue(gbk2unicode(strCurrent)), GfxValue(gbk2unicode(strAfter))))
        preName = uiUtils.getItemPreName(self.currentItem)
        afterName = uiUtils.getItemPreName(self.newItem)
        self.mediator.Invoke('setTitleInfo', (GfxValue(gbk2unicode(preName)), GfxValue(gbk2unicode(afterName))))
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[20:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'equipPrePropsConfirm%d.slot%d' % (bar, slot)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            return True
        else:
            return False

    def calcPrefixScore(self, item):
        starFactor = ESFCD.data.get(getattr(item, 'starLv', -1), {}).get('factor', 1.0)
        qualityFactor = EQFD.data.get(item.quality, {}).get('factor', 1.0)
        prefixScore = 0
        if hasattr(item, 'prefixInfo'):
            preGroupId, prefixId = item.prefixInfo
            preGroupData = EPPD.data.get(preGroupId, [])
            for prefixData in preGroupData:
                if prefixData.get('id') == prefixId:
                    prefixScore = prefixData.get('prefixScore', 0)
                    break

        initScore = prefixScore * qualityFactor
        prefixScore *= starFactor * qualityFactor
        return (initScore, prefixScore)

    def fixNewItemScore(self):
        oldInitScore, oldPrefixScore = self.calcPrefixScore(self.currentItem)
        newInitScore, newPrefixScore = self.calcPrefixScore(self.newItem)
        self.newItem.score += int(newPrefixScore - oldPrefixScore)
        self.newItem.initScore += int(newInitScore - oldInitScore)
