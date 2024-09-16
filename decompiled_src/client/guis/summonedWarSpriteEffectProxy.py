#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteEffectProxy.o
import BigWorld
import uiConst
import gameglobal
import events
import gametypes
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis import uiUtils
from guis.asObject import ASObject
from data import sprite_growth_entry_data as SGED
from data import summon_sprite_info_data as SSID
from data import sys_config_data as SCD
from cdata import sprite_growth_category_data as SGCD
from cdata import sprite_growth_entry_limit_data as SGELD

class SummonedWarSpriteEffectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteEffectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.spriteIndex = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EFFECT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_EFFECT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EFFECT)

    def reset(self):
        self.spriteIndex = None

    def show(self, spriteIndex):
        if not spriteIndex:
            return
        self.spriteIndex = spriteIndex
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EFFECT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.gotoBtn.addEventListener(events.BUTTON_CLICK, self.haneldGotoBtnClick, False, 0, True)
        self.widget.itemList.itemRenderer = 'SummonedWarSpriteEffect_effectItem'
        self.widget.itemList.barAlwaysVisible = True
        self.widget.itemList.dataArray = []
        self.widget.itemList.lableFunction = self.itemFunction

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        spriteData = SSID.data.get(spriteId, {})
        skillLabelList = spriteData.get('universalAbilityLabel', ())
        bonusNum = len(spriteInfo.get('skills', {}).get('bonus', []))
        extraAddLv = SCD.data.get('rareSpriteExtraGrowthLv', 5)
        rareLv = spriteInfo.get('rareLv', 0)
        effectList = []
        for i, parentId in enumerate(SGCD.data):
            if parentId in p.spriteGrowthInfo.keys():
                entries = p.spriteGrowthInfo.get(parentId, {}).get('entries', {})
                for entryId in entries.keys():
                    naturalLimit = SGELD.data.get(entryId, {}).get('naturalLimit', ())
                    bonusLimit = SGELD.data.get(entryId, {}).get('bonusLimit', 0)
                    if bonusNum >= bonusLimit and set(skillLabelList) >= set(naturalLimit) or entryId not in SGELD.data.keys():
                        curLv = entries.get(entryId, {}).get('lv', 0)
                        if curLv:
                            if rareLv == gametypes.SPRITE_RARE_TYPE_SPECIAL:
                                curLv = curLv + extraAddLv
                            sgedData = SGED.data.get((entryId, max(curLv, 1)), {})
                            propContentDesc = uiUtils.toHtml(sgedData.get('propContentDesc', ''), '#623A17')
                            propAddDesc = uiUtils.toHtml(sgedData.get('propAddDesc', ''), '#74C424')
                            itemInfo = {}
                            itemInfo['szName'] = '%s Lv.%d' % (sgedData.get('name', ''), curLv)
                            itemInfo['contentDesc1'] = '%s' % sgedData.get('propContentDesc1', '')
                            itemInfo['preDesc'] = '%s %s' % (propContentDesc, propAddDesc)
                            effectList.append(itemInfo)

        self.widget.noneItemDesc.visible = not effectList
        self.widget.itemList.dataArray = effectList
        self.widget.itemList.validateNow()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.nameText.htmlText = itemData.szName
        itemMc.curPreText.htmlText = itemData.preDesc
        itemMc.contentDesc1.htmlText = itemData.contentDesc1

    def haneldGotoBtnClick(self, *args):
        self.hide()
        gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX3)
