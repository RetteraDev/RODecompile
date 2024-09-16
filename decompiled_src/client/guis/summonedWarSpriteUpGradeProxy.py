#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteUpGradeProxy.o
import BigWorld
import uiConst
import events
import ui
import uiUtils
import gameglobal
from uiProxy import UIProxy
from gameStrings import gameStrings
from helpers import capturePhoto
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import summon_sprite_skin_data as SSSKIND
from data import item_data as ID
from data import sprite_upgrade_data as SUD
from cdata import game_msg_def_data as GMDD
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'
MAX_JINGJIE_NUM = 5

class SummonedWarSpriteUpGradeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteUpGradeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = 0
        self.curSelectedGrade = 0
        self.curSelectedMC = None
        self.headGen = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_SPRITE_UP_GRADE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_UP_GRADE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_UP_GRADE)
        self.endCapture()

    def reset(self):
        self.spriteIndex = 0
        self.curSelectedGrade = 0
        self.curSelectedMC = None
        self.headGen = None

    def show(self, spriteIndex):
        if not gameglobal.rds.configData.get('enableSpriteUpgrade', False):
            return
        self.spriteIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_UP_GRADE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        for i in xrange(MAX_JINGJIE_NUM):
            itemMc = getattr(self.widget, 'gradeMc%d' % i, None)
            if not itemMc:
                continue
            itemMc.icon.grade = i
            itemMc.icon.gotoAndStop('disabled')
            itemMc.icon.selectedMc.visible = False
            itemMc.shine.effect.visible = False
            ASUtils.setHitTestDisable(itemMc.shine, True)
            itemMc.icon.addEventListener(events.MOUSE_CLICK, self.handleGradeClick, False, 0, True)
            itemMc.icon.addEventListener(events.MOUSE_ROLL_OVER, self.handleGradeRollOver, False, 0, True)
            itemMc.icon.addEventListener(events.MOUSE_ROLL_OUT, self.handleGradeRollOut, False, 0, True)

        self.initHeadGen()

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
            spriteId = spriteInfo.get('spriteId', 0)
            curGrade = spriteInfo.get('upgradeStage', 0)
            subData = SUD.data.get((spriteId, curGrade), {})
            self.widget.currGradeName.text = subData.get('upGradeNmae', '')
            for i in xrange(MAX_JINGJIE_NUM):
                itemMc = getattr(self.widget, 'gradeMc%d' % i, None)
                if not itemMc:
                    continue
                subData = SUD.data.get((spriteId, i), {})
                itemMc.icon.gotoAndStop('up' if i <= curGrade else 'disabled')
                itemMc.icon.gradeName.text = subData.get('upGradeNmae', '')
                itemMc.shine.effect.visible = i == curGrade

            if self.curSelectedMC:
                self.refreshDetailInfo()
            else:
                self.updateGradeMc(curGrade)
            return

    @ui.checkInventoryLock()
    def _onSureBtnClick(self, e):
        p = BigWorld.player()
        p.base.upgradeSprite(self.spriteIndex, p.cipherOfPerson)

    def handleGradeClick(self, *args):
        e = ASObject(args[3][0])
        self.updateGradeMc(e.currentTarget.grade)

    def handleGradeRollOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.selectedMc.visible = True

    def handleGradeRollOut(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.grade != self.curSelectedGrade:
            itemMc.selectedMc.visible = False

    def updateGradeMc(self, grade):
        itemMc = getattr(self.widget, 'gradeMc%d' % grade, None)
        if not itemMc:
            return
        else:
            if self.curSelectedMC:
                self.curSelectedMC.selectedMc.visible = False
            self.curSelectedMC = itemMc.icon
            self.curSelectedMC.selectedMc.visible = True
            self.curSelectedGrade = grade
            self.refreshDetailInfo()
            return

    def refreshDetailInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        curGrade = spriteInfo.get('upgradeStage', 0)
        subData = SUD.data.get((spriteId, self.curSelectedGrade), {})
        self.updateUpGradeCondition(spriteInfo, subData, curGrade)
        self.updateGetReward(subData)
        self.takePhoto3D()

    def updateUpGradeCondition(self, spriteInfo, subData, curGrade):
        TipManager.removeTip(self.widget.sureBtn)
        if self.curSelectedGrade == 0:
            self.widget.condition0.visible = False
            self.widget.condition1.visible = False
            self.widget.itemSlot.visible = False
            self.widget.finishCondition.visible = True
            self.widget.finishCondition.finishDesc.text = subData.get('afterUpGradeDesc', '')
            self.widget.sureBtn.label = gameStrings.SPRITE_UP_GRADE_BTN_LABEL1
            self.widget.sureBtn.disabled = True
            return
        isFinishUp = self.curSelectedGrade <= curGrade
        self.widget.condition0.visible = True
        self.widget.condition1.visible = True
        self.widget.itemSlot.visible = True
        self.widget.finishCondition.visible = False
        p = BigWorld.player()
        props = spriteInfo.get('props', {})
        conditionFami = subData.get('familiar', 0)
        familiar = int(props.get('familiar', 0))
        self.widget.condition0.conditionDesc.htmlText = gameStrings.SPRITE_UP_GRADE_CONDITION0 % conditionFami
        if isFinishUp:
            self.widget.condition0.conditionVal.visible = False
            self.widget.condition0.tickIcon.visible = True
            self.widget.condition0.forkIcon.visible = False
        else:
            self.widget.condition0.conditionVal.visible = conditionFami > familiar
            self.widget.condition0.conditionVal.text = gameStrings.SPRITE_UP_GRADE_CURRENT_FMAI_LV % familiar
            self.widget.condition0.tickIcon.visible = not conditionFami > familiar
            self.widget.condition0.forkIcon.visible = conditionFami > familiar
        itemId, needNum = subData.get('item', (0, 0))
        itemName = ID.data.get(itemId, {}).get('name', '')
        myItemNum = p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
        self.widget.condition1.conditionDesc.htmlText = gameStrings.SPRITE_UP_GRADE_CONDITION1 % (needNum, itemName)
        if isFinishUp:
            self.widget.condition1.conditionVal.visible = False
            self.widget.condition1.tickIcon.visible = True
            self.widget.condition1.forkIcon.visible = False
        else:
            self.widget.condition1.conditionVal.visible = needNum > myItemNum
            self.widget.condition1.conditionVal.text = gameStrings.SPRITE_UP_GRADE_CURRENT_ITEM_LESS
            self.widget.condition1.tickIcon.visible = not needNum > myItemNum
            self.widget.condition1.forkIcon.visible = needNum > myItemNum
        if needNum > myItemNum:
            strNum = uiUtils.toHtml(myItemNum, '#FF0000')
            self.widget.itemSlot.slot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
        else:
            strNum = uiUtils.toHtml(myItemNum, '#FFFFE6')
            self.widget.itemSlot.slot.setSlotState(uiConst.ITEM_NORMAL)
        if isFinishUp:
            self.widget.itemSlot.visible = False
            self.widget.sureBtn.disabled = True
            self.widget.sureBtn.label = gameStrings.SPRITE_UP_GRADE_BTN_LABEL1
        else:
            self.widget.itemSlot.visible = True
            count = str('%s/%d' % (strNum, needNum))
            itemInfo = uiUtils.getGfxItemById(itemId, count)
            self.widget.itemSlot.slot.dragable = False
            self.widget.itemSlot.slot.setItemSlotData(itemInfo)
            self.widget.sureBtn.label = gameStrings.SPRITE_UP_GRADE_BTN_LABEL0
            if conditionFami > familiar or needNum > myItemNum or self.curSelectedGrade > curGrade + 1:
                self.widget.sureBtn.disabled = True
                spriteId = spriteInfo.get('spriteId', 0)
                subData = SUD.data.get((spriteId, min(curGrade + 1, MAX_JINGJIE_NUM)), {})
                nextStageName = subData.get('upGradeNmae', '')
                tipMsg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_UP_GRADE_BTN_DISABLED_TIP, '%s') % nextStageName
                TipManager.addTip(self.widget.sureBtn, tipMsg)
            else:
                self.widget.sureBtn.disabled = False

    def updateGetReward(self, subData):
        posY = 0
        self.widget.removeAllInst(self.widget.rewardMc)
        unlockRewardDescList = subData.get('unlockRewardDescList', [])
        for i in xrange(len(unlockRewardDescList)):
            itemMc = self.widget.getInstByClsName('SummonedWarSpriteUpGrade_rewardItem')
            itemMc.y = posY
            itemMc.rewardDesc.htmlText = unlockRewardDescList[i]
            self.widget.rewardMc.addChild(itemMc)
            posY += itemMc.height + 5

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.SummonedWarSpriteUpGradePhotoGen('gui/taskmask.tga', 314, 'SummonedWarSpriteUpGrade_unitItem')
        self.headGen.initFlashMesh()

    def takePhoto3D(self):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        sudData = SUD.data.get((spriteId, self.curSelectedGrade), {})
        skinId = sudData.get('stageSkinId', 0)
        skinData = SSSKIND.data.get((spriteId, skinId), {})
        spriteModel = skinData.get('transformModelIdBefore', 0)
        materials = skinData.get('materialsBefore', 'Default')
        if self.headGen:
            self.headGen.startCapture(spriteModel, materials, None)

    def endCapture(self):
        if self.headGen:
            self.headGen.endCapture()
