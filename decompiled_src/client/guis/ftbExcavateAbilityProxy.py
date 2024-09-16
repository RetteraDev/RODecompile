#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbExcavateAbilityProxy.o
import BigWorld
import time
import uiConst
import events
import gameglobal
import const
import ftbUtils
import gametypes
from Scaleform import GfxValue
from guis import ui
from uiProxy import UIProxy
from callbackHelper import Functor
from asObject import ASObject
from gamestrings import gameStrings
from data import ftb_config_data as FCD
from data import ftb_power_config_data as FPCD
from data import ftb_task_type_data as FTTD
from cdata import ftb_power_config_reverse_data as FPCRD

class FtbExcavateAbilityProxy(UIProxy):
    BG_HEIGHT = 70
    TIP_HEIGHT = 36
    TASK_HEIGHT = 24
    TASK_INTERVAL = 10
    TASK_Y_START = 35
    TASK_NAME_PREFIX = 'guide_task_'
    EXPIRE_TXT_HEIGHT = 20
    MAX_BTYE_PRE_LINE = 68
    TIP_TEXT_HEIGHT_PRE_LINE = 20
    TIP_BG_HEIGHT_ADD = 16
    HOME_RICH_VALUE_TYPE = 7

    def __init__(self, uiAdapter):
        super(FtbExcavateAbilityProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FTB_EXCAVATE_ABILITY, self.hide)

    def reset(self):
        self.selectTab = ''
        self.leftListDataArray = []
        self.rightListDataArray = []
        self.rightListSelectedItem = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FTB_EXCAVATE_ABILITY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FTB_EXCAVATE_ABILITY)
        self.reset()

    def show(self):
        if not gameglobal.rds.configData.get('enableFTB', False):
            return
        if gameglobal.rds.ui.realNameCheck.isPlayerThirdParty():
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FTB_EXCAVATE_ABILITY)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.guideTabBtn.addEventListener(events.MOUSE_CLICK, self._handleChangeTab, False, 0, True)
        self.widget.validityTabBtn.addEventListener(events.MOUSE_CLICK, self._handleChangeTab, False, 0, True)
        self.widget.guidePanel.itemRenderer = 'FtbExcavateAbility_guideItem'
        self.widget.guidePanel.lableFunction = self._guideItemRenderFunc
        self.widget.guidePanel.itemHeightFunction = self._guideItemHeightFunc
        self.widget.guidePanel.dataArray = []
        self.widget.validityPanel.list.itemRenderer = 'FtbExcavateAbility_validityItem'
        self.widget.validityPanel.list.lableFunction = self._validityItemRenderFunc
        self.widget.validityPanel.list.dataArray = []
        self.widget.helpIcon.helpKey = FCD.data.get('powerHelpKey', 0)
        BigWorld.callback(0.0, Functor(self._changeTab, self.widget.guideTabBtn.name))
        p = BigWorld.player()
        if hasattr(p.base, 'queryDiggingPower'):
            p.base.queryDiggingPower()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        guideDigPower = p.ftbDataDetail.guideDigPower
        ephemeralPower = p.ftbDataDetail.ephemeralPower
        baseDigPower = FCD.data.get('basePower', 30)
        self._refreshAbility(baseDigPower, guideDigPower, ephemeralPower)

    def _handleChangeTab(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        self._changeTab(target.name)

    def _handleGuideItemExpend(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.index is None or target.index < 0 or target.index >= len(self.leftListDataArray):
            return
        else:
            isExpand = self.leftListDataArray[target.index]['isExpand']
            self.leftListDataArray[target.index]['isExpand'] = not isExpand
            self.__refreshLeftList()
            return

    def _handleRightListClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if self.rightListSelectedItem:
            self.rightListSelectedItem.select.visible = False
        target.select.visible = True
        self.rightListSelectedItem = target

    def _guideItemRenderFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.__clearAllTask(itemMc)
        isExpand = itemData.isExpand
        taskType = itemData.taskType
        tasksDetail = itemData.tasksDetail
        withoutTip = self.__genItemWithoutTipHeight(len(tasksDetail))
        itemMc.background.selected = isExpand
        itemMc.background.height = withoutTip
        itemMc.background.focusable = False
        itemMc.background.validateNow()
        if isExpand:
            itemMc.tip.visible = True
            itemMc.tip.txt.wordWrap = True
            itemMc.tip.txt.text = FTTD.data.get(taskType, {}).get('typeDesc', '')
            itemMc.tip.txt.height = self.__genTipHeight(taskType) - self.TIP_BG_HEIGHT_ADD
            itemMc.tip.background.height = itemMc.tip.txt.height + self.TIP_BG_HEIGHT_ADD
            itemMc.tip.y = withoutTip
        else:
            itemMc.tip.visible = False
        expire = FTTD.data.get(taskType, {}).get('duration', -1)
        itemMc.expire.y = self.__genExpireTxtPosition(len(tasksDetail))
        itemMc.expire.text = gameStrings.FTB_TEXT_TASK_EXPIRE % expire if expire > 0 else gameStrings.COMMON_INFINITE_TIME_LONG
        itemMc.typeName.text = FTTD.data.get(taskType, {}).get('typeName', '')
        itemMc.arrow.y = itemMc.expire.y + 5
        itemMc.arrow.gotoAndStop('down' if isExpand else 'up')
        for i, detail in enumerate(tasksDetail):
            taskMc = self.widget.getInstByClsName('FtbExcavateAbility_guideDetailItem')
            taskMc.name = self.TASK_NAME_PREFIX + str(i)
            taskMc.y = self.__genTaskPistion(i)
            itemMc.addChild(taskMc)
            taskMc.gotoAndStop('finished' if detail['isDone'] else 'unfinished')
            taskMc.value.text = self.__genValueRangeStr(detail['valueRange'])
            taskMc.taskName.text = detail['taskName']

        itemMc.addEventListener(events.MOUSE_UP, self._handleGuideItemExpend, False, 0, True)

    def _guideItemHeightFunc(self, *args):
        info = ASObject(args[3][0])
        for data in self.leftListDataArray:
            tpye = data.get('taskType', -1)
            if tpye == info.taskType:
                isExpand = data.get('isExpand', False)
                tasks = FPCRD.data.get(tpye, [])
                if tpye == self.HOME_RICH_VALUE_TYPE:
                    withoutTip = self.__genItemWithoutTipHeight(2)
                else:
                    withoutTip = self.__genItemWithoutTipHeight(len(tasks))
                tipHeight = self.__genTipHeight(tpye)
                if isExpand:
                    return GfxValue(withoutTip + tipHeight)
                return GfxValue(withoutTip)

        return GfxValue(self.BG_HEIGHT)

    def _validityItemRenderFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.select.visible = False
        taskName = itemData.taskName
        value = itemData.value
        expire = itemData.expire
        itemMc.questName.text = taskName
        itemMc.value.text = str(int(value))
        itemMc.deadline.text = self.__genDeadlineTimeStr(expire)
        itemMc.addEventListener(events.MOUSE_CLICK, self._handleRightListClick, False, 0, True)

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE_ABILITY, events.EVNET_FTB_DIGPOWER_CHANGE)
    def onDigPowerChange(self, event):
        baseDigPower = FCD.data.get('basePower', 30)
        p = BigWorld.player()
        self._refreshAbility(baseDigPower, p.ftbDataDetail.guideDigPower, p.ftbDataDetail.ephemeralPower)

    @ui.uiEvent(uiConst.WIDGET_FTB_EXCAVATE_ABILITY, events.EVNET_FTB_DIGPOWERTASK_CHANGE)
    def onDigPowerTaskChange(self, event):
        self._refreshTaskList()

    def _refreshAbility(self, baseAbility, guideAbility, ephemeralPower):
        if not self.widget:
            return
        self.widget.baseAbility.text = str(baseAbility)
        self.widget.guideAbility.text = str(guideAbility + ephemeralPower)
        self.widget.totalAbility.text = str(baseAbility + guideAbility + ephemeralPower)

    def _refreshTaskList(self):
        if not self.widget:
            return
        if self.widget.validityPanel.visible:
            self.rightListDataArray = self._genRightListDataArray()
            self.__refreshRightList()
        elif self.widget.guidePanel.visible:
            self.leftListDataArray = self._genLeftListDataArray()
            self.__refreshLeftList()

    def __refreshLeftList(self):
        self.widget.guidePanel.dataArray = self.leftListDataArray
        self.widget.validityPanel.list.validateNow()

    def __refreshRightList(self):
        self.rightListSelectedItem = None
        self.widget.validityPanel.list.dataArray = self.rightListDataArray
        self.widget.validityPanel.list.validateNow()

    def _changeTab(self, btnName):
        if not self.widget:
            return
        if self.selectTab == btnName:
            return
        self.selectTab = btnName
        if btnName == self.widget.guideTabBtn.name:
            self.widget.validityTabBtn.selected = False
            self.widget.guideTabBtn.selected = True
            self.widget.validityPanel.visible = False
            self.widget.guidePanel.visible = True
        elif btnName == self.widget.validityTabBtn.name:
            self.widget.validityTabBtn.selected = True
            self.widget.guideTabBtn.selected = False
            self.widget.validityPanel.visible = True
            self.widget.guidePanel.visible = False
        self._refreshTaskList()

    def _genLeftListDataArray(self):
        p = BigWorld.player()
        doneTaskList = p.ftbDataDetail.todayTaskList
        dataDict = {}
        allHomeRichInfo = []
        for taskType, taskIds in FPCRD.data.iteritems():
            if taskType == gametypes.FTB_TASK_TYPE_ACTIVITY:
                continue
            typeConfig = FTTD.data.get(taskType, {})
            duration = typeConfig.get('duration', -1)
            typeName = typeConfig.get('typeName', '')
            typeDesc = typeConfig.get('typeDesc', '')
            dataDict[taskType] = {'taskType': taskType,
             'tasksDetail': [],
             'duration': duration,
             'typeName': typeName,
             'typeDesc': typeDesc,
             'isExpand': False}
            if taskType == self.HOME_RICH_VALUE_TYPE:
                for tid in taskIds:
                    weathLv = FPCD.data.get(tid, {}).get('weathLv', '')
                    valueRange = FPCD.data.get(tid, {}).get('valueRange', 0)
                    taskName = FPCD.data.get(tid, {}).get('taskName', '')
                    allHomeRichInfo.append({'weathLv': weathLv,
                     'valueRange': valueRange,
                     'taskId': tid,
                     'taskName': taskName})

            else:
                for tid in taskIds:
                    taskName = FPCD.data.get(tid, {}).get('taskName', '')
                    valueRange = FPCD.data.get(tid, {}).get('valueRange', 0)
                    dataDict[taskType]['tasksDetail'].append({'taskId': tid,
                     'isDone': False,
                     'taskName': taskName,
                     'valueRange': valueRange})

        maxHomeLv = 1
        richSum = 0
        for doneTask in doneTaskList:
            id = doneTask.get('taskId', -1)
            id = ftbUtils.getShowTaskId(id)
            if not id:
                continue
            value = doneTask.get('value', 0)
            tType = FPCD.data.get(id, {}).get('taskType', -1)
            if tType in dataDict:
                if tType == self.HOME_RICH_VALUE_TYPE:
                    maxHomeLv = max(maxHomeLv, FPCD.data.get(id, {}).get('weathLv', 1))
                    richSum += value
                else:
                    for detail in dataDict[tType]['tasksDetail']:
                        if detail['taskId'] == id:
                            if detail['isDone']:
                                detail['valueRange'] += value
                            else:
                                detail['valueRange'] = value
                                detail['isDone'] = True

        allHomeRichInfo.sort(key=lambda x: x['weathLv'])
        homeRichDetails = []
        for i, info in enumerate(allHomeRichInfo):
            weathLv = info['weathLv']
            taskId = info['taskId']
            taskName = info['taskName']
            if weathLv >= maxHomeLv:
                homeRichDetails.append({'taskId': taskId,
                 'isDone': True,
                 'taskName': gameStrings.FTB_HOME_RICH_CURLV % taskName,
                 'valueRange': richSum})
                if i + 1 < len(allHomeRichInfo):
                    nextValueRange = allHomeRichInfo[i + 1]['valueRange']
                    nextTaskId = allHomeRichInfo[i + 1]['taskId']
                    nextTaskName = allHomeRichInfo[i + 1]['taskName']
                    homeRichDetails.append({'taskId': nextTaskId,
                     'isDone': False,
                     'taskName': gameStrings.FTB_HOME_RICH_NEXTLV % nextTaskName,
                     'valueRange': richSum + nextValueRange[0]})
                break

        dataDict[self.HOME_RICH_VALUE_TYPE]['tasksDetail'] = homeRichDetails
        sortKeys = dataDict.keys()
        sortKeys.sort()
        return [ dataDict[k] for k in sortKeys ]

    def _genRightListDataArray(self):
        p = BigWorld.player()
        doneTaskList = p.ftbDataDetail.historyTaskList
        dataArray = []
        homeRichSum = 0
        for taskInfo in doneTaskList:
            id = taskInfo.get('taskId', -1)
            id = ftbUtils.getShowTaskId(id)
            if not id:
                continue
            tpye = FPCD.data.get(id, {}).get('taskType', 0)
            value = taskInfo.get('value', 0)
            if tpye == self.HOME_RICH_VALUE_TYPE:
                homeRichSum += value

        for taskInfo in doneTaskList:
            id = taskInfo.get('taskId', -1)
            id = ftbUtils.getShowTaskId(id)
            if not id:
                continue
            expired = taskInfo.get('expired', 0)
            value = taskInfo.get('value', 0)
            tpye = FPCD.data.get(id, {}).get('taskType', 0)
            taskName = FPCD.data.get(id, {}).get('taskName', '')
            if tpye == self.HOME_RICH_VALUE_TYPE:
                continue
            dataArray.append({'taskName': taskName,
             'expire': expired,
             'value': value})

        if homeRichSum > 0:
            dataArray.append({'taskName': FTTD.data.get(self.HOME_RICH_VALUE_TYPE, {}).get('typeName', ''),
             'expire': const.MAX_TIME,
             'value': homeRichSum})
        dataArray.sort(key=lambda x: x['expire'], reverse=True)
        return dataArray

    def __genItemWithoutTipHeight(self, subItemNum):
        return self.BG_HEIGHT + max(0, subItemNum - 1) * (self.TASK_HEIGHT + self.TASK_INTERVAL)

    def __genTipHeight(self, taskType):
        desc = FTTD.data.get(taskType, {}).get('typeDesc', '')
        lines = desc.split('\n')
        return len(lines) * self.TIP_TEXT_HEIGHT_PRE_LINE + self.TIP_BG_HEIGHT_ADD

    def __genExpireTxtPosition(self, subItemNum):
        y = max(subItemNum, 1) * self.TASK_HEIGHT
        y += max(subItemNum - 1, 0) * self.TASK_INTERVAL
        y = (y - self.EXPIRE_TXT_HEIGHT) / 2
        return self.TASK_Y_START + y

    def __genTaskPistion(self, index):
        return self.TASK_Y_START + max(index, 0) * (self.TASK_HEIGHT + self.TASK_INTERVAL)

    def __genDeadlineTimeStr(self, deadline):
        if int(deadline) == const.MAX_TIME:
            return gameStrings.COMMON_INFINITE_TIME_LONG
        else:
            return time.strftime('%Y-%m-%d  %H:%M', time.localtime(float(deadline)))

    def __clearAllTask(self, itemMc):
        if not itemMc:
            return
        waitRemove = []
        for i in xrange(itemMc.numChildren):
            child = itemMc.getChildAt(i)
            if child and child.name.startswith(self.TASK_NAME_PREFIX):
                waitRemove.append(child)

        for child in waitRemove:
            self.widget.removeToCache(child)

    def __genValueRangeStr(self, valueRange):
        if type(valueRange) in (tuple, list):
            if len(valueRange) == 2:
                if valueRange[0] < valueRange[1]:
                    return '%d-%d' % (int(valueRange[0]), int(valueRange[1]))
                if valueRange[0] == valueRange[1]:
                    return '%d' % int(valueRange[0])
            elif len(valueRange) == 1:
                return '%d' % int(valueRange[0])
        elif type(valueRange) is int:
            return '%d' % valueRange
        return ''
