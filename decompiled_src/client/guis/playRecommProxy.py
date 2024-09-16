#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/playRecommProxy.o
from gamestrings import gameStrings
import BigWorld
import time
import clientcom
import gameglobal
import uiConst
import events
import gametypes
import utils
import types
import const
import logicInfo
from callbackHelper import Functor
from gameStrings import gameStrings
from messageBoxProxy import MBButton
from guis import ui
from helpers.eventDispatcher import Event
from uiTabProxy import UITabProxy
from guis import uiUtils
from guis import activityFactory
from guis import chickenFoodFactory
from helpers import importantPlayRecommend as IPR
from data import play_recomm_activity_data as PRAD
from data import play_recomm_item_data as PRID
from data import seeker_data as SED
from data import quest_data as QD
from data import play_recomm_config_data as PRCD
from data import mall_config_data as MCFD
from data import mall_item_data as MID
from data import quest_loop_data as QLD
from data import fb_data as FD
from data import consumable_item_data as CID
from data import avoid_doing_activity_data as ADAD
from cdata import evaluate_set_play_recomm_data_export as ESPRD
from cdata import quest_loop_inverted_data as QLID
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
PLAY_RECOMM_PATH = 'playRecomm/'
PLAY_RECOMM_ACTIVITY_ICON = PLAY_RECOMM_PATH + 'activityIcon/'

class PlayRecommProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(PlayRecommProxy, self).__init__(uiAdapter)
        self.widget = None
        self.prModel = {}
        self.prMediator = {}
        self.notifyHandler = None
        self.actFactory = activityFactory.getInstance()
        self.tLastOpen = 0
        self.reset()
        self.modelMap = self.getPrModel()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PLAY_RECOMM_V2, self.hide)

    def reset(self):
        super(PlayRecommProxy, self).reset()
        self.firstShowActId = 0
        self.locateType = gametypes.PLAY_RECOMM_DAILY_LOCATE_ABD
        self.isQuitGame = False
        self.showTabIndex = uiConst.PLAY_RECOMMV2_TAB_ACTIVITY_IDX
        self.subTabIdx = uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB
        self.isGotoTab = False
        if self.notifyHandler:
            BigWorld.cancelCallback(self.notifyHandler)
            self.notifyHandler = None

    def clearAll(self):
        self.tLastOpen = 0
        self.uiAdapter.playRecommActivation.playRecommendedFinishedActivities = []
        self.uiAdapter.playRecommActivation.hofFinishActivities = []
        self.uiAdapter.playRecommActivation.needGetBonusHistory = True
        self.uiAdapter.playRecommActivation.bonusHistory = {}
        self.uiAdapter.playRecommActivation.useFly = False
        self.uiAdapter.playRecommActivation.worldQuestRefreshFilterDict = {}
        self.hide()
        if self.uiAdapter.playRecommActivation.callbackTimer:
            BigWorld.cancelCallback(self.uiAdapter.playRecommActivation.callbackTimer)
            self.uiAdapter.playRecommActivation.callbackTimer = 0
        self.uiAdapter.playRecommActivation.hadCheckTimer = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PLAY_RECOMM_V2:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(PlayRecommProxy, self).clearWidget()
        self.uiAdapter.playRecommActivation.unRegisterPanel()
        self.uiAdapter.playRecommStronger.unRegisterPanel()
        self.uiAdapter.playRecommLvUp.unRegisterPanel()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PLAY_RECOMM_V2)

    @ui.callFilter(3, False)
    def checkDailyCompleteQuestFinish(self):
        p = BigWorld.player()
        quests = p.quests
        hasCheckQuest = False
        qdd = QD.data
        kingQId = 0
        for qid in quests:
            if qdd.get(qid, {}).has_key('kingRoad'):
                kingQId = qid
                hasCheckQuest = True

        if not hasCheckQuest:
            return
        cEvent = Event(events.EVENT_QUEST_INFO_CHANGE, {'mqList': [kingQId]})
        gameglobal.rds.ui.dispatchEvent(cEvent)
        inCompleteNum, allNum = IPR.incompleteItemsNum(p)
        if inCompleteNum <= 0:
            p.cell.onQuestKingRoadFinished()
            return
        if allNum - inCompleteNum >= 2:
            p.cell.onQuestKingRoadFinished()

    def show(self, acdId = 0, locateType = gametypes.PLAY_RECOMM_DAILY_LOCATE_ABD, tabIdx = None, subTabIdx = None):
        p = BigWorld.player()
        if p.lv < PRCD.data.get('playRecommShowLv', 20):
            p.showGameMsg(GMDD.data.PLAYRECOMM_SHOW_LV_ERROR, ())
            return
        else:
            self.locateType = locateType
            self.firstShowActId = acdId
            self.checkDailyCompleteQuestFinish()
            if tabIdx == uiConst.PLAY_RECOMMV2_TAB_ACTIVITY_IDX and not self.isGotoTab:
                if subTabIdx != None:
                    self.uiAdapter.playRecommActivation.isGotoTab = True
                    self.uiAdapter.playRecommActivation.activationTabIdx = subTabIdx
            self.isGotoTab = False
            if not self.widget:
                self.uiAdapter.loadWidget(uiConst.WIDGET_PLAY_RECOMM_V2)
                gameglobal.rds.uiLog.addOpenLog(uiConst.WIDGET_PLAY_RECOMM_V2)
                if tabIdx != None:
                    self.showTabIndex = tabIdx
            elif tabIdx != None:
                if self.currentTabIndex != tabIdx:
                    self.widget.setTabIndex(tabIdx)
                else:
                    currentProxy = self.getCurrentProxy()
                    currentProxy and currentProxy.refreshInfo()
            elif self.showTabIndex >= 0:
                if self.currentTabIndex != self.showTabIndex:
                    self.widget.setTabIndex(self.showTabIndex)
                    self.showTabIndex = -1
                else:
                    currentProxy = self.getCurrentProxy()
                    currentProxy and currentProxy.refreshInfo()
            return

    def showInPage(self, page, index = 0, selectedId = 0, locateType = gametypes.PLAY_RECOMM_DAILY_LOCATE_ABD):
        self.setInitPage(page, index)
        self.show(selectedId, locateType)

    def setInitPage(self, page, index = 0):
        self.isGotoTab = True
        if page == 0:
            self.showTabIndex = uiConst.PLAY_RECOMMV2_TAB_MORE_IDX
        elif page == 3:
            self.showTabIndex = uiConst.PLAY_RECOMMV2_TAB_STRONGER_IDX
        elif page == 4:
            self.showTabIndex = uiConst.PLAY_RECOMMV2_TAB_ACTIVITY_IDX
            self.uiAdapter.playRecommActivation.activationTabIdx = uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB
        elif page == 5:
            self.showTabIndex = uiConst.PLAY_RECOMMV2_TAB_ACTIVITY_IDX
            self.uiAdapter.playRecommActivation.activationTabIdx = uiConst.PLAY_RECOMMV2_TAB_WEEKLY_ACTIVITY_SUB_TAB
        elif page == 6:
            self.showTabIndex = uiConst.PLAY_RECOMMV2_TAB_ACTIVITY_IDX
            self.uiAdapter.playRecommActivation.activationTabIdx = uiConst.PLAY_RECOMMV2_TAB_OPERATION_ACTIVITY_SUB_TAB
            self.uiAdapter.playRecommActivation.isGotoTab = True

    def getPrModel(self):
        if not self.prModel:
            self.prModel = {'getMallInfo': self.onGetMallInfo,
             'clickQumoBtn': self.onClickQumoBtn,
             'clickDailyFuncBtn': self.onClickDailyFuncBtn,
             'takeAllVipReward': self.onTakeAllVipReward,
             'buyVipBasicPackage': self.onBuyVipBasicPackage,
             'buyVipAddedPackage': self.onBuyVipAddedPackage,
             'openShenyubaodian': self.onOpenShenyubaodian,
             'timeTickTimeOut': self.onTimeTickTimeOut,
             'groupMatchClick': self.onGroupMatchClick,
             'clickActionBtn': self.onClickActionBtn,
             'itemGo': self.onItemGo,
             'itemGoGuild': self.onItemGoGuild,
             'openEvaluate': self.onOpenEvaluate,
             'clickSeekItem': self.onClickSeekItem,
             'clickOpenStore': self.onClickOpenStore,
             'getEquipTabInfo': self.uiAdapter.playRecommStronger.onGetEquipTabInfo,
             'getEquipPartInfo': self.uiAdapter.playRecommStronger.onGetEquipPartInfo,
             'searchItemInSprite': self.uiAdapter.playRecommStronger.onSearchItemInSprite,
             'getSkillTabInfo': self.uiAdapter.playRecommStronger.onGetSkillTabInfo,
             'getRuneInfo': self.uiAdapter.playRecommStronger.onGetRuneInfo,
             'openRuneHelp': self.uiAdapter.playRecommStronger.onOpenRuneHelp,
             'openAvoidDoing': self.onOpenAvoidDoing}
        return self.prModel

    def getPrMediator(self):
        if not self.prMediator:
            self.prMediator = {'playRecommModel': self.getPrModel()}
        return self.prMediator

    def getLocateType(self):
        return self.locateType

    def onGetMallInfo(self, *args):
        ret = {}
        prid = args[3][0].GetNumber()
        mType = args[3][1].GetNumber()
        if mType == 0:
            mid = MCFD.data.get('vipBasicPackage', 0)
        else:
            mid = PRID.data.get(prid, {}).get('funcParam', (0,))[0]
        ret['mallId'] = mid
        ret['packageID'] = MID.data.get(mid, {}).get('packageID', 0)
        ret['itemId'] = MID.data.get(mid, {}).get('itemId', 0)
        return uiUtils.dict2GfxDict(ret, True)

    def onClickQumoBtn(self, *args):
        seekId = args[3][0].GetString()
        self.findPos(seekId)

    def findPos(self, seekId):
        p = BigWorld.player()
        if self.uiAdapter.playRecommActivation.useFly:
            canUse = logicInfo.isUseableGuildMemberSkill(const.GUILD_SKILL_XIAOFEIXIE)
            if canUse or p.canResetCD(const.GUILD_SKILL_XIAOFEIXIE):
                seekId = uiUtils.findTrackId(seekId)
                uiUtils.gotoTrack(seekId)
                gameglobal.rds.uiLog.addFlyLog(seekId)
                return
        uiUtils.findPosWithAlert(seekId)

    def onClickDailyFuncBtn(self, *args):
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        p = BigWorld.player()
        prid = args[3][1].GetNumber()
        index = args[3][0].GetNumber()
        targetMc = args[3][2]
        qumoQuestId = args[3][3].GetNumber()
        rdata = PRID.data.get(prid, {})
        btnType = rdata.get('keyType' + str(index))
        param = rdata.get('keyParam' + str(index))
        funcParam = rdata.get('funcParam')
        if btnType == uiConst.DAILY_BTN_FUNC_1:
            labelId = rdata.get('keyParam2', (0,))[0]
            gameglobal.rds.ui.team.onQuickCreateClick()
            gameglobal.rds.ui.memberDetailsV2.setDefaultTeamGoal({'labelId': labelId})
        elif btnType == uiConst.DAILY_BTN_FUNC_2:
            self.findPos(str(param))
        elif btnType == uiConst.DAILY_BTN_FUNC_3:
            questLoopId = funcParam[0]
            info = p.questLoopInfo.get(questLoopId)
            if info and info.questInfo and info.questInfo[-1][1] != True:
                questId = info.getCurrentQuest()
                seekId = QD.data.get(questId, {}).get('playRecommSeekId')
            elif info and info.questInfo and info.questInfo[-1][1] == True:
                index = info.getNextLoopIndex()
                questId = QLD.data.get(questLoopId, {}).get('quests', [0])[index - 1]
                seekId = QD.data.get(questId, {}).get('playRecommAccId', 0)
            else:
                seekId = param[0]
            if seekId:
                self.findPos(str(seekId))
        elif btnType == uiConst.DAILY_BTN_FUNC_4:
            refActivityId = param[0]
            self.actionActivity(refActivityId)
        elif btnType == uiConst.DAILY_BTN_FUNC_5:
            gameglobal.rds.ui.zhanJu.show()
        elif btnType == uiConst.DAILY_BTN_FUNC_7:
            targetMc.Invoke('showActivityTips')
        elif btnType == uiConst.DAILY_BTN_FUNC_8:
            if qumoQuestId:
                groupInfo = QD.data.get(qumoQuestId, {}).get('quickGroup')
                if groupInfo:
                    p.onQEApplyGroupMatch(groupInfo[0], groupInfo[1], groupInfo[2], groupInfo[3])
        elif btnType == uiConst.DAILY_BTN_FUNC_9:
            self.searchInSprite(param[0])
        elif btnType == uiConst.DAILY_BTN_FUNC_10:
            self.actionActivity(10234)
        elif btnType == uiConst.DAILY_BTN_FUNC_11:
            name = FD.data.get(param[0], {}).get('name', '')
            primaryLevelName = FD.data.get(param[0], {}).get('primaryLevelName', '')
            if primaryLevelName:
                name = ''.join((name, gameStrings.COMMON_DIAN, primaryLevelName))
            modeName = FD.data.get(param[0], {}).get('modeName', '')
            if modeName:
                name = ''.join((name,
                 '(',
                 modeName,
                 ')'))
            msg = gameStrings.PLAYRECOMM_ENTER_FUBEN_CONFIRM % name
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.applyForFuben, param[0]), gameStrings.COMMON_CONFIRM)
        elif btnType == uiConst.DAILY_BTN_FUNC_12:
            chickenFoodFactory.getInstance().showRank(True)
        elif btnType == uiConst.DAILY_BTN_FUNC_13:
            panelId = param[0]
            if panelId == uiConst.WIDGET_PVP_PANEL:
                gameglobal.rds.ui.pvPPanel.show(2)
            elif panelId == uiConst.WIDGET_ARENA_PLAYOFFS_BET:
                gameglobal.rds.ui.arenaPlayoffsBet.show(uiConst.ARENA_PLAYOFFS_BET_TAB_TOP4)
            elif panelId == uiConst.WIDGET_VOID_DREAMLAND:
                gameglobal.rds.ui.voidDreamland.show()
            elif panelId == uiConst.WIDGET_CELEBRITY_RANK:
                gameglobal.rds.ui.celebrityRank.show()
            elif panelId == uiConst.WIDGET_GUILD_SIGN_IN:
                gameglobal.rds.ui.guildSignInV2.show()
            elif panelId == uiConst.WIDGET_GUILD_SIGN_IN_V2:
                gameglobal.rds.ui.guildSignInV2.show()
            elif panelId == uiConst.WIDGET_WINGWORLD_REMOVESEAL:
                gameglobal.rds.ui.wingWorldRemoveSeal.show()
            elif panelId == uiConst.WIDGET_ACTIVITY_SALE:
                tabId = param[1] if len(param) > 1 else 0
                gameglobal.rds.ui.activitySale.show(tabId)
            elif panelId == uiConst.WIDGET_YUNCHUI_QUIZZES:
                BigWorld.player().base.queryQuizzesInfo()
            elif panelId == uiConst.WIDGET_YUNCHUI_QUIZZES_APPLY:
                BigWorld.player().base.queryQuizzesJoinedInfo()
            elif panelId == uiConst.WIDGET_COMBINE_TIANYU_MALL_BUY:
                mallId, buyNum = param[1] if len(param) > 1 else (0, 0)
                buyType = 'playRecomm.0'
                if mallId and buyNum:
                    gameglobal.rds.ui.tianyuMall.mallBuyConfirm(mallId, buyNum, buyType)
            elif panelId == uiConst.WIDGET_WING_WORLD_BG:
                tabIndex = param[1] if len(param) > 1 else (0, 0)
                gameglobal.rds.ui.wingWorld.show(tabIndex)
            elif panelId == uiConst.WIDGET_ACTIVITY_SHOP:
                if self.uiAdapter.activityShop.canOpen():
                    BigWorld.player().getCurrPrivateShop()
                else:
                    BigWorld.player().showGameMsg(GMDD.data.ACTIVITY_SHOP_CLOSED, ())
            elif panelId == uiConst.WIDGET_BATTLE_OF_FORT_SIGN_UP:
                battleId = param[1] if len(param) > 1 else 0
                gameglobal.rds.ui.battleOfFortSignUp.show(battleId)
            elif panelId == uiConst.WIDGET_PVP_BG_V2:
                gameglobal.rds.ui.pvPPanel.show(1)
            elif panelId == uiConst.WIDGET_ZMJ_ACTIVITY_BG:
                gameglobal.rds.ui.zmjActivityBg.show()
            elif panelId == uiConst.WIDGET_VOID_LUNHUI:
                gameglobal.rds.ui.voidLunHui.show()
            elif panelId == uiConst.WIDGET_SPRITE_CHALLENGE:
                gameglobal.rds.ui.spriteChallenge.show()
            elif panelId == uiConst.WIDGET_MISS_TIANYU_GROUP_TOP_RANK:
                rankType = param[1] if len(param) > 1 else gametypes.TOP_TYPE_MISS_TIANYU_GROUP
                gameglobal.rds.ui.missTianyuGroupTopRank.show(rankType)
            elif panelId == uiConst.WIDGET_ASSASSINATION_MAIN:
                gameglobal.rds.ui.assassinationMain.show()
            elif panelId == uiConst.WIDGET_RANDOM_TREASURE_BAG_MAIN:
                bagId = param[1]
                gameglobal.rds.ui.randomTreasureBagMain.show(bagId=bagId, enableScrollToCurBag=True)
            elif panelId == uiConst.WIDGET_MAP_GAME_MAP:
                gameglobal.rds.ui.mapGameMap.show()
            elif panelId == uiConst.WIDGET_MAP_GAME_MAP_V2:
                gameglobal.rds.ui.mapGameMapV2.show()
            elif panelId == uiConst.WIDGET_LUNZHAN_YUNDIAN:
                gameglobal.rds.ui.lunZhanYunDian.show()
            elif panelId == uiConst.WIDGET_HUNT_GHOST:
                gameglobal.rds.ui.huntGhost.show()
        elif btnType == uiConst.DAILY_BTN_FUNC_14:
            gameglobal.rds.ui.questTrack.showFindBeastTrack(True)
            gameglobal.rds.ui.questTrack.doCurrFindBeastSeek()
        elif btnType == uiConst.DAILY_BTN_FUNC_15:
            gameglobal.rds.ui.findBeastRecover.show()
        elif btnType == uiConst.DAILY_BTN_FUNC_16:
            p = BigWorld.player()
            itemId = param[0]
            cdata = CID.data.get(itemId, {})
            stateId = cdata.get('stateIds', ())[0]
            if p.hasState(stateId):
                state = p.getStates().get(stateId)
                stateStartTime = state[0][gametypes.STATE_INDEX_STARTTIME]
                duration = state[0][gametypes.STATE_INDEX_LASTTIME]
                if stateStartTime + duration > time.time():
                    p.showGameMsg(GMDD.data.TRAVEL_BUFF_NOT_READY, ())
                    return
            itemFameData = {}
            currentCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
            needCount = param[1]
            count = uiUtils.convertNumStr(currentCount, needCount)
            itemData = uiUtils.getGfxItemById(itemId, count)
            deltaCount = needCount - currentCount
            itemFameData['itemId'] = itemId
            itemFameData['deltaNum'] = deltaCount
            msg = uiUtils.getTextFromGMD(GMDD.data.DOUBLE_TRAVLE_ITEM_USE, gameStrings.DOUBLE_TRAVLE_ITEM_USE)
            func = Functor(p.cell.useCommonDikouItem, itemId, needCount)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, func, itemData=itemData, itemFameData=itemFameData)
        elif btnType == uiConst.DAILY_BTN_FUNC_17:
            self.uiAdapter.baiDiShiLian.show()
        elif btnType == uiConst.DAILY_BTN_FUNC_18:
            if gameglobal.rds.ui.wingWorldRemoveSeal.isWingWorldDiGongExist():
                enterBaseMLNo = getattr(BigWorld.player(), 'wwBossMlgNo', 0)
                enterBaseMLNo and gameglobal.rds.ui.diGong.show(enterBaseMlNo=enterBaseMLNo)
            else:
                p.showGameMsg(GMDD.data.WINGWORLD_DIGONG_DESTROYED, ())
        elif btnType == uiConst.DAILY_BTN_FUNC_19:
            p.cell.applySkyWingFuben()
        elif btnType == uiConst.DAILY_BTN_FUNC_20:
            self.uiAdapter.rankCommon.showRankCommon(param[0])
        elif btnType == uiConst.DAILY_BTN_FUNC_21:
            self.uiAdapter.doLinkClick(rdata.get('linkText', ''), uiConst.LEFT_BUTTON)
        elif btnType == uiConst.DAILY_BTN_FUNC_22:
            url, width, height = param
            gameglobal.rds.ui.innerIE.show(url, uiConst.IE_NOLIMIT_TRANSFER, width, height, skinType=uiConst.IE_SKIN_TYPE_FIT_SIZE)
        elif btnType == uiConst.DAILY_BTN_FUNC_23:
            gameglobal.rds.ui.ftbExcavate.checkActivityInfo()

    def onTakeAllVipReward(self, *arg):
        gameglobal.rds.ui.tianyuMall.onTakeAllVipReward()

    def onBuyVipBasicPackage(self, *arg):
        gameglobal.rds.ui.tianyuMall.onOpenVipBasicPackageConfirm()

    def onBuyVipAddedPackage(self, *arg):
        prid = int(arg[3][0].GetNumber())
        mallId = PRID.data.get(prid, {}).get('funcParam', (0,))[0]
        gameglobal.rds.ui.tianyuMall.pendingBuyVipAddedPackage(mallId)

    def onOpenShenyubaodian(self, *arg):
        mainBookId = int(arg[3][0].GetNumber())
        subBookId = int(arg[3][1].GetNumber())
        pageIdx = int(arg[3][2].GetNumber())
        gameglobal.rds.ui.baoDian.show([mainBookId, subBookId, pageIdx])

    def onTimeTickTimeOut(self, *arg):
        self.uiAdapter.playRecommActivation.refreshRecomm(uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB)

    def actionActivity(self, activityID):
        actIns = self.actFactory.actIns.get(activityID, None)
        if actIns:
            actIns.onActionBtnClick()

    def searchInSprite(self, keyWord):
        gameglobal.rds.ui.help.hide()
        gameglobal.rds.ui.help.show(keyWord)

    def _getTabList(self):
        return [{'tabIdx': uiConst.PLAY_RECOMMV2_TAB_ACTIVITY_IDX,
          'tabName': 'tabBtn0',
          'view': 'PlayRecommV2ActivityWidget',
          'proxy': 'playRecommActivation'},
         {'tabIdx': uiConst.PLAY_RECOMMV2_TAB_MORE_IDX,
          'tabName': 'tabBtn1',
          'view': 'PlayRecommV2LvUpWidget',
          'proxy': 'playRecommLvUp'},
         {'tabIdx': uiConst.PLAY_RECOMMV2_TAB_STRONGER_IDX,
          'tabName': 'tabBtn2',
          'view': 'PlayRecommV2StrongerWidget',
          'proxy': 'playRecommStronger'},
         {'tabIdx': uiConst.PLAY_RECOMMV2_TAB_EXP_IDX,
          'tabName': 'tabBtn3',
          'view': 'PlayRecommExpPursueWidget',
          'proxy': 'playRecommExpPursue'}]

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        self.widget.setTabIndex(self.showTabIndex)
        self.initTabVisible()

    def initTabVisible(self):
        self.setTabVisible(uiConst.PLAY_RECOMMV2_TAB_EXP_IDX, gameglobal.rds.configData.get('enableExpPursueGuide', False), False)
        self.relayoutTab()

    def refreshInfo(self):
        if not self.widget:
            return
        currentProxy = self.getCurrentProxy()
        if currentProxy:
            currentProxy.refreshInfo()

    def exitGame(self):
        logoffDelay = SCD.data.get('logoffDelay', 10)
        p = BigWorld.player()
        p.cell.logOff()
        p.base.setOfflineType(gametypes.PLAYER_OFFLINE_TYPE_NORMAL)
        buttons = [MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494, lambda : self._doRealQuit(tryToTakeFigurePhoto=True)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, self._unlogOff)]
        gameglobal.rds.ui.messageBox.show(True, gameStrings.TEXT_PLAYRECOMMPROXY_495, gameStrings.TEXT_PLAYRECOMMPROXY_495_1, buttons, repeat=logoffDelay, countDownFunctor=lambda : self._doRealQuit(tryToTakeFigurePhoto=False))
        gameglobal.isModalDlgShow = True

    def _doRealQuit(self, tryToTakeFigurePhoto = False):
        if tryToTakeFigurePhoto and BigWorld.player().takeCharSnapshotBeforeQuit(op=gametypes.CHAR_SNAPSHOT_EXIT_GAME):
            return
        clientcom.openForceUrl()
        BigWorld.quit()

    def _unlogOff(self):
        uiUtils.unlogoff()

    def getFirstShowActId(self):
        firstShowActId = self.firstShowActId
        self.firstShowActId = 0
        return firstShowActId

    def getPlayTipData(self, playRecommId, seekId, prid, funcType = 0):
        aData = PRAD.data.get(playRecommId, {})
        displayType = aData.get('displayType', ())
        ret = self.genLvUpItemInfo(aData, displayType, playRecommId, True)
        ret['debugArg'] = str((playRecommId,
         seekId,
         prid,
         funcType))
        rdata = PRID.data.get(prid, {})
        ret['activation'] = self.uiAdapter.playRecommActivation.getActivationInfo(prid, rdata, gametypes.ACTIVATION_TYPE_ITEM)
        ret['expendQuestInfo'] = self.getQuestTipInfo(prid, rdata)
        ret['evaluateInfo'] = self.getEvaluateInfo(prid)
        ret['avoidDoingInfo'] = self.getAvoidDoingInfo(rdata)
        if seekId:
            if funcType == gametypes.RECOMMEND_TYPE_QUMO:
                pass
            else:
                try:
                    seekId = eval(seekId)
                    if type(seekId) == types.TupleType:
                        for item in seekId:
                            entryInfo = {}
                            entryInfo['entryName'] = SED.data.get(item, {}).get('name', '')
                            entryInfo['entryTrackId'] = item
                            entryInfo['enableFly'] = True
                            ret['entryList'].append(entryInfo)

                except:
                    pass

        return ret

    def getAvoidDoingInfo(self, rdata):
        activityKeys = rdata.get('avtivityKey', ())
        if gameglobal.rds.configData.get('enableAvoidDoingActivity', False):
            for activityKey in activityKeys:
                adad = ADAD.data.get(activityKey, ())
                openTime = adad.get('openTime', None)
                closeTime = adad.get('closeTime', None)
                tWhen = utils.getNow()
                if openTime and closeTime and utils.getDisposableCronTabTimeStamp(openTime) <= tWhen <= utils.getDisposableCronTabTimeStamp(closeTime):
                    return activityKey

        return 0

    def getEvaluateInfo(self, prid):
        p = BigWorld.player()
        evaluateInfo = {}
        evaId = ESPRD.data.get(prid, {}).get('ID', None)
        if evaId:
            evaluateInfo['canEvaluate'] = p.getCanEvaluatePlay(evaId)
            evaluateInfo['evaId'] = evaId
            evaluateInfo['evaBtnText'] = gameStrings.PLAYRECOMM_EVALUATE_BTN_TXT
        return evaluateInfo

    def getQuestTipInfo(self, prid, rdata):
        if not rdata.get('isRelateQuest', 0):
            return
        else:
            p = BigWorld.player()
            detailInfo = None
            questDetail = None
            if rdata.get('funcType', 0) == 3:
                for taskId in p.questData:
                    qData = QD.data.get(taskId, {})
                    activityType = qData.get('activityType', 0)
                    if activityType == rdata.get('funcParam', 0)[0]:
                        displayType = qData.get('displayType', 0)
                        if displayType in gametypes.QUEST_LOOP_DISPLAY_TYPES or displayType == gametypes.QUEST_DISPLAY_TYPE_CLUE:
                            if taskId not in BigWorld.player().questLoopInfo.keys():
                                taskId = QLID.data.get(taskId, {}).get('questLoop', taskId)
                            detailInfo = BigWorld.player().fetchQuestLoopDetail(taskId, fetchType=const.TYPE_FETCH_QUEST_DETAIL_ACTIVITYTIP)
                        else:
                            detailInfo = BigWorld.player().fetchQuestDetail(taskId, fetchType=const.TYPE_FETCH_QUEST_DETAIL_ACTIVITYTIP)
                        if detailInfo:
                            if displayType in (gametypes.QUEST_DISPLAY_TYPE_CLUE, gametypes.QUEST_DISPLAY_TYPE_FENG_WU):
                                questDetail = gameglobal.rds.ui.questLog.gfxClueQuestDetail(detailInfo, displayType)
                            else:
                                questDetail = gameglobal.rds.ui.questLog.gfxQuestDetail(detailInfo)

            return questDetail

    def genLvUpItemInfo(self, aData, dType, prId, ignoreLv = False):
        ret = {}
        ret['debugArg'] = str((dType,
         prId,
         ignoreLv,
         aData.get('serverConfigId', 0)))
        if utils.getEnableCheckServerConfig():
            serverConfigId = aData.get('serverConfigId', 0)
            if serverConfigId and not utils.checkInCorrectServer(serverConfigId):
                return ret
        previewLv = PRCD.data.get('playRecommPreviewLv', 5)
        if gameglobal.rds.loginManager.serverMode() == gametypes.SERVER_MODE_NOVICE:
            if aData.get('hideInNovice', 0):
                return ret
        lv = BigWorld.player().lv
        minLv = aData.get('minLv', 0)
        maxLv = aData.get('maxLv', 0)
        previewMinLv = 0
        if aData.get('isFilterPreview', 0):
            previewMinLv = minLv
        else:
            previewMinLv = minLv - previewLv
        atype = aData.get('type', 0)
        if atype == 0 and minLv and lv < previewMinLv and not ignoreLv:
            return ret
        elif atype == 0 and maxLv and lv > maxLv and not ignoreLv:
            return ret
        else:
            startTimes = aData.get('startTimes', ())
            endTimes = aData.get('endTimes', ())
            if startTimes and endTimes:
                ret['closeFlag'] = not utils.inDateRange(startTimes[0], endTimes[0])
            else:
                ret['closeFlag'] = False
            ret.update(aData)
            ret['prId'] = prId
            ret['iconPath'] = (PLAY_RECOMM_ACTIVITY_ICON + '%s' + uiConst.ICON_SUFFIX) % str(aData.get('icon', 0))
            ret['preview'] = lv < minLv
            ret['needLv'] = minLv
            starOrder = 0
            starNums = aData.get('starNum', {}).get(dType, {})
            lv = BigWorld.player().lv
            if starNums:
                for lvRange, star in starNums.iteritems():
                    if type(lvRange) != tuple:
                        continue
                    if len(lvRange) != 2:
                        continue
                    if lv >= lvRange[0] and lv <= lvRange[1]:
                        starOrder = star
                        break

            ret['starOrder'] = starOrder
            ret['actionName'] = self.getTipsFuncBtnName(aData, 0)
            ret['actionName2'] = self.getTipsFuncBtnName(aData, 1)
            ret['enableAction'] = self.getTipsFuncBtnStat(aData, 0)
            ret['enableAction2'] = self.getTipsFuncBtnStat(aData, 1)
            refActivityId = aData.get('refActivityId', 0)
            ret['enableGroup'] = refActivityId and uiUtils.checkIsCanGroupMatch(aData.get('isEnableGroupMatch', 0))
            joinTime = aData.get('joinActTime', ())
            if type(joinTime) == tuple and len(joinTime) == 2:
                ret['joinTime'] = self.getTimeDesc(joinTime[0], joinTime[1])
            else:
                ret['joinTime'] = ''
            startTimes = aData.get('startTimes', ())
            endTimes = aData.get('endTimes', ())
            if startTimes and endTimes:
                ret['activityTime'] = self.getTimeDesc(startTimes[0], endTimes[0])
            else:
                ret['activityTime'] = ''
            ret['memberNum'] = aData.get('num', '')
            ret['entryList'] = self.getActivityEntryList(aData)
            ret['storeInfoList'] = self.getActivityStoreInfoList(aData)
            ret['storeInfoName'] = gameStrings.OPEN_STORE
            ret['rewardInfo'] = self.getRewardInfo(aData)
            actIns = self.actFactory.actIns.get(refActivityId, None)
            ret['showProgress'] = bool(aData.get('periodCnt', 0) and actIns)
            if ret['showProgress']:
                ret['completeCnt'] = self.getCntInfo(aData, actIns)
            ret['activation'] = self.uiAdapter.playRecommActivation.getActivationInfo(prId, aData, gametypes.ACTIVATION_TYPE_ACTIVITY)
            ret['isShowFubenProgress'] = aData.get('isShowFubenProgress', 0)
            return ret

    def getRewardInfo(self, aData):
        bonusIcon = []
        bonusTypeDef = {1: 'exp',
         2: 'bindCash',
         3: 'cash',
         4: 'banggong',
         5: 'fame',
         6: 'active',
         7: 'guildContribution'}
        for item in aData.get('aAwdDetail', ()):
            bonusType, bonusNum, bonusDesc = item
            if bonusType not in bonusTypeDef:
                continue
            rInfo = {}
            rInfo['type'] = bonusTypeDef.get(bonusType)
            rInfo['desc'] = bonusDesc
            bonusIcon.append(rInfo)

        bonusItem = []
        for itemId, itemCount in aData.get('mainAward', ()):
            bonusItem.append(uiUtils.getGfxItemById(itemId, itemCount, appendInfo={'isMain': True}))

        for itemId, itemCount in aData.get('aAwdItem', ()):
            bonusItem.append(uiUtils.getGfxItemById(itemId, itemCount, appendInfo={'isMain': False}))

        ret = {}
        ret['bonusIcon'] = bonusIcon
        ret['bonusItem'] = bonusItem
        return ret

    def getTipsFuncBtnName(self, aData, idx):
        tipsFuncBtn = aData.get('tipsFuncBtn', ())
        btnName = ''
        if len(tipsFuncBtn) <= idx:
            return btnName
        else:
            btnType = tipsFuncBtn[idx][0]
            if btnType == uiConst.TIPS_FUNC_BTN_TYPE_USE_REF_ACTIVITY_ID:
                refActivityId = aData.get('refActivityId', 0)
                actIns = self.actFactory.actIns.get(refActivityId, None)
                if actIns:
                    btnName = actIns.getBtnActionName()
            if btnName == '':
                btnName = tipsFuncBtn[idx][1]
            if btnType == uiConst.TIPS_FUNC_BTN_TYPE_YMF_GUILD_RANK:
                if not gameglobal.rds.configData.get('enableGuildYMF', False):
                    btnName = ''
            if btnType == uiConst.TIPS_FUNC_BTN_TYPE_WINGWORLD_WAR_RANK:
                p = BigWorld.player()
                state = p.wingWorld.state
                if state == gametypes.WING_WORLD_STATE_DECLARE_END or state == gametypes.WING_WORLD_STATE_OPEN or state == gametypes.WING_WORLD_STATE_SETTLEMENT:
                    btnName = ''
            return btnName

    def getTipsFuncBtnStat(self, aData, idx):
        scheduleStart = aData.get('scheduleStart', ())
        scheduleEnd = aData.get('scheduleEnd', ())
        if len(scheduleStart) <= idx or len(scheduleEnd) <= idx:
            return True
        startTime = scheduleStart[idx]
        endTime = scheduleEnd[idx]
        if utils.inCrontabsRange(startTime, endTime):
            return True
        return False

    def getCntInfo(self, aData, actIns):
        if not aData or not actIns:
            return 0
        erefType = aData.get('erefType', 1)
        erefIds = aData.get('erefId', ())
        if not erefIds:
            return 0
        cnt = 0
        if erefType == uiConst.ACT_FUBEN:
            for irefId in erefIds:
                cnt = max(actIns.getCurEnterTimes(irefId), cnt)

        else:
            cnt = actIns.getCnt()
        return cnt

    def getTimeDesc(self, startCron, endCron):
        start = utils.parseCrontabPattern(startCron)
        end = utils.parseCrontabPattern(endCron)
        weekDesc = ''
        weekList = start[utils.WEEKEND]
        for w in weekList:
            weekDesc += self.getWeekdayName(w)

        if weekDesc:
            weekDesc = gameStrings.TEXT_GAMETYPES_10547 + weekDesc
        timeDesc = ''
        timeDesc += '%02d:%02d' % (start[utils.HOUR][0], start[utils.MINUTE][0])
        timeDesc += '-%02d:%02d' % (end[utils.HOUR][0], end[utils.MINUTE][0])
        return weekDesc + timeDesc

    def getActivityEntryList(self, aData):
        ret = []
        aPlace = aData.get('aPlace', ())
        trackId = aData.get('aPlaceTk', ())
        enableFly = aData.get('isEnablePlaceFly', ())
        if not type(aPlace) == type(trackId) == type(trackId) == tuple:
            return ret
        if not len(aPlace) == len(trackId) == len(enableFly):
            return ret
        for i in xrange(len(aPlace)):
            entryInfo = {}
            entryInfo['entryName'] = aPlace[i]
            entryInfo['entryTrackId'] = trackId[i]
            entryInfo['enableFly'] = enableFly[i]
            ret.append(entryInfo)

        return ret

    def getActivityStoreInfoList(self, aData):
        ret = []
        storeIDList = aData.get('storeID', ())
        storeDescribeList = aData.get('storeDescribe', ())
        if not type(storeIDList) == type(storeDescribeList) == tuple:
            return ret
        if not len(storeIDList) == len(storeDescribeList):
            return ret
        for i in xrange(len(storeIDList)):
            storeInfo = dict()
            storeInfo['storeInfoId'] = storeIDList[i]
            storeInfo['storeInfoName'] = storeDescribeList[i]
            ret.append(storeInfo)

        return ret

    def getWeekdayName(self, cronIdx):
        weekList = [gameStrings.TEXT_PLAYRECOMMPROXY_848,
         gameStrings.TEXT_PLAYRECOMMPROXY_848_1,
         gameStrings.TEXT_PLAYRECOMMPROXY_848_2,
         gameStrings.TEXT_PLAYRECOMMPROXY_848_3,
         gameStrings.TEXT_PLAYRECOMMPROXY_848_4,
         gameStrings.TEXT_PLAYRECOMMPROXY_848_5,
         gameStrings.TEXT_PLAYRECOMMPROXY_848_6]
        if cronIdx >= 0 and cronIdx <= 6:
            return weekList[cronIdx]
        return gameStrings.TEXT_PLAYRECOMMPROXY_848

    def onGroupMatchClick(self, *arg):
        type = int(arg[3][0].GetNumber())
        detailId = int(arg[3][1].GetNumber())
        if type == 1:
            actIns = self.actFactory.actIns.get(detailId, None)
            actIns.onGroupMatchClick()
        elif type == 2:
            gameglobal.rds.ui.fubenLogin.selectedFb = detailId
            gameglobal.rds.ui.fubenLogin.showFbGroupMatch()
            return

    def onClickActionBtn(self, *arg):
        playRecommId = int(arg[3][0].GetNumber())
        idx = int(arg[3][1].GetNumber())
        aData = PRAD.data.get(playRecommId, {})
        tipsFuncBtn = aData.get('tipsFuncBtn', ())
        if len(tipsFuncBtn) <= idx:
            return
        else:
            btnType = tipsFuncBtn[idx][0]
            if btnType == uiConst.TIPS_FUNC_BTN_TYPE_USE_REF_ACTIVITY_ID:
                refActivityId = aData.get('refActivityId', 0)
                self.actionActivity(refActivityId)
            elif btnType == uiConst.TIPS_FUNC_BTN_TYPE_FISHING_GAME_RANK:
                if gameglobal.rds.ui.fishingGame.rankMediator:
                    gameglobal.rds.ui.fishingGame.showType = 0
                    gameglobal.rds.ui.fishingGame.onGetRankInfo(None)
                else:
                    gameglobal.rds.ui.fishingGame.showRank(0)
            elif btnType == uiConst.TIPS_FUNC_BTN_TYPE_SXY_GUILD_RANK:
                gameglobal.rds.ui.suiXingYu.showGuildRankOrResult(const.ML_GROUP_NO_SXY)
            elif btnType == uiConst.TIPS_FUNC_BTN_TYPE_WND_KILL_RANK:
                gameglobal.rds.ui.wmdRankList.openKillRank()
            elif btnType == uiConst.TIPS_FUNC_BTN_TYPE_YMF_GUILD_RANK:
                self.uiAdapter.yumufengGuildRank.show()
                self.uiAdapter.yumufengGuildRank.getNewRankInfo()
            elif btnType == uiConst.TIPS_FUNC_BTN_TYPE_WINGWORLD_BOSSDAMAGE_RANK:
                gameglobal.rds.ui.bossDamageRank.show()
            elif btnType == uiConst.TIPS_FUNC_BTN_TYPE_WINGWORLD_DONATE_RANK:
                gameglobal.rds.ui.removeSealRank.show()
            elif btnType == uiConst.TIPS_FUNC_BTN_TYPE_SKY_WING:
                gameglobal.rds.ui.baiDiShiLian.show()
            elif btnType == uiConst.TIPS_FUNC_BTN_TYPE_WINGWORLD_WAR_RANK:
                gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_WING_WAR_GUILD_CONTRIBUTE)
            return

    def onItemGo(self, *arg):
        seekId = int(arg[3][0].GetNumber())
        uiUtils.gotoTrack(seekId)
        gameglobal.rds.uiLog.addFlyLog(seekId)

    def onItemGoGuild(self, *args):
        seekId = int(args[3][0].GetNumber())
        gameglobal.rds.ui.skill.useGuildSkill(uiConst.GUILD_SKILL_DZG, (str(seekId),))

    def onOpenEvaluate(self, *arg):
        evaId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.evaluatePlay.show(evaId, uiConst.EVALUATE_SHOWTYPE_PALY)

    def onClickSeekItem(self, *arg):
        buttonIdx = int(arg[3][0].GetNumber())
        seekId = int(arg[3][1].GetNumber())
        if buttonIdx == uiConst.LEFT_BUTTON:
            uiUtils.findPosById(str(seekId))
        elif buttonIdx == uiConst.RIGHT_BUTTON:
            gameglobal.rds.ui.littleMap.showTrackTarget(seekId)
        gameglobal.rds.uiLog.addPathLog(seekId)

    def onClickOpenStore(self, *args):
        uiUtils.closeCompositeShop()
        p = BigWorld.player()
        storeInfoId = int(args[3][0].GetNumber())
        storeInfoId and p.base.openPrivateShop(0, storeInfoId)

    def onOpenAvoidDoing(self, *arg):
        if hasattr(BigWorld.player(), 'avoidDoingActivity'):
            activityKey = int(arg[3][0].GetNumber())
            self.uiAdapter.avoidDoingActivity.show(activityKey)

    def getNotifyInterval(self):
        internalMin = PRCD.data.get('importantPushInterval', {})
        internalMin.setdefault(0, 360)
        internalKeys = internalMin.keys()
        internalKeys.sort()
        keysLen = len(internalKeys)
        internal = 0
        percent = IPR.inCompleteItemsNotifyCheck(BigWorld.player())
        for i in xrange(keysLen):
            idx = keysLen - i - 1
            keyPercent = internalKeys[idx]
            if percent >= keyPercent:
                internal = internalMin[keyPercent] * const.TIME_INTERVAL_MINUTE
                break

        return max(internal, 10 * const.TIME_INTERVAL_MINUTE)

    def autoNotifyIncompleteItems(self):
        if gameglobal.rds.configData.get('enableIncompleteItemsNotify', True):
            pct = IPR.inCompleteItemsNotifyCheck(BigWorld.player())
            if pct >= max(PRCD.data.get('importantPushMinPct', 100), 1):
                gameglobal.rds.ui.playRecommPushIcon.notifyIncompleteItems()
            else:
                gameglobal.rds.ui.playRecommPushIcon.cancelNotify()
        if self.notifyHandler:
            BigWorld.cancelCallback(self.notifyHandler)
        self.notifyHandler = BigWorld.callback(self.getNotifyInterval(), self.autoNotifyIncompleteItems)

    def initIncompleteNotifyHandler(self, needAutoShow):
        gameglobal.rds.ui.playRecommPushIcon.show()
        if not self.notifyHandler:
            self.autoNotifyIncompleteItems()
        if needAutoShow and self.autoShowPlayRecomm():
            self.show()

    def setTabIdx(self, tab):
        if not self.widget:
            self.showInPage(tab, 0)
        else:
            self.widget.setTabIndex(tab)

    def autoShowPlayRecomm(self):
        p = BigWorld.player()
        if not p:
            return False
        minLv = PRCD.data.get('importantRecommMinLv', 20)
        maxLv = PRCD.data.get('importantPushCheckBoxShowLv', 40)
        return p.lv >= minLv and p.lv < maxLv

    @ui.uiEvent(uiConst.WIDGET_PLAY_RECOMM_V2, events.EVENT_VIP_INFO_UPDATE)
    def onUpdateVipInfo(self, event = None):
        self.checkDailyCompleteQuestFinish()
        self.uiAdapter.playRecommActivation.refreshDailyRecommItems()

    @ui.uiEvent(uiConst.WIDGET_PLAY_RECOMM_V2, events.EVENT_IPRD_UPDATE)
    def onUpdateIrpData(self):
        self.uiAdapter.playRecommActivation.refreshDailyRecommItems()
