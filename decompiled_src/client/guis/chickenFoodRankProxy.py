#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chickenFoodRankProxy.o
import BigWorld
import gameglobal
import gamelog
import time
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import chickenFoodFactory
from guis import uiUtils
from gameStrings import gameStrings
from asObject import ASObject
from asObject import ASUtils
from data import sys_config_data as SCD
from data import bonus_history_check_data as BHCD
from cdata import chicken_meal_quality_material_info_data as CMQMID

class ChickenFoodRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChickenFoodRankProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rankInfo = None
        self.topInfo = None
        self.cfFactory = chickenFoodFactory.getInstance()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHICKEN_FOOD_RANK, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHICKEN_FOOD_RANK:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHICKEN_FOOD_RANK, True)

    def clearWidget(self):
        self.widget = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHICKEN_FOOD_RANK)

    def reset(self):
        self.rankInfo = None
        self.topInfo = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        ASUtils.setHitTestDisable(self.widget.title, True)
        self.widget.desc.htmlText = gameStrings.CHICKENFOOD_TIPS_STR
        self.widget.allRank.selected = True
        self.widget.updateBtn.addEventListener(events.MOUSE_CLICK, self.handleClickUpdateBtn, False, 0, True)
        self.widget.list.itemRenderer = 'ChickenFoodRank_Item'
        self.widget.list.dataArray = []
        self.widget.list.lableFunction = self.itemFunction
        self.refreshInfo()

    def refreshInfo(self):
        self.rankInfo = self.cfFactory.getTopRankData()
        if self.hasBaseData():
            _top = self.rankInfo.get('top', [])
            _myself = self.rankInfo.get('myself', [])
            myTotalScore = 0
            for x in xrange(0, 6):
                item = getattr(self.widget, 'myItem' + str(x), None)
                if item:
                    item.visible = False

            if _myself:
                for i, v in enumerate(_myself):
                    foodNo, foodId, quality, star, score, uTime = v
                    myTotalScore += score
                    detailInfo = self.cfFactory.getFoodDetailInfoById(foodId)
                    name = detailInfo.get('name', '')
                    rare = detailInfo.get('rare', 0)
                    icon = detailInfo.get('icon', 0)
                    iconPath = self.cfFactory.getChickenIcon(uiConst.ICON_SIZE40, icon)
                    score = str(score)
                    colorStr = uiUtils.getColorByQuality(rare)
                    info = {'iconPath': iconPath,
                     'score': score,
                     'colorStr': colorStr}
                    item = getattr(self.widget, 'myItem' + str(i), None)
                    if item:
                        item.visible = True
                        item.itemSlot.setData(info)
                        item.starMc.gotoAndStop(''.join(('star', str(star))))

            _str = gameStrings.CHICKENFOOD_SCORE_STR % myTotalScore
            _str = ''.join((gameStrings.CHICKENFOOD_MYCOOKING_STR, _str))
            self.widget.myScore.text = _str
            chickenRankReward = SCD.data.get('chickenRankReward', ())
            for i, v in enumerate(chickenRankReward):
                item = getattr(self.widget.awardShowList, 'item' + str(i), None)
                if item:
                    num1, num2, itemId = v
                    _str = gameStrings.CHICKENFOOD_RANKREWARDNO_STR % (num1, num2)
                    item.slotName.text = _str
                    gfxItem = uiUtils.getGfxItemById(itemId)
                    item.slot.setItemSlotData(gfxItem)

            foodNum, bid = SCD.data.get('chickenBaseReward', ())
            result = gameglobal.rds.ui.playRecommActivation.bonusHistory.get(bid, 0)
            itemId = BHCD.data.get(bid, {}).get('rewardIcons', [0])[0]
            _str = ''
            if result:
                _str = gameStrings.CHICKENFOOD_FINISHED_STR % 1
            else:
                _str = gameStrings.CHICKENFOOD_FINISHED_STR % 0
            self.widget.require.text = _str
            if itemId:
                gfxItem = uiUtils.getGfxItemById(itemId)
                self.widget.rewardItem.setItemSlotData(gfxItem)
            if _top:
                ver, mData, (self.hasReward, lastWeekRank, lastWeedVal, isReward), key = _top
                topRankInfo = []
                tmpInfo = []

                def _genKey(item):
                    mGbId, roleName, school, _info = item
                    return _info

                def _cmp(a, b):
                    score1, lastFinishTime1, foodData1 = a
                    score2, lastFinishTime2, foodData2 = b
                    if score1 > score2:
                        return 1
                    if score1 < score2:
                        return -1
                    if lastFinishTime1 > lastFinishTime2:
                        return 1
                    if lastFinishTime1 < lastFinishTime2:
                        return -1
                    return 0

                mData.sort(cmp=_cmp, key=_genKey, reverse=True)
                for n, m in enumerate(mData):
                    mGbId, roleName, school, _info = m
                    totalScore, lastFinishTime, foodData = _info
                    _chickenFoodInfo = []
                    for _k, _v in enumerate(foodData):
                        foodNo, foodId, quality, star, score, uTime = _v
                        detailInfo = self.cfFactory.getFoodDetailInfoById(foodId)
                        rare = detailInfo.get('rare', 0)
                        _chickenFoodInfo.append((rare, score))

                    topRankInfo.append((roleName, _chickenFoodInfo, totalScore))
                    tmpInfo.append(n)

                self.topInfo = topRankInfo
                self.widget.list.dataArray = tmpInfo

    def itemFunction(self, *args):
        n = int(args[3][0].GetNumber())
        itemMc = ASObject(args[3][1])
        itemInfo = self.topInfo[n]
        roleName, _chickenFoodInfo, totalScore = itemInfo
        itemMc.rank.text = str(n + 1)
        itemMc.playerName.text = roleName
        for x in xrange(0, 6):
            item = getattr(itemMc, 'chickenFood' + str(x), None)
            if item:
                if x < len(_chickenFoodInfo):
                    quality, score = _chickenFoodInfo[x]
                    item.visible = True
                    item.qualityTxt.htmlText = self.cfFactory.transFoodName(gameStrings.CHICKENFOOD_QUALITY_STR[quality], quality)
                    item.score.text = str(score)
                else:
                    item.visible = False

        _str = str(totalScore)
        itemMc.score.text = _str

    def handleClickUpdateBtn(self, *args):
        self.cfFactory.showRank()

    def hasBaseData(self):
        if self.rankInfo and self.cfFactory and self.widget:
            return True
        else:
            return False
