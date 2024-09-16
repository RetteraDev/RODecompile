#Embedded file name: I:/bag/tmp/tw2/res/entities\common/subEquipment.o
import BigWorld
if BigWorld.component in ('base', 'cell'):
    import serverlog
    import Netease
    import logconst
    from data import log_src_def_data as LSDD
import const
from inventoryCommon import InventoryCommon
from data import zaiju_data as ZJD
from data import school_switch_general_data as SSGD

class SubEquipment(InventoryCommon):

    def __init__(self, pageCount = const.SUB_EQUIP_PAGE_NUM, width = const.SUB_EQUIP_WIDTH, height = const.SUB_EQUIP_HEIGHT):
        super(SubEquipment, self).__init__(pageCount, width, height, const.RES_KIND_SUB_EQUIP_BAG)
        self.version = 0
        self.freeze = 0

    def howManyItem(self):
        cnt = 0
        for pg in xrange(self.pageCount):
            for ps in xrange(self.posCount):
                if not self.isEmpty(pg, ps):
                    cnt += 1

        return cnt

    def isFill(self, page, pos):
        if not self._isValid(page, pos):
            return False
        return not self.isEmpty(page, pos)

    def get(self, page, pos):
        if not self._isValid(page, pos):
            return None
        it = self.getQuickVal(page, pos)
        return it

    def removeItem(self, owner, page, pos, opNUID, logSrc, detail = ''):
        if not self._isValid(page, pos):
            return False
        if self.isEmpty(page, pos):
            return False
        it = self.getQuickVal(page, pos)
        self.setQuickVal(const.CONT_EMPTY_VAL, page, pos)
        owner.client.resRemove(const.RES_KIND_SUB_EQUIP_BAG, page, pos)
        owner.logItem(it, -it.cwrap, opNUID, logSrc, fromGuid=[], toGuid=it.popProp('toGuid'), detail=detail, bagType=const.RES_KIND_SUB_EQUIP_BAG)
        return True

    def insertItem(self, owner, item, page, pos, opNUID, logSrc, detail = ''):
        if not self._isValid(page, pos):
            return False
        if self.getQuickVal(page, pos) != const.CONT_EMPTY_VAL:
            return False
        if item.isEquipBind():
            oldEquipIt = item.deepcopy()
            item.bindItem()
            if BigWorld.component in ('base', 'cell'):
                opNUID = Netease.getNUID()
                serverlog.genItemLog(owner, oldEquipIt, 0, opNUID, LSDD.data.LOG_SRC_EQUIP_ITEM, detail=logconst.ITEM_EQUIP_BIND)
        self.insertObj(item, page, pos)
        owner.client.resInsert(self.RES_KIND, item, page, pos)
        owner.logItem(item, item.cwrap, opNUID, logSrc, fromGuid=item.popProp('fromGuid'), toGuid=[], detail=detail, bagType=const.RES_KIND_SUB_EQUIP_BAG)
        return True

    def isValid(self, page, pos):
        if self._isValidPage(page) and self._isValidPos(pos):
            return True
        else:
            return False

    def transfer(self, owner):
        return super(SubEquipment, self).transfer(owner, resKind=const.RES_KIND_SUB_EQUIP_BAG)

    def refuseChangeEquip(self, owner):
        if owner._isOnZaijuOrBianyao():
            zaijuNo = owner._getZaijuOrBianyaoNo()
            return ZJD.data[zaijuNo].get('isEquipLock', 0) > 0
        elif owner._isSchoolSwitch():
            switchNo = owner._getSchoolSwitchNo()
            return SSGD.data[switchNo].get('isEquipLock', 0) > 0
        else:
            return False

    def isRefuse(self, owner = None):
        if self.freeze != 0:
            return True
        if owner and self.refuseChangeEquip(owner):
            return True
        return False

    def getSendData(self, changeToItem = True):
        data = [ [ None for i in xrange(self.posCount) ] for j in xrange(self.pageCount) ]
        for pg in xrange(self.pageCount):
            for ps in xrange(self.posCount):
                it = self.getQuickVal(pg, ps, changeToItem=changeToItem)
                if it == const.CONT_EMPTY_VAL:
                    continue
                data[pg][ps] = it.copyDict()

        return data

    def updateItem(self, owner, page, pos, props):
        if not self._isValid(page, pos):
            return False
        it = self.getQuickVal(page, pos)
        if it != const.CONT_EMPTY_VAL:
            self.updateObj(it.uuid, page, pos, props)
            owner.client.resSetProps(self.RES_KIND, it.uuid, page, pos, props)
        return True
