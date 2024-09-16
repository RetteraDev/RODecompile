#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipSoulProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import const
import uiUtils
import utils
import copy
import random
import tipUtils
from uiProxy import UIProxy
from asObject import ASObject
from callbackHelper import Functor
from gameclass import PSkillInfo
from gameStrings import gameStrings
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import prop_ref_data as PRD
from data import sys_config_data as SCD
from data import equip_soul_prop_data as ESPRD
from data import state_group_inverted_index_data as SGIID
from cdata import equip_soul_pool_data as ESPOD
from cdata import equip_soul_consume_data as ESCD
from cdata import equip_soul_pool_prop_data as ESPPD
from cdata import game_msg_def_data as GMDD
SOUL_ID_LIST = ESPOD.data.keys()
SOUL_MAX_NUM = len(SOUL_ID_LIST)
BEEHIVE_X_MAX_NUM = 9
BEEHIVE_Y_MAX_NUM = 13
STONE_PROP_SHOW_NUM = 9
POOL_PROP_SHOW_NUM = 5

class EquipSoulProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipSoulProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currentIdx = -1
        self.showTabNum = 0
        self.spid = 0
        self.newList = []
        self.realList = []
        self.simulationList = []
        self.usedEnergy = 0
        self.usedNum = 0
        self.maxEnhanceNum = 0
        self.nowMap = {}
        self.stoneMap = {}
        self.allStoneMap = {}
        self.showPropDetail = False
        self.needShowStarPanel = False
        self.needShowActiveEffect = False
        self.flyEffectTimer = None
        self.flyEffectList = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_SOUL, self.checkAndHide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_EQUIP_SOUL:
            self.widget = widget
            self.initUI()
            self.refreshSchemeInfo()
            self.refreshTabInfo()
            self.showStarPanel()
            self.setTemplateState()
            self._checkNewestEquipSoulVisible()

    def setTemplateState(self):
        p = BigWorld.player()
        if p.isUsingTemp():
            self.widget.energyBarHint.visible = False
            self.widget.energyBar.visible = False
            self.widget.addBtn.visible = False
            self.widget.xingchenText.visible = False
            self.widget.resetBtn.visible = False
            self.widget.confirmBtn.visible = False
            self.widget.switchSchemeBtn.visible = False
            self.widget.switchSchemeText.visible = False
            self.widget.firstStoneHelp.visible = False

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_EQUIP_SOUL)

    def reset(self):
        self.currentIdx = -1
        self.spid = 0
        self.newList = []
        self.realList = []
        self.simulationList = []
        self.usedEnergy = 0
        self.usedNum = 0
        self.maxEnhanceNum = 0
        self.needShowStarPanel = False
        self.needShowActiveEffect = False
        self.stopFlyEffectTimer()

    def stopFlyEffectTimer(self):
        if self.widget:
            self.widget.removeAllInst(self.widget.flyEffect)
        if self.flyEffectTimer:
            BigWorld.cancelCallback(self.flyEffectTimer)
            self.flyEffectTimer = None
        self.flyEffectList = []

    def checkAndHide(self):
        if self.checkInSimulation():
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_SOUL_IN_SIMULATION_HINT, '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.hide)
        else:
            self.hide()

    def show(self, needShowStarPanel = False):
        if not gameglobal.rds.configData.get('enableEquipSoul', False):
            return
        if BigWorld.player().lv < SCD.data.get('equipSoulMinLv', 0):
            return
        self.initData()
        self.needShowStarPanel = needShowStarPanel
        if self.widget:
            self.showStarPanel()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_EQUIP_SOUL)

    def showStarPanel(self):
        if self.needShowStarPanel:
            self.uiAdapter.equipSoulStar.show()
        self.needShowStarPanel = False

    def initData(self):
        p = BigWorld.player()
        if self.allStoneMap.has_key(p.school):
            self.stoneMap = self.allStoneMap[p.school]
            return
        self.stoneMap = {}
        for schreq, positionx, positiony, spid in ESPRD.data.iterkeys():
            if schreq != p.school:
                continue
            if not self.stoneMap.has_key(spid):
                self.stoneMap[spid] = {}
            self.stoneMap[spid][positionx, positiony] = True

        self.allStoneMap[p.school] = self.stoneMap

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCloseBtn, False, 0, True)
        self.widget.firstStoneHelp.visible = False
        self.widget.helpIcon.helpKey = 309
        self.widget.switchSchemeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickSwitchSchemeBtn, False, 0, True)
        self.widget.propCheckBox.addEventListener(events.EVENT_SELECT, self.handleSelectCheckBox, False, 0, True)
        for idx in xrange(SOUL_MAX_NUM):
            itemMc = getattr(self.widget, 'tabBtn%d' % idx, None)
            if not itemMc:
                continue
            itemMc.groupName = 'soul'
            itemMc.desc.gotoAndStop('type%d' % idx)
            itemMc.data = {'idx': idx}
            itemMc.lockFlag.visible = False
            itemMc.invalidFlag.visible = False
            itemMc.addEventListener(events.BUTTON_CLICK, self.handleClickTabBtn, False, 0, True)
            itemMc.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleStateChange, False, 0, True)

        for x in xrange(BEEHIVE_X_MAX_NUM):
            for y in xrange(BEEHIVE_Y_MAX_NUM):
                itemMc = getattr(self.widget.beehive, 'slot%dx%d' % (x, y), None)
                if not itemMc:
                    continue
                itemData = {'x': x,
                 'y': y}
                ASUtils.setMcData(itemMc, 'data', itemData)

        for i in xrange(POOL_PROP_SHOW_NUM):
            itemMc = getattr(self.widget.propDetail, 'poolProp%d' % i, None)
            if not itemMc:
                continue
            itemMc.effect.visible = False

        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.resetBtn.addEventListener(events.MOUSE_CLICK, self.handleClickResetBtn, False, 0, True)
        self.widget.addBtn.addEventListener(events.MOUSE_CLICK, self.handleClickAddBtn, False, 0, True)

    def changeScheme(self):
        for idx in xrange(SOUL_MAX_NUM):
            itemMc = getattr(self.widget, 'tabBtn%d' % idx, None)
            if not itemMc:
                continue
            itemMc.selected = False

        self.reset()
        self.refreshSchemeInfo()
        self.refreshTabInfo()

    def refreshSchemeInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableEquipSoulSchemes', False) and not p.isUsingTemp():
            self.widget.switchSchemeBtn.visible = True
            self.widget.switchSchemeText.visible = True
            self.widget.switchSchemeText.text = gameStrings.CURRENT_SCHEME_TITLE % BigWorld.player().getCurEquipSoulSchemeName()
        else:
            self.widget.switchSchemeBtn.visible = False
            self.widget.switchSchemeText.visible = False
        self._checkNewestEquipSoulVisible()

    def refreshTabInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            lockMap = {}
            invalidMap = {}
            visibleMap = {}
            for idx in xrange(SOUL_MAX_NUM):
                spid = SOUL_ID_LIST[idx]
                lockMap[spid] = False
                invalidMap[spid] = False
                visibleMap[spid] = True
                espodData = self._getEspodData(spid)
                if not espodData:
                    return
                preid = espodData.get('preid', 0)
                if preid not in SOUL_ID_LIST:
                    continue
                if not visibleMap.get(preid, False) or lockMap.get(preid, False):
                    visibleMap[spid] = False
                    continue
                prePoolid = ESPOD.data.get(preid, {}).get('poolid', 0)
                preReqStone = ESPPD.data.get((prePoolid, p.school), {}).get('reqStone', 0)
                preEquipSoul = p.equipSoul.get(preid, {})
                preSumStone = sum(((1 if value == const.EQUIP_SOUL_STAT_ACTIVE else 0) for value in preEquipSoul.itervalues()))
                if invalidMap.get(preid, False):
                    invalidMap[spid] = True
                if p.equipSoul.has_key(spid):
                    if preSumStone < preReqStone:
                        invalidMap[spid] = True
                elif preSumStone < preReqStone:
                    lockMap[spid] = True

            self.showTabNum = sum(((1 if value else 0) for value in visibleMap.itervalues()))
            firstItemMc = None
            currentItemMc = None
            for idx in xrange(SOUL_MAX_NUM):
                itemMc = getattr(self.widget, 'tabBtn%d' % idx, None)
                if not itemMc:
                    continue
                needEffect = False
                spid = SOUL_ID_LIST[idx]
                itemMc.visible = visibleMap.get(spid, False)
                if not itemMc.visible:
                    continue
                espodData = ESPOD.data.get(spid, {})
                preid = espodData.get('preid', 0)
                if lockMap.get(spid, False):
                    itemMc.lockFlag.visible = True
                    itemMc.invalidFlag.visible = False
                    tips = SCD.data.get('equipSoulTabLockTips', '%s %s') % (ESPOD.data.get(preid, {}).get('name', ''), espodData.get('name', ''))
                    TipManager.addTip(itemMc, tips)
                elif invalidMap.get(spid, False):
                    itemMc.lockFlag.visible = False
                    itemMc.invalidFlag.visible = True
                    tips = SCD.data.get('equipSoulTabInvalidTips', '%s %s') % (ESPOD.data.get(preid, {}).get('name', ''), espodData.get('name', ''))
                    TipManager.addTip(itemMc, tips)
                else:
                    if itemMc.lockFlag.visible or itemMc.invalidFlag.visible:
                        needEffect = True
                    itemMc.lockFlag.visible = False
                    itemMc.invalidFlag.visible = False
                    TipManager.removeTip(itemMc)
                if needEffect:
                    itemMc.effect.visible = True
                    itemMc.effect.gotoAndPlay(1)
                else:
                    itemMc.effect.visible = False
                if idx >= self.showTabNum - 1:
                    itemMc.angle.visible = False
                else:
                    itemMc.angle.visible = True
                if not firstItemMc:
                    firstItemMc = itemMc
                if not currentItemMc and itemMc.selected:
                    currentItemMc = itemMc

            if currentItemMc:
                self.clickTabBtn(int(currentItemMc.data.idx))
            elif firstItemMc:
                self.clickTabBtn(int(firstItemMc.data.idx))
            self._checkNewestEquipSoulVisible()
            return

    def handleClickTabBtn(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selected:
            return
        p = BigWorld.player()
        if itemMc.lockFlag and itemMc.lockFlag.visible:
            p.showGameMsg(GMDD.data.EQUIP_SOUL_LOCK, ())
            return
        if itemMc.invalidFlag and itemMc.invalidFlag.visible:
            p.showGameMsg(GMDD.data.EQUIP_SOUL_INVALID, ())
            return
        if self.checkInSimulation():
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_SOUL_IN_SIMULATION_HINT, '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.clickTabBtn, int(itemMc.data.idx)))
        else:
            self.clickTabBtn(int(itemMc.data.idx))

    def clickTabBtn(self, idx):
        itemMc = getattr(self.widget, 'tabBtn%d' % idx, None)
        if not itemMc:
            return
        else:
            itemMc.selected = True
            self.currentIdx = idx
            spid = SOUL_ID_LIST[self.currentIdx]
            self.widget.soulPool.gotoAndStop('soul%d' % spid)
            self.widget.bg.loadImage('equipSoul/%d.dds' % spid)
            self.stopFlyEffectTimer()
            self.realList = []
            self.simulationList = []
            self.usedEnergy = 0
            self.usedNum = 0
            self.maxEnhanceNum = 0
            self.refreshDetailInfo()
            return

    def handleStateChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        itemMc.desc.gotoAndStop('type%d' % itemMc.data.idx)
        if itemMc.data.idx >= self.showTabNum - 1:
            itemMc.angle.visible = False
        else:
            itemMc.angle.visible = True

    def checkInSimulation(self):
        return len(self.simulationList) > 0

    def setStoneState(self, itemMc, state):
        itemMc.gotoAndStop(state)
        stoneType = int(itemMc.stoneType)
        if state == 'disable':
            stoneFrame = '%dtype%d' % (self.spid, stoneType)
        else:
            stoneFrame = 'type%d' % stoneType
        itemMc.icon.gotoAndStop(stoneFrame)
        itemMc.bg.gotoAndStop('soul%d' % self.spid)

    def playStoneActiveEffect(self, itemMc):
        itemMc.activeEffect.visible = True
        itemMc.activeEffect.gotoAndPlay(1)
        itemMc.activeEffect.effect1.gotoAndStop('soul%d' % self.spid)
        itemMc.activeEffect.effect2.gotoAndStop('soul%d' % self.spid)

    def refreshDetailInfo(self):
        if not self.widget:
            return
        elif self.currentIdx < 0 or self.currentIdx >= SOUL_MAX_NUM:
            return
        else:
            p = BigWorld.player()
            self.spid = SOUL_ID_LIST[self.currentIdx]
            self.nowMap = self.stoneMap.get(self.spid)
            if not self.nowMap:
                if not BigWorld.isPublishedVersion():
                    p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.TEXT_EQUIPSOULPROXY_420 % (p.school, self.spid))
                return
            newEnhanceNum = 0
            maxEquipEnhanceVal = round(p.maxEquipEnhanceVal, 2)
            espodData = self._getEspodData(self.spid)
            if not espodData:
                return
            validStoneNum = espodData.get('validStoneNum', 0)
            for i in xrange(1, validStoneNum + 1):
                if ESCD.data.get((self.spid, i), {}).get('enhanceNum', 0) <= maxEquipEnhanceVal:
                    newEnhanceNum = i
                else:
                    break

            self.maxEnhanceNum = newEnhanceNum
            self.realList = []
            equipSoul = p.equipSoul.get(self.spid, {})
            for pos, value in equipSoul.iteritems():
                if value == const.EQUIP_SOUL_STAT_ACTIVE:
                    self.realList.append(pos)

            for x in xrange(BEEHIVE_X_MAX_NUM):
                for y in xrange(BEEHIVE_Y_MAX_NUM):
                    itemMc = getattr(self.widget.beehive, 'slot%dx%d' % (x, y), None)
                    if not itemMc:
                        continue
                    if not self.nowMap.get((x, y), False):
                        itemMc.visible = False
                        continue
                    itemMc.visible = True
                    itemMc.activeEffect.visible = False
                    esprdData = self._getEsprdData(p.school, x, y, self.spid)
                    if not esprdData:
                        return
                    ASUtils.setMcData(itemMc, 'stoneType', esprdData.get('stoneType', 0))
                    if (x, y) in self.realList:
                        self.setStoneState(itemMc, 'normal')
                    else:
                        firstStone = esprdData.get('firstStone', 0)
                        if firstStone:
                            self.setStoneState(itemMc, 'canActive')
                        else:
                            self.setStoneState(itemMc, 'disable')
                    if not p.isUsingTemp():
                        itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickSlot, False, 0, True)
                    typeArg = (self.spid,
                     p.school,
                     x,
                     y)
                    TipManager.addTipByType(itemMc.hit, tipUtils.TYPE_EQUIP_SOUL_STONE, typeArg, False, 'bottomRight')

            typeArg = (self.spid, p.school)
            TipManager.addTipByType(self.widget.soulPool, tipUtils.TYPE_EQUIP_SOUL_POOL, typeArg, False)
            self.usedNum = len(self.realList) + len(self.simulationList)
            self.refreshPropInfo()
            self.refreshHintInfo()
            self.refreshEnergyInfo()
            self.refreshCanActiveSlotInfo()
            self.refreshBtnInfo()
            return

    def refreshPropInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            self.widget.propCheckBox.selected = self.showPropDetail
            self.widget.propDetail.visible = self.showPropDetail
            stonePropMap = {}
            totalList = self.realList + self.simulationList
            for x, y in totalList:
                if not self.nowMap.get((x, y), False):
                    continue
                esprdData = self._getEsprdData(p.school, x, y, self.spid)
                if not esprdData:
                    return
                stoneProps = esprdData.get('stoneProps', [])
                for propId, pType, propNum in stoneProps:
                    key = (propId, pType)
                    if key not in stonePropMap:
                        stonePropMap[key] = [0, 0]
                    if (x, y) in self.realList:
                        stonePropMap[key][0] += propNum
                    else:
                        stonePropMap[key][1] += propNum

            stonePropList = []
            for key, value in stonePropMap.iteritems():
                stonePropList.append((key[0],
                 key[1],
                 value[0],
                 value[1]))

            stonePropList.sort(key=lambda x: x[0])
            if len(stonePropList) < STONE_PROP_SHOW_NUM:
                stonePropList.extend([(0, 0, 0, 0)] * (STONE_PROP_SHOW_NUM - len(stonePropList)))
            showPropEffectMap = {}
            if self.needShowActiveEffect:
                if self.checkInSimulation():
                    x, y = self.simulationList[-1]
                    esprdData = self._getEsprdData(p.school, x, y, self.spid)
                    if not esprdData:
                        return
                    stoneProps = esprdData.get('stoneProps', [])
                    for propId, pType, propNum in stoneProps:
                        showPropEffectMap[propId, pType] = True

                else:
                    for x, y in self.newList:
                        stoneProps = ESPRD.data.get((p.school,
                         x,
                         y,
                         self.spid), {}).get('stoneProps', [])
                        for propId, pType, propNum in stoneProps:
                            showPropEffectMap[propId, pType] = True

            self.widget.removeAllInst(self.widget.propDetail.scrollWnd.canvas)
            firstEffectPosY = None
            posY = 0
            for propId, pType, curNum, addNum in stonePropList:
                itemMc = self.widget.getInstByClsName('EquipSoul_StonePropItem')
                prdData = PRD.data.get(propId, {})
                if prdData:
                    propNameStr = prdData.get('name', '')
                    showType = prdData.get('showType', 0)
                    propNumStr = uiUtils.formatProp(curNum, pType, showType)
                    if addNum > 0:
                        propNumStr += uiUtils.toHtml('(+%s)' % uiUtils.formatProp(addNum, pType, showType), color='#7ACC29')
                    if self.showPropDetail and showPropEffectMap.get((propId, pType), False):
                        if firstEffectPosY == None:
                            firstEffectPosY = posY
                        itemMc.effect.visible = True
                        itemMc.effect.gotoAndPlay(1)
                    else:
                        itemMc.effect.visible = False
                else:
                    propNameStr = ''
                    propNumStr = ''
                    itemMc.effect.visible = False
                itemMc.propName.htmlText = propNameStr
                itemMc.propNum.htmlText = propNumStr
                itemMc.y = posY
                posY += 26
                self.widget.propDetail.scrollWnd.canvas.addChild(itemMc)

            self.widget.propDetail.scrollWnd.refreshHeight()
            if firstEffectPosY != None:
                barPos = self.widget.propDetail.scrollWnd.getScrollToPos()
                if firstEffectPosY < barPos:
                    self.widget.propDetail.scrollWnd.scrollTo(firstEffectPosY)
                if firstEffectPosY >= barPos + 208:
                    self.widget.propDetail.scrollWnd.scrollTo(firstEffectPosY - 208)
            poolid = ESPOD.data.get(self.spid, {}).get('poolid', 0)
            esppdData = ESPPD.data.get((poolid, p.school), {})
            reqStone = esppdData.get('reqStone', 0)
            poolActive = reqStone <= self.usedNum
            self.widget.propDetail.poolNoActiveFlag.visible = not poolActive
            poolPropList = self.getPoolPropList(poolid, p.school)
            if len(poolPropList) < POOL_PROP_SHOW_NUM:
                poolPropList.extend([(0, 0, 0)] * (POOL_PROP_SHOW_NUM - len(poolPropList)))
            else:
                poolPropList = poolPropList[:POOL_PROP_SHOW_NUM]
            showPoolEffect = False
            if self.needShowActiveEffect:
                if self.checkInSimulation():
                    if reqStone == self.usedNum:
                        showPoolEffect = True
                elif poolActive and self.usedNum - len(self.newList) < reqStone:
                    showPoolEffect = True
            for i, (propId, pType, propNum) in enumerate(poolPropList):
                itemMc = getattr(self.widget.propDetail, 'poolProp%d' % i, None)
                if not itemMc:
                    continue
                prdData = PRD.data.get(propId, {})
                if prdData:
                    propNameStr = prdData.get('name', '')
                    propNumStr = uiUtils.formatProp(propNum, pType, prdData.get('showType', 0))
                    if not poolActive:
                        propNameStr = uiUtils.toHtml(propNameStr, color='#808080')
                        propNumStr = uiUtils.toHtml(propNumStr, color='#808080')
                    if self.showPropDetail and showPoolEffect:
                        itemMc.effect.visible = True
                        itemMc.effect.gotoAndPlay(1)
                    else:
                        itemMc.effect.visible = False
                else:
                    propNameStr = ''
                    propNumStr = ''
                    itemMc.effect.visible = False
                itemMc.propName.htmlText = propNameStr
                itemMc.propNum.htmlText = propNumStr

            soulPoolMc = getattr(self.widget.soulPool, 'realMc%d' % self.spid, None)
            if soulPoolMc:
                soulPoolMc.activeNum.text = '%d/%d' % (self.usedNum, reqStone)
                realNum = len(self.realList)
                realValue = 100.0
                if reqStone and reqStone > realNum:
                    realValue = realValue * realNum / reqStone
                soulPoolMc.setRealBar(realValue, True)
                if self.checkInSimulation():
                    soulPoolMc.totalBar.visible = True
                    if self.needShowActiveEffect and len(self.simulationList) == 1:
                        soulPoolMc.setTotalBar(realValue, False)
                    totalValue = 100.0
                    if reqStone and reqStone > self.usedNum:
                        totalValue = totalValue * self.usedNum / reqStone
                    soulPoolMc.setTotalBar(totalValue, True)
                else:
                    soulPoolMc.totalBar.visible = len(self.newList) > 0
                if showPoolEffect:
                    soulPoolMc.activeEffect.visible = True
                    soulPoolMc.activeEffect.gotoAndPlay(1)
                else:
                    soulPoolMc.activeEffect.visible = False
                soulPoolMc.bgEffect.visible = poolActive
            if self.needShowActiveEffect and not self.checkInSimulation():
                self.playExtraEffect()
            self.newList = []
            self.needShowActiveEffect = False
            return

    def playExtraEffect(self):
        if not gameglobal.rds.configData.get('enableEquipSoulFlyEffect', False):
            return
        else:
            self.stopFlyEffectTimer()
            offestX = self.widget.beehive.x
            offestY = self.widget.beehive.y
            for x, y in self.newList:
                if not self.nowMap.get((x, y), False):
                    continue
                itemMc = getattr(self.widget.beehive, 'slot%dx%d' % (x, y), None)
                if not itemMc:
                    continue
                posX = offestX + itemMc.x + itemMc.width / 2
                posY = offestY + itemMc.y + itemMc.height / 2
                randX = random.randint(-100, 100)
                randY = random.randint(-50, 50)
                pos = posX + posY
                if pos < 700:
                    bezierList = [{'x': posX + randX - 50,
                      'y': posY + randY - 300}]
                elif pos < 800:
                    bezierList = [{'x': posX + randX,
                      'y': posY + randY - 100}]
                elif pos < 900:
                    bezierList = [{'x': posX + randX + 150,
                      'y': posY + randY}]
                elif pos < 1000:
                    bezierList = [{'x': posX + randX,
                      'y': posY + randY + 100}]
                else:
                    bezierList = [{'x': posX + randX - 50,
                      'y': posY + randY + 300}]
                tweenerInfo = {'x': 130,
                 'y': 500,
                 'time': 1.5,
                 'transition': 'easeInCubic',
                 '_bezier': bezierList}
                self.flyEffectList.append([x,
                 y,
                 posX,
                 posY,
                 self.spid,
                 tweenerInfo])

            random.shuffle(self.flyEffectList)
            self.updateFlyEffectTimer()
            return

    def updateFlyEffectTimer(self):
        if not self.widget:
            return
        elif len(self.flyEffectList) <= 0:
            return
        else:
            x, y, posX, posY, spid, tweenerInfo = self.flyEffectList.pop()
            if spid != self.spid:
                return
            elif not self.nowMap.get((x, y), False):
                return
            itemMc = getattr(self.widget.beehive, 'slot%dx%d' % (x, y), None)
            if not itemMc:
                return
            self.playStoneActiveEffect(itemMc)
            flyEffectMc = self.widget.getInstByClsName('EquipSoul_FlyEffect')
            flyEffectMc.gotoAndStop('soul%d' % self.spid)
            flyEffectMc.x = posX
            flyEffectMc.y = posY
            flyEffectMc.setTweener(tweenerInfo)
            self.widget.flyEffect.addChild(flyEffectMc)
            BigWorld.callback(0.08, self.updateFlyEffectTimer)
            return

    def refreshHintInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        espodData = ESPOD.data.get(self.spid, {})
        validStoneNum = espodData.get('validStoneNum', 0)
        freeNum = self.maxEnhanceNum - self.usedNum
        hint = SCD.data.get('equipSoulStoneHint', '%d %d %d') % (self.usedNum, validStoneNum, freeNum)
        ASUtils.textFieldAutoSize(self.widget.hint, hint)
        self.widget.hint.x = 968 - self.widget.hint.width
        ownEnhance = round(p.maxEquipEnhanceVal, 2)
        ownEnhance100 = int(round(ownEnhance * 100))
        if freeNum > 0:
            self.widget.helpIcon.visible = False
            tips = SCD.data.get('equipSoulStoneHintFreeTips', '%d %d') % (ownEnhance100, self.maxEnhanceNum)
        else:
            self.widget.helpIcon.visible = True
            if validStoneNum > self.usedNum:
                needEnhance = ESCD.data.get((self.spid, self.usedNum + 1), {}).get('enhanceNum', 0)
                lackEnhance = int(round((needEnhance - ownEnhance) * 100))
                tips = SCD.data.get('equipSoulStoneHintTips', '%d %d %d') % (ownEnhance100, self.maxEnhanceNum, lackEnhance)
            else:
                tips = SCD.data.get('equipSoulStoneHintMaxTips', '%d %d %d') % (ownEnhance100, self.maxEnhanceNum, validStoneNum)
        TipManager.addTip(self.widget.hint, tips)
        if self.currentIdx == 0 and self.usedNum == 0:
            self.widget.firstStoneHelp.visible = True
        else:
            self.widget.firstStoneHelp.visible = False

    def refreshEnergyInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        ownEnergy = p.getFame(const.XING_CHEN_ZHI_LIN_FAME_ID)
        maxEnergy = SCD.data.get('starMax', 0)
        self.usedEnergy = utils.calcEquipSoulUsedEnergy(self.spid, len(self.realList), len(self.simulationList))
        lastEnergy = ownEnergy - self.usedEnergy if ownEnergy > self.usedEnergy else 0
        currentValue = 100.0
        if maxEnergy and maxEnergy > lastEnergy:
            currentValue = currentValue * lastEnergy / maxEnergy
        self.widget.energyBar.currentValue = currentValue
        ownValue = 1.0
        if maxEnergy and maxEnergy > ownEnergy:
            ownValue = ownValue * ownEnergy / maxEnergy
        self.widget.energyBar.totalBar.width = 870 * ownValue
        if self.usedEnergy > 0:
            usedEnergyStr = uiUtils.toHtml('- %s' % format(self.usedEnergy, ','), color='#CC2929')
            self.widget.energyBarHint.htmlText = '( %s %s ) / %s' % (format(ownEnergy, ','), usedEnergyStr, format(maxEnergy, ','))
        else:
            self.widget.energyBarHint.htmlText = '%s / %s' % (format(ownEnergy, ','), format(maxEnergy, ','))

    def handleClickSlot(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        p = BigWorld.player()
        currentFrameLabel = itemMc.currentFrameLabel
        if currentFrameLabel == 'canActive':
            if e.buttonIdx != uiConst.LEFT_BUTTON:
                return
            ownEnergy = p.getFame(const.XING_CHEN_ZHI_LIN_FAME_ID)
            needEnergy = self.usedEnergy + ESCD.data.get((self.spid, self.usedNum + 1), {}).get('energyCon', 0)
            if needEnergy > ownEnergy:
                p.showGameMsg(GMDD.data.EQUIP_SOUL_ACTIVE_LACK_ENERGY, ())
                return
            pos = (int(itemMc.data.x), int(itemMc.data.y))
            if self.simulationList.count(pos):
                return
            self.updateSlot(pos, False)
            TipManager.hideAndShowTipAgain(itemMc)
        elif currentFrameLabel == 'canCancel':
            if len(self.simulationList) == 0:
                return
            pos = (int(itemMc.data.x), int(itemMc.data.y))
            if self.simulationList[-1] != pos:
                return
            self.setStoneState(itemMc, 'canActive')
            self.updateSlot(pos, True)
            TipManager.hideAndShowTipAgain(itemMc)
        elif currentFrameLabel == 'disable':
            if e.buttonIdx != uiConst.LEFT_BUTTON:
                return
            ownEnhance = round(p.maxEquipEnhanceVal, 2)
            needEnhance = ESCD.data.get((self.spid, self.usedNum + 1), {}).get('enhanceNum', 0)
            if needEnhance > ownEnhance:
                lackEnhance = int(round((needEnhance - ownEnhance) * 100))
                p.showGameMsg(GMDD.data.EQUIP_SOUL_ACTIVE_LACK_ENHANCE, (lackEnhance,))
                return
            validStoneNum = ESPOD.data.get(self.spid, {}).get('validStoneNum', 0)
            if validStoneNum > self.usedNum:
                p.showGameMsg(GMDD.data.EQUIP_SOUL_ACTIVE_CANNOT, ())
            else:
                p.showGameMsg(GMDD.data.EQUIP_SOUL_ACTIVE_MAX_NUM, (validStoneNum,))

    def updateSlot(self, pos, isCancel):
        if isCancel:
            self.simulationList.pop()
        else:
            self.simulationList.append(pos)
        totalList = self.realList + self.simulationList
        self.usedNum = len(totalList)
        if isCancel:
            offsetPosList = utils.getEquipSoulOffsetPos(pos[0], pos[1])
            offsetPosList = filter(lambda pos: pos not in totalList and self.nowMap.get(pos, False), offsetPosList)
            for x, y in offsetPosList:
                if not self.nowMap.get((x, y), False):
                    continue
                itemMc = getattr(self.widget.beehive, 'slot%dx%d' % (x, y), None)
                if not itemMc:
                    continue
                self.setStoneState(itemMc, 'disable')

        else:
            self.needShowActiveEffect = True
        self.refreshPropInfo()
        self.refreshHintInfo()
        self.refreshEnergyInfo()
        self.refreshCanActiveSlotInfo()
        self.refreshBtnInfo()

    def refreshCanActiveSlotInfo(self):
        lastPos = self.simulationList[-1] if self.checkInSimulation() else None
        totalList = self.realList + self.simulationList
        for x, y in totalList:
            if not self.nowMap.get((x, y), False):
                continue
            itemMc = getattr(self.widget.beehive, 'slot%dx%d' % (x, y), None)
            if not itemMc:
                continue
            if (x, y) == lastPos:
                self.setStoneState(itemMc, 'canCancel')
            else:
                self.setStoneState(itemMc, 'normal')

        freeNum = self.maxEnhanceNum - self.usedNum
        totalPosList = []
        for x, y in totalList:
            totalPosList.extend(utils.getEquipSoulOffsetPos(x, y))

        totalPosList = list(set(totalPosList))
        totalPosList = filter(lambda pos: pos not in totalList and self.nowMap.get(pos, False), totalPosList)
        for x, y in totalPosList:
            if not self.nowMap.get((x, y), False):
                continue
            itemMc = getattr(self.widget.beehive, 'slot%dx%d' % (x, y), None)
            if not itemMc:
                continue
            if freeNum > 0:
                self.setStoneState(itemMc, 'canActive')
            else:
                self.setStoneState(itemMc, 'disable')

    def refreshBtnInfo(self):
        self.widget.confirmBtn.enabled = self.checkInSimulation()
        self.widget.resetBtn.enabled = len(self.realList) > 0

    def handleClickCloseBtn(self, *args):
        self.checkAndHide()

    def handleSelectCheckBox(self, *args):
        self.showPropDetail = self.widget.propCheckBox.selected
        self.widget.propDetail.visible = self.showPropDetail

    def handleClickConfirmBtn(self, *args):
        xList = [ pos[0] for pos in self.simulationList ]
        yList = [ pos[1] for pos in self.simulationList ]
        BigWorld.player().cell.activeEquipSoul(self.spid, xList, yList)

    def handleClickResetBtn(self, *args):
        msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_SOUL_RESET_HINT, '')
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.resetEquipSoul, self.spid))

    def handleClickAddBtn(self, *args):
        self.uiAdapter.equipSoulStar.show()

    def handleClickSwitchSchemeBtn(self, *args):
        self.uiAdapter.schemeSwitch.show(uiConst.SCHEME_SWITCH_EQUIP_SOUL)

    def setActiveEffect(self, data):
        if not self.widget:
            return
        p = BigWorld.player()
        newEquipSoul = copy.deepcopy(p.equipSoul)
        newEquipSoul.update(data)
        self.newList = []
        equipSoul = p.equipSoul.get(self.spid, {})
        newEquipSoul = newEquipSoul.get(self.spid, {})
        for pos, value in newEquipSoul.iteritems():
            if value == const.EQUIP_SOUL_STAT_ACTIVE and pos not in equipSoul:
                self.newList.append(pos)

        self.needShowActiveEffect = True

    def getPoolPropList(self, poolid, schreq):
        esppdData = ESPPD.data.get((poolid, schreq), {})
        poolPropMap = {}
        pskIds = esppdData.get('pasid', [])
        for pskId in pskIds:
            pskInfo = PSkillInfo(pskId, 1)
            if not gameglobal.rds.configData.get('enablePskillExtraAttr', False):
                attrId = pskInfo.getSkillData('attrId', 0)
                if attrId != 0:
                    attrValType = pskInfo.getSkillData('attrValType', 0)
                    attrVal = pskInfo.getSkillData('attrVal', 0)
                    key = (attrId, attrValType)
                    if key not in poolPropMap:
                        poolPropMap[key] = attrVal
                    else:
                        poolPropMap[key] += attrVal
                attrGroupId = pskInfo.getSkillData('attrGroupId', 0)
                if attrGroupId != 0:
                    attrGroupValType = pskInfo.getSkillData('attrGroupValType', 0)
                    attrGroupVal = pskInfo.getSkillData('attrGroupVal', 0)
                    attrs = SGIID.data.get(attrGroupId, {})
                    for attrId in attrs:
                        key = (attrId, attrGroupValType)
                        if key not in poolPropMap:
                            poolPropMap[key] = attrGroupVal
                        else:
                            poolPropMap[key] += attrGroupVal

            else:
                effects = pskInfo.getAllAffectedEffect()
                if effects:
                    for attrId, attrValType, attrVal in effects:
                        key = (attrId, attrValType)
                        if key not in poolPropMap:
                            poolPropMap[key] = attrVal
                        else:
                            poolPropMap[key] += attrVal

        poolPropList = []
        for key, value in poolPropMap.iteritems():
            poolPropList.append((key[0], key[1], value))

        poolPropList.sort(key=lambda x: x[0])
        return poolPropList

    def getPoolTip(self, spid, schreq):
        p = BigWorld.player()
        espodData = ESPOD.data.get(spid, {})
        poolid = espodData.get('poolid', 0)
        esppdData = ESPPD.data.get((poolid, schreq), {})
        info = {}
        info['poolName'] = esppdData.get('name', '')
        propDesc = ''
        poolPropList = self.getPoolPropList(poolid, p.school)
        for propId, pType, propNum in poolPropList:
            prdData = PRD.data.get(propId, {})
            if propDesc != '':
                propDesc += '<br>'
            propDesc += '%s +%s' % (prdData.get('name', ''), uiUtils.formatProp(propNum, pType, prdData.get('showType', 0)))

        for value in ESPOD.data.itervalues():
            if spid == value.get('preid', 0):
                if propDesc != '':
                    propDesc += '<br>'
                propDesc += gameStrings.EQUIP_SOUL_PROXY_POOL_TIP_OPEN_SOUL % value.get('name', '')

        info['propDesc'] = propDesc
        reqStone = esppdData.get('reqStone', 0)
        conditionDesc = gameStrings.TEXT_EQUIPSOULPROXY_1038 % (espodData.get('name', ''), self.usedNum, reqStone)
        if reqStone <= self.usedNum:
            poolType = 'type%d' % poolid
            state = gameStrings.TEXT_EQUIPSOULPROXY_1042
        else:
            poolType = 'type0'
            state = uiUtils.toHtml(gameStrings.TEXT_EQUIPSOULPROXY_1045, color='#E53900')
            conditionDesc = uiUtils.toHtml(conditionDesc, color='#E53900')
        info['poolType'] = poolType
        info['state'] = state
        info['conditionDesc'] = conditionDesc
        return uiUtils.dict2GfxDict(info, True)

    def getStoneTip(self, spid, schreq, x, y):
        p = BigWorld.player()
        esprdData = self._getEsprdData(schreq, x, y, spid)
        if not esprdData:
            return
        info = {}
        info['stoneName'] = esprdData.get('stoneName', '')
        info['stoneType'] = 'type%d' % esprdData.get('stoneType', 0)
        propDesc = ''
        stoneProps = esprdData.get('stoneProps', [])
        if isinstance(stoneProps, list):
            stoneProps.sort(key=lambda x: x[0])
        for propId, pType, propNum in stoneProps:
            prdData = PRD.data.get(propId, {})
            if propDesc != '':
                propDesc += '<br>'
            propDesc += '%s +%s' % (prdData.get('name', ''), uiUtils.formatProp(propNum, pType, prdData.get('showType', 0)))

        info['propDesc'] = propDesc
        totalList = self.realList + self.simulationList
        if (x, y) in totalList:
            state = gameStrings.TEXT_EQUIPSOULPROXY_1042
            conditionDesc = ''
            if self.checkInSimulation() and self.simulationList[-1] == (x, y):
                operationHint = gameStrings.TEXT_EQUIPSOULPROXY_1081
            else:
                operationHint = ''
        else:
            espodData = ESPOD.data.get(spid, {})
            isMax = espodData.get('validStoneNum', 0) <= self.usedNum
            isFull = self.maxEnhanceNum <= self.usedNum
            if isMax:
                conditionDesc = uiUtils.toHtml(gameStrings.TEXT_EQUIPSOULPROXY_1090 % espodData.get('name', ''), color='#E53900')
            elif isFull:
                conditionDesc = uiUtils.toHtml(gameStrings.TEXT_EQUIPSOULPROXY_1092 % espodData.get('name', ''), color='#E53900')
            else:
                conditionDesc = ''
            canActive = utils.checkEquipSoulStoneCanActive(schreq, x, y, spid, totalList)
            if not canActive:
                if conditionDesc != '':
                    conditionDesc += '<br>'
                conditionDesc += uiUtils.toHtml(gameStrings.TEXT_EQUIPSOULPROXY_1100, color='#E53900')
            if not isMax:
                ownEnergy = p.getFame(const.XING_CHEN_ZHI_LIN_FAME_ID)
                lastEnergy = ownEnergy - self.usedEnergy if ownEnergy > self.usedEnergy else 0
                needEnergy = ESCD.data.get((spid, self.usedNum + 1), {}).get('energyCon', 0)
                energyDesc = gameStrings.TEXT_EQUIPSOULPROXY_1106 % (format(lastEnergy, ','), format(needEnergy, ','))
                if needEnergy > lastEnergy:
                    energyDesc = uiUtils.toHtml(energyDesc, color='#CC2929')
                if conditionDesc != '':
                    conditionDesc += '<br>'
                conditionDesc += energyDesc
            if not isFull and canActive:
                state = uiUtils.toHtml(gameStrings.TEXT_EQUIPSOULPROXY_1115, color='#73E539')
                operationHint = gameStrings.TEXT_EQUIPSOULPROXY_1116
            else:
                state = uiUtils.toHtml(gameStrings.TEXT_EQUIPSOULPROXY_1118, color='#E53900')
                operationHint = ''
        info['state'] = state
        info['conditionDesc'] = conditionDesc
        info['describe'] = esprdData.get('describe', '')
        info['operationHint'] = operationHint
        return uiUtils.dict2GfxDict(info, True)

    def _getEsprdData(self, school, x, y, spid):
        esprdData = ESPRD.data.get((school,
         x,
         y,
         spid), {})
        if not esprdData and not BigWorld.isPublishedVersion():
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.TEXT_EQUIPSOULPROXY_1132 % (p.school,
             x,
             y,
             self.spid))
        return esprdData

    def _getEspodData(self, spid):
        espodData = ESPOD.data.get(spid, {})
        if not espodData and not BigWorld.isPublishedVersion():
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.COMMON_MSG, gameStrings.TEXT_EQUIPSOULPROXY_1139 % spid)
        return espodData

    def _checkNewestEquipSoulVisible(self):
        if not self.widget:
            return
        else:
            itemMc = getattr(self.widget, 'tabBtn%d' % (SOUL_MAX_NUM - 1), None)
            if not itemMc:
                return
            if not gameglobal.rds.configData.get('enableEquipSoulNewest', False):
                itemMc.visible = False
            return
