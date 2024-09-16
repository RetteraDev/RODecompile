#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/messageBoardSendProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import uiUtils
from callbackHelper import Functor
from guis import uiConst
from guis import ui
from guis.ui import unicode2gbk
from guis.uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class MessageBoardSendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MessageBoardSendProxy, self).__init__(uiAdapter)
        self.modelMap = {'getBasicInfo': self.onGetBasicInfo,
         'getFBData': self.onGetFBData,
         'confirm': self.onConfirm,
         'getType': self.getType,
         'getWeekSelect': self.getWeekSelect}
        self.mediator = None
        self.reset()
        self.stype = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_MESSAGEBOARD_SEND, self.clearWidget)

    def reset(self):
        self.stype = 0

    def getType(self, *args):
        return GfxValue(self.stype)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MESSAGEBOARD_SEND:
            self.mediator = mediator

    def getWeekSelect(self, *args):
        return gameglobal.rds.ui.messageBoard.getWeekSelect()

    def show(self, type = 0):
        self.stype = type
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MESSAGEBOARD_SEND)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.messageBoard.nowFocusGbId = 0
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MESSAGEBOARD_SEND)

    def onGetBasicInfo(self, *args):
        return gameglobal.rds.ui.messageBoard.onGetBasicInfo(*args)

    def onGetFBData(self, *args):
        fbData = gameglobal.rds.ui.messageBoard.getFbData()
        return uiUtils.dict2GfxDict(fbData, True)

    @ui.callFilter(3)
    def onConfirm(self, *args):
        fbNo = int(args[3][0].GetNumber())
        hard = int(args[3][1].GetNumber())
        numsStr = args[3][2].GetNumber()
        hasNumsStr = args[3][3].GetString()
        dayList = []
        arrSize = args[3][4].GetArraySize()
        arrNum = 0
        for i in xrange(arrSize):
            ret = args[3][4].GetElement(i).GetBool()
            if ret:
                arrNum = arrNum + 1
                dayList.append(i)

        startTime0 = int(args[3][5].GetNumber())
        instruction = unicode2gbk(args[3][6].GetString())
        if startTime0 == -1 or arrNum == 0 or numsStr == '' or hasNumsStr == '' or fbNo == -1 or hard == -1:
            hintTxt = uiUtils.getTextFromGMD(GMDD.data.BOARD_NEED_MORE_INFOMATION, '请完整填写必填项')
            gameglobal.rds.ui.messageBox.showMsgBox(hintTxt)
            return
        timeArray = ['6:0-11:59', '12:0-18:59', '19:0-5:59']
        timeStr = timeArray[startTime0]
        nums = int(numsStr)
        hasNums = int(hasNumsStr)
        if hasNums >= nums:
            hintTxt = uiUtils.getTextFromGMD(GMDD.data.BOARD_NEED_CORRECT_NUMS, '已有人数超过副本人数')
            gameglobal.rds.ui.messageBox.showMsgBox(hintTxt)
            return
        if self.stype != 1:
            if hasNums > nums / 2:
                txt = '你队伍中有较多队友，建议您尝试成立自己的队伍并招募队友'
                func1 = Functor(BigWorld.player().cell.publishFbMessageNotice, gametypes.FB_PUBLISH_TYPE_ACCEPT, fbNo, hard, hasNums, dayList, timeStr, instruction, nums)
                func2 = Functor(BigWorld.player().cell.publishFbMessageNotice, gametypes.FB_PUBLISH_TYPE_APPLY, fbNo, hard, hasNums, dayList, timeStr, instruction, nums)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, func1, '招募队员', func2, '坚持求组')
                return
        elif hasNums < nums / 2:
            txt = '你队伍中队友较少，建议您尝试发布自己的消息，并求组弑神'
            func1 = Functor(BigWorld.player().cell.publishFbMessageNotice, gametypes.FB_PUBLISH_TYPE_APPLY, fbNo, hard, hasNums, dayList, timeStr, instruction, nums)
            func2 = Functor(BigWorld.player().cell.publishFbMessageNotice, gametypes.FB_PUBLISH_TYPE_ACCEPT, fbNo, hard, hasNums, dayList, timeStr, instruction, nums)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, func1, '求组弑神', func2, '坚持招募')
            return
        if self.stype == 1:
            BigWorld.player().cell.publishFbMessageNotice(gametypes.FB_PUBLISH_TYPE_ACCEPT, fbNo, hard, hasNums, dayList, timeStr, instruction, nums)
        else:
            BigWorld.player().cell.publishFbMessageNotice(gametypes.FB_PUBLISH_TYPE_APPLY, fbNo, hard, hasNums, dayList, timeStr, instruction, nums)
