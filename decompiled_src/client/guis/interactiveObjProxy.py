#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/interactiveObjProxy.o
import BigWorld
from Scaleform import GfxValue
from ui import gbk2unicode
import utils
import gameglobal
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from helpers import navigator
from gamestrings import gameStrings
from data import sys_config_data as SCD
from data import interactive_data as ID
from data import interactive_type_data as ITD
from data import interactive_config_data as ICD
DEFAULT_REWARD_TOTALTIME = 120
DEFAULT_REWARD_PHASE_NUM = 4

class InteractiveObjProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InteractiveObjProxy, self).__init__(uiAdapter)
        self.modelMap = {'showKickAvatar': self.onShowKickAvatar,
         'closeKickWidget': self.onCloseKickWidget,
         'closeNodeSelect': self.onCloseNodeSelect,
         'handleSubmitClick': self.onSubmitClick,
         'handleCancelClick': self.onCancelClick,
         'getInteractiveObjRoles': self.getInteractiveObjRoles,
         'getInteractiveNodes': self.onGetInteractiveNodes,
         'selectNode': self.onSelectNode,
         'closeStoryWidget': self.onCloseStoryWidget,
         'closeLetterWidget': self.onCloseLetterWidget,
         'gotoPosition': self.onGotoPosition,
         'getRewardTips': self.onGetRewardTips,
         'gotoMailMaid': self.onGotoMailMaid,
         'getRewardProgressValue': self.onGetRewardProgressValue}
        self.interactiveObjListShow = False
        self.btnMediator = None
        self.listMediator = None
        self.nodeSelectMediator = None
        self.rewardMediator = None
        self.storyMediator = None
        self.letterMediator = None
        self.widgetBtnId = uiConst.WIDGET_INTERACTIVE_OBJ_KICK
        self.widgetListId = uiConst.WIDGET_INTERACTIVE_OBJ_LIST
        self.widgetSelectId = uiConst.WIDGET_INTERACTIVE_OBJ_INDEX
        self.widgetRewardId = uiConst.WIDGET_INTERACTIVE_OBJ_REWARD_PROGRESS
        self.widgetStoryId = uiConst.WIDGET_INTERACTIVE_STORY
        self.widgetLetterId = uiConst.WIDGET_INTERACTIVE_THANK_LETTER
        self.selectedInteractiveObjId = None
        self.rewardTickTimer = None
        self.rewardTickStartTime = None
        self.storyInteractiveObjId = None
        self.letterInteractiveType = None
        self.rewardTotalTime = DEFAULT_REWARD_TOTALTIME
        uiAdapter.registerEscFunc(uiConst.WIDGET_INTERACTIVE_OBJ_INDEX, self.onCloseSelectorWidget)
        uiAdapter.registerEscFunc(uiConst.WIDGET_INTERACTIVE_OBJ_LIST, self.onCloseListWidget)

    def closeRewardWidget(self):
        self.rewardMediator = None
        self.rewardTotalTime = DEFAULT_REWARD_TOTALTIME
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INTERACTIVE_OBJ_REWARD_PROGRESS)

    def onCloseSelectorWidget(self, *arg):
        self.closeNodeSelectWidget()

    def onCloseListWidget(self, *arg):
        self.listMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INTERACTIVE_OBJ_LIST)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.widgetBtnId:
            self.btnMediator = mediator
        elif widgetId == self.widgetListId:
            self.listMediator = mediator
        elif widgetId == self.widgetSelectId:
            self.nodeSelectMediator = mediator
        elif widgetId == self.widgetRewardId:
            self.rewardMediator = mediator
        elif widgetId == self.widgetStoryId:
            self.storyMediator = mediator
            duration = SCD.data.get('interactiveObjStoryDuration', 60)
            self.playStoryCountDown(duration)
            self.setStoryDetail()
        elif widgetId == self.widgetLetterId:
            self.letterMediator = mediator
            data = ITD.data.get(self.letterInteractiveType, {})
            title = data.get('mailTitle', '')
            content = data.get('mailDesc', '')
            self.showLetter(title, content)

    def showRewardWidget(self, rewardTotalTime):
        if self.rewardMediator:
            return
        enableInteractiveObjReward = gameglobal.rds.configData.get('enableInteractiveObjReward', False)
        if not enableInteractiveObjReward:
            return
        gameglobal.rds.ui.loadWidget(self.widgetRewardId)
        self.rewardTotalTime = rewardTotalTime
        self.rewardTickStartTime = utils.getNow()
        self.rewardTick()

    def onGetRewardProgressValue(self, *arg):
        return GfxValue(self.rewardTotalTime / DEFAULT_REWARD_PHASE_NUM)

    def stopRewardTick(self):
        if self.rewardTickTimer:
            BigWorld.cancelCallback(self.rewardTickTimer)
            self.rewardTickTimer = None

    def rewardTick(self):
        self.stopRewardTick()
        passTime = utils.getNow() - self.rewardTickStartTime
        if passTime > self.rewardTotalTime:
            return
        index = int(passTime / (self.rewardTotalTime / DEFAULT_REWARD_PHASE_NUM * 1.0))
        curValue = passTime - index * (self.rewardTotalTime / DEFAULT_REWARD_PHASE_NUM)
        self.setRewardBarInfo(index, curValue, passTime)
        self.rewardTickTimer = BigWorld.callback(0.2, self.rewardTick)

    def show(self):
        gameglobal.rds.ui.loadWidget(self.widgetBtnId)

    def showKickWidget(self):
        gameglobal.rds.ui.loadWidget(self.widgetBtnId)

    def closeKickWidget(self):
        self.btnMediator = None
        gameglobal.rds.ui.unLoadWidget(self.widgetBtnId)

    def showNodeSelectWidget(self, objId):
        self.selectedInteractiveObjId = objId
        if not self.nodeSelectMediator:
            gameglobal.rds.ui.loadWidget(self.widgetSelectId)
        else:
            self.nodeSelectMediator.Invoke('updateMemberList')

    def clearWidget(self):
        self.btnMediator = None
        gameglobal.rds.ui.unLoadWidget(self.widgetBtnId)

    def reset(self):
        pass

    def showInteractiveObjList(self, visible):
        self.interactiveObjListShow = visible
        if visible:
            gameglobal.rds.ui.loadWidget(self.widgetListId)
        else:
            gameglobal.rds.ui.unLoadWidget(self.widgetListId)

    def showStoryWidget(self, objId):
        enableInteractiveObjReward = gameglobal.rds.configData.get('enableInteractiveObjReward', False)
        if not enableInteractiveObjReward:
            return
        self.storyInteractiveObjId = objId
        gameglobal.rds.ui.loadWidget(self.widgetStoryId)

    def showLetterWidget(self, iType):
        enableInteractiveObjReward = gameglobal.rds.configData.get('enableInteractiveObjReward', False)
        if not enableInteractiveObjReward:
            return
        self.letterInteractiveType = iType
        gameglobal.rds.ui.loadWidget(self.widgetLetterId)

    def onShowKickAvatar(self, *arg):
        p = BigWorld.player()
        if p.inInteractiveObj():
            self.showInteractiveObjList(True)

    def onCloseKickWidget(self, *arg):
        self.showInteractiveObjList(False)

    def closeStoryWidget(self):
        self.storyMediator = None
        gameglobal.rds.ui.unLoadWidget(self.widgetStoryId)

    def onCloseStoryWidget(self, *arg):
        self.closeStoryWidget()

    def closeLetterWidget(self):
        self.letterMediator = None
        gameglobal.rds.ui.unLoadWidget(self.widgetLetterId)

    def onCloseLetterWidget(self, *arg):
        self.closeLetterWidget()

    def onGotoPosition(self, *arg):
        navPoint = ID.data.get(self.storyInteractiveObjId, {}).get('navPoint')
        if navPoint:
            spaceNo = BigWorld.player().mapID
            navigator.getNav().pathFinding((navPoint[0],
             navPoint[1],
             navPoint[2],
             spaceNo), None, None, True, 2, None)

    def onGetRewardTips(self, *arg):
        idx = int(arg[3][0].GetNumber())
        return uiUtils.dict2GfxDict(self.getRewardTip(idx), True)

    def onGotoMailMaid(self, *arg):
        rewardRecievepos = ICD.data.get('rewardRecievepos')
        if rewardRecievepos:
            navigator.getNav().pathFinding((rewardRecievepos[0],
             rewardRecievepos[1],
             rewardRecievepos[2],
             BigWorld.player().mapID), None, None, True, 2, None)
        self.closeLetterWidget()

    def onCloseNodeSelect(self, *arg):
        self.closeNodeSelectWidget()

    def closeNodeSelectWidget(self):
        self.nodeSelectMediator = None
        self.selectedInteractiveObjId = None
        gameglobal.rds.ui.unLoadWidget(self.widgetSelectId)

    def closeNodeSelectWidgetById(self, objId):
        if objId == self.selectedInteractiveObjId:
            self.closeNodeSelectWidget()

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == self.widgetSelectId:
            pass

    def onSubmitClick(self, *arg):
        goAwayList = uiUtils.gfxArray2Array(arg[3][0])
        if goAwayList is not None:
            ids = []
            for item in goAwayList:
                ids.append(int(item.GetNumber()))

            BigWorld.player().cell.kickoffAllSelectedInteractive(ids)
        self.showInteractiveObjList(False)

    def onCancelClick(self, *arg):
        self.showInteractiveObjList(False)

    def getInteractiveObjRoles(self, *arg):
        p = BigWorld.player()
        interactiveObjectEnt = BigWorld.entities.get(p.interactiveObjectEntId)
        others = interactiveObjectEnt.avatarMap.keys()
        ret = []
        for i in xrange(len(others)):
            tmp = {}
            otherPlayer = BigWorld.entities.get(others[i])
            if not otherPlayer:
                continue
            tmp['id'] = others[i]
            tmp['name'] = otherPlayer.roleName
            ret.append(tmp)

        return uiUtils.array2GfxAarry(ret, True)

    def onGetInteractiveNodes(self, *arg):
        interactiveObj = BigWorld.entities.get(self.selectedInteractiveObjId)
        if interactiveObj or interactiveObj.inWorld:
            indexes = interactiveObj.avatarMap.values()
            data = ID.data.get(interactiveObj.objectId, {})
            nodeName = data.get('nodeNames', ())
            ret = []
            for index, name in enumerate(nodeName):
                withAvatar = index in indexes
                ret.append((name, withAvatar))

            return uiUtils.array2GfxAarry(ret, True)
        else:
            return None

    def onSelectNode(self, *arg):
        nodeIdx = int(arg[3][0].GetNumber())
        BigWorld.player().cell.clickInteractiveObject(self.selectedInteractiveObjId, nodeIdx)
        self.closeNodeSelectWidget()

    def setRewardBarInfo(self, index, curValue, showValue):
        if self.rewardMediator:
            self.rewardMediator.Invoke('setBarInfo', (GfxValue(index), GfxValue(curValue), GfxValue(showValue)))

    def isRewardFinish(self, rType, index):
        p = BigWorld.player()
        if not hasattr(p, 'interactiveInfo'):
            return False
        if not p.interactiveInfo.has_key(rType):
            return False
        if p.interactiveInfo.get(rType).get('index') >= index:
            return True
        return False

    def getRewardTip(self, index):
        p = BigWorld.player()
        intObj = BigWorld.entities.get(p.interactiveObjectEntId)
        if not intObj or not intObj.inWorld:
            return
        rType = intObj.getType()
        typeData = ITD.data.get(rType, {})
        tip = ''
        tips = typeData.get('tips', [])
        if tips and len(tips) > index:
            tip = tips[index]
        gainState = ''
        unGainState = ''
        isRewardFinish = self.isRewardFinish(rType, index)
        isMarriage = intObj.getItemData().get('isMarriage', False)
        if not isMarriage:
            if isRewardFinish:
                gainState = gameStrings.INTERACTIVE_OBJECT_REWARD_FINISHED
            else:
                unGainState = gameStrings.INTERACTIVE_OBJECT_REWARD_WAITING
        ret = {'details': tip,
         'gainState': gainState,
         'unGainState': unGainState}
        return ret

    def playRewardGain(self, index):
        if self.rewardMediator:
            self.rewardMediator.Invoke('playRewardGain', GfxValue(index))

    def playStoryCountDown(self, second):
        if self.storyMediator:
            self.storyMediator.Invoke('countDownTimer', GfxValue(second))

    def setStoryDetail(self):
        if self.storyMediator:
            data = ID.data.get(self.storyInteractiveObjId, {})
            storyTitle = data.get('storyTitle', '')
            self.storyMediator.Invoke('setStoryTitle', GfxValue(gbk2unicode(storyTitle)))

    def showLetter(self, title, content):
        if self.letterMediator:
            self.letterMediator.Invoke('showContent', (GfxValue(gbk2unicode(title)), GfxValue(gbk2unicode(content))))
