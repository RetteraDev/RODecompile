#Embedded file name: /WORKSPACE/data/entities/client/guis/messageboardproxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import uiUtils
import const
import time
import json
import os
import utils
from guis import ui
from helpers import taboo
from helpers.messageBoard import FbMessageBoard
from callbackHelper import Functor
from guis import uiConst
from guis.ui import gbk2unicode
from guis.ui import unicode2gbk
from guis.uiProxy import UIProxy
from data import sys_config_data as SCD
from data import fb_message_board_data as FMBD
from data import message_board_combatscore_data as MBCD
from cdata import game_msg_def_data as GMDD

class MessageBoardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MessageBoardProxy, self).__init__(uiAdapter)
        self.modelMap = {'getBasicInfo': self.onGetBasicInfo,
         'getHasOutMsg': self.onGetHasOutMsg,
         'getFBData': self.onGetFBData,
         'getCurrentSetInfo': self.getCurrentSetInfo,
         'getSelfMsgList': self.onGetSelfMsgList,
         'queryMsgBoard': self.onQueryMsgBoard,
         'sendMsg': self.chatToMsgBoard,
         'getShowTitle': self.getShowTitle,
         'refreshSelfFocus': self.refreshSelfFocus,
         'modifyMyInfo': self.onModifyMyInfo,
         'challageFbMessageBoardPublishType': self.onChallageFbMessageBoardPublishType,
         'discardFbMessageNotice': self.discardFbMessageNotice,
         'chatToSomeOne': self.chatToSomeOne,
         'focusToSomeOne': self.focusToSomeOne,
         'cancelFocusToSomeOne': self.cancelFocusToSomeOne,
         'showSendView': self.showSendView,
         'getLeftTimes': self.getLeftTimes,
         'getWeekSelect': self.getWeekSelect}
        self.mediator = None
        self.reset()
        self.fbDict = {}
        self.callback = [None, None]
        self.refreshMessageCallBack = None
        self.tempFriendAddList = []
        self.clearTempFriendCallBack = None
        self.nowFocusGbId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_MESSAGEBOARD, self.clearWidget)

    def getWeekSelect(self, *args):
        week = int(time.strftime('%w'))
        if week == 7:
            week = 0
        return GfxValue(week)

    def showSendView(self, *args):
        targetId = int(args[3][0].GetNumber())
        gameglobal.rds.ui.messageBoardSend.show(targetId)

    def getLeftTimes(self, *args):
        p = BigWorld.player()
        typeId = int(args[3][0].GetNumber())
        if typeId == 0:
            cdStr = 'queryMessageBoardTime'
            cdTime = 15
        else:
            cdStr = 'sendMessageBoardChatTime'
            cdTime = 60
        beTime = getattr(p, cdStr, 0)
        now = time.time()
        passTime = int(now - beTime)
        if passTime > cdTime:
            if typeId == 0:
                return GfxValue(gbk2unicode('可刷新'))
            else:
                return GfxValue(gbk2unicode('可发送'))
        else:
            leftTime = cdTime - passTime
            return GfxValue(gbk2unicode('剩余%d秒' % leftTime))

    def setRefreshTime(self, type = 0):
        if not self.mediator:
            return
        if type == 0:
            attrName = 'queryMessageBoardTime'
            cdTime = 15
            setFuncName = 'setRefreshEnable'
        else:
            attrName = 'sendMessageBoardChatTime'
            cdTime = 60
            setFuncName = 'setInputMsgEnable'
        p = BigWorld.player()
        beTime = getattr(p, attrName, 0)
        now = time.time()
        leftTime = now - beTime
        if self.callback[type]:
            BigWorld.cancelCallback(self.callback[type])
            self.callback[type] = None
        if leftTime >= cdTime:
            self.mediator.Invoke(setFuncName, GfxValue(True))
        else:
            self.mediator.Invoke(setFuncName, GfxValue(False))
            self.callback[type] = BigWorld.callback(cdTime - leftTime, Functor(self.setRefreshTime, type))

    def getFbData(self):
        p = BigWorld.player()
        self.fbDict = {}
        orderList = {}
        for fbId in FMBD.data:
            data = FMBD.data[fbId]
            if data.get('lv'):
                if p.lv < data.get('lv'):
                    continue
            orderList[data['order']] = fbId
            self.fbDict.setdefault(gbk2unicode(data['name']), [])
            self.fbDict[gbk2unicode(data['name'])].append({'num': data['num'],
             'type': data['type'],
             'fbId': fbId})

        lst = orderList.keys()
        lst.sort()
        for fbIdOrder in lst:
            fbId = orderList[fbIdOrder]
            data = FMBD.data[fbId]
            self.fbDict.setdefault('fbNameList', [])
            if data['name'] not in self.fbDict['fbNameList']:
                self.fbDict['fbNameList'].append(data['name'])

        return self.fbDict

    def reset(self):
        pass

    def refreshWidget(self):
        if self.mediator:
            self.mediator.Invoke('refreshWidget', ())

    @ui.callFilter(3)
    def chatToSomeOne(self, *args):
        isShowFocus = False
        if hasattr(BigWorld.player(), 'fbMessageBoard') and BigWorld.player().fbMessageBoard != None:
            isShowFocus = BigWorld.player().fbMessageBoard.publishType
        if isShowFocus:
            name = unicode2gbk(args[3][0].GetString())
            self.chatToPlayer(name)
        else:
            self.hintToAddMsg(1)

    def chatToPlayer(self, name):
        fid = self.findNameInFriend(name)
        if fid != -1:
            gameglobal.rds.ui.friend.beginChat(fid)
        else:
            p = BigWorld.player()
            if p:
                p.base.addContact(name, gametypes.FRIEND_GROUP_TEMP, 0)
                self.tempFriendAddList.append(name)
                self.resetAddTempCallBack()
                self.clearTempFriendCallBack = BigWorld.callback(5, self.clearTempCallBack)

    def resetAddTempCallBack(self):
        if self.clearTempFriendCallBack:
            BigWorld.cancelCallback(self.clearTempFriendCallBack)
            self.clearTempFriendCallBack = None

    def clearTempCallBack(self):
        self.tempFriendAddList = []

    def onTempFriendAdded(self, name, fid):
        for i in xrange(len(self.tempFriendAddList)):
            if self.tempFriendAddList[i] == name:
                self.tempFriendAddList.pop(i)
                gameglobal.rds.ui.friend.beginChat(fid)
                return

        self.resetAddTempCallBack()

    def findNameInFriend(self, name):
        for gbId in BigWorld.player().friend:
            if BigWorld.player().friend[gbId].name == name:
                return gbId

        return -1

    @ui.callFilter(3)
    def focusToSomeOne(self, *args):
        isShowFocus = False
        if hasattr(BigWorld.player(), 'fbMessageBoard') and BigWorld.player().fbMessageBoard != None:
            isShowFocus = BigWorld.player().fbMessageBoard.publishType
        gbId = int(args[3][0].GetString())
        if isShowFocus:
            p = BigWorld.player()
            data = p.fbMessageBoard.connections.get(gbId, {})
            if data:
                itemType = data.itemType
            else:
                itemType = 0
            if itemType == gametypes.FB_MESSAGE_BOARD_CONNECTION_TYPE_ACKONWLEDGE:
                BigWorld.player().cell.abortFbConnection(gbId)
            elif itemType == gametypes.FB_MESSAGE_BOARD_CONNECTION_TYPE_APPLY:
                BigWorld.player().cell.acceptFbConnection(gbId)
            elif itemType == gametypes.FB_MESSAGE_BOARD_CONNECTION_TYPE_APPLIED:
                BigWorld.player().cell.cancelFbConnection(gbId)
            else:
                BigWorld.player().cell.applyBuildFbConnection(gbId)
        else:
            self.hintToAddMsg(0, gbId)

    @ui.callFilter(3)
    def cancelFocusToSomeOne(self, *args):
        isShowFocus = False
        if hasattr(BigWorld.player(), 'fbMessageBoard') and BigWorld.player().fbMessageBoard != None:
            isShowFocus = BigWorld.player().fbMessageBoard.publishType
        if isShowFocus:
            gbId = int(args[3][0].GetString())
            BigWorld.player().cell.ignoreFbConnection(gbId)

    def hintToAddMsg(self, type, gbId = 0):
        isUseTempMsg = self.isUseTempMsg()
        if not isUseTempMsg:
            if type == 0:
                msgText = '您还没登记过您的个人信息，请先填写您的相关资料，然后可关注该弑神队伍'
            else:
                msgText = '您还没登记过您的个人信息，请先填写您的相关资料,然后可使用该功能'
            yesBtnText = '马上填写'
        else:
            if type == 0:
                msgText = '您还没发布您的个人信息，请先发布您的相关资料，然后可关注该弑神队伍'
            else:
                msgText = '您还没发布您的个人信息，请先发布您的相关资料,然后可使用该功能'
            yesBtnText = '马上发布'
        if type == 0:
            noBtnText = '暂不关注'
        else:
            noBtnText = '暂不联系'
        if not isUseTempMsg:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgText, Functor(self.messageBoardSendShow, gbId), yesBtnText=yesBtnText, noBtnText=noBtnText, isModal=False)
        else:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgText, Functor(self.messageBoardTempApply, gbId), yesBtnText=yesBtnText, noBtnText=noBtnText, isModal=False)

    def messageBoardTempApply(self, gbId):
        self.nowFocusGbId = gbId
        p = BigWorld.player()
        fbNo = p.tempFbMessageBoard.fbNo
        hard = p.tempFbMessageBoard.hard
        hasNums = p.tempFbMessageBoard.hasNum
        dayList = p.tempFbMessageBoard.challengeWeekList
        timeStr = p.tempFbMessageBoard.challengeTimeStr
        instruction = p.tempFbMessageBoard.desc
        nums = p.tempFbMessageBoard.num
        self.applyTempInfo(fbNo, hard, nums, hasNums, dayList, timeStr, instruction)

    def messageBoardSendShow(self, gbId):
        gameglobal.rds.ui.messageBoardSend.show()
        self.nowFocusGbId = gbId

    def onPublishSucc(self):
        self.refreshWidget()
        if self.nowFocusGbId:
            msgText = uiUtils.getTextFromGMD(GMDD.data.MESSAGEBOARD_FOCUS_BEFORE_TEAM, '是否要关注之前你选择的那支队伍')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgText, Functor(self.focusToBefore, self.nowFocusGbId))

    def focusToBefore(self, gbId):
        isShowFocus = False
        if hasattr(BigWorld.player(), 'fbMessageBoard') and BigWorld.player().fbMessageBoard != None:
            isShowFocus = BigWorld.player().fbMessageBoard.publishType
        if isShowFocus:
            p = BigWorld.player()
            data = p.fbMessageBoard.connections.get(gbId, {})
            if data:
                itemType = data.itemType
            else:
                itemType = 0
            if itemType == gametypes.FB_MESSAGE_BOARD_CONNECTION_TYPE_ACKONWLEDGE:
                BigWorld.player().cell.abortFbConnection(gbId)
            elif itemType == gametypes.FB_MESSAGE_BOARD_CONNECTION_TYPE_APPLY:
                BigWorld.player().cell.acceptFbConnection(gbId)
            elif itemType == gametypes.FB_MESSAGE_BOARD_CONNECTION_TYPE_APPLIED:
                BigWorld.player().cell.cancelFbConnection(gbId)
            else:
                BigWorld.player().cell.applyBuildFbConnection(gbId)
        self.nowFocusGbId = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MESSAGEBOARD:
            self.mediator = mediator

    def show(self):
        yuyueLv = SCD.data.get('YU_YUE_LIMIT_LV', 45)
        if BigWorld.player().lv < yuyueLv:
            BigWorld.player().showGameMsg(GMDD.data.YU_YUE_LIMIT_LV, ())
            return
        if not self.isUseTempMsg():
            self.readTempBoardMessage()
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MESSAGEBOARD)

    @ui.callFilter(20)
    def onChallageFbMessageBoardPublishType(self, *args):
        p = BigWorld.player()
        if not self.isUseTempMsg():
            if not hasattr(p, 'fbMessageBoard') or p.fbMessageBoard == None or p.fbMessageBoard.publishType == 0:
                return
            fbMessageBoard = p.fbMessageBoard
            if fbMessageBoard.publishType == gametypes.FB_PUBLISH_TYPE_APPLY:
                pType = gametypes.FB_PUBLISH_TYPE_ACCEPT
            else:
                pType = gametypes.FB_PUBLISH_TYPE_APPLY
            p.cell.changeFbMessageBoardPublishType(pType)
        else:
            fbMessageBoard = p.tempFbMessageBoard
            if fbMessageBoard.publishType == gametypes.FB_PUBLISH_TYPE_APPLY:
                p.tempFbMessageBoard.publishType = gametypes.FB_PUBLISH_TYPE_ACCEPT
            else:
                p.tempFbMessageBoard.publishType = gametypes.FB_PUBLISH_TYPE_APPLY
            self.refreshWidget()
            BigWorld.player().showGameMsg(GMDD.data.MMESSAGE_BOARD_EVENT_UPDATE_NO_PUBLISH_MSG_SUCC, ())
            self.saveTempBoardMessage()

    @ui.callFilter(3)
    def discardFbMessageNotice(self, *args):
        p = BigWorld.player()
        if not self.isUseTempMsg():
            if not hasattr(p, 'fbMessageBoard') or p.fbMessageBoard == None or p.fbMessageBoard.publishType == 0:
                return
            msgShow = '是否要撤销发布，撤销后会取消所有关注状态'
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msgShow, p.cell.discardFbMessageNotice)
        else:
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
            self.applyTempInfo(fbNo, hard, nums, hasNums, dayList, timeStr, instruction)

    def applyTempInfo(self, fbNo, hardId, nums, hasNums, dayList, timeStr, instruction):
        if hasNums >= nums:
            hintTxt = uiUtils.getTextFromGMD(GMDD.data.BOARD_NEED_CORRECT_NUMS, '已有人数超过副本人数')
            gameglobal.rds.ui.messageBox.showMsgBox(hintTxt)
            return
        if BigWorld.player().tempFbMessageBoard.publishType == 1:
            if hasNums > nums / 2:
                txt = '你队伍中有较多队友，建议您尝试成立自己的队伍并招募队友'
                func1 = Functor(BigWorld.player().cell.publishFbMessageNotice, gametypes.FB_PUBLISH_TYPE_ACCEPT, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)
                func2 = Functor(BigWorld.player().cell.publishFbMessageNotice, gametypes.FB_PUBLISH_TYPE_APPLY, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, func1, '招募队员', func2, '坚持求组')
                return
        elif hasNums < nums / 2:
            txt = '你队伍中队友较少，建议您尝试发布自己的消息，并求组弑神'
            func1 = Functor(BigWorld.player().cell.publishFbMessageNotice, gametypes.FB_PUBLISH_TYPE_APPLY, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)
            func2 = Functor(BigWorld.player().cell.publishFbMessageNotice, gametypes.FB_PUBLISH_TYPE_ACCEPT, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, func1, '求组弑神', func2, '坚持招募')
            return
        if BigWorld.player().tempFbMessageBoard.publishType == 1:
            BigWorld.player().cell.publishFbMessageNotice(gametypes.FB_PUBLISH_TYPE_APPLY, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)
        else:
            BigWorld.player().cell.publishFbMessageNotice(gametypes.FB_PUBLISH_TYPE_ACCEPT, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)

    def clearWidget(self):
        self.mediator = None
        self.resetCallBack()
        self.clearTempCallBack()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MESSAGEBOARD)

    def resetCallBack(self):
        if self.refreshMessageCallBack:
            BigWorld.cancelCallback(self.refreshMessageCallBack)
            self.refreshMessageCallBack = None

    def setRefreshMsgCallBack(self):
        self.resetCallBack()
        self.refreshMessageCallBack = BigWorld.callback(SCD.data.get('MessageBoardRefreshTime', 60), self.queryBoardMsg)

    def queryBoardMsg(self):
        p = BigWorld.player()
        queryTime1 = getattr(p, 'queryMessageBoardChatTime', 0)
        now = time.time()
        if now - queryTime1 > 60:
            if hasattr(p, 'fbMessageBoard') and p.fbMessageBoard != None and p.fbMessageBoard.publishType != 0:
                version = getattr(p, 'messageBoardChatVersion', 0)
                p.cell.queryFbMessageBoardMsgs(version)
                p.queryMessageBoardChatTime = time.time()
        self.setRefreshMsgCallBack()

    def onGetBasicInfo(self, *args):
        p = BigWorld.player()
        info = {}
        info['playerName'] = p.playerName
        info['school'] = const.SCHOOL_DICT[p.school]
        info['otherName'], style = self._getShowTitleStyle()
        info['lv'] = p.lv
        info['guildName'] = p.guildName
        combatScoreList = BigWorld.player().combatScoreList
        allScore = combatScoreList[const.COMBAT_SCORE]
        info['combatScore'] = self.getScoreRegion(allScore)
        return uiUtils.dict2GfxDict(info, True)

    def getScoreRegion(self, score):
        for id in MBCD.data:
            startData = MBCD.data[id]['regionStart']
            endData = MBCD.data[id]['regionEnd']
            if score >= startData and score <= endData:
                return MBCD.data[id]['regionDisplay']

        return '400000以上'

    def getCurrentSetInfo(self, *args):
        info = {}
        p = BigWorld.player()
        fbMessageBoard = None
        useTempMsg = self.isUseTempMsg()
        if useTempMsg:
            fbMessageBoard = p.tempFbMessageBoard
        else:
            if not hasattr(p, 'fbMessageBoard') or p.fbMessageBoard == None or p.fbMessageBoard.publishType == 0:
                return uiUtils.dict2GfxDict(info, True)
            fbMessageBoard = p.fbMessageBoard
        info['hard'] = fbMessageBoard.hard
        info['fbNo'] = fbMessageBoard.fbNo
        info['dayCheckList'] = fbMessageBoard.challengeWeekList
        info['hasNum'] = fbMessageBoard.hasNum
        info['desc'] = fbMessageBoard.desc
        if not useTempMsg:
            if fbMessageBoard.publishType == gametypes.FB_PUBLISH_TYPE_APPLY:
                info['title'] = uiUtils.getTextFromGMD(GMDD.data.MESSAGEBOARD_SHISHEN_APPLY_TITLE, '你正在求组弑神队……')
                info['btnName'] = uiUtils.getTextFromGMD(GMDD.data.MESSAGEBOARD_SHISHEN_APPLY_BTN, '成立弑神队伍招募队员')
            else:
                info['title'] = uiUtils.getTextFromGMD(GMDD.data.MESSAGEBOARD_SHISHEN_INVITE_TITLE, '弑神队正在招募队员……')
                info['btnName'] = uiUtils.getTextFromGMD(GMDD.data.MESSAGEBOARD_SHISHEN_INVITE_BTN, '我想发布求组弑神队信息……')
            info['btnName2'] = '撤销'
        else:
            if fbMessageBoard.publishType == gametypes.FB_PUBLISH_TYPE_APPLY:
                info['title'] = uiUtils.getTextFromGMD(GMDD.data.MESSAGEBOARD_SHISHEN_APPLY_TITLE_NP, '求组弑神队……')
                info['btnName'] = uiUtils.getTextFromGMD(GMDD.data.MESSAGEBOARD_SHISHEN_APPLY_BTN_NP, '成立弑神队伍招募队员')
            else:
                info['title'] = uiUtils.getTextFromGMD(GMDD.data.MESSAGEBOARD_SHISHEN_INVITE_TITLE_NP, '弑神队招募队员……')
                info['btnName'] = uiUtils.getTextFromGMD(GMDD.data.MESSAGEBOARD_SHISHEN_INVITE_BTN_NP, '我想发布求组弑神队信息……')
            info['btnName2'] = '发布'
        data = FMBD.data[info['fbNo']]
        info['fbName'] = data['name']
        info['num'] = data['num']
        timeStr = fbMessageBoard.challengeTimeStr
        info['timeSelected'] = self.synTimeStrIndex(timeStr)
        return uiUtils.dict2GfxDict(info, True)

    def getTimeIndexText(self, timeStr):
        index = self.synTimeStrIndex(timeStr)
        timeArray = ['上午', '下午', '晚上']
        return timeArray[index]

    def synTimeStrIndex(self, timeStr):
        timeArr = timeStr.split('-')
        startTimeArr = timeArr[0].split(':')
        startTime0 = int(startTimeArr[0])
        timeSelected = 2
        if startTime0 > 5 and startTime0 < 12:
            timeSelected = 0
        elif startTime0 > 11 and startTime0 < 19:
            timeSelected = 1
        elif startTime0 > 18 or startTime0 < 6:
            timeSelected = 2
        return timeSelected

    def onGetFBData(self, *args):
        fbData = self.getFbData()
        return uiUtils.dict2GfxDict(fbData, True)

    def _getShowTitleStyle(self):
        name = ''
        style = 1
        if BigWorld.player():
            name, style = BigWorld.player().getActivateTitleStyle()
        if not name:
            name = ''
        return (name, style)

    def onGetHasOutMsg(self, *args):
        hasMsg = False
        if hasattr(BigWorld.player(), 'fbMessageBoard') and BigWorld.player().fbMessageBoard != None:
            hasMsg = BigWorld.player().fbMessageBoard.publishType
        if hasMsg:
            hasMsg = True
        else:
            if hasattr(BigWorld.player(), 'tempFbMessageBoard') and BigWorld.player().tempFbMessageBoard != None:
                hasMsg = BigWorld.player().tempFbMessageBoard.publishType
            if hasMsg:
                hasMsg = True
        return GfxValue(hasMsg)

    def isUseTempMsg(self):
        if hasattr(BigWorld.player(), 'fbMessageBoard') and BigWorld.player().fbMessageBoard != None:
            publishType = BigWorld.player().fbMessageBoard.publishType
            if publishType:
                return False
        if hasattr(BigWorld.player(), 'tempFbMessageBoard') and BigWorld.player().tempFbMessageBoard != None:
            publishType = BigWorld.player().tempFbMessageBoard.publishType
            if publishType:
                return True
        return False

    def onGetSelfMsgList(self, *args):
        ret = []
        p = BigWorld.player()
        if not hasattr(p, 'fbMessageBoard') or p.fbMessageBoard == None or p.fbMessageBoard.publishType == 0:
            return uiUtils.array2GfxAarry(ret, True)
        for event in p.fbMessageBoard.events:
            msgId = event.msgId
            args = event.args
            tWhen = event.tWhen
            msg = uiUtils.getTextFromGMD(msgId) % args
            timestr = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(tWhen))
            ret.append([msg, timestr])

        return uiUtils.array2GfxAarry(ret, True)

    def onQueryMsgBoard(self, *args):
        p = BigWorld.player()
        queryTime0 = getattr(p, 'queryMessageBoardTime', 0)
        queryTime1 = getattr(p, 'queryMessageBoardChatTime', 0)
        now = time.time()
        if now - queryTime0 > 15:
            version = getattr(p, 'messageBoardVersion', 0)
            p.cell.queryFbMessageBoardInfo(version)
            p.queryMessageBoardTime = time.time()
            self.setRefreshMsgCallBack()
        if now - queryTime1 > 60:
            if hasattr(p, 'fbMessageBoard') and p.fbMessageBoard != None and p.fbMessageBoard.publishType != 0:
                version = getattr(p, 'messageBoardChatVersion', 0)
                p.cell.queryFbMessageBoardMsgs(version)
                p.queryMessageBoardChatTime = time.time()
                self.resetCallBack()
        self.setRefreshTime()
        info = getattr(p, 'messageBoardInfo', [])
        self.setMessageBoardInfo(info)
        msgList = getattr(p, 'messageBoardMsgs', [])
        if msgList:
            self.setMessageBoardMsg(msgList)

    @ui.callFilter(3)
    def onModifyMyInfo(self, *args):
        fbNo = int(args[3][0].GetNumber())
        hardId = int(args[3][1].GetNumber())
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
        if startTime0 == -1 or arrNum == 0 or numsStr == '' or hasNumsStr == '' or fbNo == -1 or hardId == -1:
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
        p = BigWorld.player()
        if not self.isUseTempMsg():
            if p.fbMessageBoard.publishType == gametypes.FB_PUBLISH_TYPE_APPLY:
                if hasNums > nums / 2:
                    txt = '你队伍中有较多队友，建议您尝试成立自己的队伍并招募队友'
                    func1 = Functor(BigWorld.player().cell.updateFbMessageNotice, gametypes.FB_PUBLISH_TYPE_ACCEPT, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)
                    func2 = Functor(BigWorld.player().cell.updateFbMessageNotice, gametypes.FB_PUBLISH_TYPE_APPLY, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, func1, '招募队员', func2, '坚持求组')
                    return
            elif p.fbMessageBoard.publishType == gametypes.FB_PUBLISH_TYPE_ACCEPT:
                if hasNums < nums / 2:
                    txt = '你队伍中队友较少，建议您尝试发布自己的消息，并求组弑神'
                    func1 = Functor(BigWorld.player().cell.updateFbMessageNotice, gametypes.FB_PUBLISH_TYPE_APPLY, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)
                    func2 = Functor(BigWorld.player().cell.updateFbMessageNotice, gametypes.FB_PUBLISH_TYPE_ACCEPT, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, func1, '求组弑神', func2, '坚持招募')
                    return
            BigWorld.player().cell.updateFbMessageNotice(p.fbMessageBoard.publishType, fbNo, hardId, hasNums, dayList, timeStr, instruction, nums)
        else:
            p.tempFbMessageBoard.fbNo = fbNo
            p.tempFbMessageBoard.hard = hardId
            p.tempFbMessageBoard.hasNum = hasNums
            p.tempFbMessageBoard.challengeWeekList = dayList
            p.tempFbMessageBoard.challengeTimeStr = timeStr
            p.tempFbMessageBoard.desc = instruction
            p.tempFbMessageBoard.num = nums
            self.refreshWidget()
            BigWorld.player().showGameMsg(GMDD.data.MMESSAGE_BOARD_EVENT_UPDATE_NO_PUBLISH_MSG_SUCC, ())
            self.saveTempBoardMessage()

    def refreshSelfFocus(self, *args):
        infoList = []
        p = BigWorld.player()
        if not hasattr(p, 'fbMessageBoard') or p.fbMessageBoard == None or p.fbMessageBoard.publishType == 0:
            if self.mediator:
                self.mediator.Invoke('setFocusPlayerInfo', uiUtils.array2GfxAarry(infoList, True))
            return
        for gbId in p.fbMessageBoard.connections:
            itemInfo = {}
            data = p.fbMessageBoard.connections[gbId]
            itemInfo['roleName'] = data.roleName
            itemInfo['fbRestEnterTimes'] = data.fbRestEnterTimes
            itemInfo['fbMessageBoardInfo'] = {}
            itemInfo['fbMessageBoardInfo']['challengeWeekList'] = data.challengeWeekList
            itemInfo['fbMessageBoardInfo']['challengeTimeStr'] = data.challengeTimeStr
            itemInfo['combatPower'] = data.combatPower
            itemInfo['fbMessageBoardInfo']['desc'] = data.desc
            itemInfo['fbMessageBoardInfo']['fbNo'] = data.fbNo
            itemInfo['fbMessageBoardInfo']['hasNum'] = data.hasNum
            itemInfo['fbMessageBoardInfo']['hard'] = data.hard
            itemInfo['gbId'] = gbId
            itemInfo['sex'] = data.sex
            itemInfo['school'] = data.school
            itemInfo['lv'] = data.lv
            itemInfo['isOn'] = getattr(data, 'isOn', False)
            infoList.append(itemInfo)

        dataList = self.getInfoData(infoList)
        if self.mediator:
            self.mediator.Invoke('setFocusPlayerInfo', uiUtils.array2GfxAarry(dataList, True))

    def getInfoData(self, info, isFocus = True):
        ret = []
        p = BigWorld.player()
        for item in info:
            itemInfo = {}
            itemInfo['name'] = item['roleName']
            if item['fbRestEnterTimes']:
                itemInfo['leftCD'] = '剩余CD%d ' % item['fbRestEnterTimes'] + '次'
            else:
                itemInfo['leftCD'] = "剩余CD  <font color=\'#ff0000\'>无</font>"
            dayList = ['一',
             '二',
             '三',
             '四',
             '五',
             '六',
             '日']
            for i in xrange(7):
                if i in item['fbMessageBoardInfo']['challengeWeekList']:
                    dayList[i] = "<font color = \'#6de539\'>" + dayList[i] + '</font>'
                else:
                    dayList[i] = "<font color = \'#808080\'>" + dayList[i] + '</font>'

            itemInfo['date'] = ' '.join(dayList)
            itemInfo['combatData'] = '战力 ' + self.getScoreRegion(item['combatPower'])
            itemInfo['desc'] = item['fbMessageBoardInfo']['desc']
            fbNo = item['fbMessageBoardInfo']['fbNo']
            hasNum = item['fbMessageBoardInfo']['hasNum']
            data = FMBD.data[fbNo]
            hard = item['fbMessageBoardInfo']['hard']
            fbName = data['name']
            hardName = data['type'][hard]
            num = data['num']
            itemInfo['Lv'] = 'Lv %d' % item.get('lv', 10)
            itemInfo['fbName'] = '%s%s%d/%d人' % (hardName,
             fbName,
             hasNum,
             num)
            itemInfo['showTime'] = self.getTimeIndexText(item['fbMessageBoardInfo']['challengeTimeStr'])
            sexList = ['boy', 'boy', 'gril']
            itemInfo['sex'] = sexList[item.get('sex', 1)]
            itemInfo['school'] = uiConst.SCHOOL_FRAME_DESC.get(item.get('school', 3), '')
            itemInfo['gbId'] = item['gbId']
            itemInfo['isOn'] = item['isOn']
            itemInfo['canAboard'] = False
            itemInfo['focusSort'] = 2
            if not hasattr(p, 'fbMessageBoard') or p.fbMessageBoard == None or p.fbMessageBoard.publishType == 0:
                itemInfo['showFocus'] = False
                itemInfo['focusStatus'] = self.getFocusTxt(0)
                itemInfo['focus'] = '关注'
            else:
                itemInfo['showFocus'] = True
                itemInfo['focus'] = '关注'
                if p.fbMessageBoard.connections.get(item['gbId']):
                    data = p.fbMessageBoard.connections[item['gbId']]
                    itemType = data.itemType
                    itemInfo['focusSort'] = 1
                    if itemType == gametypes.FB_MESSAGE_BOARD_CONNECTION_TYPE_ACKONWLEDGE:
                        itemInfo['focus'] = '取消关注'
                    elif itemType == gametypes.FB_MESSAGE_BOARD_CONNECTION_TYPE_APPLY:
                        itemInfo['focus'] = '接受关注'
                        if isFocus == True:
                            itemInfo['canAboard'] = True
                    elif itemType == gametypes.FB_MESSAGE_BOARD_CONNECTION_TYPE_APPLIED:
                        itemInfo['focus'] = '取消关注'
                        itemInfo['focusSort'] = 0
                    itemInfo['focusStatus'] = self.getFocusTxt(itemType)
                else:
                    itemInfo['focusStatus'] = self.getFocusTxt(0)
            ret.append(itemInfo)

        ret.sort(key=lambda cData: cData.get('focusSort', 0))
        return ret

    def getFocusTxt(self, status):
        ret = ['',
         '被关注中',
         '申请关注中',
         '互相关注中']
        return ret[status]

    def setMessageBoardInfo(self, info):
        ret = self.getInfoData(info, False)
        if self.mediator:
            self.mediator.Invoke('setAllPlayerInfo', uiUtils.array2GfxAarry(ret, True))

    def setMessageBoardMsg(self, msgList):
        ret = []
        for msgItem in msgList:
            tWhen = msgItem['tWhen']
            msg = msgItem['msg']
            timestr = time.strftime('%m/%d %H:%M:%S', time.localtime(tWhen))
            useStr = msgItem['who'] + '  ' + timestr
            ret.append([msg, useStr, msgItem['who']])

        if self.mediator:
            self.mediator.Invoke('setMsgList', uiUtils.array2GfxAarry(ret, True))

    def chatToMsgBoard(self, *args):
        msg = unicode2gbk(args[3][0].GetString())
        msg = msg.strip()
        isShowFocus = False
        if hasattr(BigWorld.player(), 'fbMessageBoard') and BigWorld.player().fbMessageBoard != None:
            isShowFocus = BigWorld.player().fbMessageBoard.publishType
        if isShowFocus:
            p = BigWorld.player()
            isNormal, msg = taboo.checkDisbWord(msg)
            if not isNormal:
                p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
                return
            isNormal, msg = taboo.checkBSingle(msg)
            if not isNormal:
                p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
                return
            if time.time() - getattr(p, 'sendMessageBoardChatTime', 0) > 60:
                p.cell.chatToFbMessageBoard(msg)
                if self.mediator:
                    self.mediator.Invoke('clearText', ())
                p.sendMessageBoardChatTime = time.time()
                self.setRefreshTime(1)
            else:
                p.showGameMsg(GMDD.data.YUYUE_CANNOT_SEND_MSG_CD, ())
        else:
            self.hintToAddMsg(1)

    def readTempBoardMessage(self):
        if not os.path.isdir('messageBoard'):
            os.mkdir('messageBoard')
        try:
            f = open('messageBoard/%d' % BigWorld.player().gbId, 'r')
        except Exception as e:
            return

        if f:
            readStr = f.read()
            if readStr:
                data = json.loads(readStr, encoding='UTF-8')
                if data:
                    p = BigWorld.player()
                    p.tempFbMessageBoard = FbMessageBoard()
                    p.tempFbMessageBoard.publishType = data['publishType']
                    p.tempFbMessageBoard.fbNo = data['fbNo']
                    p.tempFbMessageBoard.hard = data['hard']
                    p.tempFbMessageBoard.hasNum = data['hasNum']
                    p.tempFbMessageBoard.challengeWeekList = data['challengeWeekList']
                    p.tempFbMessageBoard.challengeTimeStr = data['challengeTimeStr'].encode(utils.defaultEncoding())
                    p.tempFbMessageBoard.desc = data['desc'].encode(utils.defaultEncoding())
                    p.tempFbMessageBoard.num = data['num']
            f.close()

    def saveTempBoardMessage(self):
        if hasattr(BigWorld.player(), 'tempFbMessageBoard') and BigWorld.player().tempFbMessageBoard != None:
            hasMsg = BigWorld.player().tempFbMessageBoard.publishType
            if not hasMsg:
                return
        else:
            return
        if not os.path.isdir('messageBoard'):
            os.mkdir('messageBoard')
        f = open('messageBoard/%d' % BigWorld.player().gbId, 'w')
        if f:
            data = {}
            p = BigWorld.player()
            data['publishType'] = p.tempFbMessageBoard.publishType
            data['fbNo'] = p.tempFbMessageBoard.fbNo
            data['hard'] = p.tempFbMessageBoard.hard
            data['hasNum'] = p.tempFbMessageBoard.hasNum
            data['challengeWeekList'] = p.tempFbMessageBoard.challengeWeekList
            data['challengeTimeStr'] = p.tempFbMessageBoard.challengeTimeStr
            data['desc'] = p.tempFbMessageBoard.desc
            data['num'] = p.tempFbMessageBoard.num
            data_string = json.dumps(data, encoding=utils.defaultEncoding())
            f.write(data_string)
            f.close()

    def getShowTitle(self, *args):
        p = BigWorld.player()
        if not hasattr(p, 'fbMessageBoard') or p.fbMessageBoard == None or p.fbMessageBoard.publishType == 0:
            return GfxValue(gbk2unicode(''))
        fbMessageBoard = p.fbMessageBoard
        hard = fbMessageBoard.hard
        fbNo = fbMessageBoard.fbNo
        hasNum = fbMessageBoard.hasNum
        data = FMBD.data[fbNo]
        fbName = data['name']
        hardName = data['type'][hard]
        num = data['num']
        titleStr = ''
        if fbMessageBoard.publishType == gametypes.FB_PUBLISH_TYPE_APPLY:
            titleStr = gbk2unicode('您正在求组弑神队-%s-%s-（%d/%d人）' % (fbName,
             hardName,
             hasNum,
             num))
        else:
            titleStr = gbk2unicode('您正在招募弑神队-%s-%s-（%d/%d人）' % (fbName,
             hardName,
             hasNum,
             num))
        return GfxValue(titleStr)
