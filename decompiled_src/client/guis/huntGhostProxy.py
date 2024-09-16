#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/huntGhostProxy.o
import BigWorld
import Math
import gametypes
import gamelog
import gameglobal
import const
import uiConst
import uiUtils
import events
import math
import huntGhostCommon
import utils
import formula
from asObject import ASUtils
from uiProxy import UIProxy
from sMath import distance2D, limit
from gamestrings import gameStrings
from callbackHelper import Functor
from asObject import TipManager
from helpers import tickManager
from helpers import navigator
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import hunt_ghost_area_data as HGAD
from cdata import hunt_ghost_area_point_data as HGAPD
from data import hunt_ghost_config_data as HGCD
RESULT_TYPE_FAR = 0
RESULT_TYPE_MIDDLE = 1
RESULT_TYPE_NEAR = 2
RESULT_TYPE_DESTINATION = 3
GHOST_TYPE_COMMON = 1
GHOST_TYPE_SPECIAL = 0
STATE_DEFAULT = 0
STATE_START_NAVI = 1
STATE_NAVI = 2
STATE_BOX = 3
VIEW_RAD = 93

class HuntGhostProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HuntGhostProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_HUNT_GHOST, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_HUNT_GHOST:
            self.widget = widget
            ASUtils.callbackAtFrame(self.widget.compass, 9, self.initUI)

    def reset(self):
        self.widget = None
        self.displayDis = 0
        self.ghostType = 0
        self.result = 0
        self.position = [0, 0, 0]
        self.areaId = 0
        self.state = 0
        self.countDownTimer = None
        self.lastCheckResult = 0
        self.tickId = 0
        self.areaList = []
        self.genflag = False
        self.curFlashBoxId = 0
        self.bigBoxInfo = {}
        self.huntGhostInfo = {}
        self.bigBoxCount = 0
        self.msgPushed = False

    def initUI(self, *args):
        if not self.widget:
            return
        compass = self.widget.compass
        compass.closeBtn.addEventListener(events.BUTTON_CLICK, self.hide, False, 0, True)
        self.widget.compass.helpIcon.helpKey = SCD.data.get('huntGhostHelpKey', 0)
        self.widget.hit = compass.hit
        compass.leftDesc.text = HGCD.data.get('HUNT_GHOST_LEFT_DESC', gameStrings.HUNT_GHOST_LEFT_DESC)
        compass.target.visible = False
        compass.downBtn.addEventListener(events.BUTTON_CLICK, self.handleDownBtnClick, False, 0, True)
        TipManager.addTip(compass.downBtn, gameStrings.HUNT_GHOST_DOWN_TIP)
        compass.upBtn.addEventListener(events.BUTTON_CLICK, self.handleUpBtnClick, False, 0, True)
        TipManager.addTip(compass.upBtn, gameStrings.HUNT_GHOST_UP_TIP)
        compass.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleRewardBtnClick, False, 0, True)
        compass.naviBtn.addEventListener(events.BUTTON_CLICK, self.handleNaviBtnClick, False, 0, True)
        BigWorld.player().cell.getHuntGhostSpawnPoint()
        BigWorld.player().cell.getBigBoxLeftCount()
        self.refreshInfo()
        self.refreshMaskState()
        self.refreshScore()

    def hide(self, destroy = True, *args):
        if not self.widget:
            return
        else:
            if self.countDownTimer:
                BigWorld.cancelCallback(self.countDownTimer)
                self.countDownTimer = None
            self.widget.compass.gotoAndPlay('close')
            ASUtils.callbackAtFrame(self.widget.compass, 16, self.clearWidget)
            self.widget = None
            return

    def clearWidget(self, *args):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_HUNT_GHOST)

    def show(self, *args):
        if not self.isOpen():
            return
        if not self.widget:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_HUNT_GHOST)

    def onStartActivity(self, areaIdList):
        gamelog.debug('yedawang### onStartActivity', areaIdList)
        self.areaList = areaIdList
        gameglobal.rds.ui.topBar.refreshTopBarWidgets()
        self.startTick()
        self.msgPushed = False
        self.pushMessage()

    def startTick(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.lastCheckResult = 0
        self.tickId = tickManager.addTick(1, self.checkLoop)

    def onStopActivity(self):
        gamelog.debug('yedawang### onStopActivity')
        gameglobal.rds.ui.topBar.refreshTopBarWidgets()
        self.showPicTips(False)
        self.stopTick()
        self.hide()
        self.removePushMsg()
        self.reset()

    def stopTick(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = 0
        self.lastCheckResult = 0

    def checkLoop(self):
        p = BigWorld.player()
        checkResult = self.isInHuntGhostArea()
        if self.lastCheckResult != checkResult:
            self.lastCheckResult = checkResult
            p.showGameMsg(GMDD.data.ON_ENTER_HUNT_GHOST_AREA, ())
            self.checkHuntGhostPK()
        if self.lastCheckResult == self.areaId and not self.genflag:
            self.createHuntGhostFlagBox()

    def isInHuntGhostArea(self):
        if not self.isOpen():
            return 0
        p = BigWorld.player()
        for id in self.areaList:
            info = HGAD.data.get(id, {})
            leftUpPos = info.get('posLeftUp', ())
            rightDownPos = info.get('posRightDown', ())
            if len(leftUpPos) == 3 and len(rightDownPos) == 3 and leftUpPos[0] <= p.position[0] <= rightDownPos[0] and rightDownPos[2] <= p.position[2] <= leftUpPos[2]:
                return id

        return 0

    def getHuntGhostAreaBounds(self):
        areaBoundList = []
        for id in self.areaList:
            area = HGAD.data.get(id, {})
            areaBound = [0,
             0,
             0,
             0]
            posLeftUp = area.get('posLeftUp', ())
            posRightDown = area.get('posRightDown', ())
            if posLeftUp:
                areaBound[0] = posLeftUp[0]
                areaBound[1] = posLeftUp[2]
            if posRightDown:
                areaBound[2] = posRightDown[0]
                areaBound[3] = posRightDown[2]
            areaBoundList.append(areaBound)

        return areaBoundList

    def checkHuntGhostPK(self):
        BigWorld.player().cell.checkHuntGhostPK()

    def createHuntGhostFlagBox(self):
        if self.state != STATE_DEFAULT:
            BigWorld.player().cell.createHuntGhostFlagBox()

    def onHuntGhostFlagCreateOk(self):
        self.genflag = True

    def showPicTips(self, isStart):
        if isStart:
            gameglobal.rds.ui.showPicTip(gametypes.HUNT_GHOST_START_TIPS)
        else:
            gameglobal.rds.ui.showPicTip(gametypes.HUNT_GHOST_END_TIPS)

    def refreshHuntGhostInfo(self):
        self.refreshScore()

    def refreshInfo(self, *args):
        if not self.widget:
            return
        self.refreshResult()

    def refreshResult(self):
        gamelog.debug('yedawang### refreshResult', self.state)
        if not self.widget:
            return
        compass = self.widget.compass
        if not compass:
            return
        if self.countDownTimer:
            return
        exploreResult = compass.exploreResult
        if self.state == STATE_DEFAULT:
            exploreResult.gotoAndStop('result6')
            compass.point.visible = False
            compass.tips.visible = False
            compass.naviBtn.visible = False
            self.setTargetVisible(False)
            exploreResult.huntBtn.addEventListener(events.BUTTON_CLICK, self.handleHuntBtnClick, False, 0, True)
        elif self.state == STATE_START_NAVI:
            exploreResult.gotoAndStop('result5')
            compass.point.visible = False
            compass.tips.visible = False
            compass.naviBtn.visible = False
            self.setTargetVisible(True)
            exploreResult.naviBtn.addEventListener(events.BUTTON_CLICK, self.handleNaviBtnClick, False, 0, True)
        else:
            compass.naviBtn.visible = True
            compass.point.visible = True
            self.setTargetVisible(True)
            p = BigWorld.player()
            distance = distance2D(p.position, self.position)
            distanceGrading = HGCD.data.get('distanceGrading', (500.0, 100.0, 15.0))
            self.displayDis = distanceGrading[0]
            if distance > self.displayDis:
                self.result = RESULT_TYPE_FAR
                resultName = 'result0'
            elif distance > distanceGrading[1]:
                self.result = RESULT_TYPE_MIDDLE
                resultName = 'result1'
            elif distance > distanceGrading[2]:
                self.result = RESULT_TYPE_NEAR
                resultName = 'result2'
            else:
                self.result = RESULT_TYPE_DESTINATION
                self.setTargetVisible(False)
                if self.ghostType == GHOST_TYPE_SPECIAL:
                    resultName = 'result3'
                else:
                    resultName = 'result4'
            exploreResult.gotoAndStop(resultName)
        self.refreshTargetPosition()
        if self.state >= STATE_NAVI:
            BigWorld.callback(2, self.refreshResult)

    def setTargetVisible(self, visible):
        target = self.widget.compass.target
        if not target:
            return
        if visible:
            target.alpha = 1
            target.visible = True
            target.gotoAndStop('ghost%d' % self.ghostType)
        else:
            target.visible = False

    def onGetBigBoxLeftCount(self, bigBoxCount, bigBoxInfo):
        self.bigBoxCount = bigBoxCount
        self.refreshScore()
        self.addAreaLeftTips(bigBoxInfo)
        self.bigBoxInfo = {}
        for areaId, info in bigBoxInfo.iteritems():
            boxData = info.get('bigBoxData', {})
            for entId, boxInfo in boxData.iteritems():
                bornTime, pointId = boxInfo
                pos = HGAPD.data.get(pointId, {}).get('position', (0, 0, 0))
                self.bigBoxInfo[entId] = (bornTime, pos)
                boxEnt = BigWorld.entities.get(entId)
                if boxEnt and boxEnt.topLogo:
                    existTime = bornTime + HGCD.data.get('BigBoxExistTime', 120) - utils.getNow()
                    boxEnt.topLogo.startNameCountDown(existTime)

    def addAreaLeftTips(self, bigBoxInfo):
        if not self.widget:
            return
        areaText = ''
        for areaId, info in bigBoxInfo.iteritems():
            areaName = HGAD.data.get(areaId, {}).get('name', '')
            boxCount = info.get('bigBoxCount', 0)
            leftCount = HGCD.data.get('bigGhostMaxNum', 5) - boxCount
            text = gameStrings.HUNT_GHOST_LEFT_TIP % (areaName, leftCount)
            areaText += text

        TipManager.addTip(self.widget.compass.leftDesc, HGCD.data.get('HUNT_GHOST_LEFT_TIPS', '%s') % areaText)

    def refreshScore(self):
        if not self.widget:
            return
        self.huntGhostInfo = BigWorld.player().huntGhostInfo
        rewardTimes = self.huntGhostInfo.get(const.HUNT_GHOST_TREASURE_BOX_TYPE_SMALL, 0)
        if self.bigBoxCount >= 0:
            leftNumMc = self.widget.compass.leftNum
            leftNumMc.text = self.bigBoxCount
            leftDescMc = self.widget.compass.leftDesc
            self.widget.compass.leftNum.x = leftDescMc.x + leftDescMc.textWidth + leftNumMc.textWidth - leftNumMc.width + 10
        totalTimes = HGCD.data.get('totalRewardTimes', 5)
        if rewardTimes >= 0:
            self.widget.compass.rewardBtn.label = '%d/%d' % (rewardTimes, totalTimes)

    def showTip(self, txt):
        self.widget.compass.tips.text = txt

    def onGetGhostPos(self, areaId, ghostPoint):
        if self.state == STATE_DEFAULT:
            self.state = STATE_START_NAVI
        self.areaId = areaId
        pointData = HGAPD.data.get(ghostPoint, {})
        self.position = pointData.get('position', [0, 0, 0])
        self.refreshInfo()

    def onFindGhostTreasureBox(self, areaId, ghostPoint, type):
        self.state = STATE_BOX
        self.ghostType = type - 1
        self.areaId = areaId
        pointData = HGAPD.data.get(ghostPoint, {})
        self.position = pointData.get('position', [0, 0, 0])
        self.refreshInfo()

    def onCancelGhost(self):
        if not self.isOpen():
            return
        if BigWorld.player().isPathfinding and navigator.getNav().seekDest == Math.Vector3(self.position):
            navigator.getNav().stopPathFinding()
        if self.state != STATE_DEFAULT:
            BigWorld.player().showGameMsg(GMDD.data.HUNT_GHOST_BOX_DISAPPEAR, ())
        self.state = STATE_DEFAULT
        self.ghostType = 0
        self.position = [0, 0, 0]
        self.genflag = False
        self.refreshInfo()

    def refreshTargetPosition(self):
        if not self.widget:
            return
        compass = self.widget.compass
        if not compass:
            return
        p = BigWorld.player()
        isMouseMode = False
        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.MOUSE_MODE:
            isMouseMode = True
        playerPos = p.position
        playerRot = p.yaw * 180 / 3.14
        cameraRot = BigWorld.camera().direction.yaw * 180 / 3.14
        if self.result == RESULT_TYPE_FAR:
            panelDis = VIEW_RAD
        else:
            scale = VIEW_RAD / self.displayDis
            panelDis = distance2D(playerPos, self.position) * scale
        pointRot = self.getTargetDirection() * 180 / 3.14 - cameraRot
        compass.target.x = math.sin(pointRot / 180 * 3.14) * panelDis
        compass.target.y = -math.cos(pointRot / 180 * 3.14) * panelDis
        self.widget.compass.tips.visible = self.state == STATE_NAVI
        compass.point.rotation = pointRot

    def onExploreGhostToGenBox(self):
        self.state = STATE_BOX

    def setGhostType(self, type):
        self.ghostType = type - 1

    def onBigGhostAppear(self, treasureBoxId, *args):
        if not self.widget:
            return
        if self.countDownTimer and treasureBoxId != self.curFlashBoxId:
            BigWorld.callback(1, Functor(self.onBigGhostAppear, treasureBoxId))
        else:
            exploreResult = self.widget.compass.exploreResult
            exploreResult.gotoAndStop('result8')
            self.refreshBtnCountDown(4)
            self.curFlashBoxId = treasureBoxId

    def onGhostAppear(self, treasureBoxId):
        if not self.widget:
            return
        if self.countDownTimer and treasureBoxId != self.curFlashBoxId:
            BigWorld.callback(1, self.onGhostAppear)
        else:
            exploreResult = self.widget.compass.exploreResult
            exploreResult.gotoAndStop('result7')
            self.refreshBtnCountDown(4)
            self.curFlashBoxId = treasureBoxId

    def refreshBtnCountDown(self, leftTime):
        if not self.widget:
            return
        else:
            if leftTime > 0:
                leftTime -= 1
                countDownText = self.widget.compass.exploreResult.countDown
                if countDownText:
                    countDownText.text = '%ds' % leftTime
                self.widget.compass.target.visible = False
                self.widget.compass.point.visible = False
                self.widget.compass.tips.visible = False
                self.countDownTimer = BigWorld.callback(1, Functor(self.refreshBtnCountDown, leftTime))
            if leftTime <= 0:
                if self.countDownTimer:
                    BigWorld.cancelCallback(self.countDownTimer)
                    self.countDownTimer = None
                self.refreshInfo()
            return

    def setNaviState(self, isNavi):
        if self.state < STATE_BOX:
            if self.state == STATE_NAVI and not isNavi and self.result != RESULT_TYPE_DESTINATION:
                self.state = STATE_START_NAVI
            if isNavi and BigWorld.player().isPathfinding and navigator.getNav().seekDest == Math.Vector3(self.position):
                self.state = STATE_NAVI
        self.refreshResult()

    def refreshMaskState(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if not p or not getattr(p, 'chatAnonymity', {}):
            self.widget.compass.downBtn.visible = False
            self.widget.compass.upBtn.visible = True
        if p.chatAnonymity.has_key(gametypes.AnonymousType_huntGhost):
            self.widget.compass.downBtn.visible = True
            self.widget.compass.upBtn.visible = False
        else:
            self.widget.compass.downBtn.visible = False
            self.widget.compass.upBtn.visible = True

    def isOpen(self):
        if not gameglobal.rds.configData.get('enableHuntGhost', False):
            return False
        if not huntGhostCommon.checkinHuntGhostTime():
            return False
        if BigWorld.player().spaceNo != const.SPACE_NO_BIG_WORLD:
            return False
        return True

    def handleRewardBtnClick(self, *args):
        gameglobal.rds.ui.generalReward.show(gametypes.GENERAL_REWARD_HUNT_GHOST)

    def handleAbandonBtnClick(self, *args):
        if self.state in [STATE_DEFAULT, STATE_BOX]:
            msg = uiUtils.getTextFromGMD(GMDD.data.CANNOT_RELEASE_GHOST_REQUEST, '')
            gameglobal.rds.ui.messageBox.showMsgBox(msg)
            return
        p = BigWorld.player()
        msg = uiUtils.getTextFromGMD(GMDD.data.RELEASE_GHOST_REQUEST, gameStrings.HUNT_GHOST_RELEASE_GHOST)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.releaseGhostRequest)

    def handleDownBtnClick(self, *args):
        msg = uiUtils.getTextFromGMD(GMDD.data.HUNT_GHOST_MASK_DOWN, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, BigWorld.player().cell.delHuntGhostMaskName)

    def handleUpBtnClick(self, *args):
        msg = uiUtils.getTextFromGMD(GMDD.data.HUNT_GHOST_MASK_UP, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, BigWorld.player().cell.huntGhostMaskNameRequest)

    def handleHuntBtnClick(self, *args):
        p = BigWorld.player()
        if not p.isInTeamOrGroup():
            msg = uiUtils.getTextFromGMD(GMDD.data.HUNT_GHOST_BUILD_GROUP, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(gameglobal.rds.ui.team.quickCreateGroup, gametypes.TEAM_REASON_HUNT_GHOST))
        else:
            p.cell.huntGhostRequest()

    def handleNaviBtnClick(self, *args):
        position = self.position
        if position:
            pos = Math.Vector3(position)
            uiUtils.findPosByPos(const.SPACE_NO_BIG_WORLD, pos)
            if self.state < STATE_NAVI:
                self.state = STATE_NAVI
            self.refreshInfo()

    def getTargetDirection(self):
        p = BigWorld.player()
        faceDir = Math.Vector2(math.sin(p.yaw), math.cos(p.yaw))
        dstDir = Math.Vector2(self.position[0] - p.position[0], self.position[2] - p.position[2])
        dstDir.normalise()
        dot = faceDir.dot(dstDir)
        theta = math.asin(limit(faceDir.cross2D(dstDir), -1, 1))
        theta = theta if dot > 0 else math.pi - theta
        return p.yaw - theta

    def pushMessage(self):
        if not self.isOpen():
            return
        if self.msgPushed:
            return
        pushId = HGCD.data.get('huntGhostPushId', uiConst.MESSAGE_TYPE_HUNT_GHOST)
        if pushId not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': self.onPushMsgClick})

    def removePushMsg(self):
        pushId = HGCD.data.get('huntGhostPushId', uiConst.MESSAGE_TYPE_HUNT_GHOST)
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def onPushMsgClick(self):
        if not self.widget:
            self.show()
            self.msgPushed = True
