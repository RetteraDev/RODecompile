#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPersonalZone.o
from gamestrings import gameStrings
import zlib
import cPickle
import BigWorld
import gameglobal
import gamelog
import gameconfigCommon
import const
import utils
import gametypes
from guis import uiUtils
from guis import uiConst
from helpers import pyq_interface
from data import personal_zone_touch_data as PZTD
from data import personal_zone_gift_data as PZGD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class ImpPersonalZone(object):

    def onOpenZone(self, ownerGbId, data, hostId):
        gamelog.debug('@zq onOpenZone', ownerGbId, cPickle.loads(zlib.decompress(data)))
        serverData = cPickle.loads(zlib.decompress(data))
        self.getPersonalSysProxy().onOpenZone(ownerGbId, serverData, hostId)

    def updateZoneData(self, ownerGbId, op, data):
        gamelog.debug('@zq updateZoneData', ownerGbId, op, cPickle.loads(zlib.decompress(data)))
        self.getPersonalSysProxy().onUpdateInfo(ownerGbId, op, cPickle.loads(zlib.decompress(data)))
        if op == const.PERSONAL_ZONE_OP_TOUCH:
            gameglobal.rds.ui.spaceTouch.sendTouchMsg()
        elif op == const.PERSONAL_ZONE_OP_LIKE:
            self.getPersonalSysProxy().sendLikeMsg()
        elif op == const.PERSONAL_ZONE_OP_SET_INFO:
            if self.getPersonalSysProxy().isOpen():
                self.getPersonalSysProxy().updateHeadInfo(ownerGbId, cPickle.loads(zlib.decompress(data)))
        elif op == const.PERSONAL_ZONE_OP_BORDER:
            if self.getPersonalSysProxy().isOpen():
                self.getPersonalSysProxy().updatePhotoBorderInfo(ownerGbId, cPickle.loads(zlib.decompress(data)))

    def onGetZoneLikeData(self, ownerGbId, data):
        p = BigWorld.player()
        data = cPickle.loads(zlib.decompress(data))
        gamelog.debug('@zs onGetZoneLikeData', ownerGbId, data)
        ret = []
        if data:
            for value in data:
                mName = ''
                photo = ''
                tWhen = 0
                mGbId = 0
                borderId = 0
                if len(value) == 4:
                    mName, photo, tWhen, mGbId = value
                elif len(value) == 5:
                    mName, photo, tWhen, mGbId, borderId = value
                if not borderId:
                    borderId = SCD.data.get('defaultBorderId', 0)
                ret.append({'nameTxt': mName,
                 'photo': photo,
                 'dateTxt': uiUtils.getSimpleDaysAgo(tWhen),
                 'msgTxt': gameStrings.TEXT_IMPPERSONALZONE_62,
                 'newIcon': False,
                 'gbId': str(mGbId),
                 'isShow': 1,
                 'photoBorderIcon': p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)})

            gameglobal.rds.ui.friendList.show(ret)

    def onGetZoneTouchData(self, ownerGbId, data):
        p = BigWorld.player()
        data = cPickle.loads(zlib.decompress(data))
        gamelog.debug('@zs onGetZoneTouchData', ownerGbId, data)
        ret = []
        if data:
            for value in data:
                mName = ''
                opType = 0
                photo = ''
                tWhen = 0
                mGbId = 0
                borderId = 0
                if len(value) == 5:
                    mName, opType, photo, tWhen, mGbId = value
                elif len(value) == 6:
                    mName, opType, photo, tWhen, mGbId, borderId = value
                if not borderId:
                    borderId = SCD.data.get('defaultBorderId', 0)
                ret.append({'nameTxt': mName,
                 'photo': photo,
                 'dateTxt': uiUtils.getSimpleDaysAgo(tWhen),
                 'msgTxt': PZTD.data.get(opType, {}).get('sendMsg', ''),
                 'newIcon': False,
                 'gbId': str(mGbId),
                 'isShow': 1,
                 'photoBorderIcon': p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)})

            gameglobal.rds.ui.friendList.show(ret)

    def onCommitZoneMsg(self, ownerGbId, data):
        data = cPickle.loads(zlib.decompress(data))
        gamelog.debug('@zs onCommitZoneMsg', ownerGbId, data)
        self.getPersonalSysProxy().commitZoneMsgCallback(ownerGbId, data)

    def onFetchZoneMsg(self, ownerGbId, data):
        data = cPickle.loads(zlib.decompress(data))
        gamelog.debug('@zs onFetchZoneMsg', ownerGbId, data)
        self.getPersonalSysProxy().fetchZoneMsgCallback(ownerGbId, data)

    def onDelZoneMsg(self, ok, ownerGbId, msgDbId):
        gamelog.debug('@zs onDelZoneMsg', ok, ownerGbId, msgDbId)
        if ok:
            self.getPersonalSysProxy().delZoneMsgCallback(ownerGbId, msgDbId)

    def onQueryPersonalZoneInfo(self, ownerGbId, data):
        gamelog.debug('@zq onQueryPersonalZoneInfo', ownerGbId, cPickle.loads(zlib.decompress(data)))
        self.getPersonalSysProxy().onQueryPersonalZoneInfo(ownerGbId, cPickle.loads(zlib.decompress(data)))

    def onGetZoneGiftData(self, ownerGbId, data):
        gamelog.debug('@zs onGetZoneGiftData', ownerGbId, cPickle.loads(zlib.decompress(data)))
        self.getPersonalSysProxy().onGetZoneGiftData(ownerGbId, cPickle.loads(zlib.decompress(data)))

    def onGetZoneGiftHistory(self, ownerGbId, data):
        data = cPickle.loads(zlib.decompress(data))
        gamelog.debug('@zs onGetZoneGiftHistory', ownerGbId, data)
        if data:
            gameglobal.rds.ui.spaceGiftBox.onGetZoneGiftHistory(data)

    def onGetPersonalZoneConfig(self, config):
        gamelog.debug('@zs onGetPersonalZoneConfig', config)
        configs = []
        if config:
            configs = config.split('|')
            if len(configs) == 3:
                p = BigWorld.player()
                p.ckBoxHideMyJieqi = int(configs[0])
                p.zoneMsgPermission = int(configs[1])
                p.zoneHeadIconPermission = int(configs[2])

    def onSendGiftSucc(self, mName, mGbId, giftId, giftNum):
        self.showGameMsg(GMDD.data.PZONE_SEND_GIFT_SUCC, ())
        giftName = PZGD.data.get(giftId, {}).get('name', '')
        isFriend = self.friend and self.friend.isFriend(mGbId)
        isCrossFriend = self.isGobalFirendGbId(mGbId)
        zone = self.getPersonalSysProxy()
        if isFriend or isCrossFriend:
            desc = uiUtils.getTextFromGMD(GMDD.data.PZONE_SEND_GIFT_TO_ONE_SUCC, gameStrings.TEXT_IMPPERSONALZONE_141)
            desc = desc % (gameStrings.TEXT_IMPPERSONALZONE_142,
             gameStrings.TEXT_IMPPERSONALZONE_142_1,
             str(giftNum),
             giftName)
            gameglobal.rds.ui.chatToFriend._sendMsgToFid(mGbId, desc)
        elif mGbId == zone.ownerGbID and zone.isOnline() and not zone.isCrossServer():
            desc = uiUtils.getTextFromGMD(GMDD.data.PZONE_SEND_GIFT_TO_ONE_SIMPLE_SUCC, gameStrings.TEXT_IMPPERSONALZONE_145)
            desc = desc % (str(giftNum), giftName) + ':role'
            desc = utils.encodeMsgHeader(desc, {gametypes.MSG_ATTR_EGNORE_TALK_FLAG: 1})
            self.cell.chatToOne(mName, desc)
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SINGLE, desc, mName, False, True)

    def showTeamTouch(self, useType):
        """
        \xe6\x98\xbe\xe7\xa4\xba\xe9\x98\x9f\xe4\xbc\x8d\xe6\x8e\xa8\xe8\x8d\x90\xef\xbc\x88\xe5\x8c\x85\xe5\x90\xab\xe6\x92\xa9\xe4\xb8\x80\xe4\xb8\x8b\xe6\x95\xb0\xe7\x9b\xae\xef\xbc\x89
        Args:
            useType: \xe4\xbd\xbf\xe7\x94\xa8\xe7\xb1\xbb\xe5\x9e\x8b\xef\xbc\x88\xe4\xbe\x8b\xe5\xa6\x82gametypes.GET_ZONE_TOUCH_NUM_FOR_TEAM_MONSTER_TRIGGER\xef\xbc\x89
        
        Returns:
        
        """
        if not self.isInTeam():
            return
        gameglobal.rds.ui.addFriendPop.show(useType)

    def onGetZoneTouchNum(self, ownerGbId, num, touched, tags, useType):
        """
        \xe8\x8e\xb7\xe5\x8f\x96\xe6\x92\xa9\xe4\xb8\x80\xe4\xb8\x8b\xe6\x95\xb0\xe7\x9b\xae\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        Args:
            ownerGbId: \xe7\xa9\xba\xe9\x97\xb4\xe4\xb8\xbb\xe4\xba\xba\xe7\x9a\x84gbId   
            num:  \xe6\x95\xb0\xe7\x9b\xae
            touched: \xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe6\x92\xa9\xe8\xbf\x87
            tags: \xe6\xa0\x87\xe7\xad\xbe\xef\xbc\x8c\xe6\xa0\xbc\xe5\xbc\x8f\xef\xbc\x9a[101, [102,103], [201,202]]
            useType: \xe4\xbd\xbf\xe7\x94\xa8\xe7\xb1\xbb\xe5\x9e\x8b\xef\xbc\x88\xe4\xbe\x8b\xe5\xa6\x82gametypes.GET_ZONE_TOUCH_NUM_FOR_TEAM_MONSTER_TRIGGER\xef\xbc\x89
        
        Returns:
        """
        if tags is not None:
            tags = [tags[0]] + tags[1] + tags[2]
        tags = self.filterRecommendTags(tags)
        gameglobal.rds.ui.addFriendPop.onReceivedTouchInfo(ownerGbId, touched, useType)
        gameglobal.rds.ui.addFriendPop.onReceivedSignTextInfo(ownerGbId, tags)

    def onSyncPersonalZoneSkin(self, personalZoneSkin):
        """
        \xe4\xb8\x8a\xe7\xba\xbf\xe6\x97\xb6\xe5\x90\x8c\xe6\xad\xa5\xe4\xb8\xaa\xe4\xba\xba\xe7\xa9\xba\xe9\x97\xb4\xe7\x9a\xae\xe8\x82\xa4\xe6\x95\xb0\xe6\x8d\xae
        :param personalZoneSkin: 
        """
        gamelog.debug('@zq onSyncPersonalZoneSkin skins:{0} curUse:{1}'.format(personalZoneSkin.keys(), personalZoneSkin.curUseSkinId))
        self.personalZoneSkin = personalZoneSkin
        gameglobal.rds.ui.spaceSkinSetting.refreshInfo()

    def onPersonalZoneSkinChange(self, addSkins, rmSkinIds, changeSkins):
        """
        \xe4\xb8\xaa\xe4\xba\xba\xe7\xa9\xba\xe9\x97\xb4\xe7\x9a\xae\xe8\x82\xa4\xe5\x8f\x91\xe7\x94\x9f\xe5\x8f\x98\xe5\x8a\xa8\xef\xbc\x88\xe8\xb4\xad\xe4\xb9\xb0\xe3\x80\x81\xe8\xbf\x87\xe6\x9c\x9f\xe3\x80\x81\xe7\xbb\xad\xe6\x9c\x9f\xe7\xad\x89\xe6\x83\x85\xe5\x86\xb5\xef\xbc\x89
        :param addSkins: \xe5\xa2\x9e\xe5\x8a\xa0\xe7\x9a\x84\xe7\x9a\xae\xe8\x82\xa4
        :param rmSkinIds:  \xe5\x88\xa0\xe9\x99\xa4\xe7\x9a\x84\xe7\x9a\xae\xe8\x82\xa4id
        :param changeSkins: \xe4\xbf\xae\xe6\x94\xb9\xe7\x9a\x84\xe7\x9a\xae\xe8\x82\xa4 
        :return: 
        """
        gamelog.debug('@zq onPersonalZoneSkinChange', addSkins, rmSkinIds, changeSkins)
        for skin in addSkins:
            self.personalZoneSkin[skin.skinId] = skin

        for skinId in rmSkinIds:
            self.personalZoneSkin.pop(skinId, None)

        for skin in changeSkins:
            self.personalZoneSkin[skin.skinId] = skin

        gameglobal.rds.ui.spaceSkinSetting.refreshInfo()

    def onSetPersonalZoneSkin(self, curUseSkinId):
        """
        \xe8\xae\xbe\xe7\xbd\xae\xe7\xa9\xba\xe9\x97\xb4\xe7\x9a\xae\xe8\x82\xa4\xe5\x90\x8e\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param curUseSkinId: \xe8\xae\xbe\xe7\xbd\xae\xe6\x88\x90\xe5\x8a\x9f\xe7\x9a\x84\xe7\xa9\xba\xe9\x97\xb4\xe7\x9a\xae\xe8\x82\xa4id  
        """
        gamelog.debug('@zq onSetPersonalZoneSkin', curUseSkinId)
        self.personalZoneSkin.curUseSkinId = curUseSkinId
        gameglobal.rds.ui.spaceSkinSetting.refreshInfo()

    def syncSkeyPYQ(self, skey):
        gamelog.debug('@zq syncSkeyPYQ', skey)
        self.pyq_skey = skey
        self.getTopicList()

    def getPersonalSysProxy(self):
        return gameglobal.rds.ui.personalZoneDetail

    def getTopicList(self):
        pyq_interface.getTopic(self.onGetTopicList)

    def onGetTopicList(self, rStatus, content):
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            self.topicList = content.get('data', 0)

    def getPyqNewNum(self):
        if not utils.instanceof(self, 'PlayerAvatar'):
            return
        pyq_interface.getRedDot(self.onGetPyqNewNum)

    def onGetPyqNewNum(self, rStatus, content):
        if not utils.instanceof(self, 'PlayerAvatar'):
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            cData = content.get('data', {})
            if cData:
                dynaNum = cData.get('dynaNum', 0)
                msgNum = cData.get('msgNum', 0)
                newsNum = dynaNum + msgNum
                gameglobal.rds.ui.topBar.refreshPersonalZoneEffect(newsNum)
                self.pyqNewsNum = newsNum
                gameglobal.rds.ui.topBar.onUpdateClientCfg()

    def setPyqPublishUrl(self, force):
        self.pyq_forcePublishUrl = force

    def syncPYQBonusData(self, pyqBonus):
        self.getPersonalSysProxy().syncPYQBonusData(pyqBonus)
