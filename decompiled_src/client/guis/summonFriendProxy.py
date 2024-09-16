#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import utils
import uiUtils
import qrcode
import base64
import ui
import const
import keys
import clientUtils
from callbackHelper import Functor
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import messageBoxProxy
from ui import gbk2unicode
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import school_data as SD
from data import friend_invitation_reward_data as FIRD
from data import invitation_extra_reward_data as IERD
from data import flowback_invite_data as FID
from data import game_msg_data as GMD
AD_ICON_TEMPLATE = 'advertisement/%s.dds'

class SummonFriendProxy(SlotDataProxy):
    UN_COMPLETE = 1
    COMPLETE = 2
    DONE = 3

    def __init__(self, uiAdapter):
        super(SummonFriendProxy, self).__init__(uiAdapter)
        self.modelMap = {'getIWantSummonData': self.onGetIWantSummonData,
         'copyWebToClipBoard': self.onCopyWebToClipBoard,
         'copyMyCodeToClipBoard': self.onCopyMyCodeToClipBoard,
         'sendEmail': self.onSendEmail,
         'refreshSummonedPlayerInfo': self.onGetSummonedPlayerInfo,
         'selectFriend': self.onSelectFriend,
         'refreshBeSummonedPlayerInfo': self.onRefreshBeSummonedPlayerInfo,
         'sendConfirmBind': self.onSendConfirmBind,
         'addFriend': self.onAddFriend,
         'getAwardSp': self.onGetAwardSp,
         'getAward': self.onGetAward,
         'getSelectTab': self.onGetSelectTab,
         'setSelectedTab': self.onSetSelectedTab,
         'getSummonActivities': self.onGetSummonActivities,
         'getActivityReward': self.onGetActivityReward,
         'enableActivity': self.onEnableActivity,
         'enableMyInvitor': self.onEnableMyInvitor,
         'getDefaultRewardList': self.onGetDefaultRewardList,
         'getSummonRewards': self.onGetSummonRewards,
         'wantCall': self.onWantCall,
         'tab5Reward': self.onTab5Reward,
         'enableOfflineFlowback': self.onEnableOfflineFlowback}
        self.mediator = None
        self.isShow = False
        self.selectIdx = 0
        self.selectFid = 0
        self.rewardLvList = {}
        self.unclaimedList = []
        self.firstShow = True
        self.rewardCallFriendNum = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMOER_FRIEND, self.hide)

    def onSetSelectedTab(self, *args):
        idx = int(args[3][0].GetNumber())
        self.selectTab(idx)

    def onGetSelectTab(self, *args):
        return GfxValue(self.selectIdx)

    def show(self, idx = 0, openByPush = False):
        if not gameglobal.rds.configData.get('enableFriendInvite', False):
            return
        idx = self.checkCanSelected(idx)
        if not openByPush and gameglobal.rds.configData.get('enableFriendInviteActivity', False) and idx == 0:
            idx = 4
        if not self.isShow:
            self.isShow = True
            self.selectIdx = idx
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SUMMOER_FRIEND)
        else:
            self.selectTab(idx)
        self.removeSummonPush()

    def removeSummonPush(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_SUMMON_FRIEND)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_SUMMON_FRIEND_REWARD)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_SUMMON_FRIEND_AREWARD_BONUS)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_SUMMON_FRIEND_ACTIVITY)

    def checkCanSelected(self, idx):
        if idx == 0:
            if SCD.data.get('friendInviterLv', 40) > BigWorld.player().lv:
                if BigWorld.player().lv > SCD.data.get('summonFriendInvitedLimitLv', 20):
                    idx = 1
                elif self.selectIdx:
                    idx = self.selectIdx
                else:
                    idx = 2
                BigWorld.player().showGameMsg(GMDD.data.INVITE_FRIEND_LV_WRONG, ())
        return idx

    def selectTab(self, idx):
        self.selectIdx = self.checkCanSelected(idx)
        if self.mediator:
            self.mediator.Invoke('initTab', GfxValue(self.selectIdx))

    def clearWidget(self):
        self.mediator = None
        self.isShow = False
        self.selectIdx = 0
        self.selectFid = 0
        self.unclaimedList = []
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SUMMOER_FRIEND)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SUMMOER_FRIEND:
            self.mediator = mediator

    def onGetIWantSummonData(self, *args):
        if hasattr(BigWorld.player(), 'friendInviteVerifyCode'):
            self.refreshIwantSummon()
        else:
            BigWorld.player().cell.genFriendInviteVerifyCode()

    def refreshIwantSummon(self):
        if not self.mediator:
            return
        data = self.getIWantSummonData()
        if self.mediator:
            self.mediator.Invoke('setIWantSummon', uiUtils.dict2GfxDict(data, True))

    def getIWantSummonData(self):
        data = {}
        data['webRule'] = uiUtils.getTextFromGMD(GMDD.data.WEB_SUMMON_RULE, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_195)
        data['myCode'] = getattr(BigWorld.player(), 'friendInviteVerifyCode', '')
        data['webUrl'] = SCD.data.get('Summon_Friend_Web_addr', 'http://tianyu.163.com/?=%s') % data['myCode']
        data['qrUrl'] = SCD.data.get('Summon_Friend_QR_addr', 'http://tianyu.163.com/?=%s') % data['myCode']
        data['QRRule'] = uiUtils.getTextFromGMD(GMDD.data.QR_SUMMON_RULE, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_199)
        codeMaker = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=2, border=1)
        codeMaker.add_data(data['qrUrl'])
        codeMaker.make(fit=True)
        img = codeMaker.make_image()
        pngUrl = img.convert('RGB').tostring('jpeg', 'RGB', 90)
        data['QRCode'] = base64.encodestring(pngUrl)
        return data

    @ui.callFilter(1, True)
    def onCopyWebToClipBoard(self, *args):
        myCode = getattr(BigWorld.player(), 'friendInviteVerifyCode', '')
        if myCode:
            if BigWorld.isPublishedVersion():
                webUrl = SCD.data.get('Summon_Friend_Web_addr', 'http://tianyu.163.com/?=%s') % myCode
            else:
                webUrl = 'http://hd-test-qc.tianyu.163.com/2015/friend?code=%s' % myCode
            BigWorld.setClipBoardText(webUrl)
            msg = uiUtils.getTextFromGMD(GMDD.data.COPY_URL_SUCCESS, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_221)
            gameglobal.rds.ui.messageBox.showMsgBox(msg)

    @ui.callFilter(1, True)
    def onCopyMyCodeToClipBoard(self, *args):
        myCode = getattr(BigWorld.player(), 'friendInviteVerifyCode', '')
        if myCode:
            BigWorld.setClipBoardText(myCode)
            msg = uiUtils.getTextFromGMD(GMDD.data.COPY_CODE_SUCCESS, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_221)
            gameglobal.rds.ui.messageBox.showMsgBox(msg)

    @ui.callFilter(1, True)
    def onSendEmail(self, *args):
        email = args[3][0].GetString()
        if not len(email):
            return
        if not utils.isValidEmail(email):
            BigWorld.player().showGameMsg(GMDD.data.INVITE_FRIEND_INVALID_ACCOUNT, ())
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.SEND_EMAIL_SUCCESS, gameStrings.TEXT_SUMMONFRIENDPROXY_197)
            gameglobal.rds.ui.messageBox.showMsgBox(msg)
            BigWorld.player().cell.sendEmail(email)

    def onGetSummonedPlayerInfo(self, *args):
        if not self.rewardLvList:
            data = FIRD.data
            for rewardId in data:
                if data[rewardId].get('lv'):
                    self.rewardLvList[data[rewardId]['lv']] = rewardId

        data = self.getSummonedPlayerInfo()
        total = len(data)
        onlineCnt = 0
        for i in data:
            if i['state'] in (1, 2, 3):
                onlineCnt = onlineCnt + 1

        totalNum = '%d/%d' % (onlineCnt, total)
        if self.mediator:
            self.mediator.Invoke('setSummonedPlayerInfo', uiUtils.array2GfxAarry(data, True))
            self.mediator.Invoke('setSummonedPlayerInfoNum', GfxValue(gbk2unicode(totalNum)))

    def getSummonedPlayerInfo(self):
        data = []
        p = BigWorld.player()
        for fid in p.friendInviteInfo:
            if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_BUILD or p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP and fid in p.friendInvitees:
                friendInfo = self.getFriendInfoById(fid)
                data.append(friendInfo)

        data.sort(cmp=self.cmpFriend)
        return data

    def cmpFriend(self, x, y):
        p = BigWorld.player()
        xFid = int(x['fid'])
        yFid = int(y['fid'])
        xLv = p.friendInviteInfo[xFid].get('lv', 1)
        yLv = p.friendInviteInfo[yFid].get('lv', 1)
        xNums = self.getCanGetRewardNums(xFid)
        yNums = self.getCanGetRewardNums(yFid)
        numsCmp = cmp(yNums, xNums)
        if numsCmp == 0:
            lvCmp = cmp(yLv, xLv)
            if lvCmp == 0:
                return cmp(p.friendInviteInfo[yFid].get('on', False), p.friendInviteInfo[xFid].get('on', False))
            else:
                return lvCmp
        else:
            return numsCmp
        return 0

    def getCanGetRewardNums(self, fid):
        p = BigWorld.player()
        rewardList = p.friendInviteRewards.get(fid, {})
        nums = 0
        for rid in rewardList:
            if rewardList[rid] == False:
                nums = nums + 1

        nowLv = p.friendInviteInfo[fid].get('lv', 1)
        for reLv in self.rewardLvList:
            if nowLv >= reLv:
                if rewardList.get(self.rewardLvList[reLv], False) == False:
                    nums = nums + 1

        return nums

    def onDownloadOtherPhoto(self, status, fid, photoName):
        photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photoName + '.dds'
        if self.mediator:
            self.mediator.Invoke('resetPhoto', (GfxValue(fid), GfxValue(photo)))

    def onSelectFriend(self, *args):
        fid = int(args[3][0].GetString())
        self.selectFid = fid
        self.refreshSelectFriend(fid)

    def refreshSelectFriend(self, fid):
        if not self.mediator:
            return
        if self.selectIdx != 1:
            return
        friendInfo = self.getFriendInfoById(fid)
        if self.mediator:
            self.mediator.Invoke('setFriendInfo', uiUtils.dict2GfxDict(friendInfo, True))
        self.refreshRewardView(fid)

    def refreshRewardView(self, fid):
        data = FIRD.data
        combatRewardList = []
        lvRewardList = []
        maxLv = 0
        maxCombat = 0
        p = BigWorld.player()
        nowCombat = 0
        for rewardId in data:
            if data[rewardId].get('lv'):
                lvRewardData = {}
                lvRewardData['awardLvId'] = rewardId
                lvRewardData['needLv'] = data[rewardId]['lv']
                if maxLv < data[rewardId]['lv']:
                    maxLv = data[rewardId]['lv']
                bonusId = data[rewardId]['bonusId']
                rewardItems = clientUtils.genItemBonus(bonusId)
                itemId = rewardItems[0][0]
                lvRewardData['itemInfo'] = uiUtils.getItemData(itemId)
                lvRewardData['itemLvColor'] = uiUtils.getItemColor(itemId)
                if p.friendInviteInfo.get(fid, {}).get('lv', 1) < data[rewardId].get('lv', 1):
                    states = SummonFriendProxy.UN_COMPLETE
                elif p.friendInviteRewards.has_key(fid) and p.friendInviteRewards[fid].has_key(rewardId) and p.friendInviteRewards[fid][rewardId]:
                    states = SummonFriendProxy.DONE
                else:
                    states = SummonFriendProxy.COMPLETE
                lvRewardData['awardLvState'] = states
                lvRewardList.append(lvRewardData)
            if data[rewardId].get('needCombatScore'):
                scoreRewardData = {}
                scoreRewardData['awardCombatScoreId'] = rewardId
                bonusId = data[rewardId]['bonusId']
                rewardItems = clientUtils.genItemBonus(bonusId)
                itemId = rewardItems[0][0]
                scoreRewardData['itemCombatInfo'] = uiUtils.getItemData(itemId)
                scoreRewardData['itemScoreColor'] = uiUtils.getItemColor(itemId)
                scoreRewardData['needCombatScore'] = data[rewardId]['needCombatScore']
                if maxCombat < data[rewardId]['needCombatScore']:
                    maxCombat = data[rewardId]['needCombatScore']
                if p.friendInviteRewards.has_key(fid) and p.friendInviteRewards[fid].has_key(rewardId) and not p.friendInviteRewards[fid][rewardId]:
                    states = SummonFriendProxy.COMPLETE
                    if nowCombat < data[rewardId]['needCombatScore']:
                        nowCombat = data[rewardId]['needCombatScore']
                elif p.friendInviteRewards.has_key(fid) and p.friendInviteRewards[fid].has_key(rewardId) and p.friendInviteRewards[fid][rewardId]:
                    states = SummonFriendProxy.DONE
                    if nowCombat < data[rewardId]['needCombatScore']:
                        nowCombat = data[rewardId]['needCombatScore']
                else:
                    states = SummonFriendProxy.UN_COMPLETE
                scoreRewardData['awardCombatState'] = states
                combatRewardList.append(scoreRewardData)

        lvRewardList.sort(cmp=lambda x, y: cmp(x['needLv'], y['needLv']))
        combatRewardList.sort(cmp=lambda x, y: cmp(x['needCombatScore'], y['needCombatScore']))
        lvRewardList.reverse()
        combatRewardList.reverse()
        progressData = {}
        nowCombatLv = 0
        for i in xrange(7, 0, -1):
            if combatRewardList[i - 1]['needCombatScore'] == nowCombat:
                nowCombatLv = 8 - i
                break

        nowLvStep = 0
        if p.friendInviteInfo.get(fid, {}).get('lv', 1) > maxLv:
            nowLv = maxLv
        else:
            nowLv = p.friendInviteInfo.get(fid, {}).get('lv', 1)
        for i in xrange(7, 0, -1):
            if i - 2 >= 0:
                if lvRewardList[i - 1]['needLv'] <= nowLv and nowLv < lvRewardList[i - 2]['needLv']:
                    nowLvStep = 8 - i
                    diff = float(nowLv - lvRewardList[i - 1]['needLv']) / (lvRewardList[i - 2]['needLv'] - lvRewardList[i - 1]['needLv'])
                    nowLvStep = nowLvStep + diff
                    break
            elif lvRewardList[i - 1]['needLv'] <= nowLv:
                nowLvStep = 7

        progressData['nowLv'] = nowLvStep
        progressData['maxLv'] = 7
        progressData['nowCombatScore'] = nowCombatLv
        progressData['maxCombatScore'] = 7
        invitePointOpen = gameglobal.rds.configData.get('enableInvitePoint', False)
        if self.mediator:
            self.mediator.Invoke('setAwardData', (uiUtils.array2GfxAarry(lvRewardList, True),
             uiUtils.array2GfxAarry(combatRewardList, True),
             uiUtils.dict2GfxDict(progressData, True),
             GfxValue(invitePointOpen)))

    def getFriendInfoById(self, fid):
        p = BigWorld.player()
        friendInfo = {}
        friendInfo['fid'] = str(fid)
        friendInfo['name'] = utils.getDisplayName(p.friendInviteInfo[fid].get('playerName', ''))
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
        if p.friendInviteInfo[fid].get('on', ''):
            friendInfo['state'] = 1
        else:
            friendInfo['state'] = 0
        friendInfo['stateName'] = stateMap[friendInfo['state']]
        if p.friendInviteInfo[fid]['status'] == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP:
            friendInfo['stateName'] = gameStrings.TEXT_SUMMONFRIENDINVITEFRIEND_299
        friendInfo['stateName2'] = stateMap2[friendInfo['state']]
        friendInfo['combatScore'] = ''
        school = p.friendInviteInfo[fid].get('school', 3)
        schoolName = SD.data[school]['name']
        lv = p.friendInviteInfo[fid].get('lv', 1)
        friendInfo['school'] = schoolName
        friendInfo['Lv'] = 'Lv.%d' % lv
        sex = p.friendInviteInfo[fid].get('sex', 1)
        if p.friendInviteInfo[fid].get('profileIcon', ''):
            photo = p.friendInviteInfo[fid]['profileIcon']
        else:
            photo = 'headIcon/%s.dds' % str(school * 10 + sex)
        if uiUtils.isDownloadImage(photo):
            p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadOtherPhoto, (friendInfo['fid'], photo))
            photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
        friendInfo['photo'] = photo
        return friendInfo

    def refreshWidget(self):
        if not self.mediator:
            return
        elif self.selectIdx == 2:
            self.onRefreshBeSummonedPlayerInfo(None)
            return
        else:
            if self.selectIdx == 1:
                self.onGetSummonedPlayerInfo(None)
            return

    def onRefreshBeSummonedPlayerInfo(self, *args):
        if self.selectIdx != 2:
            return
        p = BigWorld.player()
        hasOtherInvited = False
        if self.mediator:
            self.mediator.Invoke('setTab2Show', GfxValue(hasOtherInvited))
        if not hasOtherInvited:
            data = {}
            if BigWorld.player().friendInviterGbId:
                data['hasBinded'] = True
            else:
                data['hasBinded'] = False
            inviteId = 0
            hasDeleted = False
            if BigWorld.player().friendInviterGbId:
                inviteId = p.friendInviterGbId
                if p.friendInviteInfo.get(inviteId, {}).get('status', gametypes.FRIEND_INVITE_STATUS_ROLE_DROP) == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP:
                    hasDeleted = True
                    inviteId = 0
            else:
                for fid in p.friendInviteInfo:
                    if p.friendInviteInfo[fid]['status'] == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                        inviteId = fid
                        break
                    if p.friendInviteInfo[fid]['status'] == gametypes.FRIEND_INVITE_STATUS_ROLE_DROP:
                        if fid not in p.friendInvitees:
                            inviteId = 0
                            hasDeleted = True

            if inviteId:
                data['friendInfo'] = self.getFriendInfoById(inviteId)
                if BigWorld.player().friend.get(inviteId):
                    data['addFriend'] = False
                else:
                    data['addFriend'] = True
            else:
                data['addFriend'] = True
            if not data['hasBinded']:
                if inviteId and not hasDeleted:
                    msg = uiUtils.getTextFromGMD(GMDD.data.BIND_HINT, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_138)
                    msg = msg % data['friendInfo']['name']
                    data['friendInfoHint'] = msg
                else:
                    msg = uiUtils.getTextFromGMD(GMDD.data.NOT_INVITE_HINT, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_142)
                    data['friendInfoHint'] = msg
            elif not hasDeleted:
                msg = uiUtils.getTextFromGMD(GMDD.data.BIND_OK_HINT, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_146)
                msg = msg % data['friendInfo']['name']
                data['friendInfoHint'] = msg
            data['showContent'] = True
            if BigWorld.player().lv > SCD.data.get('friendInviteeLv') and not BigWorld.player().friendInviterGbId:
                data['hasBinded'] = True
                msg = uiUtils.getTextFromGMD(GMDD.data.BIND_FAILED_HINT_LV, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_152)
                data['friendInfoHint'] = msg
                data['showContent'] = False
            if hasDeleted == True:
                msg = uiUtils.getTextFromGMD(GMDD.data.INVITER_FRIEND_DELETE, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_156)
                data['friendInfoHint'] = msg
                data['showContent'] = False
            if self.mediator:
                self.mediator.Invoke('setTab3Data', uiUtils.dict2GfxDict(data, True))

    @ui.callFilter(1, True)
    def onSendConfirmBind(self, *args):
        code = args[3][0].GetString()
        ret = int(args[3][1].GetNumber())
        if ret == 1:
            if len(code) == 0:
                gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_SUMMONFRIENDPROXY_509)
                return
        self.sendConfirmBind(code)

    def sendConfirmBind(self, code):
        p = BigWorld.player()
        if not code:
            if not p.friendInviterGbId:
                inviteId = 0
                for fid in p.friendInviteInfo:
                    if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                        inviteId = fid
                        break

                if inviteId:
                    BigWorld.player().base.invitedFriendByGbId(inviteId)
            else:
                return
        BigWorld.player().base.invitedFriendByVerifyCode(code)

    @ui.callFilter(1, True)
    def onAddFriend(self, *args):
        p = BigWorld.player()
        inviteId = 0
        if p.friendInviterGbId:
            inviteId = p.friendInviterGbId
        else:
            for fid in p.friendInviteInfo:
                if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                    inviteId = fid
                    break

        if inviteId:
            name = p.friendInviteInfo[inviteId].get('playerName', '')
            p.base.addContact(name, gametypes.FRIEND_GROUP_FRIEND, const.FRIEND_SRC_SUMMON)

    @ui.callFilter(1, True)
    def onGetAwardSp(self, *args):
        pass

    @ui.callFilter(1, True)
    def onGetAward(self, *args):
        awardId = int(args[3][0].GetNumber())
        BigWorld.player().cell.doFriendInvitationReward(self.selectFid, awardId)

    def close(self):
        pass

    def showMessageBox(self):
        if self.firstShow:
            self.firstShow = False
        else:
            return
        if not gameglobal.rds.configData.get('enableFriendInvite', False):
            return
        p = BigWorld.player()
        inviteId = 0
        if not p.friendInviterGbId:
            for fid in p.friendInviteInfo:
                if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                    inviteId = fid
                    break

        if inviteId:
            MBButton = messageBoxProxy.MBButton
            title = uiUtils.getTextFromGMD(GMDD.data.BIND_HINT_TITLE, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_252)
            msg = uiUtils.getTextFromGMD(GMDD.data.BIND_HINT_MESSAGEBOX, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_138) % p.friendInviteInfo[inviteId].get('playerName', '')
            buttons = [MBButton(gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_254, Functor(self.sendConfirmBind, ''), fastKey=keys.KEY_Y), MBButton(gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_254_1, fastKey=keys.KEY_N), MBButton(gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_254_2, self.onKnowSummon)]
            gameglobal.rds.ui.messageBox.show(True, title, msg, buttons)

    def onKnowSummon(self):
        self.show(0)

    def onGetSummonActivities(self, *arg):
        ret = self._getSummonActivities()
        return uiUtils.dict2GfxDict(ret, True)

    def _getSummonActivities(self):
        ret = {}
        rewardData = IERD.data
        friendActivityData = getattr(BigWorld.player(), 'friendInvitationSummary', {})
        ret['advertisements'] = []
        ret['rewardInfo'] = []
        now = utils.getNow()
        for key, value in rewardData.items():
            startStamp = value.get('tStart', 1442455200)
            endStamp = value.get('tEnd', 1445472000)
            if now < startStamp:
                continue
            adItems = {}
            adItems['iconPath'] = AD_ICON_TEMPLATE % value.get('adName', '3')
            ret['advertisements'].append(adItems)
            item = {}
            rewardId = value.get('rewardId', 0)
            item['activityId'] = key
            item['condition'] = value.get('conditionDesc', gameStrings.TEXT_SUMMONFRIENDINVITEACTIVITY_138)
            item['itemData'] = uiUtils.getGfxItemById(rewardId)
            item['itemName'] = uiUtils.getItemColorName(rewardId)
            item['isFinished'] = now > endStamp
            item['restTime'] = endStamp - now
            item['restTime'] = endStamp - now
            reqNum = value.get('num', 0)
            curNum = friendActivityData.get(key, [0, 0])[0]
            hasReward = friendActivityData.get(key, [0, 0])[1]
            item['reachGoal'] = reqNum <= curNum
            item['hasReward'] = hasReward
            ret['rewardInfo'].append(item)

        return ret

    def onGetActivityReward(self, *arg):
        rid = int(arg[3][0].GetNumber())
        BigWorld.player().cell.gainFriendInvitationSummaryReward(rid)

    def onEnableActivity(self, *arg):
        enable = gameglobal.rds.configData.get('enableFriendInviteActivity', False)
        return GfxValue(enable)

    def onEnableMyInvitor(self, *arg):
        playerLv = BigWorld.player().lv
        limitLv = SCD.data.get('summonFriendInvitedLimitLv', 20)
        return GfxValue(playerLv <= limitLv)

    def onGetDefaultRewardList(self, *arg):
        self.refreshRewardView(-1)

    def refreshFriendInviteActivity(self):
        if self.mediator and self.selectIdx == 4:
            ret = self._getSummonActivities()
            self.mediator.Invoke('refreshFriendInviteActivity', uiUtils.dict2GfxDict(ret, True))

    def pushSummon(self):
        if gameglobal.rds.configData.get('enableFriendInviteActivity', False):
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_SUMMON_FRIEND)
            if gameglobal.rds.configData.get('enableInvitePoint', False):
                if gameglobal.rds.configData.get('enableSummonFriendV2', False):
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND, {'click': Functor(self.uiAdapter.summonFriendBGV2.show, uiConst.SUMMON_FRIEND_TAB_INDEX1, 'inviteBtn')})
                else:
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND, {'click': Functor(self.uiAdapter.summonFriendNew.show, 2)})
            else:
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND, {'click': Functor(self.show, 0, True)})

    def pushSummonFriendReward(self):
        if gameglobal.rds.configData.get('enableFriendInviteActivity', False) and self._checkHasReward():
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_SUMMON_FRIEND_REWARD)
            if gameglobal.rds.configData.get('enableInvitePoint', False):
                if gameglobal.rds.configData.get('enableSummonFriendV2', False):
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND, {'click': Functor(self.uiAdapter.summonFriendBGV2.show, uiConst.SUMMON_FRIEND_TAB_INDEX0)})
                else:
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND_REWARD, {'click': Functor(self.uiAdapter.summonFriendNew.show, 1)})
            else:
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND_REWARD, {'click': Functor(self.show, 1, True)})

    def pushSummonFriendRewardBonus(self):
        if gameglobal.rds.configData.get('enableFriendInviteActivity', False) and self._checkHasBonusReward():
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_SUMMON_FRIEND_AREWARD_BONUS)
            if gameglobal.rds.configData.get('enableInvitePoint', False):
                if gameglobal.rds.configData.get('enableSummonFriendV2', False):
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND, {'click': Functor(self.uiAdapter.summonFriendBGV2.show, uiConst.SUMMON_FRIEND_TAB_INDEX1, 'activityBtn')})
                else:
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND_AREWARD_BONUS, {'click': Functor(self.uiAdapter.summonFriendNew.show, 0)})
            else:
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND_AREWARD_BONUS, {'click': Functor(self.show, 4, True)})

    def pushSummonFriendActivity(self):
        if gameglobal.rds.configData.get('enableFriendInviteActivity', False):
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_SUMMON_FRIEND_ACTIVITY)
            if gameglobal.rds.configData.get('enableInvitePoint', False):
                if gameglobal.rds.configData.get('enableSummonFriendV2', False):
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND, {'click': Functor(self.uiAdapter.summonFriendBGV2.show, uiConst.SUMMON_FRIEND_TAB_INDEX1, 'activityBtn')})
                else:
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND_ACTIVITY, {'click': Functor(self.uiAdapter.summonFriendNew.show, 0)})
            else:
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_SUMMON_FRIEND_ACTIVITY, {'click': Functor(self.show, 4, True)})

    def _checkHasReward(self):
        data = FIRD.data
        p = BigWorld.player()
        for fid in p.friendInviteInfo:
            for rewardId in data:
                if data[rewardId].get('lv'):
                    if p.friendInviteInfo.get(fid, {}).get('lv', 1) < data[rewardId].get('lv', 1):
                        pass
                    elif p.friendInviteRewards.has_key(fid) and p.friendInviteRewards[fid].has_key(rewardId) and not p.friendInviteRewards[fid][rewardId]:
                        return True
                if data[rewardId].get('needCombatScore'):
                    if p.friendInviteRewards.has_key(fid) and p.friendInviteRewards[fid].has_key(rewardId) and not p.friendInviteRewards[fid][rewardId]:
                        return True

        return False

    def _checkHasBonusReward(self):
        rewardData = IERD.data
        friendActivityData = getattr(BigWorld.player(), 'friendInvitationSummary', {})
        now = utils.getNow()
        for key, value in rewardData.items():
            startStamp = value.get('tStart', 1442455200)
            if now < startStamp:
                continue
            reqNum = value.get('num', 0)
            curNum = friendActivityData.get(key, [0, 0])[0]
            hasReward = friendActivityData.get(key, [0, 0])[1]
            reachGoal = reqNum <= curNum
            if reachGoal and not hasReward:
                return True

        return False

    def setSummonRewards(self, stat):
        self.rewardCallFriendNum = stat.get('score', 0)
        self.awardAppliedList = stat.get('awardAppliedList', [])
        if self.rewardCallFriendNum != -1:
            self.refreshSummonRewards()

    def onGetSummonRewards(self, *args):
        self.refreshSummonRewards()

    def onWantCall(self, *args):
        gameglobal.rds.ui.friend.show()

    @ui.callFilter(5, True)
    def onTab5Reward(self, *args):
        p = BigWorld.player()
        if self.unclaimedList:
            p.base.applyFlowbackInvitationReward(self.unclaimedList[0])
            self.refreshSummonRewards()
        else:
            p.showGameMsg(GMDD.data.UNCLAIMED_NOTIFY_MSG, ())

    def refreshSummonRewards(self):
        if self.mediator:
            ret = {}
            list = []
            self.unclaimedList = []
            for i in FID.data:
                map = {}
                bonusId = FID.data.get(i, 0).get('bonusId', 0)
                rewardItems = clientUtils.genItemBonus(bonusId)
                itemId = rewardItems[0][0]
                needScore = FID.data.get(i, 0).get('needScore', 0)
                map['bonus'] = uiUtils.getItemData(itemId)
                map['needScore'] = needScore
                if needScore <= self.rewardCallFriendNum:
                    map['stateLabel'] = True
                    if i in self.awardAppliedList:
                        map['state'] = True
                    else:
                        map['state'] = False
                        self.unclaimedList.append(i)
                else:
                    map['stateLabel'] = False
                list.append(map)

            ret['bonusInfo'] = list
            ret['callFriend'] = self.rewardCallFriendNum
            ret['callFriendLabel'] = GMD.data.get(GMDD.data.CALL_FRIEND_LABEL, {}).get('text', gameStrings.TEXT_SUMMONFRIENDPROXY_774)
            self.mediator.Invoke('refreshSummonRewards', uiUtils.dict2GfxDict(ret, True))

    def onEnableOfflineFlowback(self, *args):
        ret = False
        if gameglobal.rds.configData.get('enableOfflineFlowback', False) and self.rewardCallFriendNum != -1:
            ret = True
        return GfxValue(ret)
