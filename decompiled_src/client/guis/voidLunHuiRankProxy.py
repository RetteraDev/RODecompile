#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidLunHuiRankProxy.o
import BigWorld
import gameglobal
import uiConst
import formula
import const
import gametypes
import utils
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASUtils
from guis import events
from guis.asObject import TipManager
from guis import voidLunHuiHelper
from data import team_endless_config_data as TECD
from data import fb_data as FD
MAX_NUM_PALYER = 5

class VoidLunHuiRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoidLunHuiRankProxy, self).__init__(uiAdapter)
        self.widget = None
        self.fbId = 0
        self.rank = 0
        self.lvKey = 0
        self.diffIdx = 0
        self.timeCost = 0
        self.rewardGeted = False
        self.isSucess = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_LUNHUI_RANK, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_LUNHUI_RANK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VOID_LUNHUI_RANK)

    def show(self, resultData = None):
        self.removePushMsg()
        if resultData:
            self.resultData = resultData
            self.fbId = self.resultData.get('fbNo', 0)
            self.diffIdx = self.resultData.get('teamEndlessLv', 0)
            self.isSucess = self.resultData.get('isOk', False)
            self.timeCost = self.resultData.get('timeCost', 0)
            self.rank = self.resultData.get('rank', 0)
            self.rewardGeted = False
            self.lvKey = voidLunHuiHelper.getInstance().getLvKey(self.fbId)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_VOID_LUNHUI_RANK)

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onCloseBtnClick)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onCloseBtnClick)
        self.widget.rewardMc.rewardBtn.addEventListener(events.BUTTON_CLICK, self.onRewardBtnClick)
        self.widget.boxBtn.addEventListener(events.BUTTON_CLICK, self.onBoxBtnClick)
        self.widget.friendRankBtn.addEventListener(events.BUTTON_CLICK, self.onFriendRankBtnClick)
        self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick)
        self.widget.boxBtn.cacheAsBitmap = True
        ASUtils.callbackAtFrame(self.widget, 53, self.setBoxData)

    def setBoxData(self, *args):
        self.widget.boxBtn.cacheAsBitmap = True
        self.refreshBoxState()

    def updateTimeStr(self, sec):
        if sec >= 14400:
            sec = 0
        return utils.formatTimeStr(sec, 'h:m:s', True, 2, 2, 2)

    def isOverTime(self):
        return not self.isSucess or self.timeCost > FD.data.get(self.fbId, {}).get('teamEndlessDuration', 0)

    def onBoxBtnClick(self, *args):
        p = BigWorld.player()
        p.base.takeTeamEndlessLevelReward(self.lvKey, self.diffIdx)

    def onFriendRankBtnClick(self, *args):
        gameglobal.rds.ui.rankCommon.hide()
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_FRIEND_TEAM_ENDLESS, voidLunHuiHelper.getInstance().getRankDropDownKey())

    def onRewardBtnClick(self, *args):
        gameglobal.rds.ui.voidLunHuiRewardQuery.show(self.lvKey, self.diffIdx)

    def onRankBtnClick(self, *args):
        gameglobal.rds.ui.ranking.show(gametypes.TOP_TYPE_TEAM_ENDLESS, isCommonRank=True)

    def onGetReward(self, lvType, teamEndlessLv):
        self.rewardGeted = True
        self.refreshRewardState()
        self.refreshBoxState()

    def refreshBoxState(self):
        if not self.widget:
            return
        if self.rewardGeted:
            self.widget.boxBtn.selected = True
        else:
            self.widget.boxBtn.selected = False

    def refreshRewardState(self):
        if not self.widget:
            return
        if self.rewardGeted:
            ASUtils.setHitTestDisable(self.widget.boxBtn, True)
        else:
            ASUtils.setHitTestDisable(self.widget.boxBtn, False)
        lvKey = self.lvKey
        remainTime = voidLunHuiHelper.getInstance().getRemainRewardTime(lvKey)
        if remainTime <= 0 or self.rewardGeted:
            self.widget.boxBtn.enabled = False
        else:
            self.widget.boxBtn.enabled = True
        self.widget.rewardMc.amount.text = remainTime
        tipText = TECD.data.get('teamEndlessRewardRemainTip', 'remain:%d')
        TipManager.addTip(self.widget.rewardMc.rewardIcon, tipText % remainTime)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.fbName.nameText.textField.text = FD.data.get(self.fbId, {}).get('name', '')
        if self.isOverTime():
            self.widget.evaluate.gotoAndStop('fail')
            self.widget.resultState.gotoAndStop('fail')
        else:
            self.widget.evaluate.gotoAndStop('success')
            self.widget.resultState.gotoAndStop('success')
        self.widget.evaluate.textField.text = self.updateTimeStr(self.timeCost)
        self.widget.score.textField.text = str(self.diffIdx)
        if self.rank:
            self.widget.rankValue.noneRank.visible = False
            self.widget.rankValue.rankText.visible = True
            self.widget.rankValue.rankText.text = self.rank
        else:
            self.widget.rankValue.noneRank.visible = True
            self.widget.rankValue.rankText.visible = False
        self.refreshRankList()
        self.refreshRewardState()

    def refreshRankList(self):
        p = BigWorld.player()
        ranks = self.resultData.get('friends', [])
        newFriendRank = self.resultData.get('curFriendRank', 0)
        oldFriendRank = self.resultData.get('lastFriendRank', 0)
        topInfo = []
        index = -1
        lastInfo = {}
        for rankInfo in ranks:
            gbId, diffIdx, timeCost, timeStamp = rankInfo
            isRankSame = False
            if lastInfo and rankInfo and lastInfo[1] == rankInfo[1] and lastInfo[2] == rankInfo[2]:
                if lastInfo[3] == rankInfo[3]:
                    isRankSame = True
            if not isRankSame:
                index += 1
            if gbId == p.gbId:
                info = {'gbId': gbId,
                 'name': p.roleName,
                 'photo': p._getFriendPhoto(p),
                 'diffIdx': diffIdx,
                 'timeCost': timeCost,
                 'rank': newFriendRank - 1}
                topInfo.append(info)
            else:
                friendVal = p.friend.get(gbId, {})
                if friendVal:
                    info = {'gbId': gbId,
                     'name': friendVal.name,
                     'photo': p._getFriendPhoto(friendVal),
                     'diffIdx': diffIdx,
                     'timeCost': timeCost,
                     'rank': index}
                    topInfo.append(info)
            lastInfo = rankInfo

        p = BigWorld.player()
        for i in range(MAX_NUM_PALYER):
            playerMc = self.widget.getChildByName('player%d' % i)
            if i < len(topInfo):
                tInfo = topInfo[i]
                playerMc.visible = True
                rank = tInfo.get('rank', 0)
                if p.gbId == int(tInfo.get('gbId', 0)):
                    playerMc.gotoAndStop('me')
                    playerMc.rankText.text = rank + 1
                    playerMc.upIcon.visible = False
                    if newFriendRank < oldFriendRank:
                        playerMc.upIcon.visible = True
                else:
                    playerMc.gotoAndStop('friend')
                    playerMc.upIcon.visible = False
                    playerMc.rankText.text = rank + 1
                photo = tInfo.get('photo', '')
                if uiUtils.isDownloadImage(photo):
                    playerMc.playerIcon.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
                    playerMc.playerIcon.icon.fitSize = True
                    playerMc.playerIcon.icon.url = photo
                else:
                    playerMc.playerIcon.icon.clear()
                    playerMc.playerIcon.icon.fitSize = True
                    playerMc.playerIcon.icon.loadImage(photo)
                playerMc.playerName.text = tInfo.get('name', '')
                playerMc.diffScore.text = tInfo.get('diffIdx', '')
                playerMc.useTime.text = self.updateTimeStr(tInfo.get('timeCost', 0))
                if rank == 0:
                    playerMc.rankText.visible = False
                    playerMc.rankIcon.gotoAndStop('gold')
                elif rank == 1:
                    playerMc.rankText.visible = False
                    playerMc.rankIcon.gotoAndStop('silver')
                elif rank == 2:
                    playerMc.rankText.visible = False
                    playerMc.rankIcon.gotoAndStop('copper')
                else:
                    playerMc.rankText.visible = True
                    playerMc.rankIcon.visible = False
            else:
                playerMc.visible = False

    def onCloseBtnClick(self, *args):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_LUNHUI_RANK)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_LUNHUI_RANK, {'click': self.onPushMsgClick})
        self.hide()

    def onPushMsgClick(self):
        self.show()

    def removePushMsg(self):
        if uiConst.MESSAGE_TYPE_LUNHUI_RANK in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_LUNHUI_RANK)

    def clearAll(self):
        self.hide()
        self.removePushMsg()
