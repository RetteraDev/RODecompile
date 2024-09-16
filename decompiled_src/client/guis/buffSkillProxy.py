#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/buffSkillProxy.o
import BigWorld
from Scaleform import GfxValue
import const
import gameglobal
import gamelog
import logicInfo
import uiConst
import commQuest
import gametypes
from callbackHelper import Functor
from guis import events
from guis import tipUtils
from guis import uiUtils
from guis import hotkeyProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from uiProxy import UIProxy
import skillDataInfo
from gameclass import SkillInfo
from data import consumable_item_data as CID
from data import state_data as SD
from data import skill_general_template_data as SGTD
from data import monster_event_trigger_data as METD
from cdata import game_msg_def_data as GMDD
from data import fkey_data as FKD
from data import duel_config_data as DCD
from guis import hotkey as HK
SLOT_MAX_CNT = 5
SLOT_GAP = 85

class BuffSkillProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BuffSkillProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.fKeyType = const.F_NONE
        self.currentEntId = 0
        self.fKeyEntMap = {}

    def reset(self):
        self.slotMCs = {}
        self.infoList = []
        self.infoDict = {}
        self.cooldownCallbacks = {}
        self.infoQueue = []

    def addInfo(self, info, value):
        gamelog.debug('m.l@BuffSkillProxy.addInfo', info, len(self.infoList))
        if self.infoDict.has_key(info):
            return
        if len(self.infoList) >= SLOT_MAX_CNT:
            if info not in self.infoQueue:
                self.infoQueue.append(info)
            return
        self.infoList.append(info)
        self.infoDict[info] = value
        self.addSlotMC(info)
        self.refreshMC()

    def addInfoAtFirst(self, info, value):
        gamelog.debug('m.l@BuffSkillProxy.addInfo', info, len(self.infoList))
        if self.infoDict.has_key(info):
            return
        self.infoList.insert(0, info)
        self.infoDict[info] = value
        self.addSlotMC(info)
        self.refreshMC()

    def removeInfo(self, info):
        gamelog.debug('m.l@BuffSkillProxy.removeInfo', info, self.infoList, self.infoQueue)
        if info in self.infoList:
            self.infoList.remove(info)
        if self.infoDict.has_key(info):
            self.infoDict.pop(info, None)
        self.removeSlotMC(info)
        if len(self.infoList) < SLOT_MAX_CNT:
            if self.infoQueue:
                info = self.infoQueue.pop(0)
                self.addInfo(info, None)
                return
        self.refreshMC()

    def hasInfo(self, info):
        return self.infoDict.has_key(info)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BUFF_SKILL:
            self.widget = widget
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        for info in self.infoList:
            self.addSlotMC(info)

        self.refreshMC()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BUFF_SKILL)
        self.reset()

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BUFF_SKILL)
        else:
            self.initUI()

    def onItemRemove(self, params):
        kind = params[0]
        page = params[1]
        pos = params[2]
        itemId = params[3]
        p = BigWorld.player()
        if kind != const.RES_KIND_INV:
            return
        skillId = CID.data.get(itemId, {}).get('skillId', 0)
        showTempSkill = CID.data.get(itemId, {}).get('showTempSkill', 0)
        if skillId and showTempSkill:
            gamelog.debug('m.l@BuffSkillProxy.onItemRemove', kind, page, pos, itemId)
            ownCount = p.inv.countItemInPages(itemId)
            if not ownCount:
                self.removeInfo((gameglobal.BUFF_SKILL_TYPE_ITEM, itemId))

    def refreshItemChange(self, params):
        kind = params[0]
        page = params[1]
        pos = params[2]
        p = BigWorld.player()
        if kind != const.RES_KIND_INV:
            return
        else:
            item = p.inv.getQuickVal(page, pos)
            if item:
                gamelog.debug('m.l@BuffSkillProxy.refreshItemChange', page, pos)
                skillId = CID.data.get(item.id, {}).get('skillId', 0)
                showTempSkill = CID.data.get(item.id, {}).get('showTempSkill', 0)
                if skillId and showTempSkill:
                    if item.hasLatch():
                        ownCount = p.inv.countItemInPages(item.id)
                        if not ownCount:
                            self.removeInfo((gameglobal.BUFF_SKILL_TYPE_ITEM, item.id))
                    else:
                        self.addInfo((gameglobal.BUFF_SKILL_TYPE_ITEM, item.id), None)
            return

    def getSlotSkillId(self, info):
        skillId = 0
        if info[0] == gameglobal.BUFF_SKILL_TYPE_BUFF:
            skillId = SD.data.get(info[1], {}).get('tempSkillId', 0)
        elif info[0] == gameglobal.BUFF_SKILL_TYPE_ITEM:
            skillId = CID.data.get(info[1], {}).get('skillId', 0)
        return skillId

    def getIconPath(self, info):
        iconPath = 0
        if info[0] == gameglobal.BUFF_SKILL_TYPE_BUFF:
            iconPath = SD.data.get(info[1], {}).get('tempSkillIcon', 'notFound')
        elif info[0] == gameglobal.BUFF_SKILL_TYPE_ITEM:
            iconPath = CID.data.get(info[1], {}).get('tempSkillIcon', 'notFound')
        return iconPath

    def getTempSkillName(self, info):
        skillName = 0
        if info[0] == gameglobal.BUFF_SKILL_TYPE_BUFF:
            skillName = SD.data.get(info[1], {}).get('tempSkillName', '')
            if not skillName:
                skillName = SGTD.data.get(info[1], {}).get('name', '')
        elif info[0] == gameglobal.BUFF_SKILL_TYPE_ITEM:
            skillName = CID.data.get(info[1], {}).get('tempSkillName', '')
            if not skillName:
                skillName = SGTD.data.get(info[1], {}).get('name', '')
        elif info[0] == gameglobal.BUFF_SKILL_TYPE_FKEY:
            skillName = self.getFKeyName(info)
        return skillName

    def addSlotMC(self, info):
        if not self.widget:
            return
        slotMC = self.widget.getInstByClsName('BuffSkill_Slot')
        self.widget.addChild(slotMC)
        slotMC.dragable = False
        skillId = self.getSlotSkillId(info)
        iconPath = self.getIconPath(info)
        if info[0] == gameglobal.BUFF_SKILL_TYPE_FKEY:
            iconPath = self.getFKeyIcon(info)
            slotData = {'id': 0,
             'iconPath': iconPath,
             'overIconPath': iconPath}
        else:
            slotData = uiUtils.getTempSkill(skillId, iconPath)
        slotMC.setItemSlotData(slotData)
        skillName = self.getTempSkillName(info)
        slotMC.nameTF.htmlText = skillName
        ASUtils.setMcData(slotMC, 'extraData', info)
        self.setExtraDescWidget(slotMC, info)
        slotMC.validateNow()
        TipManager.addTipByType(slotMC, tipUtils.TYPE_SKILL, skillId)
        slotMC.addEventListener(events.MOUSE_CLICK, self.onSlotClick, False, 0, True)
        self.slotMCs[info] = slotMC

    def setExtraDescWidget(self, slotMC, info):
        extraDesc = self.getFKeyExtraDesc(info)
        if extraDesc:
            slotMC.descTF.visible = True
            slotMC.descTF.htmlText = extraDesc
        else:
            slotMC.descTF.visible = False

    def removeSlotMC(self, info):
        if not self.widget:
            return
        else:
            slotMC = self.slotMCs.get(info, None)
            self.widget.removeChild(slotMC)
            self.slotMCs.pop(info, None)
            return

    def refreshMC(self):
        if not self.infoList:
            self.hide()
            return
        elif not self.widget:
            if self.infoList:
                self.show()
            return
        else:
            for i in xrange(len(self.infoList)):
                info = self.infoList[i]
                fKeyVisible = True if i == 0 else False
                slotMC = self.slotMCs.get(info, None)
                if slotMC:
                    slotMC.x = SLOT_GAP * i
                    slotMC.fKeyTF.visible = fKeyVisible
                    fkeyName = hotkeyProxy.getPickAsKeyContent()[2]
                    if self.isLeaveZaiJuSkill(info):
                        fkeyName = hotkeyProxy.getAsKeyContent(HK.KEY_LEAVE_ZAIJU)[2]
                    slotMC.fKeyTF.fKeyTF.text = fkeyName

            return

    def onSlotClick(self, *args):
        e = ASObject(args[3][0])
        extraData = e.currentTarget.extraData
        if extraData:
            self.useSkill(extraData)

    def isCqzzBuffId(self, stateId):
        cqzzFlagBuffIDs = DCD.data.get('cqzzFlagBuffID', {})
        return stateId in cqzzFlagBuffIDs.values()

    def useBuffSkill(self, info):
        p = BigWorld.player()
        stateId = info[1]
        if self.isCqzzBuffId(stateId):
            p.base.putDownCqzzFlag()
            gamelog.debug('dxk@BuffSkillProxy putDownCqzzFlag', info[1])
        else:
            skillId = self.getSlotSkillId(info)
            skillInfo = SkillInfo(skillId, 10)
            if not p.checkSkillCanUse(skillInfo):
                return
            if skillInfo.isTargetSkill():
                if p.targetLocked:
                    p.cell.useSkillOfBuff(info[1], p.targetLocked.id)
            elif skillInfo.getSkillData('tgtPos', 0):
                if p.targetLocked:
                    p.cell.useSkillPosOfBuff(info[1], p.targetLocked.position)
                else:
                    p.showGameMsg(GMDD.data.NEED_LOCK_TARGET, ())
            else:
                p.cell.useSkillPosOfBuff(info[1], p.position)
        gamelog.debug('m.l@BuffSkillProxy.onSlotClick useBuff', info[1])

    def useSkill(self, info):
        p = BigWorld.player()
        if info[0] == gameglobal.BUFF_SKILL_TYPE_BUFF:
            self.useBuffSkill(info)
        elif info[0] == gameglobal.BUFF_SKILL_TYPE_ITEM:
            itemId = info[1]
            page, pos = BigWorld.player().inv.findItemInPages(itemId)
            if page != const.CONT_NO_PAGE:
                p.cell.useCommonItem(page, pos, 1, const.RES_KIND_INV)
            gamelog.debug('m.l@BuffSkillProxy.onSlotClick useItem', info[1], page, pos)
        elif info[0] == gameglobal.BUFF_SKILL_TYPE_FKEY:
            self.useFKey(info)

    def getShowingMC(self, infoType, infoId):
        if infoType == gameglobal.BUFF_SKILL_TYPE_BUFF:
            for info, mc in self.slotMCs.iteritems():
                _type = info[0]
                _infoId = info[1]
                if _type == infoType:
                    if SD.data.get(_infoId, {}).get('tempSkillId', 0) == infoId:
                        return mc

        return self.slotMCs.get((infoType, infoId), None)

    def updateCooldown(self):
        if not self.widget:
            return
        else:
            for info, slotMC in self.slotMCs.iteritems():
                try:
                    infoType = int(info[0])
                    if type(info[1]) == tuple:
                        continue
                    infoId = int(info[1])
                    end = 0
                    total = 0
                    remain = 0
                    if infoType == gameglobal.BUFF_SKILL_TYPE_ITEM:
                        remain, total = logicInfo.getItemCooldDownTime(infoId)
                    else:
                        skillId = self.getSlotSkillId(info)
                        end, total = logicInfo.cooldownSkill[skillId]
                        remain = end - BigWorld.time()
                    info = (infoType, infoId)
                    cb = self.cooldownCallbacks.get(info, None)
                    if cb:
                        BigWorld.cancelCallback(cb)
                    if remain <= 0:
                        continue
                    slotMC.playCooldown(total * 1000, (total - remain) * 1000)
                    cb = BigWorld.callback(remain, Functor(self.clearCooldown, infoType, infoId, slotMC))
                    self.cooldownCallbacks[info] = cb
                except:
                    pass

            return

    def clearCooldown(self, infoType, infoId, mc):
        self.cooldownCallbacks.pop((infoType, infoId), None)
        mc.stopCooldown()

    def isLeaveZaiJuSkill(self, info):
        if info[0] == gameglobal.BUFF_SKILL_TYPE_BUFF and SD.data.get(info[1], {}).get('useF8Key', False):
            return True
        return False

    def pressFKey(self):
        if not self.widget or not self.infoList:
            return
        info = self.infoList[0]
        if self.isLeaveZaiJuSkill(info):
            return
        self.useSkill(info)

    def pressLeaveZaiJu(self):
        if not self.widget or not self.infoList:
            return
        info = self.infoList[0]
        if not self.isLeaveZaiJuSkill(info):
            return
        self.useSkill(info)

    def addFKeyInfo(self, fType, entId, value = None):
        oldFType = self.fKeyType
        oldEntId = self.currentEntId
        self.fKeyEntMap.setdefault(fType, set([]))
        self.fKeyEntMap[fType].add(entId)
        if fType < self.fKeyType or self.fKeyType == const.F_NONE:
            self.fKeyType = fType
            self.currentEntId = entId
        elif fType == self.fKeyType:
            self.currentEntId = self.searchNearstEntId(fType)
        self.changeFKeyView(oldFType, oldEntId, self.fKeyType, self.currentEntId, value)

    def removeFKeyInfo(self, fType, entId):
        oldFType = self.fKeyType
        oldEntId = self.currentEntId
        entIdSet = self.fKeyEntMap.get(fType, None)
        if entIdSet and entId in entIdSet:
            entIdSet.remove(entId)
        if oldEntId == entId:
            if entIdSet:
                self.currentEntId = self.searchNearstEntId()
            else:
                self.fKeyType = const.F_NONE
                self.currentEntId = 0
                for fType in xrange(oldFType, const.F_TYPE_MAX_NUM):
                    newEntId = self.searchNearstEntId(fType)
                    if newEntId:
                        self.fKeyType = fType
                        self.currentEntId = newEntId
                        break

        self.changeFKeyView(oldFType, oldEntId, self.fKeyType, self.currentEntId)

    def clearFKeyInfo(self):
        oldFType = self.fKeyType
        oldEntId = self.currentEntId
        self.fKeyType = const.F_NONE
        self.currentEntId = 0
        self.changeFKeyView(oldFType, oldEntId, self.fKeyType, self.currentEntId)

    def searchNearstEntId(self, fType):
        entIdSet = self.fKeyEntMap.get(fType, None)
        nearstEntId = 0
        nearstDis = 1000000
        player = BigWorld.player()
        if entIdSet:
            entIds = list(entIdSet)
            for entId in entIds:
                ent = BigWorld.entity(entId)
                if ent == None or not ent.inWorld:
                    entIdSet.remove(entId)
                    continue
                tempDist = (ent.position - player.position).lengthSquared
                if tempDist < nearstDis:
                    nearstDis = nearstDis
                    nearstEntId = entId

        return nearstEntId

    def changeFKeyView(self, oldFType, oldEntId, newFType, newEntId, value = None):
        if (oldFType, oldEntId) == (newFType, newEntId) and newFType != const.F_MONSTER:
            return
        else:
            for info in self.infoDict.keys():
                if info[0] == gameglobal.BUFF_SKILL_TYPE_FKEY:
                    fType, entId, subInfo = info[1]
                    if entId == oldEntId and fType == oldFType:
                        self.removeInfo(info)

            player = BigWorld.player()
            if newFType == const.F_MONSTER:
                ent = BigWorld.entity(newEntId)
                eventIdxs = commQuest.getAllTriggerEvent(player, ent)
                for idx in eventIdxs:
                    self.addInfoAtFirst((gameglobal.BUFF_SKILL_TYPE_FKEY, (newFType, newEntId, idx)), value)

            elif newFType != const.F_NONE:
                self.addInfo((gameglobal.BUFF_SKILL_TYPE_FKEY, (newFType, newEntId, None)), value)
            return

    def getMonsterFKey(self, info):
        fType, entId, subInfo = info[1]
        fKey = 0
        ent = BigWorld.entity(entId)
        if ent and ent.inWorld:
            charType = ent.charType
            metd = METD.data.get(charType, [])
            eventData = metd[subInfo]
            p = BigWorld.player()
            fKey = eventData.get('fKey', 0)
            if eventData.get('teamMode') and p.groupNUID:
                if not p.groupActionState:
                    if p.isGroupInAction():
                        fKey = eventData.get('joinF', 0)
                    else:
                        fKey = eventData.get('readyF')
                elif p.groupActionState == gametypes.GROUP_ACTION_STATE_PREPARE:
                    fKey = eventData.get('cancelF')
        return fKey

    def getFKeyName(self, info):
        fType, entId, subInfo = info[1]
        if fType == const.F_MONSTER:
            fKey = self.getMonsterFKey(info)
            path, desc = uiUtils.getFKeyPathDesc(fKey)
            return desc
        data = self.infoDict.get(info)
        if info:
            return data[1]
        return ''

    def getFKeyIcon(self, info):
        fType, entId, subInfo = info[1]
        if fType == const.F_MONSTER:
            fKey = self.getMonsterFKey(info)
            path, desc = uiUtils.getFKeyPathDesc(fKey)
            return path
        data = self.infoDict.get(info)
        if data:
            return data[0]
        return ''

    def getFKeyExtraDesc(self, info):
        if info[0] == gameglobal.BUFF_SKILL_TYPE_FKEY and info[1][0] == const.F_MONSTER:
            fKey = self.getMonsterFKey(info)
            return FKD.data.get(fKey, {}).get('extraDesc', '')
        value = self.infoDict.get(info, [])
        if value and len(value) > 2:
            return value[2]
        return ''

    def useFKey(self, info):
        fType, entId, subInfo = info[1]
        player = BigWorld.player()
        if fType == const.F_MONSTER:
            player.cell.triggerMonsterEvent(entId, subInfo)
        elif self.fKeyType != const.F_NONE:
            player.pickNearByItems(True)

    def getVisible(self):
        p = BigWorld.player()
        if p.inBoothing() or p.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            return False
        return True

    def refreshVisible(self):
        if not self.widget:
            return
        visible = self.getVisible()
        self.widget.visible = visible
