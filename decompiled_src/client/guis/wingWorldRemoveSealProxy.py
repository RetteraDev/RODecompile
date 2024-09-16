#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldRemoveSealProxy.o
from random import choice
import BigWorld
import gamelog
import gameglobal
import uiConst
import utils
from guis import uiUtils
from uiProxy import UIProxy
from helpers import cgPlayer
from guis import events
from guis.asObject import ASObject
from data import wing_world_config_data as WWCD
MIN_STAGE = 1
MAX_STAGE = 12
ICON_COMMON_PATH = 'wingWorld/%s.dds'
FRAME_NAMES = ('unstart', 'ing', 'done')
UNSTART = 0
ING = 1
DONE = 2
SHINE_OFFSET = 6
BAR_WIDTH = 180

class WingWorldRemoveSealProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldRemoveSealProxy, self).__init__(uiAdapter)
        self.widget = None
        self.cgPlayer = None
        self.info = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WINGWORLD_REMOVESEAL, self.hide)

    def reset(self):
        self.cgPlayer and self.cgPlayer.endMovie()
        self.cgPlayer = None
        self.isMoviePlaying = False

    def clearAll(self):
        self.info = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WINGWORLD_REMOVESEAL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WINGWORLD_REMOVESEAL)

    def show(self):
        p = BigWorld.player()
        p.cell.queryWingWorldOpenStageInfo()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WINGWORLD_REMOVESEAL)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.extraMc.donateBtn.addEventListener(events.BUTTON_CLICK, self.onDonateBtnClick, False, 0, True)

    def playMovie(self):
        if not self.widget:
            return
        if not self.checkVideoShow():
            self.widget.videoPanel.videoLoader.visible = False
            return
        if self.isMoviePlaying:
            return
        self.isMoviePlaying = True
        self.playSound()
        self.widget.videoPanel.videoLoader.visible = True
        config = {'position': (0, 0),
         'w': 308,
         'h': 308,
         'loop': True,
         'screenRelative': False,
         'verticalAnchor': 'TOP',
         'horizontalAnchor': 'RIGHT'}
        if not self.cgPlayer:
            self.cgPlayer = cgPlayer.UIMoviePlayer('gui/widgets/WingWorldRemoveSealWidget' + self.uiAdapter.getUIExt(), 'WingWorldRemoveSeal_MovieLoader', 308, 308)
        curStage = min(MAX_STAGE, self.info.get('openStage', 1))
        videoName = self.getMovieName(curStage)
        self.cgPlayer.playMovie(videoName, config)

    def getMovieName(self, curStage):
        return WWCD.data.get('wingWorldBossVideo', {}).get(curStage, '')

    def checkVideoShow(self):
        if self.info.get('openStage', 0) > MAX_STAGE:
            return True
        else:
            isOpen = self.info.get('isOpen', False)
            isFull = self.info.get('openDonate', 0) == self.info.get('openDonateLimit', 1)
            return isOpen and isFull

    def onQueryInfo(self, openStage, isOpen, openDonate, openDonateLimit):
        self.info['openStage'] = openStage
        self.info['isOpen'] = isOpen
        self.info['openDonate'] = openDonate
        self.info['openDonateLimit'] = openDonateLimit
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshUI()
        self.playMovie()
        gamelog.info('nqb@wingWorldRemoveSealProxy.DonateInfo', self.info)

    def refreshUI(self):
        self.refreshIconInfo()
        self.refreshExtraInfo()

    def refreshIconInfo(self):
        if not self.widget:
            return
        openStage = self.info.get('openStage', MIN_STAGE)
        isOpen = self.info.get('isOpen', False)
        for stage in xrange(MIN_STAGE, MAX_STAGE + 1):
            iconMc = getattr(self.widget, 'icon%d' % stage)
            if stage > openStage:
                state = UNSTART
            elif stage == openStage:
                state = ING if isOpen else UNSTART
            else:
                state = DONE
            iconMc.gotoAndStop(FRAME_NAMES[state])
            iconMc.icon.icon.gotoAndStop('stage_%d' % stage)

        self.widget.videoPanel.bg.fitSize = True
        self.widget.videoPanel.bg.loadImage(ICON_COMMON_PATH % min(openStage, MAX_STAGE))

    def refreshExtraInfo(self):
        if not self.widget:
            return
        isOpen = self.info.get('isOpen', False)
        openStage = self.info.get('openStage', MIN_STAGE)
        openDonate = self.info.get('openDonate', 0)
        openDonateLimit = self.info.get('openDonateLimit', 1)
        extraMc = self.widget.extraMc
        pieceNum = self.getDonatePieceNum()
        if openStage > MAX_STAGE:
            extraMc.gotoAndStop('allDone')
            extraMc.hintText.htmlText = WWCD.data.get('removeSealAllDoneHintText', 'AllDone')
        elif isOpen and openDonate < openDonateLimit:
            extraMc.gotoAndStop('ing')
            extraMc.donateBtn.enabled = bool(pieceNum)
            extraMc.progressbar.currentValue = openDonate
            extraMc.progressbar.maxValue = openDonateLimit
            extraMc.pieceNumTf.text = pieceNum
            self.relayoutPieceInfo()
        elif not isOpen:
            extraMc.gotoAndStop('unstart')
            extraMc.pieceNumTf.text = pieceNum
            extraMc.donateBtn.enabled = False
            self.relayoutPieceInfo()
            extraMc.hintText.htmlText = WWCD.data.get('removeSealUnStartHintText', 'unstart')
        else:
            extraMc.gotoAndStop('done')
            extraMc.donateBtn.enabled = bool(pieceNum)
            extraMc.hintText.htmlText = WWCD.data.get('removeSealDoneHintText', 'done')
        extraMc.bossNameMc.gotoAndStop('stage_%d' % openStage)

    def relayoutPieceInfo(self):
        extraMc = self.widget.extraMc
        extraMc.pieceNumTf.width = extraMc.pieceNumTf.textWidth
        extraMc.pieceNumTf.x = (extraMc.pieceNumTf.parent.width - extraMc.pieceNumTf.width) / 2
        extraMc.pieceIcon.x = extraMc.pieceNumTf.x - extraMc.pieceIcon.width

    def getDonatePieceNum(self):
        itemId = WWCD.data.get('wwSubmitItemId', 411408)
        return BigWorld.player().inv.countItemInPages(itemId)

    def onDonateBtnClick(self, *args):
        itemId = WWCD.data.get('wwSubmitItemId', 411408)
        pieceNum = self.getDonatePieceNum()
        msg = WWCD.data.get('donateHintText', 'donate')
        gameglobal.rds.ui.messageBox.showCounterMsgBox(msg, self.onDonate, counterData=uiUtils.getGfxItemById(itemId), counterRange=(0, pieceNum))
        if gameglobal.rds.ui.systemPush.mediator:
            widget = ASObject(gameglobal.rds.ui.systemPush.mediator).getWidget()
            if widget and not widget.visible:
                widget.visible = True

    def onDonate(self, cnt):
        openStage = self.info.get('openStage', 1)
        BigWorld.player().cell.wingWorldSubmitStart(openStage, cnt)

    def onDonateSuccess(self, openDonate):
        if not self.widget:
            return
        progressbar = self.widget.extraMc.progressbar
        if not progressbar or not progressbar.shine:
            return
        self.info['openDonate'] = openDonate
        progressbar.shine.gotoAndPlay('start')
        percent = self.info.get('openDonate', 0) / float(self.info.get('openDonateLimit', 1))
        progressbar.shine.width = SHINE_OFFSET + percent * BAR_WIDTH
        self.refreshInfo()

    def playSound(self):
        stage = self.info['openStage']
        soundIds = WWCD.data.get('videoSoundId', {}).get(stage, ())
        if soundIds:
            soundId = choice(soundIds)
            gameglobal.rds.sound.playSound(soundId)

    def checkWingWorldRemoveMileStone(self, typeStr):
        if typeStr == 'open':
            mileStoneId = WWCD.data.get('mileStoneId', 10002)
            needMsg = True
        elif typeStr == 'finish':
            mileStoneId = WWCD.data.get('finishMileStoneId', 19008)
            needMsg = False
        return BigWorld.player().checkServerProgress(mileStoneId, needMsg)

    def isWingWorldDiGongExist(self):
        curTime = utils.getNow()
        p = BigWorld.player()
        wwBossMlgNo = getattr(p, 'wwBossMlgNo', 0)
        endTime = getattr(p, 'destroyDiGongTime', curTime)
        isWingWorldDiongExist = wwBossMlgNo and curTime <= endTime
        return isWingWorldDiongExist
