#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipFeedProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import const
import utils
from guis import ui
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from callbackHelper import Functor
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from cdata import font_config_data as FCD
from data import game_msg_data as GMD
from data import equip_data as ED
from cdata import equip_star_factor_data as ESFCD
from data import prop_ref_data as PRD
from data import equip_prefix_prop_data as EPPD
from cdata import equip_star_feed_data as ESFD
from data import formula_client_data as FMCD
from cdata import equip_star_lv_up_data as ESLUD
from cdata import equip_special_props_data as ESPD
from cdata import equip_quality_factor_data as EQFD
STATE_CAN_NOT_LV_UP = 0
STATE_CAN_LV_UP = 1
STATE_LV_MAX = 2

class EquipFeedProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipFeedProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'feedEquip': self.onFeedEquip,
         'removeItem': self.onRemoveItem}
        self.type = 'equipFeed'
        self.bindType = 'equipFeed'
        self.mediator = None
        self.posMap = {}
        self.isInBag = True
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_FEED, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_FEED:
            self.mediator = mediator

    def clearWidget(self):
        for i in xrange(0, 6):
            self.removeItem(0, i)

        self.mediator = None
        self.posMap = {}
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_FEED)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_FEED)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[9:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'equipFeed%d.slot%d' % (bar, slot)

    def setItem(self, srcBar, srcSlot, destBar, destSlot, it, inBag = True):
        if destSlot == 0:
            self.isInBag = inBag
        key = self._getKey(destBar, destSlot)
        if self.binding.has_key(key):
            self.bindingData[key] = it
            if inBag:
                if self.posMap.has_key((destBar, destSlot)):
                    gameglobal.rds.ui.inventory.updateSlotState(self.posMap[destBar, destSlot][0], self.posMap[destBar, destSlot][1])
                    gameglobal.rds.ui.actionbar._setItemSlotState(self.posMap[destBar, destSlot][0], self.posMap[destBar, destSlot][1], uiConst.ITEM_NORMAL)
                gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
            else:
                if self.posMap.has_key((destBar, destSlot)):
                    gameglobal.rds.ui.inventory.updateSlotState(self.posMap[destBar, destSlot][0], self.posMap[destBar, destSlot][1])
                    gameglobal.rds.ui.actionbar._setItemSlotState(self.posMap[destBar, destSlot][0], self.posMap[destBar, destSlot][1], uiConst.ITEM_NORMAL)
                gameglobal.rds.ui.actionbar._setItemSlotState(srcBar, srcSlot, uiConst.ITEM_DISABLE)
            iconPath = uiUtils.getItemIconFile40(it.id)
            count = it.cwrap
            data = {'iconPath': iconPath,
             'count': count}
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
            if hasattr(it, 'quality'):
                quality = it.quality
            else:
                quality = ID.data.get(it.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
            self.posMap[destBar, destSlot] = (srcBar, srcSlot)
            self.refreshContent()

    def removeItem(self, bar, slot):
        key = self._getKey(bar, slot)
        if self.binding.has_key(key):
            self.bindingData[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            if self.posMap.has_key((bar, slot)):
                if not self.isInBag and slot == 0:
                    gameglobal.rds.ui.actionbar._setItemSlotState(self.posMap[bar, slot][0], self.posMap[bar, slot][1], uiConst.ITEM_NORMAL)
                    part = self.posMap[bar, slot][1]
                    item = BigWorld.player().equipment[part]
                    gameglobal.rds.ui.actionbar.setEquipSlotState(item, part)
                else:
                    gameglobal.rds.ui.inventory.updateSlotState(self.posMap[bar, slot][0], self.posMap[bar, slot][1])
                self.posMap.pop((bar, slot))
            self.refreshContent()

    def refreshContent(self, feedSucc = False):
        srcKey = self._getKey(0, 0)
        feedKey = [ self._getKey(0, pos) for pos in xrange(1, 6) ]
        if feedSucc:
            p = BigWorld.player()
            srcIt = None
            if self.posMap.has_key((0, 0)):
                if self.isInBag:
                    srcIt = p.inv.getQuickVal(*self.posMap[0, 0])
                else:
                    srcIt = p.equipment[self.posMap[0, 0][1]]
                self.setItem(self.posMap[0, 0][0], self.posMap[0, 0][1], 0, 0, srcIt, self.isInBag)
                gameglobal.rds.ui.inventory.updateSlotState(self.posMap[0, 0][0], self.posMap[0, 0][1])
                gameglobal.rds.ui.actionbar._setItemSlotState(self.posMap[0, 0][0], self.posMap[0, 0][1], uiConst.ITEM_DISABLE)
            feedIt = []
            for pos in xrange(1, 6):
                it = None
                if self.posMap.has_key((0, pos)):
                    it = p.inv.getQuickVal(*self.posMap[0, pos])
                    self.bindingData[self._getKey(0, pos)] = it
                    gameglobal.rds.ui.inventory.updateSlotState(self.posMap[0, 0][0], self.posMap[0, 0][1])
                if not it:
                    self.removeItem(0, pos)
                feedIt.append(it)

        else:
            srcIt = self.bindingData.get(srcKey, None)
            feedIt = [ self.bindingData.get(fk, None) for fk in feedKey ]
        props = ''
        if srcIt and hasattr(srcIt, 'starExp'):
            starExp = srcIt.starExp
            if hasattr(srcIt, 'starLv'):
                starLv = srcIt.starLv
            else:
                starLv = 0
                maxStarLv = 0
            starExpData = ESLUD.data.get(srcIt.starLv, {})
            lvUpFormula = starExpData.get('upExp')
            maxStarExp = 0
            if lvUpFormula:
                maxStarExp = srcIt.evalValue(lvUpFormula[0], lvUpFormula[1:])
        else:
            starExp = 0
            maxStarExp = 0
            starLv = 0
        maxStarLv = getattr(srcIt, 'maxStarLv', -1)
        srcItemName = ''
        if srcIt:
            srcItemName = srcIt.name
            if hasattr(srcIt, 'prefixInfo'):
                for prefixItem in EPPD.data[srcIt.prefixInfo[0]]:
                    if prefixItem['id'] == srcIt.prefixInfo[1]:
                        if utils.isInternationalVersion():
                            srcItemName = srcIt.name + prefixItem['name']
                        else:
                            srcItemName = prefixItem['name'] + srcIt.name
                        break

        feedItemName = ''
        addExp = 0
        for fIt in feedIt:
            if fIt:
                equipData = ED.data.get(fIt.id, {})
                etp = equipData.get('equipType', -1)
                srcQuality = getattr(srcIt, 'quality', 0)
                equipSType = getattr(fIt, 'equipSType', 0)
                expFormula = ESFD.data.get((srcQuality, etp, equipSType), {}).get('exp')
                if expFormula:
                    formulaId, formulaParams = expFormula[0], expFormula[1:]
                    fd = FMCD.data.get(formulaId)
                    formula = fd.get('formula')
                    if formula:
                        exp = fIt.evalValue(formulaId, formulaParams, {'totalStarExp': fIt.calcTotalStarExp()})
                        exp *= equipData.get('equipFeedFactor', 1.0)
                        addExp += exp

        if srcIt:
            if starLv == maxStarLv:
                state = STATE_LV_MAX
            elif starExp + addExp >= maxStarExp:
                state = STATE_CAN_LV_UP
            else:
                state = STATE_CAN_NOT_LV_UP
            props = self._createPropsString(srcIt, state)
        ret = [srcItemName,
         starLv,
         maxStarLv,
         props,
         feedItemName,
         starExp,
         maxStarExp,
         addExp,
         self.validateItems(),
         0]
        if self.mediator != None:
            self.mediator.Invoke('setContent', uiUtils.array2GfxAarry(ret, True))

    def findEmptyPos(self):
        for i in xrange(0, 6):
            key = (0, i)
            if not self.posMap.has_key(key):
                return i

        return -1

    def _createPropsString(self, i, canLvUp):
        ret = ''
        starLv = getattr(i, 'starLv', -1)
        nextStarLv = starLv + 1 if starLv != -1 else -1
        starFactor = ESFCD.data.get(starLv, {}).get('factor', 1.0)
        nextStarFactor = ESFCD.data.get(nextStarLv, {}).get('factor', 1.0)
        quality = getattr(i, 'quality', 1)
        if not quality:
            quality = 1
        qualityFactor = EQFD.data.get(quality, {}).get('factor', 1.0)
        basic = []
        if hasattr(i, 'props'):
            for pid, pType, pVal in i.props:
                if pType == gametypes.DATA_TYPE_NUM and i._isIntPropRef(pid):
                    basic.append((pid,
                     pType,
                     int(round(pVal * starFactor) * qualityFactor),
                     int(round(pVal * (nextStarFactor - starFactor) * qualityFactor))))
                else:
                    basic.append((pid,
                     pType,
                     pVal * starFactor * qualityFactor,
                     pVal * (nextStarFactor - starFactor) * qualityFactor))

        basicProp = ''
        if basic:
            if ED.data[i.id]['equipType'] == 1:
                newBasic = []
                for item in basic:
                    if item[0] == 118:
                        basicProp += gameStrings.TEXT_EQUIPFEEDPROXY_257 + str(item[2]) + '-'
                        addProp = item[3]
                    elif item[0] == 119:
                        basicProp += str(item[2])
                        if canLvUp == STATE_CAN_LV_UP:
                            basicProp += " <font color = \'#ffb91c\'>(+%d-%d)</font>\n" % (addProp, item[3])
                        elif canLvUp == STATE_CAN_NOT_LV_UP:
                            basicProp += " <font color = \'#808080\'>(+%d-%d)</font>\n" % (addProp, item[3])
                        else:
                            basicProp += '\n'
                    else:
                        newBasic.append(item)

                basic = newBasic
                newBasic = []
                for item in basic:
                    if item[0] == 120:
                        basicProp += gameStrings.TEXT_EQUIPFEEDPROXY_274 + str(item[2]) + '-'
                        addProp = item[3]
                    elif item[0] == 121:
                        basicProp += str(item[2])
                        if canLvUp == STATE_CAN_LV_UP:
                            basicProp += " <font color = \'#ffb91c\'>(+%d-%d)</font>\n" % (addProp, item[3])
                        elif canLvUp == STATE_CAN_NOT_LV_UP:
                            basicProp += " <font color = \'#808080\'>(+%d-%d)</font>\n" % (addProp, item[3])
                        else:
                            basicProp += '\n'
                    else:
                        newBasic.append(item)

                basic = newBasic
            for item in basic:
                info = PRD.data[item[0]]
                basicProp += info['name'] + '  '
                if info['showType'] == 0:
                    basicProp += str(int(item[2]))
                    if canLvUp == STATE_CAN_LV_UP:
                        basicProp += " <font color = \'#ffb91c\'>(+%d)</font>" % int(item[3])
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        basicProp += " <font color = \'#808080\'>(+%d)</font>" % int(item[3])
                elif info['showType'] == 2:
                    basicProp += str(round(item[2], 1))
                    if canLvUp == STATE_CAN_LV_UP:
                        basicProp += " <font color = \'#ffb91c\'>(+%.1f)</font>" % round(item[3], 1)
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        basicProp += " <font color = \'#808080\'>(+%.1f)</font>" % round(item[3], 1)
                else:
                    basicProp += str(round(item[2] * 100, 1)) + '%'
                    if canLvUp == STATE_CAN_LV_UP:
                        basicProp += " <font color = \'#ffb91c\'>(+" + str(round(item[2] * 100, 1)) + '%)</font>'
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        basicProp += " <font color = \'#808080\'>(+" + str(round(item[2] * 100, 1)) + '%)</font>'
                basicProp += '\n'

            ret += basicProp + '\n'
        prefixProp = ''
        if hasattr(i, 'preprops'):
            preprops = i.preprops
            preprops = [ tuple(list(pp) + [PRD.data[pp[0]]['priorityLevel'], PRD.data[pp[0]]['showColor'], pp[2] * (nextStarFactor - starFactor) * qualityFactor]) for pp in preprops ]
            preprops.sort(key=lambda k: k[3])
            for item in preprops:
                info = PRD.data[item[0]]
                prefixProp += "<font color = \'#73E539\'>" + info['name'] + '</font> '
                if info['type'] == 2:
                    prefixProp += "<font color = \'#BBFF99\'>+"
                elif info['type'] == 1:
                    prefixProp += "<font color = \'#BBFF99\'>-"
                if info['showType'] == 0:
                    prefixProp += str(int(round(item[2] * starFactor * qualityFactor))) + '</font>'
                    if canLvUp == STATE_CAN_LV_UP:
                        prefixProp += " <font color = \'#ffb91c\'>(+%d)</font>" % int(item[5])
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        prefixProp += " <font color = \'#808080\'>(+%d)</font>" % int(item[5])
                elif info['showType'] == 2:
                    prefixProp += str(round(item[2] * starFactor * qualityFactor, 1)) + '</font>'
                    if canLvUp == STATE_CAN_LV_UP:
                        prefixProp += " <font color = \'#ffb91c\'>(+%.1f)</font>" % round(item[5], 1)
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        prefixProp += " <font color = \'#808080\'>(+%.1f)</font>" % round(item[5], 1)
                else:
                    prefixProp += str(round(item[2] * 100 * starFactor * qualityFactor, 1)) + '%</font>'
                    if canLvUp == STATE_CAN_LV_UP:
                        prefixProp += " <font color = \'#ffb91c\'>(+" + str(round(item[5] * 100, 1)) + '%)</font>'
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        prefixProp += " <font color = \'#808080\'>(+" + str(round(item[5] * 100, 1)) + '%)</font>'
                prefixProp += '\n'

            ret += prefixProp + '\n'
        fixedProp = ''
        if hasattr(i, 'extraProps'):
            fixed = i.extraProps
            fixed = [ tuple(list(f) + [PRD.data[f[0]]['priorityLevel'], PRD.data[f[0]]['showColor'], f[2] * (nextStarFactor - starFactor) * qualityFactor]) for f in fixed ]
            fixed.sort(key=lambda k: k[3])
            for item in fixed:
                info = PRD.data[item[0]]
                fixedProp += "<font color = \'#2491FF\'>" + info['name'] + '</font> '
                if info['type'] == 2:
                    fixedProp += "<font color = \'#99CCFF\'>+"
                elif info['type'] == 1:
                    fixedProp += "<font color = \'#99CCFF\'>-"
                if info['showType'] == 0:
                    fixedProp += str(int(round(item[2] * starFactor * qualityFactor))) + '</font>'
                    if canLvUp == STATE_CAN_LV_UP:
                        fixedProp += " <font color = \'#ffb91c\'>(+%d)</font>" % int(item[5])
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        fixedProp += " <font color = \'#808080\'>(+%d)</font>" % int(item[5])
                elif info['showType'] == 2:
                    fixedProp += str(round(item[2] * starFactor * qualityFactor, 1)) + '</font>'
                    if canLvUp == STATE_CAN_LV_UP:
                        fixedProp += " <font color = \'#ffb91c\'>(+%.1f)</font>" % round(item[5], 1)
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        fixedProp += " <font color = \'#808080\'>(+%.1f)</font>" % round(item[5], 1)
                else:
                    fixedProp += str(round(item[2] * 100 * starFactor * qualityFactor, 1)) + '%</font>'
                    if canLvUp == STATE_CAN_LV_UP:
                        fixedProp += " <font color = \'#ffb91c\'>(+" + str(round(item[5] * 100, 1)) + '%)</font>'
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        fixedProp += " <font color = \'#808080\'>(+" + str(round(item[5] * 100, 1)) + '%)</font>'
                fixedProp += '\n'

            ret += fixedProp
        rand = []
        if hasattr(i, 'rprops'):
            for pid, pType, pVal in i.rprops:
                if pType == gametypes.DATA_TYPE_NUM and i._isIntPropRef(pid):
                    rand.append((pid,
                     pType,
                     int(round(pVal * starFactor * qualityFactor)),
                     int(round(pVal * (nextStarFactor - starFactor) * qualityFactor))))
                else:
                    rand.append((pid,
                     pType,
                     pVal * starFactor * qualityFactor,
                     pVal * (nextStarFactor - starFactor) * qualityFactor))

            rand = [ tuple(list(r) + [PRD.data[r[0]]['priorityLevel'], PRD.data[r[0]]['showColor']]) for r in rand ]
            rand.sort(key=lambda k: k[4])
        randProp = ''
        if rand:
            for item in rand:
                info = PRD.data[item[0]]
                randProp += "<font color = \'#2491FF\'>" + info['name'] + '</font> '
                if info['type'] == 2:
                    randProp += "<font color = \'#99CCFF\'>+"
                elif info['type'] == 1:
                    randProp += "<font color = \'#99CCFF\'>-"
                if info['showType'] == 0:
                    randProp += str(int(item[2])) + '</font>'
                    if canLvUp == STATE_CAN_LV_UP:
                        randProp += " <font color = \'#ffb91c\'>(+%d)</font>" % int(item[3])
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        randProp += " <font color = \'#808080\'>(+%d)</font>" % int(item[3])
                elif info['showType'] == 2:
                    randProp += str(round(item[2], 1)) + '</font>'
                    if canLvUp == STATE_CAN_LV_UP:
                        randProp += " <font color = \'#ffb91c\'>(+%.1f)</font>" % round(item[3], 1)
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        randProp += " <font color = \'#808080\'>(+%.1f)</font>" % round(item[3], 1)
                else:
                    randProp += str(round(item[2] * 100, 1)) + '%</font>'
                    if canLvUp == STATE_CAN_LV_UP:
                        randProp += " <font color = \'#ffb91c\'>(+" + str(round(item[3] * 100, 1)) + ')</font>'
                    elif canLvUp == STATE_CAN_NOT_LV_UP:
                        randProp += " <font color = \'#808080\'>(+" + str(round(item[3] * 100, 1)) + ')</font>'
                randProp += '\n'

            ret += randProp + '\n'
        extraSkill = ''
        ses = getattr(i, 'ses', None)
        if ses:
            for spId in ses:
                spData = ESPD.data.get(spId, {})
                extraSkill += '%s:%s\n' % (spData.get('name', ''), spData.get('desc', ''))

            ret += "\n<font color = \'#E89BFF\'>%s</font>" % extraSkill
        starPSkill = ''
        ed = ED.data.get(i.id, {})
        if ed.get('starSEffect', None):
            starLv = getattr(i, 'starLv', 0)
            if starLv < ed.get('starLvNeed', 0):
                pskill = ed['starSEffect']
                spData = ESPD.data.get(pskill, {})
                starPSkill += "<font color = \'#808080\'>%s:%s</font>\n" % (spData.get('name', ''), spData.get('desc', ''))
            ret += '\n%s' % starPSkill
        return ret

    def validateItems(self):
        if not self.posMap.has_key((0, 0)):
            return False
        for pos in xrange(1, 6):
            if self.posMap.has_key((0, pos)):
                return True

        return False

    def doFeedEquip(self):
        p = BigWorld.player()
        srcPage = []
        srcPos = []
        for pos in xrange(1, 6):
            if not self.posMap.get((0, pos), None):
                continue
            srcPage.append(self.posMap[0, pos][0])
            srcPos.append(self.posMap[0, pos][1])

        dstPage, dstPos = self.posMap[0, 0]
        if self.isInBag:
            dstEquipIt = p.inv.getQuickVal(dstPage, dstPos)
            if not dstEquipIt:
                return
            isBind, itemId = self.checkBind(dstEquipIt)
            if isBind:
                itData = ID.data.get(itemId, {})
                text = GMD.data.get(GMDD.data.EQUIP_FEED_BIND, {}).get('text', gameStrings.TEXT_EQUIPFEEDPROXY_478)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(text % (itData.get('name'),), Functor(self.cellFeedEquipInv, srcPage, srcPos, dstPage, dstPos))
            else:
                self.cellFeedEquipInv(srcPage, srcPos, dstPage, dstPos)
        else:
            it = p.equipment[dstPos]
            if it:
                self.cellFeedEquip(srcPage, srcPos, dstPos, it)

    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.EQUIP_FEED)
    def cellFeedEquip(self, srcPage, srcPos, dstPos, it):
        BigWorld.player().cell.feedEquip(srcPage, srcPos, dstPos)

    @ui.looseGroupTradeConfirm([3, 4], GMDD.data.EQUIP_FEED)
    def cellFeedEquipInv(self, srcPage, srcPos, dstPage, dstPos):
        BigWorld.player().cell.feedEquipInv(srcPage, srcPos, dstPage, dstPos)

    def checkQuality(self):
        for pos in xrange(1, 6):
            key = self._getKey(0, pos)
            it = self.bindingData.get(key, None)
            if it and getattr(it, 'quality', 0) > uiConst.DISAS_MESSAGEBOX_QUALITY:
                return True

        return False

    def checkEnhance(self):
        for pos in xrange(1, 6):
            key = self._getKey(0, pos)
            it = self.bindingData.get(key, None)
            if it and getattr(it, 'enhLv', 0) > 0:
                return True

        return False

    def checkBind(self, dstEquipIt):
        for pos in xrange(1, 6):
            key = self._getKey(0, pos)
            it = self.bindingData.get(key, None)
            if it and it.isForeverBind() and not dstEquipIt.isForeverBind():
                return (True, it.id)

        return (False, 0)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')

    def onClosePanel(self, *arg):
        self.hide()

    def onFeedEquip(self, *arg):
        if self.validateItems():
            if self.checkQuality():
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_EQUIPFEEDPROXY_539, self.doFeedEquip)
                return
            if self.checkEnhance():
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_EQUIPFEEDPROXY_543, self.doFeedEquip)
                return
            self.doFeedEquip()

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            return item in self.bindingData.values()
