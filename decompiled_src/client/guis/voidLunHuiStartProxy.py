#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidLunHuiStartProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import utils
from helpers import tickManager
from uiProxy import UIProxy
from guis import events
from guis.asObject import TipManager
from guis import tipUtils
from data import team_endless_config_data as TECD
from data import fb_data as FD
from guis import voidLunHuiHelper
STATE_EMPTY = 0
STATE_APPLY = 1
STATE_REFUSE = 2
PLAYER_MAX_NUM = 5
MAX_BUFF_NUM = 4
BUFF_X_START = -9
BUFF_MC_WIDTH = 42
MEMBER_MC_WIDTH = 66
HEAD_START = 23

class VoidLunHuiStartProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoidLunHuiStartProxy, self).__init__(uiAdapter)
        self.widget = None
        self.tickId = 0
        self.fbType = 0
        self.diffIdx = 0
        self.fbNo = 0
        self.propList = []
        self.playerInfo = {}
        self.endTime = 0
        self.totalTime = 0
        self.isCanceled = False
        self.cancelReason = 0
        self.startData = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_LUNHUI_START, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_LUNHUI_START:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VOID_LUNHUI_START)

    def show(self, startData = None):
        if startData:
            self.startData = startData
            self.diffIdx = self.startData.get('teamEndlessLv', 0)
            self.fbNo = self.startData.get('fbNo', 0)
            self.propList = voidLunHuiHelper.getInstance().getPropList(self.diffIdx)
            self.endTime = self.startData.get('endTime', 0)
            self.totalTime = self.startData.get('endTime', 0) - utils.getNow()
            self.isCanceled = False
            self.cancelReason = 0
            self.initPlayerInfo()
        self.removePushMsg()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_VOID_LUNHUI_START)
        else:
            self.refreshInfo()

    def initPlayerInfo(self):
        self.playerInfo = self.startData.get('players', [])
        for gbid in self.playerInfo:
            self.playerInfo[gbid]['state'] = STATE_EMPTY

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onCloseBtnClick)
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.onRewardBtnClick)
        self.widget.startBtn.addEventListener(events.BUTTON_CLICK, self.onApllyBtnClick)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.onCancelBtnClick)
        self.widget.progress.lableVisible = False
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = tickManager.addTick(1, self.refreshProgress)

    def refreshProgress(self):
        if not self.widget:
            return
        if not self.totalTime or not self.endTime:
            return
        remainTime = self.endTime - utils.getNow()
        if remainTime < 0:
            remainTime = 0
        progress = remainTime
        self.widget.progress.maxValue = self.totalTime
        self.widget.progress.currentValue = progress
        if remainTime == 0:
            self.removePushMsg()
            self.hide()

    def onRewardBtnClick(self, *args):
        lvKey = voidLunHuiHelper.getInstance().getLvKey(self.fbNo)
        gameglobal.rds.ui.voidLunHuiRewardQuery.show(lvKey, self.diffIdx)

    def refreshPlayerState(self):
        gbIds = self.playerInfo.keys()
        for i in xrange(PLAYER_MAX_NUM):
            memberMc = self.widget.heads.getChildByName('member%d' % i)
            if i < len(gbIds):
                memberMc.visible = True
                gbId = gbIds[i]
                info = self.playerInfo[gbId]
                self.setPlayerInfo(memberMc, info)
            else:
                memberMc.visible = False

        moveX = HEAD_START + (PLAYER_MAX_NUM - len(gbIds)) * MEMBER_MC_WIDTH / 2
        self.widget.heads.x = moveX
        p = BigWorld.player()
        if self.playerInfo.get(p.gbId).get('state', 0) != STATE_EMPTY:
            self.widget.startBtn.enabled = False
        else:
            self.widget.startBtn.enabled = True

    def onCloseBtnClick(self, *args):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_LUNHUI_START)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_LUNHUI_START, {'click': self.onPushMsgClick})
        self.hide()

    def onPushMsgClick(self):
        self.show()

    def removePushMsg(self):
        if uiConst.MESSAGE_TYPE_LUNHUI_START in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_LUNHUI_START)

    def onPlayerReady(self, gbId):
        playerInfo = self.playerInfo.get(gbId, {})
        playerInfo['state'] = STATE_APPLY
        self.refreshInfo()

    def onPlayerRefuse(self, gbId):
        playerInfo = self.playerInfo.get(gbId, {})
        playerInfo['state'] = STATE_REFUSE
        self.isCanceled = True
        p = BigWorld.player()
        if p.gbId == gbId:
            self.clearAll()
        else:
            self.refreshInfo()

    def onConfirmCanceled(self, reason):
        self.isCanceled = True
        self.cancelReason = reason

    def onApllyBtnClick(self, *args):
        p = BigWorld.player()
        if self.isCanceled:
            self.clearAll()
        else:
            p.cell.confirmEnterTeamEndless(self.fbNo, self.diffIdx)

    def onCancelBtnClick(self, *args):
        p = BigWorld.player()
        if self.playerInfo.get(p.gbId).get('state', 0) != STATE_EMPTY or self.isCanceled:
            self.clearAll()
        else:
            p.cell.cancelEnterTeamEndless(self.fbNo, self.diffIdx)

    def refreshInfo(self):
        if not self.widget:
            return
        fbName = FD.data.get(self.fbNo, {}).get('name', '')
        self.widget.fubenName.textField.text = fbName
        self.widget.difficutyText.textField.text = self.diffIdx
        for i in xrange(MAX_BUFF_NUM):
            buffMc = self.widget.buffsMc.getChildByName('buff%d' % i)
            if buffMc:
                if i < len(self.propList):
                    buffMc.visible = True
                    propId = self.propList[i]
                    voidLunHuiHelper.getInstance().setCiZhuiInfo(buffMc.icon, propId)
                else:
                    buffMc.visible = False

        moveX = (MAX_BUFF_NUM - len(self.propList)) * BUFF_MC_WIDTH / 2
        self.widget.buffsMc.x = moveX
        self.refreshPlayerState()
        lvKey = voidLunHuiHelper.getInstance().getLvKey(self.fbNo)
        remainTime = voidLunHuiHelper.getInstance().getRemainRewardTime(lvKey)
        self.widget.rewardTime.text = remainTime
        tipText = TECD.data.get('teamEndlessRewardRemainTip', 'remain:%d')
        TipManager.addTip(self.widget.rewardIcon, tipText % remainTime)

    def clearAll(self):
        self.hide()
        self.removePushMsg()

    def setPlayerInfo(self, playerMc, playerInfo):
        school = playerInfo.get('school', 0)
        sex = playerInfo.get('sex', 0)
        state = playerInfo.get('state', 0)
        gbId = playerInfo.get('gbId', 0)
        photoUrl = playerInfo.get('photo', '')
        playerMc.gbId = gbId
        playerMc.job.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school, 'yuxu'))
        playerMc.state.visible = True
        name = playerInfo.get('roleName', 0)
        TipManager.addTip(playerMc, name, tipUtils.TYPE_DEFAULT_BLACK)
        if state == STATE_APPLY:
            playerMc.state.gotoAndPlay('gou')
        elif state == STATE_REFUSE:
            playerMc.state.gotoAndPlay('cha')
        else:
            playerMc.state.visible = False
        if uiUtils.isDownloadImage(photoUrl):
            playerMc.head.photo.fitSize = True
            playerMc.head.photo.imgType = uiConst.IMG_TYPE_NOS_FILE
            playerMc.head.photo.url = photoUrl
        else:
            photo = utils.getDefaultPhoto(school, sex)
            playerMc.head.photo.fitSize = True
            playerMc.head.photo.loadImage(photo)
