#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTopFightProxy.o
import BigWorld
from helpers import charRes
import formula
import const
import commcalc
from helpers import capturePhoto
from callbackHelper import Functor
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import TipManager
import gametypes
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from data import school_top_config_data as STCD
from cdata import game_msg_def_data as GMDD
STATE_LOADING = 1
STAGE_LOADED = 2

class SchoolTopFightProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTopFightProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.leftHeadGens = None
        self.rightHeadGens = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TOP_FIGHT, self.hide)

    def reset(self):
        self.leftImgState = STATE_LOADING
        self.rightImgState = STATE_LOADING

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TOP_FIGHT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        if self.leftHeadGens:
            self.leftHeadGens.endCapture()
        if self.rightHeadGens:
            self.rightHeadGens.endCapture()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TOP_FIGHT)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TOP_FIGHT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.fightObserver.addEventListener(events.BUTTON_CLICK, self.handleFightOberverBtnClick, False, 0, True)
        self.leftHeadGens = capturePhoto.SchoolTopPhotoGen('gui/taskmask.tga', 320, 'SchoolTopFight_LeftUnit')
        self.leftHeadGens.initFlashMesh()
        self.leftHeadGens.startCaptureDummy()
        self.leftHeadGens.setModelFinishCallback(Functor(self.headGensLoadedCallback, True))
        self.rightHeadGens = capturePhoto.SchoolTopPhotoGen('gui/taskmask.tga', 320, 'SchoolTopFight_RightUnit')
        self.rightHeadGens.initFlashMesh()
        self.rightHeadGens.startCaptureDummy()
        self.rightHeadGens.setModelFinishCallback(Functor(self.headGensLoadedCallback, False))
        self.widget.guess.guessLeft.addEventListener(events.BUTTON_CLICK, self.handleGuess, False, 0, True)
        self.widget.guess.guessRight.addEventListener(events.BUTTON_CLICK, self.handleGuess, False, 0, True)
        TipManager.addTip(self.widget.guess.guessHint, gameStrings.SCHOOL_TOP_GUESS_HINT)

    def headGensLoadedCallback(self, isLeft):
        if isLeft:
            self.leftImgState = STAGE_LOADED
        else:
            self.rightImgState = STAGE_LOADED
        self.refreshInfo()

    def getPlayersData(self):
        p = BigWorld.player()
        schoolTopFullClientData = getattr(p, 'schoolTopFullClientData', None)
        if not schoolTopFullClientData:
            return [None, None]
        elif len(schoolTopFullClientData) == 1:
            return [self.formateData(schoolTopFullClientData[0]), None]
        else:
            return [self.formateData(schoolTopFullClientData[0]), self.formateData(schoolTopFullClientData[1])]

    def formateData(self, clientData):
        return [clientData['name'],
         clientData.get('lv', 0),
         clientData['physique'],
         clientData['aspect'],
         clientData['avatarConfig'],
         clientData['signal']]

    def setPlayerData(self, playerData, playerMc, headGen):
        if not playerData:
            playerMc.playerName.text = ''
            playerMc.playerSchool.visible = False
            playerMc.playerImg.visible = False
        else:
            name = playerData[0]
            lv = playerData[1]
            physique = playerData[2]
            aspect = playerData[3]
            school = physique.school
            avatarConfig = playerData[4]
            signal = playerData[5]
            playerMc.playerSchool.visible = True
            playerMc.playerImg.visible = True
            playerMc.playerName.text = name
            playerMc.playerSchool.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school, 'yuxu'))
            modelId = charRes.transBodyType(physique.sex, physique.bodyType)
            showFashion = commcalc.getSingleBit(signal, gametypes.SIGNAL_SHOW_FASHION)
            headGen.startCaptureRes(modelId, aspect, physique, avatarConfig, self.getAvatarPhotoAct(physique), showFashion)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        leftPlayerData, rightPlayerData = self.getPlayersData()
        if self.leftImgState == STAGE_LOADED:
            self.widget.leftLoading.visible = False
        else:
            self.widget.leftLoading.visible = True
            self.widget.leftPlayer.playerImg.x = 80
            self.setPlayerData(leftPlayerData, self.widget.leftPlayer, self.leftHeadGens)
        if self.rightImgState == STAGE_LOADED:
            self.widget.rightLoading.visible = False
        else:
            self.widget.rightLoading.visible = True
            self.widget.rightPlayer.playerImg.x = 80
            self.setPlayerData(rightPlayerData, self.widget.rightPlayer, self.rightHeadGens)
        finalCandidates = getattr(p, 'finalCandidates', [])
        hadSelf = False
        for info in finalCandidates:
            if info.get('gbId', 0) == p.gbId:
                hadSelf = True

        self.widget.fightObserver.label = gameStrings.SCHOOL_TOP_FIGHT_ENTER if hadSelf else gameStrings.SCHOOL_TOP_FIGHT_OB
        p = BigWorld.player()
        p.base.querySchoolTopGuessInfo()
        self.waitForServerResponse()

    def handleFightOberverBtnClick(self, *args):
        p = BigWorld.player()
        if formula.getFubenNo(p.spaceNo) == const.FB_NO_SCHOOL_TOP_MATCH:
            p.showGameMsg(GMDD.data.SCHOOL_TOP_IN_MATCH_FUBEN, ())
            return
        BigWorld.player().cell.applySchoolTopMatch()
        self.hide()

    def getAvatarPhotoAct(self, physique):
        playerActions = STCD.data.get('schoolTopPlayerActions', {})
        if playerActions == None:
            playerActions = {}
        modelId = charRes.transBodyType(physique.sex, physique.bodyType)
        action = (playerActions.get((modelId, physique.school), '1101'),)
        return action

    def checkGuessState(self):
        p = BigWorld.player()
        p.base.querySchoolTopGuessInfo()
        schoolTopGuessData = getattr(p, 'schoolTopGuessData', None)
        if schoolTopGuessData['choosedRole'] == 0:
            self.widget.leftPlayer.support.visible = False
            self.widget.rightPlayer.support.visible = False
            self.widget.guess.leftText.text = '?%'
            self.widget.guess.rightText.text = '?%'
            self.widget.guess.guessSlider.currentValue = 50
        else:
            if schoolTopGuessData['choosedRole'] == schoolTopGuessData['other']['gbId']:
                self.widget.leftPlayer.support.visible = True
                self.widget.rightPlayer.support.visible = False
            else:
                self.widget.leftPlayer.support.visible = False
                self.widget.rightPlayer.support.visible = True
            self.widget.guess.guessLeft.disabled = True
            self.widget.guess.guessRight.disabled = True
            attackPercent = int(100 * (1.0 * schoolTopGuessData['other']['guessCnt'] / (schoolTopGuessData['other']['guessCnt'] + schoolTopGuessData['schoolTop']['guessCnt'])) + 0.5)
            self.widget.guess.leftText.text = '%d%%' % attackPercent
            self.widget.guess.rightText.text = '%d%%' % (100 - attackPercent)
            self.widget.guess.guessSlider.currentValue = attackPercent

    def handleGuess(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc == self.widget.guess.guessLeft:
            msg = gameStrings.SCHOOL_TOP_GUESS_CONFIRM % gameStrings.SCHOOL_TOP_GUESS_ATK
        else:
            msg = gameStrings.SCHOOL_TOP_GUESS_CONFIRM % gameStrings.SCHOOL_TOP_GUESS_DEF
        p = BigWorld.player()
        schoolTopStage = p.schoolTopStage
        if schoolTopStage.get(p.school, None) == gametypes.SCHOOL_TOP_STAGE_MATCH_PREPARE:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.yesCallback, itemMc), noCallback=self.noCallback)
        else:
            msg = gameStrings.SCHOOL_TOP_FIGHT_STARTED
            gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def yesCallback(self, itemMc):
        p = BigWorld.player()
        if itemMc == self.widget.guess.guessLeft:
            schoolTopGuessData = getattr(p, 'schoolTopGuessData', None)
            p.base.guessSchoolTopWinner(schoolTopGuessData['other']['gbId'])
        else:
            schoolTopGuessData = getattr(p, 'schoolTopGuessData', None)
            p.base.guessSchoolTopWinner(schoolTopGuessData['schoolTop']['gbId'])
        BigWorld.callback(0.1, self.waitForServerGuessResult)

    def noCallback(self):
        pass

    def waitForServerGuessResult(self):
        p = BigWorld.player()
        p.base.querySchoolTopGuessInfo()
        schoolTopGuessData = getattr(p, 'schoolTopGuessData', None)
        if schoolTopGuessData['choosedRole'] == 0:
            BigWorld.callback(0.1, self.waitForServerGuessResult)
        else:
            BigWorld.callback(0, self.checkGuessState)

    def waitForServerResponse(self):
        p = BigWorld.player()
        if hasattr(p, 'schoolTopGuessData'):
            self.checkGuessState()
        else:
            BigWorld.callback(0.1, self.waitForServerResponse)
