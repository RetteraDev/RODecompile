#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteFamiliarProxy.o
import BigWorld
import const
import uiConst
import events
import utils
import tipUtils
import ui
import uiUtils
import gameglobal
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from data import summon_sprite_info_data as SSID
from data import summon_sprite_familiar_data as SSFD
from cdata import game_msg_def_data as GMDD

class SummonedWarSpriteFamiliarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteFamiliarProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = None
        self.turnInSpriteIdx = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_SPRITE_FAMILIAR, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_SPRITE_FAMILIAR:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_SPRITE_FAMILIAR)

    def reset(self):
        self.spriteIndex = None
        self.turnInSpriteIdx = None

    def show(self, spriteIndex):
        self.spriteIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_SPRITE_FAMILIAR)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.help.helpKey = SCD.data.get('spriteFamiliarHelpKey', 0)
        self.widget.descMc.desc.text = SCD.data.get('spriteFamiliarDesc', '')
        self.widget.spriteList.itemHeight = 65
        self.widget.spriteList.itemRenderer = 'SummonedWarSpriteFamiliar_spriteHeadItem'
        self.widget.spriteList.barAlwaysVisible = True
        self.widget.spriteList.dataArray = []
        self.widget.spriteList.lableFunction = self.itemFunction
        self.widget.descMc.visible = True
        self.widget.previewMc.visible = False
        self.widget.turnToBtn.disabled = True

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        dataList = self.filterSprite()
        self.widget.noSpriteDesc.visible = not dataList
        self.widget.spriteList.dataArray = dataList
        self.widget.jiFenVT1.text = format(self.ownYunChuiFame, ',')
        self.updateTurnOutSprite()
        self.updateTurnInSprite()

    @ui.checkInventoryLock()
    def realCover(self):
        p = BigWorld.player()
        p.base.applyFamiCover(self.turnInSpriteIdx, self.spriteIndex, p.cipherOfPerson)
        self.hide()

    def _onTurnToBtnClick(self, e):
        if not self.spriteIndex or not self.turnInSpriteIdx:
            return
        totalFamiExpIn = utils.getSpriteTotalFamiExp(self.turnInSpriteIdx)
        if totalFamiExpIn <= 0:
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_FAMILIAR_SURE_TRUN_TO, '')
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_FAMILIAR_SURE_TRUN_AND_COVER, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.realCover)

    def _onCancelBtnClick(self, e):
        self.hide()

    def handleSelSpriteDown(self, *args):
        target = ASObject(args[3][0]).currentTarget
        if target.selected:
            return
        target.selected = True
        self.turnInSpriteIdx = target.spriteIndex
        self.updateTurnInSprite()
        totalFamiExpOut = utils.getSpriteTotalFamiExp(self.spriteIndex)
        totalFamiExpIn = utils.getSpriteTotalFamiExp(self.turnInSpriteIdx)
        yunchuiCost = utils.getSpriteCoverCost(totalFamiExpOut)
        TipManager.removeTip(self.widget.turnToBtn)
        self.widget.descMc.visible = False
        self.widget.previewMc.visible = True
        familiar, _, _ = utils.getSpriteFamiByIdx(self.spriteIndex)
        if gameglobal.rds.configData.get('enableSpriteFamiV2', False):
            canFamiliarTransfer = familiar < SCD.data.get('spriteFamiTransferLvLimit', 30)
        else:
            getTurnFamiOut = utils.getSpriteFamiTransfer(totalFamiExpOut)
            canFamiliarTransfer = getTurnFamiOut <= totalFamiExpIn
        if canFamiliarTransfer:
            self.widget.turnToBtn.disabled = True
            self.widget.previewMc.visible = False
            self.widget.descMc.visible = True
            self.widget.descMc.desc.text = SCD.data.get('noneSpriteFamiliarDesc', '')
        elif self.ownYunChuiFame < yunchuiCost:
            self.widget.turnToBtn.disabled = True
            self.updatePreviewMc()
            TipManager.addTip(self.widget.turnToBtn, gameStrings.SPRITE_FAMI_YUN_CHUI_JI_FEN_LESS)
        else:
            self.widget.turnToBtn.disabled = False
            self.updatePreviewMc()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.spriteIndex = itemData.spriteIndex
        itemMc.spriteId = itemData.spriteId
        itemMc.groupName = 'empty'
        itemMc.groupName = 'summonedWarSpriteFamiliar%s'
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleSelSpriteDown, False, 0, True)
        spriteName = itemData.name
        famiEffLv = itemData.famiEffLv
        if itemData.famiEffAdd:
            desc = str(itemData.familiar) + '<font color=\"#559423\">' + '+' + str(itemData.famiEffAdd) + '</font>'
        else:
            desc = famiEffLv
        itemMc.labels = [spriteName, desc]
        iconPath = uiUtils.getSummonSpriteIconPath(itemData.spriteId)
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': iconPath})
        itemMc.itemSlot.slot.dragable = False
        itemMc.selected = self.turnInSpriteIdx == itemData.spriteIndex
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.itemSlot.slot.validateNow()
        TipManager.addTipByType(itemMc.itemSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (itemData.spriteIndex,), False, 'upLeft')
        gameglobal.rds.ui.summonedWarSpriteMine.addFamiliarIconTip(itemMc.famiIcon, itemData.familiar, itemData.famiEffAdd, famiEffLv)

    def filterSprite(self):
        p = BigWorld.player()
        spriteList = []
        for spriteInfo in p.summonSpriteList.values():
            if spriteInfo['index'] == self.spriteIndex:
                continue
            if utils.getSpriteBattleState(spriteInfo['index']):
                continue
            if utils.getSpriteAccessoryState(spriteInfo['index']):
                continue
            props = spriteInfo.get('props', {})
            itemInfo = {}
            itemInfo['spriteIndex'] = spriteInfo.get('index', -1)
            itemInfo['spriteId'] = spriteInfo.get('spriteId', 0)
            itemInfo['name'] = spriteInfo.get('name', '')
            itemInfo['famiEffLv'] = props.get('famiEffLv', 0)
            itemInfo['familiar'] = props.get('familiar', 0)
            itemInfo['famiEffAdd'] = props.get('famiEffAdd', 0)
            spriteList.append(itemInfo)

        return sorted(spriteList, key=lambda d: d['famiEffLv'])

    def updateTurnOutSprite(self):
        self.updateSpriteItem(self.widget.turnOutSpriteItem, self.spriteIndex)
        totalFamiExpOut = utils.getSpriteTotalFamiExp(self.spriteIndex)
        yunchuiCost = utils.getSpriteCoverCost(totalFamiExpOut)
        self.widget.jiFenVT0.htmlText = uiUtils.convertNumStr(self.ownYunChuiFame, yunchuiCost, False, enoughColor=None)

    def updateTurnInSprite(self):
        if not self.turnInSpriteIdx:
            self.widget.desc0.visible = True
            self.widget.trunInSpriteItem.visible = False
        else:
            self.widget.desc0.visible = False
            self.widget.trunInSpriteItem.visible = True
            self.updateSpriteItem(self.widget.trunInSpriteItem, self.turnInSpriteIdx)

    def updateSpriteItem(self, itemMc, index):
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList[index]
        spriteId = spriteInfo.get('spriteId', 0)
        itemMc.itemSlot.slot.setItemSlotData({'iconPath': uiUtils.getSummonSpriteIconPath(spriteId)})
        itemMc.itemSlot.slot.dragable = False
        spriteName = spriteInfo.get('name', '')
        familiar, famiEffAdd, famiEffLv = utils.getSpriteFamiByIdx(index)
        if famiEffAdd:
            desc = str(familiar) + '<font color=\"#559423\">' + '+' + str(famiEffAdd) + '</font>'
        else:
            desc = famiEffLv
        itemMc.labels = [spriteName, desc]
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.itemSlot.slot.validateNow()
        TipManager.addTipByType(itemMc.itemSlot.slot, tipUtils.TYPE_SPRITE_HEAD_TIP, (index,), False, 'upLeft')
        gameglobal.rds.ui.summonedWarSpriteMine.addFamiliarIconTip(itemMc.famiIcon, familiar, famiEffAdd, famiEffLv)

    def updatePreviewMc(self):
        p = BigWorld.player()
        turnOutSpirteInfo = p.summonSpriteList[self.spriteIndex]
        turnInSpriteInfo = p.summonSpriteList[self.turnInSpriteIdx]
        self.updateTransferNumsUI()
        self.updateTransferSpriteUI(self.spriteIndex, 'Out')
        self.updateSpriteHeadIcon(turnOutSpirteInfo, 'Out')
        self.updateTransferSpriteUI(self.turnInSpriteIdx, 'In')
        self.updateSpriteHeadIcon(turnInSpriteInfo, 'In')

    def updateTransferNumsUI(self):
        turnFamiOutStr, getTurnFamiOut = utils.getSpriteFamiTransferPercentStr(self.spriteIndex)
        self.widget.previewMc.turnNumT.text = getTurnFamiOut
        self.widget.previewMc.turnPerT.text = turnFamiOutStr

    def updateTransferSpriteUI(self, curSpriteIdx, typeStr):
        turnFami0 = self.widget.previewMc.getChildByName('turn%sFami0' % typeStr)
        turnFami1 = self.widget.previewMc.getChildByName('turn%sFami1' % typeStr)
        famiIcon0 = self.widget.previewMc.getChildByName('turn%sFamiIcon0' % typeStr)
        famiIcon1 = self.widget.previewMc.getChildByName('turn%sFamiIcon1' % typeStr)
        familiar, famiEffAdd, famiEffLv = utils.getSpriteFamiByIdx(curSpriteIdx)
        if typeStr == 'Out':
            if famiEffAdd:
                turnFami0.htmlText = str(familiar) + '<font color=\"#559423\">' + '+' + str(famiEffAdd) + '</font>'
                turnFami1.htmlText = str(1) + '<font color=\"#559423\">' + '+' + str(famiEffAdd) + '</font>'
            else:
                turnFami0.text = famiEffLv
                turnFami1.text = '%d' % (1 + famiEffAdd)
            gameglobal.rds.ui.summonedWarSpriteMine.addFamiliarIconTip(famiIcon1, 1, famiEffAdd, 1 + famiEffAdd)
        elif typeStr == 'In':
            totalFamiExpOut = utils.getSpriteTotalFamiExp(self.spriteIndex)
            totalFamiExpIn = utils.getSpriteTotalFamiExp(self.turnInSpriteIdx)
            if gameglobal.rds.configData.get('enableSpriteFamiV2', False):
                getTurnFamiOut = utils.getSpriteFamiTransferV2(totalFamiExpOut)
                familiarInLv = utils.getSpriteTotalFamiExpToLv(getTurnFamiOut + totalFamiExpIn)
            else:
                getTurnFamiOut = utils.getSpriteFamiTransfer(totalFamiExpOut)
                familiarInLv = utils.getSpriteTotalFamiExpToLv(getTurnFamiOut)
            if famiEffAdd:
                turnFami0.htmlText = str(familiar) + '<font color=\"#559423\">' + '+' + str(famiEffAdd) + '</font>'
                turnFami1.htmlText = str(familiarInLv) + '<font color=\"#559423\">' + '+' + str(famiEffAdd) + '</font>'
            else:
                turnFami0.text = famiEffLv
                turnFami1.text = familiarInLv + famiEffAdd
            gameglobal.rds.ui.summonedWarSpriteMine.addFamiliarIconTip(famiIcon1, familiarInLv, famiEffAdd, familiarInLv + famiEffAdd)
        gameglobal.rds.ui.summonedWarSpriteMine.addFamiliarIconTip(famiIcon0, familiar, famiEffAdd, famiEffLv)
        famiIcon0.x = turnFami0.x + (turnFami0.width - turnFami0.textWidth) - famiIcon0.width - 5
        ASUtils.setHitTestDisable(turnFami0, True)

    def updateSpriteHeadIcon(self, spriteInfo, typeStr):
        turnSlot = self.widget.previewMc.getChildByName('turn%sSlot' % typeStr)
        turnName = self.widget.previewMc.getChildByName('turn%sName' % typeStr)
        spriteId = spriteInfo.get('spriteId', 0)
        turnSlot.slot.setItemSlotData({'iconPath': uiUtils.getSummonSpriteIconPath(spriteId)})
        turnSlot.slot.dragable = False
        spriteName = spriteInfo.get('name', '')
        turnName.text = spriteName

    @property
    def ownYunChuiFame(self):
        return BigWorld.player().getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
