#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impMiniGame.o
from gamestrings import gameStrings
import BigWorld
import const
import formula
import gameglobal
import gamelog
import logicInfo
import utils
import urllib
import urllib2
from item import Item
from callbackHelper import Functor
from gameStrings import gameStrings
from guis import uiConst
from guis import ui
from data import sys_config_data as SYSCD
from data import interactive_data as ID
from data import mini_game_data as MGD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD

class ImpMiniGame(object):

    def onJoinMiniGame(self, iObjEntId, miniGameSerialNumber, token):
        """
        \xe7\x8e\xa9\xe5\xae\xb6\xe8\xb7\x9f\xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba\xe5\x8f\xaf\xe4\xba\xa4\xe4\xba\x92\xe7\x89\xa9\xe4\xbb\xb6\xe4\xba\xa4\xe4\xba\x92\xe6\x88\x90\xe5\x8a\x9f\xe5\x90\x8e\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x8c\xe6\xad\xa4\xe6\x97\xb6\xe7\x8e\xa9\xe5\xae\xb6\xe5\xb7\xb2\xe5\x85\xa5\xe5\xba\xa7
        \xe9\x9c\x80\xe8\xa6\x81\xe9\x80\x9a\xe8\xbf\x87iObjEntId\xe8\x8e\xb7\xe5\x8f\x96iObj
        \xe6\xa0\xb9\xe6\x8d\xaeiObj\xe7\x9a\x84objectId\xe8\xaf\xbb\xe8\xa1\xa8\xe8\x8e\xb7\xe5\x8f\x96\xe4\xbd\xbf\xe7\x94\xa8\xe7\x9a\x84\xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba\xe6\x98\xaf\xe5\x90\xa6\xe5\x85\xac\xe7\x94\xa8\xe3\x80\x81\xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba\xe7\x9a\x84\xe7\xb1\xbb\xe5\x9e\x8b\xe5\x92\x8c\xe4\xbd\x8d\xe7\xbd\xae\xe4\xbf\xa1\xe6\x81\xaf
        :param iObjEntId: \xe5\x8f\xaf\xe4\xba\xa4\xe4\xba\x92\xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba\xe7\x9a\x84EntityId
        :param miniGameSerialNumber: \xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba\xe5\xba\x8f\xe5\x88\x97\xe5\x8f\xb7
        :param token:
        :return:
        """
        img = self.friend.photo
        url = ''
        if BigWorld.isPublishedVersion():
            url = SYSCD.data.get('miniGamePublishUrl', 'http://minigame.tianyu.163.com/guess.html?uuid={uuid}&avatarImg={avatarImg}&roleName={roleName}&roomId={roomId}&gameServer={gameServer}&accessToken={accessToken}')
        else:
            url = SYSCD.data.get('miniGameDebugUrl', 'http://10.246.46.178/guess.html?uuid={uuid}&avatarImg={avatarImg}&roleName={roleName}&roomId={roomId}&gameServer={gameServer}&accessToken={accessToken}')
        hostpage = url.split('?')[0]
        gameServer = '%s:%s' % (str(utils.getHostId()), ui.gbk2unicode(str(gameglobal.rds.hostName)))
        params = urllib.urlencode({'uuid': str(self.gbId),
         'avatarImg': urllib2.quote(img),
         'roleName': ui.gbk2unicode(self.roleName, self.roleName),
         'roomId': miniGameSerialNumber,
         'gameServer': gameServer,
         'accessToken': token})
        url = '%s?%s' % (hostpage, params)
        self.miniGameSerialNumber = miniGameSerialNumber
        gameglobal.rds.ui.miniGame.show(iObjEntId, url)

    def onInviteToMiniGame(self, fromName, ownerName, miniGamePublic, miniGamePositionInfo, canInteractiveCnt):
        """
        \xe6\x94\xb6\xe5\x88\xb0\xe8\xa2\xab\xe5\xa5\xbd\xe5\x8f\x8b\xe9\x82\x80\xe8\xaf\xb7\xe5\x8f\x82\xe5\x8a\xa0\xe5\xb0\x8f\xe6\xb8\xb8\xe6\x88\x8f\xe7\x9a\x84\xe6\x8e\xa5\xe5\x8f\xa3
        :param fromName: \xe9\x82\x80\xe8\xaf\xb7\xe4\xba\xba\xe7\x9a\x84\xe5\x90\x8d\xe5\xad\x97
        :param ownerName: \xe5\x85\xac\xe7\x94\xa8\xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba\xe4\xb8\xba\xe7\xa9\xba,\xe6\x88\xbf\xe9\x97\xb4\xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba\xe4\xb8\xba\xe6\x88\xbf\xe4\xb8\xbb\xe5\x90\x8d
        :param miniGamePublic: \xe8\xa2\xab\xe9\x82\x80\xe8\xaf\xb7\xe5\x8e\xbb\xe5\x8f\x82\xe5\x8a\xa0\xe6\xb8\xb8\xe6\x88\x8f\xe7\x9a\x84\xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe5\x85\xac\xe7\x94\xa8\xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba
        :param miniGamePositionInfo: \xe8\xa2\xab\xe9\x82\x80\xe8\xaf\xb7\xe5\x8e\xbb\xe5\x8f\x82\xe5\x8a\xa0\xe6\xb8\xb8\xe6\x88\x8f\xe7\x9a\x84\xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba\xe4\xbd\x8d\xe7\xbd\xae\xe4\xbf\xa1\xe6\x81\xaf(\xe5\x85\xac\xe7\x94\xa8\xe5\x88\x99\xe6\x98\xaf(spaceNo,positon), \xe7\xa7\x81\xe7\x94\xa8\xe5\x88\x99\xe6\x98\xaf(fromGbId,))
        :param canInteractiveCnt: \xe8\xa2\xab\xe9\x82\x80\xe8\xaf\xb7\xe5\x8e\xbb\xe5\x8f\x82\xe5\x8a\xa0\xe6\xb8\xb8\xe6\x88\x8f\xe7\x9a\x84\xe6\xb8\xb8\xe6\x88\x8f\xe6\x9c\xba\xe5\x89\xa9\xe4\xbd\x99\xe7\xa9\xba\xe4\xbd\x8d\xe6\x95\xb0
        :return:
        """
        inviteMsg = ''
        if canInteractiveCnt > 2:
            inviteMsg = SYSCD.data.get('miniGameInviteFriendSpareMsg', gameStrings.TEXT_IMPMINIGAME_76)
        else:
            inviteMsg = SYSCD.data.get('miniGameInviteFriendMsg', gameStrings.TEXT_IMPMINIGAME_79)
        inviteMsg = inviteMsg % (fromName, ownerName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(inviteMsg, Functor(self.joinInvitedMiniGame, ownerName, miniGamePublic, miniGamePositionInfo), yesBtnText=gameStrings.TEXT_IMPARENA_582, noBtnText=gameStrings.TEXT_IMPMINIGAME_82, isModal=False, msgType='pushLoop', textAlign='center')

    def joinInvitedMiniGame(self, fromName, miniGamePublic, miniGamePositionInfo):
        if miniGamePublic:
            spaceNo, positon = miniGamePositionInfo
            self.gotoWenQuanMiniGame('', fromName, spaceNo, positon)
        else:
            gbId = miniGamePositionInfo[0]
            self.visitRoom(gbId, fromName)

    def gotoWenQuanMiniGame(self, gbId, roleName, spaceNo, position):
        if self.checkPathfinding():
            self.cancelPathfinding()
        canUse = logicInfo.isUseableGuildMemberSkill(const.GUILD_SKILL_XIAOFEIXIE)
        if gbId and type(gbId) != str:
            gbId = '#' + str(gbId)
        if canUse:
            seekId = SYSCD.data.get('miniGameWenQuanSeekId', None)
            self.cell.useGuildMemberSkillWithParam(const.GUILD_SKILL_XIAOFEIXIE, (seekId,))
        elif self.canResetCD(const.GUILD_SKILL_XIAOFEIXIE):
            msg = GMD.data.get(GMDD.data.CONFIRM_RESET_TRACK_CD, {}).get('text', gameStrings.TEXT_UIUTILS_914)
            itemFameData = {}
            resetCDItems = SCD.data.get('resetGuildTrackSkillCDItems', ())
            if resetCDItems:
                p = BigWorld.player()
                itemId, needNum = resetCDItems
                item = Item(itemId)
                currentCount = BigWorld.player().inv.countItemInPages(item.getParentId(), enableParentCheck=True)
                itemFameData['itemId'] = itemId
                itemFameData['deltaNum'] = needNum - currentCount
            func = Functor(self.cell.resetGuildSkillCD, const.GUILD_SKILL_XIAOFEIXIE, (gbId, roleName))
            if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_RESET_TRACK_CD):
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, func, isShowCheckBox=True, itemFameData=itemFameData, checkOnceType=uiConst.CHECK_ONCE_TYPE_RESET_TRACK_CD)
            else:
                func()
        else:
            self.showGameMsg(GMDD.data.GUILD_SKILL_TRACK_CD, ())

    def inviteFriendToMiniGameFromWeb(self):
        """
        \xe6\x94\xb6\xe5\x88\xb0\xe7\xbd\x91\xe7\xab\x99\xe9\x82\xa3\xe8\xbe\xb9\xe7\x82\xb9\xe5\x87\xbb\xe9\x82\x80\xe8\xaf\xb7\xe5\xa5\xbd\xe5\x8f\x8b\xe6\x8c\x89\xe9\x92\xae\xe7\x9a\x84\xe8\xaf\xb7\xe6\xb1\x82
        :return:
        """
        gameglobal.rds.ui.selectFriend.show(self.confirmSelectFriends)

    def confirmSelectFriends(self, friends):
        hostName = ''
        if formula.spaceInHomeRoom(self.spaceNo):
            hostName = self.myHome.ownerName
        self.base.inviteFriendToMiniGame(list(friends), hostName, self.miniGameSerialNumber)

    def publishMsgOfMiniGameFromWeb(self):
        """
        \xe6\x94\xb6\xe5\x88\xb0\xe7\xbd\x91\xe7\xab\x99\xe9\x82\xa3\xe8\xbe\xb9\xe7\x82\xb9\xe5\x87\xbb\xe5\x8f\x91\xe5\xb8\x83\xe5\x88\xb0\xe5\xa4\xa7\xe4\xb8\x96\xe7\x95\x8c\xe6\x8c\x89\xe9\x92\xae\xe7\x9a\x84\xe8\xaf\xb7\xe6\xb1\x82
        :return:
        """
        ent = BigWorld.entities.get(self.interactiveObjectEntId, None)
        if not ent or not ent.inWorld:
            gamelog.error('m.l@impMiniGame.publishMsgOfMiniGameFromWeb ent not inWorld')
            return
        else:
            iData = ID.data.get(ent.objectId, {})
            miniGameId = iData.get('miniGameId', 0)
            if miniGameId:
                gameData = MGD.data.get(miniGameId, {})
                gameName = gameData.get('name', gameStrings.MINI_GAME_DUUDLE)
                hostName = self.roleName
                gbId = self.gbId
                if formula.spaceInHomeRoom(self.spaceNo):
                    hostName = self.myHome.ownerName
                    gbId = self.myHome.ownerGbID
                inviteMsg = SYSCD.data.get('miniGameInviteWorldMsg', gameStrings.TEXT_IMPMINIGAME_156)
                inviteMsg = inviteMsg % (self.roleName,
                 gameName,
                 hostName,
                 gbId,
                 gameglobal.rds.gServerid)
                gameglobal.rds.ui.sendLink(inviteMsg)
            return

    def onQuitMiniGame(self):
        """
        \xe7\xa6\xbb\xe5\xbc\x80\xe5\xb0\x8f\xe6\xb8\xb8\xe6\x88\x8f\xef\xbc\x8c\xe9\x9c\x80\xe8\xa6\x81\xe5\x85\xb3\xe9\x97\xad\xe6\xb5\x8f\xe8\xa7\x88\xe5\x99\xa8
        :return:
        """
        pass
