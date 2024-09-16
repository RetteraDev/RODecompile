#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipPushProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import utils
import commcalc
from uiProxy import UIProxy
from helpers import cellCmd
from guis import uiUtils
from guis import ui
from data import item_data as ID
from cdata import font_config_data as FCD
from data import equip_prefix_prop_data as EPPD
from data import prop_ref_data as PRD
from data import radar_chart_dimension_data as RCDD
from cdata import game_msg_def_data as GMDD

class EquipPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipPushProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickHide': self.onClickHide,
         'exchangeEquip': self.onExchangeEquip,
         'initData': self.onInitData}
        self.mediator = None
        self.uuid = None
        self.item = None
        self.dataList = []

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_PUSH:
            self.mediator = mediator

    def refresh(self):
        pass

    def pushShow(self):
        dataTuple = tuple(gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_GET_EQUIP))
        for item in dataTuple:
            self.dataList.append(item['data'])
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_GET_EQUIP, {'data': item['data']})

        self.show()

    def show(self):
        if self.mediator:
            return
        else:
            if self.dataList:
                self.uuid = self.dataList.pop()
                item, _, _ = BigWorld.player().inv.findItemByUUID(self.uuid)
                if item == const.CONT_EMPTY_VAL:
                    self.uuid = None
                    return
                self.item = item.deepcopy()
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_PUSH)
            return

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_PUSH)

    def reset(self):
        self.uuid = None
        self.item = None
        self.dataList = []

    def forceColse(self, uuid):
        if uuid == self.uuid:
            self.close()
        elif uuid in self.dataList:
            self.dataList.remove(uuid)
        else:
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_GET_EQUIP, {'data': uuid})

    def close(self):
        self.clearWidget()
        self.uuid = None
        self.item = None
        if self.dataList:
            self.show()

    def onClickClose(self, *arg):
        self.close()

    def onClickHide(self, *arg):
        dataList = tuple(self.dataList)
        self.dataList = []
        for uuid in dataList:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_EQUIP, {'data': uuid})

        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_EQUIP, {'data': self.uuid})
        self.close()

    def onExchangeEquip(self, *arg):
        item, page, pos = BigWorld.player().inv.findItemByUUID(self.uuid)
        self.exchangeEquip(page, pos, item)

    @ui.looseGroupTradeConfirm([1, 2], GMDD.data.RETURN_BACK_EQUIP)
    def exchangeEquip(self, page, pos, item):
        if page == const.CONT_NO_PAGE:
            self.close()
        else:
            dstPos = BigWorld.player().getBestMainEquipPart(self.item)
            if gameglobal.rds.configData.get('enableWardrobe', False) and BigWorld.player().isWardrobeCloth(item):
                if not cellCmd.equipWardrobeItemFromInv(page, pos, item):
                    cellCmd.exchangeInvEqu(page, pos, dstPos)
            else:
                cellCmd.exchangeInvEqu(page, pos, dstPos)

    def onInitData(self, *arg):
        if not self.item:
            self.close()
            return
        dataObj = {}
        dataObj['score'] = self.item.score
        dataObj['icon'] = uiUtils.getItemIconFile64(self.item.id)
        if hasattr(self.item, 'quality'):
            quality = self.item.quality
        else:
            quality = ID.data.get(self.item.id, {}).get('quality', 1)
        dataObj['qualitycolor'] = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        itemName = self.item.name
        if hasattr(self.item, 'prefixInfo'):
            for prefixItem in EPPD.data[self.item.prefixInfo[0]]:
                if prefixItem['id'] == self.item.prefixInfo[1]:
                    if utils.isInternationalVersion():
                        itemName = self.item.name + prefixItem['name']
                    else:
                        itemName = prefixItem['name'] + self.item.name
                    break

        dataObj['itemName'] = itemName
        dataObj['attackScore'] = self.calcAttackScore()
        return uiUtils.dict2GfxDict(dataObj, True)

    def calcAttackScore(self):
        p = BigWorld.player()
        dstPos = p.getBestMainEquipPart(self.item)
        oldEquips = [ equip for equip in p.equipment if equip ]
        equips = [ equip for equip in p.equipment if equip and equip != p.equipment[dstPos] ]
        equips.append(self.item)
        pskills = []
        for pskVal in p.pskills.values():
            for subVal in pskVal.values():
                pskills.append(subVal)

        titles = []
        propsFilter = []
        for idx in xrange(1, 6):
            data = RCDD.data.get(idx, {})
            propsFilter += data.get('formual1Params%d' % (p.realSchool - 2), [])

        propsFilter = [ PRD.data.get(id, {}).get('property', 0) for id in propsFilter ]
        oldProps = commcalc.calcSelfPropVal(p, oldEquips, pskills, titles)
        oldPreview = commcalc.calcAllPropVal(p, oldProps, oldEquips, pskills, titles, propsFilter)
        oldRet = commcalc.createRadarChartData(p, oldPreview, True)
        props = commcalc.calcSelfPropVal(p, equips, pskills, titles)
        preview = commcalc.calcAllPropVal(p, props, equips, pskills, titles, propsFilter)
        ret = commcalc.createRadarChartData(p, preview, True)
        return int(ret[0]) + int(ret[1]) + int(ret[2]) + int(ret[3]) + int(ret[4]) - int(oldRet[0]) - int(oldRet[1]) - int(oldRet[2]) - int(oldRet[3]) - int(oldRet[4])

    def onGetToolTip(self, *arg):
        return gameglobal.rds.ui.inventory.GfxToolTip(self.item)
