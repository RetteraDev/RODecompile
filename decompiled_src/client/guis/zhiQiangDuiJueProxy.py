#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zhiQiangDuiJueProxy.o
import random
import BigWorld
import gameglobal
import uiConst
import events
import const
import utils
import gametypes
import commcalc
from uiProxy import UIProxy
from helpers import capturePhoto
from helpers import charRes
from helpers import tickManager
from helpers import cgPlayer
from callbackHelper import Functor
from guis import ui
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
from data import wing_world_config_data as WWCD
ICON_NAME_PRE = 'ZhiQiangDuiJue_unit4d_'
BOSS_IMG_CLS_NAME = 'ZhiQiangDuiJue_boss'
PLAYER_NUMBER_DUIJUE = 10
PLAYER_NUMBER_TEAM = 5
PLAYER_NUMBER_TIAOZHAN = 5
TYPE_ZHIQIANG = 0
TYPE_ZHIGAO = 1

class ZhiQiangDuiJueProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZhiQiangDuiJueProxy, self).__init__(uiAdapter)
        self.widget = None
        self.headGens = {}
        self.roundNo = 0
        self.matchNo = 0
        self.allowGroupNUIDs = ()
        self.arenaWinnerGroupNUID = 0
        self.uniqueCnt = 0
        self.arenaWinnerWaitEndTime = 0
        self.bossRefreshCount = 0
        self.cache = {}
        self.cgPlayer = None
        self.bossTickId = 0
        self.bossCache = {'version': 0}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_ZHIQIANG, self.hide)

    def reset(self):
        self.bossEndTime = 0
        self.pageType = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_ZHIQIANG:
            self.widget = widget
            gameglobal.rds.sound.playSound(gameglobal.SD_4)
            self.initUI()
            self.refreshInfo()

    def clearPlayerImg(self):
        if self.headGens:
            for key in self.headGens.iterkeys():
                if self.headGens[key]:
                    self.headGens[key].endCapture()

    def clearWidget(self):
        self.clearPlayerImg()
        self.widget = None
        if self.bossTickId:
            tickManager.stopTick(self.bossTickId)
            self.bossTickId = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_ZHIQIANG)
        gameglobal.rds.sound.playSound(gameglobal.SD_5)

    def show(self, pageType = 0, roundNo = 0, matchNo = 0):
        self.pageType = pageType
        self.roundNo = roundNo
        self.matchNo = matchNo
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_ZHIQIANG)
        elif self.pageType == TYPE_ZHIQIANG:
            self.refreshDuiJueInfo(roundNo, matchNo)
        else:
            self.refreshBossInfo()

    def initUI(self):
        if self.pageType == TYPE_ZHIQIANG:
            self.widget.gotoAndStop('wanjia')
            self.initPlayerImg()
            self.widget.mainMc.historyBtn.visible = True
            self.widget.mainMc.historyBtn.addEventListener(events.MOUSE_CLICK, self.onOpenHistory, False, 0, True)
            self.widget.mainMc.chooseStageBtn.addEventListener(events.MOUSE_CLICK, self.onOpenStageChoose, False, 0, True)
            self.widget.mainMc.enterWitnessBtn.addEventListener(events.BUTTON_CLICK, self.onEnterWitnessBtn, False, 0, True)
            self.refreshDuiJueInfo(self.roundNo, self.matchNo)
        else:
            self.bossRefreshCount = 0
            self.widget.gotoAndStop('Boss')
            self.initPlayerImg()
            if gameglobal.rds.ui.wingCombatPush.activityState == const.WING_WORLD_XINMO_STATE_UNIQUE_BOSS:
                self.bossEndTime = gameglobal.rds.ui.wingCombatPush.endTime
            if self.bossTickId:
                tickManager.stopTick(self.bossTickId)
            self.widget.mainMc.timeCount.visible = False
            self.bossTickId = tickManager.addTick(1, self.bossTimeFunc)
            self.refreshBossInfo()
            self.widget.mainMc.enterWitnessBtn.addEventListener(events.BUTTON_CLICK, self.onEnterBossWitnessBtn, False, 0, True)
            self.widget.mainMc.challengeBtn.addEventListener(events.BUTTON_CLICK, self.onChallengeBossBtn, False, 0, True)
        self.widget.defaultCloseBtn = self.widget.mainMc.closeBtn
        self.widget.mainMc.yuHuangBtn.addEventListener(events.BUTTON_CLICK, self.onYuHuangClick, False, 0, True)

    def onGetAllowsData(self, allowGroupNUIDs, arenaWinnerGroupNUID, cnt, arenaWinnerWaitEndTime):
        self.allowGroupNUIDs = allowGroupNUIDs
        self.arenaWinnerGroupNUID = arenaWinnerGroupNUID
        self.uniqueCnt = cnt
        self.arenaWinnerWaitEndTime = arenaWinnerWaitEndTime

    def bossTimeFunc(self):
        if self.pageType == TYPE_ZHIQIANG:
            return
        self.widget.mainMc.timeCount.visible = True
        leftTime = self.bossEndTime - utils.getNow()
        if leftTime < 0:
            leftTime = 0
        self.widget.mainMc.timeCount.text = self.formateTime(leftTime)
        if self.bossRefreshCount > 3:
            self.bossRefreshCount -= 3
            self.queryBossInfo()
        self.bossRefreshCount += 1

    def formateTime(self, time):
        minute = int(time / 60)
        sec = time - minute * 60
        return '%02d:%02d' % (minute, sec)

    def onYuHuangClick(self, *args):
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        p = BigWorld.player()
        p.cell.applyWingWorldXinMoArenaML()
        self.hide()

    def onOpenStageChoose(self, *args):
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        gameglobal.rds.ui.wingStageChoose.show()

    def onOpenHistory(self, *args):
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        gameglobal.rds.ui.combatHistory.show()

    def getheadGen(self, index):
        if self.headGens.has_key(index):
            self.headGens.get(index).initFlashMesh()
            return self.headGens.get(index)
        headGen = capturePhoto.CombatPhotoGen('gui/taskmask.tga', 320, ICON_NAME_PRE + str(index))
        headGen.initFlashMesh()
        self.headGens[index] = headGen
        return headGen

    def initPlayerImg(self):
        self.clearPlayerImg()
        if self.pageType == TYPE_ZHIGAO:
            for i in range(PLAYER_NUMBER_TIAOZHAN):
                self.setLoadingIcon(i, True)
                headGen = self.getheadGen(i + 5)
                headGen.startCaptureDummy()
                headGen.setModelFinishCallback(Functor(self.setLoadingIcon, i, False))

            self.setBossIcon()
        else:
            for i in range(PLAYER_NUMBER_DUIJUE):
                self.setLoadingIcon(i, True)
                headGen = self.getheadGen(i)
                headGen.startCaptureDummy()
                headGen.setModelFinishCallback(Functor(self.setLoadingIcon, i, False))

    def setBossIcon(self):
        bossImgPath = WWCD.data.get('xinmoBossMovie', '')
        if bossImgPath != '':
            self.widget.mainMc.boss.bossIcon.fitSize = True
            self.widget.mainMc.boss.bossIcon.loadImage(bossImgPath)

    def onGetBossServerData(self, data):
        self.bossCache = data
        if not self.widget:
            return
        elif self.pageType != TYPE_ZHIGAO:
            return
        else:
            self.resetAllInfo()
            groupNUID = data.get('groupNUID', 0)
            teamName = data.get('teamName', '')
            members = data.get('members', {})
            headerGbId = data.get('headerGbId', 0)
            self.widget.mainMc.teamName0.text = teamName
            if len(members) > 0:
                self.widget.mainMc.waitingMask0.visible = False
            else:
                self.widget.mainMc.waitingMask0.visible = True
            for index, memberGBId in enumerate(members):
                memberInfo = members.get(memberGBId, None)
                if memberInfo:
                    self.setPlayerInfo(index, memberInfo, headerGbId == memberGBId)
                    self.loadPlayerImg(index + 5, memberInfo)

            return

    def onBossFinished(self, isSucc):
        if not isSucc and self.pageType == TYPE_ZHIGAO:
            self.resetAllInfo()
            self.widget.mainMc.waitingMask0.visible = True
            self.bossCache = {}

    def onGetDuiJueServerData(self, data):
        roundNo = data.get('roundNo', 0)
        matchNo = data.get('matchNo', 0)
        key = '%d_%d' % (roundNo, matchNo)
        self.cache[key] = data
        if self.roundNo != roundNo or self.matchNo != matchNo:
            return
        elif not self.widget:
            return
        elif self.pageType != TYPE_ZHIQIANG:
            return
        else:
            self.resetAllInfo()
            teams = data.get('teams', {})
            players = data.get('players', {})
            for index, groupNUID in enumerate(teams):
                teamInfo = teams[groupNUID]
                teamName = teamInfo[0]
                memberGbIds = teamInfo[1]
                headerGbId = teamInfo[2]
                teamNameMc = getattr(self.widget.mainMc, 'teamName%d' % index, None)
                if teamNameMc:
                    teamNameMc.text = teamName
                memberIndex = 0 if index == 0 else PLAYER_NUMBER_TEAM
                for memberGBId in memberGbIds:
                    self.setPlayerInfo(memberIndex, players.get(memberGBId, None), headerGbId == memberGBId)
                    self.loadPlayerImg(memberIndex, players.get(memberGBId, None))
                    memberIndex += 1

            return

    def resetAllInfo(self):
        if not self.widget:
            return
        else:
            if self.pageType == TYPE_ZHIQIANG:
                self.widget.mainMc.teamName0.text = ''
                self.widget.mainMc.teamName1.text = ''
                for i in range(PLAYER_NUMBER_DUIJUE):
                    self.setPlayerInfo(i, None)
                    self.loadPlayerImg(i, None)

            else:
                self.widget.mainMc.teamName0.text = ''
                for i in range(PLAYER_NUMBER_TIAOZHAN):
                    self.setPlayerInfo(i, None)
                    self.loadPlayerImg(i, None)

            return

    def setPlayerInfo(self, index, playerData, isTeamLeader = False):
        itemMc = getattr(self.widget.mainMc, 'player%d' % index, None)
        if itemMc:
            if not playerData:
                itemMc.playerName.text = ''
                itemMc.playerSchool.visible = False
                itemMc.leaderIcon.visible = False
                itemMc.playerImg.visible = False
                self.setLoadingIcon(index, False)
            else:
                name = playerData[0]
                lv = playerData[1]
                physique = playerData[2]
                school = physique.school
                signal = playerData[5]
                self.setLoadingIcon(index, True)
                itemMc.playerSchool.visible = True
                itemMc.playerImg.visible = True
                itemMc.leaderIcon.visible = isTeamLeader
                itemMc.playerName.text = name
                itemMc.playerSchool.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school, 'yuxu'))

    def loadPlayerImg(self, index, playerData):
        if index not in self.headGens.keys():
            return
        headGen = self.headGens.get(index)
        if not playerData:
            pass
        else:
            physique = playerData[2]
            aspect = playerData[3]
            avatarConfig = playerData[4]
            signal = playerData[5]
            modelId = charRes.transBodyType(physique.sex, physique.bodyType)
            showFashion = commcalc.getSingleBit(signal, gametypes.SIGNAL_SHOW_FASHION)
            headGen.startCaptureRes(modelId, aspect, physique, avatarConfig, self.getAvatarPhotoAct(physique), showFashion)

    def setLoadingIcon(self, photoIndex, visible):
        loadingMc = getattr(self.widget.mainMc, 'loading%d' % photoIndex, None)
        if loadingMc:
            loadingMc.visible = visible

    def refreshInfo(self):
        if not self.widget:
            return

    def refreshBossInfo(self):
        if not self.widget:
            return
        self.resetAllInfo()
        p = BigWorld.player()
        version = self.bossCache.get('version', 0)
        if version:
            self.onGetBossServerData(self.bossCache)
        self.queryBossInfo()

    def queryBossInfo(self):
        p = BigWorld.player()
        version = self.bossCache.get('version', 0)
        p.base.queryWingWorldXinMoUniqueBoss(version)

    def refreshDuiJueInfo(self, roundNo, matchNo):
        if not self.widget:
            return
        self.resetAllInfo()
        self.roundNo = roundNo
        self.matchNo = matchNo
        self.widget.mainMc.round.text = gameStrings.WING_WORLD_ROUND_LABEL[self.roundNo]
        if not self.roundNo or not self.matchNo:
            self.widget.mainMc.waitingMask0.visible = True
            self.widget.mainMc.waitingMask1.visible = True
            return
        self.widget.mainMc.waitingMask0.visible = False
        self.widget.mainMc.waitingMask1.visible = False
        p = BigWorld.player()
        key = '%d_%d' % (self.roundNo, self.matchNo)
        matchInfo = self.cache.setdefault(key, {'version': 0})
        version = matchInfo.get('version', 0)
        if version:
            self.onGetDuiJueServerData(matchInfo)
        p.base.queryWingWorldXinMoRoundMatch(self.roundNo, self.matchNo, version)

    def showFromPushWidget(self):
        gameglobal.rds.ui.wingStageChoose.queryDataWithCallBack(self.onGetAvaliableList)
        self.onGetAvaliableList()

    def onEnterWitnessBtn(self, *args):
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        p = BigWorld.player()
        if self.roundNo and self.matchNo:
            p.base.queryWingWorldXinMoAnnal(self.roundNo, self.matchNo)
            self.hide()
        else:
            p.showGameMsg(GMDD.data.WING_WORLD_XINMO_NO_AVALIABLE_ARENA, ())

    @ui.callFilter(1, False)
    def onEnterBossWitnessBtn(self, *args):
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        p = BigWorld.player()
        p.base.queryWingWorldXinMoUniqueBossAnnal()
        self.hide()

    @ui.callFilter(1, False)
    def onChallengeBossBtn(self, *args):
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        p = BigWorld.player()
        if p.groupNUID not in self.allowGroupNUIDs:
            p.showGameMsg(GMDD.data.WING_WORLD_XINMO_UNIQUE_BOSS_APPLY_NOT_HAS_ALLOW, ())
            return
        if not p.groupNUID:
            p.showGameMsg(GMDD.data.WING_WORLD_XINMO_FB_NOT_TEAM, ())
        if not p.isTeamLeader():
            p.showGameMsg(GMDD.data.WING_WORLD_XINMO_FB_ONLY_HEADER_CAN_APPLY, ())
            return
        p.cell.applyWingWorldXinMoUniqueBoss()
        self.hide()

    def onGetAvaliableList(self):
        p = BigWorld.player()
        if p.isTeamLeader() and (p.groupNUID in self.allowGroupNUIDs or gameglobal.rds.ui.wingStageChoose.isAllowdLeader()):
            gameglobal.rds.ui.zhiQiangDuiJue.show(0, gameglobal.rds.ui.wingStageChoose.roundNo, 0)
        else:
            avaliableList = gameglobal.rds.ui.wingStageChoose.getAvaliableArena()
            if not avaliableList:
                BigWorld.player().showGameMsg(GMDD.data.WING_WORLD_XINMO_NO_AVALIABLE_ARENA, ())
                gameglobal.rds.ui.zhiQiangDuiJue.show(0, gameglobal.rds.ui.wingStageChoose.roundNo, 0)
            else:
                i = random.randint(0, len(avaliableList) - 1)
                self.show(0, gameglobal.rds.ui.wingStageChoose.roundNo, avaliableList[i])

    def getAvatarPhotoAct(self, physique):
        playerActions = WWCD.data.get('wingWorldXinMoPlayerActions', {})
        modelId = charRes.transBodyType(physique.sex, physique.bodyType)
        action = (playerActions.get((modelId, physique.school), '1101'),)
        return action
