#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/clanWarYaBiaoProxy.o
import BigWorld
from Scaleform import GfxValue
import utils
import Math
import gametypes
from callbackHelper import Functor
from gamestrings import gameStrings
import uiConst
import gamelog
import gameglobal
from guis.asObject import ASObject
import const
from guis import uiUtils
from uiProxy import UIProxy
from guis import events
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis import ui
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import clan_courier_config_data as CCCD
from data import clan_courier_data as CCD
MAX_MEMBER_CNT = 3
VEHICLE_MAX_CNT = 2

class ClanWarYaBiaoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClanWarYaBiaoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.delPushTimer = None
        self.reset()

    def reset(self):
        self.isExpand = True
        self.isAtk = False
        self.selectedIdx = 0
        self.multiId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CLAN_WAR_YABIAO:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            BigWorld.callback(1, self.tickFun)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CLAN_WAR_YABIAO)

    def show(self):
        self.delPushIcon()
        if not BigWorld.player().inClanCourier():
            self.hide()
            return
        p = BigWorld.player()
        if not p.isClanCourierAvatar() and not p.isJct:
            self.hide()
            return
        p = BigWorld.player()
        self.isAtk = p.jctSeq and p.isJct
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CLAN_WAR_YABIAO)
        else:
            self.refreshInfo()

    def initUI(self):
        pass

    def getCourierId(self):
        p = BigWorld.player()
        courierIdList = getattr(p, 'clanCourierDic', {}).keys()
        courierIdList.sort()
        if self.selectedIdx < len(courierIdList):
            return courierIdList[self.selectedIdx]
        return 0

    def getCourierData(self, courierid):
        p = BigWorld.player()
        return getattr(p, 'clanCourierDic', {}).get(courierid, {})

    def refreshDefence(self):
        if not self.widget:
            return
        self.widget.gotoAndStop('guardExtend' if self.isExpand else 'guard')
        self.widget.hideBtn.addEventListener(events.BUTTON_CLICK, self.handleHideBtnClick, False, 0, True)
        p = BigWorld.player()
        courierIdList = getattr(p, 'clanCourierDic', {}).keys()
        courierIdList.sort()
        ASUtils.setDropdownMenuData(self.widget.dropDown, courierIdList)
        self.widget.dropDown.selectedIndex = self.selectedIdx
        courierId = self.getCourierId()
        courierData = self.getCourierData(courierId)
        configData = CCD.data.get(courierId, {})
        hp = courierData.get('hp', 0)
        mhp = courierData.get('mhp', 1)
        position = courierData.get('pos', (0, 0, 0))
        if courierData.get('state', 0) == gametypes.CLAN_COURIER_DEAD:
            if self.widget.biaocheIcon.currentFrame < 6:
                self.widget.biaocheIcon.gotoAndPlay('died')
        elif self.widget.biaocheIcon.currentFrame >= 6:
            self.widget.biaocheIcon.gotoAndPlay('normal')
        totalResources = configData.get('res', 100)
        desPosition = configData.get('dstPos', (0, 0, 0))
        self.widget.dropDown.addEventListener(events.INDEX_CHANGE, self.handleDropDownIdxChange, False, 0, True)
        self.widget.dropDown.labelFunction = self.itemToLabel
        self.widget.hp.maxValue = mhp
        self.widget.hp.currentValue = hp
        self.widget.hp.textField.visible = False
        self.widget.txtPos.htmlText = gameStrings.CLAN_WAR_COURIER_GOTO % (const.SPACE_NO_BIG_WORLD,
         position[0],
         position[1],
         position[2],
         '%d,%d,%d' % (position[0], position[2], position[1]))
        self.widget.txtCost.text = CCCD.data.get('clanCourierTeleportCost', 500)
        self.widget.teleportBtn.disabled = p.teleportCourierID and p.teleportCourierID != self.getCourierId()
        self.widget.teleportBtn.addEventListener(events.BUTTON_CLICK, self.handleTeleportBtnClick, False, 0, True)
        self.widget.txtResources.text = courierData.get('res', 0)
        self.widget.txtPoint.text = getattr(p, 'courierDonate', 0)
        tStartMove = BigWorld.player().getClanWarCourierStartTime()
        if tStartMove:
            nowTime = courierData['diedTime'] if courierData.get('diedTime', 0) else utils.getNow()
            moveTime = nowTime - tStartMove
        else:
            moveTime = 0
        moveTime = max(0, moveTime)
        self.widget.txtTime.text = utils.formatTimeStr(moveTime, 'h:m:s', zeroShow=True, hNum=2, mNum=2, sNum=2)
        if self.isExpand:
            desc = GMD.data.get(GMDD.data.CLAN_WAR_YABIAO_DES, {}).get('text', 'GMDD.data.CLAN_WAR_YABIAO_DES %d (%d,%d,%d)') % (totalResources,
             desPosition[0],
             desPosition[2],
             desPosition[1])
            self.widget.txtDesc.htmlText = desc
            self.widget.normalBtn.addEventListener(events.BUTTON_CLICK, self.handleNormalBtnClick, False, 0, True)
            clanCourierTopMember = getattr(p, 'clanCourierTopMember', [])
            memberCnt = len(clanCourierTopMember)
            for i in xrange(MAX_MEMBER_CNT):
                memberMc = self.widget.getChildByName('rank%d' % i)
                if i < memberCnt:
                    memberMc.visible = True
                    killPlayer, assist, killMonster, donate, name, gbId = clanCourierTopMember[i]
                    memberMc.txtRank.text = str(i + 1)
                    memberMc.txtPlayerName.text = name
                    memberMc.txtKill.text = str(killPlayer)
                    memberMc.txtAssist.text = str(assist)
                    memberMc.txtMonster.text = ''
                    memberMc.txtDonate.text = donate
                else:
                    memberMc.visible = False

            self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.handleRankBtnClick, False, 0, True)
            self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleRewardBtnClick, False, 0, True)
        else:
            self.widget.expandBtn.addEventListener(events.BUTTON_CLICK, self.handleExpandBtnClick, False, 0, True)

    def handleDropDownIdxChange(self, *args):
        self.selectedIdx = int(self.widget.dropDown.selectedIndex)
        self.refreshInfo()

    def itemToLabel(self, *args):
        courierId = int(args[3][0].GetNumber())
        courierName = CCD.data.get(courierId, {}).get('name', 'xxx')
        return GfxValue(ui.gbk2unicode(courierName))

    def handleExpandBtnClick(self, *args):
        self.isExpand = True
        self.refreshInfo()

    def handleRewardBtnClick(self, *args):
        gameglobal.rds.ui.generalReward.show(CCCD.data.get('generalRewardKey', 1))

    def handleTeleportBtnClick(self, *args):
        if not getattr(BigWorld.player(), 'teleportCourierID', 0):
            msg = GMD.data.get(GMDD.data.CLAN_WAR_YABIAO_BIND_CONFIRM, {}).get('text', 'GMDD.data.CLAN_WAR_YABIAO_BIND_CONFIRM')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.teleportToClanCourier, self.getCourierId()))
        else:
            if self.getCourierId() != BigWorld.player().teleportCourierID:
                BigWorld.player().showGameMsg(GMDD.data.CLAN_WAR_YABIAO_BIND_ID, ())
                return
            BigWorld.player().cell.teleportToClanCourier(self.getCourierId())

    def handleRankBtnClick(self, *args):
        gameglobal.rds.ui.rankCommon.showRankCommon(CCCD.data.get('rankId', 4))

    def refreshAtk(self):
        if not self.widget:
            return
        self.widget.gotoAndStop('atkExtend' if self.isExpand else 'atk')
        self.widget.hideBtn.addEventListener(events.BUTTON_CLICK, self.handleHideBtnClick, False, 0, True)
        p = BigWorld.player()
        clanCourierDic = getattr(p, 'clanCourierDic', {})
        infoList = clanCourierDic.values()
        infoList.sort(cmp=lambda a, b: cmp(a['courierID'], b['courierID']))
        for i in xrange(VEHICLE_MAX_CNT):
            position = infoList[i]['pos'] if i < len(infoList) else (0, 0, 0)
            txtPos = self.widget.getChildByName('txtPos%d' % i)
            txtPos.htmlText = gameStrings.CLAN_WAR_COURIER_GOTO % (const.SPACE_NO_BIG_WORLD,
             position[0],
             position[1],
             position[2],
             '%d,%d,%d' % (position[0], position[2], position[1]))
            txtResources = self.widget.getChildByName('txtResources%d' % i)
            txtResources.text = infoList[i]['res'] if i < len(infoList) else 0
            biaocheMc = self.widget.getChildByName('biaoche%d' % i)
            biaocheMc.dataIdx = i
            biaocheMc.addEventListener(events.MOUSE_CLICK, self.handleBiaocheMcClick, False, 0, True)
            hpMc = self.widget.getChildByName('hp%d' % i)
            courierData = infoList[i] if i < len(infoList) else {}
            if courierData.get('state', 0) == gametypes.CLAN_COURIER_DEAD:
                if biaocheMc.currentFrame < 6:
                    biaocheMc.gotoAndPlay('died')
            elif biaocheMc.currentFrame >= 6:
                biaocheMc.gotoAndPlay('normal')
            hp = courierData.get('hp', 0)
            mhp = courierData.get('mhp', 1)
            hpMc.maxValue = mhp
            hpMc.currentValue = hp
            hpMc.textField.visible = False

        if self.isExpand:
            self.widget.atkNormalBtn.addEventListener(events.BUTTON_CLICK, self.handleNormalBtnClick, False, 0, True)
            self.widget.atkHelp.helpKey = CCCD.data.get('jiuChongAnShaHelp', 1)
            self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleAtkRewardBtnClick, False, 0, True)
            self.widget.exitBtn.addEventListener(events.BUTTON_CLICK, self.handleExitBtnClick, False, 0, True)
            self.widget.txtDesc.htmlText = GMD.data.get(GMDD.data.CLAN_WAR_YABIAO_ATK_DESC, {}).get('text', 'GMDD.data.CLAN_WAR_YABIAO_ATK_DESC')
        else:
            self.widget.atkExpandBtn.addEventListener(events.BUTTON_CLICK, self.handleExpandBtnClick, False, 0, True)
        self.refreshAtkStatus()

    def refreshAtkStatus(self):
        startTimeStr = CCCD.data.get('startTime', '')
        startTimeSec = utils.getPreCrontabTime(startTimeStr)
        if not utils.isSameWeek(startTimeSec):
            startTimeSec = utils.getNextCrontabTime(startTimeStr)
        moveInterval = CCCD.data.get('clanCourierStartInterval', 0)
        clanCourierDic = BigWorld.player().clanCourierDic
        isEnd = len(clanCourierDic) and all((value.get('isEnd', False) for value in clanCourierDic.itervalues()))
        if utils.getNow() < startTimeSec + moveInterval:
            leftTime = int(startTimeSec + moveInterval - utils.getNow())
            self.widget.timeDesc.gotoAndStop('ready')
            self.widget.timeDesc.desc.text = gameStrings.CLAN_WAR_COURIER_READY % utils.formatTimeStr(leftTime, 'm:s', zeroShow=True)
        elif not isEnd:
            tStartMove = BigWorld.player().getClanWarCourierStartTime()
            if tStartMove:
                moveTime = max(0, utils.getNow() - tStartMove)
            else:
                moveTime = 0
            self.widget.timeDesc.gotoAndStop('atk')
            self.widget.timeDesc.attacking.text = gameStrings.CLAN_WAR_COURIER_ATK % utils.formatTimeStr(moveTime, 'm:s', zeroShow=True)
        else:
            self.widget.timeDesc.gotoAndStop('end')

    def handleBiaocheMcClick(self, *args):
        e = ASObject(args[3][0])
        idx = int(e.currentTarget.dataIdx)
        p = BigWorld.player()
        clanCourierDic = getattr(p, 'clanCourierDic', {})
        infoList = clanCourierDic.values()
        infoList.sort(cmp=lambda a, b: cmp(a['courierID'], b['courierID']))
        if idx < len(infoList):
            position = infoList[idx]['pos']
            gamelog.info('jbx:findPosByPos', position)
            uiUtils.findPosByPos(const.SPACE_NO_BIG_WORLD, Math.Vector3(position))

    def handleAtkRewardBtnClick(self, *args):
        gameglobal.rds.ui.generalReward.show(CCCD.data.get('atkGeneralReward', 1))

    def handleExitBtnClick(self, *args):
        msg = GMD.data.get(GMDD.data.CLAN_WAR_EXIT_JCT_CONFIRM, {}).get('text', 'GMDD.data.CLAN_WAR_EXIT_JCT_CONFIRM')
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, BigWorld.player().cell.exitCourierJct)

    def refreshInfo(self):
        if not self.widget:
            return
        if not BigWorld.player().inClanCourier():
            self.hide()
            return
        p = BigWorld.player()
        if not p.isClanCourierAvatar() and not p.isJct:
            self.hide()
            return
        clanCourierDic = p.clanCourierDic
        isEnd = len(clanCourierDic) and all((value.get('isEnd', False) for value in clanCourierDic.itervalues()))
        endTime = 0
        for value in clanCourierDic.values():
            if value.has_key('diedTime'):
                endTime = max(endTime, value['diedTime'])

        if isEnd:
            if p.isClanCourierAvatar():
                if endTime:
                    if utils.getNow() - endTime > CCCD.data.get('closeDuration', 180):
                        self.hide()
                        return
                else:
                    self.hide()
                    return
            elif not p.isJct:
                self.hide()
                return
        if self.isAtk:
            self.refreshAtk()
        else:
            self.refreshDefence()

    def handleHideBtnClick(self, *args):
        self.hide()
        self.addPushIcon()

    def handleNormalBtnClick(self, *args):
        self.isExpand = False
        self.refreshInfo()

    def tickFun(self):
        if not self.widget:
            return
        self.refreshInfo()
        BigWorld.callback(0.3, self.tickFun)

    def addPushIcon(self):
        if not BigWorld.player().inClanCourier():
            return
        if self.widget:
            return
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_CLAN_WAR_YABIAO, {'click': self.show})
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CLAN_WAR_YABIAO)
        if not self.delPushTimer:
            endTime = utils.getNextCrontabTime(CCCD.data.get('endTime', ''))
            if endTime > utils.getNow():
                self.delPushTimer = BigWorld.callback(endTime - utils.getNow(), self.delPushIcon)

    def delPushIcon(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_CLAN_WAR_YABIAO)

    def showJoinClanWarHuntConfirm(self):
        msg = GMD.data.get(GMDD.data.CLAN_WAR_YABIAO_HUNT_CONFIRM, {}).get('text', 'GMDD.data.CLAN_WAR_YABIAO_HUNT_CONFIRM')
        self.multiId = self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.confirmJoinCallback, noCallback=self.noCallback)

    def noCallback(self):
        BigWorld.player().showGameMsg(GMDD.data.REFUSE_JOIN_JCT, ())

    def showJoindClanWarHunt(self):
        msg = GMD.data.get(GMDD.data.CLAN_WAR_DURIED_JOINED, {}).get('text', 'GMDD.data.CLAN_WAR_DURIED_JOINED')
        self.multiId = self.uiAdapter.messageBox.showYesNoMsgBox(msg)

    def confirmJoinCallback(self):
        gamelog.info('jbx:confirmJoinJCT')
        BigWorld.player().cell.teleportToCourierJCT()
