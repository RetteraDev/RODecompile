#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impMultiLine.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gamelog
import const
import formula
import utils
import gametypes
import appSetting
from guis import messageBoxProxy
from callbackHelper import Functor
from guis import uiUtils
from guis import uiConst
from sfx import screenEffect
from sfx import screenRipple
from data import digong_boss_room_data as DBRD
from data import game_msg_data as GMD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from data import multiline_digong_data as MDD
from data import sys_config_data as SCD

class ImpMultiLine(object):

    def pvpQuery(self, memInfo, header, arrange):
        self.pvpMemInfo = memInfo
        self.pvpHeader = header
        self.pvpArrange = arrange

    def multiLineArrange(self, arrange):
        self.pvpArrange = arrange
        gameglobal.rds.ui.group.refreshGroupInfo()

    def showMultiLine(self, transportEntId):
        transport = BigWorld.entity(transportEntId)
        if transport and transport.inTrap(self):
            gameglobal.rds.ui.diGong.show(transportEntId)

    def onGetLineInfo(self, mlgNo, res):
        gameglobal.rds.ui.diGong.setLineInfo(mlgNo, res)

    def multiLineClockCmd(self, cmd, args):
        if cmd == const.CLOCK_SHOW:
            if gameglobal.rds.ui.diGong.clockShow:
                gameglobal.rds.ui.diGong.closeDigongClock()
            gameglobal.rds.ui.diGong.showDigongClock(*args)
        if cmd == const.CLOCK_CLOSE:
            gameglobal.rds.ui.diGong.closeDigongClock()

    def inBossRoom(self):
        mlgNo = formula.getMLGNo(self.spaceNo)
        return formula.getMLNo(self.spaceNo) == DBRD.data.get(mlgNo, {}).get('bossRoomSpaceNo')

    def checkCanQuickJoinDiGongGroup(self):
        if not gameglobal.rds.configData.get('enableDiGongQuickJoinGroup', False):
            return False
        if self.groupNUID > 0:
            return False
        mlgNo = formula.getMLGNo(self.spaceNo)
        if not formula.inMultiLine(mlgNo):
            return False
        quickJoinGroup = MDD.data.get(mlgNo, {}).get('quickJoinGroup', 0)
        if not quickJoinGroup:
            return False
        if self.exceedYaoliLimit():
            return False
        return True

    def isInLueYingGu(self):
        return formula.getMLGNo(self.spaceNo) == const.ML_GROUP_NO_LUEYINGGU

    def backToBasicFloor(self):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_IMPPLAYERTEAM_595, self.afterBackToBasicFloorConfirm, True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None, True, True)]
        msg = gameStrings.TEXT_IMPMULTILINE_86
        self.msgBoxId = gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPMULTILINE_88, msg, buttons)

    def afterBackToBasicFloorConfirm(self):
        self.cell.backToBasicFloorAfterConfirm()

    def set_chessBoxNo(self, old):
        ents = BigWorld.entities.values()
        for ent in ents:
            if ent.classname() != 'ChessBox':
                continue
            ent.onChangePlayerChessBoxNo()

        gameglobal.rds.ui.daFuWeng.updateChessBoxNo()

    def setChessBoxStatus(self, status):
        self.chessBoxStatus = status
        canDice = self.chessBoxStatus & 1
        canSlots = self.chessBoxStatus & 2
        gameglobal.rds.ui.daFuWeng.updateChessBoxStatus(canDice, canSlots)

    def sendSlotsVal(self, slot):
        gameglobal.rds.ui.daFuWeng.setSlotsVal(slot)

    def setLastFloorPerformance(self, performance):
        gameglobal.rds.ui.daFuWeng.updateFloorPerformance(performance)

    def setDiceResult(self, diceResult):
        gameglobal.rds.ui.daFuWeng.showDiceResult(diceResult)

    def enterLineFailTicket(self, mlgNo, ticketId):
        ticketName = ID.data.get(ticketId, {}).get('name', '')
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, Functor(self.cell.confirmUseTicket, mlgNo), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None, True, True)]
        msg = GMD.data.get(GMDD.data.ENTER_LINE_USE_ITEM, {}).get('text', gameStrings.TEXT_IMPMULTILINE_122) % (ticketName,)
        self.enterLineMsgBoxId = gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPMULTILINE_124, msg, buttons)

    def onQueryLingzhuInfo(self, mlgNo, lingzhuInfo):
        gamelog.debug('zt: onQueryLingzhuInfo', mlgNo, lingzhuInfo)
        gameglobal.rds.ui.diGong.setLingzhuInfo(lingzhuInfo)

    def getMLExpStat(self):
        if not hasattr(self, 'tMLExpStat'):
            return 0
        tOldStat = utils.getHourInt(self.tMLExpStat) + utils.getMinuteInt(self.tMLExpStat) / 60.0
        tNow = utils.getHourInt() + utils.getMinuteInt() / 60.0
        tReset = SCD.data.get('tResetMLExpStat', 5)
        if not utils.isSameDay(self.tMLExpStat, utils.getNow()):
            tNow += 24
            tReset += 24
        if tOldStat < tReset and tNow >= tReset:
            self.mlExpStat = 0
        return self.mlExpStat

    def sendMLExpStats(self, mlExpStat, tMLExpStat):
        self.mlExpStat = mlExpStat
        self.tMLExpStat = tMLExpStat

    def getMaxLingzhuDigongLv(self):
        self.base.getMaxLingzhuDigongLv()
        if hasattr(self, 'maxLingzhuLv'):
            return self.maxLingzhuLv
        else:
            return None

    def sendMaxLingzhuDigongLv(self, lingzhuLvs):
        self.maxLingzhuLv = lingzhuLvs
        gameglobal.rds.ui.diGongDetail.updateDigongDict(lingzhuLvs)
        gameglobal.rds.ui.diGongDetail.refreshDigongDetail()

    def onGetYmfMemberInfo(self, info, finished):
        if not hasattr(self, 'ymfMemberInfoCache'):
            self.ymfMemberInfoCache = {}
        self.ymfMemberInfoCache.update(info)
        if finished:
            teamArr = []
            for gbId, mebmerInfo in self.ymfMemberInfoCache.iteritems():
                pos = mebmerInfo.get(gametypes.TEAM_SYNC_PROPERTY_POSITION, (0, 0, 0))
                roleName = mebmerInfo.get(gametypes.TEAM_SYNC_PROPERTY_ROLENAME, '')
                entityId = mebmerInfo.get(gametypes.TEAM_SYNC_PROPERTY_ENTID, '')
                chunkName = getattr(self, 'chunk', '')
                isJieQi = uiUtils.isJieQiTgt(gbId)
                isZhenChuan = uiUtils.isZhenChuanTgt(gbId)
                isPartner = False
                if gbId in getattr(self, 'partner', {}):
                    isPartner = True
                isMarriageTgt = False
                if roleName == self.marriageTgtName:
                    isMarriageTgt = True
                teamArr.append([pos,
                 gbId,
                 roleName,
                 self.spaceNo,
                 chunkName,
                 entityId,
                 False,
                 False,
                 self.isInMyTeamByGbId(gbId),
                 isJieQi,
                 isZhenChuan,
                 isPartner,
                 isMarriageTgt])

            self.ymfMemberInfoCache.clear()
            gameglobal.rds.ui.map.addTeamMate(teamArr)
            gameglobal.rds.ui.littleMap.showTeamMate(teamArr)

    def notifyMultilineActivate(self, mlgNo, lineNo, floorNo):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_IMPMULTILINE_193, Functor(self.afterCheckForMultilineActivate, mlgNo, lineNo, floorNo), True, False), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, None)]
        msg = GMD.data.get(GMDD.data.ENTER_LINE_ACTIVATE_BY_HEADER, {}).get('text', gameStrings.TEXT_IMPMULTILINE_195) % (MDD.data[mlgNo].get('name', ''),)
        self.msgBoxId = gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_IMPMULTILINE_196, msg, buttons)

    def afterCheckForMultilineActivate(self, mlgNo, lineNo, floorNo):
        BigWorld.player().cell.enterLineAfterCheck(mlgNo, lineNo, floorNo, 0)
        self.messageBoxAutoDismiss(self.msgBoxId)

    def set_lingShiFlag(self, old):
        entityList = []
        for entity in BigWorld.entities.values():
            if entity.__class__.__name__ in ('Npc', 'TreasureBox', 'QuestBox', 'Dawdler'):
                entityList.append(entity)

        if self.lingShiFlag:
            for entity in entityList:
                entity.addLingShiExtraTint()
                entity.refreshOpacityState()

            self.onEnterLingShi()
        else:
            for entity in entityList:
                entity.delLingShiExtraTint()
                entity.refreshOpacityState()

            self.onLeaveLingShi()
        gameglobal.rds.ui.actionbar.setRideShine(self.lingShiFlag, uiConst.LING_SHI_FLAG_SWITCH)
        self.showGameMsg(GMDD.data.ENTER_LING_SHI if self.lingShiFlag else GMDD.data.LEAVE_LING_SHI)

    def onEnterLingShi(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        index = SCD.data.get('lingShiShaderIndex', 2)
        appSetting.lockShaderIndex(index)
        screenEffect.startEffect(gameglobal.EFFECT_TAG_LING_SHI, const.LING_SHI_STATE_SCREEN_EFF)
        self.addFakeState(const.LING_SHI_STATE_CLIENT_STATE)
        screenRipple.rippleScreen()

    def onLeaveLingShi(self):
        appSetting.restoreShader()
        screenEffect.ins.delScreenEffect(gameglobal.EFFECT_TAG_LING_SHI, True)
        self.quitFakeState(const.LING_SHI_STATE_CLIENT_STATE)
        screenRipple.rippleScreen()

    def switchLingShiFlag(self):
        if self.lingShiFlag:
            if self.inMLSpace():
                mlgNo = formula.getMLGNo(self.spaceNo)
                if MDD.data.get(mlgNo, {}).get('isLingShi', 0):
                    if not (gameglobal.rds.ui.messageBox.loadeds or gameglobal.rds.ui.messageBox.loadings):
                        text = GMD.data.get(GMDD.data.EXIT_LINGSHI_CONFIRM, {}).get('text', 'GMDD.data.EXIT_LINGSHI_CONFIRM')
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(text, Functor(self.cell.changeLingShiFlag, False))
                    return
            self.cell.changeLingShiFlag(False)
        else:
            self.cell.changeLingShiFlag(True)
