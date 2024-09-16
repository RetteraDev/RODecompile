#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/equipStarProxy.o
import BigWorld
import gameglobal
import gametypes
import const
import utils
from guis import uiUtils, uiConst
from item import Item
from Scaleform import GfxValue
from uiProxy import SlotDataProxy
from guis import ui
from callbackHelper import Functor
from data import equip_data as ED
from cdata import font_config_data as FCD
from data import item_data as ID
from data import prop_ref_data as PRD
from cdata import game_msg_def_data as GMDD
from cdata import equip_active_star_cost_data as EASCD
from cdata import equip_lvup_star_cost_data as ELSCD
from cdata import equip_star_factor_data as ESFCD
from cdata import equip_quality_factor_data as EQFD
from data import game_msg_data as GMD
TS_NONE = 0
TS_NEED_EQUIP_AC = 1
TS_NEED_EQUIP_LV = 2
TS_LACK_MATERIAL = 3
TS_LACK_MONEY = 4
SHOW_MODE_ACTIVATE = 1
SHOW_MODE_LVUP = 2
OPEN_MODE_MANUAL = 1
OPEN_MODE_AUTO = 2
SRC_MODE_INVENTORY = 1
SRC_MODE_ROLEINFO = 2

def float2Int(num):
    return int(num)


class EquipStarProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipStarProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeStarActivate': self.onCloseStarActivate,
         'closeStarLvUpConfirm': self.onCloseStarLvUpConfirm,
         'resetEquipSlot': self.onResetEquipSlot,
         'activateStar': self.onActivateStar,
         'confirmLvUpStar': self.onConfirmLvUpStar,
         'getStarLvUpInfo': self.onGetStarLvUpInfo,
         'initPanelDone': self.onInitPanelDone,
         'clickYunchuiBtn': self.onClickYunchuiBtn}
        self.bindType = 'equipStar'
        self.type = 'equipStar'
        self.activateMediator = None
        self.lvupConfirmMediator = None
        self.showMode = SHOW_MODE_ACTIVATE
        self.openMode = OPEN_MODE_MANUAL
        self.srcMode = SRC_MODE_INVENTORY
        self.lockSlotPos = []
        self.activateWidgetId = uiConst.WIDGET_EQUIP_STAR_ACTIVATE
        self.lvupConfirmWidgetId = uiConst.WIDGET_EQUIP_STAR_LVUP_CONFIRM
        uiAdapter.registerEscFunc(self.activateWidgetId, self.onCloseStarActivate)
        uiAdapter.registerEscFunc(self.lvupConfirmWidgetId, self.onCloseStarLvUpConfirm)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.activateWidgetId:
            self.activateMediator = mediator
            return uiUtils.dict2GfxDict({'showMode': self.showMode}, True)
        if widgetId == self.lvupConfirmWidgetId:
            self.lvupConfirmMediator = mediator

    def onInitPanelDone(self, *arg):
        if self.openMode == OPEN_MODE_AUTO and self.showMode == SHOW_MODE_LVUP:
            part = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_EQUIP_STAR_LV_UP).get('data', 0)
            self.setEquipBarItem(uiConst.EQUIP_ACTION_BAR, part, 0, 0)
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_EQUIP_STAR_LV_UP, {'data': part})
        else:
            gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)

    def showStarActivate(self, entId):
        self.showMode = SHOW_MODE_ACTIVATE
        gameglobal.rds.ui.loadWidget(self.activateWidgetId)

    def showStarLvUp(self):
        self.showMode = SHOW_MODE_LVUP
        self.openMode = OPEN_MODE_MANUAL
        gameglobal.rds.ui.loadWidget(self.activateWidgetId)

    def showStarLvUpByAutoPush(self):
        self.showMode = SHOW_MODE_LVUP
        self.openMode = OPEN_MODE_AUTO
        gameglobal.rds.ui.loadWidget(self.activateWidgetId)

    def showStarLvUpConfirm(self):
        gameglobal.rds.ui.loadWidget(self.lvupConfirmWidgetId, isModal=True)

    def reset(self):
        self.activateMediator = None
        self.lockSlotPos = []

    def onActivateSuccess(self):
        if not self.activateMediator:
            return
        if len(self.lockSlotPos) < 1:
            return
        invPos = self.lockSlotPos[0]
        equip = self.getCurrentEquip()
        if self.srcMode == SRC_MODE_INVENTORY:
            self.setItem(invPos[0], invPos[1], uiConst.EQUIP_STAR_ACTIVATE, 0, equip)
        elif self.srcMode == SRC_MODE_ROLEINFO:
            self.setEquipBarItem(invPos[0], invPos[1], uiConst.EQUIP_STAR_ACTIVATE, 0)
        self.activateMediator.Invoke('showSuccessAnim')

    def onLvupSuccess(self):
        if not self.lvupConfirmMediator:
            return
        self.clearLvUpConfirmWidget()
        self.onActivateSuccess()

    def onResSet(self, page, pos):
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def clearWidget(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.activateWidgetId)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        self.reset()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def clearLvUpConfirmWidget(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.lvupConfirmWidgetId)
        self.lvupConfirmMediator = None

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[9:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'equipStar%d.slot%d' % (bar, slot)

    def getCurrentEquip(self):
        if len(self.lockSlotPos) < 1:
            return
        slotPos = self.lockSlotPos[0]
        if self.srcMode == SRC_MODE_INVENTORY:
            equip = BigWorld.player().inv.getQuickVal(slotPos[0], slotPos[1])
        elif self.srcMode == SRC_MODE_ROLEINFO:
            equip = BigWorld.player().equipment[slotPos[1]]
        else:
            equip = None
        return equip

    def refreshEquipStarInfo(self):
        if self.srcMode != SRC_MODE_ROLEINFO:
            return
        if len(self.lockSlotPos) < 1:
            return
        equipPart = self.lockSlotPos[0][1]
        it = BigWorld.player().equipment[equipPart]
        if not it:
            self.onResetEquipSlot()

    def setEquipBarItem(self, nPage, nItem, destBar, destSlot):
        ret = {}
        key = self._getKey(destBar, destSlot)
        if not self.binding.has_key(key):
            return
        it = BigWorld.player().equipment[nItem]
        if not it:
            return
        if not hasattr(it, 'starLv'):
            return
        if it.isYaoPei() or it.isGuanYin():
            return
        self.srcMode = SRC_MODE_ROLEINFO
        self.lockSlotPos = []
        self.lockSlotPos.append((nPage, nItem))
        self.updateEquipSlot(it, key)
        self.appendEquipStarInfo(ret, it)
        self.appendStarCostInfo(ret, it)
        if self.activateMediator:
            self.activateMediator.Invoke('refreshActiveStar', uiUtils.dict2GfxDict(ret, True))

    def setItem(self, nPage, nItem, destBar, destSlot, it):
        ret = {}
        key = self._getKey(destBar, destSlot)
        if not self.binding.has_key(key):
            return
        if not hasattr(it, 'starLv'):
            return
        self.srcMode = SRC_MODE_INVENTORY
        self.lockSlotPos = []
        self.lockSlotPos.append((nPage, nItem))
        self.updateEquipSlot(it, key)
        self.appendEquipStarInfo(ret, it)
        self.appendStarCostInfo(ret, it)
        if self.activateMediator:
            self.activateMediator.Invoke('refreshActiveStar', uiUtils.dict2GfxDict(ret, True))

    def appendEquipStarInfo(self, ret, it):
        starInfo = {}
        if not hasattr(it, 'activeStarLv'):
            starInfo['activeStarLv'] = 0
            starInfo['inactiveStarLv'] = 0
            starInfo['starLv'] = 0
            starInfo['starExp'] = 0
        else:
            starInfo['activeStarLv'] = it.activeStarLv
            starInfo['inactiveStarLv'] = it.inactiveStarLv
            starInfo['starLv'] = it.starLv
            starInfo['starExp'] = it.starExp
        starInfo['maxStarLv'] = getattr(it, 'maxStarLv', -1)
        ret['starInfo'] = starInfo

    def appendStarCostInfo(self, ret, it):
        p = BigWorld.player()
        if self.showMode == SHOW_MODE_ACTIVATE:
            starCostData = EASCD.data.get((it.quality, it.order), None)
        else:
            starCostData = ELSCD.data.get((it.quality, it.starLv), None)
        if starCostData is None:
            return
        itemId, costFormula, cashFormula = starCostData['itemId'], starCostData['itemNum'], starCostData['cash']
        itemNum = it.evalValue(costFormula[0], costFormula[1:])
        cashNum = it.evalValue(cashFormula[0], cashFormula[1:])
        expNum = it._getEquipStarUpExp()
        it = Item(itemId)
        ret['costItem'] = self.basicItemInfo(it)
        ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if itemNum > ownNum:
            ret['materialNum'] = '%s/%s' % (uiUtils.toHtml(str(ownNum), '#FB0000'), str(itemNum))
        else:
            ret['materialNum'] = '%s/%s' % (str(ownNum), str(itemNum))
        if self.showMode == SHOW_MODE_ACTIVATE:
            enableEquipDiKou = gameglobal.rds.configData.get('enableEquipDiKou', False)
        else:
            enableEquipDiKou = False
        ret['enableEquipDiKou'] = enableEquipDiKou
        costItemEnough = True
        if enableEquipDiKou:
            itemDict = {itemId: itemNum}
            self.appendDiKouInfo(ret, itemDict)
            if not uiUtils.checkEquipMaterialDiKou(itemDict):
                costItemEnough = False
        elif itemNum > ownNum:
            costItemEnough = False
        ret['costItemEnough'] = costItemEnough
        ret['needCostItem'] = itemNum > 0
        ret['costCash'] = cashNum
        ret['ownCash'] = p.cash
        ret['costExp'] = expNum

    def appendDiKouInfo(self, ret, itemDict):
        if itemDict != {}:
            p = BigWorld.player()
            _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
            yunchuiOwn = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
            if yunchuiNeed > yunchuiOwn:
                ret['yunchui'] = '%s/%s' % (uiUtils.toHtml(format(yunchuiOwn, ','), '#FB0000'), format(yunchuiNeed, ','))
                ret['yunchuiEnabled'] = True
            else:
                ret['yunchui'] = '%s/%s' % (format(yunchuiOwn, ','), format(yunchuiNeed, ','))
                ret['yunchuiEnabled'] = False
            ret['diKouVisible'] = True
        else:
            ret['diKouVisible'] = False

    def basicItemInfo(self, it, withId = True):
        ret = {}
        itemId = it.id
        itemInfo = ID.data.get(itemId, {})
        if hasattr(it, 'quality'):
            quality = it.quality
        else:
            quality = itemInfo.get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        icon = uiUtils.getItemIconFile64(itemId)
        name = itemInfo.get('name', '未知物品')
        mwrap = itemInfo.get('mwrap', 1)
        if withId:
            ret['itemId'] = itemId
        ret['name'] = name
        ret['color'] = color
        ret['iconPath'] = icon
        ret['mwrap'] = mwrap
        return ret

    def _calAttrVal(self, item, attrs, rank):
        ret = []
        if hasattr(item, 'starLv'):
            starLv = item.starLv
        else:
            starLv = 0
        nextStarLv = starLv + 1
        starFactor = ESFCD.data.get(starLv, {}).get('factor', 1.0)
        quality = getattr(item, 'quality', 1)
        if not quality:
            quality = 1
        qualityFactor = EQFD.data.get(quality, {}).get('factor', 1.0)
        nextStarFactor = ESFCD.data.get(nextStarLv, {}).get('factor', 1.0)
        for pid, pType, pVal in attrs:
            if pType == gametypes.DATA_TYPE_NUM and item._isIntPropRef(pid):
                ret.append((pid,
                 pType,
                 float2Int(pVal * starFactor * qualityFactor),
                 float2Int(pVal * nextStarFactor * qualityFactor)))
            else:
                ret.append((pid,
                 pType,
                 pVal * starFactor * qualityFactor,
                 pVal * nextStarFactor * qualityFactor))

        if rank:
            ret = [ tuple(list(r) + [PRD.data[r[0]]['priorityLevel'], PRD.data[r[0]]['showColor']]) for r in ret ]
            ret.sort(key=lambda k: k[4])
        return ret

    def calAttrVal(self, item):
        basic = []
        rand = []
        pre = []
        extra = []
        if hasattr(item, 'props'):
            basic = self._calAttrVal(item, item.props, False)
        if hasattr(item, 'rprops'):
            rand = self._calAttrVal(item, item.rprops, True)
        if hasattr(item, 'preprops'):
            pre = self._calAttrVal(item, item.preprops, True)
        if hasattr(item, 'extraProps'):
            extra = self._calAttrVal(item, item.extraProps, True)
        return (basic,
         rand,
         pre,
         extra)

    def _appendProps(self, props, data, type):
        for item in data:
            propItem = []
            info = PRD.data[item[0]]
            propItem.append(type)
            propItem.append(info['name'])
            if info['type'] == 2:
                propItem.append('+')
                propItem.append('+')
            elif info['type'] == 1:
                propItem.append('-')
                propItem.append('-')
            if info['showType'] == 0:
                propItem[2] += str(float2Int(item[2]))
                propItem[3] += str(float2Int(item[3]))
            elif info['showType'] == 2:
                propItem[2] += str(round(item[2], 1))
                propItem[3] += str(round(item[3], 1))
            else:
                propItem[2] += str(round(item[2] * 100, 1)) + '%'
                propItem[3] += str(round(item[3] * 100, 1)) + '%'
            props.append(propItem)

    def appendEquipProps(self, ret, i):
        basic, rand, pre, extra = self.calAttrVal(i)
        props = []
        if ED.data[i.id]['equipType'] == 1:
            basicItem = []
            newBasic = []
            for item in basic:
                if item[0] == 118:
                    basicItem.append('basic')
                    basicItem.append('物理攻击力')
                    basicItem.append(str(item[2]) + '-')
                    basicItem.append(str(item[3]) + '-')
                elif item[0] == 119:
                    basicItem[2] += str(item[2])
                    basicItem[3] += str(item[3])
                else:
                    newBasic.append(item)

            if len(basicItem) > 1:
                props.append(basicItem)
            basic = newBasic
            basicItem = []
            newBasic = []
            for item in basic:
                if item[0] == 120:
                    basicItem.append('basic')
                    basicItem.append('法术攻击力')
                    basicItem.append(str(item[2]) + '-')
                    basicItem.append(str(item[3]) + '-')
                elif item[0] == 121:
                    basicItem[2] += str(item[2])
                    basicItem[3] += str(item[3])
                else:
                    newBasic.append(item)

            if len(basicItem) > 1:
                props.append(basicItem)
            basic = newBasic
        for item in basic:
            basicItem = []
            info = PRD.data[item[0]]
            basicItem.append('basic')
            basicItem.append(info['name'])
            if info['showType'] == 0:
                basicItem.append(str(float2Int(item[2])))
                basicItem.append(str(float2Int(item[3])))
            elif info['showType'] == 2:
                basicItem.append(str(round(item[2], 1)))
                basicItem.append(str(round(item[3], 1)))
            else:
                basicItem.append(str(round(item[2] * 100, 1)) + '%')
                basicItem.append(str(round(item[3] * 100, 1)) + '%')
            props.append(basicItem)

        self._appendProps(props, pre, 'pre')
        self._appendProps(props, extra, 'extra')
        self._appendProps(props, rand, 'rand')
        ret['props'] = props

    def updateEquipSlot(self, it, key):
        if not it:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        else:
            itemInfo = self.basicItemInfo(it, False)
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(itemInfo))
            self.binding[key][0].Invoke('setSlotColor', GfxValue(itemInfo['color']))

    def onCloseStarActivate(self, *arg):
        self.clearWidget()

    def onCloseStarLvUpConfirm(self, *arg):
        self.clearLvUpConfirmWidget()

    def onResetEquipSlot(self, *arg):
        ret = {}
        key = self._getKey(uiConst.EQUIP_STAR_ACTIVATE, 0)
        self.lockSlotPos = []
        ret['starInfo'] = None
        ret['costItem'] = None
        ret['costCash'] = 0
        self.updateEquipSlot(None, key)
        if self.activateMediator:
            self.activateMediator.Invoke('refreshActiveStar', uiUtils.dict2GfxDict(ret, True))

    def onActivateStar(self, *arg):
        if len(self.lockSlotPos) < 1:
            return
        if self.showMode == SHOW_MODE_ACTIVATE:
            invPos = self.lockSlotPos[0]
            self.onTrueActiveStarLv(invPos[0], invPos[1])
        else:
            self.showStarLvUpConfirm()

    @ui.checkEquipCanReturnByPos([1, 2], GMDD.data.ACTIVE_STAR_LV)
    @ui.looseGroupTradeConfirm([1, 2], GMDD.data.ACTIVE_STAR_LV)
    def onTrueActiveStarLv(self, page, pos):
        p = BigWorld.player()
        equip = p.inv.getQuickVal(page, pos)
        activeCostData = EASCD.data[equip.quality, equip.order]
        itemId, costFormula, cashFormula = activeCostData['itemId'], activeCostData['itemNum'], activeCostData['cash']
        itemNum = equip.evalValue(costFormula[0], costFormula[1:])
        remain, res = p.inv.cntItemWithPlans(itemId, itemNum, enableParentCheck=True)
        if gameglobal.rds.configData.get('enableEquipDiKou', False):
            itemDict = {itemId: itemNum}
            if not uiUtils.checkEquipMaterialDiKou(itemDict):
                p.showGameMsg(GMDD.data.EQUIP_STAR_LV_ACTIVE_ITEM_NOT_ENOUGH, ())
                return
            _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
            if yunchuiNeed > 0 and not equip.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.activeStarLv, page, pos))
                return
        elif remain:
            p.showGameMsg(GMDD.data.EQUIP_STAR_LV_ACTIVE_ITEM_NOT_ENOUGH, ())
            return
        needBind = any([ p.inv.getQuickVal(pg, ps).isForeverBind() for pg, ps, _ in res ])
        if needBind and not equip.isForeverBind():
            msg = GMD.data.get(GMDD.data.ACTIVE_STAR_LV_BIND, {}).get('text', '制作的手工装备将绑定')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.activeStarLv, page, pos))
        else:
            p.cell.activeStarLv(page, pos)

    @ui.checkEquipCanReturnByPos([1, 2], GMDD.data.ACTIVE_STAR_LV_UP_INV)
    @ui.looseGroupTradeConfirm([1, 2], GMDD.data.ACTIVE_STAR_LV_UP_INV)
    def onTrueStarLvUpInv(self, page, pos):
        BigWorld.player().cell.equipStarLvupInv(page, pos)

    def onConfirmLvUpStar(self, *arg):
        if len(self.lockSlotPos) < 1:
            return
        invPos = self.lockSlotPos[0]
        if self.srcMode == SRC_MODE_INVENTORY:
            self.onTrueStarLvUpInv(invPos[0], invPos[1])
        elif self.srcMode == SRC_MODE_ROLEINFO:
            BigWorld.player().cell.equipStarLvupRole(invPos[1])

    def onGetStarLvUpInfo(self, *arg):
        if len(self.lockSlotPos) < 1:
            return GfxValue('')
        equip = self.getCurrentEquip()
        if not equip:
            return GfxValue('')
        ret = self.basicItemInfo(equip, False)
        self.appendEquipStarInfo(ret, equip)
        self.appendEquipProps(ret, equip)
        self.appendNeedShow(ret, equip)
        return uiUtils.dict2GfxDict(ret, True)

    def appendNeedShow(self, ret, equip):
        needShow = False
        useExp = equip._getEquipStarUpExp()
        leftExp = equip.starExp - useExp
        nextUseExp = equip._getEquipStarUpExpByStarLv(equip.starLv + 1)
        if nextUseExp > leftExp:
            needShow = True
        ret['needShow'] = needShow

    def onGetToolTip(self, *arg):
        if len(self.lockSlotPos) < 1:
            return GfxValue('')
        equip = self.getCurrentEquip()
        if not equip:
            return GfxValue('')
        return gameglobal.rds.ui.inventory.GfxToolTip(equip)

    def isItemDisabled(self, kind, page, pos, item):
        if not self.activateMediator:
            return False
        if kind != const.RES_KIND_INV:
            return False
        if self.srcMode != SRC_MODE_INVENTORY:
            return False
        if not item.isEquip():
            return True
        if item.isWingOrRide():
            return True
        if item.isYaoPei() or item.isGuanYin():
            return True
        return (page, pos) in self.lockSlotPos

    def onClickYunchuiBtn(self, *arg):
        mall = gameglobal.rds.ui.tianyuMall
        if mall.mallMediator:
            mall.hide()
        mall.show(keyWord='云垂积分')
