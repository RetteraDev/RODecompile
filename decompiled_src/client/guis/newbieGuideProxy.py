#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newbieGuideProxy.o
from gamestrings import gameStrings
import time
import BigWorld
import ui
import gameglobal
import uiConst
import uiUtils
import keys
import const
import utils
from uiProxy import UIProxy
from guis import events
from helpers import taboo
from guis.ui import unicode2gbk
from data import novice_bonus_config_data as NBCD
from data import novice_boost_score_type_data as NBSTD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
KEY_GOLDEN_MISSION = 2
KEY_APPRENTICE = 3
KEY_DIGION = 4
KEY_SHI_LIAN = 5
KEY_EXAM_FIRST = 6
KEY_EXAM_SECOND = 7
COLOR_GREEN = '#3C801A'
COLOR_GOLDEN = '#956D00'
COLOR_RED = '#BF0000'

class NewbieGuideProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewbieGuideProxy, self).__init__(uiAdapter)
        self.modelMap = {'getCardInfo': self.onGetCardInfo,
         'showNewbiLvGuide': self.onShowNewbiLvGuide,
         'minBtnFunc': self.onMinBtnFunc,
         'getButtonInfo': self.onGetButtonInfo,
         'setHitBtnIndex': self.onSetHitBtnIndex,
         'setGotoBtnIndex': self.onSetGotoBtnIndex,
         'clickIcon': self.onClickIcon,
         'getNewbieInfo': self.onGetNewbieInfo,
         'getFullLvReward': self.onGetFullLvReward,
         'sendMsg': self.onSendMsg}
        self.mediator = None
        self.lvMediator = None
        self.iconMediator = None
        self.lowReward = False
        self.highReward = False
        self.chatMsg = {}
        self.sendMsgLv = 0
        self.sendMsgIdx = 0
        self.sendMsgTitle = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_NEWBIE_MSG_INPUT, self.hideMsgInput)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_NEWBIE_GUIDE:
            self.mediator = mediator
        elif widgetId == uiConst.WIDGET_NEWBIE_LV_GUIDE:
            self.lvMediator = mediator
        elif widgetId == uiConst.WIDGET_NEWBIEGUILD_ICON:
            self.iconMediator = mediator
            self.refreshIconInfo()
        elif widgetId == uiConst.WIDGET_NEWBIE_MSG_INPUT:
            initData = {'title': self.sendMsgTitle,
             'tip': SCD.data.get('NEWBIE_SEND_MSG_TIP', gameStrings.TEXT_NEWBIEGUIDEPROXY_71),
             'defaultText': self.chatMsg.get((self.sendMsgLv, self.sendMsgIdx), '')}
            return uiUtils.dict2GfxDict(initData, True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_NEWBIE_MSG_INPUT:
            self.hideMsgInput()
        else:
            UIProxy._asWidgetClose(self, widgetId, multiID)

    @ui.scenarioCallFilter()
    def showGuideIcon(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_NEWBIEGUILD_ICON)

    @ui.scenarioCallFilter()
    def show(self):
        pass

    def showLvGuide(self):
        if self.mediator:
            return
        if self.lvMediator:
            self.refreshView()
        else:
            self.refreshIconInfo()
            self.uiAdapter.loadWidget(uiConst.WIDGET_NEWBIE_LV_GUIDE)

    def closeLvGuide(self):
        self.lvMediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NEWBIE_LV_GUIDE)

    def clearGuideIcon(self):
        self.iconMediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NEWBIEGUILD_ICON)
        gameglobal.rds.ui.welfare.refreshInfo()

    def clearWidget(self):
        self.hideMsgInput()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NEWBIE_LV_GUIDE)

    def showMsgInput(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_NEWBIE_MSG_INPUT)

    def hideMsgInput(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NEWBIE_MSG_INPUT)

    def clearAll(self):
        self.lowReward = False
        self.highReward = False
        self.chatMsg = {}
        self.sendMsgLv = 0
        self.sendMsgIdx = 0
        self.sendMsgTitle = ''
        self.lvMediator = None
        self.iconMediator = None

    def setRewardInfo(self, lowReward, highReward):
        self.lowReward = lowReward
        self.highReward = highReward
        if self.highReward:
            self.closeLvGuide()
            self.clearGuideIcon()
        else:
            self.refreshView()

    def checkLvLock(self):
        p = BigWorld.player()
        needCheck = gameglobal.rds.configData.get('enableNoviceBoost', True)
        progressId = SCD.data.get('NOVICE_BOOST_PROGRESS_ID', 10003)
        isServerFinish = p.isServerProgressFinished(progressId)
        if not needCheck or not isServerFinish:
            return
        for key, item in NBCD.data.items():
            lv = item.get('lv', 0)
            if lv == p.lv:
                self.showLvGuide()
                break
        else:
            self.refreshView()

    def onGetCardInfo(self, *arg):
        p = BigWorld.player()
        ret = []
        for key, item in NBCD.data.items():
            data = {}
            data['key'] = key
            data['name'] = item.get('name', '')
            data['shortDesc'] = item.get('shortDesc', '')
            check = True if p.lv >= item.get('lv', 0) else False
            redMcVisible = False
            desText = ''
            if key in (KEY_EXAM_FIRST, KEY_EXAM_SECOND):
                func3 = item.get('fun3')
                if func3:
                    if not self.checkHostId(func3[0][1]):
                        check = False
                        desText = uiUtils.toHtml(gameStrings.TEXT_NEWBIEGUIDEPROXY_172, COLOR_RED)
                    elif not self.checkServerProgressFinished(func3[0][1]):
                        check = False
                        desText = uiUtils.toHtml(NBSTD.data.get(func3[0][1], {}).get('progressDesc', ''), COLOR_RED)
            if not check:
                desText = uiUtils.toHtml(item.get('unlockText', ''), COLOR_RED) if desText == '' else desText
            elif key == KEY_GOLDEN_MISSION:
                if self.lowReward:
                    desText = uiUtils.toHtml(gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187, COLOR_GOLDEN)
                else:
                    desText = uiUtils.toHtml(gameStrings.TEXT_XINMORECORDPROXY_187, COLOR_GREEN)
                    redMcVisible = True
            elif key == KEY_APPRENTICE:
                if not p.hasMentor():
                    desText = uiUtils.toHtml(gameStrings.TEXT_NEWBIEGUIDEPROXY_188, COLOR_GREEN)
                else:
                    desText = uiUtils.toHtml(gameStrings.TEXT_NEWBIEGUIDEPROXY_190, COLOR_GREEN)
            elif key == KEY_DIGION:
                pass
            elif key == KEY_SHI_LIAN:
                if self.isNuLingFinished():
                    desText = uiUtils.toHtml(gameStrings.TEXT_NEWBIEGUIDEPROXY_199, COLOR_GOLDEN)
                else:
                    desText = uiUtils.toHtml(gameStrings.TEXT_NEWBIEGUIDEPROXY_201, COLOR_GREEN)
            elif key in (KEY_EXAM_FIRST, KEY_EXAM_SECOND):
                func3 = item.get('fun3')
                redMcVisible = gameglobal.rds.ui.newbieGuideExam.checkCanFinish(func3[0][1])
                if func3:
                    if gameglobal.rds.ui.newbieGuideExam.fineFinishExam(func3[0][1]):
                        desText = uiUtils.toHtml(gameStrings.TEXT_NEWBIEGUIDEPROXY_207, COLOR_GOLDEN)
                    elif gameglobal.rds.ui.newbieGuideExam.finishExam(func3[0][1]):
                        desText = uiUtils.toHtml(gameStrings.TEXT_NEWBIEGUIDEPROXY_209, COLOR_GOLDEN)
                    elif gameglobal.rds.ui.newbieGuideExam.failExam(func3[0][1]):
                        desText = uiUtils.toHtml(gameStrings.TEXT_CONST_10009, COLOR_GOLDEN)
                    elif gameglobal.rds.ui.newbieGuideExam.needNotExam(func3[0][1]):
                        desText = uiUtils.toHtml(gameStrings.TEXT_NEWBIEGUIDEPROXY_213, COLOR_GOLDEN)
                    else:
                        desText = uiUtils.toHtml(gameStrings.TEXT_GAMETYPES_5472, COLOR_GREEN)
            data['check'] = check
            data['unlockText'] = desText
            data['redMcVisible'] = redMcVisible
            ret.append(data)

        data = {'cardList': ret,
         'maxLv': SCD.data.get('NOVICE_BOOST_MAX_LV', 59),
         'lv': min(p.lv, SCD.data.get('NOVICE_BOOST_MAX_LV', 59)),
         'highReward': self.highReward}
        return uiUtils.dict2GfxDict(data, True)

    def isNuLingFinished(self):
        p = BigWorld.player()
        if hasattr(p, 'importantPlayRecommendInfo'):
            for recomValues in p.importantPlayRecommendInfo.values():
                for fbNo, value, maxValue, _lastEnterDays, _coef in recomValues:
                    if fbNo in (1102, 1250):
                        return value == maxValue

        return False

    def onGetNewbieInfo(self, *arg):
        ret = {}
        ret['name'] = BigWorld.player().realRoleName
        ret['time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        return uiUtils.dict2GfxDict(ret, True)

    def onGetFullLvReward(self, *args):
        BigWorld.player().cell.applyNoviceBoostLevelReward(const.NOVICE_BOOST_LEVEL_REWARD_HIGH_LV)

    def onSendMsg(self, *args):
        msg = unicode2gbk(args[3][0].GetString()).strip()
        p = BigWorld.player()
        if len(msg):
            isNormal, msg = taboo.checkDisbWord(msg)
            if not isNormal:
                p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
                return
            flag, msg = self.uiAdapter.chat._tabooCheck(const.CHAT_CHANNEL_WORLD, msg)
            if not flag:
                p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
                return
            p.cell.chatToWorldForCompanion(self.sendMsgLv, self.sendMsgIdx, uiUtils.htmlToText(msg))
            self.hideMsgInput()
            self.chatMsg[self.sendMsgLv, self.sendMsgIdx] = msg
        else:
            p.showGameMsg(GMDD.data.NEWBIE_WORLD_MSG_EMPTY, ())

    def onShowNewbiLvGuide(self, *arg):
        self.mediator = None
        BigWorld.player().cell.clickNoviceBoostPanel()
        self.uiAdapter.loadWidget(uiConst.WIDGET_NEWBIE_LV_GUIDE)

    @ui.uiEvent(uiConst.WIDGET_NEWBIE_GUIDE, events.EVENT_KEY_DOWN)
    def onKeyYDown(self, event):
        if event.data[0] == keys.KEY_Y:
            self.onShowNewbiLvGuide()
            event.stop()

    def onMinBtnFunc(self, *arg):
        self.closeLvGuide()
        self.uiAdapter.loadWidget(uiConst.WIDGET_NEWBIEGUILD_ICON)

    def onGetButtonInfo(self, *arg):
        key = arg[3][0].GetNumber()
        ret = {}
        ret['goto'] = []
        ret['hit'] = []
        ret['desc'] = ''
        ret['longName'] = ''
        data = NBCD.data.get(key)
        p = BigWorld.player()
        if data:
            check = True if p.lv >= data.get('lv', 0) else False
            func1 = data.get('fun1')
            func2 = data.get('fun2')
            func3 = data.get('fun3')
            desc = data.get('desc', '')
            longName = data.get('longName', '')
            if func1:
                for item in func1:
                    if len(item) == 3:
                        lvMin, lvMax = item[2].get('lv', (0, 100))
                        if p.lv < lvMin or p.lv > lvMax:
                            continue
                    if key == KEY_DIGION:
                        ret['goto'].append((item[0], check and p.yaoliPoint < p.getYaoliMPoint()))
                    elif key == KEY_SHI_LIAN:
                        ret['goto'].append((item[0], check and not self.isNuLingFinished()))
                    else:
                        ret['goto'].append((item[0], check))

            if func2:
                for item in func2:
                    if len(item) == 3:
                        lvMin, lvMax = item[2].get('lv', (0, 100))
                        if p.lv < lvMin or p.lv > lvMax:
                            continue
                    if key == KEY_APPRENTICE:
                        enabled = check and not p.hasMentor()
                    elif key == KEY_SHI_LIAN:
                        enabled = check and not self.isNuLingFinished()
                    elif key == KEY_DIGION:
                        enabled = check and p.yaoliPoint < p.getYaoliMPoint()
                    else:
                        enabled = check
                    ret['hit'].append({'label': item[0],
                     'enabled': enabled})

            if func3:
                for item in func3:
                    if len(item) == 3:
                        lvMin, lvMax = item[2].get('lv', (0, 100))
                        if p.lv < lvMin or p.lv > lvMax:
                            continue
                    if key in (KEY_EXAM_FIRST, KEY_EXAM_SECOND):
                        enabled = check and self._checkExamBtnEnable(item[1])
                        effectVisible = gameglobal.rds.ui.newbieGuideExam.checkCanFinish(item[1]) if enabled else False
                        ret['hit'].append({'label': item[0],
                         'enabled': enabled,
                         'effectVisible': effectVisible,
                         'examInfo': item[1]})

            ret['desc'] = desc
            ret['longName'] = longName
            if key == KEY_GOLDEN_MISSION:
                if p.lv >= SCD.data.get('NOVICE_BOOST_REWARD_LOW_LV', (20, 0))[0]:
                    if self.lowReward:
                        ret['hit'].append({'label': gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187,
                         'enabled': False})
                    else:
                        ret['hit'].append({'label': gameStrings.TEXT_NEWBIEGUIDEPROXY_344,
                         'enabled': True,
                         'effectVisible': True})
                else:
                    ret['hit'].append({'label': gameStrings.TEXT_NEWBIEGUIDEPROXY_344,
                     'enabled': False})
        return uiUtils.dict2GfxDict(ret, True)

    def _checkExamBtnEnable(self, typeId):
        if not self.checkHostId(typeId):
            return False
        if not self.checkServerProgressFinished(typeId):
            return False
        if gameglobal.rds.ui.newbieGuideExam.fineFinishExam(typeId):
            return False
        if gameglobal.rds.ui.newbieGuideExam.finishExam(typeId):
            return False
        if gameglobal.rds.ui.newbieGuideExam.failExam(typeId):
            return False
        return True

    def onSetHitBtnIndex(self, *arg):
        p = BigWorld.player()
        key = int(arg[3][0].GetNumber())
        index = int(arg[3][1].GetNumber())
        lable = unicode2gbk(arg[3][2].GetString())
        if key == KEY_GOLDEN_MISSION:
            p.cell.applyNoviceBoostLevelReward(const.NOVICE_BOOST_LEVEL_REWARD_LOW_LV)
        elif key in (KEY_EXAM_FIRST, KEY_EXAM_SECOND):
            gameglobal.rds.ui.newbieGuideExam.show(index)
        elif p.lv >= SCD.data.get('NEWBIE_SEND_CUSTOM_MSG_LV', 30):
            self.sendMsgIdx = index
            self.sendMsgLv = key
            self.sendMsgTitle = lable
            if not self.chatMsg.get((key, index)):
                msgId = NBCD.data.get(key, {}).get('fun2', ())[index][1]
                self.chatMsg[key, index] = uiUtils.getTextFromGMD(msgId)
            self.hideMsgInput()
            self.showMsgInput()
        else:
            p.cell.chatToWorldForCompanion(key, index, '')

    def onSetGotoBtnIndex(self, *arg):
        p = BigWorld.player()
        key = int(arg[3][0].GetNumber())
        index = int(arg[3][1].GetNumber())
        p.cell.useNoviceBoostTeleport(key, index)

    def onClickIcon(self, *arg):
        self.showLvGuide()

    def canGainAward(self):
        p = BigWorld.player()
        if p.lv >= SCD.data.get('NOVICE_BOOST_MAX_LV', 59) and not self.highReward:
            hasAward = True
        else:
            hasAward = False
        for key, item in NBCD.data.items():
            check = True if p.lv >= item.get('lv', 0) else False
            redMcVisible = False
            if key in (KEY_EXAM_FIRST, KEY_EXAM_SECOND):
                func3 = item.get('fun3')
                if func3:
                    if not self.checkHostId(func3[0][1]):
                        check = False
                    elif not self.checkServerProgressFinished(func3[0][1]):
                        check = False
            if check:
                if key == KEY_GOLDEN_MISSION:
                    if not self.lowReward:
                        redMcVisible = True
                elif key in (KEY_EXAM_FIRST, KEY_EXAM_SECOND):
                    func3 = item.get('fun3')
                    redMcVisible = gameglobal.rds.ui.newbieGuideExam.checkCanFinish(func3[0][1])
            if redMcVisible:
                hasAward = True

        return hasAward

    def refreshIconInfo(self):
        gameglobal.rds.ui.welfare.refreshInfo()
        if self.iconMediator:
            info = {'hasAward': self.canGainAward()}
            self.iconMediator.Invoke('refreshIconInfo', uiUtils.dict2GfxDict(info, True))

    def refreshView(self):
        self.refreshIconInfo()
        if self.lvMediator:
            self.lvMediator.Invoke('refreshView')

    def checkHostId(self, key):
        includeHosts = NBSTD.data.get(key, {}).get('includeHosts', ())
        excludeHosts = NBSTD.data.get(key, {}).get('excludeHosts', ())
        if includeHosts:
            return utils.getHostId() in includeHosts
        if excludeHosts:
            return utils.getHostId() not in excludeHosts
        return True

    def checkServerProgressFinished(self, key):
        progressId = NBSTD.data.get(key, {}).get('progressId')
        if progressId:
            return BigWorld.player().isServerProgressFinished(progressId)
        return True
