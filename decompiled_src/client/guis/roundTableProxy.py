#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/roundTableProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import utils
import gametypes
from guis import events
from guis import ui
from guis import uiConst
from guis import uiUtils
from item import Item
from cdata import game_msg_def_data as GMDD
from data import guild_activity_item_data as GAID
from data import state_data as SD
from data import game_msg_data as GMD
from data import sys_config_data as SCD
from callbackHelper import Functor
from uiProxy import UIProxy
RT_STATE_NOT_BEGIN = 0
RT_STATE_NOT_JOIN = 1
RT_STATE_IN_MEETING = 2
RT_STATE_END = 3
RT_STATE_ERROR = 4
RT_REFRESH_EVENTS = (events.EVENT_RT_JOINED, events.EVENT_RT_SEAT_CHAGED)
OPEN_TYPE_BY_ITEM = 0
OPEN_TYPE_BY_ENTITY = 1

class RoundTableProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RoundTableProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeRoundTable': self.onCloseRoundTable,
         'getRoundTableInfo': self.onGetRoundTableInfo,
         'startMeeting': self.onStartMeeting,
         'stopMeeting': self.onStopMeeting,
         'joinMeeting': self.onJoinMeeting,
         'leaveMeeting': self.onLeaveMeeting}
        self.reset()
        self.tableType = 0
        self.tableWidgetId = uiConst.WIDGET_ROUND_TABLE
        uiAdapter.registerEscFunc(self.tableWidgetId, self.onCloseRoundTable)
        self.addEvent(events.EVENT_RT_APPLY, self.onApplyRoundTable, isGlobal=True)
        self.addEvent(events.EVENT_RT_LEAVE, self.onLeaveRoundTable, isGlobal=True)
        self.addEvent(events.EVENT_RT_END, self.onRoundTableEnd, isGlobal=True)
        self.addEvent(events.EVENT_RT_SEAT_CREATED, self.onRoundTableCreated, isGlobal=True)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.tableWidgetId:
            self.mediator = mediator

    def openRoundTableByItem(self, item, page, pos, tableType):
        if not self.enableRoundTable():
            return
        elif not item:
            return
        else:
            self.tableType = tableType
            if self.tableType == gametypes.ROUND_TABLE_TYPE_GUILD:
                if not getattr(item, 'cstype', None) == Item.SUBTYPE_2_GUILD_OPEN_ROUND_TABLE:
                    return
            elif self.tableType == gametypes.ROUND_TABLE_TYPE_FUBEN:
                if not getattr(item, 'cstype', None) == Item.SUBTYPE_2_FUBEN_OPEN_ROUND_TABLE:
                    return
            p = BigWorld.player()
            if p.belongToRoundTable:
                p.showGameMsg(GMDD.data.ROUND_TABLE_ALREADY_JOIN, ())
                return
            self.lockedPos = [(page, pos)]
            self.openType = OPEN_TYPE_BY_ITEM
            self.itemId = item.id
            self.show()
            return

    def openRoundTableByEntity(self, entId):
        if not self.enableRoundTable():
            return
        self.openType = OPEN_TYPE_BY_ENTITY
        self.lockedPos = []
        self.entId = entId
        self.show()

    def openRoundTableByPushMsg(self):
        p = BigWorld.player()
        if not (p.belongToRoundTable or self.endFlag):
            return
        self.openRoundTableByEntity(p.belongToRoundTable)

    def show(self, *arg):
        if not self.enableRoundTable():
            return
        self.removePushMsg()
        gameglobal.rds.ui.loadWidget(self.tableWidgetId)

    def enableRoundTable(self):
        return gameglobal.rds.configData.get('enableGuildRoundTable', False)

    def onCloseRoundTable(self, *arg):
        if BigWorld.player().belongToRoundTable and not self.leaveAction:
            self.addPushMsg()
        self.hide(True)

    def clearWidget(self):
        self.lockedPos = []
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(self.tableWidgetId)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def reset(self):
        self.mediator = None
        self.lockedPos = []
        self.openType = OPEN_TYPE_BY_ITEM
        self.itemId = 0
        self.entId = 0
        self.leaveAction = False
        self.endFlag = False
        self.endSeatsShot = None

    def addPushMsg(self):
        pushMsg = gameglobal.rds.ui.pushMessage
        msgType = uiConst.MESSAGE_TYPE_ROUND_TABLE
        callBackDict = {'click': self.openRoundTableByPushMsg}
        if pushMsg.hasMsgType(msgType):
            return
        pushMsg.addPushMsg(msgType)
        pushMsg.setCallBack(msgType, callBackDict)

    def removePushMsg(self):
        pushMsg = gameglobal.rds.ui.pushMessage
        msgType = uiConst.MESSAGE_TYPE_ROUND_TABLE
        if not pushMsg.hasMsgType(msgType):
            return
        pushMsg.removePushMsg(msgType)

    def onApplyRoundTable(self, event):
        srcEntId = event.data.get('srcEntId', 0)
        ent = BigWorld.entities.get(srcEntId)
        msg = ent.roleName + gameStrings.TEXT_ROUNDTABLEPROXY_161
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onApplyRoundTableAccept, srcEntId), gameStrings.TEXT_IMPFRIEND_962, Functor(self.onApplyRoundTableReject, srcEntId), gameStrings.TEXT_IMPFRIEND_963, isModal=False)

    def onLeaveRoundTable(self):
        self.leaveAction = True
        self.onCloseRoundTable()
        self.removePushMsg()

    def onRoundTableEnd(self, event):
        self.endFlag = True
        self.itemId = event.data['itemId']
        self.endSeatsShot = event.data['seats']
        if self.mediator:
            self.refreshRoundTable()
        else:
            self.openRoundTableByPushMsg()

    def onApplyRoundTableAccept(self, srcEntId):
        BigWorld.player().cell.acceptRoundTable(srcEntId, self.tableType)

    def onApplyRoundTableReject(self, srcEntId):
        BigWorld.player().cell.denyRoundTableApplicant(srcEntId)

    @ui.uiEvent(uiConst.WIDGET_ROUND_TABLE, RT_REFRESH_EVENTS)
    @ui.callAfterTime()
    def refreshRoundTable(self):
        if self.mediator:
            self.mediator.Invoke('refreshTable')

    def onGetRoundTableInfo(self, *arg):
        ret = {}
        p = BigWorld.player()
        ret['state'] = self.getRoundTableState()
        if ret['state'] == RT_STATE_NOT_BEGIN:
            itemData = GAID.data.get(self.itemId, {})
            ret['memberNumMax'] = itemData.get('seatNum', 5)
            ret['durationMax'] = itemData.get('TTL', 300)
            self.appendBuffListByItemId(ret, self.itemId)
        elif ret['state'] == RT_STATE_END:
            self.appendBuffListByItemId(ret, self.itemId)
            self.appendSeatsInfo(ret)
            itemData = GAID.data.get(self.itemId, {})
            ret['memberNumMax'] = itemData.get('seatNum', 5)
            ret['memberNumNow'] = len(ret['memberList'])
        else:
            entity = BigWorld.entities.get(self.entId)
            if not entity:
                self.appendSeatsInfo(ret)
                ret['state'] = RT_STATE_ERROR
                return uiUtils.dict2GfxDict(ret, True)
            ret['isHeader'] = entity.ownerGbId == p.gbId
            ret['memberNumNow'] = len(entity.seats)
            ret['memberNumMax'] = entity.seatNum
            ret['meetingStartTime'] = entity.createTime
            ret['durationMax'] = entity.ttl
            ret['initDuration'] = int(ret['durationMax'] - (p.getServerTime() - ret['meetingStartTime']))
            self.appendBuffListByEntity(ret, entity)
            self.appendSeatsInfo(ret)
        ret['maxTimesToday'] = 1
        ret['usedTimesToday'] = 1 if utils.isSameDay(getattr(p, 'lastOpenRoundTableTimeInfo', {}).get(self.tableType, 0)) else 0
        self.refreshRoundTableTeacherBuffId()
        return uiUtils.dict2GfxDict(ret, True)

    def refreshRoundTableTeacherBuffId(self):
        p = BigWorld.player()
        buffId = SCD.data.get('roundTableTeacherBuffId', 0)
        needAddBuffId = False
        headerGbId = getattr(p, 'headerGbId', 0)
        if self.getRoundTableState() == RT_STATE_IN_MEETING:
            if headerGbId:
                if p.isTeacher(headerGbId) or p.isApprentice(headerGbId):
                    needAddBuffId = True
        if needAddBuffId:
            p.addBuffIconByClient(buffId)
        else:
            p.removeBuffIconByClient(buffId)

    def getRoundTableState(self):
        p = BigWorld.player()
        if self.endFlag:
            ret = RT_STATE_END
        elif self.openType == OPEN_TYPE_BY_ITEM:
            if not p.belongToRoundTable:
                ret = RT_STATE_NOT_BEGIN
            else:
                self.entId = p.belongToRoundTable
                ret = RT_STATE_IN_MEETING
        elif p.belongToRoundTable != self.entId:
            ret = RT_STATE_NOT_JOIN
        else:
            ret = RT_STATE_IN_MEETING
        return ret

    def appendSeatsInfo(self, ret):
        memberList = []
        if self.endFlag:
            seats = self.endSeatsShot
        else:
            ent = BigWorld.entities.get(self.entId)
            if ent:
                seats = ent.seats
            else:
                seats = []
        if not seats:
            memberList.append(self.getRoundMemberInfo(None))
            ret['memberList'] = memberList
            return
        else:
            for gbId in seats:
                memberList.append(self.getRoundMemberInfo(seats[gbId]))

            memberList.sort(key=lambda k: k['seatPos'])
            ret['memberList'] = memberList
            return

    def appendBuffListByItemId(self, ret, itemId):
        itemData = GAID.data.get(itemId, {})
        ownerBuffId = itemData.get('ownerBuf', 0)
        inBuffs = itemData.get('inBufs', [])
        endBuffId = itemData.get('endBuf', 0)
        self._appendBufList(ret, ownerBuffId, inBuffs, endBuffId)

    def appendBuffListByEntity(self, ret, ent):
        itemId = getattr(ent, 'itemId', 319000)
        self.appendBuffListByItemId(ret, itemId)

    def _appendBufList(self, ret, ownerBuf, inBuffs, endBuf):
        bufList = []
        bufList.append(self.getBuffInfo(ownerBuf, ret.get('isHeader', False)))
        for bufId in inBuffs:
            if bufId is 0:
                continue
            needNum = inBuffs.index(bufId, 0) + 1
            bufList.append(self.getBuffInfo(bufId, ret.get('memberNumNow', 0) == needNum))

        bufList.append(self.getBuffInfo(endBuf, ret['state'] == RT_STATE_END))
        ret['buffList'] = bufList

    def getRoundMemberInfo(self, seatInfo):
        ret = {}
        ret['seatPos'] = seatInfo[1] if seatInfo else 0
        ret['onLine'] = seatInfo[3] == 0 if seatInfo else True
        ret['roleName'] = seatInfo[4] if seatInfo else BigWorld.player().realRoleName
        return ret

    def getBuffInfo(self, bufId, active):
        ret = {}
        sdData = SD.data.get(bufId, {})
        iconId = str(sdData.get('iconId', 0))
        ret['active'] = active
        ret['iconPath40'] = uiConst.STATE_ICON_PATH_40 + iconId + uiConst.ICON_SUFFIX
        ret['iconPath48'] = uiConst.STATE_ICON_PATH_48 + iconId + uiConst.ICON_SUFFIX
        ret['desc'] = sdData.get('desc', '')
        return ret

    def onStartMeeting(self, *arg):
        if not BigWorld.player().stateMachine.checkStartMeeting(self.tableType):
            return
        msg = GMD.data.get(GMDD.data.ROUND_TABLE_WARN_START, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmStartMeeting))

    def onConfirmStartMeeting(self):
        if not self.lockedPos:
            return
        if not BigWorld.player().stateMachine.checkStartMeeting(self.tableType):
            return
        itemPos = self.lockedPos[0]
        BigWorld.player().cell.openRoundTable(itemPos[0], itemPos[1], self.tableType)

    def onStopMeeting(self, *arg):
        msg = GMD.data.get(GMDD.data.ROUND_TABLE_WARN_STOP, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmStopMeeting))

    def onConfirmStopMeeting(self):
        BigWorld.player().cell.leaveRoundTable()

    def onJoinMeeting(self, *arg):
        msg = GMD.data.get(GMDD.data.ROUND_TABLE_WARN_JOIN, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmJoinMeeting))

    def onConfirmJoinMeeting(self):
        BigWorld.player().cell.applyForRoundTable(self.entId, self.tableType)

    def onLeaveMeeting(self, *arg):
        msg = GMD.data.get(GMDD.data.ROUND_TABLE_WARN_LEAVE, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmLeaveMeeting))
        self.refreshRoundTableTeacherBuffId()

    def onConfirmLeaveMeeting(self):
        BigWorld.player().cell.leaveRoundTable()

    def isItemDisabled(self, kind, page, pos, item):
        return (page, pos) in self.lockedPos

    def onRoundTableCreated(self, event):
        self.tableType = event.data.get('tableType', 0)
