#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spriteChallengeResultProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import formula
from guis import uiUtils
import uiConst
import gametypes
import const
import utils
from guis.asObject import ASUtils
from fbStatistics import FubenStats
from guis import events
from guis import menuManager
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis import spriteChallengeHelper
from data import sprite_challenge_config_data as SCCD
from data import summon_sprite_info_data as SSID
from gamestrings import gameStrings
from callbackHelper import Functor
MAX_NUM_PALYER = 5
MAX_NUM_SPRITE = 4
ASK_CONFIRM_TIME = 120

class SpriteChallengeResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SpriteChallengeResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.isGetReward = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPRITE_CHALLENGE_RESULT, self.hide)

    def reset(self):
        self.isGetReward = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SPRITE_CHALLENGE_RESULT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SPRITE_CHALLENGE_RESULT)
        self.reset()

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SPRITE_CHALLENGE_RESULT)

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onCloseBtnClick)
        self.widget.retryBtn.addEventListener(events.BUTTON_CLICK, self.onRetryBtnClick)
        self.widget.nextBtn.addEventListener(events.BUTTON_CLICK, self.onNextBtnClick)
        self.widget.leaveBtn.addEventListener(events.BUTTON_CLICK, self.onLeaveBtnClick)
        self.widget.boxBtn.addEventListener(events.BUTTON_CLICK, self.onBoxBtnClick)
        self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick)
        self.widget.friendRankBtn.addEventListener(events.BUTTON_CLICK, self.onFriendRankBtnClick)
        ASUtils.callbackAtFrame(self.widget, 49, self.refreshBoxState)
        ASUtils.callbackAtFrame(self.widget, 53, self.refreshBoxState)
        ASUtils.callbackAtFrame(self.widget, 54, self.refreshBoxState)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        spriteChallengeResult = getattr(p, 'spriteChallengeResult', {})
        self.widget.difficulty.textField.text = spriteChallengeResult.get('progress', 0)
        progress = spriteChallengeResult.get('progress', 0)
        topRank = spriteChallengeResult.get('topRank', 0)
        if topRank > 0:
            self.widget.rankValue.rankText.text = spriteChallengeHelper.getInstance().getFakeRankStr(topRank)
            self.widget.rankValue.noneRank.visible = False
        else:
            self.widget.rankValue.rankText.text = ''
            self.widget.rankValue.noneRank.visible = True
        result = spriteChallengeResult.get('result', False)
        if result:
            self.widget.resultState.gotoAndStop('success')
            self.widget.timeText.gotoAndStop('success')
            self.widget.nextBtn.label = gameStrings.SPRITE_CHALLENGE_NEXT_LEVEL
            if progress >= spriteChallengeHelper.getInstance().getMaxProgress(spriteChallengeHelper.getInstance().getSelfLvKey()):
                self.widget.nextBtn.enabled = False
            else:
                self.widget.nextBtn.enabled = True
        else:
            self.widget.resultState.gotoAndStop('fail')
            self.widget.timeText.gotoAndStop('fail')
            self.widget.nextBtn.label = gameStrings.SPRITE_CHALLENGE_PREV_LEVEL
            if progress > 1:
                self.widget.nextBtn.enabled = True
            else:
                self.widget.nextBtn.enabled = False
        self.widget.timeText.textField.text = self.formateTime(spriteChallengeResult.get('useTime', 0))
        self.refreshRankList()
        self.refreshRewardMc()
        self.refreshBoxState()
        self.refreshSpriteList()

    def isSucess(self):
        p = BigWorld.player()
        spriteChallengeResult = getattr(p, 'spriteChallengeResult', {})
        result = spriteChallengeResult.get('result', False)
        return result

    def isRewardGeted(self):
        remainTime = spriteChallengeHelper.getInstance().getRemainRewardTime()
        return self.isGetReward or remainTime <= 0

    def refreshBoxState(self, *args):
        if not self.widget:
            return
        if self.isRewardGeted():
            self.widget.boxBtn.selected = True
            self.widget.boxBtn.enabled = False
        else:
            self.widget.boxBtn.selected = False
            if self.isSucess():
                self.widget.boxBtn.enabled = True
            else:
                self.widget.boxBtn.enabled = False
        self.widget.boxBtn.validateNow()

    def onBoxBtnClick(self, *args):
        p = BigWorld.player()
        if self.isRewardGeted():
            return
        spriteChallengeResult = getattr(p, 'spriteChallengeResult', {})
        result = spriteChallengeResult.get('result', False)
        if not result:
            return
        useTime = spriteChallengeResult.get('useTime', 0)
        if useTime < ASK_CONFIRM_TIME:
            msg = gameStrings.ZMJ_ASK_REWARD_CONFIRM
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.getSpriteChallengeSuccReward, spriteChallengeHelper.getInstance().getSelfLvKeyStr()), yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1)
        else:
            p.base.getSpriteChallengeSuccReward(spriteChallengeHelper.getInstance().getSelfLvKeyStr())

    def refreshRewardMc(self):
        if not self.widget:
            return
        rewardMc = self.widget.rewardMc
        remainTime = spriteChallengeHelper.getInstance().getRemainRewardTime()
        rewardMc.amount.text = remainTime
        tipText = SCCD.data.get('SpriteChallengeRewardRemainTip', 'remain:%d')
        TipManager.addTip(rewardMc.rewardIcon, tipText % remainTime)
        rewardMc.rewardBtn.addEventListener(events.BUTTON_CLICK, self.onRewardBtnClick)

    def onRewardBtnClick(self, *args):
        p = BigWorld.player()
        spriteChallengeResult = getattr(p, 'spriteChallengeResult', {})
        gameglobal.rds.ui.spriteChallengeRewardQuery.show(spriteChallengeHelper.getInstance().getSelfLvKey(), spriteChallengeResult.get('progress', 0))

    def sortSpriteKeys(self, spriteIndexs):
        attendList, _, _ = spriteChallengeHelper.getInstance().getAttendAndCheckList(len(spriteIndexs))
        if len(spriteIndexs) != len(attendList):
            return spriteIndexs
        for spriteIdx in spriteIndexs:
            if spriteIdx not in attendList:
                return spriteIndexs

        return attendList

    def refreshSpriteList(self):
        if not self.widget:
            return
        p = BigWorld.player()
        spriteChallengeStats = getattr(p, 'resultSpriteChallengeStats', {})
        totalDamage = sum([ recordInfo.get(FubenStats.K_SPRITE_DAMAGE, 0) for recordInfo in spriteChallengeStats.values() ])
        totalBeDamage = sum([ recordInfo.get(FubenStats.K_SPRITE_BE_DAMAGE, 0) for recordInfo in spriteChallengeStats.values() ])
        spriteIndexs = spriteChallengeStats.keys()
        spriteIndexs = self.sortSpriteKeys(spriteIndexs)
        for i in xrange(MAX_NUM_SPRITE):
            spriteMc = self.widget.getChildByName('sprite%d' % i)
            if i < len(spriteIndexs):
                spriteIdx = spriteIndexs[i]
                spriteInfo = p.summonSpriteList.get(spriteIdx, {})
                recordInfo = spriteChallengeStats.get(spriteIdx, {})
                if spriteInfo:
                    damage = recordInfo.get(FubenStats.K_SPRITE_DAMAGE, 0)
                    beDamege = recordInfo.get(FubenStats.K_SPRITE_BE_DAMAGE, 0)
                    dmgRate = damage * 100.0 / totalDamage if totalDamage else 0
                    beDmgRate = beDamege * 100.0 / totalBeDamage if totalBeDamage else 0
                    spriteId = spriteInfo.get('spriteId', 0)
                    ssidData = SSID.data.get(spriteId, {})
                    iconId = ssidData.get('spriteIcon', '000')
                    spriteName = spriteInfo.get('name', '')
                    spriteMc.visible = True
                    spriteMc.nameText.text = spriteName
                    iconPath = uiConst.SPRITE_ICON_PATH % str(iconId)
                    spriteMc.icon.fitSize = True
                    spriteMc.icon.loadImage(iconPath)
                    spriteMc.dmgText.text = utils.convertNum(damage)
                    spriteMc.dmgRate.text = '%.1f%%' % dmgRate
                    spriteMc.dmgBar.currentValue = dmgRate
                    spriteMc.takeDmgText.text = utils.convertNum(beDamege)
                    spriteMc.takeDmgRate.text = '%.1f%%' % beDmgRate
                    spriteMc.takeDmgBar.currentValue = beDmgRate
                else:
                    spriteMc.visible = False
            else:
                spriteMc.visible = False

    def sortFunc(self, rankInfo1, rankInfo2):
        diffIdx1, timeCost1, timeStamp1 = rankInfo1[0], rankInfo1[1], rankInfo1[2]
        diffIdx2, timeCost2, timeStamp2 = rankInfo2[0], rankInfo2[1], rankInfo2[2]
        if diffIdx1 != diffIdx2:
            return -cmp(diffIdx1, diffIdx2)
        if timeCost1 != timeCost2:
            return cmp(timeCost1, timeCost2)
        return cmp(timeStamp1, timeStamp2)

    def refreshRankList(self):
        p = BigWorld.player()
        resultData = getattr(p, 'spriteChallengeResult', {})
        ranks = resultData.get('friendTopInfo', [])
        ranks.sort(cmp=self.sortFunc)
        newFriendRank = resultData.get('newFriendRank', 0)
        oldFriendRank = resultData.get('oldFriendRank', 0)
        topInfo = []
        index = -1
        lastInfo = {}
        for rankInfo in ranks:
            gbId, diffIdx, timeCost, timeStamp = (rankInfo[7],
             rankInfo[0],
             rankInfo[1],
             rankInfo[2])
            isRankSame = False
            if lastInfo and rankInfo and lastInfo[1] == rankInfo[1] and lastInfo[2] == rankInfo[2]:
                if lastInfo[0] == rankInfo[0]:
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
                playerMc.useTime.text = self.formateTime(tInfo.get('timeCost', 0))
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

    def formateTime(self, time):
        return utils.formatTimeStr(time, 'h:m:s', True, 2, 2, 2)

    def onCloseBtnClick(self, *args):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.SPRITE_CHALLENGE_QUIT_CONFIRM, self.quitFb, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1)

    def onRetryBtnClick(self, *args):
        p = BigWorld.player()
        spriteChallengeResult = getattr(p, 'spriteChallengeResult', {})
        progress = spriteChallengeResult.get('progress', 0)
        spriteChallengeHelper.getInstance().startLevel(progress)

    def onNextBtnClick(self, *args):
        p = BigWorld.player()
        spriteChallengeResult = getattr(p, 'spriteChallengeResult', {})
        result = spriteChallengeResult.get('result', True)
        if result:
            progress = spriteChallengeResult.get('progress', 0)
            spriteChallengeHelper.getInstance().startLevel(progress + 1)
        else:
            progress = spriteChallengeResult.get('progress', 0)
            spriteChallengeHelper.getInstance().startLevel(progress - 1)

    def onLeaveBtnClick(self, *args):
        p = BigWorld.player()
        if p.inFuben() and not p.inFubenTypes(const.FB_TYPE_ARENA):
            menuManager.getInstance().leaveFuben()

    def onRankBtnClick(self, *args):
        gameglobal.rds.ui.ranking.show(gametypes.TOP_TYPE_SPRITE_CHALLENGE, isCommonRank=True)

    def onFriendRankBtnClick(self, *args):
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_SPRITE_CHALLENGE_FRIEND)

    def quitFb(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        fbType = formula.whatFubenType(fbNo)
        menuManager.getInstance().confirmOK(fbType)
        self.hide()
