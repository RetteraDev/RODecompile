#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tutorial.o
from gamestrings import gameStrings
import cPickle
import zlib
import weakref
import re
import BigWorld
import gameglobal
import const
import utils
import formula
import clientcom
import datetime
import gamelog
import gametypes
import gameglobal
from callbackHelper import Functor
from gameclass import Singleton
from guis import hotkey as HK
from guis import uiConst
from helpers.scenario import Scenario
from helpers.charRes import transDummyBodyType
from data import tutorial_module_data as TMD
from data import tutorial_steps_data as TID
from data import tutorial_config_data as TCD
from data import tutorial_slow_time_data as TSTD
CBC_LOGIN_TRIGGER = 1
CBC_KILL_MONSTER = 2
CBC_LV = 3
CBC_ACCEPT_QUEST = 4
CBC_COMPLETE_QUEST_CONDITION = 5
CBC_FINISH_QUEST = 6
CBC_ENTER_FUBEN = 7
CBC_ENTER_TRAP = 8
CBC_MONSTER_DYING = 9
CBC_QUEST_ITEM = 10
CBC_OPERATION_SELECT = 11
CBC_HP_PERCENT = 12
CBC_USE_SKILL = 13
CBC_FINISH_ACTIVITY = 14
CBC_GET_ITEM = 15
CBC_EQUIP_REPAIR = 16
CBC_YAO_HUA = 17
CBC_SET_EQUIP = 18
CBC_CHUNK_NAME_TRIGGER = 19
CBC_QING_GONG_STATE_TRIGGER = 20
CBC_FULL_EXP = 21
CBC_GET_MAIL = 22
CBC_LOGIN_DAILY_TRIGGER = 23
CBC_PLAYER_DYE_TRIGGER = 24
CBC_PLAYER_SHIHUN_TRIGGER = 25
CBC_GET_STATE = 26
CBC_MALL_SCORE = 27
CBC_GET_TITLE = 28
CBC_BREAK_JINGJIE = 29
CBC_OPEN_DAOHENG_SLOT = 30
CBC_GET_FREEZE_CASH = 31
CBC_START_CCBOX = 32
CBC_APPRENTICE_GRADUATE = 33
CBC_BE_APPRENTICE = 34
CBC_GUILD_ACTIVE = 35
CBC_BE_GUILD_HAS_SPACE = 36
CBC_LOADED_UI = 37
CBC_IN_CLAN_WAR = 38
CBC_GUILD_MEMBER_SKILL = 39
CBC_IN_FLY = 40
CBC_GAME_LOADED = 41
CBC_YMF_SCORE = 42
CBC_LEAVE_MAP = 43
CBC_UNLOAD_WIDGET = 44
CBC_CHECK_AVATAR = 45
CBC_FINISH_CLUE = 46
CBC_OPEN_THEATER = 47
CBC_USE_ITEM = 48
CBC_FINISH_FB = 49
CBC_EXCITEMENT = 50
CBC_TEAM = 51
CBC_GET_SPECIFIC_TITLE = 52
CBC_MULTI_CARRIER_READY_ENOUGH = 53
CBC_LOADED_SWF = 54
CBC_LOADED_UI_IN_WING_WORLD = 55
IEC_MOUSE_LEFTBTN_DOWN = 1
IEC_MOUSE_RIGHTBTN_DOWN = 2
IEC_PRESS_KEY = 3
IEC_CHECK_YAW = 4
IEC_CHECK_MOVE = 5
IEC_IMMEDIATELY = 6
IEC_DELAY_TIME = 7
IEC_FINISH_FUBEN = 8
IEC_MOUSE_RIGHTBTN_DOWN_DYNAMIC = 9
IEC_CHECK_STATE = 10
IEC_MOUSE_LEFTBTN_DOWN_DYNAMIC = 11
IEC_CHECK_ACTION = 12
IEC_CHECK_FINISH_QUEST = 13
IEC_CHECK_COMPLETE_QUEST = 14
IEC_CHECK_LOAD_WIDGET = 15
IEC_CHECK_USE_ITEM = 16
IEC_CHECK_USE_SKILL = 17
IEC_CHECK_USE_COMMON_SKILL = 18
IGD_SHOW_NO_ARROWS = 1
IGD_SHOW_ARROWS = 2
IGD_DO_NOTHING = 3
IGD_SHOW_WIDGET = 4
IGD_SHOW_ARROWS_DYNAMIC_ITEM = 5
IGD_SHOW_SCENARIO = 6
IGD_SHOW_ARROWS_DYNAMIC_TAB = 7
IGD_SHOW_USETIPS = 8
IGD_SHOW_INTRODUCER = 9
IGD_SHOW_FEED_BACK = 10
IGD_SHOW_QTE = 11
IGD_SHOW_UI = 12
IGD_TOPBAR_TIP = 13
IGD_SHOW_TUTORQTE = 14
IGD_SHOW_PIC = 15
TUTORIAL_TYPE_2 = 2
ARG_SOUND_INDEX = 4
TIME_OUT_FAIL = 0
TIME_OUT_SUCCESS = 1
TUTORIAL_SUCCESS_ID = 12
TUTORIAL_FAIL_ID = 13
STEP_PRE_CHECK_WIDGET_LOAD = 1

def isCloseBtn(btnName, componentId):
    if btnName[0] + btnName[1] == 'closeBtn' + str(componentId):
        return True
    return False


def btnNameCmp(btnName, realBtnName):
    for index, value in enumerate(btnName):
        if value != realBtnName[index] and value != 'None':
            return False

    return True


class IntroEndChecker(object):

    def __init__(self, owner, itemInfo, index):
        self.owner = weakref.ref(owner)
        self.isMyEnd = False
        self.needCheckTimer = False
        self.checkTimerHandle = None
        self.needTimeout = True
        self.timeoutValue = itemInfo['timeout']
        self.timeoutType = itemInfo.get('timeoutType', TIME_OUT_FAIL)
        self.timeoutHandle = None

    def isEnd(self):
        return self.isMyEnd

    def onMouseLeftBtnUp(self, realBtnName):
        pass

    def onMouseRightBtnUp(self, realBtnName):
        pass

    def onKeyEvent(self, key, mods):
        pass

    def onFinishedQuest(self, questId):
        pass

    def onCompletedQuest(self, questId):
        pass

    def onLoadWidget(self, widgetId):
        pass

    def onUseItemEndCheck(self, itemId):
        pass

    def onUseSkillEndCheck(self, skillId):
        pass

    def onUseCommonSkillEndCheck(self, skillId):
        pass

    def onTimer(self):
        pass

    def onTimeout(self):
        self.timeoutHandle = None
        owner = self.owner()
        if self.timeoutType == TIME_OUT_FAIL:
            if owner:
                owner.goFail()
        else:
            self.isMyEnd = True

    def onTimerWrapper(self):
        self.onTimer()
        self.checkTimerHandle = BigWorld.callback(0.1, self.onTimerWrapper)

    def play(self):
        if self.needCheckTimer:
            self.checkTimerHandle = BigWorld.callback(0.1, self.onTimerWrapper)
        if self.needTimeout:
            self.timeoutHandle = BigWorld.callback(self.timeoutValue, self.onTimeout)

    def stop(self):
        if self.checkTimerHandle:
            BigWorld.cancelCallback(self.checkTimerHandle)
            self.checkTimerHandle = None
        if self.timeoutHandle:
            BigWorld.cancelCallback(self.timeoutHandle)
            self.timeoutHandle = None

    def onFinishFbId(self, fubenId):
        pass

    def onCheckQingGongState(self, stateId):
        pass

    def onCheckAction(self, actionId):
        pass


class IntroEndCheckerMLB(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerMLB, self).__init__(owner, itemInfo, index)
        self.btnName = itemInfo['endChecks'][index][1]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId) or btnNameCmp(self.btnName, realBtnName):
            self.isMyEnd = True

    def onMouseRightBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True


class IntroEndCheckerMLBDynamic(IntroEndCheckerMLB):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerMLBDynamic, self).__init__(owner, itemInfo, index)
        self.btnName = self._genBtnName(list(itemInfo['endChecks'][index][1]))

    def _genBtnName(self, btnName):
        if hasattr(self.owner().op, 'posIndex'):
            posIndex = self.owner().op.posIndex
            if posIndex != -1:
                btnName[0] = btnName[0] + str(posIndex)
        else:
            gamelog.error('hjx debug tutorial IntroEndCheckerMLBDynamic#_genBtnName: type error, type must be IGD_SHOW_ARROWS_DYNAMIC(5)')
        return btnName


class IntroEndCheckerMRB(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerMRB, self).__init__(owner, itemInfo, index)
        self.btnName = itemInfo['endChecks'][index][1]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True

    def onMouseRightBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId) or btnNameCmp(self.btnName, realBtnName):
            self.isMyEnd = True


class IntroEndCheckerMRBDynamic(IntroEndCheckerMRB):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerMRBDynamic, self).__init__(owner, itemInfo, index)
        self.btnName = self._genBtnName(list(itemInfo['endChecks'][index][1]))

    def _genBtnName(self, btnName):
        if hasattr(self.owner().op, 'posIndex'):
            posIndex = self.owner().op.posIndex
            if posIndex != -1:
                btnName[0] = btnName[0] + str(posIndex)
        else:
            gamelog.error('hjx debug tutorial _genBtnName: type error, type must be IGD_SHOW_ARROWS_DYNAMIC(5)')
        return btnName


class IntroEndCheckerImmediately(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerImmediately, self).__init__(owner, itemInfo, index)
        self.isMyEnd = True
        self.needTimeout = False


class IntroEndCheckerKey(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerKey, self).__init__(owner, itemInfo, index)
        self.key = itemInfo['endChecks'][index][1][0]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True

    def onKeyEvent(self, key, mods):
        key = HK.keyDef(key, 1, mods)
        if key == HK.HKM[self.key]:
            self.isMyEnd = True


class IntroEndCheckerDelay(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerDelay, self).__init__(owner, itemInfo, index)
        self.delayTime = itemInfo['endChecks'][index][1]
        self.needTimeout = False

    def onTimer(self):
        self.isMyEnd = True
        owner = self.owner()
        if owner:
            owner.checkNext()

    def play(self):
        self.checkTimerHandle = BigWorld.callback(self.delayTime, self.onTimer)

    def stop(self):
        pass


class IntroEndCheckerFINFB(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerFINFB, self).__init__(owner, itemInfo, index)
        self.needTimeout = False
        self.fubenId = itemInfo['endChecks'][index][1]

    def onFinishFbId(self, fubenId):
        if fubenId == self.fubenId:
            self.isMyEnd = True


class IntroEndCheckerState(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerState, self).__init__(owner, itemInfo, index)
        self.stateId = itemInfo['endChecks'][index][1]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True

    def onCheckQingGongState(self, stateId):
        if stateId == self.stateId:
            self.isMyEnd = True


class IntroEndCheckerAction(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerAction, self).__init__(owner, itemInfo, index)
        self.actionId = itemInfo['endChecks'][index][1]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True

    def onCheckAction(self, actionId):
        if actionId == self.actionId:
            self.isMyEnd = True


class IntroEndCheckerFinishQuest(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerFinishQuest, self).__init__(owner, itemInfo, index)
        self.questId = itemInfo['endChecks'][index][1]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True

    def onFinishedQuest(self, questId):
        if questId in self.questId:
            self.isMyEnd = True


class IntroEndCheckerCompleteQuest(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerCompleteQuest, self).__init__(owner, itemInfo, index)
        self.questId = itemInfo['endChecks'][index][1]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True

    def onCompletedQuest(self, questId):
        if questId in self.questId:
            self.isMyEnd = True


class IntroEndCheckerLoadWidget(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerLoadWidget, self).__init__(owner, itemInfo, index)
        self.widgetId = itemInfo['endChecks'][index][1]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True

    def onLoadWidget(self, widgetId):
        if widgetId == self.widgetId:
            self.isMyEnd = True


class IntroEndCheckerUseItem(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerUseItem, self).__init__(owner, itemInfo, index)
        self.itemId = itemInfo['endChecks'][index][1]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True

    def onUseItemEndCheck(self, itemId):
        if itemId in self.itemId:
            self.isMyEnd = True


class IntroEndCheckerUseSkill(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerUseSkill, self).__init__(owner, itemInfo, index)
        self.skillIds = itemInfo['endChecks'][index][1]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True

    def onUseSkillEndCheck(self, skillId):
        if skillId in self.skillIds:
            self.isMyEnd = True


class IntroEndCheckerUseCommonSkill(IntroEndChecker):

    def __init__(self, owner, itemInfo, index):
        super(IntroEndCheckerUseCommonSkill, self).__init__(owner, itemInfo, index)
        self.skillIds = itemInfo['endChecks'][index][1]

    def onMouseLeftBtnUp(self, realBtnName):
        owner = self.owner()
        componentId = owner.chain().componentId
        if isCloseBtn(realBtnName, componentId):
            self.isMyEnd = True

    def onUseCommonSkillEndCheck(self, skillId):
        if skillId in self.skillIds:
            self.isMyEnd = True


class IntroGuid(object):

    def __init__(self, itemInfo, componentId):
        self.showType = itemInfo['type']
        self.msg = itemInfo['msg']
        self.widgetArg = list(itemInfo['arg'])
        self.componentId = componentId
        self.nextPage = False
        self.delayCallbackId = 0
        self.delayTime = itemInfo.get('delayTime', 0)
        self.soundId = 0
        self.noStopSound = itemInfo.get('noStopSound', 0)

    def play(self):
        if self.delayCallbackId > 0:
            return
        if self.delayTime:
            self.delayCallbackId = BigWorld.callback(self.delayTime, self.doPlay)
        else:
            self.doPlay()

    def doPlay(self):
        pass

    def stop(self, success = True):
        if self.delayCallbackId:
            BigWorld.cancelCallback(self.delayCallbackId)
            self.delayCallbackId = 0
        if self.soundId and not self.noStopSound:
            gameglobal.rds.sound.stopSound(self.soundId)


class IntroGuidShowWidget(IntroGuid):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidShowWidget, self).__init__(itemInfo, componentId)
        if len(self.widgetArg) > ARG_SOUND_INDEX:
            self.soundId = self.widgetArg[ARG_SOUND_INDEX]
        else:
            self.soundId = 0

    def doPlay(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        gameglobal.rds.ui._genarateWidgetData(self.showType, self.widgetArg, self.msg)
        gameglobal.rds.ui.openTutorialWidget(self.componentId)
        if self.widgetArg and type(self.widgetArg) is list or type(self.widgetArg) is tuple:
            if int(self.widgetArg[0]) == uiConst.WIDGET_NEW_GUIDER_OPERATION:
                gameglobal.rds.ui.showCursorForActionPhysics()
        if self.soundId:
            gameglobal.rds.sound.playSound(self.soundId)

    def stop(self, success = True):
        super(IntroGuidShowWidget, self).stop(success)
        gameglobal.rds.ui.closeTutorialWidget(self.componentId)


class IntroGuidUseTips(IntroGuid):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidUseTips, self).__init__(itemInfo, componentId)
        if len(self.widgetArg) > ARG_SOUND_INDEX:
            self.soundId = self.widgetArg[ARG_SOUND_INDEX]
        else:
            self.soundId = 0

    def doPlay(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        gameglobal.rds.ui.useTips.show(self.msg)
        if self.soundId:
            gameglobal.rds.sound.playSound(self.soundId)

    def stop(self, success = True):
        super(IntroGuidUseTips, self).stop(success)
        gameglobal.rds.ui.useTips.hide()


class IntroGuidQte(IntroGuid):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidQte, self).__init__(itemInfo, componentId)
        self.timeOut = itemInfo.get('timeout', 2)
        if len(self.widgetArg) > ARG_SOUND_INDEX:
            self.soundId = self.widgetArg[ARG_SOUND_INDEX]
        else:
            self.soundId = 0

    def doPlay(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        gameglobal.rds.ui.exactQte.setData(self.msg, self.timeOut)
        gameglobal.rds.ui.exactQte.show(0)
        if self.soundId:
            gameglobal.rds.sound.playSound(self.soundId)

    def stop(self, success = True):
        super(IntroGuidQte, self).stop(success)
        gameglobal.rds.ui.exactQte.onTutorialEnd(success)


class IntroTutorialQte(IntroGuid):

    def __init__(self, itemInfo, componentId):
        super(IntroTutorialQte, self).__init__(itemInfo, componentId)
        self.timeOut = itemInfo.get('timeout', 2)
        if len(self.widgetArg) > ARG_SOUND_INDEX:
            self.soundId = self.widgetArg[ARG_SOUND_INDEX]
        else:
            self.soundId = 0

    def doPlay(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        gameglobal.rds.ui.tutorialQte.setData(self.msg, self.timeOut)
        gameglobal.rds.ui.tutorialQte.show(0)
        if self.soundId:
            gameglobal.rds.sound.playSound(self.soundId)

    def stop(self, success = True):
        super(IntroTutorialQte, self).stop(success)
        gameglobal.rds.ui.tutorialQte.onTutorialEnd(success)


class IntroShowUI(IntroGuid):

    def __init__(self, itemInfo, componentId):
        super(IntroShowUI, self).__init__(itemInfo, componentId)
        self.module, self.funcName = self.widgetArg[0].split('.')
        self.fucnArgs = self.widgetArg[1]
        self.closeFunc = self.widgetArg[6]
        if len(self.widgetArg) > ARG_SOUND_INDEX:
            self.soundId = self.widgetArg[ARG_SOUND_INDEX]
        else:
            self.soundId = 0

    def doPlay(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        module = getattr(gameglobal.rds.ui, self.module)
        funcName = getattr(module, self.funcName)
        if funcName:
            funcName(*self.fucnArgs)
        if self.soundId:
            gameglobal.rds.sound.playSound(self.soundId)

    def stop(self, success = True):
        super(IntroShowUI, self).stop(success)
        module = getattr(gameglobal.rds.ui, self.module)
        if self.closeFunc:
            funcName = getattr(module, self.closeFunc)
        else:
            funcName = getattr(module, 'close')
        if funcName:
            funcName()


class IntroGuidIntroducer(IntroGuid):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidIntroducer, self).__init__(itemInfo, componentId)
        if len(self.widgetArg) > ARG_SOUND_INDEX:
            self.soundId = self.widgetArg[ARG_SOUND_INDEX]
        else:
            self.soundId = 0

    def doPlay(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        gameglobal.rds.ui.introducer.show(self.widgetArg)
        if self.soundId:
            gameglobal.rds.sound.playSound(self.soundId)

    def stop(self, success = True):
        super(IntroGuidIntroducer, self).stop(success)
        gameglobal.rds.ui.introducer.hideIntroducer()


class IntroGuidShowFeedback(IntroGuid):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidShowFeedback, self).__init__(itemInfo, componentId)
        self.componentId = componentId
        if len(self.widgetArg) > ARG_SOUND_INDEX:
            self.soundId = self.widgetArg[ARG_SOUND_INDEX]
        else:
            self.soundId = 0

    def doPlay(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        gameglobal.rds.ui.yingXiaoFeedback.showPushMessage(int(self.widgetArg[0]), self.componentId)
        if self.soundId:
            gameglobal.rds.sound.playSound(self.soundId)

    def stop(self, success = True):
        super(IntroGuidShowFeedback, self).stop(success)
        gameglobal.rds.ui.yingXiaoFeedback.removePushMsg(feedbackId=int(self.widgetArg[0]), comId=self.componentId)


class IntroGuidShowText(IntroGuidShowWidget):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidShowText, self).__init__(itemInfo, componentId)
        self.generateStr()

    def _formatstr(self, m):
        return m.group(1) + "<font color = \'" + m.group(2) + "\'>" + m.group(3) + '</font>'

    def generateStr(self):
        try:
            reg = re.compile('(.*?)\\[(#[a-fA-F0-9]{6})](.+?)\\[/#\\]', re.DOTALL)
            self.msg = reg.sub(self._formatstr, self.msg)
        except:
            gamelog.error('hjx debug tutorial format string error!')


class IntroTopbar(IntroGuidShowText):

    def __init__(self, itemInfo, componentId):
        super(IntroTopbar, self).__init__(itemInfo, componentId)
        if len(self.widgetArg) > ARG_SOUND_INDEX:
            self.soundId = self.widgetArg[ARG_SOUND_INDEX]
        else:
            self.soundId = 0

    def doPlay(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        gameglobal.rds.ui.topBar.addTutorialTip(self.widgetArg, self.msg)
        if self.soundId:
            gameglobal.rds.sound.playSound(self.soundId)

    def stop(self, success = True):
        super(IntroTopbar, self).stop(success)
        gameglobal.rds.ui.topBar.removeTutorialTip()


class IntroGuidShowNoArrow(IntroGuidShowText):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidShowNoArrow, self).__init__(itemInfo, componentId)


class IntroGuidShowArrow(IntroGuidShowText):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidShowArrow, self).__init__(itemInfo, componentId)


class IntroGuidPic(IntroGuidShowText):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidPic, self).__init__(itemInfo, componentId)

    def doPlay(self):
        gameglobal.rds.ui._genaratePicWidgetData(self.showType, self.widgetArg, self.msg)
        gameglobal.rds.ui.openPicTutorialWidget(self.componentId)


class IntroGuidArrowDynamic(IntroGuidShowArrow):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidArrowDynamic, self).__init__(itemInfo, componentId)
        self.showType = TUTORIAL_TYPE_2
        self.posIndex = -1
        if self.genArrowPosition():
            self.isFinded = True
        else:
            self.isFinded = False

    def genArrowPosition(self):
        raise NotImplementedError

    def doPlay(self):
        if self.isFinded:
            gameglobal.rds.ui._genarateWidgetData(self.showType, self.widgetArg, self.msg)
            gameglobal.rds.ui.openTutorialWidget(self.componentId)
        else:
            gamelog.error('hjx debug tutorial error in IntroGuidArrowDynamic:%d not in the inv', self.widgetArg[1][0])


class IntroGuidArrowDynamicItem(IntroGuidArrowDynamic):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidArrowDynamicItem, self).__init__(itemInfo, componentId)

    def genArrowPosition(self):
        invetory = getattr(BigWorld.player(), 'inv', None)
        self.widgetArg[1] = list(self.widgetArg[1])
        if invetory:
            for itemId in self.widgetArg[1][0]:
                page, pos = invetory.findItemInPages(itemId, includeExpired=True, includeLatch=True, includeShihun=True)
                if page > 0:
                    self.nextPage = True
                INV_ITEM_START_X = TCD.data.get('INV_ITEM_START_X', 10)
                INV_ITEM_START_Y = TCD.data.get('INV_ITEM_START_Y', 88)
                GRID_HEIGHT = TCD.data.get('GRID_HEIGHT', 47)
                GRID_WIDTH = TCD.data.get('GRID_WIDTH', 46)
                GRID_NUM = TCD.data.get('GRID_NUM', 7)
                if page != const.CONT_NO_PAGE:
                    self.posIndex = pos
                    self.widgetArg[1][0] = INV_ITEM_START_X + pos % GRID_NUM * GRID_WIDTH + GRID_WIDTH / 2
                    self.widgetArg[1][1] = INV_ITEM_START_Y + pos / GRID_NUM * GRID_HEIGHT
                    return True

            return False
        else:
            return


class IntroGuidArrowDynamicTab(IntroGuidArrowDynamic):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidArrowDynamicTab, self).__init__(itemInfo, componentId)

    def _calcWidth(self, tabWidthList, page):
        width = 0
        for index in xrange(page):
            width += tabWidthList[index]

        return width

    def genArrowPosition(self):
        invetory = getattr(BigWorld.player(), 'inv', None)
        self.widgetArg[1] = list(self.widgetArg[1])
        if invetory:
            for itemId in self.widgetArg[1][0]:
                page, pos = invetory.findItemInPages(itemId, includeExpired=True, includeLatch=True, includeShihun=True)
                INV_TAB_START_X = TCD.data.get('INV_TAB_START_X', 11)
                INV_TAB_START_Y = TCD.data.get('INV_TAB_START_Y', 42)
                TAB_WIDTH = TCD.data.get('TAB_WIDTH', [66,
                 45,
                 45,
                 45,
                 45])
                if page != const.CONT_NO_PAGE:
                    self.posIndex = page + 1
                    self.widgetArg[1][0] = INV_TAB_START_X + self._calcWidth(TAB_WIDTH, page) + TAB_WIDTH[page] / 2
                    self.widgetArg[1][1] = INV_TAB_START_Y
                    return True

            return False
        else:
            return


class IntroGuidPlayScenario(IntroGuid):

    def __init__(self, itemInfo, componentId):
        super(IntroGuidPlayScenario, self).__init__(itemInfo, componentId)
        self.slowTimeCallbacks = []
        self.slowTimeStage = 0

    def doPlay(self):
        scen = Scenario.getInstanceInPlay()
        scen.loadScript(self.widgetArg[0], True)
        if self.widgetArg[1]:
            stages = self.widgetArg[1]
            if stages:
                self.playSlowStage(scen, stages[0])
        scen.play()

    def playSlowStage(self, scen, stage):
        gameStrings.TEXT_TUTORIAL_934
        stageData = TSTD.data.get(stage, {})
        if stageData:
            steps = stageData.get('steps', ())
            l = len(steps)
            endIndex = -1
            isEnd = False
            for i in xrange(l - 1, -1, -1):
                step = steps[i]
                if step[-1] and endIndex == -1:
                    endIndex = i
                if i == endIndex:
                    isEnd = True
                else:
                    isEnd = False
                scen.addTutorialEvent(step[0], Functor(self.pauseScenario, step[1:], isEnd), bool(step[-1]))

    def pauseScenario(self, info, isEnd):
        fadeIn, fadeOut, rate, componentId = info
        BigWorld.setParticleFrameRateMagnitude(rate, fadeIn)
        BigWorld.setActionFrameRateMagnitude(rate, fadeIn)
        if componentId:
            gameglobal.rds.tutorial.startComponent(componentId, Functor(self.restoreScenario, fadeOut, isEnd))

    def restoreScenario(self, fadeOut, isEnd, success):
        BigWorld.setParticleFrameRateMagnitude(1, fadeOut)
        BigWorld.setActionFrameRateMagnitude(1, fadeOut)
        scen = Scenario.getInstanceInPlay()
        scen.continuePlay(isEnd, success)

    def stop(self, success = True):
        super(IntroGuidPlayScenario, self).stop(success)
        scen = Scenario.getInstanceInPlay()
        name = '%s%s' % (scen.PREFIX_PATH_NAME, self.widgetArg[0])
        if gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_END and scen.name == name:
            scen.stopPlay()
        BigWorld.setParticleFrameRateMagnitude(1, 0)
        BigWorld.setActionFrameRateMagnitude(1, 0)


class IntroPlayer(object):
    OP_2_CLASS = {IGD_SHOW_NO_ARROWS: IntroGuidShowNoArrow,
     IGD_SHOW_ARROWS: IntroGuidShowArrow,
     IGD_DO_NOTHING: IntroGuid,
     IGD_SHOW_WIDGET: IntroGuidShowWidget,
     IGD_SHOW_ARROWS_DYNAMIC_ITEM: IntroGuidArrowDynamicItem,
     IGD_SHOW_SCENARIO: IntroGuidPlayScenario,
     IGD_SHOW_ARROWS_DYNAMIC_TAB: IntroGuidArrowDynamicTab,
     IGD_SHOW_USETIPS: IntroGuidUseTips,
     IGD_SHOW_INTRODUCER: IntroGuidIntroducer,
     IGD_SHOW_FEED_BACK: IntroGuidShowFeedback,
     IGD_SHOW_QTE: IntroGuidQte,
     IGD_SHOW_UI: IntroShowUI,
     IGD_TOPBAR_TIP: IntroTopbar,
     IGD_SHOW_TUTORQTE: IntroTutorialQte,
     IGD_SHOW_PIC: IntroGuidPic}
    EC_2_CLASS = {IEC_MOUSE_LEFTBTN_DOWN: IntroEndCheckerMLB,
     IEC_MOUSE_RIGHTBTN_DOWN: IntroEndCheckerMRB,
     IEC_IMMEDIATELY: IntroEndCheckerImmediately,
     IEC_PRESS_KEY: IntroEndCheckerKey,
     IEC_DELAY_TIME: IntroEndCheckerDelay,
     IEC_FINISH_FUBEN: IntroEndCheckerFINFB,
     IEC_MOUSE_RIGHTBTN_DOWN_DYNAMIC: IntroEndCheckerMRBDynamic,
     IEC_CHECK_STATE: IntroEndCheckerState,
     IEC_MOUSE_LEFTBTN_DOWN_DYNAMIC: IntroEndCheckerMLBDynamic,
     IEC_CHECK_ACTION: IntroEndCheckerAction,
     IEC_CHECK_FINISH_QUEST: IntroEndCheckerFinishQuest,
     IEC_CHECK_COMPLETE_QUEST: IntroEndCheckerCompleteQuest,
     IEC_CHECK_LOAD_WIDGET: IntroEndCheckerLoadWidget,
     IEC_CHECK_USE_ITEM: IntroEndCheckerUseItem,
     IEC_CHECK_USE_SKILL: IntroEndCheckerUseSkill,
     IEC_CHECK_USE_COMMON_SKILL: IntroEndCheckerUseCommonSkill}

    def __init__(self, chain, itemInfo):
        self.op = self.OP_2_CLASS[itemInfo['type']](itemInfo, chain.componentId)
        self.stepInfo = itemInfo
        self.ecs = []
        self.isEndForcely = False
        if itemInfo.has_key('endChecks') and itemInfo['endChecks']:
            for index, v in enumerate(itemInfo['endChecks']):
                if len(v) == 2:
                    cls = self.EC_2_CLASS[v[0]]
                    if cls:
                        self.ecs.append(cls(self, itemInfo, index))

        self.chain = weakref.ref(chain)

    def checkNext(self):
        chain = self.chain()
        if chain:
            chain.checkNext()

    def goFail(self):
        chain = self.chain()
        if chain:
            chain.goFail()

    def isEnd(self):
        if self.isEndForcely:
            return True
        for ec in self.ecs:
            if ec.isEnd():
                return True

        return False

    def onMouseLeftBtnUp(self, btnName):
        for ec in self.ecs:
            ec.onMouseLeftBtnUp(btnName)

    def onMouseRightBtnUp(self, btnName):
        for ec in self.ecs:
            ec.onMouseRightBtnUp(btnName)

    def onFinishedQuest(self, questId):
        for ec in self.ecs:
            ec.onFinishedQuest(questId)

    def onCompletedQuest(self, questId):
        for ec in self.ecs:
            ec.onCompletedQuest(questId)

    def onLoadWidget(self, widgetId):
        for ec in self.ecs:
            ec.onLoadWidget(widgetId)

    def onUseItemEndCheck(self, itemId):
        for ec in self.ecs:
            ec.onUseItemEndCheck(itemId)

    def onUseSkillEndCheck(self, skillId):
        for ec in self.ecs:
            ec.onUseSkillEndCheck(skillId)

    def onUseCommonSkillEndCheck(self, skillId):
        for ec in self.ecs:
            ec.onUseCommonSkillEndCheck(skillId)

    def onFinishFbId(self, fubenId):
        for ec in self.ecs:
            ec.onFinishFbId(fubenId)

    def onCheckQingGongState(self, stateId):
        for ec in self.ecs:
            ec.onCheckQingGongState(stateId)

    def onCheckAction(self, actionId):
        for ec in self.ecs:
            ec.onCheckAction(actionId)

    def onKeyEvent(self, key, mods):
        for ec in self.ecs:
            ec.onKeyEvent(key, mods)

    def play(self):
        self.op.play()
        for ec in self.ecs:
            ec.play()

    def stop(self, success = True):
        self.op.stop(success)
        for ec in self.ecs:
            ec.stop()


class IntroChain(object):

    def __init__(self, owner, componentId, itemIdList):
        self.componentId = componentId
        self.owner = weakref.ref(owner)
        self.staringNext = False
        self.curr = -1
        self.players = []
        self.isKeySensitive = TMD.data.get(componentId).get('keySensitive', 0)
        for itemId in itemIdList:
            if TID.data.has_key(itemId):
                player = IntroPlayer(self, TID.data[itemId])
                self.players.append(player)

    def isSkipCurStep(self):
        if self.curr + 2 >= len(self.players):
            return False
        elif len(self.players) == 1:
            return False
        nextStep = self.players[self.curr + 2]
        if isinstance(nextStep.op, IntroGuidArrowDynamicItem) and not nextStep.op.nextPage:
            return True
        else:
            return False

    def isComplete(self):
        if self.curr + 1 >= len(self.players):
            return False
        else:
            curStep = self.players[self.curr + 1]
            if curStep.stepInfo['type'] == IGD_SHOW_ARROWS:
                stepPreCheckType = curStep.stepInfo.get('preCheckType', None)
                if not stepPreCheckType:
                    return False
                widgetId = curStep.stepInfo['preCheckCond']
                isWidgetLoaded = gameglobal.rds.ui.isWidgetLoaded(widgetId)
                isWidgetLoading = gameglobal.rds.ui.isWidgetLoading(widgetId)
                if isWidgetLoaded or isWidgetLoading:
                    return True
                else:
                    return False
            return False

    def setPlayerEnd(self, index):
        if index >= len(self.players):
            return
        player = self.players[index]
        player.isEndForcely = True

    def playNext(self):
        self.staringNext = False
        if self.isComplete():
            self.curr += 1
            self.setPlayerEnd(self.curr)
            self.checkNext()
            return
        if self.isSkipCurStep():
            self.curr += 1
            self.setPlayerEnd(self.curr)
            self.checkNext()
            return
        self.curr += 1
        if self.curr >= len(self.players):
            self.curr = -1
            owner = self.owner()
            if owner:
                owner.chainFinish(self)
            return
        player = self.players[self.curr]
        player.play()
        self.checkNext()

    def getCurrPlayer(self):
        if self.curr == -1:
            return None
        else:
            return self.players[self.curr]

    def checkNext(self):
        if self.staringNext:
            return
        player = self.getCurrPlayer()
        if player and player.isEnd():
            player.stop(True)
            self.staringNext = True
            BigWorld.callback(0.6, self.playNext)

    def checkAndPlayNext(self):
        if self.staringNext:
            return
        player = self.getCurrPlayer()
        if player and player.isEnd():
            player.stop(True)
            self.staringNext = True
            self.playNext()

    def goFail(self):
        player = self.getCurrPlayer()
        player.stop(False)
        owner = self.owner()
        if owner:
            owner.chainFail(self)

    def forceStop(self):
        player = self.getCurrPlayer()
        if player:
            player.stop(False)

    def onMouseLeftBtnUp(self, btnName):
        player = self.getCurrPlayer()
        if player:
            player.onMouseLeftBtnUp(btnName)
            self.checkNext()

    def onMouseRightBtnUp(self, btnName):
        player = self.getCurrPlayer()
        if player:
            player.onMouseRightBtnUp(btnName)
            self.checkNext()

    def onKeyEvent(self, key, mods):
        player = self.getCurrPlayer()
        if player:
            player.onKeyEvent(key, mods)
            if self.isKeySensitive:
                self.checkAndPlayNext()
            else:
                self.checkNext()

    def onFinishedQuest(self, questId):
        player = self.getCurrPlayer()
        if player:
            player.onFinishedQuest(questId)
            self.checkNext()

    def onCompletedQuest(self, questId):
        player = self.getCurrPlayer()
        if player:
            player.onCompletedQuest(questId)
            self.checkNext()

    def onLoadWidget(self, widgetId):
        player = self.getCurrPlayer()
        if player:
            player.onLoadWidget(widgetId)
            self.checkNext()

    def onUseItemEndCheck(self, itemId):
        player = self.getCurrPlayer()
        if player:
            player.onUseItemEndCheck(itemId)
            self.checkNext()

    def onUseSkillEndCheck(self, skillId):
        player = self.getCurrPlayer()
        if player:
            player.onUseSkillEndCheck(skillId)
            self.checkNext()

    def onUseCommonSkillEndCheck(self, skillId):
        player = self.getCurrPlayer()
        if player:
            player.onUseCommonSkillEndCheck(skillId)
            self.checkNext()

    def onFinishFbId(self, fubenId):
        player = self.getCurrPlayer()
        if player:
            player.onFinishFbId(fubenId)
            self.checkNext()

    def onCheckQingGongState(self, stateId):
        player = self.getCurrPlayer()
        if player:
            player.onCheckQingGongState(stateId)
            self.checkNext()

    def onCheckAction(self, actionId):
        player = self.getCurrPlayer()
        if player:
            player.onCheckAction(actionId)
            self.checkNext()


class ComponentSet(object):

    def __init__(self, manager):
        self.manager = weakref.ref(manager)
        self.reset()

    def reset(self):
        chainList = getattr(self, 'runningChains', None)
        if chainList:
            for chain in chainList:
                chain.forceStop()

        self.acceptQuestMap = {}
        self.finishQuestMap = {}
        self.finishActivityMap = {}
        self.getItemMap = {}
        self.enterTrapMap = {}
        self.completeQuestCondMap = {}
        self.fubenMap = {}
        self.lvMap = {}
        self.jingJieMap = {}
        self.daoHengSlotMap = {}
        self.componentMap = {}
        self.monsterMap = {}
        self.monsterDyingMap = {}
        self.questboxMap = {}
        self.operaSelectMap = {}
        self.hpPercentMap = {}
        self.useSkillMap = {}
        self.mouseModeList = []
        self.keyboardModeList = []
        self.loginTrigger = []
        self.loginDailyTrigger = []
        self.equipRepairTrigger = []
        self.yaoHuaTrigger = []
        self.questItem = {}
        self.setEquipMap = {}
        self.chunkNameMap = {}
        self.qingGongStateMap = {}
        self.expMap = {}
        self.runningChains = []
        self.demoChains = {}
        self.componentIdList = []
        self.finishCallback = {}
        self.mailTrigger = []
        self.dyeTrigger = []
        self.shiHunTrigger = []
        self.stateTrigger = {}
        self.mallScoreTrigger = {}
        self.specificTitleTrigger = {}
        self.titleTrigger = []
        self.freezeCashTrigger = []
        self.startCCBoxTrigger = []
        self.metorTrigger = []
        self.apprenticeTrigger = []
        self.guildActiveTrigger = []
        self.guildSpaceTrigger = []
        self.loadedUIMap = {}
        self.loadedSWFMap = {}
        self.loadedWingWorldUIMap = {}
        self.inClanWarTrigger = []
        self.guildMemberSkillMap = {}
        self.inFlyTrigger = []
        self.gameLoadedTrigger = []
        self.ymfScorePercentMap = {}
        self.leaveMapId = {}
        self.unloadWidgetId = {}
        self.checkAvatarMap = {}
        self.finishClueMap = {}
        self.openTheaterMap = {}
        self.useItemMap = {}
        self.finishFbMap = {}
        self.excitementMap = {}
        self.teamMap = {}
        self.multiCarrierReadyTrigger = {}

    def getBeginCond(self, componentId):
        d = TMD.data[componentId]
        return {'triggerFunc': d.get('triggerFunc', ()),
         'triggerArg': d.get('triggerArg', ())}

    def getStep(self, componentId):
        com = TMD.data.get(componentId, None)
        if com:
            return com.get('steps', None)
        else:
            return

    def addComponent(self, componentId):
        if self.hasComponent(componentId):
            return
        k = componentId
        v = self.getBeginCond(k)
        self.componentIdList.append(k)
        if len(v['triggerFunc']) == 0:
            manager = self.manager()
            if manager:
                manager.componentFail(k)
            return
        for index, trigger in enumerate(v['triggerFunc']):
            if trigger == 0:
                continue
            if trigger == CBC_LOGIN_TRIGGER:
                self.loginTrigger.append(k)
            elif trigger == CBC_LOGIN_DAILY_TRIGGER:
                self.loginDailyTrigger.append(k)
            elif trigger == CBC_KILL_MONSTER:
                for monsterId in v['triggerArg'][index]:
                    self.monsterMap.setdefault(monsterId, []).append(k)

            elif trigger == CBC_ACCEPT_QUEST:
                for questId in v['triggerArg'][index]:
                    self.acceptQuestMap.setdefault(questId, []).append(k)

            elif trigger == CBC_FINISH_QUEST:
                for questId in v['triggerArg'][index]:
                    self.finishQuestMap.setdefault(questId, []).append(k)

            elif trigger == CBC_COMPLETE_QUEST_CONDITION:
                for questId in v['triggerArg'][index]:
                    self.completeQuestCondMap.setdefault(questId, []).append(k)

            elif trigger == CBC_LV:
                for lv in v['triggerArg'][index]:
                    self.lvMap.setdefault(lv, []).append(k)

            elif trigger == CBC_ENTER_FUBEN:
                for fubenId in v['triggerArg'][index]:
                    self.fubenMap.setdefault(fubenId, []).append(k)

            elif trigger == CBC_ENTER_TRAP:
                for charType in v['triggerArg'][index]:
                    self.enterTrapMap[charType] = k

            elif trigger == CBC_MONSTER_DYING:
                for charType in v['triggerArg'][index]:
                    self.monsterDyingMap[charType] = k

            elif trigger == CBC_QUEST_ITEM:
                self.questItem[k] = v['triggerArg'][index]
            elif trigger == CBC_OPERATION_SELECT:
                for id in v['triggerArg'][index]:
                    self.operaSelectMap[id] = k

            elif trigger == CBC_HP_PERCENT:
                for id in v['triggerArg'][index]:
                    self.hpPercentMap[id] = k

            elif trigger == CBC_USE_SKILL:
                for skillId in v['triggerArg'][index]:
                    self.useSkillMap.setdefault(skillId, []).append(k)

            elif trigger == CBC_FINISH_ACTIVITY:
                for actId in v['triggerArg'][index]:
                    self.finishActivityMap.setdefault(actId, []).append(k)

            elif trigger == CBC_GET_ITEM:
                for itemId in v['triggerArg'][index]:
                    self.getItemMap.setdefault(itemId, []).append(k)

            elif trigger == CBC_EQUIP_REPAIR:
                self.equipRepairTrigger.append(k)
            elif trigger == CBC_YAO_HUA:
                self.yaoHuaTrigger.append(k)
            elif trigger == CBC_SET_EQUIP:
                for equipId in v['triggerArg'][index]:
                    self.setEquipMap.setdefault(equipId, []).append(k)

            elif trigger == CBC_CHUNK_NAME_TRIGGER:
                for chunkName in v['triggerArg'][index]:
                    self.chunkNameMap.setdefault(chunkName, []).append(k)

            elif trigger == CBC_QING_GONG_STATE_TRIGGER:
                for qingGongState in v['triggerArg'][index]:
                    self.qingGongStateMap.setdefault(qingGongState, []).append(k)

            elif trigger == CBC_FULL_EXP:
                for lv in v['triggerArg'][index]:
                    self.expMap[lv] = k

            elif trigger == CBC_GET_MAIL:
                self.mailTrigger.append(k)
            elif trigger == CBC_PLAYER_DYE_TRIGGER:
                self.dyeTrigger.append(k)
            elif trigger == CBC_PLAYER_SHIHUN_TRIGGER:
                self.shiHunTrigger.append(k)
            elif trigger == CBC_GET_STATE:
                for stateId in v['triggerArg'][index]:
                    self.stateTrigger.setdefault(stateId, []).append(k)

            elif trigger == CBC_MALL_SCORE:
                for mScore in v['triggerArg'][index]:
                    self.mallScoreTrigger[mScore] = k

            elif trigger == CBC_GET_TITLE:
                self.titleTrigger.append(k)
            elif trigger == CBC_GET_SPECIFIC_TITLE:
                for titleId in v['triggerArg'][index]:
                    self.specificTitleTrigger[titleId] = k

            elif trigger == CBC_BREAK_JINGJIE:
                for lv in v['triggerArg'][index]:
                    self.jingJieMap.setdefault(lv, []).append(k)

            elif trigger == CBC_OPEN_DAOHENG_SLOT:
                for lv in v['triggerArg'][index]:
                    self.daoHengSlotMap.setdefault(lv, []).append(k)

            elif trigger == CBC_GET_FREEZE_CASH:
                self.freezeCashTrigger.append(k)
            elif trigger == CBC_START_CCBOX:
                self.startCCBoxTrigger.append(k)
            elif trigger == CBC_APPRENTICE_GRADUATE:
                self.metorTrigger.append(k)
            elif trigger == CBC_BE_APPRENTICE:
                self.apprenticeTrigger.append(k)
            elif trigger == CBC_GUILD_ACTIVE:
                self.guildActiveTrigger.append(k)
            elif trigger == CBC_BE_GUILD_HAS_SPACE:
                self.guildSpaceTrigger.append(k)
            elif trigger == CBC_LOADED_UI:
                for uId in v['triggerArg'][index]:
                    self.loadedUIMap.setdefault(uId, []).append(k)

            elif trigger == CBC_LOADED_SWF:
                for uId in v['triggerArg'][index]:
                    self.loadedSWFMap.setdefault(uId, []).append(k)

            elif trigger == CBC_LOADED_UI_IN_WING_WORLD:
                for uId in v['triggerArg'][index]:
                    self.loadedWingWorldUIMap.setdefault(uId, []).append(k)

            elif trigger == CBC_IN_CLAN_WAR:
                self.inClanWarTrigger.append(k)
            elif trigger == CBC_GUILD_MEMBER_SKILL:
                for skillId in v['triggerArg'][index]:
                    self.guildMemberSkillMap.setdefault(skillId, []).append(k)

            elif trigger == CBC_IN_FLY:
                self.inFlyTrigger.append(k)
            elif trigger == CBC_GAME_LOADED:
                self.gameLoadedTrigger.append(k)
            elif trigger == CBC_YMF_SCORE:
                for id in v['triggerArg'][index]:
                    self.ymfScorePercentMap[id] = k

            elif trigger == CBC_LEAVE_MAP:
                for lv in v['triggerArg'][index]:
                    self.leaveMapId.setdefault(lv, []).append(k)

            elif trigger == CBC_UNLOAD_WIDGET:
                for lv in v['triggerArg'][index]:
                    self.unloadWidgetId.setdefault(lv, []).append(k)

            elif trigger == CBC_CHECK_AVATAR:
                for cnt in v['triggerArg'][index]:
                    self.checkAvatarMap.setdefault(cnt, []).append(k)

            elif trigger == CBC_FINISH_CLUE:
                for cnt in v['triggerArg'][index]:
                    self.finishClueMap.setdefault(cnt, []).append(k)

            elif trigger == CBC_OPEN_THEATER:
                for cnt in v['triggerArg'][index]:
                    self.openTheaterMap.setdefault(cnt, []).append(k)

            elif trigger == CBC_USE_ITEM:
                for cnt in v['triggerArg'][index]:
                    self.useItemMap.setdefault(cnt, []).append(k)

            elif trigger == CBC_FINISH_FB:
                for fbNo in v['triggerArg'][index]:
                    self.finishFbMap.setdefault(fbNo, []).append(k)

            elif trigger == CBC_EXCITEMENT:
                self.excitementMap.setdefault(v['triggerArg'][index], []).append(k)
            elif trigger == CBC_TEAM:
                self.teamMap.setdefault(v['triggerArg'][index], []).append(k)
            elif trigger == CBC_MULTI_CARRIER_READY_ENOUGH:
                for carrierNo in v['triggerArg'][index]:
                    self.multiCarrierReadyTrigger[carrierNo] = k

    def removeMultiTutorialMap(self, tMap, componentId):
        needRemove = []
        for key, val in tMap.iteritems():
            try:
                val.remove(componentId)
                if len(val) == 0:
                    needRemove.append(key)
            except:
                continue

        for key in needRemove:
            tMap.pop(key)

        return tMap

    def removeComponent(self, componentId):
        k = componentId
        v = self.getBeginCond(k)
        if k in self.componentIdList:
            self.componentIdList.remove(k)
        else:
            return
        for index, trigger in enumerate(v['triggerFunc']):
            if trigger == CBC_LOGIN_TRIGGER:
                self.loginTrigger.remove(k)
            elif trigger == CBC_LOGIN_DAILY_TRIGGER:
                self.loginDailyTrigger.remove(k)
            elif trigger == CBC_KILL_MONSTER:
                self.monsterMap = self.removeMultiTutorialMap(self.monsterMap, k)
            elif trigger == CBC_ACCEPT_QUEST:
                self.acceptQuestMap = self.removeMultiTutorialMap(self.acceptQuestMap, k)
            elif trigger == CBC_FINISH_QUEST:
                self.finishQuestMap = self.removeMultiTutorialMap(self.finishQuestMap, k)
            elif trigger == CBC_COMPLETE_QUEST_CONDITION:
                self.completeQuestCondMap = self.removeMultiTutorialMap(self.completeQuestCondMap, k)
            elif trigger == CBC_LV:
                self.lvMap = self.removeMultiTutorialMap(self.lvMap, k)
            elif trigger == CBC_ENTER_FUBEN:
                self.fubenMap = self.removeMultiTutorialMap(self.fubenMap, k)
            elif trigger == CBC_ENTER_TRAP:
                for charType in v['triggerArg'][index]:
                    del self.enterTrapMap[charType]

            elif trigger == CBC_MONSTER_DYING:
                for charType in v['triggerArg'][index]:
                    del self.monsterDyingMap[charType]

            elif trigger == CBC_QUEST_ITEM:
                del self.questItem[k]
            elif trigger == CBC_OPERATION_SELECT:
                for id in v['triggerArg'][index]:
                    del self.operaSelectMap[id]

            elif trigger == CBC_HP_PERCENT:
                for id in v['triggerArg'][index]:
                    del self.hpPercentMap[id]

            elif trigger == CBC_USE_SKILL:
                self.useSkillMap = self.removeMultiTutorialMap(self.useSkillMap, k)
            elif trigger == CBC_FINISH_ACTIVITY:
                self.finishActivityMap = self.removeMultiTutorialMap(self.finishActivityMap, k)
            elif trigger == CBC_GET_ITEM:
                self.getItemMap = self.removeMultiTutorialMap(self.getItemMap, k)
            elif trigger == CBC_EQUIP_REPAIR:
                self.equipRepairTrigger.remove(k)
            elif trigger == CBC_YAO_HUA:
                self.yaoHuaTrigger.remove(k)
            elif trigger == CBC_SET_EQUIP:
                self.setEquipMap = self.removeMultiTutorialMap(self.setEquipMap, k)
            elif trigger == CBC_CHUNK_NAME_TRIGGER:
                self.chunkNameMap = self.removeMultiTutorialMap(self.chunkNameMap, k)
            elif trigger == CBC_QING_GONG_STATE_TRIGGER:
                self.qingGongStateMap = self.removeMultiTutorialMap(self.qingGongStateMap, k)
            elif trigger == CBC_FULL_EXP:
                for lv in v['triggerArg'][index]:
                    del self.expMap[lv]

            elif trigger == CBC_GET_MAIL:
                self.mailTrigger.remove(k)
            elif trigger == CBC_PLAYER_DYE_TRIGGER:
                self.dyeTrigger.remove(k)
            elif trigger == CBC_PLAYER_SHIHUN_TRIGGER:
                self.shiHunTrigger.remove(k)
            elif trigger == CBC_GET_STATE:
                self.stateTrigger = self.removeMultiTutorialMap(self.stateTrigger, k)
            elif trigger == CBC_MALL_SCORE:
                for mScore in v['triggerArg'][index]:
                    del self.mallScoreTrigger[mScore]

            elif trigger == CBC_GET_TITLE:
                self.titleTrigger.remove(k)
            elif trigger == CBC_GET_SPECIFIC_TITLE:
                for titleId in v['triggerArg'][index]:
                    del self.specificTitleTrigger[titleId]

            elif trigger == CBC_BREAK_JINGJIE:
                self.jingJieMap = self.removeMultiTutorialMap(self.jingJieMap, k)
            elif trigger == CBC_OPEN_DAOHENG_SLOT:
                self.daoHengSlotMap = self.removeMultiTutorialMap(self.daoHengSlotMap, k)
            elif trigger == CBC_GET_FREEZE_CASH:
                self.freezeCashTrigger.remove(k)
            elif trigger == CBC_START_CCBOX:
                self.startCCBoxTrigger.remove(k)
            elif trigger == CBC_APPRENTICE_GRADUATE:
                self.metorTrigger.remove(k)
            elif trigger == CBC_BE_APPRENTICE:
                self.apprenticeTrigger.remove(k)
            elif trigger == CBC_GUILD_ACTIVE:
                self.guildActiveTrigger.remove(k)
            elif trigger == CBC_BE_GUILD_HAS_SPACE:
                self.guildSpaceTrigger.remove(k)
            elif trigger == CBC_LOADED_UI:
                self.loadedUIMap = self.removeMultiTutorialMap(self.loadedUIMap, k)
            elif trigger == CBC_LOADED_SWF:
                self.loadedSWFMap = self.removeMultiTutorialMap(self.loadedSWFMap, k)
            elif trigger == CBC_LOADED_UI_IN_WING_WORLD:
                self.loadedWingWorldUIMap = self.removeMultiTutorialMap(self.loadedWingWorldUIMap, k)
            elif trigger == CBC_IN_CLAN_WAR:
                self.inClanWarTrigger.remove(k)
            elif trigger == CBC_GUILD_MEMBER_SKILL:
                self.guildMemberSkillMap = self.removeMultiTutorialMap(self.guildMemberSkillMap, k)
            elif trigger == CBC_IN_FLY:
                self.inFlyTrigger.remove(k)
            elif trigger == CBC_GAME_LOADED:
                self.gameLoadedTrigger.remove(k)
            elif trigger == CBC_YMF_SCORE:
                self.ymfScorePercentMap = self.removeMultiTutorialMap(self.ymfScorePercentMap, k)
            elif trigger == CBC_LEAVE_MAP:
                self.leaveMapId = self.removeMultiTutorialMap(self.leaveMapId, k)
            elif trigger == CBC_UNLOAD_WIDGET:
                self.unloadWidgetId = self.removeMultiTutorialMap(self.unloadWidgetId, k)
            elif trigger == CBC_CHECK_AVATAR:
                self.checkAvatarMap = self.removeMultiTutorialMap(self.checkAvatarMap, k)
            elif trigger == CBC_FINISH_CLUE:
                self.finishClueMap = self.removeMultiTutorialMap(self.finishClueMap, k)
            elif trigger == CBC_OPEN_THEATER:
                self.openTheaterMap = self.removeMultiTutorialMap(self.openTheaterMap, k)
            elif trigger == CBC_USE_ITEM:
                self.useItemMap = self.removeMultiTutorialMap(self.useItemMap, k)
            elif trigger == CBC_FINISH_FB:
                self.finishFbMap = self.removeMultiTutorialMap(self.finishFbMap, k)
            elif trigger == CBC_EXCITEMENT:
                self.excitementMap = self.removeMultiTutorialMap(self.excitementMap, k)
            elif trigger == CBC_TEAM:
                self.teamMap = self.removeMultiTutorialMap(self.teamMap, k)
            elif trigger == CBC_MULTI_CARRIER_READY_ENOUGH:
                for carrierNo in v['triggerArg'][index]:
                    del self.multiCarrierReadyTrigger[carrierNo]

    def isDailyComponent(self, componentId):
        if not TMD.data.has_key(componentId):
            return False
        triggerFunc = TMD.data[componentId]['triggerFunc']
        return CBC_LOGIN_DAILY_TRIGGER in triggerFunc

    def chainFinish(self, chain):
        if chain not in self.runningChains:
            return
        self.runningChains.remove(chain)
        if self.finishCallback.has_key(chain.componentId):
            callback = self.finishCallback.pop(chain.componentId)
            callback(True)
        if self.demoChains.has_key(chain):
            del self.demoChains[chain]
        else:
            componentId = chain.componentId
            self.removeComponent(componentId)
            manager = self.manager()
            if manager:
                manager.componentFinish(componentId)

    def chainFail(self, chain):
        self.runningChains.remove(chain)
        if self.finishCallback.has_key(chain.componentId):
            callback = self.finishCallback.pop(chain.componentId)
            callback(False)
        if self.demoChains.has_key(chain):
            del self.demoChains[chain]
        else:
            componentId = chain.componentId
            canReTrigger = TMD.data[componentId].get('canReTrigger', 0)
            if not canReTrigger:
                self.removeComponent(componentId)
            manager = self.manager()
            if manager:
                if self.isDailyComponent(componentId):
                    manager.dailyComponentFail(componentId)
                else:
                    manager.componentFail(componentId)

    def _isNoArrowWiget(self, componentId):
        steps = TMD.data[componentId]['steps']
        for step in steps:
            if TID.data[step]['type'] == 1:
                return True

        return False

    def createChain(self, componentId, callback = None):
        if not componentId:
            return
        elif gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        else:
            p = BigWorld.player()
            componentData = TMD.data.get(componentId)
            if componentData is None:
                return
            elif componentData.get('saveType') == const.TUTOR_ACCOUNT_SAVE and p.inWingCity():
                return
            elif componentData['minLv'] > p.lv or componentData['maxLv'] < p.lv:
                return
            elif p.physique.school not in componentData['school']:
                return
            modelId = transDummyBodyType(p.physique.sex, p.physique.bodyType, True)
            if componentData.has_key('modelId') and modelId not in componentData['modelId']:
                return
            elif componentData.has_key('opMode') and p.getOperationMode() not in componentData['opMode']:
                return
            hour = formula.getXingJiTime()
            dayMode = utils.getDayMode(hour)
            if componentData.has_key('dayMode') and dayMode not in componentData['dayMode']:
                return
            for chain in self.runningChains:
                if chain.componentId == componentId:
                    return

            chain = IntroChain(self, componentId, TMD.data[componentId]['steps'])
            self.runningChains.append(chain)
            if callback:
                self.finishCallback[componentId] = callback
            BigWorld.callback(0.3, chain.playNext)
            return chain

    def createChainDemo(self, componentId):
        chain = self.createChain(componentId)
        if chain:
            self.demoChains[chain] = True

    def hasComponent(self, componentId):
        return componentId in self.componentIdList

    def onComponentFinish(self, componentId):
        nextComponentIdList = self.componentMap.get(componentId, None)
        if nextComponentIdList:
            for nextComponentId in nextComponentIdList:
                self.createChain(nextComponentId)

    def onComponentFail(self, componentId):
        nextComponentIdList = self.componentMap.get(componentId, None)
        if nextComponentIdList:
            for nextComponentId in nextComponentIdList:
                self.removeComponent(nextComponentId)
                manager = self.manager()
                if manager:
                    manager.componentFail(nextComponentId)

    def doCreateMultiChain(self, comMap, key):
        componentList = comMap.get(key, None)
        if componentList:
            for componentId in componentList:
                self.createChain(componentId)

    def onEnterFuben(self, fubenId):
        self.doCreateMultiChain(self.fubenMap, fubenId)

    def onAcceptQuest(self, questId):
        self.doCreateMultiChain(self.acceptQuestMap, questId)

    def onSetEquip(self, equipId):
        self.doCreateMultiChain(self.setEquipMap, equipId)

    def onChunkNameTrigger(self, chunkName):
        self.doCreateMultiChain(self.chunkNameMap, chunkName)

    def onQuestItem(self, questId):
        for key, value in self.questItem.iteritems():
            if value[0] == questId:
                questBag = getattr(BigWorld.player(), 'questBag', None)
                if questBag:
                    page = questBag.findItemInPages(value[0], includeExpired=True, includeLatch=True, includeShihun=True)
                    if page != const.CONT_NO_PAGE:
                        self.createChain(key)

    def onFinishQuest(self, questId):
        self.doCreateMultiChain(self.finishQuestMap, questId)

    def onFinishActivity(self, actId):
        self.doCreateMultiChain(self.finishActivityMap, actId)

    def onGetItem(self, itemId):
        self.doCreateMultiChain(self.getItemMap, itemId)

    def onCompleteQuestCondition(self, questId):
        self.doCreateMultiChain(self.completeQuestCondMap, questId)

    def onEnterTrap(self, charType):
        componentId = self.enterTrapMap.get(charType, None)
        self.createChain(componentId)

    def onQingGongState(self, state):
        self.doCreateMultiChain(self.qingGongStateMap, state)

    def onFullExp(self, lv):
        componentId = self.expMap.get(lv, None)
        self.createChain(componentId)

    def onKillMonster(self, monsterId):
        self.doCreateMultiChain(self.monsterMap, monsterId)

    def onMonsterDying(self, charType):
        componentId = self.monsterDyingMap.get(charType, None)
        self.createChain(componentId)

    def onHpByPercent(self, preHP, currentHP, maxHp):
        for threshold in self.hpPercentMap.keys():
            thresholdHP = 1.0 * maxHp * threshold / 100
            if preHP >= thresholdHP and currentHP < thresholdHP:
                componentId = self.hpPercentMap.get(threshold, None)
                self.createChain(componentId)

    def onLevelUp(self, lv):
        self.doCreateMultiChain(self.lvMap, lv)

    def onExcitementActivate(self, exId):
        self.doCreateMultiChain(self.excitementMap, exId)

    def onTeamActivate(self, identityType):
        self.doCreateMultiChain(self.teamMap, identityType)

    def onUseSkill(self, skillId):
        self.doCreateMultiChain(self.useSkillMap, skillId)

    def onLoginTrigger(self):
        p = BigWorld.player()
        if not p:
            return
        for componentId in self.loginTrigger:
            self.createChain(componentId)

        for componentId in self.loginDailyTrigger:
            self.createChain(componentId)

    def onEquipRepair(self):
        for componentId in self.equipRepairTrigger:
            self.createChain(componentId)

    def onInYaoHua(self):
        for componentId in self.yaoHuaTrigger:
            self.createChain(componentId)

    def onGetMail(self):
        for componentId in self.mailTrigger:
            self.createChain(componentId)

    def onGetFreezeCash(self):
        for componentId in self.freezeCashTrigger:
            self.createChain(componentId)

    def onGetStartCCBox(self):
        for componentId in self.startCCBoxTrigger:
            self.createChain(componentId)

    def onGetState(self, stateId):
        self.doCreateMultiChain(self.stateTrigger, stateId)

    def onGetMallScore(self, mScore):
        oldScore = mScore
        for score in sorted(self.mallScoreTrigger.keys()):
            if mScore < score:
                break
            oldScore = score

        componentId = self.mallScoreTrigger.get(oldScore, None)
        if componentId:
            self.createChain(componentId)

    def onGetTitle(self):
        for componentId in self.titleTrigger:
            self.createChain(componentId)

    def onMultiCarrierReadyFull(self, carrierNo):
        componentId = self.multiCarrierReadyTrigger.get(carrierNo, None)
        if componentId:
            self.createChain(componentId)

    def onGetSpecificTitle(self, titleId):
        componentId = self.specificTitleTrigger.get(titleId, None)
        self.createChain(componentId)

    def onDye(self):
        for componentId in self.dyeTrigger:
            self.createChain(componentId)

    def onEquipShiHun(self):
        for componentId in self.shiHunTrigger:
            self.createChain(componentId)

    def onOperaSelectTrigger(self, operaType):
        componentId = self.operaSelectMap.get(operaType, None)
        self.createChain(componentId)

    def onMouseLeftBtnUp(self, btnName):
        for chain in self.runningChains:
            chain.onMouseLeftBtnUp(btnName)

    def onMouseRightBtnUp(self, btnName):
        for chain in self.runningChains:
            chain.onMouseRightBtnUp(btnName)

    def onKeyEvent(self, down, key, vk, mods):
        for chain in self.runningChains:
            chain.onKeyEvent(key, mods)

    def onFinishedQuest(self, questId):
        for chain in self.runningChains:
            chain.onFinishedQuest(questId)

    def onCompletedQuest(self, questId):
        for chain in self.runningChains:
            chain.onCompletedQuest(questId)

    def onLoadWidget(self, widgetId):
        for chain in self.runningChains:
            chain.onLoadWidget(widgetId)

    def onUseItemEndCheck(self, itemId):
        for chain in self.runningChains:
            chain.onUseItemEndCheck(itemId)

    def onUseSkillEndCheck(self, skillId):
        for chain in self.runningChains:
            chain.onUseSkillEndCheck(skillId)

    def onUseCommonSkillEndCheck(self, skillId):
        for chain in self.runningChains:
            chain.onUseCommonSkillEndCheck(skillId)

    def onFinishFbId(self, fubenId):
        for chain in self.runningChains:
            chain.onFinishFbId(fubenId)

    def onCheckQingGongState(self, stateId):
        for chain in self.runningChains:
            chain.onCheckQingGongState(stateId)

    def onCheckAction(self, actionId):
        for chain in self.runningChains:
            chain.onCheckAction(actionId)

    def onBreakJingJie(self, jingJie):
        self.doCreateMultiChain(self.jingJieMap, jingJie)

    def onAddDaoHengSlot(self, skillId):
        self.doCreateMultiChain(self.daoHengSlotMap, skillId)

    def onApprenticeGraduate(self):
        for componentId in self.metorTrigger:
            self.createChain(componentId)

    def onBeApprentice(self):
        for componentId in self.apprenticeTrigger:
            self.createChain(componentId)

    def onActiveGuild(self):
        for componentId in self.guildActiveTrigger:
            self.createChain(componentId)

    def onHasGuildSpace(self):
        for componentId in self.guildSpaceTrigger:
            self.createChain(componentId)

    def onLoadedWidgetTrigger(self, widgetId):
        self.doCreateMultiChain(self.loadedUIMap, widgetId)
        p = BigWorld.player()
        if p and hasattr(p, 'inWingPeaceCity') and p.inWingPeaceCity():
            self.doCreateMultiChain(self.loadedWingWorldUIMap, widgetId)

    def onLoadedSwfTrigger(self, swfName):
        self.doCreateMultiChain(self.loadedSWFMap, swfName)

    def onInClanWar(self):
        for componentId in self.inClanWarTrigger:
            self.createChain(componentId)

    def onGuildMemberSkillTrigger(self, skillId):
        self.doCreateMultiChain(self.guildMemberSkillMap, skillId)

    def onInFly(self):
        for componentId in self.inFlyTrigger:
            self.createChain(componentId)

    def onGameLoaded(self):
        for componentId in self.gameLoadedTrigger:
            self.createChain(componentId)

    def onYmfScoreByPercent(self, preScore, currentScore, maxScore):
        for threshold in self.ymfScorePercentMap.keys():
            thresholdScore = 1.0 * maxScore * threshold / 100
            if thresholdScore > preScore and thresholdScore <= currentScore:
                componentId = self.ymfScorePercentMap.get(threshold, None)
                self.createChain(componentId)

    def onLeaveMap(self, mapId):
        self.doCreateMultiChain(self.leaveMapId, mapId)

    def onUnloadWidget(self, widgetId):
        self.doCreateMultiChain(self.unloadWidgetId, widgetId)

    def onCheckAvatarCnt(self, cnt):
        self.doCreateMultiChain(self.checkAvatarMap, cnt)

    def onFinishClue(self, cId):
        self.doCreateMultiChain(self.finishClueMap, cId)

    def onOpenTheater(self, tId):
        self.doCreateMultiChain(self.openTheaterMap, tId)

    def onUseItem(self, itemId):
        self.doCreateMultiChain(self.useItemMap, itemId)

    def onFinishFb(self, fbNo):
        self.doCreateMultiChain(self.finishFbMap, fbNo)


class TutorManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.hasLoginTrigger = True
        self.loginTriggerIdx = 0
        self.completeQuestCond = {}
        self.comSet = ComponentSet(self)

    def _getSaveType(self, componentId):
        return TMD.data.get(componentId, None).get('saveType', 1)

    def dailyComponentFinish(self, componentId):
        p = BigWorld.player()
        if not p or p.__class__.__name__ == 'PlayerAccount':
            return
        self.setTutorInfo(self._getSaveType(componentId), componentId, p.getServerTime())
        self.save()

    def dailyComponentFail(self, componentId):
        p = BigWorld.player()
        if not p or p.__class__.__name__ == 'PlayerAccount':
            return
        self.setTutorInfo(self._getSaveType(componentId), componentId, p.getServerTime())
        self.save()

    def componentFinish(self, componentId):
        if componentId not in TMD.data:
            return
        self.setTutorInfo(self._getSaveType(componentId), componentId, const.TUTOR_CFS_DONE)
        self.save()
        self.onComponentFinish(componentId)
        p = BigWorld.player()
        p and p.cell and p.cell.triggerTutorialStats(componentId)

    def componentFail(self, componentId):
        failCnt = self.getTutorInfo(self._getSaveType(componentId), componentId) + 1
        if failCnt > const.TUTOR_CFS_DONE:
            failCnt = const.TUTOR_CFS_DONE
        self.setTutorInfo(self._getSaveType(componentId), componentId, failCnt)
        self.save()
        failTriggerComponent = TMD.data[componentId].get('failTriggerComponent', -1)
        if failTriggerComponent != -1 and TMD.data.has_key(failTriggerComponent):
            self.startComponent(failTriggerComponent)

    def initComponentSet(self):
        self.comSet.reset()
        p = BigWorld.player()
        if not p:
            return
        currDate = datetime.date.fromtimestamp(p.getServerTime())
        modelId = transDummyBodyType(p.physique.sex, p.physique.bodyType, True)
        for k, v in TMD.data.iteritems():
            if v.get('includeServer', ()) and gameglobal.rds.g_serverid not in v['includeServer']:
                continue
            if v.get('excludeServer', ()) and gameglobal.rds.g_serverid in v['excludeServer']:
                continue
            if p.physique.school not in v['school']:
                continue
            if v.has_key('modelId') and modelId not in v['modelId']:
                continue
            if p.lv > v['maxLv']:
                continue
            flag = self.getTutorInfo(v['saveType'], k)
            if flag == const.TUTOR_CFS_DONE:
                continue
            elif flag > const.TUTOR_CFS_DONE:
                lastTriggerDate = datetime.date.fromtimestamp(flag)
                gamelog.debug('@hjx tutor#initComponentSet', currDate, lastTriggerDate)
                if lastTriggerDate >= currDate:
                    continue
            self.comSet.addComponent(k)

    def getTutorInfo(self, saveType, key):
        if saveType == const.TUTOR_ACCOUNT_SAVE:
            return gameglobal.rds.accTutorialInfo.get(key, 0)
        if saveType == const.TUTOR_AVATAR_SAVE:
            return gameglobal.rds.avaTutorialInfo.get(key, 0)

    def setTutorInfo(self, saveType, key, value):
        self._setTutorInfo(saveType, key, value)
        p = BigWorld.player()
        if gameglobal.rds.GameState < gametypes.GS_PLAYGAME:
            return
        if p._isSoul():
            if saveType == const.TUTOR_ACCOUNT_SAVE:
                p.base.saveOneAccTutorial(key, value)
            elif saveType == const.TUTOR_AVATAR_SAVE:
                p.cell.setOneTutorial(key, value)

    def _setTutorInfo(self, saveType, key, value):
        if saveType == const.TUTOR_ACCOUNT_SAVE:
            gameglobal.rds.accTutorialInfo[key] = value
        elif saveType == const.TUTOR_AVATAR_SAVE:
            gameglobal.rds.avaTutorialInfo[key] = value

    def loadAccTutorial(self, savedData):
        gameglobal.rds.accTutorialInfo = {}
        if savedData:
            try:
                gameglobal.rds.accTutorialInfo = cPickle.loads(zlib.decompress(savedData))
            except:
                gameglobal.rds.accTutorialInfo = {}

        if type(gameglobal.rds.accTutorialInfo) != dict:
            gameglobal.rds.accTutorialInfo = {}
        self.load()

    def load(self):
        self.completeQuestCond = {}
        p = BigWorld.player()
        gameglobal.rds.avaTutorialInfo = p.tutorial
        self.initComponentSet()
        self.hasLoginTrigger = False

    def clearTutor(self, ok):
        if ok:
            gameglobal.rds.accTutorialInfo = {}
            gameglobal.rds.avaTutorialInfo = {}
            self.completeQuestCond = {}
            self.save()
            self.initComponentSet()

    def save(self):
        p = clientcom.getPlayerAvatar()
        if p and hasattr(gameglobal.rds, 'accTutorialInfo'):
            savedData = zlib.compress(cPickle.dumps(gameglobal.rds.accTutorialInfo, 2))
            p.base.saveAccTutorial(savedData)
        if p and hasattr(gameglobal.rds, 'avaTutorialInfo'):
            tutorialKeys = gameglobal.rds.avaTutorialInfo.keys()
            tutorialVals = [ gameglobal.rds.avaTutorialInfo[k] for k in tutorialKeys ]
            p.cell.setTutorial(tutorialKeys, tutorialVals)

    def startComponent(self, componentId, callback = None):
        v = TMD.data.get(componentId)
        if not v:
            return
        flag = self.getTutorInfo(v['saveType'], componentId)
        if flag == const.TUTOR_CFS_DONE and v.get('canReTrigger', 0) != gametypes.TUTORIAL_FAILED_TYPE_RETRIGGER_FORCELY:
            return
        self.comSet.createChain(componentId, callback)

    def forceStopComponent(self, componentId):
        for chain in self.comSet.runningChains:
            if chain and chain.componentId == componentId:
                chain.forceStop()

    def startComponentDemo(self, componentId):
        if self.comSet.hasComponent(componentId):
            self.comSet.createChainDemo(componentId)
            return
        self.comSet.createChainDemo(componentId)

    def onComponentFinish(self, componentId):
        self.comSet.onComponentFinish(componentId)

    def onEnterFuben(self, fubenId):
        self.comSet.onEnterFuben(fubenId)

    def onAcceptQuest(self, questId):
        self.comSet.onAcceptQuest(questId)

    def onSetEquip(self, equipId):
        self.comSet.onSetEquip(equipId)

    def onChunkNameTrigger(self, chunkName):
        self.comSet.onChunkNameTrigger(chunkName)

    def onQuestItem(self, questId):
        self.comSet.onQuestItem(questId)

    def onFinishQuest(self, questId):
        self.comSet.onFinishQuest(questId)

    def onFinishActivity(self, actId):
        self.comSet.onFinishActivity(actId)

    def onGetItem(self, itemId):
        self.comSet.onGetItem(itemId)

    def onCompleteQuestCondition(self, questId):
        self.comSet.onCompleteQuestCondition(questId)

    def onEnterTrap(self, charType):
        self.comSet.onEnterTrap(charType)

    def onQingGongState(self, state):
        self.comSet.onQingGongState(state)

    def onFullExp(self, lv):
        self.comSet.onFullExp(lv)

    def onKillMonster(self, monsterId):
        self.comSet.onKillMonster(monsterId)

    def onMonsterDying(self, charType):
        self.comSet.onMonsterDying(charType)

    def onHpByPercent(self, preHP, currentHP, maxHp):
        self.comSet.onHpByPercent(preHP, currentHP, maxHp)

    def onLevelUp(self, lv):
        self.comSet.onLevelUp(lv)

    def onExcitementActivate(self, exId):
        self.comSet.onExcitementActivate(exId)

    def onTeamActivate(self, identityType):
        self.comSet.onTeamActivate(identityType)

    def onUseSkill(self, skillId):
        self.comSet.onUseSkill(skillId)

    def realLoginTrigger(self, loginTriggerIdx):
        if self.loginTriggerIdx != loginTriggerIdx:
            return
        self.comSet.onLoginTrigger()

    def onLoginTrigger(self):
        if self.hasLoginTrigger:
            return
        self.hasLoginTrigger = True
        self.loginTriggerIdx += 1
        loginTriggerTime = TCD.data.get('loginTriggerTime', 2)
        BigWorld.callback(loginTriggerTime, Functor(self.realLoginTrigger, self.loginTriggerIdx))

    def onEquipRepair(self):
        self.comSet.onEquipRepair()

    def onInYaoHua(self):
        self.comSet.onInYaoHua()

    def onGetMail(self):
        self.comSet.onGetMail()

    def onGetFreezeCash(self):
        self.comSet.onGetFreezeCash()

    def onGetStartCCBox(self):
        self.comSet.onGetStartCCBox()

    def onGetState(self, stateId):
        self.comSet.onGetState(stateId)

    def onGetMallScore(self, mScore):
        self.comSet.onGetMallScore(mScore)

    def onGetTitle(self):
        self.comSet.onGetTitle()

    def onMultiCarrierReadyFull(self, carrierNo):
        self.comSet.onMultiCarrierReadyFull(carrierNo)

    def onGetSpecificTitle(self, titleId):
        self.comSet.onGetSpecificTitle(titleId)

    def onDye(self):
        self.comSet.onDye()

    def onEquipShiHun(self):
        self.comSet.onEquipShiHun()

    def onOperaSelectTrigger(self, operaType):
        self.comSet.onOperaSelectTrigger(operaType)

    def onMouseLeftBtnUp(self, btnName):
        if btnName[0] == None:
            return
        else:
            self.comSet.onMouseLeftBtnUp(btnName)
            return

    def onMouseRightBtnUp(self, btnName):
        if btnName[0] == None:
            return
        else:
            self.comSet.onMouseRightBtnUp(btnName)
            return

    def onFinishedQuest(self, questId):
        self.comSet.onFinishedQuest(questId)

    def onCompletedQuest(self, questId):
        self.comSet.onCompletedQuest(questId)

    def onLoadWidget(self, widgetId):
        self.comSet.onLoadWidget(widgetId)

    def onUseItemEndCheck(self, itemId):
        self.comSet.onUseItemEndCheck(itemId)

    def onUseSkillEndCheck(self, skillId):
        self.comSet.onUseSkillEndCheck(skillId)

    def onUseCommonSkillEndCheck(self, skillId):
        self.comSet.onUseCommonSkillEndCheck(skillId)

    def onKeyEvent(self, down, key, vk, mods):
        self.comSet.onKeyEvent(down, key, vk, mods)

    def onFinishFbId(self, fubenId):
        self.comSet.onFinishFbId(fubenId)

    def onCheckQingGongState(self, stateId):
        self.comSet.onCheckQingGongState(stateId)

    def onCheckAction(self, actionId):
        self.comSet.onCheckAction(actionId)

    def onBreakJingJie(self, jingJie):
        self.comSet.onBreakJingJie(jingJie)

    def onAddDaoHengSlot(self, skillId):
        self.comSet.onAddDaoHengSlot(skillId)

    def onApprenticeGraduate(self):
        self.comSet.onApprenticeGraduate()

    def onBeApprentice(self):
        self.comSet.onBeApprentice()

    def onActiveGuild(self):
        self.comSet.onActiveGuild()

    def onHasGuildSpace(self):
        self.comSet.onHasGuildSpace()

    def onLoadedWidgetTrigger(self, widgetId):
        self.comSet.onLoadedWidgetTrigger(widgetId)

    def onLoadedSwfTrigger(self, widgetId):
        self.comSet.onLoadedSwfTrigger(widgetId)

    def onInClanWar(self):
        self.comSet.onInClanWar()

    def onGuildMemberSkillTrigger(self, skillId):
        self.comSet.onGuildMemberSkillTrigger(skillId)

    def onInFly(self):
        self.comSet.onInFly()

    def onGameLoaded(self):
        self.comSet.onGameLoaded()

    def onYmfScoreByPercent(self, preScore, currentScore, maxScore):
        self.comSet.onYmfScoreByPercent(preScore, currentScore, maxScore)

    def onLeaveMap(self, mapId):
        self.comSet.onLeaveMap(mapId)

    def onUnloadWidget(self, widgetId):
        self.comSet.onUnloadWidget(widgetId)

    def onCheckAvatarCnt(self, cnt):
        self.comSet.onCheckAvatarCnt(cnt)

    def onFinishClue(self, cId):
        self.comSet.onFinishClue(cId)

    def onOpenTheater(self, tId):
        self.comSet.onOpenTheater(tId)

    def onUseItem(self, itemId):
        self.comSet.onUseItem(itemId)

    def onFinishFb(self, fbNo):
        self.comSet.onFinishFb(fbNo)


def initTutorManager():
    gameglobal.rds.accTutorialInfo = {}
    gameglobal.rds.avaTutorialInfo = {}
    return TutorManager.getInstance()
