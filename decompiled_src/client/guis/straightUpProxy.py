#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/straightUpProxy.o
import BigWorld
import gametypes
import gameglobal
import uiConst
import clientUtils
from guis import events
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import straight_up_task_data as SUTD
from data import sys_config_data as SCD
MAX_ITEM_NUM = 3

class StraightUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(StraightUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_STRAIGHT_UP, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_STRAIGHT_UP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_STRAIGHT_UP)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_STRAIGHT_UP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def checkRedPointVisible(self):
        p = BigWorld.player()
        straightUpTask = getattr(p, 'straightUpTask', {})
        for taskInfo in straightUpTask.values():
            if taskInfo.get('state', gametypes.STRAIGHT_TASK_STATE_DEFAULT) == gametypes.STRAIGHT_TASK_STATE_ENABLE:
                return True

        return False

    def checkTaskUnfinished(self):
        p = BigWorld.player()
        straightUpTask = getattr(p, 'straightUpTask', {})
        for taskInfo in straightUpTask.values():
            if taskInfo.get('state', gametypes.STRAIGHT_TASK_STATE_DEFAULT) == gametypes.STRAIGHT_TASK_STATE_DEFAULT:
                return True

        return False

    def isNeedShow(self):
        p = BigWorld.player()
        straightUpTask = getattr(p, 'straightUpTask', {})
        for taskInfo in straightUpTask.values():
            if taskInfo.get('state', gametypes.STRAIGHT_TASK_STATE_DEFAULT) != gametypes.STRAIGHT_TASK_STATE_TAKEN:
                return True

        return False

    def getTaskListInfo(self):
        p = BigWorld.player()
        straightUpTask = getattr(p, 'straightUpTask', {})
        taskGroupTitles = SCD.data.get('straightGroupTitle', {})
        taskListInfo = {}
        for taskId in straightUpTask.keys():
            taskInfo = SUTD.data.get(taskId, {})
            groupId = taskInfo.get('groupId', -1)
            if not taskListInfo.has_key(groupId):
                taskListInfo[groupId] = []
            taskListInfo[groupId].append(taskId)

        ret = []
        groupKeys = taskListInfo.keys()
        groupKeys.sort()
        for groupId in groupKeys:
            tasks = taskListInfo.get(groupId, [])
            tasks.sort()
            ret.append({'title': taskGroupTitles.get(groupId, ''),
             'tasks': tasks})

        return ret

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshTasks()

    def refreshTasks(self):
        canvas = self.widget.questList.canvas
        self.removeAllChild(canvas)
        currY = 0
        listInfo = self.getTaskListInfo()
        for info in listInfo:
            titleMc = self.widget.getInstByClsName('StraightUp_title')
            titleMc.textField.text = info.get('title', '')
            canvas.addChild(titleMc)
            titleMc.y = currY
            currY += titleMc.height
            taskIds = info.get('tasks', ())
            for taskId in taskIds:
                taskMc = self.widget.getInstByClsName('StraightUp_questItem')
                self.setTaskInfo(taskMc, taskId)
                canvas.addChild(taskMc)
                taskMc.y = currY
                currY += taskMc.height

    def setTaskInfo(self, taskMc, taskId):
        p = BigWorld.player()
        straightUpTask = getattr(p, 'straightUpTask', {})
        taskInfo = SUTD.data.get(taskId, {})
        taskState = straightUpTask.get(taskId, {}).get('state', gametypes.STRAIGHT_TASK_STATE_DEFAULT)
        taskMc.gotoBtn.visible = taskState == gametypes.STRAIGHT_TASK_STATE_DEFAULT
        taskMc.confirmBtn.visible = taskState == gametypes.STRAIGHT_TASK_STATE_ENABLE
        taskMc.finishBtn.visible = taskState == gametypes.STRAIGHT_TASK_STATE_TAKEN
        if taskInfo.get('clickFunc', ''):
            taskMc.gotoBtn.label = taskInfo.get('clickLabel', gameStrings.PLAY_RECOMM_WEEK_ACTIVATION_GOTO)
            taskMc.gotoBtn.taskId = taskId
            taskMc.gotoBtn.addEventListener(events.BUTTON_CLICK, self.onGotoBtnClick)
        else:
            taskMc.gotoBtn.removeEventListener(events.BUTTON_CLICK, self.onGotoBtnClick)
            taskMc.gotoBtn.visible = False
        taskMc.confirmBtn.taskId = taskId
        taskMc.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirmBtnClick)
        bonusID = taskInfo.get('bonusID', 0)
        itemList = clientUtils.genItemBonus(bonusID)
        for i in xrange(MAX_ITEM_NUM):
            slotMc = taskMc.getChildByName('slot%d' % i)
            if i < len(itemList):
                itemId, num = itemList[i]
                itemInfo = uiUtils.getGfxItemById(itemId, num)
                slotMc.visible = True
                slotMc.setItemSlotData(itemInfo)
            else:
                slotMc.visible = False

        desc = taskInfo.get('desc', '')
        taskMc.content.htmlText = uiUtils.toHtml(desc, color=taskMc.content.textColor, fontSize=12)
        if taskMc.content.textWidth > taskMc.content.width:
            taskMc.content.htmlText = uiUtils.toHtml(desc, color=taskMc.content.textColor, fontSize=11)
        varName = taskInfo.get('varName', '')
        currProgress = 0
        if varName:
            currProgress = p.statsInfo.get(varName, 0)
        currProgress = min(currProgress, taskInfo.get('totalProgress', 0))
        progressText = '(%d/%d)' % (currProgress, taskInfo.get('totalProgress', 0))
        taskMc.progress.text = progressText

    def onConfirmBtnClick(self, *args):
        e = ASObject(args[3][0])
        taskId = e.currentTarget.taskId
        p = BigWorld.player()
        p.base.takeStraightTaskReward(taskId)

    def onGotoBtnClick(self, *args):
        e = ASObject(args[3][0])
        taskId = e.currentTarget.taskId
        taskInfo = SUTD.data.get(taskId, {})
        linkFunc = taskInfo.get('clickFunc', '')
        if linkFunc:
            gameglobal.rds.ui.doLinkClick(linkFunc, 0)

    def removeAllChild(self, canvasMc):
        while canvasMc.numChildren > 0:
            canvasMc.removeChildAt(0)
