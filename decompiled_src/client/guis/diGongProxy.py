#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/diGongProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import random
import gameglobal
import const
import formula
import uiUtils
import gametypes
import gamelog
from guis import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy
from gameStrings import gameStrings
from callbackHelper import Functor
from data import multiline_digong_data as MDD
from data import transport_data as TD
from data import game_msg_data as GMD
from cdata import teleport_destination_data as TDD
from cdata import game_msg_def_data as GMDD
from data import activity_basic_data as ABD
from data import sys_config_data as SCD
from data import clan_war_fort_data as CWFD

class DiGongProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DiGongProxy, self).__init__(uiAdapter)
        self.modelMap = {'getLines': self.onGetLines,
         'getLineInfo': self.onGetLineInfo,
         'enterLine': self.onEnterLine,
         'closePanel': self.onClosePanel,
         'getTitleName': self.onGetTitleName,
         'countDownFinished': self.onCountDownFinished,
         'getClockContent': self.onGetClockContent,
         'getLineNo': self.onGetLineNo,
         'switchLine': self.onSwitchLine,
         'getDiGongPic': self.onGetDiGongPic,
         'diGongButtonClick': self.onDiGongButtonClick,
         'showLeaderSetting': self.onShowLeaderSetting,
         'closeLeaderSetting': self.onCloseLeaderSetting,
         'getLingZhuInfo': self.onGetLingZhuInfo,
         'leaderSetting': self.onLeaderSetting,
         'changeTab': self.onChangeTab,
         'hasLingzhuDiGong': self.onHasLingzhuDiGong,
         'canChooseMode': self.canChooseMode,
         'isLingZhu': self.isLingZhu,
         'inLingzhuDiGong': self.onInLingzhuDiGong,
         'getDesc': self.onGetDescription,
         'updateData': self.onUpdateData,
         'getLinesStateDesc': self.onGetLinesStateDesc,
         'getDefaultLingzhuMonsterLv': self.onGetDefaultLingzhuMonsterLv,
         'confirmSelectDigong': self.onConfirmSelectDigong,
         'fastEnterLine': self.onFastEnterLine,
         'isVisibleFastEnterBtn': self.onIsVisibleFastEnterBtn}
        self.isShow = False
        self.lineInfo = {}
        self.lingzhuLineInfo = {}
        self.transportId = 0
        self.mlgNo = 0
        self.commonMlgNo = 0
        self.lingzhumlgNo = 0
        self.currentTab = 0
        self.canBeShow = False
        self.isInit = True
        self.switchMediator = None
        self.clockMediator = None
        self.lineInfoMediator = None
        self.leaderSettingMediator = None
        self.clockText = ''
        self.timeVal = 0
        self.startOnShow = True
        self.countDown = True
        self.clockShow = False
        self.lingzhuInfo = {}
        self.canChooseMode = False
        self.isLingZhu = False
        self.timerId = 0
        self.inLingZhuDigong = False
        self.minLevel = 0
        self.maxLevel = 100
        self.isFromActivity = False
        self.actId = 0
        self.selectMlgNos = None
        self.debugInfo = {}
        self.enterBaseMLNo = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_DIGONG, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_DIGONG_SELECT, self.hideDigongSelect)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DIGONG_CLOCK:
            self.clockMediator = mediator
        elif widgetId == uiConst.WIDGET_DIGONG:
            self.lineInfoMediator = mediator
        elif widgetId == uiConst.WIDGET_DIGONG_LEADER_SETTING:
            self.leaderSettingMediator = mediator
        elif widgetId == uiConst.WIDGET_DIGONG_SELECT:
            initData = []
            for mlgNo in self.selectMlgNos:
                initData.append({'res': 'digongSelect/%s.dds' % mlgNo,
                 'desc': MDD.data.get(mlgNo, {}).get('desc', ''),
                 'actId': self.actId,
                 'mlgNo': mlgNo})

            return uiUtils.array2GfxAarry(initData, True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_DIGONG_SELECT:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DIGONG_SELECT)
        else:
            UIProxy._asWidgetClose(self, widgetId, multiID)

    def onGetLines(self, *arg):
        tab = arg[3][0].GetNumber()
        self.currentTab = int(tab)
        ret = []
        lineNoList = self._sortLineNo()
        lineInfo = self.getInfoData()
        fullList = []
        notFullList = []
        isMax = True
        for i, lineNo in enumerate(lineNoList):
            info = lineInfo['lines'][lineNo]
            groupNo = lineInfo.get('groupNo', 0)
            count = info.get('count', 0)
            lineMemberMax = int(MDD.data[groupNo].get('lineMemberMax') * lineInfo.get('lineMemberRatio', 1))
            if gameglobal.rds.configData.get('enableDiGongLineLogic', False):
                defaultLineCount = MDD.data.get(groupNo, {}).get('defaultLineCount', 0)
                if defaultLineCount > 0 and i > defaultLineCount - 1 and count == 0 and not isMax:
                    continue
                if count < lineMemberMax:
                    isMax = False
            ar = {}
            ar['lineName'] = gameStrings.TEXT_DIGONGPROXY_147 + str(lineNo + 1)
            info = lineInfo['lines'][lineNo]
            status = info.get('status', 0)
            selfLineNo, _ = formula.getMLInfo(BigWorld.player().spaceNo)
            ar['lineNo'] = lineNo
            ar['status'] = status
            ar['selfLine'] = selfLineNo == lineNo
            ar['count'] = count
            ar['max'] = lineMemberMax
            if count >= lineMemberMax:
                fullList.append(ar)
            else:
                notFullList.append(ar)
            ret.append(ar)

        if self.getFullSortEffectOrNot():
            fullList.sort(key=lambda k: k['lineNo'])
            notFullList.sort(key=lambda k: k['lineNo'])
            ret = notFullList + fullList
        else:
            ret.sort(key=lambda k: k['lineNo'])
        return uiUtils.array2GfxAarry(ret, True)

    def _sortLineNo(self):
        lineNoList = self.getLineNoList()
        lineInfo = self.getInfoData()
        emptyLines = []
        for i, lineNo in enumerate(lineNoList):
            info = lineInfo['lines'][lineNo]
            count = info.get('count', 0)
            if count == 0:
                emptyLines.append(lineNo)
                lineNoList.remove(lineNo)

        lineNoList.extend(emptyLines)
        return lineNoList

    def getInfoData(self):
        info = {}
        if self.currentTab == 0:
            info = self.lineInfo
        elif self.currentTab == 1:
            info = self.lingzhuLineInfo
        return info

    def onGetLineInfo(self, *arg):
        lineNo = int(arg[3][0].GetNumber())
        lineNoList = self.getLineNoList()
        lineInfo = self.getInfoData()
        if lineNo not in lineNoList:
            if self.lineInfoMediator:
                self.lineInfoMediator.Invoke('setLines')
            return
        info = lineInfo['lines'][lineNo]
        status = (gameStrings.TEXT_DIGONGPROXY_207,
         gameStrings.TEXT_DIGONGPROXY_207_1,
         gameStrings.TEXT_DIGONGPROXY_207_2,
         gameStrings.TEXT_DIGONGPROXY_207_3,
         gameStrings.TEXT_DIGONGPROXY_207_2,
         gameStrings.TEXT_DIGONGPROXY_207_4)
        groupNo = lineInfo.get('groupNo', 0)
        lineMemberMax = int(MDD.data[groupNo].get('lineMemberMax') * lineInfo.get('lineMemberRatio', 1))
        ret = self.movie.CreateArray()
        ret.SetElement(0, GfxValue(info.get('count', 0)))
        ret.SetElement(1, GfxValue(lineMemberMax))
        ret.SetElement(2, GfxValue(gbk2unicode(status[info.get('status', 0)])))
        ret.SetElement(3, GfxValue(info.get('mcount', 0)))
        return ret

    def onGetLingZhuInfo(self, *arg):
        if self.lingzhuInfo != {}:
            self.updateLingzhuInfo(self.lingzhuInfo)
        else:
            p = BigWorld.player()
            mlgNo = formula.getMLGNo(p.spaceNo)
            p.cell.queryLingzhuInfo(mlgNo)

    def setLineInfo(self, mlgNo, info):
        if mlgNo == self.commonMlgNo:
            self.lineInfo = info
            self.debugInfo = info
        elif mlgNo == self.lingzhumlgNo:
            self.lingzhuLineInfo = info
        if self.canBeShow and not self.isShow:
            self.realShow()
        elif self.isShow:
            self.lineInfoMediator and self.lineInfoMediator.Invoke('setLines')

    def getLineNoList(self):
        lineNoList = []
        if self.currentTab == 0 and self.lineInfo.has_key('lines'):
            if len(self.lineInfo['lines'].keys()) == 0:
                BigWorld.player().showGameMsg(GMDD.data.COMMON_MSG, gameStrings.TEXT_DIGONGPROXY_245)
            lineNoList = self.lineInfo['lines'].keys()
        elif self.currentTab == 1 and self.lingzhuLineInfo.has_key('lines'):
            lineNoList = self.lingzhuLineInfo['lines'].keys()
        lineNoList.sort()
        return lineNoList

    def onEnterLine(self, *arg):
        lineNo = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if p.getIsAllNotFollow():
            self._onEnterLine(lineNo)
        else:
            msg = gameStrings.CONFIRM_ENTERLINE_INGROUPFOLLOW
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cancelGroupFollowEnterLine, lineNo))

    def cancelGroupFollowEnterLine(self, lineNo):
        p = BigWorld.player()
        p.cell.cancelGroupFollow()
        self._onEnterLine(lineNo)

    def _onEnterLine(self, lineNo = None):
        lineNoList = self.getLineNoList()
        if lineNo is None and lineNoList:
            lineNo = random.choice(lineNoList)
        p = BigWorld.player()
        if lineNo in lineNoList:
            p.cancelTransportSpell()
            if self.enterBaseMLNo:
                if p.inCombat:
                    p.showGameMsg(GMDD.data.ENTER_LINE_FAIL_IN_COMBAT, ())
                else:
                    curMLGNo = formula.getMLGNo(p.spaceNo)
                    if formula.spaceInMultiLine(p.spaceNo) and curMLGNo == self.enterBaseMLNo:
                        fromLineNo, _ = formula.getMLInfo(p.spaceNo)
                        if fromLineNo != lineNo:
                            p.cell.switchLine(lineNo, 0)
                    else:
                        p.cell.enterLineByActivity(self.enterBaseMLNo, lineNo, 0, 0)
                    self.hide()
            elif self.isFromActivity:
                if p.inCombat:
                    p.showGameMsg(GMDD.data.ENTER_LINE_FAIL_IN_COMBAT, ())
                else:
                    if formula.spaceInMultiLine(p.spaceNo):
                        p.showGameMsg(GMDD.data.SWITCH_LINE_FAILED_FROM_ACTIVITY_PANEL, ())
                    else:
                        btnActionType = ABD.data.get(self.actId, {}).get('btnActionType', 0)
                        if btnActionType == gametypes.ACTIVITY_ENTER_TYPE_DIGONG_SXY:
                            p.cell.enterLineByActivity(self.commonMlgNo, lineNo, 0, 0)
                        elif btnActionType == gametypes.ACTIVITY_ENTER_TYPE_DIGONG_YMF:
                            p = BigWorld.player()
                            if p.pvpTempCamp == const.CAMP_PVP_TEMP_CAMP_NONE:
                                p.showGameMsg(GMDD.data.DIGONG_BATTLE_FIELD_ENTER_FAILED_NO_CAMP, ())
                                return
                            _, destIds = ABD.data.get(self.actId, {}).get('btnActionArg', {})
                            playerDest = destIds.get(p.pvpTempCamp, ())
                            if playerDest:
                                random.shuffle(playerDest)
                                destId = playerDest[0]
                                p.cell.enterLineByActivity(self.commonMlgNo, lineNo, 0, destId)
                        elif btnActionType == gametypes.ACTIVIIY_ENTER_TYPE_DIGONG_DYD:
                            if p.inCombat:
                                p.showGameMsg(GMDD.data.ENTER_LINE_FAIL_IN_COMBAT, ())
                            else:
                                if formula.spaceInMultiLine(p.spaceNo):
                                    fromLineNo, _ = formula.getMLInfo(p.spaceNo)
                                    if fromLineNo != lineNo:
                                        p.cell.switchLine(lineNo, 0)
                                else:
                                    p.cell.enterLineByActivity(const.ML_GROUP_NO_FISHING, lineNo, 0, 0)
                                self.hide()
                        else:
                            gamelog.error('btnActionType error:%d:%d' % (self.actId, btnActionType))
                    self.hide()
            elif formula.spaceInMultiLine(p.spaceNo):
                p.cell.switchLine(lineNo, 0)
            elif p.stateMachine.checkStatus(const.CT_ENTER_MULTILINE):
                p.cell.lineSelected(self.transportId, self.currentTab, lineNo)

    def onClosePanel(self, *arg):
        self.hide()

    def onGetTitleName(self, *arg):
        lineInfo = self.getInfoData()
        groupNo = lineInfo.get('groupNo', 0)
        name = MDD.data.get(groupNo, {}).get('name', '')
        return GfxValue(gbk2unicode(name))

    def onGetDescription(self, *arg):
        lineInfo = self.getInfoData()
        groupNo = lineInfo.get('groupNo', 0)
        desc = MDD.data.get(groupNo, {}).get('desc', '')
        return GfxValue(gbk2unicode(desc))

    def show(self, transportId = 0, enterBaseMlNo = 0):
        self.canBeShow = True
        if self.transportId != transportId:
            self.lineInfo = {}
            self.lingzhuLineInfo = {}
            self.lingzhuInfo = {}
            self.commonMlgNo = 0
            self.lingzhumlgNo = 0
        self.transportId = transportId
        self.enterBaseMLNo = enterBaseMlNo
        self.inLingZhuDigong = False
        self.callData()

    def onUpdateData(self, *arg):
        self.updateData()

    def callData(self):
        if self.enterBaseMLNo:
            self.commonMlgNo = self.enterBaseMLNo
            self.canChooseMode = False
        elif self.transportId == 0:
            p = BigWorld.player()
            self.commonMlgNo = formula.getMLGNo(p.spaceNo)
            self.canChooseMode = False
            multilineData = MDD.data.get(self.commonMlgNo, {})
            self.inLingZhuDigong = multilineData.has_key('owerFortId')
        else:
            ent = BigWorld.entity(self.transportId)
            if ent:
                tData = TD.data.get(ent.charType, {})
                dest = tData.get('destination', [])
                self.commonMlgNo = self.getMlgNo(dest[0][0])
                if len(dest) > 1:
                    self.lingzhumlgNo = self.getMlgNo(dest[1][0])
            self.canChooseMode = True
        p = BigWorld.player()
        if self.commonMlgNo != 0:
            p.cell.queryLines(self.commonMlgNo)
        if self.lingzhumlgNo != 0:
            p.cell.queryLingzhuLines(self.lingzhumlgNo)
            p.cell.queryLingzhuInfo(self.lingzhumlgNo)

    def showDigongSelect(self, actId, mlgNos):
        self.actId = actId
        self.selectMlgNos = mlgNos
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DIGONG_SELECT)

    def showFromActivity(self, actId, commonMlgNo):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DIGONG_SELECT)
        self.enterBaseMLNo = 0
        if isinstance(commonMlgNo, tuple):
            if len(commonMlgNo) == 2:
                self.showDigongSelect(actId, commonMlgNo)
        else:
            self.showSingleDigongFromActivity(actId, commonMlgNo)

    def showSingleDigongFromActivity(self, actId, mlgNo):
        self.actId = actId
        self.commonMlgNo = mlgNo
        self.enterBaseMLNo = 0
        p = BigWorld.player()
        if self.commonMlgNo != 0:
            self.canBeShow = True
            self.isFromActivity = True
            p.cell.queryLinesFromActivity(self.actId, self.commonMlgNo)

    def updateData(self):
        p = BigWorld.player()
        if self.currentTab == 0 and self.commonMlgNo != 0:
            p.cell.queryLines(self.commonMlgNo)
            p.cell.queryLingzhuInfo(self.commonMlgNo)
        elif self.currentTab == 1 and self.lingzhumlgNo != 0:
            p.cell.queryLingzhuLines(self.lingzhumlgNo)
            p.cell.queryLingzhuInfo(self.lingzhumlgNo)
        elif self.isFromActivity and self.actId and self.commonMlgNo:
            p.cell.queryLinesFromActivity(self.actId, self.commonMlgNo)

    def getMlgNo(self, des):
        mlgNo = 0
        data = TDD.data.get(des, {})
        if data != None:
            space = data.get('space', 0)
            if space != 0:
                mlgNo = formula.getMLGNoByMLNo(space)
        return mlgNo

    def realShow(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DIGONG)
        self.isShow = True

    def clearWidget(self):
        BigWorld.cancelCallback(self.timerId)
        self.lineInfoMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DIGONG)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DIGONG_SELECT)
        self.isShow = False

    def hideDigongSelect(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DIGONG_SELECT)

    def reset(self):
        self.transportId = 0
        self.canBeShow = False
        self.enterBaseMLNo = 0
        self.lineInfo = {}
        self.lingzhuLineInfo = {}
        self.currentTab = 0
        self.lingzhuInfo = {}
        self.isFromActivity = False

    def setClockText(self, text):
        if self.clockMediator:
            self.clockMediator.Invoke('setClockText', GfxValue(gbk2unicode(text)))

    def startClock(self, timeVal, isCountDown = True):
        if self.clockMediator:
            self.clockMediator.Invoke('startClock', (GfxValue(timeVal), GfxValue(isCountDown)))

    def showDigongClock(self, msgId, msgArgs, timeVal, startOnShow = True, countDown = True):
        text = GMD.data.get(msgId, {}).get('text')
        if text:
            text = text % msgArgs
        self.clockText = text
        self.timeVal = timeVal - 2
        self.startOnShow = startOnShow
        self.countDown = countDown
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DIGONG_CLOCK)
        self.clockShow = True

    def onShowLeaderSetting(self, *arg):
        if self.lingzhuInfo != {}:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DIGONG_LEADER_SETTING)

    def onCloseLeaderSetting(self, *arg):
        self.leaderSettingMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DIGONG_LEADER_SETTING)

    def onLeaderSetting(self, *arg):
        level = int(arg[3][0].GetNumber())
        if level < self.minLevel or level > self.maxLevel:
            BigWorld.player().showGameMsg(GMDD.data.WRONG_DIGONG_LEVEL_TO_SET, ())
            return
        else:
            if self.lingzhumlgNo > 0:
                BigWorld.player().cell.setLingzhuDigongMonsterLv(self.lingzhumlgNo, level)
                self.callData()
            if self.leaderSettingMediator != None:
                self.onCloseLeaderSetting()
            return

    def closeDigongClock(self):
        self.clockMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DIGONG_CLOCK)
        self.clockShow = False

    def onCountDownFinished(self, *arg):
        self.closeDigongClock()

    def onGetClockContent(self, *arg):
        ret = self.movie.CreateArray()
        ret.SetElement(0, GfxValue(gbk2unicode(self.clockText)))
        ret.SetElement(1, GfxValue(self.timeVal))
        ret.SetElement(2, GfxValue(self.startOnShow))
        ret.SetElement(3, GfxValue(self.countDown))
        return ret

    def onGetLineNo(self, *arg):
        lineNo, _ = formula.getMLInfo(BigWorld.player().spaceNo)
        return GfxValue(gbk2unicode(gameStrings.TEXT_DIGONGPROXY_528 % (lineNo + 1)))

    def onSwitchLine(self, *arg):
        p = BigWorld.player()
        mlgNo = formula.getMLGNo(p.spaceNo)
        p.cell.queryLines(mlgNo)
        self.show()

    def onGetDiGongPic(self, *arg):
        groupNo = self.lineInfo.get('groupNo', 0)
        iconPath = MDD.data.get(groupNo, {}).get('iconPath', '100')
        path = 'diGong/%s.dds' % iconPath
        return GfxValue(path)

    def onDiGongButtonClick(self, *arg):
        mlgNo = formula.getMLGNo(BigWorld.player().spaceNo)
        lineData = MDD.data.get(mlgNo)
        if lineData:
            destId = lineData.get('destination', ())
            if mlgNo == const.ML_SPACE_NO_DAFUWENG:
                mlNo = formula.getMLNo(BigWorld.player().spaceNo)
                if mlNo > const.ML_SPACE_NO_DAFUWENG_FLOOR1:
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_DIGONGPROXY_552, self._realExitLine)
                else:
                    self._realExitLine()
            elif len(destId) > 1:
                msg = uiUtils.getTextFromGMD(GMDD.data.LEAVE_DI_GONG_MULTI_DES_MSG, '%s') % lineData.get('name', '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self._realExitLine)
            elif uiUtils.inNeedNotifyStates():
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_DIGONGPROXY_559, self._realExitLine)
            else:
                self._realExitLine()

    def _realExitLine(self):
        p = BigWorld.player()
        if getattr(p, 'inGroupFollow', None) and not getattr(p, 'groupHeader', None) == p.id:
            p.cell.cancelGroupFollow()
        p.cell.exitLine()

    def _getAllLeaders(self):
        p = BigWorld.player()
        ret = []
        owerFortId = MDD.data.get(self.lingzhumlgNo, {}).get('owerFortId', 0)
        ownerSubFortIds = MDD.data.get(self.lingzhumlgNo, {}).get('ownerSubFortIds', [])
        if p.clanWar.fort.has_key(owerFortId) and p.clanWar.fort[owerFortId].ownerGuildNUID > 0:
            ret.append(p.clanWar.fort[owerFortId].ownerGuildNUID)
        else:
            for ownerSubId in ownerSubFortIds:
                if p.clanWar.fort.has_key(ownerSubId) and p.clanWar.fort[ownerSubId].ownerGuildNUID > 0:
                    ret.append(p.clanWar.fort[ownerSubId].ownerGuildNUID)

        return ret

    def setLingzhuInfo(self, info):
        p = BigWorld.player()
        owerFortId = MDD.data.get(self.lingzhumlgNo, {}).get('owerFortId', 0)
        if info != None:
            self.lingzhuInfo = info
            isClaimed = p.clanWar.fort.has_key(owerFortId) and p.clanWar.fort[owerFortId].ownerGuildNUID > 0
            self.lingzhuLineInfo['isClaimed'] = isClaimed
            if not info.has_key('configRole'):
                self.lingzhuInfo['hasConfigRole'] = False
                if info.has_key('lv'):
                    self.lingzhuInfo['defaultMonsterLv'] = uiUtils.getTextFromGMD(GMDD.data.LAST_TIME_DIGONG_MONSTER_LEVEL, gameStrings.TEXT_DIGONGPROXY_599) % info['lv']
                else:
                    self.lingzhuInfo['defaultMonsterLv'] = uiUtils.getTextFromGMD(GMDD.data.DEFAULT_DIGONG_MONSTER_LEVEL, gameStrings.TEXT_DIGONGPROXY_601)
            else:
                self.lingzhuInfo['hasConfigRole'] = True
            allLeaders = self._getAllLeaders()
            self.isLingZhu = p.guildNUID in allLeaders and p.gbId == p.guild.leaderGbId
            info['isLingZhu'] = self.isLingZhu
            if info.get('tSetMonsterProp', 0) == 0 or not info.has_key('configRole'):
                info['timeLeft'] = -1
            else:
                info['timeLeft'] = info['tSetMonsterProp'] - BigWorld.player().getServerTime()
            if not info.has_key('lvRange'):
                self.minLevel = 0
                self.maxLevel = 100
            else:
                self.minLevel = info['lvRange'][0]
                self.maxLevel = info['lvRange'][1]
            if isClaimed and len(self.lingzhuInfo['leaderRoles']) > 0:
                self.lingzhuInfo['leaderRole'] = self.lingzhuInfo['leaderRoles'][0]
            else:
                self.lingzhuInfo['leaderRole'] = gameStrings.TEXT_DIGONGPROXY_622 % CWFD.data.get(owerFortId, {}).get('name', '')
            self.lingzhuInfo['minLv'] = self.minLevel
            self.lingzhuInfo['maxLv'] = self.maxLevel
            self.updateLingzhuInfo(self.lingzhuInfo)

    def updateLingzhuInfo(self, info):
        self.lingzhuInfo = info
        if self.lineInfoMediator != None:
            self.lineInfoMediator.Invoke('updateLingzhuInfo', uiUtils.dict2GfxDict(self.lingzhuInfo, True))
        if self.leaderSettingMediator != None:
            self.leaderSettingMediator.Invoke('updateLingzhuInfo', uiUtils.dict2GfxDict(self.lingzhuInfo, True))

    def onChangeTab(self, *arg):
        self.currentTab = arg[3][0].GetNumber()
        if self.lineInfoMediator:
            self.lineInfoMediator.Invoke('setTitleName', self.onGetTitleName())
            self.lineInfoMediator.Invoke('setDescription', self.onGetDescription())

    def onHasLingzhuDiGong(self, *arg):
        hasLingZhuDiGong = self.lingzhuLineInfo != {}
        return GfxValue(hasLingZhuDiGong)

    def canChooseMode(self, *arg):
        return GfxValue(self.canChooseMode)

    def isLingZhu(self, *arg):
        return GfxValue(self.isLingZhu)

    def onInLingzhuDiGong(self, *arg):
        return GfxValue(self.inLingZhuDigong)

    def onGetLinesStateDesc(self, *arg):
        ret = SCD.data.get('DigongLineStateDesc', {'xinkai': gameStrings.TEXT_DIGONGPROXY_655,
         'kongxian': gameStrings.TEXT_DIGONGPROXY_655_1,
         'lianghao': gameStrings.TEXT_DIGONGPROXY_655_2,
         'fanmang': gameStrings.TEXT_DIGONGPROXY_655_3,
         'baoman': gameStrings.TEXT_DIGONGPROXY_655_4,
         'weihu': gameStrings.TEXT_DIGONGPROXY_655_5})
        return uiUtils.dict2GfxDict(ret, True)

    def onGetDefaultLingzhuMonsterLv(self, *arg):
        msg = uiUtils.getTextFromGMD(GMDD.data.DEFAULT_DIGONG_MONSTER_LEVEL, gameStrings.TEXT_DIGONGPROXY_659)
        return GfxValue(gbk2unicode(msg))

    def onConfirmSelectDigong(self, *args):
        actId = args[3][0].GetNumber()
        mlgNo = args[3][1].GetNumber()
        self.showSingleDigongFromActivity(actId, mlgNo)

    def onFastEnterLine(self, *args):
        p = BigWorld.player()
        mlNo = formula.getMLNo(p.spaceNo)
        if p.getIsAllNotFollow():
            if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_DI_GONG_FAST_ENTER):
                msg = uiUtils.getTextFromGMD(GMDD.data.DI_GONG_FAST_ENTER_DESC, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.sureFastEnter, mlNo), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_DI_GONG_FAST_ENTER)
            else:
                self.sureFastEnter(mlNo)
        else:
            msg = gameStrings.CONFIRM_ENTERLINE_INGROUPFOLLOW
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cancelGroupFollowFastEnter, mlNo))

    def cancelGroupFollowFastEnter(self, mlNo):
        p = BigWorld.player()
        p.cell.cancelGroupFollow()
        if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_DI_GONG_FAST_ENTER):
            msg = uiUtils.getTextFromGMD(GMDD.data.DI_GONG_FAST_ENTER_DESC, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.sureFastEnter, mlNo), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_DI_GONG_FAST_ENTER)
        else:
            self.sureFastEnter(mlNo)

    def sureFastEnter(self, mlNo):
        p = BigWorld.player()
        p.cell.quickEnterLine(mlNo)
        self.hide()

    def onIsVisibleFastEnterBtn(self, *args):
        p = BigWorld.player()
        mlgNo = formula.getMLGNo(p.spaceNo)
        if formula.isCrackSpaceML(mlgNo):
            isVisible = False
        else:
            isVisible = MDD.data.get(self.enterBaseMLNo, {}).get('isVisibleFastEnter', 0)
        return GfxValue(isVisible)

    def getFullSortEffectOrNot(self):
        p = BigWorld.player()
        mlgNo = formula.getMLGNo(p.spaceNo)
        if formula.isCrackSpaceML(mlgNo):
            isVisible = MDD.data.get(mlgNo, {}).get('isFullSortEffect', 0)
        else:
            isVisible = MDD.data.get(self.enterBaseMLNo, {}).get('isFullSortEffect', 0)
        return isVisible
