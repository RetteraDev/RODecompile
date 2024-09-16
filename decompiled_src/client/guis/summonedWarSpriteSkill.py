#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteSkill.o
import BigWorld
import gameglobal
import gamelog
import const
import events
import skillDataInfo
import tipUtils
import ui
import gametypes
from guis import uiUtils
from asObject import ASUtils
from item import Item
from asObject import ASObject
from callbackHelper import Functor
from guis import uiConst
from gamestrings import gameStrings
from guis.asObject import TipManager
from data import sys_config_data as SYSCD
from data import summon_sprite_skill_data as SSSD
from data import consumable_item_data as CID
from data import item_data as ID
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from cdata import summon_sprite_skill_replace_relation_data as SSSRRD
LEARN_SKILL_COLUMN_COUNT = 4
LEARN_SKILL_ITEM_HEIGHT = 65
LEARN_SKILL_ITEM_WIDTH = 65
PROPERTY_HEIGHT = 27
SKILL_SLOT_NUM = 8
SPRITE_SKILL_LEVEL = 1
SKILL_SLOT_TIP_DIFF_INDEX = 4
SKILL_SLOT_FORBIDDEN_NONE = 0
SHOW_SKILL_MC_TYPE0 = 0
SHOW_SKILL_MC_TYPE1 = 1
SHOW_SKILL_MC_TYPE2 = 2
SHOW_SKILL_MC_TYPE3 = 3

class SummonedWarSpriteSkill(object):

    def __init__(self, proxy):
        super(SummonedWarSpriteSkill, self).__init__()
        self.parentProxy = proxy
        self.learnSkillPanel = None
        self.currSelectLearnSkillItem = None
        self.currSelectLearnSkillId = None
        self.selectedSkillSlot = None
        self.showSkillMcType = SHOW_SKILL_MC_TYPE0
        self.disableLearnSkills = None
        self.replaceSkillPanel = None
        self.curReplaceSelectSkillId = None
        self.curReplaceSelectSkillItem = None
        self.allLearnedSkills = []
        self.besetSkillPanel = None
        self.curBesetSelectSkillId = None
        self.curBesetSelectSkillItem = None

    def getWidget(self):
        return self.parentProxy.widget

    def getCurSelectSpriteInfo(self):
        idx = self.parentProxy.currSelectItemSpriteIndex
        return BigWorld.player().summonSpriteList.get(idx, {})

    def hideWidget(self):
        self.reset()

    def showWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        self.reset()
        self.parentProxy.updateTabBtnState()

    def refreshWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        self.updateSkillMcVisible()
        skillMc = widget.mineWarSpritePanel.skillMc
        showSelectSkillMc = skillMc.showSelectSkillMc
        skillMc.unlockSlotBtn.addEventListener(events.BUTTON_CLICK, self.handleUnlockSlotClick, False, 1, True)
        skillMc.learnSkillBtn.addEventListener(events.BUTTON_CLICK, self.handleLearnSkill, False, 1, True)
        skillMc.skillTransferBtn.addEventListener(events.BUTTON_CLICK, self.handleSkillTransferBtnClick, False, 1, True)
        showSelectSkillMc.forgetSkillBtn.addEventListener(events.BUTTON_CLICK, self.handleForgetSkill, False, 1, True)
        showSelectSkillMc.replaceBtn.addEventListener(events.BUTTON_CLICK, self.handleReplaceBtnClick, False, 1, True)
        showSelectSkillMc.besetBtn.addEventListener(events.BUTTON_CLICK, self.handleBesetBtnClick, False, 1, True)
        skillMc.skillTransferBtn.visible = gameglobal.rds.configData.get('enableSpriteSkillTransfer', False)
        skillMc.spriteSkillHelp.helpKey = SYSCD.data.get('spriteSkillHelp', 0)
        self.updateConsumesNum(skillMc)
        self.refreshSkillMCs()
        self.updateSelectedSkillSlotIcon(self.selectedSkillSlot)
        self.updateLearnSkillBookPanel()
        self.updateReplaceSkillBookPanel()
        self.updateBesetSkillBookPanel()
        self.setTemplateState()

    def setTemplateState(self):
        p = BigWorld.player()
        if p.isUsingTemp():
            widget = self.getWidget()
            skillMc = widget.mineWarSpritePanel.skillMc
            skillMc.unlockSlotBtn.visible = False
            skillMc.learnSkillBtn.visible = False
            skillMc.skillTransferBtn.visible = False
            skillMc.besetSkillMc.visible = False
            skillMc.showSelectSkillMc.forgetSkillBtn.visible = False
            skillMc.showSelectSkillMc.besetBtn.visible = False
            skillMc.showSelectSkillMc.replaceBtn.visible = False

    def updateConsumesNum(self, skillMc):
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteConsumesDict = SYSCD.data.get('spriteSkillConsumes', {})
        logSrc = spriteConsumesDict.get('logSrc', 505)
        itemId = spriteConsumesDict.get('itemId', 785012)
        _consumesDict = spriteInfo.get('_consumesDict', {})
        itemNum = _consumesDict.get(logSrc, {}).get(itemId, 0)
        skillMc.consumesT.text = itemNum

    def getLearnedSkillInfo(self, spriteInfo):
        infos = {}
        learnedSkills = spriteInfo.get('skills', {}).get('learns', [])
        if learnedSkills:
            for info in learnedSkills:
                infos[info.get('part', None)] = info

        return infos

    def getDisableLearnSkills(self, learnedSkillInfos):
        disableSkills = ()
        for i, part in enumerate(learnedSkillInfos):
            info = learnedSkillInfos[part]
            spriteSkillId = info.get('id', 0)
            if spriteSkillId:
                disableLearnSkillRefIds = SSSD.data.get(spriteSkillId, {}).get('disableLearnSkillRefIds', ())
                disableSkills += disableLearnSkillRefIds

        return disableSkills

    def refreshSkillMCs(self):
        widget = self.getWidget()
        if not widget:
            return
        else:
            skillMc = widget.mineWarSpritePanel.skillMc
            spriteInfo = self.getCurSelectSpriteInfo()
            learnedSkillInfos = self.getLearnedSkillInfo(spriteInfo)
            self.disableLearnSkills = self.getDisableLearnSkills(learnedSkillInfos)
            self.allLearnedSkills = []
            for i in xrange(SKILL_SLOT_NUM):
                info = learnedSkillInfos.get(i, None)
                if info:
                    slotMC = getattr(skillMc, 'skillSlot' + str(i), None)
                    slotMC.slotIdx = i
                    self.allLearnedSkills.append(info.get('id', 0))
                    self.refreshSingleSkillMC(slotMC, info)

            return

    def refreshSingleSkillMC(self, slotMC, info):
        if slotMC:
            slotMC.lvTF.visible = False
            slotState = info.get('slot', 0)
            spriteSkillId = info.get('id', 0)
            slotMC.lockMC.visible = slotState == const.SSPRITE_SKILL_SLOT_PROTECT
            stateLocked = slotState == const.SSPRITE_SKILL_SLOT_FORBIDDEN
            slotMC.slotMC.lockMC.visible = stateLocked
            ASUtils.setHitTestDisable(slotMC.slotMC.lockMC, stateLocked)
            skillId = SSSD.data.get(spriteSkillId, {}).get('virtualSkill', 0)
            slot = slotMC.slotMC.slot
            slotMC.skillId = skillId
            slotMC.data = info
            slotMC.spriteSkillId = spriteSkillId
            if skillId:
                skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=SPRITE_SKILL_LEVEL)
                iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
                slot.fitSize = True
                slot.dragable = False
                slot.setItemSlotData({'iconPath': iconPath})
                slotMC.nameTF.text = skillInfo.getSkillData('sname', '')
                slotMC.bgTF.visible = True
                ASUtils.setHitTestDisable(slot, False)
            else:
                slotMC.nameTF.text = ''
                slotMC.bgTF.visible = False
                slot.setItemSlotData(None)
                ASUtils.setHitTestDisable(slot, True)
            slotMC.selectedMC.visible = True if self.selectedSkillSlot and skillId and self.selectedSkillSlot.skillId == skillId else False
            slotMC.skillName = slotMC.nameTF.text
            slotMC.losePic.visible = False
            slot.setSlotState(uiConst.ITEM_NORMAL)
            if spriteSkillId and spriteSkillId in self.disableLearnSkills:
                slotMC.losePic.visible = True
                slot.setSlotState(uiConst.ITEM_GRAY)
                ASUtils.setHitTestDisable(slotMC.losePic, True)
            slotMC.learnSkillSucSfx.visible = False
            ASUtils.setHitTestDisable(slotMC.learnSkillSucSfx, True)
            slotMC.addEventListener(events.MOUSE_CLICK, self.handleSelectSkillSlot, False, 1, True)
            if skillId:
                slot.validateNow()
                TipManager.addTipByType(slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
                 'lv': SPRITE_SKILL_LEVEL}, False, 'upLeft')
            else:
                self.updateSkillSlotMcTip(slotMC.slotMC, slotMC.slotIdx, slotState)

    def updateSkillSlotMcTip(self, slotMC, slotIdx, slotState):
        if slotIdx <= SKILL_SLOT_TIP_DIFF_INDEX:
            if slotState == const.SSPRITE_SKILL_SLOT_EMPTY:
                tipMsg = GMD.data.get(GMDD.data.SPRITE_SLOTIDX_FIRST_5_LV_UP_TIP, {}).get('text', '')
                TipManager.addTip(slotMC, tipMsg)
            elif slotState == const.SSPRITE_SKILL_SLOT_FORBIDDEN:
                tipMsg = GMD.data.get(GMDD.data.SPRITE_SLOTIDX_FIRST_5_UNLOCK_TIP, {}).get('text', '')
                TipManager.addTip(slotMC, tipMsg)
            else:
                TipManager.removeTip(slotMC)
        elif slotState == const.SSPRITE_SKILL_SLOT_EMPTY:
            tipMsg = GMD.data.get(GMDD.data.SPRITE_SLOTIDX_AFTER_3_LV_UP_TIP, {}).get('text', '')
            TipManager.addTip(slotMC, tipMsg)
        elif slotState == const.SSPRITE_SKILL_SLOT_FORBIDDEN:
            tipMsg = GMD.data.get(GMDD.data.SPRITE_SLOTIDX_AFTER_3_UNLOCK_TIP, {}).get('text', '')
            TipManager.addTip(slotMC, tipMsg)
        else:
            TipManager.removeTip(slotMC)

    def handleSelectSkillSlot(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        self.setSlotSelected(target)

    def setSlotSelected(self, target):
        dataInfo = target.data
        if dataInfo.get('slot', -1) in (const.SSPRITE_SKILL_SLOT_FORBIDDEN, const.SSPRITE_SKILL_SLOT_EMPTY):
            gamelog.debug('m.l@SummonedWarSpriteSkill.handleSelectSkillSlot return ', dataInfo)
            return
        self.showSkillMcType = SHOW_SKILL_MC_TYPE0
        self.updateSkillMcVisible()
        if self.selectedSkillSlot and self.selectedSkillSlot.selectedMC:
            self.selectedSkillSlot.selectedMC.visible = False
        self.selectedSkillSlot = target
        self.selectedSkillSlot.selectedMC.visible = True
        self.updateSelectedSkillSlotIcon(target)

    def updateSelectedSkillSlotIcon(self, target):
        widget = self.getWidget()
        if not widget:
            return
        else:
            p = BigWorld.player()
            skillMc = widget.mineWarSpritePanel.skillMc
            showSelectSkillMc = skillMc.showSelectSkillMc
            slot = showSelectSkillMc.showSkillSlot.slotMC.slot
            skillId = target.skillId if target else 0
            spriteSkillId = target.spriteSkillId if target else 0
            skillLv = SPRITE_SKILL_LEVEL
            if not target or not skillId:
                if target:
                    TipManager.removeTip(target)
                slot.setItemSlotData(None)
                showSelectSkillMc.descTF1.visible = False
                showSelectSkillMc.descTF2.visible = True
                showSelectSkillMc.descTF2.htmlText = SYSCD.data.get('spriteNoneSelectSkillDesc', '')
                showSelectSkillMc.showSkillSlot.visible = False
                showSelectSkillMc.forgetSkillBtn.visible = False
                showSelectSkillMc.besetBtn.visible = False
            else:
                TipManager.addTipByType(target, tipUtils.TYPE_SKILL, {'skillId': skillId,
                 'lv': skillLv}, False, 'upLeft')
                skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=skillLv)
                iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
                slot.fitSize = True
                slot.dragable = False
                slot.setItemSlotData({'iconPath': iconPath})
                slot.validateNow()
                TipManager.addTipByType(slot, tipUtils.TYPE_SKILL, {'skillId': skillId,
                 'lv': skillLv}, False, 'upLeft')
                showSelectSkillMc.showSkillSlot.visible = True
                showSelectSkillMc.showSkillSlot.lockMC.visible = False
                showSelectSkillMc.showSkillSlot.slotMC.lockMC.visible = False if skillId else True
                showSelectSkillMc.showSkillSlot.nameTF.text = skillInfo.getSkillData('sname', '')
                showSelectSkillMc.showSkillSlot.bgTF.visible = True
                slotLocked = target.data.get('slot', -1) == const.SSPRITE_SKILL_SLOT_PROTECT
                showSelectSkillMc.showSkillSlot.lockMC.visible = True if slotLocked else False
                skillTipsInfo = p.getSkillTipsInfo(skillId, skillLv)
                virtualDesc = skillTipsInfo.getSkillData('virtualDesc', '')
                showSelectSkillMc.descTF1.visible = True
                showSelectSkillMc.descTF2.visible = False
                showSelectSkillMc.descTF1.text = virtualDesc
                showSelectSkillMc.forgetSkillBtn.visible = True
                showSelectSkillMc.forgetSkillBtn.enabled = not slotLocked
                showSelectSkillMc.besetBtn.visible = gameglobal.rds.configData.get('enableSpriteSkillBeset', False)
                losePic = showSelectSkillMc.showSkillSlot.losePic
                losePic.visible = False
                slot.setSlotState(uiConst.ITEM_NORMAL)
                if spriteSkillId and spriteSkillId in self.disableLearnSkills:
                    losePic.visible = True
                    slot.setSlotState(uiConst.ITEM_GRAY)
                    ASUtils.setHitTestDisable(losePic, True)
            learnSkillSucSfx = showSelectSkillMc.showSkillSlot.learnSkillSucSfx
            learnSkillSucSfx.visible = False
            ASUtils.setHitTestDisable(learnSkillSucSfx, False)
            showSelectSkillMc.showSkillSlot.lvTF.visible = False
            showSelectSkillMc.showSkillSlot.selectedMC.visible = False
            forbidden = self.getSkillSlotStateNum(const.SSPRITE_SKILL_SLOT_FORBIDDEN)
            skillMc.learnSkillBtn.enabled = False if forbidden == const.SSPRITE_LEARN_SKILL_LIMIT else True
            skillMc.unlockSlotBtn.enabled = False if forbidden == SKILL_SLOT_FORBIDDEN_NONE else True
            showSelectSkillMc.replaceBtn.visible = True if spriteSkillId in SSSRRD.data else False
            self.setTemplateState()
            return

    def getLearnSkillBookInfo(self):
        ret1 = []
        ret2 = []
        items = BigWorld.player().inv.countItemsInPagesBySType(Item.SUBTYPE_2_SPRITE_TEXTBOOK)
        if items:
            for i, v in enumerate(items.iteritems()):
                itemId = v[0]
                num = v[1]
                teachSpriteSkill = CID.data.get(itemId, {}).get('teachSpriteSkill', 0)
                if teachSpriteSkill and (teachSpriteSkill in self.allLearnedSkills or teachSpriteSkill in self.disableLearnSkills):
                    ret2.append([itemId, num, True])
                else:
                    ret1.append([itemId, num, False])

        ret = []
        for i, v in enumerate(ret1 + ret2):
            itemId = v[0]
            num = v[1]
            isLearned = v[2]
            ret.append({'itemId': itemId,
             'itemNum': num,
             'numberId': i,
             'isLearned': isLearned})

        return ret

    def getReplaceSkillBookInfo(self):
        spriteSkillId = 0
        if self.selectedSkillSlot:
            spriteSkillId = self.selectedSkillSlot.spriteSkillId
        replaceData = SSSRRD.data.get(spriteSkillId, [])
        if not replaceData:
            return []
        ret = []
        items = BigWorld.player().inv.countItemsInPagesBySType(Item.SUBTYPE_2_SPRITE_TEXTBOOK)
        if items:
            for i, v in enumerate(items.iteritems()):
                itemId = v[0]
                num = v[1]
                teachSpriteSkill = CID.data.get(itemId, {}).get('teachSpriteSkill', 0)
                if teachSpriteSkill in replaceData:
                    ret.append({'itemId': itemId,
                     'itemNum': num,
                     'numberId': i,
                     'isLearned': False})

        return ret

    def getBesetSkillBookInfo(self):
        if not self.selectedSkillSlot:
            return []
        spriteSkillId = self.selectedSkillSlot.spriteSkillId
        oldLearnSkillHigh = SSSD.data.get(spriteSkillId, {}).get('learnSkillHigh', gametypes.SPRITE_LEARN_SKILL_LOW)
        ret1 = []
        ret2 = []
        items = BigWorld.player().inv.countItemsInPagesBySType(Item.SUBTYPE_2_SPRITE_TEXTBOOK)
        if items:
            for i, v in enumerate(items.iteritems()):
                itemId = v[0]
                num = v[1]
                teachSpriteSkill = CID.data.get(itemId, {}).get('teachSpriteSkill', 0)
                disableLearnSkillRefIds = SSSD.data.get(teachSpriteSkill, {}).get('disableLearnSkillRefIds', ())
                disableSkillRefId = disableLearnSkillRefIds[0] if disableLearnSkillRefIds else 0
                disableSkillId = SSSD.data.get(disableSkillRefId, {}).get('virtualSkill', 0)
                learnSkillHigh = SSSD.data.get(teachSpriteSkill, {}).get('learnSkillHigh', gametypes.SPRITE_LEARN_SKILL_LOW)
                if oldLearnSkillHigh in [gametypes.SPRITE_LEARN_SKILL_LOW, gametypes.SPRITE_LEARN_SKILL_HIGH] and learnSkillHigh in [gametypes.SPRITE_LEARN_SKILL_LOW, gametypes.SPRITE_LEARN_SKILL_HIGH]:
                    if teachSpriteSkill and (teachSpriteSkill in self.allLearnedSkills or teachSpriteSkill in self.disableLearnSkills or self.checkDisableLearnedSkill(disableSkillId)):
                        ret2.append([itemId, num, True])
                    else:
                        ret1.append([itemId, num, False])
                elif oldLearnSkillHigh == gametypes.SPRITE_LEARN_SKILL_ULTIMATE:
                    if teachSpriteSkill and (teachSpriteSkill in self.allLearnedSkills or teachSpriteSkill in self.disableLearnSkills or self.checkDisableLearnedSkill(disableSkillId)):
                        ret2.append([itemId, num, True])
                    else:
                        ret1.append([itemId, num, False])

        ret = []
        for i, v in enumerate(ret1 + ret2):
            itemId = v[0]
            num = v[1]
            isLearned = v[2]
            ret.append({'itemId': itemId,
             'itemNum': num,
             'numberId': i,
             'isLearned': isLearned})

        return ret

    def skillItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.setSkillBookData(itemData, itemMc)
        itemMc.selected = False
        if self.currSelectLearnSkillId and self.currSelectLearnSkillId == itemData.itemId:
            itemMc.selected = True
        elif not self.currSelectLearnSkillId and itemData.numberId == 0:
            itemMc.selected = True
        itemMc.disabled = itemData.isLearned
        if itemMc.selected:
            self.currSelectLearnSkillId = itemData.itemId
            self.currSelectLearnSkillItem = itemMc
            self.updateLearnSkillConsumeMc()
            self.updateLearnBtnState(itemData.isLearned)
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleLearnSkillSlotClick, False, 0, True)

    def handleLearnSkillSlotClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if self.currSelectLearnSkillItem:
            self.currSelectLearnSkillItem.selected = False
        target.selected = True
        self.currSelectLearnSkillId = target.itemId
        self.currSelectLearnSkillItem = target
        self.updateLearnSkillConsumeMc()
        self.updateLearnBtnState(target.isLearned)

    def updateLearnBtnState(self, isLearned = False):
        if not self.learnSkillPanel:
            return
        if not self.currSelectLearnSkillItem:
            return
        skillId = SSSD.data.get(self.currSelectLearnSkillItem.teachSpriteSkill, {}).get('virtualSkill', 0)
        skillName = self.getSkillName(skillId)
        if isLearned:
            self.learnSkillPanel.sureLearnSkilllBtn.disabled = True
            TipManager.addTip(self.learnSkillPanel.sureLearnSkilllBtn, gameStrings.SPRITE_LEARNED_SILL_TIP % skillName)
        else:
            self.learnSkillPanel.sureLearnSkilllBtn.disabled = False
            TipManager.removeTip(self.learnSkillPanel.sureLearnSkilllBtn)

    def updateLearnSkillConsumeMc(self):
        widget = self.getWidget()
        if not widget:
            return
        skillMc = widget.mineWarSpritePanel.skillMc
        learnConsumeMc = skillMc.learnSkillMc.learnConsumeMc
        learnConsumeMc.consumeIcon.bonusType = 'bindCash'
        learnConsumeMc.consumeValueText.text = ID.data.get(self.currSelectLearnSkillId, {}).get('learnSpriteSkillSpendCash', 0)

    def handleComfirmLearnSkill(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.disabled:
            return
        selectItem = self.currSelectLearnSkillItem
        if selectItem:
            p = BigWorld.player()
            itemId = selectItem.itemId
            spriteInfo = self.getCurSelectSpriteInfo()
            selectedIndex = spriteInfo.get('index', -99)
            page, pos = p.inv.findItemInPages(itemId)
            if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.SPRITE_LEARN_SKILL_NO_ITEM, ())
                return
            primarySkillId = SSSD.data.get(selectItem.teachSpriteSkill, {}).get('virtualSkill', 0)
            disableLearnSkillRefIds = SSSD.data.get(selectItem.teachSpriteSkill, {}).get('disableLearnSkillRefIds', ())
            disableSkillRefId = disableLearnSkillRefIds[0] if disableLearnSkillRefIds else 0
            disableSkillId = SSSD.data.get(disableSkillRefId, {}).get('virtualSkill', 0)
            primaryName = self.getSkillName(primarySkillId)
            if disableSkillRefId and self.checkDisableLearnedSkill(disableSkillId):
                replaceName = self.getSkillName(disableSkillId)
                msg = SYSCD.data.get('hasDisableSkillWillReplace', '%s%s') % (primaryName, replaceName)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.checkBindCash, selectedIndex, itemId, page, pos))
            elif self.checkLearnedSkill():
                alreadyUltimateCount = self.getUltimalteSkillCount()
                maxUltimateCount = SYSCD.data.get('spriteUltimateSkillNumLimit', 3)
                if self.isUltimateLevelSkill(selectItem.teachSpriteSkill) and alreadyUltimateCount >= maxUltimateCount:
                    msg = SYSCD.data.get('ultimateSkillMoreWillReplace', '%d%s') % (maxUltimateCount, primaryName)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.checkBindCash, selectedIndex, itemId, page, pos))
                elif not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_SPRITE_LEARNED_SKILL):
                    msg = SYSCD.data.get('nilDisableSkillMaybeRepalce', '%s') % primaryName
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.checkBindCash, selectedIndex, itemId, page, pos), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_SPRITE_LEARNED_SKILL)
                else:
                    self.checkBindCash(selectedIndex, itemId, page, pos)
            else:
                self.checkBindCash(selectedIndex, itemId, page, pos)

    def checkBindCash(self, selectedIndex, itemId, page, pos):
        p = BigWorld.player()
        cashNeed = ID.data.get(self.currSelectLearnSkillId, {}).get('learnSpriteSkillSpendCash', 0)
        if p.bindCash < cashNeed:
            msg = uiUtils.getTextFromGMD(GMDD.data.BINDCASH_IS_NOT_ENOUGH, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realComfirm, selectedIndex, itemId, page, pos), msgType='bindCash', isShowCheckBox=True)
        else:
            self.realComfirm(selectedIndex, itemId, page, pos)

    @ui.checkInventoryLock()
    def realComfirm(self, selectedIndex, itemId, page, pos):
        p = BigWorld.player()
        p.base.useSpriteTextBook(selectedIndex, itemId, page, pos, p.cipherOfPerson)

    def checkDisableLearnedSkill(self, disableSkillId):
        widget = self.getWidget()
        if not widget:
            return
        else:
            skillMc = widget.mineWarSpritePanel.skillMc
            for i in xrange(SKILL_SLOT_NUM):
                slotMC = getattr(skillMc, 'skillSlot' + str(i), None)
                if slotMC and disableSkillId and slotMC.skillId == disableSkillId:
                    return True

            return False

    def checkLearnedSkill(self):
        widget = self.getWidget()
        if not widget:
            return
        else:
            skillMc = widget.mineWarSpritePanel.skillMc
            for i in xrange(SKILL_SLOT_NUM):
                slotMC = getattr(skillMc, 'skillSlot' + str(i), None)
                if slotMC and slotMC.skillId:
                    return True

            return False

    def getUltimalteSkillCount(self):
        widget = self.getWidget()
        if not widget:
            return
        else:
            count = 0
            skillMc = widget.mineWarSpritePanel.skillMc
            for i in xrange(SKILL_SLOT_NUM):
                slotMC = getattr(skillMc, 'skillSlot' + str(i), None)
                if slotMC and slotMC.spriteSkillId and self.isUltimateLevelSkill(slotMC.spriteSkillId):
                    count += 1

            return count

    def isUltimateLevelSkill(self, spriteSkillId):
        return SSSD.data.get(spriteSkillId, {}).get('learnSkillHigh', gametypes.SPRITE_LEARN_SKILL_DEFAULT) == gametypes.SPRITE_LEARN_SKILL_ULTIMATE

    def handleCancelLeanSkillSpriteBtnClick(self, *args):
        widget = self.getWidget()
        if not widget:
            return
        else:
            self.currSelectLearnSkillId = None
            self.showSkillMcType = SHOW_SKILL_MC_TYPE0
            self.updateSkillMcVisible()
            return

    def cancelSlotSelectedMc(self):
        if self.selectedSkillSlot and self.selectedSkillSlot.selectedMC:
            self.selectedSkillSlot.selectedMC.visible = False
            self.selectedSkillSlot = None
            self.updateSelectedSkillSlotIcon(self.selectedSkillSlot)

    def showLearnSkillBookMC(self, target, skillBookInfo):
        widget = self.getWidget()
        if not widget:
            return
        self.cancelSlotSelectedMc()
        self.updateSkillMcVisible()
        skillMc = widget.mineWarSpritePanel.skillMc
        learnSkillMc = skillMc.learnSkillMc
        self.learnSkillPanel = learnSkillMc
        self.learnSkillPanel.getSkillWayHelp.helpKey = SYSCD.data.get('getSkillWayHelp', 0)
        self.learnSkillPanel.titleTF.text = gameStrings.SPRITE_SKILL_PANEL_TITLE
        self.learnSkillPanel.learnSkillList.itemHeight = LEARN_SKILL_ITEM_HEIGHT
        self.learnSkillPanel.learnSkillList.itemRenderer = 'SummonedWarSpriteMine_skillLearnItem'
        self.learnSkillPanel.learnSkillList.dataArray = skillBookInfo
        self.learnSkillPanel.learnSkillList.lableFunction = self.skillItemFunction
        self.learnSkillPanel.learnSkillList.validateNow()
        self.learnSkillPanel.learnSkillList.scrollToHead()
        self.skillPanelControlVisible(skillBookInfo)
        self.learnSkillPanel.sureLearnSkilllBtn.addEventListener(events.MOUSE_CLICK, self.handleComfirmLearnSkill, False, 0, True)
        self.learnSkillPanel.cancelSkillBtn.addEventListener(events.MOUSE_CLICK, self.handleCancelLeanSkillSpriteBtnClick, False, 0, True)

    def skillPanelControlVisible(self, skillBookInfo):
        self.learnSkillPanel.sureLearnSkilllBtn.enabled = True if skillBookInfo else False
        self.learnSkillPanel.learnConsumeMc.visible = True if skillBookInfo else False
        self.learnSkillPanel.descTF3.visible = False if skillBookInfo else True
        self.learnSkillPanel.descTF3.htmlText = SYSCD.data.get('getSpriteSkillBookDesc', '')

    def updateLearnSkillBookPanel(self):
        widget = self.getWidget()
        if not widget:
            return
        else:
            if self.learnSkillPanel and self.learnSkillPanel.stage:
                skillBookInfo = self.getLearnSkillBookInfo()
                if not self.checkInLearnSkillBook(skillBookInfo):
                    self.currSelectLearnSkillId = None
                self.learnSkillPanel.learnSkillList.dataArray = skillBookInfo
                if not self.currSelectLearnSkillId:
                    self.learnSkillPanel.learnSkillList.validateNow()
                    self.learnSkillPanel.learnSkillList.scrollToHead()
                self.skillPanelControlVisible(skillBookInfo)
            return

    def checkInLearnSkillBook(self, skillBookInfo):
        for items in skillBookInfo:
            if self.currSelectLearnSkillId and self.currSelectLearnSkillId == items.get('itemId', 0):
                return True

        return False

    def handleReplaceBtnClick(self, *args):
        self.showSkillMcType = SHOW_SKILL_MC_TYPE2
        replaceBookInfo = self.getReplaceSkillBookInfo()
        self.showReplaceSkillBookMc(replaceBookInfo)

    def handleBesetBtnClick(self, *args):
        self.showSkillMcType = SHOW_SKILL_MC_TYPE3
        besetBookInfo = self.getBesetSkillBookInfo()
        self.showBesetSkillBookMc(besetBookInfo)

    def showBesetSkillBookMc(self, besetBookInfo):
        widget = self.getWidget()
        if not widget:
            return
        skillMc = widget.mineWarSpritePanel.skillMc
        besetSkillMc = skillMc.besetSkillMc
        if besetSkillMc.visible:
            return
        self.updateSkillMcVisible()
        self.besetSkillPanel = besetSkillMc
        self.besetSkillPanel.besetHelpIcon.helpKey = SYSCD.data.get('spriteSkillBesetHelpIcon', 0)
        self.besetSkillPanel.besetSkillList.itemHeight = LEARN_SKILL_ITEM_HEIGHT
        self.besetSkillPanel.besetSkillList.itemRenderer = 'SummonedWarSpriteMine_skillLearnItem'
        self.besetSkillPanel.besetSkillList.dataArray = besetBookInfo
        self.besetSkillPanel.besetSkillList.lableFunction = self.besetSkillFunction
        self.besetSkillPanel.besetSkillList.validateNow()
        self.besetSkillPanel.besetSkillList.scrollToHead()
        self.besetSkillPanel.besetBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBesetBtnClick, False, 0, True)
        self.besetSkillPanel.thinkBtn.addEventListener(events.BUTTON_CLICK, self.handleThinkBesetBtnClick, False, 0, True)
        self.updateConsumeBesetItem()

    def updateConsumeBesetItem(self):
        if not self.selectedSkillSlot:
            return
        p = BigWorld.player()
        spriteSkillId = self.selectedSkillSlot.spriteSkillId
        learnSkillHigh = SSSD.data.get(spriteSkillId, {}).get('learnSkillHigh', gametypes.SPRITE_LEARN_SKILL_LOW)
        typeIndex = 0 if learnSkillHigh < gametypes.SPRITE_LEARN_SKILL_ULTIMATE else 1
        spriteInfo = self.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        consumeSpecialItemId = SYSCD.data.get('spriteSkillReplaceConsumeSpecialItemId', {}).get(spriteId, 0)
        spriteSkillReplaceConsumeCommonItem = SYSCD.data.get('spriteSkillReplaceConsumeCommonItem', ())
        shopItemId, itemNum = spriteSkillReplaceConsumeCommonItem[typeIndex]
        shopItemNum = p.inv.countItemInPages(uiUtils.getParentId(shopItemId), enableParentCheck=True)
        specialNum = p.inv.countItemInPages(uiUtils.getParentId(consumeSpecialItemId), enableParentCheck=True)
        sumNum = specialNum + shopItemNum
        if specialNum:
            itemInfo = uiUtils.getGfxItemById(consumeSpecialItemId)
        else:
            itemInfo = uiUtils.getGfxItemById(shopItemId)
        if sumNum < itemNum:
            color = '#FF0000'
            self.besetSkillPanel.slot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
        else:
            color = '#FFFFE6'
            self.besetSkillPanel.slot.setSlotState(uiConst.ITEM_NORMAL)
        self.besetSkillPanel.slot.fitSize = True
        self.besetSkillPanel.slot.dragable = False
        self.besetSkillPanel.slot.setItemSlotData(itemInfo)
        strNum = uiUtils.toHtml(sumNum, color)
        count = str('%s/%s' % (strNum, itemNum))
        self.besetSkillPanel.slot.validateNow()
        self.besetSkillPanel.slot.setValueAmountTxt(count)
        self.besetSkillPanel.besetBtn.enabled = False if sumNum < itemNum else True

    def handleSureBesetBtnClick(self, *args):
        oldSkillId = 0
        slotPart = 0
        if self.selectedSkillSlot:
            oldSkillId = self.selectedSkillSlot.skillId
            slotPart = self.selectedSkillSlot.slotIdx
        if not oldSkillId:
            return
        if not self.curBesetSelectSkillId:
            return
        p = BigWorld.player()
        spriteInfo = self.getCurSelectSpriteInfo()
        selectedIndex = spriteInfo.get('index', -99)
        page, pos = p.inv.findItemInPages(self.curBesetSelectSkillId)
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            return
        teachSpriteSkill = CID.data.get(self.curBesetSelectSkillId, {}).get('teachSpriteSkill', 0)
        newSkillId = SSSD.data.get(teachSpriteSkill, {}).get('virtualSkill', 0)
        newRefName = self.getSkillName(newSkillId)
        oldRefName = self.getSkillName(oldSkillId)
        msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_TO_BESET_SKILL, '%s-%s') % (oldRefName, newRefName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realBesetSkill, selectedIndex, slotPart, self.curBesetSelectSkillId, page, pos))

    @ui.checkInventoryLock()
    def realBesetSkill(self, selectedIndex, slotPart, itemId, page, pos):
        p = BigWorld.player()
        p.base.useSpriteTextBookReplaceOldSkill(selectedIndex, slotPart, itemId, page, pos, p.cipherOfPerson)

    def handleThinkBesetBtnClick(self, *args):
        widget = self.getWidget()
        if not widget:
            return
        self.showSkillMcType = SHOW_SKILL_MC_TYPE0
        self.updateSkillMcVisible()

    def besetSkillFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.setSkillBookData(itemData, itemMc)
        itemMc.selected = False
        if self.curBesetSelectSkillId and self.curBesetSelectSkillId == itemData.itemId:
            itemMc.selected = True
        elif not self.curBesetSelectSkillId and itemData.numberId == 0:
            itemMc.selected = True
        itemMc.disabled = itemData.isLearned
        if itemMc.selected:
            self.curBesetSelectSkillId = itemData.itemId
            self.curBesetSelectSkillItem = itemMc
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleBesetSkillSlotClick, False, 0, True)

    def handleBesetSkillSlotClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if self.curBesetSelectSkillItem:
            self.curBesetSelectSkillItem.selected = False
        target.selected = True
        self.curBesetSelectSkillId = target.itemId
        self.curBesetSelectSkillItem = target

    def updateBesetSkillBookPanel(self):
        widget = self.getWidget()
        if not widget:
            return
        elif not self.selectedSkillSlot or self.selectedSkillSlot and not self.selectedSkillSlot.selectedMC.visible:
            self.showSkillMcType = SHOW_SKILL_MC_TYPE0
            self.updateSkillMcVisible()
            return
        else:
            if self.besetSkillPanel and self.besetSkillPanel.stage:
                besetBookInfo = self.getBesetSkillBookInfo()
                if not self.checkInBesetSkillBook(besetBookInfo):
                    self.curBesetSelectSkillId = None
                self.besetSkillPanel.besetSkillList.dataArray = besetBookInfo
                if not self.curBesetSelectSkillId:
                    self.besetSkillPanel.besetSkillList.validateNow()
                    self.besetSkillPanel.besetSkillList.scrollToHead()
                self.updateConsumeBesetItem()
            return

    def checkInBesetSkillBook(self, besetBookInfo):
        for items in besetBookInfo:
            if self.curBesetSelectSkillId and self.curBesetSelectSkillId == items.get('itemId', 0):
                return True

        return False

    def handleSkillTransferBtnClick(self, *args):
        gameglobal.rds.ui.summonedWarSpriteSkillTransfer.show(self.parentProxy.currSelectItemSpriteIndex)

    def updateReplaceSkillBookPanel(self):
        widget = self.getWidget()
        if not widget:
            return
        else:
            if self.replaceSkillPanel and self.replaceSkillPanel.stage:
                replaceBookInfo = self.getReplaceSkillBookInfo()
                if not self.checkInReplaceSkillBook(replaceBookInfo):
                    self.curReplaceSelectSkillId = None
                self.replaceSkillPanel.learnSkillList.dataArray = replaceBookInfo
                if not self.curReplaceSelectSkillId:
                    self.replaceSkillPanel.learnSkillList.validateNow()
                    self.replaceSkillPanel.learnSkillList.scrollToHead()
            return

    def checkInReplaceSkillBook(self, replaceBookInfo):
        for items in replaceBookInfo:
            if self.curReplaceSelectSkillId and self.curReplaceSelectSkillId == items.get('itemId', 0):
                return True

        return False

    def showReplaceSkillBookMc(self, replaceBookInfo):
        widget = self.getWidget()
        if not widget:
            return
        skillMc = widget.mineWarSpritePanel.skillMc
        replaceSkillMc = skillMc.replaceSkillMc
        if replaceSkillMc.visible:
            return
        self.updateSkillMcVisible()
        self.replaceSkillPanel = replaceSkillMc
        self.replaceSkillPanel.getSkillWayHelp.helpKey = SYSCD.data.get('getSkillWayHelp', 0)
        self.replaceSkillPanel.learnSkillList.itemHeight = LEARN_SKILL_ITEM_HEIGHT
        self.replaceSkillPanel.learnSkillList.itemRenderer = 'SummonedWarSpriteMine_skillLearnItem'
        self.replaceSkillPanel.learnSkillList.dataArray = replaceBookInfo
        self.replaceSkillPanel.learnSkillList.lableFunction = self.replaceSkillFunction
        self.replaceSkillPanel.learnSkillList.validateNow()
        self.replaceSkillPanel.learnSkillList.scrollToHead()
        self.replaceSkillPanel.sureReplaceBtn.addEventListener(events.MOUSE_CLICK, self.handleSureReplaceBtnClick, False, 0, True)
        self.replaceSkillPanel.thinkBtn.addEventListener(events.MOUSE_CLICK, self.handleThinkBtnClick, False, 0, True)

    def handleSureReplaceBtnClick(self, *args):
        oldSkillId = 0
        slotPart = 0
        if self.selectedSkillSlot:
            oldSkillId = self.selectedSkillSlot.skillId
            slotPart = self.selectedSkillSlot.slotIdx
        if not oldSkillId:
            return
        if not self.curReplaceSelectSkillId:
            return
        p = BigWorld.player()
        spriteInfo = self.getCurSelectSpriteInfo()
        selectedIndex = spriteInfo.get('index', -99)
        page, pos = p.inv.findItemInPages(self.curReplaceSelectSkillId)
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            p.showGameMsg(GMDD.data.SPRITE_LEARN_SKILL_NO_ITEM, ())
            return
        teachSpriteSkill = CID.data.get(self.curReplaceSelectSkillId, {}).get('teachSpriteSkill', 0)
        newSkillId = SSSD.data.get(teachSpriteSkill, {}).get('virtualSkill', 0)
        newRefName = self.getSkillName(newSkillId)
        oldRefName = self.getSkillName(oldSkillId)
        msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_TO_REPLACE_SKILL, '%s%s') % (oldRefName, newRefName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.realReplaceSkill, selectedIndex, slotPart, self.curReplaceSelectSkillId, page, pos))

    @ui.checkInventoryLock()
    def realReplaceSkill(self, selectedIndex, slotPart, itemId, page, pos):
        p = BigWorld.player()
        p.base.useSpriteTextBookReplaceSkill(selectedIndex, slotPart, itemId, page, pos, p.cipherOfPerson)

    def handleThinkBtnClick(self, *args):
        widget = self.getWidget()
        if not widget:
            return
        self.showSkillMcType = SHOW_SKILL_MC_TYPE0
        self.updateSkillMcVisible()

    def handleReplcaeSkillSlotClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if self.curReplaceSelectSkillItem:
            self.curReplaceSelectSkillItem.selected = False
        target.selected = True
        self.curReplaceSelectSkillId = target.itemId
        self.curReplaceSelectSkillItem = target

    def replaceSkillFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.setSkillBookData(itemData, itemMc)
        itemMc.selected = False
        if self.curReplaceSelectSkillId and self.curReplaceSelectSkillId == itemData.itemId:
            itemMc.selected = True
        elif not self.curReplaceSelectSkillId and itemData.numberId == 0:
            itemMc.selected = True
        if itemMc.selected:
            self.curReplaceSelectSkillId = itemData.itemId
            self.curReplaceSelectSkillItem = itemMc
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleReplcaeSkillSlotClick, False, 0, True)

    def setSkillBookData(self, itemData, itemMc):
        itemMc.numberId = itemData.numberId
        itemMc.itemId = itemData.itemId
        itemMc.isLearned = itemData.isLearned
        itemMc.validateNow()
        itemMc.mouseChildren = True
        teachSpriteSkill = CID.data.get(itemData.itemId, {}).get('teachSpriteSkill', 0)
        skillId = SSSD.data.get(teachSpriteSkill, {}).get('virtualSkill', 0)
        itemMc.teachSpriteSkill = teachSpriteSkill
        slot = itemMc.itemSlot.slot
        skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=SPRITE_SKILL_LEVEL)
        iconPath = uiUtils.getSkillIconPath(skillInfo, uiConst.ICON_SIZE64)
        slot.fitSize = True
        slot.dragable = False
        slotData = uiUtils.getGfxItemById(itemData.itemId, itemData.itemNum)
        slotData['iconPath'] = iconPath
        slotData['overIconPath'] = iconPath
        slot.setItemSlotData(slotData)
        skillDesc = ID.data.get(itemData.itemId, {}).get('spriteSkillDesc', '')
        sName = skillInfo.getSkillData('sname', '')
        itemMc.labels = [sName, skillDesc]

    def updateSkillMcVisible(self):
        widget = self.getWidget()
        if not widget:
            return
        widget.mineWarSpritePanel.skillMc.showSelectSkillMc.visible = self.showSkillMcType == SHOW_SKILL_MC_TYPE0
        widget.mineWarSpritePanel.skillMc.learnSkillMc.visible = self.showSkillMcType == SHOW_SKILL_MC_TYPE1
        widget.mineWarSpritePanel.skillMc.replaceSkillMc.visible = self.showSkillMcType == SHOW_SKILL_MC_TYPE2
        widget.mineWarSpritePanel.skillMc.besetSkillMc.visible = self.showSkillMcType == SHOW_SKILL_MC_TYPE3
        self.setTemplateState()

    def handleLearnSkill(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.SPRITE_LEARNED_BOOK_FROM_RIGHT, ())
        if self.showSkillMcType == SHOW_SKILL_MC_TYPE1:
            return
        self.showSkillMcType = SHOW_SKILL_MC_TYPE1
        skillBookInfo = self.getLearnSkillBookInfo()
        self.showLearnSkillBookMC(e.target, skillBookInfo)

    def getSkillSlotStateNum(self, slotState):
        spriteInfo = self.getCurSelectSpriteInfo()
        learnedSkillInfos = self.getLearnedSkillInfo(spriteInfo)
        slotNum = 0
        for i in xrange(SKILL_SLOT_NUM):
            info = learnedSkillInfos.get(i, None)
            if info:
                if info.get('slot', -1) == slotState:
                    slotNum = slotNum + 1

        return slotNum

    def getNeedUnlockSkillSlot(self, spriteInfo):
        learnedSkillInfos = self.getLearnedSkillInfo(spriteInfo)
        for i in xrange(SKILL_SLOT_NUM):
            info = learnedSkillInfos.get(i, None)
            if info:
                if info.get('slot', -1) == const.SSPRITE_SKILL_SLOT_FORBIDDEN:
                    return info.get('part')

        return -1

    def handleUnlockSlotClick(self, *args):
        self.openSummonedWarSpriteMsg()

    def openSummonedWarSpriteMsg(self):
        spriteInfo = self.getCurSelectSpriteInfo()
        selectedIndex = spriteInfo.get('index', -99)
        needUnlockSkillSlot = self.getNeedUnlockSkillSlot(spriteInfo)
        gameglobal.rds.ui.summonedWarSpriteMsg.show(selectedIndex, needUnlockSkillSlot)

    def handleForgetSkill(self, *args):
        spriteInfo = self.getCurSelectSpriteInfo()
        selectedIndex = spriteInfo.get('index', -99)
        if self.selectedSkillSlot == None:
            BigWorld.player().showGameMsg(GMDD.data.SPRITE_SKILL_NOT_SELECTED, ())
            return
        else:
            skillName = self.selectedSkillSlot.skillName
            slotIdx = self.selectedSkillSlot.slotIdx
            gameglobal.rds.ui.summonedWarSpriteForgetSkill.show(selectedIndex, slotIdx, skillName)
            return

    def reset(self):
        self.learnSkillPanel = None
        self.selectedSkillSlot = None
        self.currSelectLearnSkillItem = None
        self.currSelectLearnSkillId = None
        self.showSkillMcType = SHOW_SKILL_MC_TYPE0
        self.disableLearnSkills = None
        self.replaceSkillPanel = None
        self.curReplaceSelectSkillId = None
        self.curReplaceSelectSkillItem = None
        self.allLearnedSkills = []
        self.besetSkillPanel = None
        self.curBesetSelectSkillId = None
        self.curBesetSelectSkillItem = None

    def palyLearnedSkillSfx(self, slot):
        widget = self.getWidget()
        if not widget:
            return
        else:
            skillMc = widget.mineWarSpritePanel.skillMc
            slotMC = getattr(skillMc, 'skillSlot' + str(slot), None)
            if slotMC:
                slotMC.learnSkillSucSfx.visible = True
                slotMC.learnSkillSucSfx.gotoAndPlay(1)
            return

    def getSkillName(self, skillId):
        skillInfo = skillDataInfo.ClientSkillInfo(skillId, lv=SPRITE_SKILL_LEVEL)
        skillName = skillInfo.getSkillData('sname', '')
        return skillName

    def showLearnedSkillMsg(self, index, newRefID, oldRefID):
        p = BigWorld.player()
        spriteName = p.summonSpriteList.get(index, {}).get('name', '')
        newSkillId = SSSD.data.get(newRefID, {}).get('virtualSkill', 0)
        oldSkillId = SSSD.data.get(oldRefID, {}).get('virtualSkill', 0)
        if newRefID and oldRefID:
            newRefName = self.getSkillName(newSkillId)
            oldRefName = self.getSkillName(oldSkillId)
            p.showGameMsg(GMDD.data.SPRITE_LEARNED_REPLACE_SKILL, (spriteName, newRefName, oldRefName))
            self.showSkillEffectMsg()
        elif newRefID and not oldRefID:
            newRefName = self.getSkillName(newSkillId)
            p.showGameMsg(GMDD.data.SPRITE_LEARNED_SKILL, (spriteName, newRefName))
            self.showSkillEffectMsg()

    @ui.callAfterTime(0.5)
    def showSkillEffectMsg(self):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.SPRITE_SKILL_EFFECT_OUT_COMBAT, ())

    def setSkillSelected(self, spriteSkillId):
        widget = self.getWidget()
        if not widget:
            return
        else:
            skillMc = widget.mineWarSpritePanel.skillMc
            spriteInfo = self.getCurSelectSpriteInfo()
            learnedSkillInfos = self.getLearnedSkillInfo(spriteInfo)
            for i in xrange(SKILL_SLOT_NUM):
                info = learnedSkillInfos.get(i, None)
                if info:
                    slotMC = getattr(skillMc, 'skillSlot' + str(i), None)
                    if slotMC.skillId == spriteSkillId:
                        self.setSlotSelected(slotMC)

            return

    def usedSkillReplaceSucc(self, slot, newRefID, oldRefID):
        widget = self.getWidget()
        if not widget:
            return
        self.showSkillMcType = SHOW_SKILL_MC_TYPE0
        self.updateSkillMcVisible()
        self.palyLearnedSkillSfx(slot)
        p = BigWorld.player()
        newSkillId = SSSD.data.get(newRefID, {}).get('virtualSkill', 0)
        oldSkillId = SSSD.data.get(oldRefID, {}).get('virtualSkill', 0)
        if newRefID and oldRefID:
            newRefName = self.getSkillName(newSkillId)
            oldRefName = self.getSkillName(oldSkillId)
            p.showGameMsg(GMDD.data.SPRITE_REPLACE_SKILL_SUCCESS, (oldRefName, newRefName))
            self.showSkillEffectMsg()

    def usedSkillBesetSucc(self, index, slot, newRefID, oldRefID):
        widget = self.getWidget()
        if not widget:
            return
        p = BigWorld.player()
        newSkillId = SSSD.data.get(newRefID, {}).get('virtualSkill', 0)
        oldSkillId = SSSD.data.get(oldRefID, {}).get('virtualSkill', 0)
        if newRefID and oldRefID:
            newRefName = self.getSkillName(newSkillId)
            oldRefName = self.getSkillName(oldSkillId)
            p.showGameMsg(GMDD.data.SPRITE_BESET_SKILL_SUCCESS, (oldRefName, newRefName))
        if self.parentProxy.currSelectItemSpriteIndex != index:
            return
        self.showSkillMcType = SHOW_SKILL_MC_TYPE0
        self.updateSkillMcVisible()
        self.palyLearnedSkillSfx(slot)
