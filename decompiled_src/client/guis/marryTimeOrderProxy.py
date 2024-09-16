#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryTimeOrderProxy.o
import BigWorld
from Scaleform import GfxValue
import gametypes
import gameglobal
import uiConst
import utils
import uiUtils
import const
import pinyinConvert
import events
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from asObject import ASUtils
from data import marriage_config_data as MCD
from data import marriage_package_data as MPD
from cdata import marriage_subscribe_date_data as MSDD
DAY_SEC = 86400

class MarryTimeOrderProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryTimeOrderProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MARRY_TIME_ORDER, self.hide)

    def reset(self):
        self.subscribeDateMap = {}
        self.planParam = []
        self.marriageType = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_TIME_ORDER:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_TIME_ORDER)

    def show(self, subscribeDateMap, planParam, marriageType):
        self.subscribeDateMap = subscribeDateMap
        self.planParam = planParam
        self.marriageType = marriageType
        self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_TIME_ORDER, True)

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        if self.marriageType[0] == gametypes.MARRIAGE_TYPE_PACKAGE:
            self.widget.timeText.text = gameStrings.MARRIAGE_PACKAGE_TIME_TEXT
        elif self.marriageType[0] == gametypes.MARRIAGE_TYPE_GREAT:
            self.widget.timeText.text = gameStrings.MARRIAGE_GREAT_TIME_TEXT

    def initState(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.dayMenu.addEventListener(events.INDEX_CHANGE, self.handleSelectDayMenu, False, 0, True)
        dayInfo, hourInfo = self.getTimeInfo(self.subscribeDateMap)
        ASUtils.setDropdownMenuData(self.widget.dayMenu, dayInfo)
        self.widget.dayMenu.menuRowCount = 7
        _index = 0
        for i, dInfo in enumerate(dayInfo):
            if dInfo.get('rendererEnabled', False):
                _index = i
                break

        self.widget.dayMenu.selectedIndex = _index
        costItemCount = MPD.data.get(self.marriageType, {}).get('costItemCounts', 0)
        costItemIds = MPD.data.get(self.marriageType, {}).get('costItemIds', 0)
        specialDays = MCD.data.get('specialDays', [])
        itemSlot0 = getattr(self.widget.slotNode, 'itemSlot0')
        itemSlot1 = getattr(self.widget.slotNode, 'itemSlot1')
        if len(costItemIds) == 1:
            self.widget.slotNode.gotoAndPlay('one')
        elif len(costItemIds) == 2:
            self.widget.slotNode.gotoAndPlay('two')
        for i, costItemId in enumerate(costItemIds):
            gfxItem = uiUtils.getGfxItemById(costItemId)
            p = BigWorld.player()
            count = p.inv.countItemInPages(costItemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
            numStr = uiUtils.convertNumStr(count, costItemCount[i])
            itemSlot = getattr(self.widget.slotNode, 'itemSlot%s' % i)
            numTxt = getattr(self.widget.slotNode, 'numTxt%s' % i)
            numTxt.htmlText = numStr
            itemSlot.setItemSlotData(gfxItem)
            itemSlot.dragable = False
            if count < costItemCount[i]:
                itemSlot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
                itemSlot.state = uiConst.COMPLETE_ITEM_LEAKED
            else:
                itemSlot.setSlotState(uiConst.ITEM_NORMAL)
                itemSlot.state = uiConst.ITEM_NORMAL
            itemSlot.addEventListener(events.MOUSE_UP, self.handleMouseUp, False, 0, True)

        self.onSelectDay()

    def handleMouseUp(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.state == uiConst.COMPLETE_ITEM_LEAKED:
            self.uiAdapter.onOpenItemSourcePanel()

    def getTimeInfo(self, subscribeDateMap):
        mData = []
        dData = {}
        hData = {}
        dayInfo = []
        hourInfo = {}
        nowTime = utils.getNow()
        beginDay = 0
        endDay = const.MARRIAGE_SUBSCRIBE_DAY_INTERVAL
        if hasattr(self, 'marriageType') and len(self.marriageType) > 0:
            if self.marriageType[0] == 1:
                beginDay = 0
                endDay = const.MARRIAGE_SUBSCRIBE_DAY_INTERVAL
            elif self.marriageType[0] == 2:
                beginDay = 7
                endDay = 30
        for i in xrange(beginDay, endDay):
            tplSec = utils.localtimeEx(nowTime + DAY_SEC * (i + 1), False)
            tmpDayInfo = {'label': gameStrings.MARRY_DAY_FORMAT % (tplSec.tm_mon, tplSec.tm_mday),
             'data': (tplSec.tm_mon, tplSec.tm_mday)}
            if tmpDayInfo not in dayInfo:
                dayInfo.append(tmpDayInfo)
            specialDays = MCD.data.get('specialDays', [])
            hourInfo.setdefault((tplSec.tm_mon, tplSec.tm_mday), [])
            blockTimeIndex = []
            hInfos = subscribeDateMap.get((tplSec.tm_mon, tplSec.tm_mday), [])
            for idx in hInfos:
                blockTime = MSDD.data.get(idx, {}).get('timeBlockList', [])
                if blockTime:
                    blockTimeIndex.extend(blockTime)

            for k, v in MSDD.data.iteritems():
                if (tplSec.tm_wday == 5 or tplSec.tm_wday == 6) and v.get('disableInWeek', 0) and (tplSec.tm_mon, tplSec.tm_mday) not in specialDays:
                    continue
                isMarriageGreat = v.get('isMarriageGreat', 0)
                if self.marriageType and self.marriageType[0] == gametypes.MARRIAGE_TYPE_PACKAGE and isMarriageGreat:
                    continue
                elif self.marriageType and self.marriageType[0] == gametypes.MARRIAGE_TYPE_GREAT and not isMarriageGreat:
                    continue
                msg = gameStrings.MARRY_TIME_FORMAT % (v.get('beginTimeTuple', (0, 0))[0],
                 v.get('beginTimeTuple', (0, 0))[1],
                 v.get('endTimeTuple', (0, 0))[0],
                 v.get('endTimeTuple', (0, 0))[1])
                tmpHourInfo = {'label': msg,
                 'data': k,
                 'rendererEnabled': k not in subscribeDateMap.get((tplSec.tm_mon, tplSec.tm_mday), []) and k not in blockTimeIndex}
                if tmpHourInfo not in hourInfo.get((tplSec.tm_mon, tplSec.tm_mday), ()):
                    hourInfo[tplSec.tm_mon, tplSec.tm_mday].append(tmpHourInfo)

        for dInfo in dayInfo:
            mon, day = dInfo.get('data', (0, 0))
            rendererEnabled = False
            for hInfo in hourInfo.get((mon, day), []):
                if hInfo.get('rendererEnabled', False):
                    rendererEnabled = True
                    break

            dInfo['rendererEnabled'] = rendererEnabled

        return (dayInfo, hourInfo)

    def onSelectDay(self):
        month, day = self.widget.dayMenu.dataProvider[self.widget.dayMenu.selectedIndex].get('data', [0, 0])
        _, hourInfo = self.getTimeInfo(self.subscribeDateMap)
        ASUtils.setDropdownMenuData(self.widget.timeMenu, hourInfo.get((month, day), []))
        self.widget.timeMenu.menuRowCount = min(5, len(hourInfo.get((month, day), [])))
        _index = 0
        for i, hInfo in enumerate(hourInfo.get((month, day), [])):
            if hInfo.get('rendererEnabled', False):
                _index = i
                break

        self.widget.timeMenu.selectedIndex = _index

    def handleSelectDropMenu(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        p = BigWorld.player()
        mType, subType = self.marriageType
        month, day = self.widget.dayMenu.dataProvider[self.widget.dayMenu.selectedIndex].get('data', [0, 0])
        timeIndex = self.widget.timeMenu.dataProvider[self.widget.timeMenu.selectedIndex].get('data', 0)
        p.cell.subscribeMarriagePackageDone(mType, subType, tuple(self.planParam), month, day, timeIndex)
        self.hide()

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def handleSelectMonthMenu(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])

    def handleSelectDayMenu(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        self.onSelectDay()

    def hasEmptyTime(self, subscribeDateMap):
        dayInfo, hourInfo = self.getTimeInfo(subscribeDateMap)
        for i, dInfo in enumerate(dayInfo):
            if dInfo.get('rendererEnabled', False):
                return True

        return False
