#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/hierogramShareProxy.o
import BigWorld
import gameglobal
import uiConst
import gametypes
import events
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from guis import tipUtils
from guis.uiProxy import UIProxy
TL_NUM = 8
DL_NUM = 4
WAKE_POS_OFFSET = 23
DL_EFFECT_NUM = 12

class HierogramShareProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HierogramShareProxy, self).__init__(uiAdapter)
        self.widget = None
        self.runeWakeMc = None
        self.hierogramData = {}
        self.jifaPskillMc = None
        self.tianlunPskillMc = None
        self.dilunPskillMc = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_HIEROGRAM_SHARE, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initData()
        self.initUI()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        self.runeWakeMc = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HIEROGRAM_SHARE)

    def show(self):
        if not self.widget:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HIEROGRAM_SHARE)

    def initData(self):
        p = BigWorld.player()
        roleInformationHierogram = gameglobal.rds.ui.roleInformationHierogram
        roleInformationHierogram.appendInitSlotOpenData(self.hierogramData, p.sharedHierogramInfo.get('lv', 0))
        roleInformationHierogram.appendEquipData(self.hierogramData, p.sharedHierogramInfo, uiConst.BAG_RUNE_SHARE)
        roleInformationHierogram.appendPSkillData(self.hierogramData, p.sharedHierogramInfo)
        roleInformationHierogram.appendWakeData(self.hierogramData, p.sharedHierogramInfo)
        roleInformationHierogram.appendEffectData(self.hierogramData, p.sharedHierogramInfo)

    def initUI(self):
        self.initState()
        self.setOpenLvInfo()
        self.setItems()
        self.setPSkillInfo()
        self.setWakeInfo()
        self.setEffectInfo()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.sgexpand.refreshHeight()

    def initState(self):
        self.widget.tianlun.gotoAndPlay('tianlun8')
        self.widget.dilun.gotoAndPlay('dilun4')
        ASUtils.setHitTestDisable(self.widget.tianlunEffect, True)
        if not self.runeWakeMc:
            self.runeWakeMc = self.widget.getInstByClsName('HierogramShare_sgAwakeList')
            self.widget.sgexpand.canvas.addChild(self.runeWakeMc)
            self.jifaPskillMc = self.widget.getInstByClsName('flash.display.MovieClip')
            self.tianlunPskillMc = self.widget.getInstByClsName('flash.display.MovieClip')
            self.dilunPskillMc = self.widget.getInstByClsName('flash.display.MovieClip')
            self.runeWakeMc.jifa.addChild(self.jifaPskillMc)
            self.runeWakeMc.tianlun.addChild(self.tianlunPskillMc)
            self.runeWakeMc.dilun.addChild(self.dilunPskillMc)
        self.runeWakeMc.tianlun.visible = False
        self.runeWakeMc.dilun.visible = False

    def setEffectInfo(self):
        effectInfo = self.hierogramData.get('effectInfo', {})
        if effectInfo:
            if self.widget.tianlunEffect.currentFrameLabel != 'light' and effectInfo['tlEffect']:
                self.widget.tianlunEffect.gotoAndPlay('on')
            if self.widget.tianlunEffect.currentFrameLabel != 'off' and not effectInfo['tlEffect']:
                self.widget.tianlunEffect.gotoAndPlay('off')
            for i in xrange(0, DL_EFFECT_NUM):
                dilunEff = self.widget.getChildByName('dilunEff%d' % i)
                if i in effectInfo['dlEffect']:
                    if dilunEff.currentFrameLabel != 'light':
                        dilunEff.gotoAndPlay('on')
                elif dilunEff.currentFrameLabel != 'off':
                    dilunEff.gotoAndPlay('off')

        else:
            self.widget.tianlunEffect.gotoAndPlay('off')
            for i in xrange(0, DL_EFFECT_NUM):
                dilunEff = self.widget.getChildByName('dilunEff%d' % i)
                dilunEff.gotoAndPlay('off')

    def setWakeInfo(self):
        wakeInfo = self.hierogramData.get('wakeInfo', {})
        self.widget.removeAllInst(self.tianlunPskillMc)
        self.widget.removeAllInst(self.dilunPskillMc)
        self.runeWakeMc.tianlun.visible = False
        self.runeWakeMc.dilun.visible = False
        if wakeInfo:
            self.runeWakeMc.tianlun.y = self.runeWakeMc.jifa.height + 5
            tlY = 0
            wakeItemMc = self.widget.getInstByClsName('HierogramShare_tianlunWakeDesc')
            wakeItemMc.descText.htmlText = wakeInfo['tianlunWakeNum'][0]
            wakeItemMc.descText.textColor = 14995110
            self.tianlunPskillMc.addChild(wakeItemMc)
            wakeItemMc.y = WAKE_POS_OFFSET + 5
            lastHeight = self.runeWakeMc.tianlun.height
            tlArr = wakeInfo['tianlunWake']
            for i in xrange(0, len(tlArr)):
                wakeItemMc = self.widget.getInstByClsName('HierogramShare_tianlunWakeDesc')
                wakeItemMc.descText.htmlText = tlArr[i][0]
                wakeItemMc.descText.textColor = 16777190 if tlArr[i][1] else 10065034
                self.tianlunPskillMc.addChild(wakeItemMc)
                wakeItemMc.y = lastHeight + WAKE_POS_OFFSET * i

            self.runeWakeMc.tianlun.visible = True
            self.runeWakeMc.dilun.y = self.runeWakeMc.tianlun.y + self.runeWakeMc.tianlun.height + 5
            wakeItemMc = self.widget.getInstByClsName('HierogramShare_tianlunWakeDesc')
            wakeItemMc.descText.htmlText = wakeInfo['dilunWakeNum'][0]
            wakeItemMc.descText.textColor = 14995110
            self.dilunPskillMc.addChild(wakeItemMc)
            wakeItemMc.y = WAKE_POS_OFFSET + 4
            lastHeight = self.runeWakeMc.dilun.height + 2
            dlArr = wakeInfo['dilunWake']
            for i in xrange(0, len(dlArr)):
                wakeItemMc = self.widget.getInstByClsName('HierogramShare_dilunWakeDesc')
                wakeItemMc.descText.htmlText = dlArr[i][0]
                wakeItemMc.descText.textColor = 16777190 if dlArr[i][1] else 10065034
                self.dilunPskillMc.addChild(wakeItemMc)
                wakeItemMc.y = lastHeight + WAKE_POS_OFFSET * i

            self.runeWakeMc.dilun.visible = True

    def setPSkillInfo(self):
        self.widget.removeAllInst(self.jifaPskillMc)
        pSkillInfo = self.hierogramData.get('pskillInfo', {})
        if pSkillInfo:
            pArr = pSkillInfo['pskillArray']
            wakeHeight = self.runeWakeMc.jifa.height
            for pskillItemCount in xrange(0, len(pArr)):
                pskillItemMc = self.widget.getInstByClsName('HierogramShare_pskillItem')
                pskillItemMc.nameText.text = pArr[pskillItemCount]['name']
                pskillItemMc.descText.htmlText = pArr[pskillItemCount]['desc']
                pskillItemMc.descText.x = pskillItemMc.nameText.x + pskillItemMc.nameText.textWidth + 2
                self.jifaPskillMc.addChild(pskillItemMc)
                pskillItemMc.y = wakeHeight + pskillItemCount * WAKE_POS_OFFSET

            if len(pArr) <= 0:
                pskillItemMc = self.widget.getInstByClsName('HierogramShare_PskillNotice')
                pskillItemMc.y = self.runeWakeMc.jifa.height
                self.jifaPskillMc.addChild(pskillItemMc)

    def setItems(self):
        itemInfos = self.hierogramData.get('itemInfos', {})
        if itemInfos['hieroEquipItem']:
            TipManager.removeTip(self.widget.sgslot)
            self.widget.sgslot.gotoAndPlay('wake')
            hieroEquipItem = itemInfos['hieroEquipItem']
            hieroEquipItem['itemId'] = hieroEquipItem['id']
            self.widget.sgslot.slot.setItemSlotData(hieroEquipItem)
            self.widget.sgslot.slot.dragable = False
            self.widget.sgslot.redPointMc.visible = False
            self.widget.sgslot.slot.visible = True
        if itemInfos['tianlunItems']:
            for i in xrange(0, len(itemInfos['tianlunItems'])):
                _index = itemInfos['tianlunItems'][i][0]
                tianlunSlot = self.widget.tianlun.tl.getChildByName('tlslot%d' % _index)
                TipManager.removeTip(tianlunSlot)
                tianlunSlot.gotoAndPlay('wake')
                itemInfos['tianlunItems'][i][1]['itemId'] = itemInfos['tianlunItems'][i][1]['id']
                tianlunSlot.slot.setItemSlotData(itemInfos['tianlunItems'][i][1])
                tianlunSlot.slot.dragable = False
                tianlunSlot.redPointMc.visible = False
                tianlunSlot.slot.visible = True
                if itemInfos['tianlunItems'][i][1]['isInvalid']:
                    ASUtils.setMcEffect(tianlunSlot.slot, 'gray')

        if itemInfos['dilunItems']:
            for i in xrange(0, len(itemInfos['dilunItems'])):
                _index = itemInfos['dilunItems'][i][0]
                dlSlot = self.widget.dilun.dl.getChildByName('dlslot%d' % _index)
                TipManager.removeTip(dlSlot)
                dlSlot.gotoAndPlay('wake')
                itemInfos['dilunItems'][i][1]['itemId'] = itemInfos['dilunItems'][i][1]['id']
                dlSlot.slot.setItemSlotData(itemInfos['dilunItems'][i][1])
                dlSlot.slot.dragable = False
                dlSlot.redPointMc.visible = False
                dlSlot.slot.visible = True
                if itemInfos['dilunItems'][i][1]['isInvalid']:
                    ASUtils.setMcEffect(dlSlot.slot, 'gray')

        if itemInfos['benyuanItem']:
            TipManager.removeTip(self.widget.benyuan)
            self.widget.benyuan.gotoAndPlay('wake')
            itemInfos['benyuanItem']['itemId'] = itemInfos['benyuanItem']['id']
            self.widget.benyuan.slot.setItemSlotData(itemInfos['benyuanItem'])
            self.widget.benyuan.slot.dragable = False
            self.widget.benyuan.redPointMc.visible = False
            self.widget.benyuan.slot.visible = True

    def setOpenLvInfo(self):
        openLvInfo = self.hierogramData.get('openLv', {})
        for i in xrange(0, TL_NUM):
            tlSlot = self.widget.tianlun.tl.getChildByName('tlslot%d' % i)
            if i < openLvInfo['openArr'][0]:
                tlSlot.gotoAndPlay('wakewait')
                TipManager.addTip(tlSlot, openLvInfo['tianlun'][i][3])
                tlSlot.redPointMc.visible = True
                tlSlot.slot.visible = True
            else:
                tlSlot.gotoAndPlay('nowake')
                tlSlot.lvTxt.text = openLvInfo['tianlun'][i][1]
                ASUtils.setHitTestDisable(tlSlot.lvTxt, True)
                ASUtils.setHitTestDisable(tlSlot.openTxt, True)
                TipManager.addTip(tlSlot, openLvInfo['tianlun'][i][2])
                tlSlot.redPointMc.visible = False
                tlSlot.slot.visible = False
            tlSlot.slot.setItemSlotData(None)
            tlSlot.slot.dragable = False
            ASUtils.setMcEffect(tlSlot.slot, '')

        for i in xrange(0, DL_NUM):
            diLunSlot = self.widget.dilun.dl.getChildByName('dlslot%d' % i)
            if i < openLvInfo['openArr'][1]:
                diLunSlot.gotoAndPlay('wakewait')
                TipManager.addTip(diLunSlot, openLvInfo['dilun'][i][3])
                diLunSlot.redPointMc.visible = True
                diLunSlot.slot.visible = True
            else:
                diLunSlot.gotoAndPlay('nowake')
                diLunSlot.lvTxt.text = openLvInfo['dilun'][i][1]
                ASUtils.setHitTestDisable(diLunSlot.lvTxt, True)
                ASUtils.setHitTestDisable(diLunSlot.openTxt, True)
                TipManager.addTip(diLunSlot, openLvInfo['dilun'][i][2])
                diLunSlot.redPointMc.visible = False
                diLunSlot.slot.visible = False
            diLunSlot.slot.setItemSlotData(None)
            diLunSlot.slot.dragable = False
            ASUtils.setMcEffect(diLunSlot.slot, '')

        if openLvInfo['openArr'][2] > 0:
            self.widget.benyuan.gotoAndPlay('wakewait')
            TipManager.addTip(self.widget.benyuan, openLvInfo['benyuan'][3])
            self.widget.benyuan.redPointMc.visible = True
            self.widget.benyuan.slot.visible = True
        else:
            self.widget.benyuan.gotoAndPlay('nowake')
            self.widget.benyuan.lvTxt.text = openLvInfo['benyuan'][1]
            ASUtils.setHitTestDisable(self.widget.benyuan.lvTxt, True)
            ASUtils.setHitTestDisable(self.widget.benyuan.openTxt, True)
            TipManager.addTip(self.widget.benyuan, openLvInfo['benyuan'][2])
            self.widget.benyuan.redPointMc.visible = False
            self.widget.benyuan.slot.visible = False
        self.widget.benyuan.slot.setItemSlotData(None)
        self.widget.benyuan.slot.dragable = False
        if openLvInfo['openArr'][3] > 0:
            self.widget.sgslot.gotoAndPlay('wakewait')
            TipManager.addTip(self.widget.sgslot, openLvInfo['sgslot'][3])
            self.widget.sgslot.redPointMc.visible = True
            self.widget.sgslot.slot.visible = True
        else:
            self.widget.sgslot.gotoAndPlay('nowake')
            self.widget.sgslot.lvTxt.text = openLvInfo['sgslot'][1]
            ASUtils.setHitTestDisable(self.widget.sgslot.lvTxt, True)
            ASUtils.setHitTestDisable(self.widget.sgslot.openTxt, True)
            TipManager.addTip(self.widget.sgslot, openLvInfo['sgslot'][2])
            self.widget.sgslot.redPointMc.visible = False
            self.widget.sgslot.slot.visible = False
        self.widget.sgslot.slot.setItemSlotData(None)
        self.widget.sgslot.slot.dragable = False
