#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendRecall.o
import BigWorld
import gameglobal
import events
import clientUtils
import gametypes
import const
import utils
import time
from asObject import ASObject
from gameStrings import gameStrings
from guis import uiConst
from guis import menuManager
from guis import uiUtils
from guis.asObject import ASUtils
from guis.asObject import MenuManager
from data import friend_recall_task_data as FRTD
from data import friend_recall_data as FRD
from data import sys_config_data as SCD
AD_ICON_TEMPLATE = 'advertisement/%s.dds'

class SummonFriendRecall(object):

    def __init__(self, proxy):
        super(SummonFriendRecall, self).__init__()
        self.parentProxy = proxy
        self.curSelGbId = 0

    def getWidget(self):
        return self.parentProxy.widget

    def hideWidget(self):
        self.reset()

    def reset(self):
        self.curSelGbId = 0

    def showWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        self.reset()
        self.parentProxy.updateTabBtnState()

    def refreshWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        recallMc = widget.recallFriendPanel.recallMc
        recallMc.getBtn.addEventListener(events.MOUSE_CLICK, self.handleGetRewardBtnClick, False, 0, True)
        recallMc.playerName.text = ''
        recallMc.scrollListL.itemRenderer = 'SummonFriendBackV2_recallItem'
        recallMc.scrollListL.dataArray = []
        recallMc.scrollListL.lableFunction = self.itemFunctionL
        recallMc.scrollListL.validateNow()
        recallMc.scrollListR.itemRenderer = 'SummonFriendBackV2_targetItem'
        recallMc.scrollListR.dataArray = []
        recallMc.scrollListR.lableFunction = self.itemFunctionR
        recallMc.scrollListR.validateNow()
        self.refreshRecallFriend()

    def refreshRecallFriend(self):
        widget = self.getWidget()
        if not widget:
            return
        if not widget.recallFriendPanel:
            return
        recallMc = widget.recallFriendPanel.recallMc
        friendList = self.filterFriends()
        recallMc.scrollListL.dataArray = friendList
        recallMc.scrollListL.validateNow()
        self.updateRewardBar()

    def handleGetRewardBtnClick(self, *args):
        p = BigWorld.player()
        p.base.receiveFriendRecallReward()

    def handleSendBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        itemMc = target.parent
        if not self.curSelGbId:
            return
        gbId = int(self.curSelGbId)
        p = BigWorld.player()
        if itemMc.recallType == gametypes.FRIEND_RECALL_TASK_TYPE_RECALLED:
            p.base.sendRecallRequest(gbId)
        elif itemMc.recallType == gametypes.FRIEND_RECALL_TASK_TYPE_SIGN_IN:
            gameglobal.rds.ui.friend.beginChat(gbId)
        elif itemMc.recallType in gametypes.FRIEND_RECALL_TASK_TYPE_FOR_QUESTLOOP:
            fVal = p.getFValByGbId(gbId)
            if fVal:
                menuManager.getInstance().menuTarget.apply(roleName=fVal.name)
                menuManager.getInstance().inviteTeam()

    def handleSelDown(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.selected:
            return
        target.selected = True
        self.curSelGbId = target.gbId
        self.updateTasks()

    def itemFunctionL(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.groupName = 'empty'
        itemMc.groupName = 'summonFriendRecalls%s'
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleSelDown, False, 0, True)
        MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_TARGET, {'roleName': itemData.name,
         'gbId': itemData.gbId})
        itemMc.gbId = itemData.gbId
        itemMc.headIcon.gotoAndStop('stop')
        itemMc.headIcon.playerIcon.icon.fitSize = True
        itemMc.headIcon.playerIcon.icon.loadImage(itemData.photo)
        if itemData.state != 0:
            itemMc.headIcon.playerIcon.gotoAndStop('normal')
        else:
            itemMc.headIcon.playerIcon.gotoAndStop('gray')
        itemMc.nameText.text = itemData.name
        itemMc.familiarVal.text = gameStrings.SUMMON_FRIEND_RECALL_FAMILIAR % itemData.intimacy
        itemMc.lv.text = 'Lv %d' % itemData.level
        itemMc.onLine.text = gameStrings.PLAYER_STATE_MPA[itemData.state]
        itemMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(itemData.school, ''))
        itemMc.disabled = itemData.state != 1
        itemMc.selected = False
        if not self.curSelGbId:
            itemMc.selected = True
        elif self.curSelGbId and self.curSelGbId == itemData.gbId:
            itemMc.selected = True
        if itemMc.selected:
            self.curSelGbId = itemData.gbId
            self.updateTasks()

    def itemFunctionR(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.recallType = itemData.recallType
        itemMc.recallTaskId = itemData.recallTaskId
        itemMc.targetTxt.text = itemData.desc
        itemMc.pointVal.text = itemData.score
        itemMc.finishIcon.visible = itemData.finishState
        itemMc.sendMsgBtn.enabled = not itemData.finishState
        itemMc.sendMsgBtn.label = itemData.btnDesc
        itemMc.pointIcon.bonusType = 'recall'
        itemMc.sendMsgBtn.addEventListener(events.MOUSE_CLICK, self.handleSendBtnClick, False, 0, True)

    def filterFriends(self):
        p = BigWorld.player()
        alreadyRecall = []
        canReacll = []
        finishTaskRecall = []
        maxTaskNum = len(FRTD.data.keys())
        friendList = sorted(p.friend.values(), key=lambda d: d.intimacy, reverse=True)
        for fVal in friendList:
            recallState = fVal.recallState
            recallInfo = fVal.recallInfo
            if recallState == gametypes.FRIEND_RECALL_STATE_CAN_BE_RECALLED:
                canReacll.append(fVal)
            elif recallState == gametypes.FRIEND_RECALL_STATE_ALREADY_RECALLED:
                recallFinishTaskIds = recallInfo.get('recallFinishTaskIds', [])
                if len(recallFinishTaskIds) < maxTaskNum:
                    alreadyRecall.append(fVal)
                else:
                    finishTaskRecall.append(fVal)

        allRecall = alreadyRecall + canReacll + finishTaskRecall
        itemList = []
        for fVal in allRecall:
            itemInfo = {}
            itemInfo['gbId'] = fVal.gbId
            itemInfo['name'] = fVal.name
            itemInfo['level'] = fVal.level
            itemInfo['intimacy'] = fVal.intimacy
            photo = fVal.photo if fVal.photo else p._getFriendPhoto(fVal, fVal.school, fVal.sex)
            if uiUtils.isDownloadImage(photo):
                if p.isGlobalFriendVal(fVal):
                    p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, int(p.globalFriends.friends.get(fVal.gbId).server), gametypes.NOS_FILE_PICTURE, None, (None,))
                else:
                    p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, None, (None,))
                photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
            itemInfo['photo'] = photo
            itemInfo['state'] = fVal.state
            itemInfo['school'] = fVal.school
            itemList.append(itemInfo)

        return itemList

    def updateTasks(self):
        widget = self.getWidget()
        if not widget:
            return
        p = BigWorld.player()
        fVal = p.getFValByGbId(int(self.curSelGbId))
        if not fVal:
            return
        recallFinishTaskIds = fVal.recallInfo.get('recallFinishTaskIds', [])
        noFinishTasks = []
        finishTasks = []
        for key, value in FRTD.data.iteritems():
            if key in recallFinishTaskIds:
                finishTasks.append([key, value])
            else:
                noFinishTasks.append([key, value])

        allTasks = noFinishTasks + finishTasks
        itemList = []
        for key, value in allTasks:
            itemInfo = {}
            itemInfo['recallTaskId'] = key
            itemInfo['recallType'] = value.get('type', '')
            itemInfo['desc'] = value.get('desc', '')
            itemInfo['finishState'] = key in recallFinishTaskIds
            itemInfo['score'] = value.get('score', 0)
            itemInfo['btnDesc'] = value.get('btnDesc', '')
            itemList.append(itemInfo)

        recallMc = widget.recallFriendPanel.recallMc
        recallMc.playerName.text = fVal.name
        recallMc.scrollListR.dataArray = itemList
        recallMc.scrollListR.validateNow()

    def updateRewardBar(self):
        widget = self.getWidget()
        if not widget:
            return
        if not widget.recallFriendPanel:
            return
        recallMc = widget.recallFriendPanel.recallMc
        p = BigWorld.player()
        myScore = p.friendRecallStatics.get('totalScore', 0)
        finishRewardScroreBonusIds = p.friendRecallStatics.get('finishRewardScroreBonusIds', [])
        frdData = FRD.data.get(SCD.data.get('friendRecallActivityId', gametypes.FRIEND_RECALL_ID), {})
        bannerIconPath = AD_ICON_TEMPLATE % frdData.get('bannerIconId', 10086)
        recallMc.bannerIcon.fitSize = True
        recallMc.bannerIcon.loadImage(bannerIconPath)
        endTime = frdData.get('crontabEnd', 0)
        crontab = utils.getDisposableCronTabTimeStamp(endTime)
        recallMc.endTime.text = gameStrings.SUMMON_FIREND_RECALL_ENDTIME % time.strftime('%m/%d %H:%M', time.localtime(crontab))
        scoreMargins = frdData.get('scoreMargins', [])
        recallMc.recallVal.text = gameStrings.SUMMON_FRIEND_RECALLED_POINT % myScore
        pointPartVal = []
        prePointVal = 0
        for pointVal in scoreMargins:
            maxPartVal = pointVal - prePointVal
            curVal = maxPartVal if myScore >= pointVal else max(0, myScore - prePointVal)
            pointPartVal.append([curVal, maxPartVal])
            prePointVal = pointVal

        pointNum = len(scoreMargins)
        for i in xrange(pointNum):
            rewardItem = recallMc.getChildByName('item%d' % i)
            pointBar = recallMc.getChildByName('pointBar%d' % i)
            bonusIds = frdData.get('bonusIds', [])
            bonusId = bonusIds[i] if i < len(bonusIds) else 0
            itemBonus = clientUtils.genItemBonus(bonusId)
            itemId, num = itemBonus[0] if itemBonus else (0, 0)
            itemInfo = uiUtils.getGfxItemById(itemId, num)
            rewardItem.slot.fitSize = True
            rewardItem.slot.dragable = False
            rewardItem.slot.setItemSlotData(itemInfo)
            rewardItem.getedPic.visible = False
            ASUtils.setHitTestDisable(rewardItem.getedPic, True)
            rewardItem.effect.visible = False
            ASUtils.setHitTestDisable(rewardItem.effect, True)
            rewardItem.slot.setSlotState(uiConst.ITEM_NORMAL)
            if bonusId in finishRewardScroreBonusIds:
                rewardItem.getedPic.visible = True
                rewardItem.slot.setSlotState(uiConst.ITEM_GRAY)
            else:
                iScore = scoreMargins[i] if i < len(scoreMargins) else 0
                rewardItem.effect.visible = True if myScore >= iScore else False
            rewardItem.coinIcon.bonusType = 'recall'
            score = scoreMargins[i] if i < len(scoreMargins) else 0
            rewardItem.coinVal.text = score
            pointBar.maxValue = pointPartVal[i][1]
            pointBar.currentValue = pointPartVal[i][0]

        getedRewards = len(finishRewardScroreBonusIds)
        nextPoint = 0
        if getedRewards + 1 <= len(scoreMargins):
            nextPoint = scoreMargins[getedRewards]
        recallMc.getBtn.enabled = True if myScore and nextPoint and myScore >= nextPoint else False
