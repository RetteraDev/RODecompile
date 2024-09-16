#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendInviteFriend.o
from gamestrings import gameStrings
import BigWorld
import const
import events
import gametypes
import utils
from asObject import ASObject
from guis import uiUtils
from guis.asObject import ASUtils
from data import school_data as SD
from data import sys_config_data as SCD
from data import friend_invitation_reward_data as FIRD

class SummonFriendInviteFriend(object):

    def __init__(self, proxy):
        super(SummonFriendInviteFriend, self).__init__()
        self.parentProxy = proxy
        self.lastSelectedFIndex = -1
        self.photoDict = {}
        self.invitedFriendList = []
        self.firstShow = True

    def getWidget(self):
        return self.parentProxy.widget

    def hideWidget(self):
        self.lastSelectedFIndex = -1
        self.invitedFriendList = []

    def showWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        self.parentProxy.updateTabBtnState()

    def refreshWidget(self):
        widget = self.getWidget()
        if not widget:
            return
        if not widget.invitePanel:
            return
        if not widget.invitePanel.friendMc:
            return
        friendMc = widget.invitePanel.friendMc
        friendMc.itemList.itemRenderer = 'SummonFriendInviteV2_PlayerItem_New'
        friendMc.itemList.lableFunction = self.lableFunPlayerIem
        friendMc.priceType0.bonusType = 'tianBi'
        friendMc.priceType1.bonusType = 'invite'
        self.refreshFriend()

    def lableFunPlayerIem(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        item.nameText.htmlText = data.name
        item.name = str(int(data.index))
        item.isOnLine.htmlText = data.stateName
        item.combatScore.htmlText = data.school
        item.lvAndSchool.htmlText = data.Lv
        item.selected = False
        item.enabled = True
        item.playerHead.playerIcon.icon.fitSize = True
        item.playerHead.playerIcon.icon.loadImage(data.photo)
        item.playerHead.gotoAndStop('stop')
        if data.state != 0:
            item.playerHead.playerIcon.gotoAndStop('normal')
        else:
            item.playerHead.playerIcon.gotoAndStop('gray')
        item.playerHead.status.gotoAndStop(data.stateName2)
        item.addEventListener(events.MOUSE_CLICK, self.onSelectFriendClick, False, 0, True)
        if self.lastSelectedFIndex >= 0:
            if int(data.index) == int(self.lastSelectedFIndex):
                item.selected = True
                item.enabled = False
                self.selectedFriendFun(item)

    def onSelectFriendClick(self, *args):
        e = ASObject(args[3][0])
        self.selectedFriendFun(e.currentTarget)

    def selectedFriendFun(self, newMC):
        widget = self.getWidget()
        if not widget:
            return
        friendMc = widget.invitePanel.friendMc
        fid = 0
        if self.lastSelectedFIndex >= 0:
            lastMC = friendMc.itemList.canvas.getChildByName('%d' % self.lastSelectedFIndex)
            if lastMC:
                lastMC.selected = False
                lastMC.enabled = True
        if newMC:
            newMC.selected = True
            newMC.enabled = False
            self.lastSelectedFIndex = int(newMC.name)
            index = int(newMC.name)
            fid = self.invitedFriendList[index]['fid']
        self.refreshRewardView(fid)

    def refreshRewardView(self, fid):
        widget = self.getWidget()
        if not widget:
            return
        friendMc = widget.invitePanel.friendMc
        rewardData = self.getRewardData(fid)
        friendInfo = self.getFriendInfo(fid)
        friendMc.headIcon.icon.fitSize = True
        friendMc.headIcon.icon.loadImage(friendInfo['photo'])
        friendMc.nameText.htmlText = friendInfo['name']
        friendMc.headIcon.status.gotoAndStop(friendInfo['stateName2'])
        ASUtils.setMcEffect(friendMc.headIcon, 'gray')
        friendMc.txtCost.visible = False
        friendMc.priceType0.visible = False
        friendMc.txtDesc0.visible = False
        friendMc.txtGained.visible = False
        friendMc.priceType1.visible = False
        friendMc.txtDesc1.visible = False
        if friendInfo['state'] == 0:
            ASUtils.setMcEffect(friendMc.headIcon, 'gray')
        else:
            ASUtils.setMcEffect(friendMc.headIcon)
        friendMc.txtCost.text = rewardData['tianBi']
        friendMc.txtGained.text = rewardData['invitePoint']
        friendMc.awardList.canvas.lvProgress.currentValue = rewardData['lvPercent'] * 100
        friendMc.awardList.canvas.scroeProgress.currentValue = rewardData['combatScorePercent'] * 100
        for i in range(len(rewardData['lvRewardList'])):
            lvRewardData = rewardData['lvRewardList'][i]
            item = friendMc.awardList.canvas.getChildByName('item%d' % i)
            combatRewardData = rewardData['combatScoreRewardList'][i]
            item.txtLv.text = 'LV.%d' % lvRewardData['needLv']
            item.txtCombatScore.text = combatRewardData['needCombatScore']
            item.txtLvReward.text = lvRewardData['rewardScore']
            item.priceType0.bonusType = 'invite'
            item.priceType1.bonusType = 'invite'
            if lvRewardData['done']:
                item.lvRule.htmlText = uiUtils.toHtml(gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_146, '#FFFFE5')
                item.txtLvReward.htmlText = uiUtils.toHtml(str(lvRewardData['rewardScore']), '#FFFFE5')
            else:
                item.lvRule.htmlText = uiUtils.toHtml(gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_146, '#CC2929')
                item.txtLvReward.htmlText = uiUtils.toHtml(str(lvRewardData['rewardScore']), '#CC2929')
            if combatRewardData['done']:
                item.txtRule2.htmlText = uiUtils.toHtml(gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_146, '#FFFFE5')
                item.txtCombatScoreReward.htmlText = uiUtils.toHtml(str(combatRewardData['rewardScore']), '#FFFFE5')
            else:
                item.txtRule2.htmlText = uiUtils.toHtml(gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_146, '#CC2929')
                item.txtCombatScoreReward.htmlText = uiUtils.toHtml(str(combatRewardData['rewardScore']), '#CC2929')

    def getRewardData(self, fid):
        rewardData = {}
        lvRewardList = []
        combatRewardList = []
        p = BigWorld.player()
        friendInfo = p.friendInviteInfo.get(fid, {})
        inviteFriendConsumeRecord = getattr(p, 'inviteFriendConsumeRecord', {})
        tianBi = inviteFriendConsumeRecord.get(fid, 0)
        factor = SCD.data.get('COIN_2_INVITE_POINT_RATIO', 0)
        invitePoint = int(tianBi * factor)
        inviteReward = p.friendInviteRewards.get(fid, {})
        lvDoneCount = 0
        combatDoneCount = 0
        for key, data in FIRD.data.iteritems():
            if data.has_key('lv'):
                lvRewardData = {}
                lvRewardData['rewardScore'] = data.get('invitePoint', 0)
                needLv = data.get('lv', 0)
                lvRewardData['needLv'] = needLv
                done = friendInfo.get('lv', 1) >= needLv
                lvRewardData['done'] = done
                lvRewardList.append(lvRewardData)
                if done:
                    lvDoneCount += 1
            if data.has_key('needCombatScore'):
                scoreRewardData = {}
                needCombatScore = data.get('needCombatScore', 0)
                scoreRewardData['needCombatScore'] = needCombatScore
                scoreRewardData['rewardScore'] = data.get('invitePoint', 0)
                done = inviteReward.has_key(key)
                scoreRewardData['done'] = done
                if done:
                    combatDoneCount += 1
                combatRewardList.append(scoreRewardData)

        lvRewardList.sort(key=lambda x: x['needLv'], reverse=True)
        combatRewardList.sort(key=lambda x: x['needCombatScore'], reverse=True)
        rewardData['lvPercent'] = lvDoneCount / (len(lvRewardList) * 1.0)
        rewardData['combatScorePercent'] = combatDoneCount / (len(combatRewardList) * 1.0)
        rewardData['lvRewardList'] = lvRewardList
        rewardData['combatScoreRewardList'] = combatRewardList
        rewardData['tianBi'] = tianBi
        rewardData['invitePoint'] = invitePoint
        return rewardData

    def refreshFriend(self):
        widget = self.getWidget()
        if not widget:
            return
        self.lastSelectedFIndex = -1
        playerData = self.getSummedPlayersData()
        self.refreshSummedPlyaers(playerData)

    def refreshSummedPlyaers(self, playersData):
        widget = self.getWidget()
        if not widget:
            return
        else:
            friendMc = widget.invitePanel.friendMc
            friendMc.total.text = '%d/%d' % (playersData['onlineCount'], playersData['totalCount'])
            plyerList = playersData['playerList']
            if len(plyerList) > 0:
                if self.lastSelectedFIndex == -1:
                    self.lastSelectedFIndex = plyerList[0]['index']
            else:
                self.selectedFriendFun(None)
            friendMc.itemList.dataArray = plyerList
            return

    def getSummedPlayersData(self):
        data = {}
        list = []
        onlineCount = 0
        totalCount = 0
        p = BigWorld.player()
        for fid in p.friendInviteInfo:
            if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_BUILD or p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP and fid in p.friendInvitees:
                friendInfo = self.getFriendInfo(fid)
                friendInfo['index'] = totalCount
                if friendInfo['state'] in (1, 2, 3):
                    onlineCount += 1
                totalCount += 1
                list.append(friendInfo)

        self.invitedFriendList = list[:]
        list.sort(cmp=self.cmpFriend)
        data['playerList'] = list
        data['onlineCount'] = onlineCount
        data['totalCount'] = totalCount
        return data

    def cmpFriend(self, x, y):
        p = BigWorld.player()
        xFid = int(x['fid'])
        yFid = int(y['fid'])
        xLv = p.friendInviteInfo[xFid].get('lv', 1)
        yLv = p.friendInviteInfo[yFid].get('lv', 1)
        xNums = self.getCanGetRewardNums(xFid)
        yNums = self.getCanGetRewardNums(yFid)
        onLineCmp = cmp(p.friendInviteInfo[yFid].get('on', False), p.friendInviteInfo[xFid].get('on', False))
        if onLineCmp == 0:
            numsCmp = cmp(yNums, xNums)
            if numsCmp == 0:
                lvCmp = cmp(yLv, xLv)
                return lvCmp
            else:
                return numsCmp
        else:
            return onLineCmp
        return 0

    def getCanGetRewardNums(self, fid):
        rewardData = self.getRewardData(fid)
        reward = rewardData['lvPercent'] + rewardData['combatScorePercent']
        return reward

    def getFriendInfo(self, fid):
        p = BigWorld.player()
        friendInfo = {}
        friendInfo['fid'] = fid
        inviteInfo = p.friendInviteInfo.get(fid, {})
        friendInfo['name'] = utils.getDisplayName(inviteInfo.get('playerName', ''))
        stateMap = {0: gameStrings.TEXT_UIUTILS_1414,
         1: gameStrings.TEXT_FRIENDPROXY_293_1,
         2: gameStrings.TEXT_FRIENDPROXY_293_2,
         3: gameStrings.TEXT_FRIENDPROXY_293_3,
         4: gameStrings.TEXT_FRIENDPROXY_293_4}
        stateMap2 = {0: 'online',
         1: 'online',
         2: 'busy',
         3: 'leave',
         4: 'hide'}
        if inviteInfo.get('on', ''):
            friendInfo['state'] = 1
        else:
            friendInfo['state'] = 0
        friendInfo['stateName'] = stateMap[friendInfo['state']]
        if inviteInfo.get('status', 0) == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP:
            friendInfo['stateName'] = gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_299
        friendInfo['stateName2'] = stateMap2[friendInfo['state']]
        friendInfo['combatScore'] = 0
        school = inviteInfo.get('school', 3)
        schoolName = SD.data.get(school, {}).get('name', '')
        lv = inviteInfo.get('lv', 1)
        friendInfo['school'] = schoolName
        friendInfo['Lv'] = 'Lv.%d' % lv
        sex = inviteInfo.get('sex', 1)
        if inviteInfo.get('profileIcon', ''):
            photo = inviteInfo.get('profileIcon', '')
        else:
            photo = 'headIcon/%s.dds' % str(school * 10 + sex)
        if uiUtils.isDownloadImage(photo):
            if self.photoDict.has_key(fid):
                photo = self.photoDict[fid]
            else:
                p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadOtherPhoto, (friendInfo.get('fid', 0), photo))
                photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
        friendInfo['photo'] = photo
        return friendInfo

    def onDownloadOtherPhoto(self, status, fid, photoName):
        photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photoName + '.dds'
        self.photoDict[fid] = photo
        self.refreshFriend()
