#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/backflowPriviegeProxy.o
import BigWorld
import utils
import events
import uiConst
import clientUtils
import const
from uiProxy import UIProxy
from asObject import ASObject
from guis import uiUtils
from gameStrings import gameStrings
from asObject import RedPotManager
from data import flowback_group_privilege_data as FGPD
from cdata import game_msg_def_data as GMDD
MAX_PRIVIEGE_MUN = 5
MAX_PRIVIEGE_TYPE2_REWARD_NUM = 6
PRIVIEGE_HEIGHT = 120
PRIVIEGE_TYPE_HAS_REWARD = 2
PRIVIEGE_DAY_TO_SECOND = 86400
PRIVIEGE_ICON_PATH = 'backflow/%d.dds'

class BackflowPriviegeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BackflowPriviegeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.callback = None
        self.items = []
        self.copyItems = []

    def reset(self):
        self.callback = None
        self.items = []
        self.copyItems = []

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        pass

    def handleGetRewardBtnClick(self, *args):
        e = ASObject(args[3][0])
        priviegeMc = e.currentTarget.parent
        priviegeId = priviegeMc.priviegeId
        if priviegeId:
            p = BigWorld.player()
            p.cell.receiveFlowbackPrivilegeReward(priviegeId)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        privilegesInfo = p.flowbackGroupBonus.privilegesInfo
        startTime = p.flowbackGroupBonus.startTime
        curTime = utils.getNow()
        priviegeList = self.getPriviegeList(privilegesInfo, startTime, curTime)
        priviegePanel = self.widget.priviegePanel
        self.widget.removeAllInst(priviegePanel)
        self.items = []
        self.copyItems = []
        for i, priviegeId in enumerate(priviegeList):
            priviegeMc = self.widget.getInstByClsName('BackflowPriviege_priviegeItem')
            stage = privilegesInfo[priviegeId]
            data = FGPD.data.get(priviegeId, {})
            iconId = data.get('iconId', 0)
            day = data.get('duration', 0)
            privilegeType = data.get('privilegeType', 0)
            if privilegeType == const.FLOWBACK_PRIVILEGE_TYPE_BONUS_EQUIPS:
                equipBonusIds = data.get('equipBonusIds', (1,))
                for lvData, schoolBonusData in equipBonusIds[0].iteritems():
                    if lvData[0] <= p.lv <= lvData[1]:
                        bonusId = schoolBonusData.get(p.school, 0)
                        break

            else:
                bonusId = data.get('bonusId', 0)
            privilegeDesc = data.get('privilegeDesc', '')
            endTime = startTime + day * const.TIME_INTERVAL_DAY
            priviegeMc.priviegeId = priviegeId
            priviegeMc.endTime = endTime
            iconPath = PRIVIEGE_ICON_PATH % iconId
            priviegeMc.icon.clear()
            priviegeMc.icon.fitSize = True
            priviegeMc.icon.loadImage(iconPath)
            priviegeMc.desc.text = privilegeDesc
            if privilegeType in (const.FLOWBACK_PRIVILEGE_TYPE_AURA, const.FLOWBACK_PRIVILEGE_TYPE_MULTI_FUBEN_TREASURE_BOX):
                priviegeMc.getRewardBtn.visible = False
                priviegeMc.getedPic.visible = False
                priviegeMc.itemMc.visible = False
            else:
                priviegeMc.itemMc.visible = True
                self.updatePriviegeRewardItem(priviegeMc, bonusId)
                if stage == const.FLOWBACK_PRIVILEGE_STATE_NO_AWARD:
                    priviegeMc.getRewardBtn.visible = True
                    priviegeMc.getedPic.visible = False
                elif stage == const.FLOWBACK_PRIVILEGE_STATE_ALREADY_AWARD:
                    priviegeMc.getRewardBtn.visible = False
                    priviegeMc.getedPic.visible = True
            priviegeMc.getRewardBtn.addEventListener(events.MOUSE_CLICK, self.handleGetRewardBtnClick, False, 0, True)
            priviegeMc.y = PRIVIEGE_HEIGHT * i
            priviegePanel.addChild(priviegeMc)
            self.items.append(priviegeMc)
            self.copyItems.append(priviegeMc)

        self.updateLeftTime()

    def updateLeftTime(self):
        if not self.copyItems:
            self.stopCallback()
            return
        curTime = utils.getNow()
        for item in self.items:
            leftTime = max(item.endTime - curTime, 0)
            self.updateTime(item, leftTime)

        BigWorld.callback(1, self.updateLeftTime)

    def updateTime(self, item, leftTime):
        day = utils.formatDurationLeftDay(leftTime)
        hour = utils.formatDurationLeftHour(leftTime)
        minute = utils.formatDurationLeftMin(leftTime)
        srtTime = gameStrings.BACK_FLOW_LEFT_TIME % (day, hour, minute)
        if leftTime > 0:
            item.leftTimeT.htmlText = gameStrings.BACK_FLOW_LEFT_TIME_TITLE % uiUtils.toHtml(srtTime, '#f65c3f')
            item.getRewardBtn.enabled = True
        else:
            item.leftTimeT.htmlText = gameStrings.SCHEME_SWITCH_TIME_OUT
            item.getRewardBtn.enabled = False
            if item in self.copyItems:
                self.copyItems.remove(item)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def updatePriviegeRewardItem(self, priviegeMc, bonusId):
        itemBonus = clientUtils.genItemBonus(bonusId)
        for i in range(MAX_PRIVIEGE_TYPE2_REWARD_NUM):
            slot = priviegeMc.itemMc.getChildByName('slot%d' % i)
            if i < len(itemBonus):
                slot.visible = True
                itemId, num = itemBonus[i]
                slot.fitSize = True
                slot.dragable = False
                itemInfo = uiUtils.getGfxItemById(itemId, num)
                slot.setItemSlotData(itemInfo)
            else:
                slot.visible = False

    def getPriviegeList(self, privilegesInfo, startTime, curTime):
        priviegeList = []
        for i, priviegeId in enumerate(sorted(privilegesInfo.keys(), reverse=True)):
            stage = privilegesInfo[priviegeId]
            day = FGPD.data.get(priviegeId, {}).get('duration', 0)
            endTime = startTime + day * PRIVIEGE_DAY_TO_SECOND
            if curTime > endTime:
                priviegeList.append(priviegeId)
            elif stage == const.FLOWBACK_PRIVILEGE_STATE_NO_AWARD or stage == const.FLOWBACK_PRIVILEGE_STATE_ALREADY_AWARD_BUT_VALID:
                priviegeList.insert(0, priviegeId)
            else:
                priviegeList.append(priviegeId)

        return priviegeList

    def checkRedPoint(self):
        isRedPot = False
        p = BigWorld.player()
        startTime = p.flowbackGroupBonus.startTime
        curTime = utils.getNow()
        privilegesInfo = p.flowbackGroupBonus.privilegesInfo
        for i, priviegeId in enumerate(privilegesInfo):
            data = FGPD.data.get(priviegeId, {})
            day = data.get('duration', 0)
            endTime = startTime + day * const.TIME_INTERVAL_DAY
            leftTime = max(endTime - curTime, 0)
            stage = privilegesInfo[priviegeId]
            if stage == const.FLOWBACK_PRIVILEGE_STATE_NO_AWARD and leftTime > 0:
                isRedPot = True
                break

        return isRedPot

    def updateRedPot(self):
        RedPotManager.updateRedPot(uiConst.BACK_FLOW_PRIVIEGE_RED_POT)

    def checkTimeEnd(self):
        p = BigWorld.player()
        privilegesInfo = p.flowbackGroupBonus.privilegesInfo
        startTime = p.flowbackGroupBonus.startTime
        curTime = utils.getNow()
        for i, priviegeId in enumerate(privilegesInfo):
            data = FGPD.data.get(priviegeId, {})
            day = data.get('duration', 0)
            endTime = startTime + day * const.TIME_INTERVAL_DAY
            leftTime = max(endTime - curTime, 0)
            if leftTime > 0:
                return False

        return True
