#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/deadAndReliveProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import const
import gameglobal
import gametypes
import gamelog
import formula
import uiUtils
import logicInfo
import utils
import wingWorldUtils
from ui import gbk2unicode
from ui import unicode2gbk
from guis import ui
from uiProxy import UIProxy
from guis import uiConst
from callbackHelper import Functor
from helpers import deadPlayBack
from item import Item
from gamestrings import gameStrings
from data import battle_field_data as BFD
from data import map_config_data as MCD
from data import game_msg_data as GMD
from data import mapSearch_ii_data as MII
from data import sys_config_data as SCD
from data import item_data as ID
from data import relive_pos_data as RPD
from data import vip_service_data as VSD
from data import world_war_config_data as WWCD
from data import duel_config_data as DCD
from data import wing_world_config_data as WINGCD
from cdata import game_msg_def_data as GMDD

class DeadAndReliveProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DeadAndReliveProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickAcceptReliveBtn': self.onClickAcceptReliveBtn,
         'clickReturnReliveBtn': self.onClickReturnReliveBtn,
         'clickReliveBtn': self.onClickReliveBtn,
         'isReliveEnable': self.onIsReliveEnable,
         'getOption': self.onGetOption,
         'deadBloodLoaded': self.onDeadBloodLoaded,
         'getReliveTime': self.onGetReliveTime,
         'isInBattleField': self.onIsInBattleField,
         'forceRelive': self.onForceRelive,
         'getReliveHereCD': self.onGetReliveHereCD,
         'getReliveNearTip': self.onGetReliveNearTip,
         'doReliveLingHunShi': self.onDoReliveLingHunShi,
         'needShowGuildBtn': self.onNeedShowGuildBtn,
         'clickGuildReliveBtn': self.onClickGuildReliveBtn,
         'clickSoulReliveBtn': self.onClickSoulReliveBtn,
         'getSoulReliveCD': self.onGetSoulReliveCD,
         'getClanWarFlag': self.onGetClanWarFlag,
         'getTipDesc': self.onGetTipDesc,
         'getClanWarReliveCD': self.onGetClanWarReliveCD,
         'getBtnVisible': self.onGetBtnVisible,
         'clickBtn': self.onClickBtn,
         'isGetLvLimitReliveFree': self.onIsGetLvLimitReliveFree,
         'getLvLimitReliveFreeTipDesc': self.onGetLvLimitReliveFreeTipDesc,
         'isBfHunt': self.onIsBfhunt,
         'getReliveCountDownCnt': self.onGetReliveCountDownCnt,
         'isBfDota': self.onIsBfDota,
         'addWeakerProtect': self.onAddWeakerProtect,
         'isTriggerWeakProtect': self.onIsTriggerWeakProtect,
         'getWeakProtectTip': self.onGetWeakProtectTip,
         'isinWingWorldWar': self.onIsInWingWorldWar,
         'isClanWarCourier': self.onIsClanWarCourier,
         'getClanWarCourierTip': self.onGetClanWarCourierTip,
         'isInPUBG': self.onIsInPUBG,
         'obTgtInPUBG': self.onObTgtInPUBG,
         'leaveInPUBG': self.onLeaveInPUBG,
         'getDataInPUBG': self.onGetDataInPUBG}
        self.mediator = None
        self.enableRelive = True
        self.enableAtPoint = True
        self.options = None
        self.isShow = False
        self.callbackHandler = None
        self.reliveTime = 0
        self.reliveCallback = 0
        self.isBfReliveCounting = False
        self.bfCountingTimeStamp = 0
        self.isGuildReliveCounting = False
        self.guildCountingTimeStamp = 0
        self.tip = ''
        self.msgBoxId = None
        self.reliveHereType = 0
        self.vipValidCount = -1
        self.isServer = False
        self.isTriggerWeakProtect = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DEAD_RELIVE:
            self.mediator = mediator

    def onClickAcceptReliveBtn(self, *arg):
        BigWorld.player().onConfirmReliveByOther(True)

    def reliveInCommonBattleField(self):
        p = BigWorld.player()
        self.cancelBFForceReliveTimer()
        p.battleFieldConfirmRelive()

    def onClickReturnReliveBtn(self, *arg):
        p = BigWorld.player()
        if self.canSelectRelivePos():
            self.uiAdapter.relivePosSelect.show()
        elif p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.reliveInCommonBattleField()
        elif p.inFubenType(const.FB_TYPE_SHENGSICHANG):
            p.cell.leaveShengSiChang()
        elif p.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            msg = uiUtils.getTextFromGMD(GMDD.data.TEAM_SSC_RELIVE_MSG, 'relive?')
            self.msgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=p.cell.leaveTeamShengSiChang)
        else:
            spaceNo = formula.getMapId(p.spaceNo)
            if p.inFuben() and not p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD) and not p.inFubenTypes(const.FB_TYPE_ARENA) and MCD.data.get(spaceNo, {}).get('reliveSpaceNo', 0):
                msg = GMD.data.get(GMDD.data.RELIVE_OUTSIDE, {}).get('text', gameStrings.TEXT_DEADANDRELIVEPROXY_126)
                self.msgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self._doReliveOrigin, noCallback=self._cancelReliveOrigin)
            else:
                p.reliveOrigin()

    def _doReliveOrigin(self):
        BigWorld.player().reliveOrigin()
        self.msgBoxId = None

    def _cancelReliveOrigin(self):
        self.msgBoxId = None

    def cancelBFForceReliveTimer(self):
        if self.mediator:
            self.mediator.Invoke('cancelForceReliveRimer')

    @ui.callFilter(1)
    def onClickReliveBtn(self, *arg):
        if self.enableRelive:
            p = BigWorld.player()
            spaceNo = formula.getMapId(p.spaceNo)
            reliveHereType = MCD.data.get(spaceNo, {}).get('reliveHereType', gametypes.RELIVE_HERE_TYPE_FORBID)
            if uiUtils.isInFubenShishenLow():
                reliveHereType = gametypes.RELIVE_HERE_TYPE_NORMAL
            if reliveHereType == gametypes.RELIVE_HERE_TYPE_NORMAL:
                if p.inClanWar and p.clanWarStatus:
                    typeList = [Item.SUBTYPE_2_RELIVE_CW, Item.SUBTYPE_2_RELIVE]
                    callBackType = Item.SUBTYPE_2_RELIVE_CW
                    p.cell.probePassiveItemByAttribute(['cstype', 'cstype'], typeList, callBackType)
                elif utils.enableReliveAutoWithLvLess() and p.lv <= SCD.data.get('AUTO_RELIVE_LV', 29):
                    self.confirmRelive()
                else:
                    typeList = [Item.SUBTYPE_2_RELIVE]
                    callBackType = Item.SUBTYPE_2_RELIVE
                    p.cell.probePassiveItemByAttribute(['cstype'], typeList, callBackType)
            elif reliveHereType == gametypes.RELIVE_HERE_TYPE_WW and gameglobal.rds.configData.get('enableCrossBoarderReliveNow', False) and (formula.inWorldWar(p.spaceNo) or formula.spaceInWorldWarRob(p.spaceNo)):
                wwReliveItemCost = SCD.data.get('wwReliveItemCost')
                if not wwReliveItemCost:
                    return
                if p.dieNumInBoarder < wwReliveItemCost[0][0]:
                    msg = WWCD.data.get('reliveWWNormalMsg', '')
                    self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=self.confirmRelive, title=gameStrings.TEXT_DEADANDRELIVEPROXY_176)
                else:
                    for lowerBound, upperBound, itemId, itemNum in wwReliveItemCost:
                        if lowerBound <= p.dieNumInBoarder <= upperBound:
                            msg = WWCD.data.get('reliveWWCostMsg', '%s_%s/%s') % (p.dieNumInBoarder, itemNum, itemNum * WWCD.data.get('WWContribToYinhundanRatio', 1500))
                            self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=self.confirmRelive, title=gameStrings.TEXT_DEADANDRELIVEPROXY_176, itemData=uiUtils.getGfxItemById(itemId, itemNum))
                            return

            elif reliveHereType == gametypes.RELIVE_HERE_TYPE_WING and formula.spaceInWingBornIslandOrPeaceCity(p.spaceNo):
                if formula.spaceInWingPeaceCity(p.spaceNo) and not p.wingWorldFreeReliveCnt:
                    msg = WINGCD.data.get('peaceCityReliveFrameConfirm', '') % wingWorldUtils.getPeaceCityReliveHereFrameCost()
                else:
                    msg = WINGCD.data.get('peaceCityReliveNoFrameConfirm', '')
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=self.confirmReliveFrame, title=gameStrings.TEXT_DEADANDRELIVEPROXY_193)
            else:
                self.confirmRelive()

    def reliveShowMessage(self, found, page, pos):
        if found:
            item = BigWorld.player().realInv.getQuickVal(page, pos)
        else:
            item = None
        if item:
            self.setReliveHereType()
            if self.reliveHereType == gametypes.RELIVE_HERE_TYPE_COUNT and self.isServer:
                self.confirmRelive()
            else:
                reliveText = GMD.data.get(GMDD.data.RELIVE_DESC, {}).get('text', gameStrings.TEXT_DEADANDRELIVEPROXY_207) % item.name
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(reliveText, self.confirmRelive)
        else:
            self.confirmRelive()

    def onGetTipDesc(self, *arg):
        tipDesc = []
        self.setReliveHereType()
        reliveTipDesc = SCD.data.get('reliveTipDesc', gameStrings.TEXT_DEADANDRELIVEPROXY_215)
        clanWarReliveTipDesc = SCD.data.get('clanWarReliveTipDesc', gameStrings.TEXT_DEADANDRELIVEPROXY_216)
        countReliveTipDesc = SCD.data.get('countReliveTipDesc', gameStrings.TEXT_DEADANDRELIVEPROXY_217 % self.vipValidCount)
        p = BigWorld.player()
        if p.lv < SCD.data.get('lvLimitReliveFree', 30):
            reliveTipDesc = SCD.data.get('lvLimitReliveFreeTipDesc', gameStrings.TEXT_DEADANDRELIVEPROXY_220)
            countReliveTipDesc = SCD.data.get('lvLimitReliveFreeTipDesc', gameStrings.TEXT_DEADANDRELIVEPROXY_220)
        wingReliveTipDesc = SCD.data.get('wingReliveTipDesc', gameStrings.TEXT_DEADANDRELIVEPROXY_222)
        tipDesc.append(reliveTipDesc)
        tipDesc.append(clanWarReliveTipDesc)
        tipDesc.append(countReliveTipDesc)
        tipDesc.append(wingReliveTipDesc)
        return uiUtils.array2GfxAarry(tipDesc, True)

    def confirmRelive(self):
        BigWorld.player().reliveHere()

    def confirmReliveLingHunShi(self):
        if self.mediator:
            self.mediator.Invoke('playLingHunShiAnimation')

    def confirmReliveFrame(self):
        BigWorld.player().reliveByFrame()

    def cancelReliveLingHunShi(self):
        if self.mediator:
            self.mediator.Invoke('refreshState', GfxValue(self.reliveHereType))

    def onIsReliveEnable(self, *arg):
        p = BigWorld.player()
        self.setReliveHereType()
        flagState = p.flagStateCommon.get(gametypes.FLAG_STATE_ID_LIN_HUN_SHI)
        flagCnt = flagState.flagCnt if flagState else 0
        spaceNo = formula.getMapId(p.spaceNo)
        canUseLingHunShi = MCD.data.get(spaceNo, {}).get('canUseLingHunShi', 0)
        ret = [self.enableRelive,
         self.enableAtPoint,
         self.reliveHereType,
         flagCnt,
         canUseLingHunShi]
        return uiUtils.array2GfxAarry(ret)

    def onGetOption(self, *arg):
        gamelog.debug('wy:onGetOption', self.options)
        ret = self.movie.CreateArray()
        if self.options:
            ret.SetElement(0, GfxValue(gbk2unicode(self.options[0])))
            ret.SetElement(1, GfxValue(self.options[1]))
        return ret

    def onDeadBloodLoaded(self, *arg):
        p = BigWorld.player()
        if p.hp and p.life == gametypes.LIFE_ALIVE and float(p.hp) / p.mhp < 0.05:
            gameglobal.rds.ui.deadAndRelive.showBloodBg()
        else:
            gameglobal.rds.ui.deadAndRelive.closeBloodBg()

    def show(self, enableRelive, enableAtPoint = True, beRelived = False, options = None, reliveHereType = 0):
        p = BigWorld.player()
        if gameglobal.rds.GameState == gametypes.GS_LOGIN:
            return
        elif p.isInPUBG() and not self.checkShowDeadRelivePanelInPUBG():
            return
        elif gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            if self.callbackHandler:
                BigWorld.cancelCallback(self.callbackHandler)
                self.callbackHandler = None
            if not p.isInBfDota():
                self.callbackHandler = BigWorld.callback(1, Functor(self.show, enableRelive, enableAtPoint, beRelived, options))
            return
        else:
            p = BigWorld.player()
            if not beRelived and p.inFubenTypes(const.FB_TYPE_ARENA):
                return
            if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
                self.isBfReliveCounting = False
            self.isGuildReliveCounting = False
            if beRelived:
                self.enableAtPoint = False
                self.enableRelive = False
            else:
                self.enableRelive = enableRelive
                self.enableAtPoint = enableAtPoint
                BigWorld.beginGrayFilter(3)
            self.options = options
            self.reliveHereType = reliveHereType
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DEAD_RELIVE)
            if not gameglobal.rds.ui.isHideAllUI():
                if p.bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
                    if gameglobal.rds.ui.zaiju.mediator:
                        gameglobal.rds.ui.zaiju.mediator.Invoke('setVisible', GfxValue(False))
                    elif gameglobal.rds.ui.zaijuV2.widget and gameglobal.rds.ui.zaijuV2.showType != uiConst.ZAIJU_SHOW_TYPE_EXIT:
                        self.uiAdapter.zaijuV2.widget.visible = False
                elif gameglobal.rds.ui.skill.inAirBattleState():
                    gameglobal.rds.ui.airbar.showAirbar(False)
                else:
                    if gameglobal.rds.ui.actionbar.mc != None:
                        gameglobal.rds.ui.actionbar.mc.Invoke('setVisible', GfxValue(False))
                    if gameglobal.rds.ui.actionbar.wsMc != None:
                        gameglobal.rds.ui.actionbar.wsMc.Invoke('setVisible', GfxValue(False))
                for i in xrange(2):
                    if gameglobal.rds.ui.actionbar.itemMc[i] != None:
                        gameglobal.rds.ui.actionbar.itemMc[i].Invoke('setVisible', GfxValue(False))

                gameglobal.rds.ui.expbar.setVisible(False)
                gameglobal.rds.ui.bullet.setVisible(False)
                if gameglobal.rds.ui.assign.isTeamBagShow:
                    gameglobal.rds.ui.assign.closeTeambag()
                if gameglobal.rds.ui.qinggongBar.thisMc:
                    gameglobal.rds.ui.qinggongBar.thisMc.SetVisible(False)
            else:
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_DEAD_RELIVE, True)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ACTION_BARS, False)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_WUSHUANG_BARS, False)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ITEMBAR, False)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ITEMBAR2, False)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_EXPBAR, False)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_AIR_BATTLE_BAR, False)
            self.isShow = True
            if p.inFubenTypes(const.FB_TYPE_ALL_FB):
                deadPlayBack.getInstance().doCalcData()
            return

    def bfReliveCountDown(self):
        p = BigWorld.player()
        if not p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return
        elif not p.inWorld:
            return
        elif self.isBfReliveCounting:
            return
        elif not p.battleFieldTeam.has_key(p.gbId):
            return
        else:
            bfStatsInfo = p.battleFieldTeam[p.gbId]
            if bfStatsInfo is None:
                return
            bfStatsInfo['isConfirmRelive'] = True
            if bfStatsInfo['isConfirmRelive']:
                self.reliveTime = uiUtils.getBFReliveTime(bfStatsInfo)
                gamelog.debug('@hjx bf#BFReliveCountDown1:', self.reliveTime, self.isBfReliveCounting)
                if self.reliveTime > 0:
                    self.isBfReliveCounting = True
                    self.bfCountingTimeStamp = p.getServerTime()
                    p.showGameMsg(GMDD.data.BATTLE_FIELD_RELIVE_COUNT_DOWN, (self.reliveTime,))
                    if self.reliveCallback:
                        BigWorld.cancelCallback(self.reliveCallback)
                    self.reliveCallback = BigWorld.callback(1, self._reliveCounting)
            return

    def _reliveCounting(self):
        p = BigWorld.player()
        self.reliveCallback = 0
        curTimeStamp = p.getServerTime()
        delta = curTimeStamp - self.bfCountingTimeStamp
        gamelog.debug('@hjx bf#_reliveCounting:', self.bfCountingTimeStamp, curTimeStamp, int(delta), self.reliveTime)
        self.reliveTime -= int(delta)
        if self.reliveTime <= 0 or p.life == gametypes.LIFE_ALIVE:
            if self.reliveCallback:
                BigWorld.cancelCallback(self.reliveCallback)
        else:
            p.showGameMsg(GMDD.data.BATTLE_FIELD_RELIVE_COUNT_DOWN, (self.reliveTime,))
            if self.reliveCallback:
                BigWorld.cancelCallback(self.reliveCallback)
            self.reliveCallback = BigWorld.callback(1, self._reliveCounting)
        self.bfCountingTimeStamp = curTimeStamp

    def guildReliveCountDown(self, reliveInterval):
        p = BigWorld.player()
        if not p.inWorld:
            return
        if self.isGuildReliveCounting:
            return
        self.reliveTime = reliveInterval
        if self.reliveTime > 0:
            self.isGuildReliveCounting = True
            self.guildCountingTimeStamp = p.getServerTime()
            p.showGameMsg(GMDD.data.CLAN_WAR_GUILD_RELIVE_COUNT_DOWN, (self.reliveTime,))
            if self.reliveCallback:
                BigWorld.cancelCallback(self.reliveCallback)
            self.reliveCallback = BigWorld.callback(1, self._guildReliveCounting)

    def _guildReliveCounting(self):
        p = BigWorld.player()
        self.reliveCallback = 0
        curTimeStamp = p.getServerTime()
        delta = curTimeStamp - self.guildCountingTimeStamp
        self.reliveTime -= int(delta)
        if self.reliveTime <= 0 or p.life == gametypes.LIFE_ALIVE:
            if self.reliveCallback:
                BigWorld.cancelCallback(self.reliveCallback)
        else:
            p.showGameMsg(GMDD.data.CLAN_WAR_GUILD_RELIVE_COUNT_DOWN, (self.reliveTime,))
            if self.reliveCallback:
                BigWorld.cancelCallback(self.reliveCallback)
            self.reliveCallback = BigWorld.callback(1, self._guildReliveCounting)
        self.guildCountingTimeStamp = curTimeStamp

    def clearWidget(self):
        if self.callbackHandler:
            BigWorld.cancelCallback(self.callbackHandler)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DEAD_RELIVE)
        self.uiAdapter.relivePosSelect.hide()
        if not gameglobal.rds.ui.isHideAllUI():
            if BigWorld.player() and BigWorld.player().bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
                if gameglobal.rds.ui.zaiju.mediator:
                    gameglobal.rds.ui.zaiju.mediator.Invoke('setVisible', GfxValue(True))
                elif gameglobal.rds.ui.zaijuV2.widget and gameglobal.rds.ui.zaijuV2.showType != uiConst.ZAIJU_SHOW_TYPE_EXIT:
                    self.uiAdapter.zaijuV2.widget.visible = True
            elif gameglobal.rds.ui.skill.inAirBattleState():
                gameglobal.rds.ui.airbar.showAirbar(True)
            elif not formula.inHuntBattleField(BigWorld.player().mapID):
                if gameglobal.rds.ui.actionbar.mc != None:
                    gameglobal.rds.ui.actionbar.mc.Invoke('setVisible', GfxValue(True))
                if gameglobal.rds.ui.actionbar.wsMc != None:
                    gameglobal.rds.ui.actionbar.wsMc.Invoke('setVisible', GfxValue(True))
            if not formula.inHuntBattleField(BigWorld.player().mapID) and not formula.inDotaBattleField(BigWorld.player().mapID):
                for i in xrange(2):
                    if gameglobal.rds.ui.actionbar.itemMc[i] != None:
                        gameglobal.rds.ui.actionbar.itemMc[i].Invoke('setVisible', GfxValue(True))

            gameglobal.rds.ui.expbar.setVisible(True)
            gameglobal.rds.ui.bullet.setVisible(True)
            if gameglobal.rds.ui.qinggongBar.thisMc:
                gameglobal.rds.ui.qinggongBar.changeQinggongBarState(True, False)
        else:
            if not formula.inDotaBattleField(BigWorld.player().mapID):
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ITEMBAR, True)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ITEMBAR2, True)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ACTION_BARS, True)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_WUSHUANG_BARS, True)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_AIR_BATTLE_BAR, True)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_EXPBAR, True)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_DEAD_RELIVE, False)
        BigWorld.endGrayFilter(1)
        self.mediator = None
        self.isShow = False
        self.tip = ''
        self.msgBoxId = None
        self.reliveHereType = 0
        self.isTriggerWeakProtect = False

    def beRelived(self, name, timeInterval):
        if self.mediator != None:
            self.mediator.Invoke('setBtnEnabled', (GfxValue(gbk2unicode(name)), GfxValue(timeInterval)))

    def showBloodBg(self):
        p = BigWorld.player()
        if p.physique.sex == const.SEX_MALE:
            if not gameglobal.rds.sound.haveSdHandle(gameglobal.SD_63):
                gameglobal.rds.sound.playSound(gameglobal.SD_63)
        elif not gameglobal.rds.sound.haveSdHandle(gameglobal.SD_82):
            gameglobal.rds.sound.playSound(gameglobal.SD_82)

    def closeBloodBg(self):
        try:
            p = BigWorld.player()
            if p.physique.sex == const.SEX_MALE:
                gameglobal.rds.sound.stopSound(gameglobal.SD_63)
            else:
                gameglobal.rds.sound.stopSound(gameglobal.SD_82)
        except:
            pass

    def onGetReliveTime(self, *arg):
        p = BigWorld.player()
        reliveTime = 0
        forceReliveTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('forceReliveTime', 60)
        deltaOfReliveTime = forceReliveTime - int(p.getServerTime() - p.bfTimeRec.get('tDeath', 0))
        if p.isBfTroopLogon:
            reliveTime = 0 if deltaOfReliveTime <= 0 else deltaOfReliveTime
        else:
            reliveTime = forceReliveTime
        gamelog.debug('@hjx dead#onGetReliveTime:', reliveTime, forceReliveTime, deltaOfReliveTime, p.isBfTroopLogon)
        return GfxValue(reliveTime)

    def onIsInBattleField(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD))

    def onForceRelive(self, *arg):
        p = BigWorld.player()
        if p.isInPUBG():
            return
        p.battleFieldConfirmRelive()

    def onGetReliveHereCD(self, *arg):
        ret = 0
        p = BigWorld.player()
        if self.reliveHereType == gametypes.RELIVE_HERE_TYPE_FREE:
            return GfxValue(ret)
        else:
            if p.inFuben():
                reliveItemId = SCD.data.get('fuBenReliveItemId', uiConst.FU_BEN_RELIVE_ITEM_ID)
            elif p.inClanWar and p.clanWarStatus:
                reliveItemId = SCD.data.get('clanWarReliveItemId', uiConst.CLAN_WAR_ITEM_ID)
            else:
                reliveItemId = SCD.data.get('worldReliveItemId', uiConst.WORLD_RELIVE_ITEM_ID)
            cdgroup = ID.data.get(reliveItemId, {}).get('cdgroup', 0)
            if cdgroup:
                cd = logicInfo.commonCooldownItem.get(cdgroup, None)
            else:
                cd = logicInfo.cooldownItem.get(reliveItemId, None)
            if cd:
                ret = max(0, cd[0] - BigWorld.time())
            return GfxValue(ret)

    def onGetClanWarReliveCD(self, *arg):
        return GfxValue(max(0, getattr(BigWorld.player(), 'clanWarReliveStamp', 0) - utils.getNow()))

    def onGetBtnVisible(self, *args):
        btnName = unicode2gbk(args[3][0].GetString())
        val = False
        p = BigWorld.player()
        if btnName == 'camp':
            val = p.inWorldWarEx() or p.inWingWarCity()
        if btnName == 'town':
            val = not p.inWorldWarEx() and not p.inWingWarCity()
        if btnName == 'here':
            val = not p.inWorldWarBattle() and not p.inWingWarCity()
        return GfxValue(val)

    def onClickBtn(self, *args):
        btnName = unicode2gbk(args[3][0].GetString())
        p = BigWorld.player()
        if btnName == 'camp':
            if p.inWingWarCity():
                self.uiAdapter.map.openMap(True, uiConst.MAP_TYPE_TRANSPORT)
            else:
                self.uiAdapter.relivePosSelect.show()
        if btnName == 'jct':
            BigWorld.player().reliveClanWarYaBiao()

    def onGetReliveNearTip(self, *arg):
        if self.canSelectRelivePos():
            return GfxValue(gbk2unicode(gameStrings.TEXT_DEADANDRELIVEPROXY_586))
        return GfxValue(gbk2unicode(self.tip))

    def setReliveNearBtnEnable(self, enable):
        if self.mediator != None:
            self.mediator.Invoke('setReliveNearBtnEnable', GfxValue(enable))
        if not enable and self.msgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.msgBoxId)
            self.msgBoxId = None

    def onDoReliveLingHunShi(self, *arg):
        BigWorld.player().reliveByLinHunShi()

    def onNeedShowGuildBtn(self, *arg):
        p = BigWorld.player()
        return GfxValue((formula.spaceInWorld(p.spaceNo) or formula.spaceInWingBornIsland(p.spaceNo)) and not formula.spaceInWorldWarEx(p.spaceNo) and not p.inWingWarCity())

    def onClickGuildReliveBtn(self, *arg):
        spaceNo = BigWorld.player().spaceNo
        if MII.data.has_key(spaceNo) or formula.spaceInClanWarPhase(spaceNo) or formula.spaceInWingBornIsland(spaceNo):
            gameglobal.rds.ui.map.openMap(True, uiConst.MAP_TYPE_TRANSPORT)

    def onClickSoulReliveBtn(self, *arg):
        p = BigWorld.player()
        flagState = p.flagStateCommon.get(gametypes.FLAG_STATE_ID_LIN_HUN_SHI)
        flagCnt = flagState.flagCnt if flagState else 0
        if flagCnt:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_DEADANDRELIVEPROXY_616, yesCallback=self.confirmReliveLingHunShi)

    def onGetSoulReliveCD(self, *arg):
        p = BigWorld.player()
        now = p.getServerTime()
        flagState = p.flagStateCommon.get(gametypes.FLAG_STATE_ID_LIN_HUN_SHI)
        coolDown = flagState.time if flagState else now
        ret = max(0, coolDown - now)
        return GfxValue(ret)

    def onGetClanWarFlag(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.inClanWar and p.clanWarStatus)

    def onIsClanWarCourier(self, *args):
        p = BigWorld.player()
        return GfxValue(p.inClanCourier() and p.jctSeq)

    def onGetClanWarCourierTip(self, *args):
        tips = GMD.data.get(GMDD.data.CLAN_WAR_COURIER_RELIVE_TIP, {}).get('text', 'GMDD.data.CLAN_WAR_COURIER_RELIVE_TIP')
        return GfxValue(gbk2unicode(tips))

    def canSelectRelivePos(self):
        p = BigWorld.player()
        spaceNo = formula.getMapId(p.spaceNo)
        return spaceNo in RPD.data.keys()

    def setReliveHereType(self):
        p = BigWorld.player()
        vipValidCountList = p.vipValidCnt
        for item in vipValidCountList:
            serviceId = item[0]
            mall = gameglobal.rds.ui.tianyuMall
            if not mall.vipServiceCheck(serviceId):
                self.isServer = False
                return
            self.isServer = True
            propID = VSD.data.get(serviceId, {}).get('propID')
            if propID == gametypes.VIP_SERVICE_FUBEN_RELIVE:
                self.vipValidCount = item[1]
                if self.vipValidCount != 0 and self.reliveHereType == 0 and p.inFuben():
                    self.reliveHereType = gametypes.RELIVE_HERE_TYPE_COUNT

        if self.mediator != None:
            self.mediator.Invoke('setVipValidCount', GfxValue(self.vipValidCount))

    def onIsGetLvLimitReliveFree(self, *args):
        p = BigWorld.player()
        if p.lv < SCD.data.get('lvLimitReliveFree', 30):
            return GfxValue(True)
        return GfxValue(False)

    def onGetLvLimitReliveFreeTipDesc(self, *args):
        desc = SCD.data.get('lvLimitReliveFreeTipDesc', gameStrings.TEXT_DEADANDRELIVEPROXY_220)
        return GfxValue(gbk2unicode(desc))

    def onIsBfhunt(self, *args):
        isBfHunt = formula.inHuntBattleField(BigWorld.player().mapID)
        return GfxValue(isBfHunt)

    def onIsTriggerWeakProtect(self, *args):
        p = BigWorld.player()
        stateId = DCD.data.get('BATTLE_FIELD_WEAK_PROTECT_PRE_BUFF_ID', 0)
        return GfxValue(p._isHasState(p, stateId) or self.isTriggerWeakProtect)

    def onGetReliveCountDownCnt(self, *args):
        return GfxValue(uiUtils.getReliveCountDownTime())

    def onIsBfDota(self, *args):
        p = BigWorld.player()
        return GfxValue(formula.inDotaBattleField(p.mapID))

    def setTriggerWeakProtect(self):
        if self.mediator:
            self.mediator.Invoke('setTriggerWeakProtect')

    def onAddWeakerProtect(self, *args):
        BigWorld.player().cell.addWeakerProtect()

    def onGetWeakProtectTip(self, *args):
        weakProtectTip = SCD.data.get('weakProtectTip', '')
        return GfxValue(gbk2unicode(weakProtectTip))

    def onIsInWingWorldWar(self, *args):
        return GfxValue(BigWorld.player().inWingWarCity())

    def onIsInPUBG(self, *args):
        return GfxValue(BigWorld.player().isInPUBG())

    def checkShowDeadRelivePanelInPUBG(self):
        p = BigWorld.player()
        gbId = p.getMaxHpTeamMateGbIdInPUBG()
        if not gbId:
            return False
        else:
            return True

    def onObTgtInPUBG(self, *args):
        p = BigWorld.player()
        entId = p.getMaxHpTeamMateEntIdInPUBG()
        gameglobal.rds.ui.deadAndRelive.hide()
        p.cell.pubgObserve(entId, p.getTeamMateGbIdByEntIdInPUBG(entId))

    def onLeaveInPUBG(self, *args):
        gameglobal.rds.ui.deadAndRelive.hide()
        BigWorld.player().leavePUBG(warningMsg=False)

    def onGetDataInPUBG(self, *args):
        info = dict()
        info['hintTxt'] = str(gbk2unicode(DCD.data.get('pubgDeadObHintTxt', '')))
        info['obHintTxt'] = str(gbk2unicode(gameStrings.PUBG_DEAD_AND_RELIVE_CENTER_HINT))
        info['obTgtInPUBGAllTime'] = DCD.data.get('pubgDeadToOBTime', 100)
        return uiUtils.dict2GfxDict(info)
