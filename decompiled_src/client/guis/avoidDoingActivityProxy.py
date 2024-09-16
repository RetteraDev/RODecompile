#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/avoidDoingActivityProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import utils
import events
import const
import uiConst
import gamelog
import gametypes
from item import Item
from uiProxy import UIProxy
from guis import uiUtils
from asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import avoid_doing_activity_data as ADAD
from data import play_recomm_item_data as PRID
from data import fame_data as FD
from data import consumable_item_data as CID
from data import bonus_data as BD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
CONDITION_TIP = gameStrings.TEXT_AVOIDDOINGACTIVITYPROXY_27
FREESCORE_TIP = gameStrings.TEXT_AVOIDDOINGACTIVITYPROXY_28
ACTIVITY_DESC = gameStrings.TEXT_AVOIDDOINGACTIVITYPROXY_29
BARBECUE = gameStrings.TEXT_AVOIDDOINGACTIVITYPROXY_30
WINE = gameStrings.TEXT_AVOIDDOINGACTIVITYPROXY_31
TIP_DATA = {'addActivation': 'active',
 'addFame': 'shenwang',
 'addExp': 'exp',
 'addSocialExp': 'socialExp',
 'addBindCash': 'bindCash'}
HEART_DEMON_KEY = [11, 12, 13]
HOT_SPRING_KEY = [9, 10]

class AvoidDoingActivityProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AvoidDoingActivityProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_AVOID_DOING_ACTIVITY, self.hide)

    def reset(self):
        self.widget = None
        self.first = True
        self.activityKey = 0
        self.itemMC = None
        self.tipMc = None
        self.mc = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_AVOID_DOING_ACTIVITY:
            self.widget = widget
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        else:
            self.itemMC = None
            self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onClickCloseBtn, False, 0, True)
            self.widget.tex.helpIcon.helpKey = 370
            item = Item(SCD.data.get('avoidDoingID', 441702))
            itemData = uiUtils.getGfxItem(item, appendInfo={'itemId': SCD.data.get('avoidDoingID', 441702)})
            self.widget.tex.slot.setItemSlotData(itemData)
            self.widget.tex.slot.dragable = False
            TipManager.addItemTipById(self.widget.tex.slot, itemData['id'])
            self.widget.dailyList.itemRenderer = 'AvoidDoingActivity_ItemMC'
            self.itemMCs = []
            self.initData()
            if not self.heartDemonKey:
                self.widget.dailyList.dataArray = self.data
            self.widget.dailyList.lableFunction = self.lableFunction
            self.widget.dailyList.column = 2
            self.widget.dailyList.itemWidth = 380
            self.widget.dailyList.itemHeight = 80
            self.widget.dailyList.barAlwaysVisible = True
            self.widget.pointIcon.bonusType = 'avoidDoing'
            self.widget.pointIcon.tip = gameStrings.TEXT_AVOIDDOINGACTIVITYPROXY_78
            self.widget.pointLbl.text = BigWorld.player().freeScore
            if CID.data.get(SCD.data.get('avoidDoingID', 441702), {}).has_key('useLimit'):
                total = CID.data.get(SCD.data.get('avoidDoingID', 441702), {}).get('useLimit', [])[0][1]
                self.widget.timesLbl.text = '%d/%d' % (total - uiUtils.getItemUseNum(SCD.data.get('avoidDoingID', 441702), gametypes.ITEM_USE_LIMIT_TYPE_DAY), total)
            else:
                self.widget.timesLbl.visible = False
                self.widget.timesTipLbl.visible = False
            return

    def onClickCloseBtn(self, *args):
        self.hide()

    def lableFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        activityKey = itemData[0]
        avoidDoneCount = itemData[1]
        disabled = itemData[2]
        point = ADAD.data.get(activityKey, {}).get('consumeFreeCredits', 0)
        ASUtils.setHitTestDisable(itemMc.hoverMc, True)
        itemMc.idx = activityKey
        itemMc.activityName.text = ADAD.data.get(activityKey, {}).get('name', '')
        itemMc.point.text = point
        itemMc.icon.bonusType = 'avoidDoing'
        itemMc.icon.tip = gameStrings.TEXT_AVOIDDOINGACTIVITYPROXY_78
        maxTimes = ADAD.data.get(activityKey, {}).get('count', 0)
        id = ADAD.data.get(activityKey, {}).get('activationIds', ())[0]
        if activityKey in HOT_SPRING_KEY:
            fameId = ADAD.data.get(activityKey, {}).get('fameId', 0)
            curValue = BigWorld.player().fame.get(fameId, 0)
            maxValue = FD.data.get(fameId).get('maxVal', 0)
            if fameId == gametypes.RECOMMEND_WENQUAN_SHILIANG:
                itemMc.desc.text = BARBECUE % (curValue, maxValue)
            elif fameId == gametypes.RECOMMEND_WENQUAN_JIULI:
                itemMc.desc.text = WINE % (curValue, maxValue)
            if curValue:
                itemMc.comFlag.visible = False
                itemMc.btn.visible = True
            else:
                itemMc.comFlag.visible = True
                itemMc.btn.visible = False
        else:
            itemMc.desc.text = ACTIVITY_DESC % (avoidDoneCount, maxTimes)
            comFlag = gameglobal.rds.ui.playRecommActivation.getComFlagFromId(id)
            if comFlag[0] == 2:
                itemMc.comFlag.visible = True
                itemMc.btn.visible = False
            else:
                itemMc.comFlag.visible = False
                itemMc.btn.visible = True
        itemMc.btn.disabled = False
        if disabled:
            itemMc.btn.disabled = True
            TipManager.addTip(itemMc.btn, CONDITION_TIP)
        if BigWorld.player().freeScore < point:
            itemMc.btn.disabled = True
            TipManager.addTip(itemMc.btn, FREESCORE_TIP)
            if not disabled:
                self.itemMCs.append(itemMc)
                itemMc.point.htmlText = "<font color=\'#e51717\'>" + itemMc.point.text + '</font>'
        itemMc.btn.key = activityKey
        itemMc.btn.addEventListener(events.BUTTON_CLICK, self.onClickAvoidDoingBtn, False, 0, True)
        if not self.itemMC and (not self.activityKey or not self.first or self.activityKey and activityKey == self.activityKey):
            self.itemMC = itemMc
            if self.first and self.activityKey:
                if itemMc.btn.visible and not itemMc.btn.disabled:
                    self.uiAdapter.avoidDoingActivityTip.show(activityKey)
            self.first = False
            itemMc.hoverMc.visible = True
            self.updateTipMc(activityKey)
        else:
            itemMc.hoverMc.visible = False
        icon = PRID.data.get(id, {}).get('icon', 0)
        item = Item(icon)
        itemData = uiUtils.getGfxItem(item, appendInfo={'itemId': icon})
        itemMc.slot.setItemSlotData(itemData)
        ASUtils.setHitTestDisable(itemMc.slot, True)
        itemMc.addEventListener(events.MOUSE_CLICK, self.onClickItemMc, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.onRollOverItemMc, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.onRollOutItemMc, False, 0, True)

    def updateTipMc(self, activityKey):
        if not self.tipMc:
            self.tipMc = self.widget.getInstByClsName('ActivityTips_AvoidDoing')
            self.widget.addChild(self.tipMc)
            self.tipMc.x = self.widget.hit.x + self.widget.hit.width
            self.tipMc.y = self.widget.hit.y
            self.tipMc.closeBtn.addEventListener(events.BUTTON_CLICK, self.onClickTipCloseBtn, False, 0, True)
        for i in xrange(len(self.mc)):
            self.tipMc.removeChild(self.mc[i])

        self.tipMc.visible = True
        self.tipMc.title.text = ADAD.data.get(activityKey, {}).get('name', '')
        bonusByLv = ADAD.data.get(activityKey, {}).get('bonusByLv', {})
        bonusId = 0
        p = BigWorld.player()
        for lvRange, lvBonusId in bonusByLv.iteritems():
            if lvRange[0] <= p.lv <= lvRange[1]:
                bonusId = lvBonusId
                break

        datas = BD.data.get(bonusId, {}).get('fixedBonus', ())
        posY = 70
        for idx, data in enumerate(datas):
            if data[0] == 1:
                item = Item(data[1])
                itemData = uiUtils.getGfxItem(item, appendInfo={'itemId': data[1]})
                itemData['count'] = data[2]
                itemMc = self.widget.getInstByClsName('M12_InventorySlot_L')
                self.tipMc.addChild(itemMc)
                self.mc.append(itemMc)
                itemMc.x = 12 + idx % 6 * itemMc.width
                itemMc.y = 70 + int(idx / 6) * itemMc.height
                posY = itemMc.y + itemMc.height
                itemMc.setItemSlotData(itemData)
                itemMc.dragable = False
                TipManager.addItemTipById(itemMc, itemData['id'])

        posY += 10
        for key, bonusType in TIP_DATA.iteritems():
            if ADAD.data.get(activityKey, {}).has_key(key):
                data = ADAD.data.get(activityKey, {})[key]
                if type(data) == tuple:
                    for item in data:
                        itemMc = self.widget.getInstByClsName('ActivityQuest_RewardIcon')
                        itemMc.icon.bonusType = bonusType
                        itemMc.value.text = item[1]
                        itemMc.icon.tip = FD.data.get(item[0], {}).get('name', '')
                        posY = self.addItemMc(itemMc, posY)

                else:
                    itemMc = self.widget.getInstByClsName('ActivityQuest_RewardIcon')
                    itemMc.icon.bonusType = bonusType
                    if type(data) == int:
                        itemMc.value.text = data
                    elif hasattr(data, '__call__'):
                        d = {'lv': p.lv,
                         'slv': p.socLv,
                         'n': 3}
                        itemMc.value.text = int(data(d))
                    posY = self.addItemMc(itemMc, posY)

        self.tipMc.bg.height = posY + 15

    def addItemMc(self, itemMc, posY):
        self.tipMc.addChild(itemMc)
        self.mc.append(itemMc)
        itemMc.x = 12
        itemMc.y = posY
        posY += itemMc.height + 5
        return posY

    def onClickTipCloseBtn(self, *args):
        self.tipMc.visible = False

    def onClickItemMc(self, *args):
        e = ASObject(args[3][0])
        if self.itemMC:
            if self.itemMC.idx == e.currentTarget.idx:
                return
            self.itemMC.hoverMc.visible = False
        self.itemMC = e.currentTarget
        self.updateTipMc(self.itemMC.idx)

    def onRollOverItemMc(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.hoverMc.visible = True

    def onRollOutItemMc(self, *args):
        e = ASObject(args[3][0])
        if self.itemMC and self.itemMC.idx == e.currentTarget.idx:
            return
        e.currentTarget.hoverMc.visible = False

    def onClickAvoidDoingBtn(self, *args):
        e = ASObject(args[3][0])
        activityKey = e.currentTarget.key
        if self.inOpenTime(activityKey):
            self.uiAdapter.avoidDoingActivityTip.show(activityKey)
        else:
            BigWorld.player().showGameMsg(GMDD.data.AVOID_DOING_INVALID_TIP, ())

    def initData(self):
        self.data = []
        self.heartDemonKey = 0
        isRequest = False
        p = BigWorld.player()
        for activityType, activity in getattr(p, 'avoidDoingActivity', {}).iteritems():
            try:
                if not self.inOpenTime(activity.activityKey):
                    continue
                group = ADAD.data.get(activity.activityKey, {}).get('group', 0)
                if group and not isRequest:
                    isRequest = True
                    self.heartDemonKey = activity.activityKey
                    p.cell.queryBonusHistory(group)
                self.data.append([activity.activityKey, activity.avoidDoneCount, not activity.calcActivityAvoidDoingFlag(p)])
            except Exception as e:
                gamelog.info('@ljb:error', e.message)

        if not isRequest:
            self.data.sort(cmp=self.compare)

    def inOpenTime(self, activityKey):
        adad = ADAD.data.get(activityKey, ())
        openTime = adad.get('openTime', None)
        closeTime = adad.get('closeTime', None)
        tWhen = utils.getNow()
        if openTime and closeTime and utils.getDisposableCronTabTimeStamp(openTime) <= tWhen <= utils.getDisposableCronTabTimeStamp(closeTime):
            return True
        else:
            return False

    def compare(self, d1, d2):
        if d2[2] and not d1[2]:
            return -1
        else:
            return 0

    def setBonusHistory(self, data):
        if not self.widget or data[0] != ADAD.data.get(self.heartDemonKey, {}).get('group', 0):
            return
        for key in HEART_DEMON_KEY:
            activityType = ADAD.data.get(key, {}).get('activityType', 0)
            activity = BigWorld.player().avoidDoingActivity.getActivity(activityType)
            activity.avoidDoneCount = data[1].values()[0]

        self.heartDemonKey = 0
        for item in self.data:
            if item[0] in HEART_DEMON_KEY:
                item[1] = data[1].values()[0]
                item[2] = data[1].values()[0] >= ADAD.data.get(item[0], {}).get('count', 0) or item[2]

        self.data.sort(cmp=self.compare)
        self.widget.dailyList.dataArray = self.data

    def updateFreeScore(self, old, new):
        if not self.widget:
            return
        self.widget.pointLbl.text = new
        if CID.data.get(SCD.data.get('avoidDoingID', 441702), {}).has_key('useLimit'):
            total = CID.data.get(SCD.data.get('avoidDoingID', 441702), {}).get('useLimit', [])[0][1]
            self.widget.timesLbl.text = '%d/%d' % (total - uiUtils.getItemUseNum(SCD.data.get('avoidDoingID', 441702), gametypes.ITEM_USE_LIMIT_TYPE_DAY), total)
        if old > new:
            self.uiAdapter.playRecommActivation.refreshInfo()
        else:
            for itemMc in self.itemMCs:
                point = ADAD.data.get(itemMc.idx, {}).get('consumeFreeCredits', 0)
                if new >= point and itemMc.btn.disabled:
                    itemMc.btn.disabled = False
                    TipManager.removeTip(itemMc.btn)
                    itemMc.point.htmlText = itemMc.point.text

    def setActivityKey(self):
        if self.activityKey in HEART_DEMON_KEY:
            power = BigWorld.player().combatScoreList[const.COMBAT_SCORE]
            self.activityKey = HEART_DEMON_KEY[0]
            for key in HEART_DEMON_KEY:
                score = ADAD.data.get(key, {}).get('combatScore', ())[0]
                if power >= score:
                    self.activityKey = key
                else:
                    return

        elif self.activityKey in HOT_SPRING_KEY:
            self.activityKey = HOT_SPRING_KEY[0]
            for key in HOT_SPRING_KEY:
                fameId = ADAD.data.get(key, {}).get('fameId', 0)
                curValue = BigWorld.player().fame.get(fameId, 0)
                if curValue:
                    self.activityKey = key
                    return

    def show(self, activityKey = 0):
        if not self.widget:
            self.activityKey = activityKey
            self.setActivityKey()
            p = BigWorld.player()
            p.cell.refreshAvoidDoingActivity()
            self.uiAdapter.loadWidget(uiConst.WIDGET_AVOID_DOING_ACTIVITY)

    def clearWidget(self):
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_AVOID_DOING_ACTIVITY)
        self.uiAdapter.avoidDoingActivityTip.hide()
