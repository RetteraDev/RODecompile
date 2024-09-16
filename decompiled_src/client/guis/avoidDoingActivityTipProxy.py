#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/avoidDoingActivityTipProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import const
import events
import gametypes
import gameglobal
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
from data import avoid_doing_activity_data as ADAD
from data import avatar_lv_data as ALD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
POWER_TIP = gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_21
CUR_POWER_TIP = gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_22
TIP = gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_23
SUBMIT_ITEM = gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_24
AVOID_DOING = gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_25
WINE_TIP = gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_26
BARBECUE_TIP = gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_27

class AvoidDoingActivityTipProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AvoidDoingActivityTipProxy, self).__init__(uiAdapter)
        self.type = 'avoidDoing'
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_AVOID_DOING_ACTIVITY_TIP, self.hide)

    def reset(self):
        self.widget = None
        self.inventoryCloseCallback = False
        self.itemId = 0
        self.activityKey = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_AVOID_DOING_ACTIVITY_TIP:
            self.widget = widget
            self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onClickCloseBtn, False, 0, True)
            self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.onClickCloseBtn, False, 0, True)
            self.initUI()

    def initUI(self):
        self.widget.powerTip.visible = False
        self.widget.curPowerTip.visible = False
        self.widget.confirmTip.visible = False
        self.widget.itemTip.visible = False
        power = ADAD.data.get(self.activityKey, {}).get('combatScore', ())
        p = BigWorld.player()
        score = p.combatScoreList[const.COMBAT_SCORE]
        if len(power) and score < power[0]:
            self.widget.title.textField.text = TIP
            self.widget.powerTip.visible = True
            self.widget.powerTip.text = POWER_TIP % power[0]
            self.widget.curPowerTip.visible = True
            self.widget.curPowerTip.htmlText = CUR_POWER_TIP % score
            self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onClickCloseBtn, False, 0, True)
            self.widget.cancelBtn.visible = False
            self.widget.confirmBtn.x = 140
        else:
            items = ADAD.data.get(self.activityKey, {}).get('consumeItems', ())
            if len(items):
                self.widget.title.textField.text = SUBMIT_ITEM
                self.widget.itemTip.visible = True
                fameId = ADAD.data.get(self.activityKey, {}).get('fameId', 0)
                if fameId == gametypes.RECOMMEND_WENQUAN_SHILIANG:
                    self.widget.itemTip.tip.text = BARBECUE_TIP
                elif fameId == gametypes.RECOMMEND_WENQUAN_JIULI:
                    self.widget.itemTip.tip.text = WINE_TIP
                if not self.uiAdapter.inventory.mediator:
                    self.uiAdapter.inventory.show()
                self.widget.itemTip.slot.setItemSlotData(None)
                self.widget.itemTip.slot.binding = 'avoidDoingActivityTip..%d' % fameId
                self.inventoryCloseCallback = True
                self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.confirmTip, False, 0, True)
            else:
                self.confirmTip()

    def setItem(self, item):
        items = ADAD.data.get(self.activityKey, {}).get('consumeItems', ())
        itemId = uiUtils.getParentId(item.id)
        if len(items):
            for data in items:
                if data[0] == itemId:
                    self.itemId = item.id
                    itemData = uiUtils.getGfxItem(item, appendInfo={'itemId': item.id})
                    itemData['count'] = 1
                    self.widget.itemTip.slot.setItemSlotData(itemData)
                    self.widget.itemTip.slot.dragable = False
                    TipManager.addItemTipById(self.widget.itemTip.slot, itemData['id'])
                    return True

        return False

    def confirmTip(self, *args):
        if self.widget.itemTip.visible and not self.itemId:
            return
        self.widget.title.textField.text = TIP
        self.widget.confirmTip.visible = True
        self.widget.itemTip.visible = False
        self.widget.confirmTip.icon.bonusType = 'avoidDoing'
        self.widget.confirmTip.point.text = ADAD.data.get(self.activityKey, {}).get('consumeFreeCredits', 0)
        self.widget.confirmTip.avtivityName.text = AVOID_DOING % ADAD.data.get(self.activityKey, {}).get('name', '')
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.avoidDoing, False, 0, True)

    def avoidDoing(self, *args):
        p = BigWorld.player()
        d = {'lv': p.lv,
         'slv': p.socLv,
         'n': 1}
        if self.itemId:
            for index, data in enumerate(ADAD.data.get(self.activityKey, {}).get('consumeItems', ())):
                if data[0] == self.itemId:
                    d['n'] = index + 1

        maxVal = ALD.data.get(p.lv, {}).get('maxExpXiuWei', 0)
        if ADAD.data.get(self.activityKey, {}).has_key('addExp'):
            addExpFunc = ADAD.data.get(self.activityKey, {})['addExp']
            addExp = int(addExpFunc(d))
            oldVal = p.expXiuWei
            newVal = min(oldVal + addExp, maxVal)
            delta = newVal - oldVal
            if delta < addExp:
                msg = uiUtils.getTextFromGMD(GMDD.data.AVOID_DOING_EXP_CHECK, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.confirmAvoidDoing, yesBtnText=gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_128, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)
            else:
                self.confirmAvoidDoing()
        else:
            self.confirmAvoidDoing()

    def confirmAvoidDoing(self):
        p = BigWorld.player()
        if ADAD.data.get(self.activityKey, {}).has_key('isExpAddSprite') and not p.summonedSpriteInWorld and not self.uiAdapter.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_REWARD_RECOVERY_SUMMON_SPRITE, False):
            msg = GMD.data.get(GMDD.data.AVOID_DOING_SUMMON_SPRITE_NOT_IN_WORLD, {}).get('text', '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self._avoidDoing, yesBtnText=gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_138, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_REWARD_RECOVERY_SUMMON_SPRITE)
        else:
            self._avoidDoing()

    def _avoidDoing(self):
        p = BigWorld.player()
        items = []
        if self.itemId:
            items.append(self.itemId)
        p.cell.avoidDoingActivityRequest(ADAD.data.get(self.activityKey, {}).get('activityType', 0), items)
        self.hide()

    def onClickCloseBtn(self, *args):
        if self.inventoryCloseCallback:
            self.uiAdapter.inventory.hide()
        self.hide()

    def show(self, activityKey):
        if not self.widget:
            self.activityKey = activityKey
            self.uiAdapter.loadWidget(uiConst.WIDGET_AVOID_DOING_ACTIVITY_TIP)

    def clearWidget(self):
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_AVOID_DOING_ACTIVITY_TIP)
