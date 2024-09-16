#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenLoginProxy.o
from gamestrings import gameStrings
import math
import BigWorld
from Scaleform import GfxValue
import formula
import gameglobal
import uiConst
import const
import gamelog
import gametypes
import uiUtils
import utils
import clientUtils
import commNewServerActivity
from uiProxy import SlotDataProxy
from ui import gbk2unicode
from callbackHelper import Functor
from data import fb_data as FD
from data import item_data as ID
from cdata import font_config_data as FCD
from cdata import fb_unlock_data as FUD
from cdata import fb_unlock_group_data as FUGD
from data import state_data as SD
from data import quest_data as QD
from data import achievement_data as AD
from data import fame_data as FAD
from cdata import group_match_tree_data as GMTD
from cdata import game_msg_def_data as GMDD
from data import server_progress_data as SPD
from data import transport_data as TD
from data import sys_config_data as SCD
from data import map_config_data as MCD
from data import top_fb_data as TFD
CLIENT_FORBID_MSG = [gameStrings.TEXT_FUBENLOGINPROXY_39]
SLOT_NUM = 6
SHISHENMODE = 8
CFG_CAN_HELP = 1
NO_SHISHENMODE_SELECTED = 1
GUIDE_TIP = ['FB_GUIDE_CHECK_SUCC',
 'FB_GUIDE_LV_CHECK',
 'FB_GUIDE_TIMES_CHECK',
 'FB_GUIDE_MAC_CHECK',
 'FB_GUIDE_MEMBER_CHECK']
WARNNING_COLOR = 16005124
PRE_FLAG = ''

class FubenLoginProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(FubenLoginProxy, self).__init__(uiAdapter)
        self.bindType = 'fbLogin'
        self.type = 'fbLogin'
        self.descMediator = None
        self.buttonMediator = None
        self.selectedFb = 0
        self.isShow = False
        self.isGuidMode = False
        self.isCrazyMode = False
        self.args = ('normal', 'normal', 'hard', 'hard', 'jingsu', 'tafang', 'simple', 'difficult')
        self.fbTitles = (gameStrings.TEXT_FUBENLOGINPROXY_65,
         gameStrings.TEXT_FUBENLOGINPROXY_65_1,
         gameStrings.TEXT_FUBENLOGINPROXY_65_2,
         gameStrings.TEXT_FUBENLOGINPROXY_65_3,
         gameStrings.TEXT_FUBENLOGINPROXY_65_4,
         gameStrings.TEXT_FUBENLOGINPROXY_65_5,
         gameStrings.TEXT_FUBENLOGINPROXY_65_6,
         gameStrings.TEXT_FUBENLOGINPROXY_65_7)
        self.fbStyle = ('null', 'juqing', 'yincang', 'tuandui', 'jingsu', 'tafang')
        self.fbInfo = {}
        self.groupMatchMediator = None
        self.resetGroupMatchData()
        self.transportEntId = 0
        self.fbAvaiable = True
        self.errorMsg = {}
        self.dropItems = None
        self.crazyShishenModeInfo = {}
        self.crazyTogetherFightingState = 0
        self.modelMap = {'getBgPath': self.onGetBgPath,
         'getMap': self.onGetMap,
         'getDesc': self.onGetDesc,
         'getBtnInfo': self.onGetBtnInfo,
         'modeChoice': self.onModeChoice,
         'rankListClick': self.onRankListClick,
         'enterClick': self.onEnterClick,
         'leaveClick': self.onLeaveClick,
         'resetClick': self.onResetClick,
         'groupMatchClick': self.onGroupMatchClick,
         'getFbTip': self.onGetFbTip,
         'groupMatchInfo': self.onGroupMatchInfo,
         'selectFirstLevel': self.onSelectFirstLevel,
         'selectSecondLevel': self.onSelectSecondLevel,
         'groupOkClick': self.onGroupOkClick,
         'groupCancelClick': self.onGroupCancelClick,
         'crazyShishenSelect': self.onCrazyShishenSelect,
         'showSealInfo': self.onShowSealInfo}
        uiAdapter.registerEscFunc(uiConst.WIDGET_ENTER_FUBEN_BTN, self.dismiss)
        uiAdapter.registerEscFunc(uiConst.WIDGET_ENTER_FUBEN_DESC, self.dismiss)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ENTER_FUBEN_CONTAINER:
            self.isShow = True
        elif widgetId == uiConst.WIDGET_ENTER_FUBEN_DESC:
            self.descMediator = mediator
        elif widgetId == uiConst.WIDGET_ENTER_FUBEN_BTN:
            self.buttonMediator = mediator
        elif widgetId == uiConst.WIDGET_ENTER_FUBEN_GROUP_MATCH:
            self.groupMatchMediator = mediator

    def lockMode(self, currentFb):
        if not self.isShow:
            return

    def resetGroupMatchData(self):
        self.curFirstLevelIndex = 0
        self.firstLevelListVal = []
        self.firstLevelListDesc = []
        self.curSecondLevelIndex = 0
        self.secondLevelListVal = []
        self.secondLevelListDesc = []

    def isShowExpAdd(self, fbData):
        p = BigWorld.player()
        self.queryTogetherFightingState()
        if p.baseVp + p.savedVp and fbData.get('vpExp', 0):
            return 1
        return 0

    def queryTogetherFightingState(self):
        p = BigWorld.player()
        data = FD.data.get(self.selectedFb, {})
        mbBonusLimit = data.get('mbBonusLimit', 0)
        self.crazyTogetherFightingState = 0
        if mbBonusLimit:
            p.cell.queryGroupMutualBenefitAvatars(self.selectedFb)
        elif self.descMediator:
            self.descMediator.Invoke('refreshTogetherFightingState', (GfxValue(0), GfxValue(gbk2unicode(''))))

    def getTogetherFightingState(self, mbPlayerCnt):
        ret = 0
        p = BigWorld.player()
        data = FD.data.get(self.selectedFb, {})
        tipsDes = data.get('togetherFightingTips', gameStrings.TEXT_FUBENLOGINPROXY_151)
        mbBonusLimit = data.get('mbBonusLimit', 0)
        if mbBonusLimit:
            if mbPlayerCnt >= mbBonusLimit:
                ret = 1
            else:
                ret = 2
            if self.selectedFb in self.crazyShishenModeInfo and self.getCrazyShishenModeMaxCnt(self.selectedFb) != 0 and self.getCrazyShishenModeMaxCnt(self.selectedFb) <= self.getCrazyShishenModeCnt(self.selectedFb) and (p.isInTeamOrGroup() and p.isTeamLeader() or not p.isInTeamOrGroup()):
                self.crazyTogetherFightingState = ret
            if self.descMediator:
                self.descMediator.Invoke('refreshTogetherFightingState', (GfxValue(ret), GfxValue(gbk2unicode(tipsDes))))
        else:
            self.crazyTogetherFightingState = ret

    def onModeChoice(self, *arg):
        index = int(arg[3][0].GetNumber())
        fbNo = self.fbInfo['fbList'][index]
        if fbNo != self.selectedFb:
            self.selectedFb = fbNo
            if self.descMediator:
                obj = self.onGetDesc()
                self.descMediator.Invoke('refreshDesc', obj)
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ENTER_FUBEN_DESC)
            self.refreshFubenBtn()
        self.isCrazyMode = False
        self.isGuidMode = False
        if self.buttonMediator:
            self.buttonMediator.Invoke('resetGuideMode', GfxValue(False))
            self.buttonMediator.Invoke('resetCrazyMode', GfxValue(False))
        gameglobal.rds.sound.playSound(gameglobal.SD_494)

    def onRankListClick(self, *arg):
        if gameglobal.rds.ui.ranking.mediator:
            gameglobal.rds.ui.ranking.hide()
        else:
            gameglobal.rds.ui.ranking.show(const.PROXY_KEY_TOP_FB_TIME, uiConst.RANK_TYPE_OTHER, self.selectedFb)

    def onCrazyShishenSelect(self, *arg):
        ret = 0
        tipsDes = ''
        if self.crazyTogetherFightingState:
            iscrazy = arg[3][0].GetBool()
            data = FD.data.get(self.selectedFb, {})
            tipsDes = data.get('togetherFightingTips', '')
            if iscrazy:
                ret = 2
            else:
                ret = self.crazyTogetherFightingState
        if self.descMediator:
            self.descMediator.Invoke('refreshTogetherFightingState', (GfxValue(ret), GfxValue(gbk2unicode(tipsDes))))

    def onEnterFbWorld(self, *arg):
        if not self.fbInfo.has_key('fbList'):
            return
        if self.selectedFb in self.fbInfo['fbList']:
            p = BigWorld.player()
            self.isCrazyMode = arg[3][1].GetBool()
            if self.isCrazyMode:
                self.showCrazyModeItems()
            elif p.isArenaMatching():
                p.confirmCancelApplyArena(formula.getFbDetailName(self.selectedFb), Functor(p.cell.fbModeSelected, self.transportEntId, self.selectedFb, 0, 0, 0))
            else:
                enableShishenCascade = gameglobal.rds.configData.get('enableShishenCascade', False)
                fd = FD.data.get(self.selectedFb, {})
                noShishenModeSelect = fd.get('noShishenModeSelect', 0)
                cfgFbMode = fd.get('fbMode', 0)
                if enableShishenCascade and cfgFbMode == uiConst.SHISHEN_FB_MODE:
                    enableHelpMode = gameglobal.rds.configData.get('enableFubenHelpMode', False)
                    helpMode = self.fbInfo.get('fbHelpInfo', {}).get(self.selectedFb, 0)
                    currentMode = self.fbInfo.get('currShishenMode', {}).get(self.selectedFb, 0)
                    if not self.isOpenedFb() and self.hasRightOpenFb():
                        if not noShishenModeSelect:
                            self.showShishenModeSelectPage(enableHelpMode and helpMode, False, currentMode)
                        else:
                            p.cell.fbModeSelected(self.transportEntId, self.selectedFb, 0, 0, 0)
                    elif helpMode:
                        fbHelp = fd.get('fbHelp', 0)
                        if noShishenModeSelect == NO_SHISHENMODE_SELECTED and fbHelp == CFG_CAN_HELP:
                            gameglobal.rds.ui.fubenDegree.open(self.selectedFb, 3, fbHelp)
                        else:
                            self.showShishenModeSelectPage(enableHelpMode and helpMode, True, currentMode)
                    else:
                        p.cell.fbModeSelected(self.transportEntId, self.selectedFb, 0, 0, 0)
                else:
                    enableTeleportSpell = gameglobal.rds.configData.get('enableTeleportSpell', False)
                    if enableTeleportSpell:
                        BigWorld.player().unlockKey(gameglobal.KEY_POS_FUBEN_LOGIN)
                        p.enterTeleportSpell(gameglobal.TELEPORT_SPELL_ENTER_FUBEN, Functor(self.cellFbModeSelected, self.transportEntId, self.selectedFb, 0, 0, 0))
                        self.hide(True)
                    else:
                        p.cell.fbModeSelected(self.transportEntId, self.selectedFb, 0, 0, 0)

    def cellFbModeSelected(self, transportEntId, selectedFb, guideMode, itemId, shishenMode):
        BigWorld.player().cell.fbModeSelected(transportEntId, selectedFb, guideMode, itemId, shishenMode)

    def onEnterClick(self, *arg):
        self.isGuidMode = arg[3][0].GetBool()
        fd = FD.data.get(self.selectedFb, {})
        fbMode = fd.get('fbMode', {})
        if SHISHENMODE == fbMode or self.isGuidMode:
            self.onEnterFbWorld(*arg)
        else:
            self.enterConfirm(*arg)

    def enterConfirm(self, *arg):
        requireCom = FD.data.get(self.selectedFb, {}).get('isNeedConfirm', False)
        if requireCom and not self.isOpenedFb() and self.hasRightOpenFb():
            fbNo = self.selectedFb
            fbName = formula.getFbDetailName(fbNo)
            msg = SCD.data.get('fubenEnterConfirm', gameStrings.TEXT_FUBENLOGINPROXY_289) % fbName
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onEnterFbWorld, *arg))
        else:
            self.onEnterFbWorld(*arg)

    def isOpenedFb(self):
        return self.fbInfo.get('existInfo', {}).get(self.selectedFb, False)

    def hasRightOpenFb(self):
        p = BigWorld.player()
        return p.isInTeamOrGroup() and p.isTeamLeader() or not p.isInTeamOrGroup()

    def showShishenModeSelectPage(self, enableHelpMode, isOpenAsPop, currentMode):
        gameglobal.rds.ui.fubenDegree.show(True, enableHelpMode, isOpenAsPop, currentMode)

    def onLeaveClick(self, *arg):
        BigWorld.player().unlockKey(gameglobal.KEY_POS_FUBEN_LOGIN)
        self.hide(True)

    def onResetClick(self, *arg):
        if self.selectedFb:
            BigWorld.player().cell.existFubenDestroyCheck(self.selectedFb)

    def onGroupMatchClick(self, *arg):
        gamelog.debug('@hjx groupMatch#onGroupMatchClick:', self.selectedFb)
        self.showFbGroupMatch()

    def showFbGroupMatch(self):
        if not uiUtils.groupMatchApplyCheck():
            return
        if not self.checkCanGroupMatchLevel():
            BigWorld.player().showGameMsg(GMDD.data.FUBEN_TEAM_LV_FAIL, ())
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ENTER_FUBEN_GROUP_MATCH)

    def closeFbGroupMatch(self):
        self.groupMatchMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ENTER_FUBEN_GROUP_MATCH)

    def _getFirstLevelDesc(self, fbNo):
        return FD.data.get(fbNo, {}).get('primaryLevelName', '')

    def _getSecondLevelDesc(self, fbNo):
        return FD.data.get(fbNo, {}).get('modeName', '')

    def _updateGroupMatchLevel(self):
        treeData = GMTD.data.get(utils.getFbGroupNo(self.selectedFb), {})
        for fKey, fVal in treeData.items():
            isValid = False
            sValTmp = []
            sDescTmp = []
            fbNo = 0
            for sKey, sVal in fVal.items():
                if uiUtils.checkFbGroupMatchCondition(sVal['fbNo']):
                    fbNo = sVal['fbNo']
                    isValid = True
                    sValTmp.append(sKey)
                    sDescTmp.append(self._getSecondLevelDesc(fbNo))

            if isValid:
                self.firstLevelListVal.append(fKey)
                self.firstLevelListDesc.append(self._getFirstLevelDesc(fbNo))
                self.secondLevelListVal.append(sValTmp)
                self.secondLevelListDesc.append(sDescTmp)

        gamelog.debug('@hjx groupMatch#_updateGroupMatchLevel:', self.firstLevelListVal, self.secondLevelListVal)

    def checkCanGroupMatchLevel(self):
        treeData = GMTD.data.get(utils.getFbGroupNo(self.selectedFb), {})
        for fKey, fVal in treeData.items():
            for sKey, sVal in fVal.items():
                if uiUtils.checkFbGroupMatchCondition(sVal['fbNo']):
                    return True

        return False

    def _setCurLevelIndex(self):
        fbData = FD.data.get(self.selectedFb, {})
        primaryLevel = fbData.get('primaryLevel', 0)
        mode = fbData.get('mode', 0)
        if len(self.firstLevelListVal) == 1 or primaryLevel not in self.firstLevelListVal:
            self.curFirstLevelIndex = 0
            self.curSecondLevelIndex = 0
            return
        self.curFirstLevelIndex = self.firstLevelListVal.index(primaryLevel)
        if len(self.secondLevelListVal) == 0:
            self.curSecondLevelIndex = 0
        else:
            self.curSecondLevelIndex = self.secondLevelListVal[self.curFirstLevelIndex].index(mode)

    def _getFirstLevel(self):
        ret = self.movie.CreateArray()
        for index, val in enumerate(self.firstLevelListDesc):
            ret.SetElement(index, GfxValue(gbk2unicode(val)))

        return ret

    def _getSecondLevel(self):
        ret = self.movie.CreateArray()
        for index, val in enumerate(self.secondLevelListDesc[self.curFirstLevelIndex]):
            ret.SetElement(index, GfxValue(gbk2unicode(val)))

        return ret

    def _getFbName(self):
        fbName = ''
        fbData = FD.data
        fVal = self.firstLevelListVal[self.curFirstLevelIndex]
        sVal = self.secondLevelListVal[self.curFirstLevelIndex][self.curSecondLevelIndex]
        fbNo = GMTD.data.get(utils.getFbGroupNo(self.selectedFb), {}).get(fVal, {}).get(sVal, {}).get('fbNo', 0)
        fbName = formula.getFbDetailName(fbNo)
        return GfxValue(gbk2unicode(fbName))

    def onGroupMatchInfo(self, *arg):
        gamelog.debug('@hjx groupMatch#onGroupMatchInfo')
        self.resetGroupMatchData()
        self._updateGroupMatchLevel()
        self._setCurLevelIndex()
        ret = self.movie.CreateObject()
        fbName = formula.getFbDetailName(self.selectedFb)
        ret.SetMember('fbName', GfxValue(gbk2unicode(fbName)))
        ret.SetMember('curFirstIndex', GfxValue(self.curFirstLevelIndex))
        ret.SetMember('curSecondIndex', GfxValue(self.curSecondLevelIndex))
        ret.SetMember('firstLevel', self._getFirstLevel())
        ret.SetMember('secondLevel', self._getSecondLevel())
        return ret

    def onSelectFirstLevel(self, *arg):
        self.curFirstLevelIndex = int(arg[3][0].GetNumber())
        self.curSecondLevelIndex = 0
        gamelog.debug('@hjx groupMatch#onSelectFirstLevel:', self.curFirstLevelIndex)
        if self.groupMatchMediator:
            self.groupMatchMediator.Invoke('refreshSecondLevelDM', (self._getSecondLevel(),))
        if self.groupMatchMediator:
            self.groupMatchMediator.Invoke('refreshFbName', (self._getFbName(),))

    def onSelectSecondLevel(self, *arg):
        self.curSecondLevelIndex = int(arg[3][0].GetNumber())
        if self.groupMatchMediator:
            self.groupMatchMediator.Invoke('refreshFbName', (self._getFbName(),))

    def _getGroupMatchArg(self):
        groupMatchNo = utils.getFbGroupNo(self.selectedFb)
        firstLevelMode = self.firstLevelListVal[self.curFirstLevelIndex]
        secondLevelMode = self.secondLevelListVal[self.curFirstLevelIndex][self.curSecondLevelIndex]
        try:
            fbNo = GMTD.data[groupMatchNo][firstLevelMode][secondLevelMode]['fbNo']
        except:
            fbNo = GMTD.data[groupMatchNo].values()[0].values()[0].values()[0]

        if self.curSecondLevelIndex != 0:
            secondLevelMode = uiUtils.genGroupMatchSecondMode(secondLevelMode)
        gamelog.debug('@hjx groupMatch#_getGroupMatchArg:', groupMatchNo, firstLevelMode, secondLevelMode, fbNo)
        return (groupMatchNo,
         firstLevelMode,
         secondLevelMode,
         fbNo)

    def onGroupOkClick(self, *arg):
        p = BigWorld.player()
        self.closeFbGroupMatch()
        if self.selectedFb == 0:
            return
        groupMatchArg = self._getGroupMatchArg()
        gameglobal.rds.ui.team.openTeamWithType(groupMatchArg[3], type=const.GROUP_GOAL_FB)

    def onGroupCancelClick(self, *arg):
        self.closeFbGroupMatch()

    def dismiss(self):
        self.onLeaveClick()

    def reset(self):
        self.selectedFb = 0
        self.fbInfo = {}
        self.transportEntId = 0
        self.fbAvaiable = True
        self.errorMsg = {}
        self.dropItems = None
        self.descMediator = None
        self.buttonMediator = None

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ENTER_FUBEN_BG)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ENTER_FUBEN_CONTAINER)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ENTER_FUBEN_DESC)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ENTER_FUBEN_BTN)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ENTER_FUBEN_GROUP_MATCH)
        if gameglobal.rds.ui.ranking.mediator:
            gameglobal.rds.ui.ranking.hide()
        gameglobal.rds.ui.restoreUI()
        self.crazyShishenModeInfo.clear()
        self.isShow = False
        self.crazyTogetherFightingState = 0

    def show(self, transportEntId, fbInfo):
        if self.isShow:
            return
        if not gameglobal.rds.ui.enableUI:
            BigWorld.player().showUI(True)
        player = BigWorld.player()
        player.ap.stopMove(True)
        player.ap.forceAllKeysUp()
        player.lockKey(gameglobal.KEY_POS_FUBEN_LOGIN)
        self.fbInfo = fbInfo
        self.transportEntId = transportEntId
        self.selectedFb = 0
        currentFb = self.fbInfo.get('currentFb', 0)
        self.errorMsg = self.fbInfo.get('errorMsg', {})
        for fbNo in self.fbInfo['fbList']:
            if currentFb and fbNo != currentFb and fbNo not in self.errorMsg.keys() and FD.data[fbNo].get('type') == const.FB_TYPE_GROUP:
                self.errorMsg[fbNo] = CLIENT_FORBID_MSG

        if currentFb:
            self.selectedFb = currentFb
        else:
            deltaLv = 1000
            deltaMinLv = 1000
            if self.fbInfo['fbList']:
                self.selectedFb = self.fbInfo['fbList'][0]
            for fbNo in self.fbInfo['fbList']:
                data = FD.data.get(fbNo, {})
                recommendLv = data.get('recommendLv', 0)
                lvMin = data.get('lvMin', 0)
                lvMax = data.get('lvMax', 0)
                if player.lv >= lvMin and player.lv <= lvMax:
                    tmpMinLv = player.lv - lvMin
                    tmpLv = math.fabs(player.lv - recommendLv)
                    if tmpMinLv < deltaMinLv or tmpMinLv == deltaMinLv and tmpLv < deltaLv:
                        self.selectedFb = fbNo
                        deltaLv = tmpLv
                        deltaMinLv = tmpMinLv

        for fbNo in self.fbInfo['fbList']:
            self.crazyShishenModeInfo[fbNo] = [0, FD.data.get(fbNo, {}).get('crazyShishenModelThreshold', 0)]
            if self.getCrazyShishenModeMaxCnt(fbNo) != 0:
                BigWorld.player().cell.getHighShishenModeCnt(fbNo)

        if gameglobal.rds.ui.ranking.mediator:
            gameglobal.rds.ui.ranking.hide()
        gameglobal.rds.ui.hideAllUI()
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_CHAT_LOG, True)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ENTER_FUBEN_BG)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ENTER_FUBEN_CONTAINER)
        if self.selectedFb:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ENTER_FUBEN_DESC)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ENTER_FUBEN_BTN)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHAT_LOG)

    def update(self, fbInfo):
        if not self.isShow:
            return
        fbNo = fbInfo.get('currentFb', 0)
        self.lockMode(fbNo)

    def onGetBgPath(self, *arg):
        obj = {}
        background = self.fbInfo.get('fbBackground', 'fbLingxu')
        transport = BigWorld.entities.get(self.transportEntId)
        transportId = 0
        if transport:
            transportId = transport.charType
        dynamicBg = TD.data.get(transportId, {}).get('dynamicBg', 0)
        if dynamicBg:
            obj['bg'] = 'loading/%s.swf' % background
        else:
            obj['bg'] = 'loading/%s.dds' % background
        return uiUtils.dict2GfxDict(obj, True)

    def onGetBtnInfo(self, *arg):
        p = BigWorld.player()
        ret = self.movie.CreateObject()
        fd = FD.data.get(self.selectedFb, {})
        isEnableGroupMatch = fd.get('isEnableGroupMatch', 0)
        matchCrazyShishen = False
        if self.selectedFb in self.crazyShishenModeInfo and self.getCrazyShishenModeMaxCnt(self.selectedFb) != 0 and self.getCrazyShishenModeMaxCnt(self.selectedFb) <= self.getCrazyShishenModeCnt(self.selectedFb) and (p.isInTeamOrGroup() and p.isTeamLeader() or not p.isInTeamOrGroup()):
            matchCrazyShishen = True
        canFubenGuide = False
        canDestroy = self.fbInfo.get('canDestroyInfo', {}).get(self.selectedFb, False)
        canGroupMatch = uiUtils.checkFbGroupMatchCondition(self.selectedFb) and uiUtils.checkIsCanGroupMatch(isEnableGroupMatch)
        gamelog.debug('@hjx fb#onGetBtnInfo:', self.selectedFb)
        ret.SetMember('canDestroy', GfxValue(canDestroy))
        ret.SetMember('canGroupMatch', GfxValue(canGroupMatch))
        ret.SetMember('canFubenGuide', GfxValue(canFubenGuide))
        ret.SetMember('matchCrazyShishen', GfxValue(matchCrazyShishen))
        ret.SetMember('rankListBtnEnabled', GfxValue(self.isRankListBtnEnabled()))
        return ret

    def isRankListBtnEnabled(self):
        if self.selectedFb <= 0:
            return False
        fbList = [ fbData['fbNo'] for _, fbData in TFD.data.items() ] + const.GROUP_FB_TOP_TYPE_MAP.keys()
        return self.selectedFb in fbList

    def refreshFubenBtn(self):
        if self.buttonMediator:
            self.buttonMediator.Invoke('setBtnAvailable', (self.onGetBtnInfo(),))

    def refreshGuideIcon(self):
        if not self.descMediator:
            return
        descInfo = self.getGuideIconState()
        if descInfo:
            self.descMediator.Invoke('refreshGuideIcon', descInfo)

    def getGuideIconState(self):
        data = FD.data.get(self.selectedFb, {})
        guideMode = data.get('guideMode', 0)
        info = {}
        if guideMode:
            guideState = BigWorld.player().fbGuideModeLoginInfo(self.selectedFb)[0]
            info['enableGuide'] = guideState == gametypes.FB_GUIDE_SUC
            guideTip = GUIDE_TIP[guideState]
            tipContent = SCD.data.get(guideTip, '')
            info['guideTip'] = tipContent
        return uiUtils.dict2GfxDict(info, True)

    def onGetDesc(self, *arg):
        data = FD.data.get(self.selectedFb, {})
        obj = {}
        obj['fubenName'] = formula.getFbDetailName(self.selectedFb)
        obj['num'] = data.get('recommendNumber', 1)
        obj['lv'] = '%d~%d' % (data.get('lvMin', 0), data.get('lvMax', 0))
        enterNum = self.fbInfo.get('enterInfo', {}).get(self.selectedFb, (0, 0))
        obj['enterNum'] = '%d/%d' % enterNum
        obj['time'] = str(data.get('time', 6000) / 60) + gameStrings.TEXT_FUBENLOGINPROXY_665
        obj['guide'] = data.get('guideDesc', gameStrings.TEXT_BATTLEFIELDPROXY_1605)
        obj['condition'] = data.get('fbDescription', '')
        obj['exp'] = self.isShowExpAdd(data)
        guideMode = data.get('guideMode', 0)
        BigWorld.player().guideDataCheck(self.selectedFb)
        if guideMode:
            obj['guideOpen'] = True
            guideState = BigWorld.player().fbGuideModeLoginInfo(self.selectedFb)[0]
            obj['enableGuide'] = guideState == gametypes.FB_GUIDE_SUC
            guideTip = GUIDE_TIP[guideState]
            tipContent = SCD.data.get(guideTip, '')
            obj['guideTip'] = tipContent
        else:
            obj['guideOpen'] = False
        itemArray = []
        itemInfo = []
        self.dropItems = data.get('dropItems', [])
        for i, itemId in enumerate(self.dropItems):
            itemArray.append(itemId)
            itemInfo.append(self.getSlotValue(i))

        obj['itemArray'] = itemArray
        obj['itemInfo'] = itemInfo
        return uiUtils.dict2GfxDict(obj, True)

    def onGetMap(self, *arg):
        obj = {}
        background = self.fbInfo.get('fbBackground', 'fbLingxu')
        obj['mapPath'] = 'widgets/%s%s' % (background, gameglobal.rds.ui.getUIExt())
        fbLocation = self.fbInfo.get('fbLocation', [])
        p = BigWorld.player()
        guanQiaArray = []
        closeLocationArray = []
        transport = BigWorld.entities.get(self.transportEntId)
        charType = getattr(transport, 'charType', 0)
        jingsuActivityLocation = TD.data.get(charType, {}).get('jingsuActivityLocation', ())
        for i, fbNo in enumerate(self.fbInfo['fbList']):
            guanQia = {}
            data = FD.data.get(fbNo, {})
            mode = data.get('fbMode', 0)
            style = data.get('fbStyle', 0)
            guanQia['fbNo'] = fbNo
            guanQia['lock'] = self.fbInfo.get('lockInfo', {}).get(fbNo, 0)
            if gameglobal.rds.configData.get('enableServerProgress', False) and data.get('serverProgressMsId', None) and utils.getHostId() not in data.get('spExcludeHostIds', ()):
                serverProgressMsId = data.get('serverProgressMsId', [])
                if not p.hadServerProgressFinished(serverProgressMsId):
                    guanQia['lock'] = 1
            guanQia['relyLock'] = self.fbInfo.get('stubEnableInfo', {}).get(fbNo, 2) == 1
            guanQia['relyTip'] = data.get('relyLockTip', '')
            guanQia['mode'] = mode
            guanQia['msg'] = data.get('keyHint', '')
            if fbLocation and i < len(fbLocation):
                guanQia['fbLocation'] = fbLocation[i]
            else:
                guanQia['fbLocation'] = i
            fud = FUD.data.get(fbNo, {})
            buffInfo = fud.get('buffAward', [])
            guanQia['buff'] = self.getBuffInfo(buffInfo)
            bonusId = fud.get('bonusId', 0)
            guanQia['bonus'] = self.getLockBonus(bonusId)
            guanQia['modeIcon'] = self.fbStyle[style]
            guanQiaArray.append(guanQia)
            if guanQia['fbLocation'] in jingsuActivityLocation and (not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_FUBEN_RACE) or not commNewServerActivity.checkNSJingSuInActivityTime(guanQia['fbNo'])):
                closeLocationArray.append(guanQia['fbLocation'])

        for location in jingsuActivityLocation:
            if location not in fbLocation:
                closeLocationArray.append(location)

        obj['guanQiaArray'] = guanQiaArray
        obj['selectedFb'] = self.selectedFb
        obj['currentFb'] = self.fbInfo.get('currentFb', 0)
        obj['closeLocationArray'] = closeLocationArray
        return uiUtils.dict2GfxDict(obj, True)

    def getBuffInfo(self, buffInfo):
        if not buffInfo:
            return ''
        ret = {}
        buffId, bufflv, buffTime = buffInfo
        sd = SD.data.get(buffId, {})
        iconPath = 'state/icon/%d.dds' % sd.get('iconId', 0)
        ret['iconPath'] = iconPath
        ret['time'] = buffTime
        ret['tip'] = sd.get('name', '') + '\n' + sd.get('desc', '')
        return ret

    def getLockBonus(self, bonusId):
        bonus = clientUtils.genItemBonus(bonusId)
        if not bonus:
            return ''
        ret = gameStrings.TEXT_FUBENLOGINPROXY_764
        for itemId, itemNum in bonus:
            itemName = ID.data.get(itemId, {}).get('name', '')
            ret += itemName + 'x%s\n' % itemNum

        return ret

    def getSlotValue(self, index):
        ret = {}
        if self.dropItems and index < len(self.dropItems):
            itemIdx = self.dropItems[index]
            itemData = ID.data.get(itemIdx, {})
            path = uiUtils.getItemIconFile40(itemIdx)
            ret['iconPath'] = path
            quality = itemData.get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            ret['color'] = color
        else:
            ret['iconPath'] = ''
            ret['color'] = 'nothing'
        return ret

    def getFameStep(self, group, primaryLevel):
        fbGroups = FUGD.data.get(group, [])
        fameStep = set()
        fameId = 0
        for fbNo in fbGroups:
            fud = FUD.data.get(fbNo, {})
            if fud.get('primaryLevel', 0) == primaryLevel:
                fameInfo = fud.get('unlockFame', [0, 0])
                fameStep.add(fameInfo[1])
                if fameInfo[0]:
                    fameId = fameInfo[0]

        fameStep = list(fameStep)
        fameStep.sort()
        return (fameId, fameStep)

    def onGetFbTip(self, *arg):
        index = int(arg[3][0].GetNumber())
        fbNo = self.fbInfo['fbList'][index]
        data = FD.data.get(fbNo, {})
        obj = {}
        fbStyle = data.get('fbStyle', 0)
        obj['fubenName'] = formula.getFbDetailName(fbNo)
        obj['modeIcon'] = self.fbStyle[fbStyle]
        obj['lock'] = self.fbInfo.get('lockInfo', {}).get(fbNo, 0)
        p = BigWorld.player()
        fud = FUD.data.get(fbNo, {})
        fameInfo = fud.get('unlockFame', None)
        fameId, obj['fameStep'] = self.getFameStep(fud.get('group', 0), fud.get('primaryLevel', 0))
        if fameId:
            obj['currentFame'] = p.fame.get(fameId, 0)
        else:
            obj['currentFame'] = 0
        if fameInfo:
            obj['fameStepIndex'] = obj['fameStep'].index(fameInfo[1])
        else:
            obj['fameStepIndex'] = 0
        obj['maxFame'] = FAD.data.get(fameId, {}).get('maxVal', 0)
        obj['condition'] = []
        lv = fud.get('unlockLevel', 0)
        if lv:
            lvText = PRE_FLAG + gameStrings.TEXT_FUBENLOGINPROXY_830 % lv
            lvColor = ''
            if p.lv < lv:
                lvColor = WARNNING_COLOR
            obj['condition'].append((lvText, lvColor))
        questId = fud.get('unlockQuestId', 0)
        if questId:
            questText = PRE_FLAG + gameStrings.TEXT_FUBENLOGINPROXY_838 + QD.data.get(questId, {}).get('name', '') + gameStrings.TEXT_FUBENLOGINPROXY_838_1
            questColor = ''
            if not p.getQuestFlag(questId):
                questColor = WARNNING_COLOR
            obj['condition'].append((questText, questColor))
        achieveId = fud.get('unlockAchieveId', 0)
        if achieveId:
            achieveFbText = PRE_FLAG + gameStrings.TEXT_FUBENLOGINPROXY_846 + AD.data.get(achieveId, {}).get('name', '') + gameStrings.TEXT_FUBENLOGINPROXY_846_1
            achieveFbColor = ''
            if self.fbInfo.has_key('achieveFb') and fbNo in self.fbInfo['achieveFb']:
                pass
            else:
                achieveFbColor = WARNNING_COLOR
            obj['condition'].append((achieveFbText, achieveFbColor))
        if fameInfo:
            fameText = PRE_FLAG + gameStrings.TEXT_FUBENLOGINPROXY_855 % fameInfo[1]
            fameColor = ''
            if obj['currentFame'] < fameInfo[1]:
                fameColor = WARNNING_COLOR
            obj['condition'].append((fameText, fameColor))
        unlockItemId = fud.get('unlockItemId', 0)
        if unlockItemId:
            itemText = PRE_FLAG + gameStrings.TEXT_FUBENLOGINPROXY_863 + ID.data.get(unlockItemId, {}).get('name', '') + gameStrings.TEXT_FUBENLOGINPROXY_863_1
            itemColor = ''
            if obj['lock'] != 2:
                itemColor = WARNNING_COLOR
            obj['condition'].append((itemText, itemColor))
        if gameglobal.rds.configData.get('enableServerProgress', False) and data.get('serverProgressMsId', None) and utils.getHostId() not in data.get('spExcludeHostIds', ()):
            serverProgressMsId = data.get('serverProgressMsId')
            color = WARNNING_COLOR if not p.hadServerProgressFinished(serverProgressMsId) else ''
            text = gameStrings.TEXT_FUBENLOGINPROXY_872 % SPD.data.get(serverProgressMsId[0], {}).get('tipsName', '')
            obj['condition'].append((text, color))
        return uiUtils.dict2GfxDict(obj, True)

    def updateCrazyShishenModeCnt(self, fbNo, cnt):
        if fbNo not in self.crazyShishenModeInfo:
            self.crazyShishenModeInfo[fbNo] = [cnt, FD.data.get(fbNo, {}).get('crazyShishenModelThreshold', 0)]
        else:
            self.crazyShishenModeInfo[fbNo][0] = cnt
        self.refreshFubenBtn()

    def getCrazyShishenModeMaxCnt(self, fbNo):
        return self.crazyShishenModeInfo.get(fbNo, (0, 0))[1]

    def getCrazyShishenModeCnt(self, fbNo):
        return self.crazyShishenModeInfo.get(fbNo, (0, 0))[0]

    def showCrazyModeItems(self):
        items = FD.data.get(self.selectedFb, {}).get('crazyReinforceItems', [])
        itemList = []
        for itemId in items:
            itemInfo = (itemId, '', 1)
            itemList.append(itemInfo)

        msg = uiUtils.getTextFromGMD(GMDD.data.CRAZYMODE_ITEM_NEED_TIP, gameStrings.TEXT_FUBENLOGINPROXY_898)
        gameglobal.rds.ui.itemSelect.show(itemList, msg, None, Functor(self.onConfirmSelectItem))

    def onConfirmSelectItem(self, itemInfo):
        gameglobal.rds.ui.itemSelect.hide()
        BigWorld.player().cell.fbModeSelected(self.transportEntId, self.selectedFb, 0, itemInfo[0], gametypes.FB_SHISHEN_MODE_HIGH)

    def onShowSealInfo(self, *args):
        sealFbNo = int(args[3][0].GetNumber())
        self.uiAdapter.fengyinShow.show(sealFbNo)
