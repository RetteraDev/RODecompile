#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArena2PersonTeamProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import commcalc
import gamelog
import utils
import const
import formula
from guis import uiUtils
from guis import uiConst
from guis import events
from guis.asObject import TipManager
from helpers import capturePhoto
from guis import menuManager
from callbackHelper import Functor
from gamestrings import gameStrings
from helpers import charRes
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD
ICON_NAME_PRE = 'BalanceArena2Person_photo3d'
SKILL_MAX_NUM = 3
DOUBLEARENA_16QIANG_TIMES = ['20:30-21:00',
 '21:00-22:00',
 '20:30-21:00',
 '21:00-22:00',
 '20:30-21:00',
 '21:00-22:00',
 '20:30-21:00',
 '21:00-22:00']
ARENA_PANEL_STAGE_INIT = 1
ARENA_PANEL_STAGE_WAITING_TEAM = 2
ARENA_PANEL_STAGE_MATCHING = 3
ARENA_PANEL_STAGE_IN_GAME = 4
ARENA_PANEL_STAGE_MATCHED = 5

class BalanceArena2PersonTeamProxy(object):

    def __init__(self):
        super(BalanceArena2PersonTeamProxy, self).__init__()
        self.widget = None
        self.arenaMode = const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA

    def initPanel(self, widget):
        self.widget = widget
        self.headGens = {}
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.clearPlayerImg()
        self.widget = None

    def initUI(self):
        self.widget.startBtn.addEventListener(events.BUTTON_CLICK, self.onStartBtnClick, False, 0, True)
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.onRewardBtnClick, False, 0, True)
        self.widget.zhanbaoBtn.addEventListener(events.BUTTON_CLICK, self.onZhanBaoBtnClick, False, 0, True)
        self.widget.templateBtn.addEventListener(events.BUTTON_CLICK, self.onTemplateBtnClick, False, 0, True)
        self.widget.skillSlot0.addEventListener(events.MOUSE_CLICK, self.showSkillMenu, False, 0, True)
        self.widget.skillSlot0.visible = False
        self.widget.skillSlot1.visible = False
        self.widget.skillName0.visible = False
        self.widget.skillName1.visible = False
        self.widget.tip.visible = False
        self.widget.skillMenuMc.visible = False
        if self.isInState16():
            self.widget.openTime.visible = False
        else:
            self.widget.openTime.visible = True
            self.widget.openTime.text = DCD.data.get('doubleArenaOpenTime', '')
        self.initSkillMenu()
        self.initScorePanels()
        p = BigWorld.player()
        p.base.dArenaQueryFightScore()

    def initScorePanels(self):
        self.widget.stateCommon.rankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick, False, 0, True)
        self.widget.stateCommon.inviteBtn.addEventListener(events.BUTTON_CLICK, self.onCheerBtnClick, False, 0, True)
        self.widget.stateCommon.dismissBtn.addEventListener(events.BUTTON_CLICK, self.onDismissBtnClick, False, 0, True)
        self.widget.stateCommon.tipText.htmlText = DCD.data.get('doubleArenaWinLoseTip', gameStrings.DOUBLE_ARENA_WIN_LOSE_TIP)
        TipManager.addTip(self.widget.stateCommon.inviteBtn, DCD.data.get('doubleArenaInviteCheerTip', ''))

    def initSkillMenu(self):
        pass

    def refreshInfo(self):
        p = BigWorld.player()
        self.stage = getattr(p, 'arenaStage', 1)
        if self.isInDoubleArenaDiGong():
            if self.stage == ARENA_PANEL_STAGE_MATCHING or self.stage == ARENA_PANEL_STAGE_WAITING_TEAM:
                self.widget.startBtn.label = gameStrings.DOUBLEARENA_QUITMATCH
            else:
                self.widget.startBtn.label = gameStrings.DOUBLEARENA_STARTMATCH
        else:
            self.widget.startBtn.label = gameStrings.DOUBLEARENA_TELEPORT
        if self.isInState16():
            self.widget.stateCommon.visible = False
            self.widget.state16.visible = True
            self.widget.zhanjiText.text = gameStrings.DOUBLEARENA_SATE16
            self.refreshMatchInfoState16()
        else:
            self.widget.zhanjiText.text = gameStrings.DOUBLEARENA_ZHANJI
            self.widget.stateCommon.visible = True
            self.widget.state16.visible = False
            self.refreshMatchInfo()
        self.refreshBuffInfo()
        self.refreshTeamInfo()
        if p.isInDoubleArenaGroup() or p.isInDoubleArenaState16():
            self.widget.startBtn.enabled = True
        else:
            self.widget.startBtn.enabled = False
        if self.isInState16():
            if not gameglobal.rds.configData.get('enableDoubleArena16QiangZhanBao', True):
                self.widget.zhanbaoBtn.visible = False
            else:
                self.widget.zhanbaoBtn.visible = True
        elif not gameglobal.rds.configData.get('enableDoubleArenaZhanBao', False):
            self.widget.zhanbaoBtn.visible = False
        else:
            self.widget.zhanbaoBtn.visible = True

    def refreshBuffInfo(self):
        p = BigWorld.player()
        self.buffType = getattr(p.doubleArenaTeamInfo, 'relation', 0)
        if self.buffType:
            self.widget.teamBuffMc.visible = True
            self.widget.teamBuffMc.textField.text = gameStrings.DOUBLEARENA_BUFF_TYPES[self.buffType - 1]
        else:
            self.widget.teamBuffMc.visible = False

    def clearPlayerImg(self):
        if self.headGens:
            for key in self.headGens.iterkeys():
                if self.headGens[key]:
                    self.headGens[key].endCapture()

    def getheadGen(self, index):
        if self.headGens.has_key(index):
            self.headGens.get(index).initFlashMesh()
            return self.headGens.get(index)
        headGen = capturePhoto.BalanceArenaPerson2PhotoGen('gui/taskmask.tga', 265, ICON_NAME_PRE + str(index))
        headGen.initFlashMesh()
        self.headGens[index] = headGen
        return headGen

    def refreshTeamInfo(self):
        p = BigWorld.player()
        teamInfo = p.doubleArenaTeamInfo
        self.widget.teamName.text = getattr(teamInfo, 'teamName', '')
        zhenyingInfos = DCD.data.get('doubleArenaZhenYingInfo', {})
        camp = getattr(teamInfo, 'camp', 0)
        self.widget.zhanyingName.text = zhenyingInfos.get(camp, {}).get('name', '')
        headGen0 = self.getheadGen(0)
        headGen0.startCaptureDummy()
        headGen0.backGroundPath = 'gui/photoGenBg/620.dds'
        headGen1 = self.getheadGen(1)
        headGen1.backGroundPath = 'gui/photoGenBg/621.dds'
        headGen1.startCaptureDummy()
        self.setPlayerInfo(0, self.generatePlayerData())
        self.setPlayerInfo(1, self.generateMateData())

    def setPlayerInfo(self, index, playerData):
        if not playerData:
            self.widget.getChildByName('name' + str(index)).text = ''
            self.widget.getChildByName('school' + str(index)).visible = False
            return
        gbId = playerData[0]
        name = playerData[1]
        physique = playerData[2]
        aspect = playerData[3]
        avatarConfig = playerData[4]
        signal = playerData[5]
        school = physique.school
        nameMc = self.widget.getChildByName('name' + str(index))
        p = BigWorld.player()
        if index == 1 and p.isInDoubleArenaGroup():
            fullName = playerData[6]
            name = "%s<font color = \'#27A5D9\'><a href=\'event:dArenaInviteMate\'><u>[%s]</u></a></font>" % (name, gameStrings.FUBEN_SOURCE_TEAM)
        nameMc.htmlText = str(name)
        self.widget.getChildByName('school' + str(index)).visible = True
        self.widget.getChildByName('school' + str(index)).gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(school, 'yuxu'))
        if index not in self.headGens.keys():
            return
        headGen = self.headGens.get(index)
        modelId = charRes.transBodyType(physique.sex, physique.bodyType)
        showFashion = commcalc.getSingleBit(signal, gametypes.SIGNAL_SHOW_FASHION)
        headGen.startCaptureRes(modelId, aspect, physique, avatarConfig, ('1901',), showFashion)

    def generatePlayerData(self):
        playerData = []
        p = BigWorld.player()
        playerData.append(p.gbId)
        playerData.append(p.playerName)
        playerData.append(p.physique)
        playerData.append(p.aspect)
        playerData.append(p.avatarConfig)
        playerData.append(p.signal)
        return playerData

    def generateMateData(self):
        playerData = []
        p = BigWorld.player()
        mateData = p.doubleArenaTeamInfo.playerTwo
        if p.doubleArenaTeamInfo.playerOne.gbId != p.gbId:
            mateData = p.doubleArenaTeamInfo.playerOne
        playerData.append(mateData.gbId)
        fullMateName = mateData.roleName
        if p._isSoul():
            fullMateName = '%s-%s' % (mateData.roleName, utils.getServerName(utils.getHostId()))
            mateName = fullMateName
            if len(mateName.decode(utils.defaultEncoding())) > 8:
                mateName = mateData.roleName
            playerData.append(mateName)
        else:
            playerData.append(mateData.roleName)
        if hasattr(p, 'doubleArenaMateInfo'):
            playerData.append(p.doubleArenaMateInfo['physique'])
            playerData.append(p.doubleArenaMateInfo['aspect'])
            playerData.append(p.doubleArenaMateInfo['avatarConfig'])
            playerData.append(p.doubleArenaMateInfo['signal'])
            playerData.append(fullMateName)
        else:
            return None
        return playerData

    def refreshMatchInfo(self):
        p = BigWorld.player()
        statistics = p.doubleArenaTeamInfo.statistics
        statistics.refreshCheers()
        matchMc = self.widget.stateCommon
        matchMc.teamScore.text = statistics.score
        matchMc.teamRank.text = getattr(p, 'doubleArenatotalScore', 0)
        matchMc.voteScore.text = gameStrings.TEXT_BALANCEARENA2PERSONTEAMPROXY_248 % (statistics.todayCheers - statistics.usedCheers)
        matchMc.value0.text = statistics.fights
        matchMc.value1.text = statistics.wins
        matchMc.value2.text = statistics.killCnt
        matchMc.value3.text = statistics.assistCnt
        matchMc.value4.text = utils.convertNum(statistics.cureVal)
        matchMc.value5.text = utils.convertNum(statistics.beDamageVal)
        matchMc.value6.text = utils.convertNum(statistics.damageVal)

    def refreshMatchInfoState16(self):
        state16Panel = self.widget.state16
        arenaStartTimes = DCD.data.get('doubleArena16QiangTimes', DOUBLEARENA_16QIANG_TIMES)
        for i in xrange(len(arenaStartTimes)):
            timeText = state16Panel.getChildByName('time%s' % str(i))
            timeText.text = arenaStartTimes[i]

    def showSkillMenu(self, *args):
        self.widget.skillMenuMc.visible = True
        self.widget.stage.focus = self.widget.skillMenuMc
        self.widget.skillMenuMc.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.hideSkillMenu, False, 0, True)

    def hideSkillMenu(self, *args):
        self.widget.skillMenuMc.visible = False
        self.widget.skillMenuMc.removeEventListener(events.FOCUS_EVENT_FOCUS_OUT)

    def isInState16(self):
        p = BigWorld.player()
        return p.isInDoubleArenaState16() or p.isInDoubleArenaStateEnd()

    def isInDoubleArenaDiGong(self):
        p = BigWorld.player()
        return formula.isDoubleArenaCrossServerML(formula.getMLGNo(p.spaceNo))

    def onChangeArenaMode(self, arenaMode):
        self.arenaMode = arenaMode
        self.refreshInfo()

    def onStartBtnClick(self, *args):
        p = BigWorld.player()
        if not self.isInDoubleArenaDiGong():
            p.cell.applyEnterDoubleArenaReadyRoom(const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA)
        else:
            stage = getattr(p, 'arenaStage', 1)
            if stage == ARENA_PANEL_STAGE_MATCHING or stage == ARENA_PANEL_STAGE_WAITING_TEAM:
                p.cancelApplyArena()
            else:
                p = BigWorld.player()
                if p.isInDoubleArenaState16():
                    p.cell.dArenaApplyEnterSixteenArena()
                else:
                    p.arenaMode = const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA
                    p.cell.dArenaApplyArena(const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA)

    def onRewardBtnClick(self, *args):
        gameglobal.rds.ui.balanceArena2PersonReward.show()

    def onZhanBaoBtnClick(self, *args):
        if not self.isInState16():
            gameglobal.rds.ui.balanceArena2PersonZhanBao.show()
        else:
            gameglobal.rds.ui.balanceArena2PersonInfo.show()

    def onTemplateBtnClick(self, *args):
        gameglobal.rds.ui.balanceArenaTemplate.show()

    def onRankBtnClick(self, *args):
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_DOUBLE_ARENA_SCORE)

    def isInDismissTeamCoolDown(self):
        coolDownTime = self.getCoolTime()
        if coolDownTime > self.getTeamCreateTime():
            return True
        return False

    def getCoolTime(self):
        return DCD.data.get('dArenaDisbandCD', 43200)

    def getTeamCreateTime(self):
        p = BigWorld.player()
        createTeamTime = getattr(p.doubleArenaTeamInfo.statistics, 'createTime', 0)
        return utils.getNow() - createTeamTime

    def onDismissBtnClick(self, *args):
        p = BigWorld.player()
        if self.isInDismissTeamCoolDown():
            remainTime = self.getCoolTime() - self.getTeamCreateTime()
            p.showGameMsg(GMDD.data.DOUBLE_ARENA_DISMISS_TEAM_COOLDOWN, (utils.formatTime(remainTime),))
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.DOUBLE_ARENA_DISSMISS_TEAM_MSG)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.base.dArenaDisbandTeam)

    def onCheerBtnClick(self, *args):
        p = BigWorld.player()
        if not p.isInDoubleArenaGroup() or not self.isInCheerTime():
            p.showGameMsg(GMDD.data.DOUBLE_ARENA_CHEER_NOT_IN_TIME, ())
            return
        statistics = p.doubleArenaTeamInfo.statistics
        statistics.refreshCheers()
        totalLimit = DCD.data.get('dArenaTotalCheersLimit', 30)
        todayLimit = DCD.data.get('dArenaDayCheersLimit', 6)
        todayCheer = statistics.todayCheers
        totalCheer = statistics.totalCheers
        limit = todayLimit
        rest = todayCheer
        if limit <= rest:
            p.showGameMsg(GMDD.data.DOUBLE_ARENA_CHEER_DAY_LIMIT, ())
            return
        if totalLimit <= totalCheer:
            p.showGameMsg(GMDD.data.DOUBLE_ARENA_CHEER_TOTAL_LIMIT, ())
            return
        todayRestTime = totalLimit - totalCheer + todayCheer
        if todayRestTime < todayLimit:
            limit = todayRestTime
        p = BigWorld.player()
        linkText = gameStrings.TEXT_BALANCEARENA2PERSONTEAMPROXY_379 % (p.doubleArenaTeamInfo.teamName,
         p.doubleArenaTeamInfo.playerOne.gbId,
         const.SYMBOL_RENAME_SPLIT,
         str(utils.getNow()),
         const.SYMBOL_RENAME_SPLIT,
         p.roleName,
         rest,
         limit)
        gameglobal.rds.ui.sendLink(linkText)

    def isInCheerTime(self):
        doubleArenaCheerStartTimes = DCD.data.get('doubleArenaCheerStartTimes', ())
        doubleArenaCheerEndTimes = DCD.data.get('doubleArenaCheerEndTimes', ())
        if doubleArenaCheerStartTimes and doubleArenaCheerStartTimes:
            if utils.inCrontabsRange(doubleArenaCheerStartTimes, doubleArenaCheerEndTimes):
                return True
        return False
