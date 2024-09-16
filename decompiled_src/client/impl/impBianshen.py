#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impBianshen.o
import BigWorld
import gameglobal
import skillDataInfo
import gamelog
import gametypes
import utils
from gameclass import SkillInfo
from helpers import navigator
from callbackHelper import Functor
from guis import ui
from guis import uiConst
from sfx import keyboardEffect
from data import carrousel_data as CD
from data import zaiju_data as ZJD
from data import school_switch_general_data as SSGD
from data import school_switch_ws_data as SSWD
from cdata import game_msg_def_data as GMDD
from data import yabiao_config_data as YCD

class ImpBianshen(object):

    def needForbidJump(self, bMsg = True):
        if self._isOnZaijuOrBianyao():
            zjd = ZJD.data.get(self._getZaijuNo(), {})
            r = zjd.get('lockJump', False)
            r and bMsg and self.showGameMsg(GMDD.data.ZAIJU_FORBID_JUMP, (zjd['name'],))
            return r
        return False

    def needForbidForwardOp(self, bMsg = True):
        if self._isOnZaijuOrBianyao():
            zjd = ZJD.data.get(self._getZaijuNo(), {})
            r = zjd.get('lockForwardWalk', False)
            r and bMsg and self.showGameMsg(GMDD.data.ZAIJU_FORBID_FORWARDOP, (zjd['name'],))
            return r
        return False

    def needForbidBackOp(self, bMsg = True):
        if self._isOnZaijuOrBianyao():
            zjd = ZJD.data.get(self._getZaijuNo(), {})
            r = zjd.get('lockBackWalk', False)
            r and bMsg and self.showGameMsg(GMDD.data.ZAIJU_FORBID_BACKOP, (zjd['name'],))
            return r
        return False

    def exceedYaoliLimit(self):
        if not self.inMLYaoLiSpace():
            return False
        if self.yaoliPoint >= self.getYaoliMPoint():
            return False
        return False

    def needForbidSideOp(self, bMsg = True):
        if self._isOnZaijuOrBianyao():
            zjd = ZJD.data.get(self._getZaijuNo(), {})
            r = zjd.get('lockSideWalk', False)
            r and bMsg and self.showGameMsg(GMDD.data.ZAIJU_FORBID_SIDEOP, (zjd['name'],))
            return r
        return False

    def showZaijuUI(self, skills = [], zaijuType = uiConst.ZAIJU_TYPE_SKILL, showType = uiConst.ZAIJU_SHOW_TYPE_ZAIJU):
        if gameglobal.rds.configData.get('enableZaijuV2', False):
            gameglobal.rds.ui.zaijuV2.show(skills, zaijuType, showType)
        elif showType == uiConst.ZAIJU_SHOW_TYPE_ZAIJU:
            gameglobal.rds.ui.zaiju.show(skills, zaijuType)
        elif showType == uiConst.ZAIJU_SHOW_TYPE_CARROUSEL:
            gameglobal.rds.ui.zaiju.showCarrousel()
        elif showType == uiConst.ZAIJU_SHOW_TYPE_EXIT:
            gameglobal.rds.ui.zaiju.showExitBtn()
        keyboardEffect.updateZaijuState(True)

    def hideZaijuUI(self, showType = uiConst.ZAIJU_SHOW_TYPE_ZAIJU):
        if showType == uiConst.ZAIJU_SHOW_TYPE_EXIT:
            if gameglobal.rds.ui.zaiju.exitMediator:
                gameglobal.rds.ui.zaiju.closeExitBtn()
        elif showType == uiConst.ZAIJU_SHOW_TYPE_CARROUSEL:
            gameglobal.rds.ui.zaiju.hide()
        elif showType == uiConst.ZAIJU_SHOW_TYPE_ZAIJU:
            gameglobal.rds.ui.zaiju.hide()
        gameglobal.rds.ui.zaijuV2.hide()
        keyboardEffect.updateZaijuState(False)

    def skillSwitch(self, wsNo):
        if not self._isSchoolSwitch():
            return
        switchNo = self._getSchoolSwitchNo()
        if not SSWD.data.has_key((wsNo, switchNo)):
            return
        if not SSGD.data.has_key(switchNo):
            return
        self.skills.clear()
        validSkills = [ x for x, needShow in SSGD.data[switchNo].get('skillShows') if needShow ]
        skills = SSGD.data[switchNo].get('skills', [])
        for skillId, skillLv in skills:
            if skillId in validSkills:
                self.skills[skillId] = skillDataInfo.SkillInfoVal(skillId, skillLv)

        self.wsSkills.clear()
        sswd = SSWD.data[wsNo, switchNo]
        wsSkills = sswd.get('wushuangSkills', [])
        for skillId, skillLv in wsSkills:
            self.wsSkills[skillId] = skillDataInfo.SkillInfoVal(skillId, skillLv)
            skillInfo = SkillInfo(skillId, skillLv)
            if skillInfo.hasSkillData('wsNeed1'):
                self.wsSkills[skillId].wsType = 1
                self.wsSkills[skillId].isWsSkill = True
            elif skillInfo.hasSkillData('wsNeed2'):
                self.wsSkills[skillId].wsType = 2
                self.wsSkills[skillId].isWsSkill = True
            self.wsSkills[skillId].enable = True
            self.wsSkills[skillId].slots = []
            self.wsSkills[skillId].proficiency = {}

        gameglobal.rds.ui.actionbar.refreshActionbar()

    def zaijuPathFind(self, routes):
        if len(routes) > 0:
            if navigator.getNav().canEnterRideFly():
                self.ap.seekPoints(routes, self.zaijuPathCallback)
            else:
                BigWorld.callback(1, Functor(self.ap.seekPoints, routes, self.zaijuPathCallback))
            self.inForceNavigate = True
            if self == BigWorld.player():
                if self.getOperationMode() == gameglobal.ACTION_MODE:
                    self.ap.restore()
            self.physics.fall = False
            self.zaijuRouteInfo = routes
        else:
            self.inForceNavigate = False
            self.physics.fall = True

    def zaijuPathCallback(self, success):
        if success:
            self.onZaijuPathFindOver()
        else:
            self.onZaijuPathFindFail()

    def onZaijuPathFindOver(self):
        self.inForceNavigate = False
        if self == BigWorld.player():
            self.ap.forwardMagnitude = 0
            self.ap.reset()
            if gameglobal.rds.ui.zaiju.mediator:
                gameglobal.rds.ui.zaiju.leaveZaiju()
            else:
                gameglobal.rds.ui.zaijuV2.leaveZaiju()
        self.physics.fall = True
        self.zaijuRouteInfo = None

    def onZaijuPathFindFail(self):
        if self.zaijuRouteInfo:
            self.zaijuPathFind(self.zaijuRouteInfo)

    def limitQinggongByBianshen(self, qType):
        if self._isInBianyao() or self._isOnZaiju():
            data = ZJD.data.get(self.bianshen[1], {})
            if data.get('limitQinggong', 0):
                allowQinggongs = data.get('allowQinggongs', ())
                if qType in allowQinggongs:
                    return False
                else:
                    return True
        return False

    def createUsedZaiju(self, eid, bianshen):
        ent = BigWorld.entities.get(eid)
        if not ent or not ent.inWorld:
            return
        BigWorld.player().createUsedZaijuData[eid] = bianshen

    def inCarrousel(self):
        if not self.carrousel[0]:
            return False
        elif BigWorld.entities.get(self.carrousel[0]):
            return True
        else:
            return False
        return False

    def _checkCanLeaveCarrousel(self):
        carrouselEId = self.carrousel[0]
        carrousel = BigWorld.entities.get(carrouselEId)
        data = CD.data.get(carrousel.carrouselId, {})
        if data.get('leaveForbid', 0) > 0:
            return False
        return True

    def leaveCarrousel(self):
        if not self.inCarrousel():
            return
        if not self._checkCanLeaveCarrousel():
            self.showGameMsg(GMDD.data.FORBID_LEAVE_CARROUSEL, ())
            return
        self.cell.leaveCarrousel()

    @ui.callFilter(0.5, False)
    def fetchBusinessNpcInfo(self, npcEntId):
        npc = BigWorld.entities.get(npcEntId)
        if npc is not None and npc._isBusinessNpc():
            npc.cell.fetchBusinessNpcInfo(npc.priceVer)

    def onFetchBusinessNpcInfo(self, npcEntId, priceVer, salePriceClass, saleReserveInfo, npcSellPriceInfo, npcBuyPriceInfo, lastRefreshTime):
        gamelog.info('@szh onFetchBusinessNpcInfo', npcEntId, priceVer, salePriceClass, saleReserveInfo, npcSellPriceInfo, npcBuyPriceInfo, lastRefreshTime)
        npc = BigWorld.entities.get(npcEntId)
        if npc is not None and npc._isBusinessNpc():
            npc.priceVer = priceVer
        gameglobal.rds.ui.guildBusinessShop.setShopInfo(npcEntId, salePriceClass, saleReserveInfo, npcSellPriceInfo, npcBuyPriceInfo, lastRefreshTime)
        gameglobal.rds.ui.guildBusinessShop.refreshShopInfo()
        gameglobal.rds.ui.guildBusinessShop.refreshPackageInfo()
        gameglobal.rds.ui.guildBusinessShop.refreshMarketInfo()

    def sellBusinessItemToNpc(self, npcEntId, saleIds, positions, isBlack):
        if not self._isOnZaiju():
            self.showGameMsg(GMDD.data.BUSINESS_FAIL_BY_ZAIJU, ())
            return
        elif not utils.isInBusinessZaiju(self):
            self.showGameMsg(GMDD.data.BUSINESS_FAIL_BY_ZAIJU, ())
            return
        else:
            npc = BigWorld.entities.get(npcEntId)
            if npc is None or not npc._isBusinessNpc():
                return
            if isBlack:
                npc.cell.buyBlackBusinessItemFromPlayer(saleIds, positions)
            else:
                npc.cell.buyBusinessItemFromPlayer(npc.priceVer, saleIds, positions)
            return

    def onSellBusinessItemToNpc(self, result):
        if result == gametypes.BUSINESS_SELL_SUC:
            pass
        elif result == gametypes.BUSINESS_SELL_FAIL_BY_VER:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_SELL_FAIL_BY_VER, ())
            gameglobal.rds.ui.guildBusinessShop.onRefresh(None)
        elif result == gametypes.BUSINESS_SELL_FAIL_BY_ZAIJU:
            self.showGameMsg(GMDD.data.BUSINESS_FAIL_BY_ZAIJU, ())
        elif result == gametypes.BUSINESS_SELL_FAIL_BY_QUEST:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_FAIL_NO_QUEST, ())
        elif result == gametypes.BUSINESS_SELL_FAIL_BY_ITEM_NOT_ENOUGH:
            self.showGameMsg(GMDD.data.BUSINESS_SELL_ITEM_NOT_ENOUGH, ())
        elif result == gametypes.BUSINESS_SELL_FAIL_BY_GUILD_JOB:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_MAN_NOT, ('',))
        elif result == gametypes.BUSINESS_SELL_FAIL_BY_ILLEGAL:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_SELL_FAIL_BY_ILLEGAL, ())
        elif result == gametypes.BUSINESS_SELL_FAIL_BY_MONEY_MAX:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_SELL_FAIL_BY_MONEY_MAX, ())

    def buyBusinessItemFromNpc(self, npcEntId, saleIds):
        if not self._isOnZaiju():
            self.showGameMsg(GMDD.data.BUSINESS_FAIL_BY_ZAIJU, ())
            return
        elif not utils.isInBusinessZaiju(self):
            self.showGameMsg(GMDD.data.BUSINESS_FAIL_BY_ZAIJU, ())
            return
        else:
            npc = BigWorld.entities.get(npcEntId)
            if npc is None or not npc._isBusinessNpc():
                return
            npc.cell.sellBusinessItemToPlayer(npc.priceVer, saleIds)
            return

    def onBuyBusinessItemFromNpc(self, result):
        if result == gametypes.BUSINESS_BUY_SUC:
            pass
        elif result == gametypes.BUSINESS_BUY_FAIL_BY_VER:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_BUY_FAIL_BY_VER, ())
            gameglobal.rds.ui.guildBusinessShop.onRefresh(None)
        elif result == gametypes.BUSINESS_BUY_FAIL_BY_ZAIJU:
            self.showGameMsg(GMDD.data.BUSINESS_FAIL_BY_ZAIJU, ())
        elif result == gametypes.BUSINESS_BUY_FAIL_BY_QUEST:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_FAIL_NO_QUEST, ())
        elif result == gametypes.BUSINESS_BUY_FAIL_BY_SLOT_NOT_ENOUGH:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_SLOT_NOT_ENOUGH, ())
        elif result == gametypes.BUSINESS_BUY_FAIL_BY_SALEID:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_BUY_FAIL_BY_SALEID, ())
        elif result == gametypes.BUSINESS_BUY_FAIL_BY_FAME:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_BUY_FAME_NOT_ENOUGH, ())
        elif result == gametypes.BUSINESS_BUY_FAIL_BY_GUILD_JOB:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_MAN_NOT, ('',))
        elif result == gametypes.BUSINESS_BUY_FAIL_BY_QUEST_COM:
            self.showGameMsg(GMDD.data.GUILD_BUSINESS_BUY_FAIL_BY_QUEST_COM, ())

    def onFetchSpyBusinessInfo(self, spyNpcNo, saleId, saleInfoType, businessNpcNo):
        gamelog.info('@szh onFetchSpyBusinessInfo', self.id, spyNpcNo, saleId, saleInfoType, businessNpcNo)
        gameglobal.rds.ui.funcNpc.refreshBusinessSpy(spyNpcNo, saleId, saleInfoType, businessNpcNo)

    def addYabiaoPot(self):
        if hasattr(self, 'yabiaoTrapId') and self.yabiaoTrapId:
            self.rmYabiaoPot()
        self.yabiaoTrapId = BigWorld.addPot(self.matrix, YCD.data['yabiaoWarningScope'], self.leaveYabiaoCallback)

    def rmYabiaoPot(self):
        if hasattr(self, 'yabiaoTrapId') and self.yabiaoTrapId:
            BigWorld.delPot(self.yabiaoTrapId)
            self.yabiaoTrapId = None

    def leaveYabiaoCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if enteredTrap:
            return
        player = BigWorld.player()
        if player.groupNUID == self.groupNUID and player.ybStatus:
            player.cell.leaveYabiao(self.groupNUID, self.position)

    def isInDotaZaiju(self):
        if self.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            data = ZJD.data.get(self.bianshen[1], {})
            if data.get('isDotaZaiju', 0):
                return True
        return False
