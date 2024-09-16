#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/getSkillPointProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import events
import formula
from uiProxy import UIProxy
from item import Item
from callbackHelper import Functor
from guis.asObject import TipManager
from guis.asObject import ASUtils
from cdata import skill_enhance_jingjie_data as SEJD
from cdata import skill_enhance_cost_data as SECD
from data import item_data as ID
from data import sys_config_data as SCD
from data import consumable_item_data as CID
YUNCHUI_FAME_ID = 453
COLOR_RED = '#CC2929'

class GetSkillPointProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GetSkillPointProxy, self).__init__(uiAdapter)
        self.resetData()

    def resetData(self):
        self.frameInfo = {}
        self.widget = None
        self.costCount = 0

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self._initUI()
        self.refreshFrame()

    def show(self):
        p = BigWorld.player()
        frameInfo = self.getFrameInfo()
        if not frameInfo:
            return
        self.frameInfo = frameInfo
        self.uiAdapter.loadWidget(uiConst.WIDGET_GET_SKILL_POINT)

    def getFrameInfo(self):
        p = BigWorld.player()
        frameInfo = {}
        nowEnhPont = self._getUsedEnhancePoint() + p.skillEnhancePoint
        totalEnhPoint = SEJD.data.get((p.arenaJingJie, p.arenaLv), {}).get('maxEnhancePoint', 0)
        nextEnhPoint = nowEnhPont + 1
        cfgData = SECD.data.get(nextEnhPoint, None)
        if not cfgData:
            return
        else:
            needYuanSheng = cfgData.get('exp', 0)
            itemId = SCD.data.get('YSD_ITEM_ID', 999)
            frameInfo['itemId'] = itemId
            fid0 = SCD.data.get('YSD_EQUAL_IN_VAL_FORMULA')
            vars = {'lv': p.lv}
            effect = formula.calcFormulaById(fid0, vars)
            fid1 = SCD.data.get('YSD_MAX_USE_PER_POINT_FORMULA')
            vars = {'exp': needYuanSheng,
             'per': effect}
            maxDiKouCount = formula.calcFormulaById(fid1, vars)
            frameInfo['effect'] = effect
            frameInfo['totalPoint'] = totalEnhPoint
            frameInfo['nowEnhPoint'] = nowEnhPont
            frameInfo['yunQuan'] = cfgData.get('cash', 0)
            frameInfo['totalYunQuan'] = p.bindCash
            frameInfo['yunBi'] = p.cash
            frameInfo['exp'] = p.exp
            frameInfo['maxDiKouCount'] = maxDiKouCount
            allItem = p.inv.findAllItemByAttr({'cstype': Item.SUBTYPE_2_YUANSHENDAN})
            itemCount = 0
            for page, pos in allItem:
                item = p.inv.getQuickVal(page, pos)
                canUse = True
                serverEvent = CID.data.get(item.id, {}).get('serverEvent', ())
                for msId in serverEvent:
                    if not p.isServerProgressFinished(msId):
                        canUse = False
                        break

                if not canUse:
                    continue
                conditionList = ID.data.get(item.id, {}).get('conditionsList')
                if conditionList:
                    if item.extraCheck(p) and not item.hasLatch():
                        itemCount += item.cwrap

            frameInfo['itemCount'] = itemCount
            dailyMaxDiKou = cfgData.get('yuanShenDanLimitDaily', 0)
            if dailyMaxDiKou != 0:
                leftDiKouCount = dailyMaxDiKou - getattr(p, 'usedYuanShenDanDaily', 0)
                if not self.widget:
                    self.costCount = min(itemCount, maxDiKouCount, leftDiKouCount)
            else:
                leftDiKouCount = 0
                self.costCount = 0
            yuansheng = needYuanSheng - effect * self.costCount
            frameInfo['yuanSheng'] = max(0, yuansheng)
            frameInfo['totalYuanSheng'] = p.expXiuWei
            frameInfo['dailMaxDiKou'] = dailyMaxDiKou
            frameInfo['leftDiKouCount'] = leftDiKouCount
            itemInfo = uiUtils.getGfxItemById(itemId)
            if itemCount < self.costCount:
                countDesc = '%s/%d' % (uiUtils.toHtml(str(itemCount), COLOR_RED), self.costCount)
            else:
                countDesc = '%d/%d' % (itemCount, self.costCount)
            itemInfo['count'] = countDesc
            frameInfo['maxCount'] = min(itemCount, maxDiKouCount, leftDiKouCount)
            frameInfo['itemInfo'] = itemInfo
            return frameInfo

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GET_SKILL_POINT)

    def cleanData(self):
        pass

    def refreshFrame(self):
        if not self.widget:
            return
        frameInfo = self.frameInfo
        self.widget.nowPoint.text = str(frameInfo['nowEnhPoint'])
        self.widget.maxPoint.text = str(frameInfo['totalPoint'])
        cash = frameInfo['totalYunQuan'] + frameInfo['yunBi']
        des0 = str(cash)
        if cash < frameInfo['yunQuan']:
            des0 = uiUtils.toHtml(des0, COLOR_RED)
        des0 = '%s/%d' % (des0, frameInfo['yunQuan'])
        self.widget.cost0.descNum.htmlText = des0
        if frameInfo['totalYunQuan'] == 0:
            self.widget.cost0.txtType.text = gameStrings.TEXT_INVENTORYPROXY_3296
            self.widget.cost0.yes.bonusType = 'cash'
        else:
            self.widget.cost0.txtType.text = gameStrings.TEXT_INVENTORYPROXY_3297
            self.widget.cost0.yes.bonusType = 'bindCash'
        tips = SCD.data.get('skill_point_dikou_desc0', gameStrings.TEXT_GETSKILLPOINTPROXY_152) % (frameInfo['totalYunQuan'], frameInfo['yunBi'])
        TipManager.addTip(self.widget.cost0.descNum, tips)
        exp = frameInfo['totalYuanSheng'] + frameInfo['exp']
        des1 = str(exp)
        if exp < frameInfo['yuanSheng']:
            des1 = uiUtils.toHtml(des1, COLOR_RED)
        des1 = '%s/%d' % (des1, frameInfo['yuanSheng'])
        self.widget.cost1.descNum.htmlText = des1
        textWidth = self.widget.cost1.descNum.textWidth
        mcWidth = self.widget.cost1.descNum.width
        if textWidth > mcWidth:
            ASUtils.autoSizeWithFont(self.widget.cost1.descNum, 14, mcWidth, 5)
        else:
            self.widget.cost1.descNum.getTextFormat().size = 14
        if frameInfo['totalYuanSheng'] == 0:
            self.widget.cost1.costIcon.bonusType = 'exp'
            self.widget.cost1.txtType.text = gameStrings.TEXT_GAMETYPES_6408
        else:
            self.widget.cost1.costIcon.bonusType = 'lingshi'
            self.widget.cost1.txtType.text = gameStrings.TEXT_GETSKILLPOINTPROXY_174
        tips = SCD.data.get('skill_point_dikou_desc1', gameStrings.TEXT_GETSKILLPOINTPROXY_175) % (frameInfo['totalYuanSheng'], frameInfo['exp'])
        TipManager.addTip(self.widget.cost1.descNum, tips)
        leftDiKouDes = str(frameInfo['leftDiKouCount'])
        if frameInfo['leftDiKouCount'] <= 0:
            leftDiKouDes = uiUtils.toHtml(leftDiKouDes, COLOR_RED)
        leftDiKouDes = gameStrings.TEXT_GETSKILLPOINTPROXY_181 % (leftDiKouDes, frameInfo['dailMaxDiKou'])
        self.widget.cost1.leftDiKou.htmlText = leftDiKouDes
        itemInfo = frameInfo['itemInfo']
        itemName = ID.data.get(itemInfo['itemId']).get('name')
        self.widget.cost1.useItem.text = gameStrings.TEXT_GETSKILLPOINTPROXY_187 % itemName
        self.widget.cost1.useEffect.text = gameStrings.TEXT_GETSKILLPOINTPROXY_188 % frameInfo['effect']
        if not self.widget.cost1.itemSlot.data:
            self.widget.cost1.itemSlot.setItemSlotData(itemInfo)
        else:
            self.widget.cost1.itemSlot.setValueAmountTxt(itemInfo['count'])
        self.widget.cost1.numStepper.minCount = 0
        self.widget.cost1.numStepper.maxCount = frameInfo['maxCount']
        self.widget.cost1.numStepper.count = self.costCount
        self.costCount = int(self.widget.cost1.numStepper.count)
        self.widget.cost1.numStepper.addEventListener(events.EVENT_COUNT_CHANGE, self.onCounterChange, False, 0, True)

    def _initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.cost1.maxBtn.addEventListener(events.MOUSE_CLICK, self.onMaxBtnClick, False, 0, True)
        self.widget.yesBtn.addEventListener(events.MOUSE_CLICK, self.onYesClick, False, 0, True)
        self.widget.noBtn.addEventListener(events.MOUSE_CLICK, self.onNoClick, False, 0, True)
        self.uiAdapter.registerEscFunc(uiConst.WIDGET_GET_SKILL_POINT, self.hide)

    def onMaxBtnClick(self, *args):
        self.widget.cost1.numStepper.count = int(self.widget.cost1.numStepper.maxCount)

    def onCounterChange(self, *args):
        self.costCount = int(self.widget.cost1.numStepper.count)
        self.frameInfo = self.getFrameInfo()
        self.refreshFrame()

    def onYesClick(self, *args):
        func = Functor(self.getSkillPointFun, self.costCount)
        gameglobal.rds.ui.skill.gotoGetSkillEnhancePoint(self.frameInfo['yuanSheng'], self.frameInfo['yunQuan'], func)

    def getSkillPointFun(self, costCount):
        BigWorld.player().cell.getSkillEnhancePoint(costCount)
        self.hide()

    def onNoClick(self, *args):
        self.hide()

    def _getUsedEnhancePoint(self):
        ret = 0
        for skVal in BigWorld.player().skills.values():
            if hasattr(skVal, 'enhanceData'):
                for enhData in skVal.enhanceData.values():
                    ret += enhData.enhancePoint

        return ret
