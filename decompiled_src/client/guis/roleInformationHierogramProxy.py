#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/roleInformationHierogramProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import utils
from guis.uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from gameclass import PSkillInfo
import gameconfigCommon
import gametypes
from gameStrings import gameStrings
from ui import unicode2gbk
from data import rune_data as RD
from data import rune_effect_data as RED
from data import sys_config_data as SCD
from cdata import hiero_equip_data as HED
from cdata import hiero_awake_rule_data as HARD
from cdata import game_msg_def_data as GMDD
dleffectDict = {0: (0, 1, 2),
 1: (3, 4, 5),
 2: (6, 7, 8),
 3: (9, 10, 11)}

class RoleInformationHierogramProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(RoleInformationHierogramProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getHieroInfo': self.onGetHieroInfo,
         'clickHierogramItem': self.onClickHierogramItem,
         'runeView': self.onRuneView,
         'resetFunc': self.onResetFunc,
         'getTransNum': self.onGetTransNum,
         'shareHierogram': self.onShareHierogram,
         'openRuneInv': self.onOpenRuneInv,
         'openEquipChange': self.onOpenEquipChange,
         'enableRuneInv': self.onEnableRuneInv}
        self.panelMc = None
        self.bindType = 'hieroRole'
        self.type = 'hieroRole'
        self.reset()

    def onRegisterMc(self, *args):
        self.panelMc = args[3][0]

    def onUnRegisterMc(self, *args):
        self.panelMc = None

    def reset(self):
        pass

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        p = BigWorld.player()
        item = None
        if bar == uiConst.HIERO_TYPE_EQUIP:
            item = p.hierogramDict.get('hieroEquip', None)
        elif bar == uiConst.HIERO_TYPE_TIANLUN:
            hieroCrystals = p.hierogramDict.get('hieroCrystals', None)
            item = hieroCrystals.get((bar, slot), None)
        elif bar == uiConst.HIERO_TYPE_DILUN:
            hieroCrystals = p.hierogramDict.get('hieroCrystals', None)
            item = hieroCrystals.get((bar, slot), None)
        elif bar == uiConst.HIERO_TYPE_BENYUAN:
            hieroCrystals = p.hierogramDict.get('hieroCrystals', None)
            item = hieroCrystals.get((bar, slot), None)
        return self.uiAdapter.inventory.GfxToolTip(item)

    def onGetHieroInfo(self, *args):
        ret = {}
        p = BigWorld.player()
        self.appendInitSlotOpenData(ret, p.lv)
        self.appendEquipData(ret, p.hierogramDict)
        self.appendPSkillData(ret, p.hierogramDict)
        self.appendWakeData(ret, p.hierogramDict)
        self.appendEffectData(ret, p.hierogramDict)
        ret['isTrans'] = p.isClearAndTransitToHierogram()
        return uiUtils.dict2GfxDict(ret, True)

    def appendEffectData(self, ret, hierogramDict):
        p = BigWorld.player()
        info = None
        if hierogramDict:
            hieroCrystals = hierogramDict.get('hieroCrystals', {})
            curEquipCrystalValidDataDict = p.getCurEquipCrystalItemValidData(hieroCrystals)
            tlNum = 0
            dlEffect = ()
            tianlunEffect = 0
            for hType, hPart in hieroCrystals:
                if not curEquipCrystalValidDataDict.get((hType, hPart), True):
                    continue
                if hType == uiConst.HIERO_TYPE_TIANLUN:
                    tlNum += 1
                elif hType == uiConst.HIERO_TYPE_DILUN:
                    dlEffect += dleffectDict[hPart]

            if tlNum >= uiConst.HIERO_TIANLUN_NUM:
                tianlunEffect = 1
            info = {'tlEffect': tianlunEffect,
             'dlEffect': dlEffect}
        ret['effectInfo'] = info

    def appendWakeData(self, ret, hierogramDict):
        p = BigWorld.player()
        info = None
        hieroEquipItem = hierogramDict.get('hieroEquip', None)
        if hieroEquipItem:
            tianlunWake = []
            tlCrystalLvSum = 0
            dilunWake = []
            dlCrystalLvSum = 0
            hieroCrystals = hierogramDict.get('hieroCrystals', None)
            curEquipCrystalValidDataDict = p.getCurEquipCrystalItemValidData(hieroCrystals)
            if hieroCrystals:
                for hType, hPart in hieroCrystals:
                    if not curEquipCrystalValidDataDict.get((hType, hPart), True):
                        continue
                    crystalItemID = hieroCrystals[hType, hPart].id
                    if hType == uiConst.HIERO_TYPE_TIANLUN:
                        tlCrystalLvSum += p.getRuneData(crystalItemID, 'lv', 0)
                    elif hType == uiConst.HIERO_TYPE_DILUN:
                        dlCrystalLvSum += p.getRuneData(crystalItemID, 'lv', 0)

            _tlNumStr = gameStrings.TEXT_ROLEINFORMATIONHIEROGRAMPROXY_141 % tlCrystalLvSum
            ruleIds = self.getRulesIDofEquipAwake(hieroEquipItem.id, uiConst.HIERO_TYPE_TIANLUN)
            for rid in ruleIds:
                match, sumLimit, _str = self.getAwakeRuleSumCondition(uiConst.HIERO_TYPE_TIANLUN, rid)
                if match:
                    if tlCrystalLvSum >= sumLimit:
                        tianlunWake.append((_str, True))
                    else:
                        tianlunWake.append((_str, False))

            _dlNumStr = gameStrings.TEXT_ROLEINFORMATIONHIEROGRAMPROXY_152 % dlCrystalLvSum
            ruleIds = self.getRulesIDofEquipAwake(hieroEquipItem.id, uiConst.HIERO_TYPE_DILUN)
            for rid in ruleIds:
                match, sumLimit, _str = self.getAwakeRuleSumCondition(uiConst.HIERO_TYPE_DILUN, rid)
                if match:
                    if dlCrystalLvSum >= sumLimit:
                        dilunWake.append((_str, True))
                    else:
                        dilunWake.append((_str, False))

            info = {'tianlunWakeNum': (_tlNumStr, True),
             'tianlunWake': tianlunWake,
             'dilunWakeNum': (_dlNumStr, True),
             'dilunWake': dilunWake}
        ret['wakeInfo'] = info

    def getAwakeRuleSumCondition(self, hieroType, ruleID):
        sumLimit = HARD.data.get(ruleID, {}).get('awakeSumCondition', 0)
        typeCondition = HARD.data.get(ruleID, {}).get('hieroAwakeType', -1)
        detail = HARD.data.get(ruleID, {}).get('detail', -1)
        if hieroType == typeCondition:
            return (True, sumLimit, detail)
        else:
            return (False, 0, detail)

    def getRulesIDofEquipAwake(self, equipItemID, hieroType):
        if uiConst.HIERO_TYPE_TIANLUN == hieroType:
            return HED.data.get(equipItemID, {}).get('tianlunAwakeRules', ())
        if uiConst.HIERO_TYPE_DILUN == hieroType:
            return HED.data.get(equipItemID, {}).get('dilunAwakeRules', ())
        return ()

    def appendPSkillData(self, ret, hierogramDict):
        pskillArray = []
        pskillSet = hierogramDict.get('pSkills', {})
        for effectId in pskillSet:
            pskillId, pskillLv = pskillSet[effectId]
            pskill = {}
            desc = gameglobal.rds.ui.runeView.generateDesc(pskillId, PSkillInfo(pskillId, pskillLv, {}), pskillLv)
            pskill['name'] = RED.data.get(effectId, [])[pskillLv - 1].get('name', '')
            pskill['desc'] = desc
            pskillArray.append(pskill)

        info = {'pskillArray': pskillArray}
        ret['pskillInfo'] = info

    def appendEquipData(self, ret, hierogramDict, fromPage = uiConst.BAG_EQUIP_RUNE):
        if not hierogramDict:
            ret['itemInfos'] = {}
            return
        else:
            p = BigWorld.player()
            hieroCrystals = hierogramDict.get('hieroCrystals', {})
            curEquipCrystalValidDataDict = p.getCurEquipCrystalItemValidData(hieroCrystals)
            tianlunItems = []
            dilunItems = []
            benyuanItem = None
            for (hType, hPart), itemData in hieroCrystals.iteritems():
                crystalItemInfo = None
                if hType == uiConst.HIERO_TYPE_TIANLUN:
                    crystalItemInfo = self.uiAdapter.equipChangeRuneFeed.getGfxItemData(itemData, fromPage, hType, hPart)
                    tianlunItems.append((hPart, crystalItemInfo))
                elif hType == uiConst.HIERO_TYPE_DILUN:
                    crystalItemInfo = self.uiAdapter.equipChangeRuneFeed.getGfxItemData(itemData, fromPage, hType, hPart)
                    dilunItems.append((hPart, crystalItemInfo))
                elif hType == uiConst.HIERO_TYPE_BENYUAN:
                    crystalItemInfo = self.uiAdapter.equipChangeRuneFeed.getGfxItemData(itemData, fromPage, hType, hPart)
                    benyuanItem = crystalItemInfo
                if itemData and crystalItemInfo:
                    currentAddPercnet = p.getRuneAddPercent(itemData)
                    runeLv = p.getRuneData(itemData.id, 'lv', 0)
                    crystalItemInfo['feedMax'] = runeLv >= self.uiAdapter.equipChangeRuneFeed.getMinCanFeedRuneLv() and currentAddPercnet >= self.uiAdapter.equipChangeRuneFeed.getTotalMaxPercent(runeLv)
                    crystalItemInfo['isInvalid'] = not curEquipCrystalValidDataDict.get((hType, hPart), True)

            hieroEquipItem = hierogramDict.get('hieroEquip', None)
            hieroEquipItemInfo = uiUtils.getGfxItem(hieroEquipItem) if hieroEquipItem else None
            info = {'hieroEquipItem': hieroEquipItemInfo,
             'tianlunItems': tianlunItems,
             'dilunItems': dilunItems,
             'benyuanItem': benyuanItem}
            ret['itemInfos'] = info
            return

    def getCurOpenLvArr(self):
        p = BigWorld.player()
        openLvDict = SCD.data.get('HierogramSlotOpenMapByLv', {})
        openLvList = []
        openArr = [0,
         0,
         0,
         0]
        lastLv = 0
        for k, v in openLvDict.iteritems():
            if p.lv >= k and k >= lastLv:
                openArr = v
                lastLv = k

        return openArr

    def getCrystalBestPart(self, hieroType):
        p = BigWorld.player()
        curOpenLv = self.getCurOpenLvArr()
        if p.hierogramDict:
            if hieroType == uiConst.HIERO_TYPE_TIANLUN:
                for i in xrange(curOpenLv[0]):
                    if not p.hierogramDict.get('hieroCrystals').get((uiConst.HIERO_TYPE_TIANLUN, i), None):
                        return i

            elif hieroType == uiConst.HIERO_TYPE_DILUN:
                for i in xrange(curOpenLv[1]):
                    if not p.hierogramDict.get('hieroCrystals').get((uiConst.HIERO_TYPE_DILUN, i), None):
                        return i

            elif hieroType == uiConst.HIERO_TYPE_BENYUAN:
                for i in xrange(curOpenLv[2]):
                    if i == 0:
                        return i

        return -1

    def appendInitSlotOpenData(self, ret, lv):
        openLvDict = SCD.data.get('HierogramSlotOpenMapByLv', {})
        openLvList = []
        openArr = [0,
         0,
         0,
         0]
        lastLv = 0
        for k, v in openLvDict.iteritems():
            if lv >= k and k >= lastLv:
                openArr = v
                lastLv = k
            tmpV = list(v)
            tmpV.insert(0, k)
            openLvList.append(tmpV)

        openLvList.sort(key=lambda x: x[0])
        tianlun = []
        dilun = []
        benyuan = 0
        sgslot = 0
        lastList = [0,
         0,
         0,
         0,
         0]
        tlNo = 0
        dlNo = 0
        for i, v in enumerate(openLvList):
            tl = v[1] - lastList[1]
            dl = v[2] - lastList[2]
            by = v[3] - lastList[3]
            sg = v[4] - lastList[4]
            lastList = v
            if tl:
                for j in xrange(tl):
                    tianlun.append((v[0],
                     'Lv.%d' % v[0],
                     gameStrings.TEXT_ROLEINFORMATIONHIEROGRAMPROXY_310 % v[0],
                     gameStrings.TEXT_ROLEINFORMATIONHIEROGRAMPROXY_310_1))

            if dl:
                for j in xrange(dl):
                    dilun.append((v[0],
                     'Lv.%d' % v[0],
                     gameStrings.TEXT_ROLEINFORMATIONHIEROGRAMPROXY_310 % v[0],
                     gameStrings.TEXT_ROLEINFORMATIONHIEROGRAMPROXY_313))

            if by:
                benyuan = (v[0],
                 'Lv.%d' % v[0],
                 gameStrings.TEXT_ROLEINFORMATIONHIEROGRAMPROXY_310 % v[0],
                 gameStrings.TEXT_ROLEINFORMATIONHIEROGRAMPROXY_315)
            if sg:
                sgslot = (v[0],
                 'Lv.%d' % v[0],
                 gameStrings.TEXT_ROLEINFORMATIONHIEROGRAMPROXY_317 % v[0],
                 gameStrings.TEXT_ROLEINFORMATIONHIEROGRAMPROXY_317_1)

        info = {'tianlun': tianlun,
         'dilun': dilun,
         'benyuan': benyuan,
         'sgslot': sgslot,
         'openArr': openArr}
        ret['openLv'] = info

    def refreshInfo(self):
        if self.panelMc:
            self.panelMc.Invoke('refreshAllInfo')

    def onClickHierogramItem(self, *args):
        p = BigWorld.player()
        key = unicode2gbk(args[3][0].GetString())
        hieroType, part = self.getSlotID(key)
        if self.uiAdapter.equipChange.mediator:
            BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
            return
        else:
            it = None
            if hieroType == uiConst.HIERO_TYPE_EQUIP:
                if p.hierogramDict:
                    it = p.hierogramDict.get('hieroEquip', None)
            elif p.hierogramDict:
                it = p.hierogramDict.get('hieroCrystals', {}).get((hieroType, part), None)
            if not it:
                return
            emptyPg, emptyPos = p.inv.searchBestInPages(it.id, it.cwrap, it)
            if emptyPg != const.CONT_NO_PAGE:
                if hieroType == uiConst.HIERO_TYPE_EQUIP:
                    p.cell.unEquipHieroEquipment(emptyPg, emptyPos)
                else:
                    p.cell.removeHieroCrystal(hieroType, part, emptyPg, emptyPos)
            else:
                msgId = GMDD.data.HIERO_EQUIP_BAG_FULL if hieroType == uiConst.HIERO_TYPE_EQUIP else GMDD.data.HIERO_BAG_FULL
                p.showGameMsg(msgId, ())
            return

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[9:]), int(idItem[4:]))

    def onRuneView(self, *args):
        if not gameglobal.rds.ui.runeView.mediator:
            gameglobal.rds.ui.runeView.show()

    def onResetFunc(self, *args):
        p = BigWorld.player()
        p.cell.clearAndTransitToHierogram()

    def isLegitimateSlot(self, opType, _type, part = None):
        p = BigWorld.player()
        openArr = self.getCurOpenLvArr()
        hieroCrystals = p.hierogramDict.get('hieroCrystals', None)
        tlCrystalSum = 0
        dlCrystalSum = 0
        if hieroCrystals:
            for hType, hPart in hieroCrystals:
                crystalItemID = hieroCrystals[hType, hPart].id
                if hType == uiConst.HIERO_TYPE_TIANLUN:
                    tlCrystalSum += 1
                elif hType == uiConst.HIERO_TYPE_DILUN:
                    dlCrystalSum += 1

        if opType == uiConst.HIERO_CLICK_BAG_ITEM:
            if _type == uiConst.HIERO_TYPE_EQUIP:
                if openArr[3] == 0:
                    p.showGameMsg(GMDD.data.HIERO_EQUIP_LV_LIMIT, ())
                    return False
            elif _type == uiConst.HIERO_TYPE_TIANLUN:
                if tlCrystalSum >= openArr[0] and openArr[0] < uiConst.HIERO_TIANLUN_NUM:
                    p.showGameMsg(GMDD.data.HIERO_CRYSTAL_LV_LIMIT, ())
                    return False
                if self.getCrystalBestPart(uiConst.HIERO_TYPE_TIANLUN) == -1:
                    p.showGameMsg(GMDD.data.HIERO_CRYSTAL_NUM_FULL, ())
                    return False
            elif _type == uiConst.HIERO_TYPE_DILUN:
                if dlCrystalSum >= openArr[0] and openArr[1] < uiConst.HIERO_DILUN_NUM:
                    p.showGameMsg(GMDD.data.HIERO_CRYSTAL_LV_LIMIT, ())
                    return False
                if self.getCrystalBestPart(uiConst.HIERO_TYPE_DILUN) == -1:
                    p.showGameMsg(GMDD.data.HIERO_CRYSTAL_NUM_FULL, ())
                    return False
            elif _type == uiConst.HIERO_TYPE_BENYUAN:
                if openArr[2] == 0:
                    p.showGameMsg(GMDD.data.HIERO_CRYSTAL_LV_LIMIT, ())
                    return False
        elif opType == uiConst.HIERO_DRAG_BAG_ITEM:
            if _type == uiConst.HIERO_TYPE_EQUIP:
                if openArr[3] == 0:
                    p.showGameMsg(GMDD.data.HIERO_EQUIP_LV_LIMIT, ())
                    return False
            elif _type == uiConst.HIERO_TYPE_TIANLUN:
                if part and part + 1 > openArr[0]:
                    p.showGameMsg(GMDD.data.HIERO_CRYSTAL_LV_LIMIT, ())
                    return False
            elif _type == uiConst.HIERO_TYPE_DILUN:
                if part and part + 1 > openArr[1]:
                    p.showGameMsg(GMDD.data.HIERO_CRYSTAL_LV_LIMIT, ())
                    return False
            elif _type == uiConst.HIERO_TYPE_BENYUAN:
                if openArr[2] == 0:
                    p.showGameMsg(GMDD.data.HIERO_CRYSTAL_LV_LIMIT, ())
                    return False
        return True

    def onGetTransNum(self, *args):
        p = BigWorld.player()
        ret = {}
        transNum = 0
        runeEquipItem = None
        runeCrystals = None
        if p.runeBoard:
            runeEquipItem = p.runeBoard.runeEquip
        if runeEquipItem:
            transNum += 1
            for runeDataVal in p.runeBoard.runeEquip.runeData:
                if runeDataVal.item:
                    transNum += 1

        _str = gameStrings.TEXT_ROLEINFOPROXY_4481 % transNum
        ret = {'transNum': transNum,
         'transStr': _str}
        return uiUtils.dict2GfxDict(ret, True)

    def isHasAvailablePos(self):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableHierogram', False) and p.hierogramDict:
            ret = {}
            self.appendInitSlotOpenData(ret, p.lv)
            self.appendEquipData(ret, p.hierogramDict)
            if ret.get('openLv', {}).get('openArr', [0,
             0,
             0,
             0])[3] > 0 and not ret.get('itemInfos', {}).get('hieroEquipItem', None):
                return True
            if ret.get('openLv', {}).get('openArr', [0,
             0,
             0,
             0])[2] > 0 and not ret.get('itemInfos', {}).get('benyuanItem', None):
                return True
            if ret.get('openLv', {}).get('openArr', [0,
             0,
             0,
             0])[1] > len(ret.get('itemInfos', {}).get('dilunItems', [])):
                return True
            if ret.get('openLv', {}).get('openArr', [0,
             0,
             0,
             0])[0] > len(ret.get('itemInfos', {}).get('tianlunItems', [])):
                return True
        return False

    def onShareHierogram(self, *args):
        p = BigWorld.player()
        if p._isSoul():
            p.showGameMsg(GMDD.data.HIEROGRAM_SHARE_NOT_AVALIABLE_CROSS, ())
            return
        roleName = p.roleName
        msg = gameStrings.HIEROGRAM_SHARE_TXT % (roleName, utils.getHostId(), roleName)
        gameglobal.rds.ui.sendLink(msg)

    def onOpenRuneInv(self, *args):
        self.uiAdapter.runeInv.show()

    def onOpenEquipChange(self, *args):
        self.uiAdapter.equipChange.show(uiConst.EQUIPCHANGE_TAB_RUNE)

    def onEnableRuneInv(self, *args):
        return GfxValue(gameconfigCommon.enableHierogramBag() and BigWorld.player().checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_HIEROGRAM))
