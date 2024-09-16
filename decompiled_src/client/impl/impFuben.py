#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impFuben.o
from gamestrings import gameStrings
import zlib
import cPickle
import copy
import BigWorld
import Sound
import Math
import gamelog
import gameglobal
import gametypes
import const
import formula
import utils
from sfx import sfx
from guis import messageBoxProxy, uiConst
from guis import chickenFoodFactory
from helpers import camera
from helpers import loadingProgress
from callbackHelper import Functor
from fbStatistics import FubenStats
from guis import uiUtils
from appSetting import Obj as AppSettings
from guis.asObject import MenuManager
from gamestrings import gameStrings
from guis import groupDetailFactory
from guis import events
from cdata import game_msg_def_data as GMDD
from cdata import group_fb_menu_data as GFMD
from data import fb_data as FD
from data import challenge_mission_data as CMD
from data import fb_ui_data as FUD
from data import sys_config_data as SCD
from data import isolate_config_data as ICD
from data import monster_data as MD
from data import map_config_data as MCD
from data import group_label_data as GLD
from data import zmj_fuben_config_data as ZFCD
ANOTHER_CALLBACK = 1
GOAL_TYPE_FUBEN = 1

class ImpFuben(object):

    def fbLose(self, fbNo):
        pass

    def cameraModify(self, battleState):
        gamelog.debug('@szh cameraModify', battleState)
        if battleState:
            camera.instance().enterBossBattle()
        else:
            camera.instance().quitBossBattle()

    def showFubenMode(self, transportEntId, fbInfo):
        fbInfo = cPickle.loads(zlib.decompress(fbInfo))
        gamelog.debug('zt:showFbSelectDialog', fbInfo)
        if self.life != gametypes.LIFE_DEAD:
            if fbInfo.get('openUI', None):
                self.showUIdToWidget(int(fbInfo['openUI']))
            else:
                gameglobal.rds.ui.fubenLogin.show(transportEntId, fbInfo)

    def showUIdToWidget(self, widgetId):
        if widgetId == uiConst.WIDGET_VOID_DREAMLAND:
            if not gameglobal.rds.ui.voidDreamland.widget:
                gameglobal.rds.ui.voidDreamland.show()

    def onGetFubenEnterHelpInfo(self, fbNo, fbInfo):
        if fbInfo.get('fbHelp', False):
            gameglobal.rds.ui.fubenDegree.open(fbNo, fbInfo.get('shishenMode', 3), True)
        else:
            BigWorld.player().cell.enterExistFuben(fbNo)

    def startFbCountDown(self, time):
        gamelog.debug('jorsef: startFbCountDown', time)

    def showCountDown(self, wave, counts, isShowWave):
        gamelog.debug('@szh: showCountDown', wave)
        if wave == 0:
            gameglobal.rds.ui.towerDefense.hideCountDown()
        else:
            gameglobal.rds.ui.towerDefense.hideCountDown()
            gameglobal.rds.ui.towerDefense.curWave = wave - 1
            gameglobal.rds.ui.towerDefense.setShowCurWave(not not isShowWave)
            gameglobal.rds.ui.towerDefense.setTime(counts)
            gameglobal.rds.ui.towerDefense.showCountDown()

    def showScores(self, win, info):
        gamelog.debug('jorsef: showCountDown', win, info)
        gameglobal.rds.ui.towerDefense.result = win
        gameglobal.rds.ui.towerDefense.info = info
        gameglobal.rds.ui.towerDefense.showTdResult()

    def showSpeedFbCountDown(self, countDown):
        if countDown >= 15:
            delay = countDown - 15
            if delay:
                BigWorld.callback(delay, Functor(self.showSpeedFbCountDown, countDown - delay))
            else:
                self.callArenaMsg('showCountDown15', (15,))
                BigWorld.callback(1, Functor(self.showSpeedFbCountDown, countDown - 1))
        elif countDown >= 10:
            delay = countDown - 10
            if delay:
                BigWorld.callback(delay, Functor(self.showSpeedFbCountDown, countDown - delay))
            else:
                self.callArenaMsg('showCountDown15', (10,))
                BigWorld.callback(1, Functor(self.showSpeedFbCountDown, countDown - 1))
        elif countDown >= 5:
            delay = countDown - 5
            if delay:
                BigWorld.callback(delay, Functor(self.showSpeedFbCountDown, countDown - delay))
            else:
                self.callArenaMsg('showCountDown5', (5,))
                BigWorld.callback(1, Functor(self.showSpeedFbCountDown, countDown - 1))
        elif countDown > 0:
            self.callArenaMsg('showCountDown5', (countDown,))
            BigWorld.callback(1, Functor(self.showSpeedFbCountDown, countDown - 1))
        elif countDown < 0:
            gameglobal.rds.ui.arena.closeArenaCountDown()

    def speedFbWillStart(self, countDown):
        gamelog.debug('zt: fubenWillstatr', countDown)
        if countDown > 0:
            self.fubenClockCommand(const.CLOCK_SHOW, (0,))
            gameglobal.rds.ui.arena.openArenaMsg()
            self.showSpeedFbCountDown(countDown)
        else:
            gameglobal.rds.ui.fubenClock.showClock(uiConst.FUBEN_MAIN_CLOCK, False, -countDown)

    def fubenClockCommand(self, cmd, args):
        gamelog.debug('zt: fubenClockCommand', cmd, args)
        if cmd == const.CLOCK_SHOW:
            gameglobal.rds.ui.fubenClock.showClock(uiConst.FUBEN_MAIN_CLOCK, False, args[0], False)
        elif cmd == const.CLOCK_CLOSE:
            gameglobal.rds.ui.fubenClock.hide()
        elif cmd == const.CLOCK_STOP:
            gameglobal.rds.ui.fubenClock.stopTimer(uiConst.FUBEN_MAIN_CLOCK, args[0])
        elif cmd == const.CLOCK_START:
            gameglobal.rds.ui.fubenClock.setTimer(uiConst.FUBEN_MAIN_CLOCK, False, args[0])

    def showFubenClock(self, isShow, times):
        gamelog.debug('@szh showFubenClock', isShow, times)
        if isShow == 1:
            gameglobal.rds.ui.fubenClock.showClock(uiConst.FUBEN_MAIN_CLOCK, False, times)
        elif isShow == 0:
            gameglobal.rds.ui.fubenClock.hide()
        elif isShow == 2:
            gameglobal.rds.ui.fubenClock.stopTimer(uiConst.FUBEN_MAIN_CLOCK, times)

    def showGuideMsg(self, transportId, fbNo):
        fbName = formula.getFbDetailName(fbNo)
        guideLowLv, guideUpLv = utils.getFubenGuideLvs(self, fbNo)
        msg = gameStrings.TEXT_IMPFUBEN_161 % fbName
        msg += gameStrings.TEXT_IMPFUBEN_162 % (guideUpLv, guideUpLv)
        msg += gameStrings.TEXT_IMPFUBEN_163 % guideLowLv
        msg += gameStrings.TEXT_IMPFUBEN_164 % guideLowLv
        if self.fbGuideModeLoginInfo(fbNo)[0] == gametypes.FB_GUIDE_SUC:
            if self.lv >= guideUpLv:
                self.cell.checkFbGuideCnt(fbNo, transportId)
            else:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : self.cell.fbModeSelected(transportId, fbNo, 1, 0, 0))
        else:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : self.showGuideWarningMsg(transportId, fbNo))

    def showGuideWarningMsg(self, transportId, fbNo):
        guideLowLv, guideUpLv = utils.getFubenGuideLvs(self, fbNo)
        msg = gameStrings.TEXT_IMPFUBEN_176 % (guideLowLv, guideUpLv)
        msg += gameStrings.TEXT_IMPFUBEN_177
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : self.cell.fbModeSelected(transportId, fbNo, 1, 0, 0))

    def showGuideCntWarningMsg(self, transportId, fbNo):
        msg = gameStrings.TEXT_IMPFUBEN_182
        msg += gameStrings.TEXT_IMPFUBEN_177
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : self.cell.fbModeSelected(transportId, fbNo, 1, 0, 0))

    def onCheckFbGuideCntFail(self, fbNo, transportId):
        self.showGuideCntWarningMsg(transportId, fbNo)

    def messageBoxEnter(self, fbNo):
        if self.inCombat:
            self.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_INCOMBAT, ())
        elif self.life == gametypes.LIFE_DEAD:
            self.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_DEAD, ())
        elif formula.spaceInFuben(self.spaceNo):
            self.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_INFB, ())
        elif formula.spaceInDuel(self.spaceNo):
            self.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_IN_BATTLEFIELD, ())
        else:
            gamelog.debug('zt: enter fuben from messageBox', fbNo)
            p = BigWorld.player()
            if getattr(self, 'msgBoxId', None):
                gameglobal.rds.ui.messageBox.dismiss(self.msgBoxId, needDissMissCallBack=False)
            if p.isArenaMatching():
                p.confirmCancelApplyArena(formula.getFbDetailName(fbNo), Functor(p.cell.enterFubenAfterHeaderApply, fbNo, False))
            else:
                p.cell.enterFubenAfterHeaderApply(fbNo, False)
            if hasattr(self, 'autoDismissCallback'):
                BigWorld.cancelCallback(self.autoDismissCallback)

    def messageBoxCancel(self):
        if hasattr(self, 'autoDismissCallback'):
            BigWorld.cancelCallback(self.autoDismissCallback)
        if getattr(self, 'inGroupFollow', None):
            self.cell.cancelGroupFollow()

    def messageBoxAutoDismiss(self, msgBoxId):
        gameglobal.rds.ui.messageBox.dismiss(msgBoxId, needDissMissCallBack=False)
        if hasattr(self, 'autoDismissCallback'):
            BigWorld.cancelCallback(self.autoDismissCallback)

    def onFubenOccupied(self, fbNo, guideMode, shishenMode, fbHelp):
        gamelog.debug('zt:onFubenOccupied', fbNo)
        fbData = FD.data.get(fbNo, {})
        if fbData.get('isDirectlyEnter'):
            if self.carrier.isRunningState() and self.carrier.getCarrierEnt():
                self.messageBoxEnter(fbNo)
            return
        elif self.inGroupFollow and AppSettings.get('conf/ui/GroupFollowHeaderCall/isAutoEnterFuben', 1):
            BigWorld.callback(1, Functor(self.messageBoxEnter, fbNo))
            return
        else:
            fbInfo = gameglobal.rds.ui.fubenLogin.fbInfo
            noShishenModeSelect = fbData.get('noShishenModeSelect', 0)
            if gameglobal.rds.ui.fubenLogin.isShow:
                if fbNo in fbInfo.get('fbList', ()):
                    gameglobal.rds.ui.fubenLogin.update({'currentFb': fbNo})
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_IMPARENA_582, Functor(self.messageBoxEnter, fbNo), True, False), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, self.messageBoxCancel)]
            fbName = formula.getFbDetailName(fbNo)
            enableHelpMode = gameglobal.rds.configData.get('enableFubenHelpMode', False)
            if guideMode:
                msg = uiUtils.getTextFromGMD(GMDD.data.ENTER_FUBEN_COMFIRM_GUIDE_MODE, gameStrings.TEXT_IMPFUBEN_251) % fbName
                self.msgBoxId = gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_FUBENDEGREEPROXY_56, msg, buttons)
            else:
                shishenMode = shishenMode if shishenMode < 4 else 4
                if noShishenModeSelect == 1 and fbHelp == 1:
                    self.enterShishenInNewWay(fbNo, 3, fbHelp)
                elif shishenMode > 0:
                    if enableHelpMode and shishenMode < 4:
                        self.enterShishenInNewWay(fbNo, shishenMode, fbHelp)
                    else:
                        self.enterShishenInOldWay(fbNo, fbName, shishenMode)
                else:
                    msg = uiUtils.getTextFromGMD(GMDD.data.ENTER_FUBEN_COMFIRM_NORMAL_MODE, gameStrings.TEXT_IMPFUBEN_263) % fbName
                    if hasattr(self, 'msgBoxId') and self.msgBoxId:
                        gameglobal.rds.ui.messageBox.dismiss(self.msgBoxId)
                        self.msgBoxId = None
                    self.msgBoxId = gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_FUBENDEGREEPROXY_56, msg, buttons)
            if hasattr(self, 'msgBoxId'):
                self.autoDismissCallback = BigWorld.callback(30, Functor(self.messageBoxAutoDismiss, self.msgBoxId))
            return

    def enterShishenInOldWay(self, fbNo, fbName, shishenMode):
        shishenMode = shishenMode if shishenMode < 4 else 4
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_IMPARENA_582, Functor(self.messageBoxEnter, fbNo), True, False), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, self.messageBoxCancel)]
        fbMode = SCD.data.get('fubenModeNames', ['',
         gameStrings.TEXT_QUESTTRACKPROXY_1748,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_1,
         gameStrings.TEXT_QUESTTRACKPROXY_1748_2,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_3])
        shishenModeStr = fbMode[shishenMode]
        msg = uiUtils.getTextFromGMD(GMDD.data.ENTER_FUBEN_COMFIRM_SHISHEN_MODE, gameStrings.TEXT_IMPFUBEN_279) % (fbName, shishenModeStr)
        self.msgBoxId = gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_FUBENDEGREEPROXY_56, msg, buttons)

    def enterShishenInNewWay(self, fbNo, shishenMode, helpMode):
        gameglobal.rds.ui.fubenDegree.open(fbNo, shishenMode, helpMode)

    def onFbApplyChecked(self, fbNo, notMatchNum, matchScoreFlag):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AVATAR_6426, Functor(self.afterFbApplyCheck, fbNo), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None)]
        msg = ''
        if notMatchNum > 0:
            msg += gameStrings.TEXT_IMPFUBEN_291 % notMatchNum
        if not matchScoreFlag:
            fbType = formula.whatFubenType(fbNo)
            if fbType in const.FB_TYPE_SINGLE_SET:
                msg += gameStrings.TEXT_IMPFUBEN_295
            else:
                msg += gameStrings.TEXT_IMPFUBEN_297
        msg += gameStrings.TEXT_IMPFUBEN_298
        self.msgBoxId = gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPFUBEN_300, msg, buttons)

    def afterFbApplyCheck(self, fbNo):
        self.cell.applyFubenNoDoubleCheck(fbNo)

    def onFbProgressChecked(self, fbNo, pg, fbVars):
        if gameglobal.rds.configData.get('enableNewFubenProgress', True):
            gameglobal.rds.ui.fubenProgress.show(fbNo, pg, fbVars)
        else:
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton(gameStrings.TEXT_IMPARENA_582, Functor(self.afterFbProgressCheck, fbNo, True, pg, fbVars), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, Functor(self.afterFbProgressCheck, fbNo, False, pg, fbVars), True, True)]
            msg = gameStrings.TEXT_IMPFUBEN_312
            self.msgBoxId = gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPFUBEN_314, msg, buttons)

    def afterFbProgressCheck(self, fbNo, fCover, pg, fbVars):
        self.cell.enterFubenAfterProgressCheck(fbNo, fCover, zlib.compress(cPickle.dumps(pg, -1)), zlib.compress(cPickle.dumps(fbVars, -1)))

    def onFubenDestroy(self, fbNo):
        if gameglobal.rds.ui.fubenLogin.isShow:
            gameglobal.rds.ui.fubenLogin.update({})

    def onFbDestroyByHeaderChecked(self, fbNo, membersIn):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_GM_COMMAND_WINGWORLD_1215, Functor(self.afterCheckForDestroyFbByHeader, fbNo), True, False), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None)]
        msg = ''
        if membersIn > 0:
            msg += gameStrings.TEXT_IMPFUBEN_329 % membersIn
        elif FD.data.get(fbNo, {}).get('longterm', 0) > 0:
            msg += gameStrings.TEXT_IMPFUBEN_331
        else:
            msg += gameStrings.TEXT_IMPFUBEN_333
        self.msgBoxId = gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPFUBEN_335, msg, buttons)

    def afterCheckForDestroyFbByHeader(self, fbNo):
        self.cell.destroyFbByHeader(fbNo)
        self.messageBoxAutoDismiss(self.msgBoxId)
        fbInfo = gameglobal.rds.ui.fubenLogin.fbInfo
        if fbInfo.has_key('canDestroyInfo') and fbInfo['canDestroyInfo'].has_key(fbNo):
            fbInfo['canDestroyInfo'].pop(fbNo)
            gameglobal.rds.ui.fubenLogin.refreshFubenBtn()
            if FD.data.get(fbNo).get('longterm', 0) > 0:
                gameglobal.rds.ui.fubenLogin.dismiss()

    def showEvaluation(self, spaceNo, evalInfo):
        gamelog.debug('yedawang### showEvaluation', spaceNo, evalInfo)
        if self.spaceNo != spaceNo:
            return
        fbNo = formula.getFubenNo(spaceNo)
        gameglobal.rds.tutorial.onFinishFb(fbNo)
        if self.inFbHelp:
            return
        if fbNo == const.FB_NO_SCHOOL_TOP_DPS:
            return
        if fbNo == const.FB_NO_XUNLIANCHANG_QUANZHIYE:
            gameglobal.rds.ui.trainingFubenEval.showFubenEval(evalInfo)
        elif fbNo in (const.FB_NO_GUILD_FUBEN, const.FB_NO_GUILD_FUBEN_ELITE):
            gameglobal.rds.ui.guildMembersFbResult.show(fbNo, evalInfo)
        elif FD.data.get(fbNo, {}).get('isPhaseFb'):
            gameglobal.rds.ui.phaseFuben.showFubenResult(fbNo, evalInfo)
        elif formula.inZMJFubenSpace(spaceNo):
            fbNo = formula.getFubenNo(spaceNo)
            if formula.inZMJHighFuben(fbNo):
                gameglobal.rds.ui.zmjBigBossResult.show(evalInfo)
            elif formula.inZMJStarBossFuben(fbNo):
                gameglobal.rds.ui.zmjLittleBossResult.show(evalInfo, fbNo)
            elif formula.inZMJLowFuben(fbNo):
                gameglobal.rds.ui.zmjLittleBossResult.show(evalInfo)
        elif formula.inMapGameFuben(fbNo):
            gameglobal.rds.ui.mapGameFBResult.show(fbNo, evalInfo)
        else:
            gameglobal.rds.ui.fuben.showFubenEval(evalInfo)

    def showSkyWingEvaluation(self, fbType, evalInfo):
        gameglobal.rds.ui.ransackResult.showEvaluation(fbType, evalInfo)

    def sendFbAward(self, fbAwardData):
        gamelog.debug('@zs sendFbAward', fbAwardData)
        part, award = fbAwardData
        if not self.fbAward:
            self.fbAward = [None] * const.FB_REWARD_COUNT
        if part >= 0:
            self.fbAward[part] = award
        else:
            for i in range(const.FB_REWARD_COUNT):
                if not self.fbAward[i]:
                    self.fbAward[i] = award
                    break

        if self.fbAward.count(None) == 0:
            gameglobal.rds.ui.fuben.showRewardItem()
            self.fbAward = []

    def onFbMapLoaded(self):
        loadingProgress.instance().onServerLoaded()

    def onMissionStart(self, iNormalMission, missionId, leftTime, isClockStop):
        cmd = CMD.data[missionId]
        gameglobal.rds.ui.fuben.hide()
        targetMsg = [ (x, '') for x in cmd.get('tgts', []) ]
        gameglobal.rds.ui.fuben.showFubenTarget(targetMsg, iNormalMission)
        gameglobal.rds.ui.fubenClock.hide(1)
        gameglobal.rds.ui.fubenClock.showClock(1, True, leftTime, not isClockStop)
        comType = cmd['comType']
        if comType in [const.FB_CHALLENGE_COMPLETE_TIMELIMIT, const.FB_CHALLENGE_COMPLETE_TIMEPERSIST]:
            timeLimit = cmd['comArgs']
            gameglobal.rds.ui.fubenClock.showClock(0, True, timeLimit)
        gameglobal.rds.ui.trainingFubenEval.hide()
        gameglobal.rds.ui.sidiGuide.missionStart(iNormalMission, missionId)
        self.playTeleportSpellLeave()

    def onMissionEnd(self, iNormalMission, missionId, spaceNo, evalInfo, succ, leftTime):
        gameglobal.rds.ui.fuben.hide()
        gameglobal.rds.ui.fubenClock.hideClock(0)
        if gameglobal.rds.ui.fubenClock.getMediatorByType(1):
            gameglobal.rds.ui.fubenClock.setTimer(1, True, leftTime)
            gameglobal.rds.ui.fubenClock.stopTimer(1)
        else:
            gameglobal.rds.ui.fubenClock.showClock(1, True, leftTime, False)
        baseScore = int(sum([ evalInfo.get(s, 0) for s in (const.FB_EVAL_TYPE_ATTACK, const.FB_EVAL_TYPE_DEFENCE) ]))
        timeScore = evalInfo.get(const.FB_EVAL_TYPE_COMP, 0)
        extra = int(evalInfo.get(const.FB_EVAL_TYPE_EXTRA, 0))
        socre = gameStrings.TEXT_IMPFUBEN_448 % (baseScore + timeScore, extra)
        msg = [(gameStrings.TEXT_IMPFUBEN_449, socre)]
        gameglobal.rds.ui.fuben.showFubenOneResult(msg, iNormalMission, succ)
        gameglobal.rds.ui.sidiGuide.missionEnd(iNormalMission, missionId, baseScore, timeScore, extra, succ)

    def onAllMissionEnd(self, score, oldRank, newRank):
        gameglobal.rds.ui.fuben.showFubenTotalResult(score, oldRank, newRank)
        gameglobal.rds.ui.sidiGuide.missionAllEnd()

    def missionRestart(self, missionId, missionLeftTime, totalLeftTime, isClockStop):
        gameglobal.rds.ui.fubenClock.showClock(1, True, totalLeftTime, not isClockStop)
        if missionLeftTime > 0:
            gameglobal.rds.ui.fubenClock.showClock(0, True, missionLeftTime)

    def onTrainingFubenBossDie(self, charType):
        gamelog.debug('@hjx training#onTrainingFubenMonsterDie', charType)

    def onFbBossHistory(self, bossHistory, bossScores, bossWeekScores):
        gameglobal.rds.ui.trainingArea.initData(bossHistory, bossScores, bossWeekScores)

    def onFbItemModify(self, fbItemData):
        gameglobal.rds.ui.fubenInfo.refreshFubenItem(fbItemData)

    def playFxFromFubenAI(self, srcEntIds, dstEntIds, fxType, fxParams):
        srcEnts = [ BigWorld.entities[srcId] for srcId in srcEntIds if BigWorld.entities.has_key(srcId) ]
        dstEnts = [ BigWorld.entities[dstId] for dstId in dstEntIds if BigWorld.entities.has_key(dstId) ]
        if fxType == 1:
            fxId, speed, startPosBias, targetNodeName, curverate = fxParams
            for srcEnt in srcEnts:
                for dstEnt in dstEnts:
                    flyer = sfx.FlyToNode(None)
                    attachedEffect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (1,
                     gameglobal.EFF_HIGHEST_PRIORITY,
                     flyer.model,
                     fxId,
                     sfx.EFFECT_LIMIT,
                     -1,
                     dstEnt.position))
                    startPos = srcEnt.position + Math.Vector3(0, startPosBias, 0)
                    if targetNodeName:
                        targetNode = dstEnt.model.node(targetNodeName)
                    else:
                        targetNode = dstEnt.model.node('Scene Root')
                    flyer.start(startPos, targetNode, curverate, 0, speed, attachedEffect, 0, True, Math.Vector3(0.0, 0.0, 0.0), None, None, (), self)

        elif fxType == 2:
            fxId, lastTime, startNodeName, endNodeName = fxParams
            for srcEnt in srcEnts:
                for dstEnt in dstEnts:
                    if startNodeName:
                        startNode = srcEnt.model.node(startNodeName)
                    else:
                        startNode = srcEnt.model.node(gameglobal.HIT_NODE_MAP[gameglobal.NORMAL_HIT])
                    if endNodeName:
                        endNode = dstEnt.model.node(endNodeName)
                    else:
                        endNode, endNodeName = dstEnt.getHitNodePairRandom()
                    eff = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (1,
                     startNode,
                     fxId,
                     endNode,
                     30,
                     gameglobal.EFF_HIGHEST_PRIORITY))
                    BigWorld.callback(lastTime, Functor(self.releaseFxFromFubenAI, eff))

    def releaseFxFromFubenAI(self, eff):
        if eff:
            eff.release()

    def onLeaveFuben(self, fbNo):
        gameglobal.rds.ui.towerDefense.hide()
        gameglobal.rds.ui.fubenClock.hide()
        gameglobal.rds.ui.fuben.hide()
        gameglobal.rds.ui.fuben.cancelCallback()
        gameglobal.rds.ui.fubenInfo.hide()
        gameglobal.rds.ui.fubenStat.hide()
        gameglobal.rds.ui.fubenStat.reset()
        gameglobal.rds.ui.fubenGuide.hide()
        self.refreshFbTeacherGuideBuff()
        gameglobal.rds.ui.multiBossBlood.hide()
        gameglobal.rds.ui.questTrack.resetFubenTargetGuideInfo()
        gameglobal.rds.ui.sidiGuide.missionAllEnd()
        if gameglobal.rds.ui.fbDeadData.mediator:
            gameglobal.rds.ui.fbDeadData.hide()
        if gameglobal.rds.ui.fbDeadDetailData.mediator:
            gameglobal.rds.ui.fbDeadDetailData.hide()
        gameglobal.rds.ui.player.setLv(self.lv)
        gameglobal.rds.ui.player.addFbAvoidDieTip()
        self.motionUnpin()
        Sound.stopCues()
        gameglobal.rds.ui.currentShishenMode = 0
        gameglobal.rds.ui.fubenDegree.leaveAndClear()
        gameglobal.rds.ui.monsterBlood.hide()
        gameglobal.rds.ui.fightObserve.closeMonsterBlood()
        gameglobal.rds.ui.sanCun.hide()
        gameglobal.rds.ui.fubenBangDai.hide()
        gameglobal.rds.ui.zhenyao.closeProgressPanel()
        gameglobal.rds.ui.zhenyao.closeFbResult()
        gameglobal.rds.ui.voidDreamlandRank.hide()
        gameglobal.rds.ui.voidDreamlandBar.hide()
        gameglobal.rds.ui.skyWingFuben.hide()
        if not hasattr(self, 'members') or not self.members:
            if gameglobal.rds.ui.teamComm.teamPlayerMed:
                gameglobal.rds.ui.teamComm.closeTeamPlayer()
        chickenFoodFactory.getInstance().closeAllUI()
        gameglobal.rds.ui.questTrack.showFindBeastTrack(False)
        self.removeRebalancePushMsg()
        self.fbExitMsgBoxIds = getattr(self, 'fbExitMsgBoxIds', [])
        for msgBoxId in self.fbExitMsgBoxIds:
            gameglobal.rds.ui.messageBox.dismiss(msgBoxId)

        self.fbExitMsgBoxIds = []
        gameglobal.rds.ui.findBeastLuckJoy.hide()
        gameglobal.rds.ui.schoolTopFubenEval.hide()
        gameglobal.rds.ui.zmjLittleBossResult.hide()
        gameglobal.rds.ui.zmjBigBossResult.hide()
        gameglobal.rds.ui.zmjSpriteEnter.hide()
        gameglobal.rds.ui.zmjSpriteInvite.hide()
        gameglobal.rds.ui.zmjSpriteReward.hide()
        gameglobal.rds.ui.zmjSpriteBuff.hide()
        gameglobal.rds.ui.mapGameFBResult.hide()
        if formula.inMapGameFuben(fbNo):
            BigWorld.callback(1, gameglobal.rds.ui.mapGameMap.show)
        if fbNo == const.FB_NO_FIGHT_FOR_LOVE:
            self.topLogo.hideTitleEffect(False)
            self.topLogo.hideGuildIcon(False)
            gameglobal.rds.ui.fightForLoveRankList.hide()
            gameglobal.rds.ui.fightForLoveRankList.removeFFLScore()
            self.fightForLoveResult = {}
            for k, v in self.fightForLoveMsgIds.iteritems():
                gameglobal.rds.ui.messageBox.dismiss(v, needDissMissCallBack=False)

            self.fightForLoveMsgIds = {}

    def onEnterFuben(self, fbNo):
        filterWidgets = copy.deepcopy(uiConst.FUBEN_FILTER_WIDGETS)
        filterWidgets.extend(uiConst.HUD_WIDGETS)
        multiIdList = []
        for data in gameglobal.rds.ui.bossEnergy.bossID2Data.values():
            if data.get('multiID', 0):
                multiIdList.append(data['multiID'])

        filterWidgets.extend(multiIdList)
        gameglobal.rds.ui.unLoadAllWidget(filterWidgets)
        gameglobal.rds.ui.player.setLv(self.lv)
        gameglobal.rds.ui.player.addFbAvoidDieTip()
        gameglobal.rds.ui.map.realClose()
        for fbInfo in FUD.data.values():
            if fbInfo.get('fubenId') == fbNo and fbInfo.get('uiId'):
                gameglobal.rds.ui.loadWidget(fbInfo.get('uiId'))

        if FD.data.get(fbNo, {}).get('showStatistic'):
            gameglobal.rds.ui.fubenStat.show()
            gameglobal.rds.ui.fubenStat.showHateList()
        if not self.guideDataCheck(fbNo):
            self.openFbGuideFunc = Functor(self.delayOpenFubenGuide, fbNo)
        else:
            self.delayOpenFubenGuide(fbNo)
        gameglobal.rds.ui.fubenInfo.onEnterFuben(fbNo)
        gameglobal.rds.ui.questTrack.hideTrackPanel(False)
        gameglobal.rds.tutorial.onEnterFuben(fbNo)
        if self.noticeShow:
            gameglobal.rds.ui.messageBox.showMsgBox(FD.data.get(fbNo, {}).get('noticeShow', gameStrings.TEXT_IMPFUBEN_624))
            self.noticeShow = False
        if self.fbGuideEffect:
            self.cell.onFbMateAddedCheckGuide()
        if fbNo == const.FB_NO_SPRING_ACTIVITY:
            chickenFoodFactory.getInstance().enterBFY()
        if getattr(self, 'inGroupFollow', None):
            gameglobal.rds.ui.disIndicator.show()
        gameglobal.rds.ui.questTrack.showFindBeastTrack(False)
        self.addRebalancePushMsg(fbNo)
        self.setDynamicSkybox(fbNo)
        if fbNo in const.FB_NO_SKY_WING_LIST:
            gameglobal.rds.ui.skyWingFuben.show()
        if fbNo == const.FB_NO_FIGHT_FOR_LOVE:
            self.topLogo.hideTitleEffect(True)
            self.topLogo.hideGuildIcon(True)
            gameglobal.rds.ui.fightForLoveRankList.show()
            self.fightForLoveResult = {}
        if formula.inZMJLowFuben(fbNo):
            gameglobal.rds.ui.zmjSpriteEnter.show()
            gameglobal.rds.ui.zmjSpriteBuff.show()
        elif formula.inZMJStarBossFuben(fbNo):
            gameglobal.rds.ui.zmjSpriteBuff.show()
        elif formula.inZMJHighFuben(fbNo):
            gameglobal.rds.ui.zmjSpriteBuff.show()

    def delayOpenFubenGuide(self, fbNo):
        self.openFbGuideFunc = None
        if self.isFbGuideMode and self.fbGuideModeLoginInfo(fbNo)[0] == gametypes.FB_GUIDE_SUC:
            gameglobal.rds.ui.fubenGuide.show()
            self.refreshFbTeacherGuideBuff()

    def notifyMonsterPropInfoInFB(self, monsterInfo):
        gameglobal.rds.ui.fubenInfo.refreshFbMonsterInfo(monsterInfo)

    def updateFubenStats(self, spaceNo, memberStats, bossCharTypes):
        if self.spaceNo != spaceNo:
            return
        needRefreshHateView = False
        for gbId, statsDict in memberStats.iteritems():
            if bossCharTypes:
                addTotalStat = True
                for bossCharType in bossCharTypes:
                    gameglobal.rds.ui.fubenStat.updateFbStat(gbId, bossCharType, statsDict, addTotalStat)
                    addTotalStat = False

            else:
                gameglobal.rds.ui.fubenStat.updateFbStat(gbId, 0, statsDict)
            if statsDict.has_key(FubenStats.K_BOSS_HATE):
                needRefreshHateView = True

        gameglobal.rds.ui.fubenStat.setAllHateBoss(bossCharTypes)
        gameglobal.rds.ui.fubenStat.refreshView()
        if needRefreshHateView:
            gameglobal.rds.ui.fubenStat.refreshHateView()

    def resetAvatarCombatStats(self, spaceNo, gbIdList):
        gameglobal.rds.ui.fubenStat.resetAvatarCombatStats(spaceNo, gbIdList)

    def resetBossCombatStats(self, spaceNo, bossCharType):
        gameglobal.rds.ui.fubenStat.resetBossStat(bossCharType)
        self.setDamage(-1, 0)

    def startCalcDps(self):
        self.calcDPS()
        self.dpsCallback = BigWorld.callback(1.0, self.startCalcDps)

    def endCalcDps(self):
        dpsCallback = getattr(self, 'dpsCallback', 0)
        dpsCallback and BigWorld.cancelCallback(dpsCallback)

    def setDamage(self, allDamage, bossDamage):
        if allDamage >= 0:
            self.allDamage = allDamage
        if bossDamage >= 0:
            self.bossDamage = bossDamage

    def incDmg(self, dmg):
        if not formula.spaceInFuben(self.spaceNo):
            return
        if self != BigWorld.player():
            return
        combatStats = gameglobal.rds.ui.fubenStat.fbStatDict.get(self.gbId)
        if not combatStats:
            return
        enterCombatTime = combatStats.getStats(FubenStats.K_MONSTER_ENTER_COMBAT_TIME)
        leaveCombatTime = combatStats.getStats(FubenStats.K_MONSTER_LEAVE_COMBAT_TIME)
        now = self.getServerTime()
        for charType, et in enterCombatTime.iteritems():
            lt = leaveCombatTime.get(charType, 0)
            if et > lt or et <= now <= lt:
                self.bossDamage += dmg
                break

    def calcDPS(self):
        if self != BigWorld.player():
            return
        if not formula.spaceInFuben(self.spaceNo):
            return
        combatStats = gameglobal.rds.ui.fubenStat.fbStatDict.get(self.gbId)
        if not combatStats:
            return
        for stat in gameglobal.rds.ui.fubenStat.fbStatDict.itervalues():
            stat.calcDPS(self.getServerTime())

        enterCombatTime = combatStats.getStats(FubenStats.K_MONSTER_ENTER_COMBAT_TIME)
        leaveCombatTime = combatStats.getStats(FubenStats.K_MONSTER_LEAVE_COMBAT_TIME)
        bossDps = 0
        bossCharType = []
        bossEnterCombatTime = 0
        now = self.getServerTime()
        for charType, et in enterCombatTime.iteritems():
            lt = leaveCombatTime.get(charType, 0)
            if et > lt or et <= now <= lt:
                bossCharType.append(charType)
                bossEnterCombatTime = et

        if bossCharType and bossEnterCombatTime and now > bossEnterCombatTime:
            bossDps = self.bossDamage / (now - bossEnterCombatTime)
        playerEnterCombatTime = combatStats.getStats(FubenStats.K_AVATAR_ENTER_COMBAT_TIME)
        playerLeaveCombatTime = combatStats.getStats(FubenStats.K_AVATAR_LEAVE_COMBAT_TIME)
        dps = 0
        if playerEnterCombatTime > playerLeaveCombatTime or playerEnterCombatTime < now < playerLeaveCombatTime:
            combatTime = combatStats.getStats(FubenStats.K_AVATAR_COMBAT_TIME) + now - playerEnterCombatTime
            dps = int(self.allDamage / combatTime if combatTime > 0 else 0)
        stats = FubenStats()
        if dps > 0:
            stats.record(FubenStats.K_DPS, int(dps))
        if bossCharType:
            stats.record(FubenStats.K_BOSS_COMBAT_DPS, int(bossDps))
        self.updateFubenStats(self.spaceNo, self.gbId, tuple(bossCharType), stats.statsDict)
        self.lastDps = dps
        self.lastBossDps = bossDps

    def dispatchFbUnlockAward(self, fbNo):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_REWARD, {'data': (uiConst.ACT_SPECIAL_AWD, fbNo)})

    def onGetFbUnlockAward(self, fbNo):
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_GET_REWARD, {'data': (uiConst.ACT_SPECIAL_AWD, fbNo)})

    def onQueryFbUnlockInfo(self, fbUnlockInfo):
        self.fbUnlockInfo = {}
        for fbNo, value in fbUnlockInfo.iteritems():
            self.fbUnlockInfo[fbNo] = value

    def showFbRoute(self, showRouteId, routes, hideRouteId, isAffixed = True, ttl = 0):
        self.navigatorRouter.hideLine(hideRouteId)
        self.navigatorRouter.drawLine(showRouteId, routes, isAffixed, ttl)

    def guideDataCheck(self, fbNo, call = True):
        integrity = True
        for gbId, memberInfo in self.members.iteritems():
            if not memberInfo['isOn']:
                continue
            guideData = self.membersGuideCnt.get(gbId, {}).get(fbNo, None)
            if guideData == None:
                if call:
                    BigWorld.player().cell.queryAllMateGuideCnt(fbNo)
                integrity = False
                break

        return integrity

    def onQueryMateGuideCnt(self, fbNo, cnt, gbId):
        memberGuideInfo = self.membersGuideCnt.get(gbId, {})
        memberGuideInfo[fbNo] = cnt
        self.membersGuideCnt[gbId] = memberGuideInfo
        if not self.guideDataCheck(fbNo, False):
            return
        else:
            gameglobal.rds.ui.fubenGuide.refreshInfo()
            self.refreshFbTeacherGuideBuff()
            gameglobal.rds.ui.fubenLogin.refreshGuideIcon()
            showGuideEffectFun = getattr(self, 'checkFbGuideEffectFun', None)
            openGuideFun = getattr(self, 'openFbGuideFunc', None)
            if showGuideEffectFun:
                if not self.inFuben():
                    self.checkFbGuideEffectFun = None
                else:
                    showGuideEffectFun()
            if openGuideFun:
                if not self.inFuben():
                    self.openFbGuideFunc = None
                else:
                    openGuideFun()
            return

    def fbGuideModeLoginInfo(self, fbNo, excludeIds = []):
        fd = FD.data.get(fbNo, {})
        if not fd:
            return (gametypes.FB_GUIDE_FAIL_LEVEL, const.GUIDE_NONE_MODE, [])
        fbGuideMode = fd.get('guideMode', 0)
        fbGuideLowLv, fbGuideUpLv = utils.getFubenGuideLvs(self, fbNo)
        minLv = fd.get('lvMin')
        memberList = []
        mode = const.GUIDE_NONE_MODE
        if self.lv <= fbGuideLowLv and fd.has_key('guideCnt'):
            if not self.fbGuideEffect and self.fbGuideInfo.get(fbNo, 0) >= fd.get('guideCnt', 0):
                return (gametypes.FB_GUIDE_FAIL_TIMES, mode, memberList)
        if len(self.members) <= 1:
            return (gametypes.FB_GUIDE_FAIL_LEVEL, mode, memberList)
        elif self.lv > fbGuideLowLv and self.lv < fbGuideUpLv:
            return (gametypes.FB_GUIDE_FAIL_LEVEL, mode, memberList)
        isLvSatisfied = False
        isTimesSatisfied = False
        isMacSatisfied = False
        selfMacAddress = self.members[self.gbId]['macAddress']
        if self.lv <= fbGuideLowLv and self.lv >= minLv:
            isTimesSatisfied = True
            mode = const.GUIDE_ROOKIE_MODE
            for gbId, member in self.members.iteritems():
                if not member['isOn'] or member['id'] in excludeIds:
                    continue
                if member['level'] >= fbGuideUpLv:
                    isLvSatisfied = True
                    if member['macAddress'] != selfMacAddress:
                        isMacSatisfied = True
                        entity = BigWorld.entities.get(member['id'], None)
                        if entity:
                            if entity.fbGuideEffect == const.GUIDE_MASTER_MODE or fbGuideMode == gametypes.FB_GUIDE_MODE_RANK_DIFF:
                                memberList.append(member)

        elif self.lv >= fbGuideUpLv:
            mode = const.GUIDE_MASTER_MODE
            for gbId, member in self.members.iteritems():
                if not member['isOn'] or member['id'] in excludeIds:
                    continue
                if member['level'] <= fbGuideLowLv and member['level'] >= minLv:
                    isLvSatisfied = True
                    entity = BigWorld.entities.get(member['id'], None)
                    if not (entity and entity.fbGuideEffect) and not self.guideCntCheck(fd, fbNo, gbId):
                        continue
                    else:
                        isTimesSatisfied = True
                        if member['macAddress'] != selfMacAddress:
                            isMacSatisfied = True
                            if entity:
                                if entity.fbGuideEffect == const.GUIDE_ROOKIE_MODE or fbGuideMode == gametypes.FB_GUIDE_MODE_RANK_DIFF:
                                    memberList.append(member)

        if not isLvSatisfied:
            return (gametypes.FB_GUIDE_FAIL_LEVEL, mode, memberList)
        elif not isTimesSatisfied:
            return (gametypes.FB_GUIDE_FAIL_TIMES, mode, memberList)
        elif not isMacSatisfied:
            return (gametypes.FB_GUIDE_FAIL_MAC_SAME, mode, memberList)
        else:
            return (gametypes.FB_GUIDE_SUC, mode, memberList)

    def getfbGuideEffectInfo(self, fbNo):
        guideCntNames = []
        sameMacNames = []
        fd = FD.data[fbNo]
        fbGuideLowLv, fbGuideUpLv = utils.getFubenGuideLvs(self, fbNo)
        minLv = fd.get('lvMin')
        mode = const.GUIDE_NONE_MODE
        memberList = []
        if len(self.members) <= 1:
            return (False, (sameMacNames, guideCntNames))
        if self.lv > fbGuideLowLv and self.lv < fbGuideUpLv:
            return (False, (sameMacNames, guideCntNames))
        if self.lv <= fbGuideLowLv and fd.has_key('guideCnt'):
            if self.fbGuideInfo.get(fbNo, 0) >= fd.get('guideCnt', 0):
                guideCntNames.append(self.roleName)
                return (False, (sameMacNames, guideCntNames))
        selfMacAddress = self.members[self.gbId]['macAddress']
        if self.lv <= fbGuideLowLv and self.lv >= minLv:
            for member in self.members.values():
                if not member['isOn']:
                    continue
                if member['level'] >= fbGuideUpLv:
                    if member['macAddress'] != selfMacAddress:
                        return (True, ([], []))
                    sameMacNames.append(member['roleName'])

        elif self.lv >= fbGuideUpLv:
            for gbid, member in self.members.iteritems():
                if not member['isOn']:
                    continue
                if member['level'] <= fbGuideLowLv and member['level'] >= minLv:
                    if not self.guideCntCheck(fd, fbNo, gbid):
                        continue
                    if member['macAddress'] != selfMacAddress:
                        return (True, ([], []))
                    sameMacNames.append(member['roleName'])

        return (False, (sameMacNames, guideCntNames))

    def guideCntCheck(self, fd, fbId, gbId):
        maxGuideCnt = fd.get('guideCnt', const.MAX_INT32)
        guideCnt = self.membersGuideCnt.get(gbId, {}).get(fbId, 0)
        return guideCnt < maxGuideCnt

    def getGuideMembers(self, fbNo, guideMode):
        ret = []
        for member in self.members.values():
            if not member['isOn']:
                continue
            mate = BigWorld.entities.get(member['id'])
            if mate is None:
                continue
            if mate and mate.fbGuideEffect != guideMode:
                continue
            if guideMode == const.GUIDE_MASTER_MODE:
                ret.append(member)
            elif guideMode == const.GUIDE_ROOKIE_MODE:
                ret.append(member)
            elif guideMode == const.GUIDE_NONE_MODE:
                ret.append(member)

        return ret

    def checkFbGuideEffect(self, newPlayerId):
        self.checkFbGuideEffectFun = None
        fbNo = formula.getFubenNo(self.spaceNo)
        if not fbNo or fbNo not in FD.data:
            return
        else:
            if not self.guideDataCheck(fbNo):
                self.checkFbGuideEffectFun = Functor(self.checkFbGuideEffect, newPlayerId)
            if self.id == newPlayerId:
                if self.fbGuideModeLoginInfo(fbNo)[0] == gametypes.FB_GUIDE_SUC:
                    gameglobal.rds.ui.fubenGuide.show()
                    self.refreshFbTeacherGuideBuff()
            elif not self.fbGuideModeLoginInfo(fbNo, [newPlayerId])[0] == gametypes.FB_GUIDE_SUC and self.fbGuideModeLoginInfo(fbNo)[0] == gametypes.FB_GUIDE_SUC:
                gameglobal.rds.ui.fubenGuide.show()
                self.refreshFbTeacherGuideBuff()
            return

    def sendFubenVars(self, fbNo, stage, info):
        gameglobal.rds.ui.questTrack.updateFubenData(fbNo, stage, info)
        if fbNo in SCD.data.get('sidiFubenList', []):
            gameglobal.rds.ui.sidiGuide.sendFubenVars(fbNo, stage, info)
        if fbNo == const.FB_NO_SC:
            gameglobal.rds.ui.sanCun.setFbInfo(info)
        elif fbNo == const.FB_NO_QINGLINZHENYAO_YUESAI:
            gameglobal.rds.ui.zhenyao.setFbInfo(info)
        elif fbNo == const.FB_NO_QINGLINZHENYAO_PUTONG:
            gameglobal.rds.ui.zhenyao.setFbInfo(info)
        elif fbNo == const.FB_NO_SPRING_ACTIVITY:
            chickenFoodFactory.getInstance().setVars(info)
        elif fbNo in const.FB_TYPE_ENDLESS_CHALLENGE_LIST:
            gameglobal.rds.ui.voidDreamlandBar.setFbInfo(info)
        elif fbNo in const.FB_NO_FLY_UPS:
            gameglobal.rds.ui.flyUpFubenBoss.setFbInfo(info)

    def sendFubenFamesAdded(self, fbNo, scoreLv, famesAdded):
        gameglobal.rds.ui.fuben.setFame(famesAdded)

    def sendFubenEnterInfo(self, fbNo, canEnter):
        gameglobal.rds.ui.playRecomm.onFubenDataBack(fbNo, canEnter)

    def sendFbGuideCnt(self, guideInfo):
        gamelog.info('@szh sendFbGuideCnt', guideInfo)
        self.fbGuideInfo.update(guideInfo)

    def onSetShishenMode(self, currentMode, aimMode):
        if currentMode == aimMode:
            gameglobal.rds.ui.funcNpc.close()
            gameglobal.rds.ui.shishenMode.hide()

    def onGetShishenMode(self, currentMode):
        if FD.data.get(formula.getFubenNo(self.spaceNo), {}).get('noShishenModeSelect', 0):
            return
        gameglobal.rds.ui.currentShishenMode = currentMode
        gameglobal.rds.ui.topBar.refreshTopBarWidgets()
        gameglobal.rds.ui.questTrack.refreshFubenTargetGuideInfo()

    def onGetHighShishenModeCnt(self, fbNo, cnt):
        gameglobal.rds.ui.fubenLogin.updateCrazyShishenModeCnt(fbNo, cnt)
        gameglobal.rds.ui.shishenBoard.updateCrazyShishenModeCnt(fbNo, cnt)

    def onGetFubenSeat(self, fbNo, extra):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AVATAR_6426, Functor(self.applyFubenOnGetQueue, fbNo, extra), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, Functor(self.cancelFubenQueue, fbNo), True, True)]
        gameglobal.rds.ui.fuben.closeFubenQueue()
        msg = gameStrings.TEXT_IMPFUBEN_1052 % (formula.whatFubenName(fbNo),)
        self.msgBoxId = gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPFUBEN_1054, msg, buttons)

    def applyFubenOnGetQueue(self, fbNo, extra):
        self.cell.applyFubenOnGetQueue(fbNo)

    def cancelFubenQueue(self, fbNo):
        self.cell.cancelFubenQueue(fbNo)

    def updateFubenQueue(self, fbNo, rank):
        gameglobal.rds.ui.fuben.showFubenQueue(fbNo, rank)

    def onDiscardFubenQueue(self, fbNo):
        self.showGameMsg(GMDD.data.SINGLE_FB_QUEUE_GIVE_UP, (formula.whatFubenName(fbNo),))
        gameglobal.rds.ui.fuben.closeFubenQueue()

    def onQueryFirstKill(self, fbNo, data, version):
        gameglobal.rds.ui.achvmentDetail.onQueryFirstKill(fbNo, data, version)

    def inFbPunish(self):
        lvl, _ = self.getFbMaxPunishBailInfo()
        return lvl >= 0

    def getFbMaxPunishBailInfo(self):
        if not getattr(self, 'fbPunish', None):
            return (-1, -1)
        else:
            maxLevel = -1
            expireTime = -1
            for fbNo in self.fbPunish.keys():
                if len(self.fbPunish[fbNo]) == 3:
                    startTime, expireTime, _ = self.fbPunish[fbNo]
                    bailLevel = 3
                else:
                    startTime, expireTime, _, bailLevel = self.fbPunish[fbNo][:4]
                if startTime <= utils.getNow() <= expireTime and bailLevel > maxLevel:
                    maxLevel = bailLevel
                    expireTime = expireTime

            return (maxLevel, expireTime)

    def getFreeFbPunishBail(self):
        maxLevel, _ = self.getFbMaxPunishBailInfo()
        if maxLevel < 0:
            return 0
        freeFbPunishBailsInfo = ICD.data.get('freeFbPunishBail', {})
        blockCnt = maxLevel if maxLevel <= max(freeFbPunishBailsInfo.keys()) else max(freeFbPunishBailsInfo.keys())
        return freeFbPunishBailsInfo.get(blockCnt, 0)

    def sendFbPunishInfo(self, res):
        self.fbPunish = cPickle.loads(zlib.decompress(res))

    def sendNonGuideWarning(self):
        msg = SCD.data.get('nonGuideWarningMsg', '')
        gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def sendNotFirstKillWarning(self):
        self.noticeShow = True

    def sendMbPlayerCount(self, mbPlayerCnt):
        gameglobal.rds.ui.fubenLogin.getTogetherFightingState(mbPlayerCnt)

    def notifyGroupFubenRank(self, score, oldRank, newRank, curRank):
        gameglobal.rds.ui.ranking.showTeamRankEval(score, oldRank, curRank)
        gameglobal.rds.ui.zhenyao.setResultRank(curRank)
        gameglobal.rds.ui.zhenyao.showFbResult()
        gameglobal.rds.ui.guildMembersFbResult.updateMyFbRank(curRank)

    def set_fbStatusList(self, old):
        for fbNo in self.fbStatusList:
            if formula.isWingWorldXinMoArenaFb(fbNo):
                if uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_XINMO_ARENA not in gameglobal.rds.ui.pushMessage.msgs:
                    self.onWingWorldXinMoArenaFuBenUpdated()

        filterFuben = gameglobal.rds.ui.phaseFuben.filterFuben(self.fbStatusList)
        if len(filterFuben) == 0:
            gameglobal.rds.ui.phaseFuben.removePhaseFubenMsg(uiConst.MESSAGE_TYPE_PUSH_PHASE_FUBEN)
        else:
            gameglobal.rds.ui.phaseFuben.pushPhaseFubenMsg(uiConst.MESSAGE_TYPE_PUSH_PHASE_FUBEN)
        xinMoBossFbs = []
        for fbNo in filterFuben:
            if formula.isWingWorldXinMoUniqueBossFb(fbNo) or formula.isWingWorldXinMoNormalBossFb(fbNo):
                xinMoBossFbs.append(fbNo)

        if self._isSoul() and xinMoBossFbs:
            gameglobal.rds.ui.phaseFuben.pushPhaseFubenMsg(uiConst.MESSAGE_TYPE_WING_WORLD_XIN_MO_FUBEN)
        else:
            gameglobal.rds.ui.phaseFuben.removePhaseFubenMsg(uiConst.MESSAGE_TYPE_WING_WORLD_XIN_MO_FUBEN)

    def updateFbHelpPlayer(self, fbHelpInfo):
        res = []
        if not fbHelpInfo:
            return
        for roleName, inFbHelp in fbHelpInfo:
            res.append({'roleName': roleName,
             'inFbHelp': inFbHelp})

        gameglobal.rds.ui.fubenBangDai.setBangdaiData(res)
        gameglobal.rds.ui.fubenBangDai.refreshInfo()

    def obGetPlayersBasicInfo(self, groupNUID, groupMemberInfo):
        self.observedMembers = groupMemberInfo

    def obUpdatePlayersInfo(self, groupNUID, result):
        if not hasattr(self, 'observeOthersInfo'):
            self.observeOthersInfo = {}
        for memberGbId, info in result.iteritems():
            if self.observeOthersInfo.has_key(memberGbId):
                self.observeOthersInfo[memberGbId].update(info)
            else:
                self.observeOthersInfo[memberGbId] = info
            if self.observedMembers.has_key(memberGbId):
                self.observedMembers[memberGbId]['id'] = info.get(gametypes.TEAM_SYNC_PROPERTY_ENTID, -1)

        for memberGbId, info in result.iteritems():
            mid = -1
            hp = self.observeOthersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_HP, -1)
            mhp = self.observeOthersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_MHP, -1)
            mp = self.observeOthersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_MP, -1)
            mmp = self.observeOthersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_MMP, -1)
            lv = info.get(gametypes.TEAM_SYNC_PROPERTY_LV, -1)
            spaceNo = BigWorld.player().spaceNo
            pos = info.get(gametypes.TEAM_SYNC_PROPERTY_POSITION)
            roleName = info.get(gametypes.TEAM_SYNC_PROPERTY_ROLENAME)
            chunkName = info.get(gametypes.TEAM_SYNC_PROPERTY_CHUNKNAME)
            teamInfo = (hp,
             mhp,
             mp,
             mmp,
             lv)
            if self == BigWorld.player() and self.inFightObserve():
                self.onReceiveObserveMemberInfo(memberGbId, teamInfo)
                if self.observedMembers.has_key(memberGbId):
                    mid = self.observedMembers[memberGbId]['id']
            if mid == -1:
                continue
            if self.observedMembersPos.has_key(memberGbId):
                spaceNo = spaceNo or self.observedMembersPos[memberGbId][0]
                pos = pos or self.observedMembersPos[memberGbId][1]
                roleName = roleName or self.observedMembersPos[memberGbId][2]
                chunkName = chunkName or self.observedMembersPos[memberGbId][3]
            self.observedMembersPos[memberGbId] = (spaceNo,
             pos,
             roleName,
             chunkName,
             mid)

    def onReceiveObserveMemberInfo(self, memberGbId, info):
        if not self.observedMembers.has_key(memberGbId):
            return
        memberId = self.observedMembers[memberGbId]['id']
        hp, mhp, mp, mmp, lv = info
        for idx, mid in enumerate(gameglobal.rds.ui.teamComm.memberId):
            if mid == memberId:
                gameglobal.rds.ui.teamComm.setOldVal(idx, hp, mhp, mp, mmp, lv)

        gameglobal.rds.ui.teamComm.refreshMemberInfo()

    def updateChickenMealScore(self, totalScore, info):
        gamelog.debug('@zq updateChickenMealScore', totalScore, info)
        chickenFoodFactory.getInstance().setTopRankData(info, 2)

    def onQueryEndlessChallengeInfo(self, challengeInfo):
        """
        \xe6\x8c\x91\xe6\x88\x98\xe4\xb8\xbb\xe7\x95\x8c\xe9\x9d\xa2\xe6\x98\xbe\xe7\xa4\xba\xe4\xbf\xa1\xe6\x81\xaf\xe8\x8e\xb7\xe5\x8f\x96\xe5\x9b\x9e\xe8\xb0\x83
        :param challengeInfo:
        :return:
        """
        gameglobal.rds.ui.voidDreamland.updatelevelItemData(challengeInfo)

    def onGetEndlessChallengeReward(self, rank, progress):
        """
        \xe9\xa2\x86\xe5\x8f\x96\xe5\xa5\x96\xe5\x8a\xb1\xe6\x88\x90\xe5\x8a\x9f\xe5\x90\x8e\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83(\xe4\xb8\xbb\xe8\xa6\x81\xe7\x94\xa8\xe4\xba\x8e\xe7\x95\x8c\xe9\x9d\xa2\xe5\xae\x9d\xe7\xae\xb1\xe7\x8a\xb6\xe6\x80\x81\xe7\x9a\x84\xe6\x98\xbe\xe7\xa4\xba)
        :param rank:
        :param progress:
        :return:
        """
        gameglobal.rds.ui.voidDreamland.updateRewardBoxState(rank, progress)

    def onGetFriendEndlessChallengeTopRank(self, key, friendTopInfo):
        """
        \xe6\x8c\x87\xe5\xae\x9a\xe7\xad\x89\xe7\xba\xa7\xe6\xae\xb5\xe7\x9a\x84\xe5\xa5\xbd\xe5\x8f\x8b\xe6\x8e\x92\xe8\xa1\x8c\xe6\xa6\x9c\xe6\x95\xb0\xe6\x8d\xae
        :param key: \xe7\xad\x89\xe7\xba\xa7\xe6\xae\xb5
        :param friendTopInfo: \xe5\xa5\xbd\xe5\x8f\x8b\xe6\x8e\x92\xe8\xa1\x8c\xe6\xa6\x9c\xe6\x95\xb0\xe6\x8d\xae
        :return:
        """
        info = {'lvKey': key,
         'info': friendTopInfo}
        gameglobal.rds.ui.ranking.updateHuanjingData(info)

    def onEndEndlessChallenge(self, resultInfo):
        """
        \xe4\xb8\x80\xe6\xac\xa1\xe6\x97\xa0\xe5\xb0\xbd\xe5\x89\xaf\xe6\x9c\xac\xe7\x9a\x84\xe7\xbb\x93\xe7\xae\x97\xe5\x9b\x9e\xe8\xb0\x83
        :param resultInfo:
        :return:
        """
        gameglobal.rds.ui.voidDreamlandRank.show(resultInfo)
        gameglobal.rds.ui.voidDreamlandBar.updateEndEndlessBarInfo()

    def onQueryHistoryEndlessTopInfo(self, levelRank, school, historyInfo):
        """
        \xe6\x9f\xa5\xe8\xaf\xa2\xe5\x8e\x86\xe5\xb1\x8a\xe6\x8e\x92\xe8\xa1\x8c\xe6\xa6\x9c\xe6\x95\xb0\xe6\x8d\xae\xe5\x9b\x9e\xe8\xb0\x83
        :param levelRank
        :param school
        :param historyInfo:
        :return:
        """
        info = {'lvKey': levelRank,
         'school': school,
         'info': historyInfo}
        gameglobal.rds.ui.ranking.updateHuanjingData(info)

    def onSetEndlessConfigId(self, configId, progress):
        """
        \xe6\x97\xa0\xe5\xb0\xbd\xe6\x8c\x91\xe6\x88\x98\xe5\x89\xaf\xe6\x9c\xac\xe9\x9a\x8f\xe6\x9c\xba\xe5\x9c\xb0\xe5\x9b\xbe\xe7\x9a\x84\xe4\xbf\xa1\xe6\x81\xaf
        :param configId: endless_challenge_config_reverse_data.py\xe4\xb8\xad\xe7\x9a\x84key\xef\xbc\x8c\xe9\x9c\x80\xe8\xa6\x81\xe4\xbb\x8e\xe4\xb8\xad\xe8\xaf\xbb\xe5\x8f\x96\xe5\xb0\x8f\xe5\x9c\xb0\xe5\x9b\xbe\xe7\x9b\xb8\xe5\x85\xb3\xe4\xbf\xa1\xe6\x81\xaf
        :param progress: \xe9\x9a\xbe\xe5\xba\xa6
        :return:
        """
        self.voidDreamlandConfigId = configId
        self.voidDreamlandProgress = progress

    def onUpdateEndlessMonsterKilledValue(self, endlessShowAni, curKilledValue, totalKilledValue):
        """
        \xe6\x97\xa0\xe5\xb0\xbd\xe6\x8c\x91\xe6\x88\x98\xe6\x80\xaa\xe7\x89\xa9\xe8\xa2\xab\xe6\x9d\x80\xe8\xbf\x9b\xe5\xba\xa6\xe5\x90\x8c\xe6\xad\xa5
        :param curKilledValue: \xe6\x9c\xac\xe6\xac\xa1\xe6\x80\xaa\xe7\x89\xa9\xe8\xa2\xab\xe6\x9d\x80\xe7\x9a\x84\xe8\xbf\x9b\xe5\xba\xa6\xe5\x80\xbc
        :param totalKilledValue: \xe5\xbd\x93\xe5\x89\x8d\xe5\x89\xaf\xe6\x9c\xac\xe6\x80\xbb\xe7\x9a\x84\xe8\xa2\xab\xe6\x9d\x80\xe8\xbf\x9b\xe5\xba\xa6\xe5\x80\xbc
        :return:
        """
        gameglobal.rds.ui.voidDreamlandBar.updateKilledValueBar(curKilledValue, totalKilledValue)
        if endlessShowAni:
            gameglobal.rds.ui.voidDreamlandBar.playEffect()

    def refreshFbTeacherGuideBuff(self):
        teamGuideTeacherBuff = SCD.data.get('fbQuestTeacherBuffId', 0)
        fbNo = formula.getFubenNo(self.spaceNo)
        if not FD.data.get(fbNo, {}):
            self.removeBuffIconByClient(teamGuideTeacherBuff)
            return
        guideState, mode, memberList = self.fbGuideModeLoginInfo(fbNo)
        isNeedBuff = False
        if guideState == gametypes.FB_GUIDE_SUC:
            for member in memberList:
                if self.isApprentice(member['id']):
                    isNeedBuff = True

        if isNeedBuff:
            self.addBuffIconByClient(teamGuideTeacherBuff)
        else:
            self.removeBuffIconByClient(teamGuideTeacherBuff)
        self.refreshTeamGuideBuff()

    def addRebalancePushMsg(self, fbNo):
        isPushBalanceMode = MCD.data.get(fbNo, {}).get('isNotPushBalanceMode', 0)
        if isPushBalanceMode:
            return
        rebalanceMode = MCD.data.get(fbNo, {}).get('rebalanceMode', 0)
        if rebalanceMode:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_REBALANCE_MODE)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_REBALANCE_MODE, {'click': self.onClickRebalanceIntroMsg})

    def removeRebalancePushMsg(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_REBALANCE_MODE)

    def onClickRebalanceIntroMsg(self):
        fbNo = formula.getFubenNo(self.spaceNo)
        gameglobal.rds.ui.fengyinShow.show(fbNo)
        self.removeRebalancePushMsg()

    def confirmEnterRandomFuben(self, fbNo):
        msg = gameglobal.rds.ui.arena.genConfirmDesc(gameStrings.TEXT_IMPFUBEN_1331)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._doConfirmEnterRandomFuben, fbNo), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def _doConfirmEnterRandomFuben(self, fbNo):
        self.cell.onConfirmEnterRandomFuben(fbNo)

    def onGetSkyWingScore(self, score, rank, passTime, lastChallengeCD, lastRobCD):
        """
        \xe7\xa7\xaf\xe5\x88\x86\xe5\x8f\x98\xe5\x8a\xa8\xe6\x97\xb6\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x8c\xe5\x9c\xa8\xe4\xb8\x8a\xe7\xba\xbf\xe6\x97\xb6/\xe6\xb4\xbb\xe5\x8a\xa8\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6/\xe6\x8c\x91\xe6\x88\x98\xe5\xae\x8c\xe6\x88\x90\xe6\x97\xb6/\xe6\x8a\xa2\xe5\xa4\xba\xe7\xa7\xaf\xe5\x88\x86/\xe8\xa2\xab\xe6\x8a\xa2\xe5\xa4\xba\xe7\xa7\xaf\xe5\x88\x86\xe6\x97\xb6 \xe8\xa2\xab\xe8\xb0\x83\xe7\x94\xa8
        :param score: \xe5\xa4\xa9\xe7\xbe\xbd\xe6\xbc\x94\xe6\xad\xa6\xe7\xa7\xaf\xe5\x88\x86
        :param rank: \xe5\xa4\xa9\xe7\xbe\xbd\xe6\xbc\x94\xe6\xad\xa6\xe6\x8e\x92\xe5\x90\x8d\xef\xbc\x88\xe6\x8e\x92\xe8\xa1\x8c\xe6\xa6\x9c\xe8\xa7\x84\xe6\xa8\xa11050\xef\xbc\x8c\xe6\x9c\xaa\xe4\xb8\x8a\xe6\xa6\x9c\xe4\xb8\xba0\xef\xbc\x89
        :param passTime: \xe9\xa1\xba\xe4\xbe\xbf\xe5\x8f\x91\xe9\x80\x81\xe7\x9a\x84\xe5\xa4\xa9\xe7\xbe\xbd\xe6\xbc\x94\xe6\xad\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe8\xbf\x87\xe5\x8e\xbb\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88\xe7\x94\xa8\xe4\xba\x8e\xe4\xbf\xae\xe6\xad\xa3\xe4\xb8\x80\xe4\xb8\x8b\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe5\x80\x92\xe8\xae\xa1\xe6\x97\xb6\xef\xbc\x89
        :param lastChallengeCD: \xe5\x89\xa9\xe4\xbd\x99\xe8\xb0\x83\xe6\x95\xb4cd\xe6\x97\xb6\xe9\x97\xb4
        :param lastRobCD: \xe5\x89\xa9\xe4\xbd\x99\xe6\x8a\xa2\xe5\xa4\xbacd\xe6\x97\xb6\xe9\x97\xb4
        """
        gamelog.info('jbx:onGetSkyWingScore', score, rank, passTime, lastChallengeCD, lastRobCD)
        gameglobal.rds.ui.baiDiShiLian.selfScore = score
        gameglobal.rds.ui.baiDiShiLian.skyWingPassTime = passTime
        gameglobal.rds.ui.baiDiShiLian.setFuBenCD(lastChallengeCD, lastRobCD)
        gameglobal.rds.ui.baiDiShiLian.getTime()

    def onSkyWingStart(self):
        gamelog.info('jbx:onSkyWingStart')
        gameglobal.rds.ui.baiDiShiLian.onSkyWingStart()

    def onGetSkyWingPassTime(self, passTime):
        """
        \xe6\xb4\xbb\xe5\x8a\xa8\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6/\xe8\xbf\x9b\xe5\x85\xa5\xe5\x89\xaf\xe6\x9c\xac\xe6\x97\xb6 \xe8\xa2\xab\xe8\xb0\x83\xe7\x94\xa8
        :param passTime:passTime\xe6\x98\xaf\xe5\xb7\xb2\xe7\xbb\x8f\xe8\xbf\x87\xe5\x8e\xbb\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x8c\xe7\x94\xa8\xe4\xba\x8e\xe5\x80\x92\xe8\xae\xa1\xe6\x97\xb6\xe4\xbf\xae\xe6\xad\xa3 
        """
        gameglobal.rds.ui.baiDiShiLian.skyWingPassTime = passTime
        gameglobal.rds.ui.baiDiShiLian.getTime()
        gamelog.info('jbx:getTime', gameglobal.rds.ui.baiDiShiLian.getTime())

    def onSkyWingGuildMemberChallengeNotify(self, memberGbId, memberName, guildNuid, score):
        """
        \xe5\x85\xac\xe4\xbc\x9a\xe6\x88\x90\xe5\x91\x98\xe6\x8c\x91\xe6\x88\x98\xe8\x8e\xb7\xe5\xbe\x97\xe7\xa7\xaf\xe5\x88\x86\xe7\x9a\x84\xe9\x80\x9a\xe7\x9f\xa5\xef\xbc\x88\xe5\x8c\x85\xe5\x90\xab\xe8\x87\xaa\xe5\xb7\xb1\xef\xbc\x89
        :param memberGbId: \xe6\x88\x90\xe5\x91\x98gbId
        :param memberName: \xe6\x88\x90\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97
        :param guildNuid: \xe5\x85\xac\xe4\xbc\x9aNuid
        :param score: \xe6\x8c\x91\xe6\x88\x98\xe8\x8e\xb7\xe5\xbe\x97\xe7\xa7\xaf\xe5\x88\x86
        """
        gameglobal.rds.ui.baiDiShiLian.addLogList(uiConst.LOG_TYPE_CHALLENGE, memberGbId, memberName, score)

    def onSkyWingGuildMemberRobNotify(self, memberGbId, memberName, guildNuid, tGbId, tName, tGuildNuid, tGuildName, robscore):
        """
        \xe5\x85\xac\xe4\xbc\x9a\xe6\x88\x90\xe5\x91\x98\xe6\x8a\xa2\xe5\xa4\xba\xe8\x8e\xb7\xe5\xbe\x97\xe7\xa7\xaf\xe5\x88\x86\xe7\x9a\x84\xe9\x80\x9a\xe7\x9f\xa5\xef\xbc\x88\xe5\x8c\x85\xe5\x90\xab\xe8\x87\xaa\xe5\xb7\xb1\xef\xbc\x89
        :param memberGbId: \xe6\x88\x90\xe5\x91\x98gbId
        :param memberName: \xe6\x88\x90\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97
        :param guildNuid: \xe5\x85\xac\xe4\xbc\x9aNuid
        :param tGbId: \xe5\xaf\xb9\xe6\x96\xb9gbId
        :param tName: \xe5\xaf\xb9\xe6\x96\xb9\xe5\x90\x8d\xe5\xad\x97
        :param tGuildNuid: \xe5\xaf\xb9\xe6\x96\xb9\xe5\x85\xac\xe4\xbc\x9aNuid
        :param tGuildName: \xe5\xaf\xb9\xe6\x96\xb9\xe5\x85\xac\xe4\xbc\x9a\xe5\x90\x8d\xe5\xad\x97
        :param robscore: \xe6\x8a\xa2\xe5\xa4\xba\xe7\xa7\xaf\xe5\x88\x86
        """
        gameglobal.rds.ui.baiDiShiLian.addLogList(uiConst.LOG_TYPE_RANSACK, memberGbId, memberName, guildNuid, tGbId, tName, tGuildNuid, tGuildName, robscore)

    def onSkyWingGuildMemberBeRobNotify(self, memberGbId, memberName, guildNuid, sGbId, sName, sGuildNuid, sGuildName, robscore):
        """
        \xe5\x85\xac\xe4\xbc\x9a\xe6\x88\x90\xe5\x91\x98\xe8\xa2\xab\xe6\x8a\xa2\xe5\xa4\xba\xe7\xa7\xaf\xe5\x88\x86\xe7\x9a\x84\xe9\x80\x9a\xe7\x9f\xa5\xef\xbc\x88\xe5\x8c\x85\xe5\x90\xab\xe8\x87\xaa\xe5\xb7\xb1\xef\xbc\x89
        :param memberGbId: \xe6\x88\x90\xe5\x91\x98gbId
        :param memberName: \xe6\x88\x90\xe5\x91\x98\xe5\x90\x8d\xe5\xad\x97
        :param guildNuid: \xe5\x85\xac\xe4\xbc\x9aNuid
        :param sGbId: \xe5\xaf\xb9\xe6\x96\xb9gbId
        :param sName: \xe5\xaf\xb9\xe6\x96\xb9\xe5\x90\x8d\xe5\xad\x97
        :param sGuildNuid: \xe5\xaf\xb9\xe6\x96\xb9\xe5\x85\xac\xe4\xbc\x9aNuid
        :param sGuildName: \xe5\xaf\xb9\xe6\x96\xb9\xe5\x85\xac\xe4\xbc\x9a\xe5\x90\x8d\xe5\xad\x97
        :param robscore: \xe6\x8a\xa2\xe5\xa4\xba\xe7\xa7\xaf\xe5\x88\x86
        """
        gameglobal.rds.ui.baiDiShiLian.addLogList(uiConst.LOG_TYPE_BERANSACK, memberGbId, memberName, guildNuid, sGbId, sName, sGuildNuid, sGuildName, robscore)

    def onFbPlayerDoubleCheck(self, fbNo, checkType, reasonSet):
        """
        \xe5\x89\xaf\xe6\x9c\xac\xe4\xba\x8c\xe6\xac\xa1\xe7\xa1\xae\xe8\xae\xa4
        \xe4\xb8\x80\xe4\xb8\xaacheck\xe7\xb1\xbb\xe5\x9e\x8b\xe5\xaf\xb9\xe5\xba\x94\xe4\xb8\x80\xe4\xb8\xaa\xe4\xba\x8c\xe6\xac\xa1\xe7\xa1\xae\xe8\xae\xa4\xe6\xa1\x86\xef\xbc\x8c\xe4\xb8\x80\xe4\xb8\xaacheck\xe7\xb1\xbb\xe5\x9e\x8b\xe5\x8f\xaf\xe5\x8c\x85\xe5\x90\xab\xe5\xa4\x9a\xe7\xa7\x8dcheck\xe5\x8e\x9f\xe5\x9b\xa0\xef\xbc\x8c\xe5\xa4\x9a\xe4\xb8\xaa\xe5\x8e\x9f\xe5\x9b\xa0\xe6\x98\xbe\xe7\xa4\xba\xe5\x9c\xa8\xe5\x90\x8c\xe4\xb8\x80\xe4\xb8\xaa\xe4\xba\x8c\xe6\xac\xa1\xe7\xa1\xae\xe8\xae\xa4\xe6\xa1\x86\xe5\x86\x85\xef\xbc\x88\xe5\x8d\xb3\xe4\xb8\x80\xe6\xac\xa1\xe6\x80\xa7\xe5\xaf\xb91-N\xe4\xb8\xaa\xe6\x83\x85\xe5\x86\xb5\xe7\xa1\xae\xe8\xae\xa4\xef\xbc\x89
        :param fbNo: 
        :param checkType:check\xe7\xb1\xbb\xe5\x9e\x8b\xef\xbc\x8c\xe8\xa7\x81 const.FB_PLAYER_DOUBLE_CHECK_TYPE_TEAM_PEOPLE \xe7\xad\x89
        :param reasonSet: check\xe5\x8e\x9f\xe5\x9b\xa0\xef\xbc\x8c\xe8\xa7\x81 const.FB_PLAYER_DOUBLE_CHECK_REASON_TEAM_NUM_LOWER_FB_MAX_NUM \xe7\xad\x89
        
        # \xe7\x8e\xa9\xe5\xae\xb6\xe4\xba\x8c\xe6\xac\xa1\xe7\xa1\xae\xe8\xae\xa4\xe5\x90\x8e\xef\xbc\x8c\xe8\xb0\x83\xe7\x94\xa8cell.fbPlayerDoubleCheckDone\xef\xbc\x8c\xe5\xb0\x86fbNo\xe5\x92\x8ccheckType\xe4\xbc\xa0\xe5\x9b\x9e
        """
        if checkType == const.FB_PLAYER_DOUBLE_CHECK_TYPE_TEAM_PEOPLE:
            msg = ''
            if const.FB_PLAYER_DOUBLE_CHECK_REASON_TEAM_NUM_LOWER_FB_MAX_NUM in reasonSet:
                msg += gameStrings.FUBEN_CHECK_MEMBER_TXT1
            if const.FB_PLAYER_DOUBLE_CHECK_REASON_TEAM_SCHOOL_N in reasonSet:
                msg += gameStrings.FUBEN_CHECK_MEMBER_TXT2
            if const.FB_PLAYER_DOUBLE_CHECK_REASON_TEAM_SCHOOL_T in reasonSet:
                msg += gameStrings.FUBEN_CHECK_MEMBER_TXT3
            if msg != '':
                msg += gameStrings.FUBEN_CHECK_MEMBER_TXT4
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton(gameStrings.FUBEN_CHECK_MEMBER_TXT5, Functor(self.cell.fbPlayerDoubleCheckDone, fbNo, checkType)), MBButton(gameStrings.FUBEN_CHECK_MEMBER_TXT6, Functor(self.sendToTeamAndGuildChannel, fbNo))]
                gameglobal.rds.ui.messageBox.show(False, gameStrings.FUBEN_CHECK_MEMBER_TXT7, msg, buttons)

    def sendToTeamAndGuildChannel(self, fbNo):
        groupDetailIns = groupDetailFactory.getInstance()
        dropDownMenuInfo = groupDetailIns.getDropDownMenuInfoV2(uiConst.MENU_GOAL_TYPE_LIST[GOAL_TYPE_FUBEN])
        fubenData = FD.data.get(fbNo)
        realFubenId = fubenData.get('realFubenId', None)
        if realFubenId:
            fubenData = FD.data.get(realFubenId)
        goal1Name = fubenData.get('name', '')
        goal2Name = fubenData.get('primaryLevelName', '')
        goal1MenuData = self.genGoal1MenuData(dropDownMenuInfo)
        index = 0
        for data in goal1MenuData:
            if data['label'] == goal1Name:
                break
            index = index + 1

        goal1Idx = index
        if goal1Idx == len(goal1MenuData):
            p = BigWorld.player()
            msg = gameglobal.rds.ui.team.getShareTeamInfoMsg()
            p.cell.chatToGroupInfo(msg)
            p.cell.chatToGuild(msg, True)
            return
        else:
            goal2MenuData = self.genGoal2MenuDataByGoal1(dropDownMenuInfo, goal1Idx)
            index = 0
            for data in goal2MenuData:
                if data['label'] == goal2Name:
                    break
                index = index + 1

            goal2Idx = index
            if goal2Idx == len(goal2MenuData):
                p = BigWorld.player()
                msg = gameglobal.rds.ui.team.getShareTeamInfoMsg()
                p.cell.chatToGroupInfo(msg)
                p.cell.chatToGuild(msg, True)
                return
            info = self.getTeamGoalInfo(goal1Idx, goal2Idx)
            BigWorld.player().setGroupDetails(info, ANOTHER_CALLBACK)
            return

    def genGoal1MenuData(self, dropDownMenuInfo):
        return [ {'label': goal.get('keyName')} for goal in dropDownMenuInfo ]

    def genGoal2MenuDataByGoal1(self, dropDownMenuInfo, goal1):
        goal2DetailsData = dropDownMenuInfo[goal1]['data']
        goal2MenuData = [ {'label': goal.get('keyName')} for goal in goal2DetailsData ]
        return goal2MenuData

    def getTeamGoalInfo(self, goal1Idx, goal2Idx):
        p = BigWorld.player()
        lvMinDefault, lvMaxDefault = self.getGoalLvLimit(goal1Idx, goal2Idx)
        extraInfo = {}
        if not extraInfo and hasattr(p, 'detailInfo'):
            extraInfo = p.detailInfo
            extraInfo['lvMin'] = lvMinDefault
            extraInfo['lvMax'] = lvMaxDefault
        teamName = extraInfo.get('teamName', utils.getTeamName())
        lvMin = extraInfo.get('lvMin', lvMinDefault)
        lvMax = extraInfo.get('lvMax', lvMaxDefault)
        schoolReqs = extraInfo.get('schoolReq', const.SCHOOL_DICT.keys())
        isPublic = True
        goalType = uiConst.MENU_GOAL_TYPE_LIST[GOAL_TYPE_FUBEN]
        self.updateCurrentTeamGoalMenuIdx(goal1Idx, goal2Idx)
        fKey, sKey, tKey = self.getCurrentTeamGoalKey(goal1Idx, goal2Idx)
        return (teamName,
         goalType,
         lvMin,
         lvMax,
         schoolReqs,
         isPublic,
         fKey,
         sKey,
         tKey)

    def getGoalLvLimit(self, goal1Idx, goal2Idx):
        goalType = uiConst.MENU_GOAL_TYPE_LIST[GOAL_TYPE_FUBEN]
        lvMin = const.MIN_CURRENT_LEVEL
        lvMax = const.MAX_CURRENT_LEVEL
        actAvlData = groupDetailFactory.getActAvlData()
        if goalType == const.GROUP_GOAL_RELAXATION:
            if goal1Idx != 0 and goal2Idx != 0:
                key = actAvlData.get(goal1Idx)[goal2Idx - 1]
                item = GLD.data.get(key, {})
                if item.get('recommendLv'):
                    lvMin, lvMax = item['recommendLv']
                elif item.get('lv'):
                    lvMin, lvMax = item['lv']
        elif goalType == const.GROUP_GOAL_FB:
            lvMin, lvMax = self.getMenuFbLvLimit(goal1Idx, goal2Idx)
        return (lvMin, lvMax)

    def updateCurrentTeamGoalMenuIdx(self, fIndex, sIndex):
        groupDetailIns = groupDetailFactory.getInstance()
        goalType = uiConst.MENU_GOAL_TYPE_LIST[GOAL_TYPE_FUBEN]
        tIndex = const.GROUP_GOAL_DEFAULT
        groupDetailIns.goalIns[goalType].setDropDownMenuIndex(fIndex, sIndex, tIndex)

    def getCurrentTeamGoalKey(self, fIndex, sIndex):
        groupDetailIns = groupDetailFactory.getInstance()
        goalType = uiConst.MENU_GOAL_TYPE_LIST[GOAL_TYPE_FUBEN]
        tIndex = const.GROUP_GOAL_DEFAULT
        return groupDetailIns.goalIns[goalType].getCreateTeamKeys(fIndex, sIndex, tIndex)

    def getMenuFbLvLimit(self, fIndex, sIndex, tIndex = const.GROUP_GOAL_DEFAULT):
        if fIndex == 0 or sIndex == 0:
            return (const.MIN_CURRENT_LEVEL, const.MAX_CURRENT_LEVEL)
        groupDetailIns = groupDetailFactory.getInstance()
        dropDownMenuInfo = groupDetailIns.getDropDownMenuInfoV2(const.GROUP_GOAL_FB)
        fData = dropDownMenuInfo[fIndex]
        fKey = fData['key']
        sData = fData['data'][sIndex]
        sKey = sData['key']
        tData = sData['data'][tIndex]
        tKey = tData['key']
        fbNo = GFMD.data.get(fKey, {}).get(sKey, {}).get(tKey, {}).get('fbNo', 0)
        if fbNo:
            lvMin = FD.data.get(fbNo, {}).get('lvMin', 1)
            lvMax = FD.data.get(fbNo, {}).get('lvMax', const.MAX_CURRENT_LEVEL)
        else:
            lvMin = const.MIN_CURRENT_LEVEL
            lvMax = const.MAX_CURRENT_LEVEL
        return (lvMin, lvMax)

    def _getZMJData(self, dataType, default = None):
        return self.zmjData.get(dataType, default)

    def onGetZMJData(self, data):
        gamelog.debug('@zq onGetZMJData', data)
        oldCnt = self.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_ENTER_CNT, 0)
        oldFbNo = self.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_NO, 0)
        oldAwardStars = set(self.zmjData.get(const.ZMJ_FB_INFO_TOOK_AWARD_STAR_IDS, ()))
        oldAssitApplyNum = self.zmjData.get(const.ZMJ_FB_INFO_ASSIST_DAY_CNT, 0)
        self.zmjData = data
        newCnt = self.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_ENTER_CNT, 0)
        newFbNo = self.zmjData.get(const.ZMJ_FB_INFO_CUR_FB_NO, 0)
        newAwardStars = set(self.zmjData.get(const.ZMJ_FB_INFO_TOOK_AWARD_STAR_IDS, ()))
        newAssitApplyNum = self.zmjData.get(const.ZMJ_FB_INFO_ASSIST_DAY_CNT, 0)
        if newFbNo == oldFbNo and newCnt == oldCnt + 1:
            gameglobal.rds.ui.zmjActivityBg.hide()
        else:
            gameglobal.rds.ui.zmjActivityBg.refreshInfo()
        if oldAwardStars != newAwardStars:
            gameglobal.rds.ui.zmjLittleBossPanel.refreshInfoStarList()
        if oldAssitApplyNum != newAssitApplyNum:
            gameglobal.rds.ui.zmjSpriteInvite.refreshLeftCount()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def bFirstZmj(self):
        if gameglobal.rds.configData.get('enableZMJFuben', False) and not self.zmjData:
            return True
        return False

    def onGetZmjRank(self, inTop, idx):
        """
        \xe8\x8e\xb7\xe5\xbe\x97\xe6\x8e\x92\xe5\x90\x8d\xe6\x95\xb0\xe6\x8d\xae
        :param inTop:\xe6\x98\xaf\xe5\x90\xa6\xe5\x9c\xa8\xe6\x8e\x92\xe8\xa1\x8c\xe6\xa6\x9c\xe4\xb8\xad\xef\xbc\x88\xe5\x89\x8d6\xe5\x90\x8d\xef\xbc\x89
        :param idx: \xe5\xa6\x82\xe6\x9e\x9cinTop=True,\xe5\x88\x99idx\xe4\xb8\xba\xe6\x8e\x92\xe5\x90\x8d\xef\xbc\x9b\xe5\xa6\x82\xe6\x9e\x9cinTop=False\xef\xbc\x8c\xe5\x88\x99idx\xe6\x98\xafhighFbTotalMaxDmgRewardsNotInTop\xe7\x9a\x84\xe4\xb8\x8b\xe6\xa0\x87
        """
        gameglobal.rds.ui.zmjBigBossPanel.onGetZmjRank(inTop, idx)

    def onGetZMJPhotoData(self, photoData):
        """
        \xe6\x96\xa9\xe9\xad\x94\xe6\x9e\x81\xe9\x9d\xa2\xe6\x9d\xbf\xe5\x90\x84\xe6\x98\x9f\xe7\xba\xa7\xe7\x9a\x84\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xa4\xb4\xe5\x83\x8f\xe6\x95\xb0\xe6\x8d\xae
        :param photoData: = {star: (gbId, name, customPhoto)}
        """
        gamelog.debug('@zq onGetZMJPhotoData', photoData)
        self.zmjPhotoData = photoData
        gameglobal.rds.ui.zmjActivityBg.refreshInfo()

    def onGetZMJAssistInfo(self, qType, data):
        """
        \xe8\x8e\xb7\xe5\xbe\x97\xe5\x8d\x8f\xe6\x88\x98\xe9\x9d\xa2\xe6\x9d\xbf\xe6\x95\xb0\xe6\x8d\xae\xef\xbc\x8c\xe5\xa5\xbd\xe5\x8f\x8b\xe4\xbf\xa1\xe6\x81\xaf\xe8\xaf\xb7\xe6\xa0\xb9\xe6\x8d\xaegbId\xe5\x88\xb0friend\xe4\xbb\x8e\xe8\x8e\xb7\xe5\xbe\x97
        \xe9\x85\x8d\xe8\xa1\xa8beApplyAssistDayLimit - \xe6\xad\xa4\xe4\xba\xba\xe4\xbb\x8a\xe6\x97\xa5\xe5\xb7\xb2\xe5\x8d\x8f\xe6\x88\x98\xe6\xac\xa1\xe6\x95\xb0 = \xe6\xad\xa4\xe4\xba\xba\xe8\xbf\x98\xe8\x83\xbd\xe5\x8d\x8f\xe6\x88\x98\xe5\x87\xa0\xe6\xac\xa1
        :param qType: \xe8\xa7\x81const.ZMJ_ASSIST_TYPE_FRIEND\xe7\xad\x89
        :param data: [(gbId, \xe5\xb1\x82\xe6\x95\xb0, \xe6\xad\xa4\xe4\xba\xba\xe4\xbb\x8a\xe6\x97\xa5\xe5\xb7\xb2\xe5\x8d\x8f\xe6\x88\x98\xe6\xac\xa1\xe6\x95\xb0)]
        """
        gamelog.debug('@xzh onGetZMJAssistInfo', qType, data)
        gameglobal.rds.ui.zmjSpriteInvite.setAssitInfo(qType, data)

    def notifyBeApplyZMJAssist(self, qType, todayAssistNum, gbId, name, fbNo, nuid, star, awardFame):
        """
        \xe6\x94\xb6\xe5\x88\xb0\xe9\x82\x80\xe8\xaf\xb7\xe5\x8d\x8f\xe6\x88\x98\xe6\xb6\x88\xe6\x81\xaf
        \xe5\xa6\x82\xe6\x9e\x9c\xe5\x90\x8cgbId\xe5\x8f\x91\xe6\x9d\xa5\xe6\x96\xb0\xe7\x9a\x84\xe9\x82\x80\xe8\xaf\xb7\xef\xbc\x8c\xe5\xba\x94\xe8\xaf\xa5\xe5\xb0\x86\xe6\x9d\xa5\xe8\x87\xaa\xe8\xaf\xa5gbId\xe7\x9a\x84\xe6\x97\xa7\xe9\x82\x80\xe8\xaf\xb7\xe5\x88\xa0\xe9\x99\xa4
        :param qType: \xe8\xa7\x81const.ZMJ_ASSIST_TYPE_FRIEND\xe7\xad\x89
        :param todayAssistNum: \xe4\xbb\x8a\xe6\x97\xa5\xe5\xb7\xb2\xe5\x8d\x8f\xe6\x88\x98\xe6\xac\xa1\xe6\x95\xb0
        :param gbId:
        :param name:
        :param fbNo:
        :param nuid: \xe7\x94\xa8\xe4\xba\x8e\xe6\xa0\x87\xe8\xaf\x86\xe5\xbd\x93\xe5\x89\x8d\xe5\x89\xaf\xe6\x9c\xac
        :param star: \xe5\xaf\xb9\xe6\x96\xb9\xe7\x8e\xa9\xe5\xae\xb6\xe5\xbd\x93\xe5\x89\x8d\xe5\x89\xaf\xe6\x9c\xac\xe6\x98\x9f\xe7\xba\xa7
        :param awardFame: \xe6\x94\xb6\xe7\x9b\x8a
        """
        gamelog.debug('@xzh notifyBeApplyZMJAssist', qType, todayAssistNum, gbId, name, fbNo, nuid, star, awardFame)
        gameglobal.rds.ui.zmjSpriteBeInvited.addAssistApply(qType, todayAssistNum, gbId, name, fbNo, nuid, star, awardFame)

    def onApplyZMJAssistFail(self, reason, gbId):
        """
        :param reason: \xe5\xa4\xb1\xe8\xb4\xa5\xe5\x8e\x9f\xe5\x9b\xa0\xef\xbc\x8c\xe7\x94\xa8\xe4\xba\x8e\xe7\xa8\x8b\xe5\xba\x8f\xe5\x86\x85\xe9\x83\xa8\xe5\x8c\xba\xe5\x88\x86
        :param gbId: \xe8\xa2\xab\xe9\x82\x80\xe8\xaf\xb7\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6
        """
        if reason == const.ZMJ_APPLY_ASSIST_FAIL_OFFLINE:
            self.showGameMsg(GMDD.data.ZMJ_APPLY_ASSIST_FAIL_NOT_ONLINE, ())
        elif reason == const.ZMJ_APPLY_ASSIST_FAIL_NOT_FRIEND:
            self.showGameMsg(GMDD.data.ZMJ_APPLY_ASSIST_FAIL_NOT_FRIEND, ())
        elif reason == const.ZMJ_APPLY_ASSIST_FAIL_NOT_SAME_GUILD:
            self.showGameMsg(GMDD.data.ZMJ_APPLY_ASSIST_FAIL_NOT_SAME_GUILD, ())
        elif reason == const.ZMJ_APPLY_ASSIST_FAIL_ASSITER_NUM_LIMIT:
            self.showGameMsg(GMDD.data.ZMJ_APPLY_ASSIST_FAIL_NOT_HAS_NUM, ())
        elif reason == const.ZMJ_APPLY_ASSIST_FAIL_ONCE_LIMIT:
            self.showGameMsg(GMDD.data.ZMJ_APPLY_ASSIST_FAIL_ONCE_LIMIT, ())

    def onAgreeZMJAssistFail(self, reason, gbId):
        """
        
        :param reason: \xe5\xa4\xb1\xe8\xb4\xa5\xe5\x8e\x9f\xe5\x9b\xa0\xef\xbc\x8c\xe7\x94\xa8\xe4\xba\x8e\xe7\xa8\x8b\xe5\xba\x8f\xe5\x86\x85\xe9\x83\xa8\xe5\x8c\xba\xe5\x88\x86
        :param gbId: \xe8\xa2\xab\xe5\x8d\x8f\xe6\x88\x98\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6
        """
        if reason == const.ZMJ_AGREE_ASSIST_FAIL_OFFLINE:
            self.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_NOT_ONLINE, ())
        elif reason == const.ZMJ_AGREE_ASSIST_FAIL_NOT_FRIEND:
            self.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_NOT_FRIEND, ())
        elif reason == const.ZMJ_AGREE_ASSIST_FAIL_NOT_THAT_FUBEN:
            self.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_NOT_THAT_FUBEN, ())
        elif reason == const.ZMJ_AGREE_ASSIST_FAIL_OTHER_ASSIST:
            self.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_OTHER_ASSIST, ())
        elif reason == const.ZMJ_AGREE_ASSIST_FAIL_FUBEN_STUB:
            self.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_ENTER, ())
        elif reason == const.ZMJ_AGREE_ASSIST_FAIL_ALREADY_ASSIST:
            self.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_IN_ASSISTING, ())
        elif reason == const.ZMJ_AGREE_ASSIST_FAIL_NOT_SAME_GUILD:
            self.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_NOT_SAME_GUILD, ())
        elif reason == const.ZMJ_AGREE_ASSIST_FAIL_ASSITER_NUM_LIMIT:
            self.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_NOT_HAS_NUM, ())
        elif reason == const.ZMJ_AGREE_ASSIST_FAIL_OTHER_ASSIST_IN_PROCESS:
            self.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_OTHER_ASSIST_IN_PROCESS, ())
        elif reason == const.ZMJ_AGREE_ASSIST_FAIL_ASSIST_IN_PROCESS:
            self.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_ASSISTING_IN_PROCESS, ())
        gameglobal.rds.ui.zmjSpriteBeInvited.removeAssistApply(gbId)

    def notifyZMJAssistEnter(self, gbId):
        """
        \xe4\xbd\x9c\xe4\xb8\xba\xe5\x8d\x8f\xe6\x88\x98\xe8\x80\x85\xef\xbc\x8c\xe8\xbf\x9b\xe5\x85\xa5\xe4\xba\x86\xe6\x96\xa9\xe9\xad\x94\xe6\x9e\x81\xe5\x89\xaf\xe6\x9c\xac
        :param gbId: \xe8\xa2\xab\xe5\x8d\x8f\xe5\x8a\xa9\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6
        """
        gameglobal.rds.ui.zmjSpriteBeInvited.removeAssistApply(gbId)

    def notifyZMJAssistResult(self, succ, gbId, name, school, fameVal):
        """
        \xe9\x80\x9a\xe7\x9f\xa5\xe5\x8d\x8f\xe6\x88\x98\xe7\xbb\x93\xe6\x9e\x9c
        :param succ:\xe6\x98\xaf\xe5\x90\xa6\xe6\x88\x90\xe5\x8a\x9f
        :param gbId:
        :param name:
        :param school:
        :param fameVal:\xe5\xa6\x82\xe6\x9e\x9c\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe8\x8e\xb7\xe5\xbe\x97\xe5\xa4\x9a\xe5\xb0\x91\xe5\xa3\xb0\xe6\x9c\x9b
        """
        gamelog.debug('@xzh notifyZMJAssistResult', succ, gbId, name, school, fameVal)
        if succ:
            self.showGameMsg(GMDD.data.ZMJ_ASSIST_CLAIM_REWARD_TXT, (name, fameVal, fameVal))
            gameglobal.rds.ui.zmjSpriteReward.queryInfo()

    def onGetZMJAssistAwardInfo(self, dataNotTake, dataTook):
        """
        \xe4\xb8\xa4\xe4\xb8\xaa\xe9\x83\xbd\xe6\x98\xaflist\xef\xbc\x8c\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba list = [(gbId,name,school,fame,timeStamp),]
        :param dataTook: \xe5\xb7\xb2\xe9\xa2\x86\xe5\x8f\x96\xe7\x9a\x84
        :param dataNotTake: \xe6\x9c\xaa\xe9\xa2\x86\xe5\x8f\x96\xe7\x9a\x84
        :return:
        """
        gamelog.debug('@xzh onGetZMJAssistAwardInfo', dataNotTake, dataTook)
        gameglobal.rds.ui.zmjSpriteReward.setAwardInfo(dataNotTake, dataTook)

    def onGetFriendZMJRecord(self):
        gameglobal.rds.ui.zmjPublishBoss.refreshInfo()

    def onGetGuildZMJRecord(self, guildNUID, record):
        pass

    def onAddZMJStarBoss(self, nuid, mVal):
        self.zmjStarBoss[nuid] = mVal
        gameglobal.rds.ui.zmjActivityBossPanel.refreshBossList()
        gameglobal.rds.ui.zmjActivityBossPanel.refreshPushMsg()

    def onRemoveZMJStarBoss(self, nuid):
        self.zmjStarBoss.pop(nuid, None)
        gameglobal.rds.ui.zmjActivityBossPanel.refreshBossList()
        gameglobal.rds.ui.zmjActivityBossPanel.refreshPushMsg()

    def onUpdateZMJStarBossProps(self, nuid, props):
        mVal = self.zmjStarBoss.get(nuid)
        if not mVal:
            return
        for attrName, attrVal in props.iteritems():
            if not hasattr(mVal, attrName):
                continue
            setattr(mVal, attrName, attrVal)

        gameglobal.rds.ui.zmjActivityBossPanel.refreshBossList()

    def onAddZMJStarBossCandidate(self, nuid, gbId):
        mVal = self.zmjStarBoss.get(nuid)
        if not mVal:
            return
        if gbId in mVal.candidates:
            return
        mVal.candidates.append(gbId)
        gameglobal.rds.ui.zmjPublishBoss.refreshInfo()

    def onOpenOptionalBonus(self, opNUID, optionId):
        gamelog.debug('@yj onOpenOptionalBonus', opNUID, optionId)
        gameglobal.rds.ui.optionalRewardBox.show(opNUID, optionId)

    def onGenOptionalBonusItem(self, item):
        gamelog.debug('@yj onGenOptionalBonusItem', item)
        gameglobal.rds.ui.optionalRewardBox.getedOptionalRewards(item)

    def syncMonsterFbEntityNo(self, mId, mEntityNo):
        if mId and mEntityNo:
            ent = BigWorld.entity(mId)
            if ent:
                ent.fbEntityNo = mEntityNo

    def onShowBossRandomUI(self):
        gameglobal.rds.ui.flyUpFubenBoss.show()
