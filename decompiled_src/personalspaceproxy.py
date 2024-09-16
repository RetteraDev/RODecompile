#Embedded file name: /WORKSPACE/data/entities/client/guis/personalspaceproxy.o
import random
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
import utils
import gametypes
import const
import formula
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
from guis import ui
from guis.asObject import ASObject
import events
from guis.ui import unicode2gbk
from guis.ui import gbk2unicode
from guis import richTextUtils
from helpers import taboo
from callbackHelper import Functor
from gamestrings import gameStrings
from data import friend_location_data as FLD
from cdata import personal_zone_config_data as PZCD
from data import personal_zone_tag_data as PZTD
from data import title_data as TD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import personal_zone_bonus_data as PZBD
from cdata import region_server_name_data as RSND
from data import fight_for_love_config_data as FFLCD
from data import photo_border_data as PBD
DEFAULTPHOTO = 'headIcon/%s.dds'
NAME_LEN_LIMIT = 25

class PersonalSpaceProxy(DataProxy):
    MSG_LIST_ITEM_NUM = 5
    VISIT_TYPE_SELF = 0
    VISIT_TYPE_OTHER = 1
    TYPE_SAVEBIRTHDAY = 0
    TYPE_SAVECITY = 1
    MSG_MAX_NUM = 50
    TAG_SIZE_MAX = 22
    TAG_SIZE_MIN = 14
    TAG_COLOR_ARRAY = [16744742,
     16245081,
     10699007,
     16777215,
     2399474,
     4315482]

    def __init__(self, uiAdapter):
        super(PersonalSpaceProxy, self).__init__(uiAdapter)
        self.bindType = 'personalSpace'
        self.modelMap = {'getSpaceInfo': self.onGetSpaceInfo,
         'getDetailInfo': self.onGetDetailInfo,
         'getMonthAndDayInfo': self.onGetMonthAndDayInfo,
         'getProvinceCity': self.onGetProvinceCity,
         'setBirthInfo': self.onSetBirthInfo,
         'refreshMessageInfo': self.onRefreshMessageInfo,
         'likePerson': self.onLikePerson,
         'shareZone': self.onShareZone,
         'callLabelSetting': self.onCallLabelSetting,
         'addFriend': self.onAddFriend,
         'talk2Me': self.onTalk2Me,
         'getLabelTips': self.onGetLabelTips,
         'getZodiac': self.onGetZodiac,
         'openGiftGiving': self.onOpenGiftGiving,
         'likePersonTag': self.onLikePersonTag,
         'queryRole': self.onQueryRole,
         'reportPlayer': self.onReportPlayer,
         'openTouchPerson': self.onOpenTouchPerson,
         'openGiftBox': self.onOpenGiftBox,
         'calcPersent': self.onCalcPersent,
         'sendSignature': self.onSendSignature,
         'editRoleFigure': self.onEditRoleFigure,
         'openSetting': self.onOpenSetting,
         'isFriend': self.onIsFriend,
         'clickDetailItem': self.onClickDetailItem,
         'clickAddress': self.onClickAddress,
         'openReplyBox': self.onOpenReplyBox,
         'delZoneMsg': self.onDelZoneMsg,
         'getReplyMsgInfo': self.onGetReplyMsgInfo,
         'commitReplyMsg': self.onCommitReplyMsg,
         'closeReplyMsg': self.onCloseReplyMsg,
         'fetchMsgList': self.onFetchMsgList,
         'openLikeList': self.onOpenLikeList,
         'openGiftList': self.onOpenGiftList,
         'openTouchList': self.onOpenTouchList,
         'getFuDaiTips': self.onGetFuDaiTips,
         'openSettingFudai': self.onOpenSettingFudai,
         'getFuDaiNumber': self.onGetFuDaiNumber,
         'getFuDaiBtnShow': self.onGetFuDaiBtnShow,
         'clickVoiceItem': self.onClickVoiceItem,
         'shareHome': self.onShareHome,
         'openPrettyGirlFunc': self.onOpenPrettyGirlFunc,
         'getSkin': self.onGetSkin}
        self.spaceType = PersonalSpaceProxy.VISIT_TYPE_SELF
        self.mediator = None
        self.replyMsgMed = None
        self.friendSrcId = const.FRIEND_SRC_PERSONAL_ZONE
        self.reset()
        self.detailInfo = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_PERSONAL_SPACE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PERSONAL_SPACE:
            self.mediator = mediator
            itemList = []
        elif widgetId == uiConst.WIDGET_ZONE_MSG_REPLY:
            self.replyMsgMed = mediator
        if hasattr(self, 'autoOpenChat'):
            if self.autoOpenChat:
                self.openChatWnd()
            self.autoOpenChat = False

    def openChatWnd(self):
        self.replyGbId = 0
        self.replyDbId = 0
        self.replyName = ''
        self.uiAdapter.loadWidget(uiConst.WIDGET_ZONE_MSG_REPLY)

    def onRefreshMessageInfo(self, *arg):
        if self.ownerGbID:
            p = BigWorld.player()
            p.base.refreshZoneData(self.ownerGbID)

    def onIsFriend(self, *arg):
        return GfxValue(self.isFriend())

    def isFriend(self):
        p = BigWorld.player()
        if p.isGobalFirendGbId(self.ownerGbID):
            return True
        fVal = p.friend.get(self.ownerGbID, None)
        if fVal and hasattr(fVal, 'acknowledge'):
            return fVal.acknowledge
        return False

    def onSendSignature(self, *arg):
        msg = unicode2gbk(arg[3][0].GetString())
        p = BigWorld.player()
        if not msg:
            msg = '这个家伙很懒，什么都没有留下~'
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
            return
        isNormal, msg = taboo.checkBSingle(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
            return
        keyList = [const.PERSONAL_ZONE_DATA_SIGNATURE]
        valueList = [msg]
        p.base.setPersonalZoneInfo(keyList, valueList)

    def onOpenSetting(self, *arg):
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_PERSONAL)

    def onShareZone(self, *arg):
        if self.ownerGbID:
            msg = PZCD.data.get('PERSONAL_ZONE_LINK_MSG', '%s的个人空间')
            msg = msg % self.baseInfo.get('roleName', '')
            color = '#ffe566'
            if self.getFuDaiNumber() > 0:
                color = uiUtils.getColorValueByQuality(uiConst.QUALITY_ORANGE)
            msgFormat = "<font color= \'%s\'>[<a href = \'event:shareZone-%d-%d\'><u>%s</u></a>]</font>"
            isMissTianyu = self.isApplyGroupMT()
            if isMissTianyu:
                missTianyuPrefix = PZCD.data.get('shareLinkPrefix', '~萌~')
                msg = missTianyuPrefix + ' ' + msg
                color = '#ff3aff'
            msg = msgFormat % (color,
             self.ownerGbID,
             self.getHostId(),
             msg)
            audioKey = self.baseInfo['audioKey']
            if audioKey:
                msg = richTextUtils.voiceRichText(audioKey) + msg
            gameglobal.rds.ui.sendLink(msg)

    def onShareHome(self, *arg):
        if self.ownerGbID:
            msg = gameStrings.DESC_HOME_LINK % self.baseInfo.get('roleName', '')
            color = '#ffe566'
            if self.getFuDaiNumber() > 0:
                color = uiUtils.getColorValueByQuality(uiConst.QUALITY_ORANGE)
            msg = "<font color= \'%s\'>[<a href = \'event:shareHome-%s-%d-%d\'><u>%s</u></a>]</font>" % (color,
             self.baseInfo.get('roleName', ''),
             self.ownerGbID,
             self.getHostId(),
             msg)
            gameglobal.rds.ui.sendLink(msg)

    @ui.checkInventoryLock()
    def onOpenSettingFudai(self, *arg):
        gameglobal.rds.ui.spaceFuDai.show()

    def onGetFuDaiNumber(self, *arg):
        fudaiNumber = self.getFuDaiNumber()
        return GfxValue(fudaiNumber)

    def onReportPlayer(self, *arg):
        srcId = uiConst.MENU_CHAT
        gameglobal.rds.ui.prosecute.show(self.baseInfo.get('roleName', ''), srcId)

    def onQueryRole(self, *arg):
        if self.baseInfo.get('roleName'):
            p = BigWorld.player()
            p.cell.getEquipment(self.baseInfo['roleName'])

    def onGetLabelTips(self, *arg):
        tagId = int(arg[3][0].GetNumber())
        tmpText = ''
        if len(self.baseInfo.get('tags', {}).get(tagId, [])) > 0:
            if self.baseInfo['tags'][tagId][0] > 0:
                i = 0
                while i < 3 and i < len(self.baseInfo['tags'][tagId][1]):
                    if i == 2 or i == len(self.baseInfo['tags'][tagId][1]) - 1:
                        tmpText += self.baseInfo['tags'][tagId][1][i]
                    else:
                        tmpText += self.baseInfo['tags'][tagId][1][i] + '、'
                    i += 1

                if self.baseInfo['tags'][tagId][0] == 1:
                    tmpText = tmpText + '赞同了该标签。'
                else:
                    tmpText = tmpText + '等' + str(self.baseInfo['tags'][tagId][0]) + '位玩家赞同了该标签。'
            else:
                tmpText = '还没有人赞同过该标签'
        return GfxValue(gbk2unicode(tmpText))

    def onLikePerson(self, *arg):
        if self.isCrossServer(True):
            return
        if self.ownerGbID:
            p = BigWorld.player()
            p.base.likePersonalZone(self.ownerGbID)

    def onLikePersonTag(self, *arg):
        tagId = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        p.base.likePersonalZoneTag(self.ownerGbID, tagId)

    def isCrossServer(self, showMsg = False):
        if self.hostId and self.hostId != int(gameglobal.rds.gServerid):
            if showMsg:
                p = BigWorld.player()
                p.showGameMsg(GMDD.data.FUNC_FORBID_IN_CROSS_SERVER_ZONE, ())
            return True
        return False

    def getHostId(self):
        if self.hostId:
            return self.hostId
        return int(gameglobal.rds.gServerid)

    def onAddFriend(self, *arg):
        group = gametypes.FRIEND_GROUP_FRIEND
        p = BigWorld.player()
        if self.isCrossServer():
            p.base.addRemoteFriendRequest(self.hostId, self.ownerGbID)
        else:
            p.base.addContactByGbId(self.ownerGbID, group, self.friendSrcId)

    def onTalk2Me(self, *arg):
        gameglobal.rds.ui.chatToFriend.show(None, self._createFriendData(), False)

    def onGetZodiac(self, *arg):
        month = int(arg[3][0].GetNumber()) + 1
        day = int(arg[3][1].GetNumber()) + 1
        if month <= 0 or day <= 0:
            return GfxValue(gbk2unicode(''))
        n = ('\xc4\xa6\xf4\xc9\xd7\xf9', '\xcb\xae\xc6\xbf\xd7\xf9', '\xcb\xab\xd3\xe3\xd7\xf9', '\xb0\xd7\xd1\xf2\xd7\xf9', '\xbd\xf0\xc5\xa3\xd7\xf9', '\xcb\xab\xd7\xd3\xd7\xf9', '\xbe\xde\xd0\xb7\xd7\xf9', '\xca\xa8\xd7\xd3\xd7\xf9', '\xb4\xa6\xc5\xae\xd7\xf9', '\xcc\xec\xb3\xd3\xd7\xf9', '\xcc\xec\xd0\xab\xd7\xf9', '\xc9\xe4\xca\xd6\xd7\xf9')
        d = ((1, 20),
         (2, 19),
         (3, 21),
         (4, 21),
         (5, 21),
         (6, 22),
         (7, 23),
         (8, 23),
         (9, 23),
         (10, 23),
         (11, 23),
         (12, 23))
        return GfxValue(gbk2unicode(n[len(filter(lambda y: y <= (month, day), d)) % 12]))

    def _createFriendData(self):
        return {'id': str(self.ownerGbID),
         'name': self.baseInfo['roleName'],
         'photo': self.baseInfo['photo'],
         'signature': self.baseInfo['signature'],
         'state': 1,
         'yixinOpenId': 0,
         'photoBorderIcon': self.baseInfo['photoBorderIcon']}

    def onGetSpaceInfo(self, *arg):
        tempData = self.getSpaceaBaseInfo()
        return tempData

    def onSetBirthInfo(self, *arg):
        value = unicode2gbk(arg[3][0].GetString())
        _type = int(arg[3][1].GetNumber())
        keyList = []
        if _type == PersonalSpaceProxy.TYPE_SAVEBIRTHDAY:
            keyList = [const.PERSONAL_ZONE_DATA_BIRTHDAY]
            self.baseInfo['birthday'] = value
        elif _type == PersonalSpaceProxy.TYPE_SAVECITY:
            keyList = [const.PERSONAL_ZONE_DATA_CITY]
            self.baseInfo['city'] = value
        valueList = [value]
        p = BigWorld.player()
        p.base.setPersonalZoneInfo(keyList, valueList)

    def onGetDetailInfo(self, *arg):
        if self.ownerGbID:
            p = BigWorld.player()
            p.base.getPersonalZoneInfo(self.ownerGbID, self.hostId)

    def onGetFuDaiTips(self, *arg):
        if self.getFuDaiNumber() <= 0:
            tmpText = '空间主人未设置福袋'
        else:
            name = PZBD.data.get(self.baseInfo['fuDaiBonusType'], {}).get('name', '')
            tmpText = '空间主人设置了%s，还剩%d份，赶紧给主人点个喜欢吧，有几率获得福袋哦' % (name, self.baseInfo['fuDaiBonusNum'])
        return GfxValue(gbk2unicode(tmpText))

    def onCallLabelSetting(self, *arg):
        tags = self.baseInfo.get('tags', {})
        gameglobal.rds.ui.spaceLabelSetting.show(tags)

    def onOpenGiftGiving(self, *arg):
        if self.ownerGbID and self.baseInfo.get('roleName'):
            gameglobal.rds.ui.spaceGiftGiving.show(self.ownerGbID, self.baseInfo['roleName'], self.hostId)

    def onOpenTouchPerson(self, *arg):
        if self.ownerGbID and self.baseInfo.get('roleName'):
            gameglobal.rds.ui.spaceTouch.show(self.ownerGbID, self.baseInfo['roleName'], self.hostId)

    def onOpenGiftBox(self, *arg):
        if self.isCrossServer(True):
            return
        self.waitOpenGiftBox = True
        p = BigWorld.player()
        p.base.getZoneGiftData(self.ownerGbID)

    def onGetMonthAndDayInfo(self, *arg):
        tempMonth = []
        tempMonth = range(1, 13)
        tempDay = []
        tempDay = [range(1, 32),
         range(1, 30),
         range(1, 32),
         range(1, 31),
         range(1, 32),
         range(1, 31),
         range(1, 32),
         range(1, 32),
         range(1, 31),
         range(1, 32),
         range(1, 31),
         range(1, 32)]
        tempData = {}
        tempData['month'] = tempMonth
        tempData['day'] = tempDay
        return uiUtils.dict2GfxDict(tempData, True)

    def onGetInfoPersent(self, *arg):
        pass

    def onGetProvinceCity(self, *arg):
        tempProvince = []
        tempCity = []
        i = 1
        while FLD.data.get(i, {}):
            tempProvince.append(FLD.data.get(i, {})['provinceName'])
            tempCity.append(FLD.data.get(i, {})['cityNames'])
            i += 1

        tempData = {}
        tempData['province'] = tempProvince
        tempData['city'] = tempCity
        return uiUtils.dict2GfxDict(tempData, True)

    def getSpaceaBaseInfo(self):
        msgArray = self.baseInfo.get('msgArray', [])
        newMsgNum = self.baseInfo.get('newMsgNum', 0)
        msgArray = self.getGfxMsgArray(msgArray, newMsgNum)
        ret = uiUtils.dict2GfxDict(self.baseInfo, True)
        ret.SetMember('msgArray', msgArray)
        return ret

    def getValue(self, key):
        if key == '':
            return uiUtils.array2GfxAarry([], True)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PERSONAL_SPACE)

    def clearWidget(self):
        self.mediator = None
        self.detailInfo = {}
        if self.replyMsgMed:
            self.onCloseReplyMsg()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PERSONAL_SPACE)

    def reset(self):
        self.replyGbId = 0
        self.replyDbId = 0
        self.replyName = None
        self.baseInfo = {}
        self.ownerGbID = 0
        self.waitOpenGiftBox = False
        self.persentInfo = {}
        self.ckBoxHideMyJieqi = 0
        self.zoneMsgPermission = 0
        self.zoneHeadIconPermission = 0
        self.voiceMc = None
        self.friendSrcId = const.FRIEND_SRC_PERSONAL_ZONE
        self.hostId = 0

    def onOpenReplyBox(self, *arg):
        gbId = int(arg[3][0].GetString())
        dbId = int(arg[3][1].GetString())
        replyName = unicode2gbk(arg[3][2].GetString())
        self.replyGbId = gbId
        self.replyDbId = dbId
        self.replyName = replyName
        self.uiAdapter.loadWidget(uiConst.WIDGET_ZONE_MSG_REPLY)

    def onDelZoneMsg(self, *arg):
        gbId = int(arg[3][0].GetString())
        dbId = int(arg[3][1].GetString())
        gameglobal.rds.ui.messageBox.showYesNoMsgBox('确定删除该留言', Functor(self.realDelZoneMsg, gbId, dbId))

    def realDelZoneMsg(self, gbId, dbId):
        p = BigWorld.player()
        p.base.delZoneMsg(self.ownerGbID, dbId)

    def getGfxMsgArray(self, msgArray, newMsgNum):
        ret = []
        if msgArray:
            l = len(msgArray)
            p = BigWorld.player()
            for i, item in enumerate(msgArray):
                dbID = 0
                mGbID = 0
                mName = ''
                msg = ''
                replyId = 0
                replyName = ''
                photo = ''
                tWhen = 0
                serverId = 0
                borderId = 0
                if len(item) == 8:
                    dbID, mGbID, mName, msg, replyId, replyName, photo, tWhen = item
                elif len(item) == 9:
                    dbID, mGbID, mName, msg, replyId, replyName, photo, tWhen, extra = item
                    if extra in RSND.data or extra > 99999 and extra / 10 in RSND.data:
                        serverId = extra
                    else:
                        borderId = extra
                elif len(item) == 10:
                    dbID, mGbID, mName, msg, replyId, replyName, photo, tWhen, serverId, borderId = item
                if not borderId:
                    borderId = SCD.data.get('defaultBorderId', 0)
                isApp = False
                isCrossServer = False
                if serverId > 0:
                    if serverId > 99999 and serverId % 10 == 0:
                        isCrossServer = True
                        serverId = serverId / 10
                    else:
                        isApp = True
                item = {'dbId': str(dbID),
                 'gbId': str(mGbID),
                 'msgTxt': msg,
                 'photo': photo,
                 'replyName': mName,
                 'dateTxt': utils.formatDate(tWhen),
                 'newIcon': i >= l - newMsgNum,
                 'isMe': mGbID == p.gbId or self.ownerGbID == p.gbId,
                 'isShow': 1,
                 'isApp': isApp,
                 'isCrossServer': isCrossServer,
                 'serverId': serverId,
                 'photoBorderIcon': p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)}
                if replyName:
                    item['nameTxt'] = '%s 回复 %s' % (mName, replyName)
                else:
                    item['nameTxt'] = mName
                ret.append(item)

            ret.reverse()
        if len(ret) < PersonalSpaceProxy.MSG_LIST_ITEM_NUM:
            for n in xrange(len(ret), PersonalSpaceProxy.MSG_LIST_ITEM_NUM):
                item = {'isShow': 0}
                ret.append(item)

        return uiUtils.array2GfxAarry(ret, True)

    def onGetReplyMsgInfo(self, *arg):
        ret = {'replyName': self.replyName,
         'msgMaxNum': PersonalSpaceProxy.MSG_MAX_NUM}
        return uiUtils.dict2GfxDict(ret, True)

    def onCommitReplyMsg(self, *arg):
        p = BigWorld.player()
        if self.zoneMsgPermission == 1:
            if not self.isFriend() and self.spaceType == PersonalSpaceProxy.VISIT_TYPE_OTHER:
                p.showGameMsg(GMDD.data.SPACE_MSG_PERMISSION_FRIEND, ())
                self.onCloseReplyMsg()
                return
        msg = unicode2gbk(arg[3][0].GetString())
        if not msg:
            return
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
            return
        isNormal, msg = taboo.checkBSingle(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
            return
        if formula.isBalanceArenaCrossServerML(formula.getMLGNo(p.spaceNo)):
            p.cell.commitZoneMsgCell(self.ownerGbID, msg, self.replyDbId, self.replyName, self.replyGbId, self.hostId)
        else:
            p.base.commitZoneMsg(self.ownerGbID, msg, self.replyDbId, self.replyName, self.replyGbId, self.hostId)
        self.onCloseReplyMsg()

    def onCloseReplyMsg(self, *arg):
        self.replyMsgMed = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZONE_MSG_REPLY)

    def onOpenZone(self, ownerGbId, data, hostId = 0):
        if self.mediator:
            self.hide()
        p = BigWorld.player()
        if p.profileIcon != '':
            p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, p.profileIcon, gametypes.NOS_FILE_PICTURE, self.onDownloadSelfProfilePhoto, (None,))
        if (p.profileIconStatus == gametypes.NOS_FILE_STATUS_SERVER_APPROVED or p.profileIconStatus == gametypes.NOS_FILE_STATUS_APPROVED) and p.profileIconUsed == False and p.iconUpload == True:
            photo = p.profileIcon if p.profileIcon else ''
            sex = p.physique.sex
            p.base.abandonNOSFile(p.friend.photo)
            p.cell.updateProfileApply(True, False)
            p.base.updateProfile(0, photo, 0, 1, 1, sex, 0, 0, 0, '', '', '')
            keyList = [const.PERSONAL_ZONE_DATA_CUSTOM_PHOTO, const.PERSONAL_ZONE_DATA_CURR_PHOTO]
            valueList = [p.profileIcon, p.profileIcon]
            p.base.setPersonalZoneInfo(keyList, valueList)
        if ownerGbId == p.gbId:
            self.spaceType = PersonalSpaceProxy.VISIT_TYPE_SELF
        else:
            self.spaceType = PersonalSpaceProxy.VISIT_TYPE_OTHER
        self.ownerGbID = ownerGbId
        self.hostId = hostId
        config = data[const.PERSONAL_ZONE_DATA_CONFIG]
        configs = []
        if config:
            configs = config.split('|')
            if len(configs) == 3:
                p.ckBoxHideMyJieqi = int(configs[0])
                p.zoneMsgPermission = int(configs[1])
                p.zoneHeadIconPermission = int(configs[2])
                self.ckBoxHideMyJieqi = int(configs[0])
                self.zoneMsgPermission = int(configs[1])
                self.zoneHeadIconPermission = int(configs[2])
        self.baseInfo['roleName'] = data[const.PERSONAL_ZONE_DATA_NAME]
        self.baseInfo['hostId'] = self.hostId
        _school = data[const.PERSONAL_ZONE_DATA_SCHOOL]
        self.baseInfo['_school'] = data[const.PERSONAL_ZONE_DATA_SCHOOL]
        self.baseInfo['schoolName'] = const.SCHOOL_DICT[_school]
        self.baseInfo['schoolState'] = uiConst.SCHOOL_FRAME_DESC[_school]
        self.baseInfo['lv'] = data[const.PERSONAL_ZONE_DATA_LV]
        self.baseInfo['_sex'] = data[const.PERSONAL_ZONE_DATA_SEX]
        self.baseInfo['fuDaiBonusType'] = data[const.PERSONAL_ZONE_DATA_BONUS_TYPE]
        self.baseInfo['fuDaiBonusNum'] = data[const.PERSONAL_ZONE_DATA_BONUS_NUM]
        _sex = data[const.PERSONAL_ZONE_DATA_SEX]
        if _sex == const.SEX_MALE:
            self.baseInfo['sex'] = 'man'
        elif _sex == const.SEX_FEMALE:
            self.baseInfo['sex'] = 'woman'
        else:
            self.baseInfo['sex'] = 'man'
        self.baseInfo['sexType'] = _sex
        if ownerGbId == p.gbId:
            self.baseInfo['relativeTitle'] = '我'
        elif _sex == const.SEX_MALE:
            self.baseInfo['relativeTitle'] = '他'
        elif _sex == const.SEX_FEMALE:
            self.baseInfo['relativeTitle'] = '她'
        else:
            self.baseInfo['relativeTitle'] = '他'
        self.baseInfo['spaceType'] = self.spaceType
        self.baseInfo['signature'] = data[const.PERSONAL_ZONE_DATA_SIGNATURE]
        self.baseInfo['likeNum'] = data[const.PERSONAL_ZONE_DATA_LIKE_NUM]
        self.baseInfo['touchNum'] = data[const.PERSONAL_ZONE_DATA_TOUCH_NUM]
        self.baseInfo['msgArray'] = data[const.PERSONAL_ZONE_DATA_MSG]
        self.baseInfo['popularity'] = data[const.PERSONAL_ZONE_DATA_POPULARITY]
        self.baseInfo['hotLv'] = self.getHotLv(self.baseInfo['popularity'])
        self.baseInfo['intimacy'] = data[const.PERSONAL_ZONE_DATA_INTIMACY]
        self.baseInfo['birthday'] = data[const.PERSONAL_ZONE_DATA_BIRTHDAY]
        self.baseInfo['city'] = data[const.PERSONAL_ZONE_DATA_CITY]
        self.baseInfo['tags'] = data[const.PERSONAL_ZONE_DATA_TAGS]
        self.baseInfo['tagsFormat'] = self.getTagsInfo(self.baseInfo['tags'])
        self.baseInfo['curTitle'] = data[const.PERSONAL_ZONE_DATA_CURR_TITLE]
        self.baseInfo['isOnline'] = data[const.PERSONAL_ZONE_DATA_ONLINE]
        self.baseInfo['customPhoto'] = data[const.PERSONAL_ZONE_DATA_CUSTOM_PHOTO]
        self.baseInfo['sysPhoto'] = data[const.PERSONAL_ZONE_DATA_SYS_PHOTO]
        self.baseInfo['curPhoto'] = data[const.PERSONAL_ZONE_DATA_CURR_PHOTO]
        self.baseInfo['mentorName'] = self.calcMentorName(data.get(const.PERSONAL_ZONE_DATA_MENTOR_NAME, []))
        _audiokey = data.get(const.PERSONAL_ZONE_DATA_AUDIO_KEY, '')
        self.baseInfo['audioKey'] = _audiokey if _audiokey != '0' and gameglobal.rds.configData.get('enablePersonalZoneVoice', False) else ''
        self.baseInfo['audioTip'] = '暂时仅支持APP端录制和修改个性语音'
        self.baseInfo['floorNo'] = data.get(const.PERSONAL_ZONE_DATA_ROOM_FLOOR_NO, 0)
        self.baseInfo['roomNo'] = data.get(const.PERSONAL_ZONE_DATA_ROOM_NO, 0)
        self.baseInfo['roomWealth'] = data.get(const.PERSONAL_ZONE_DATA_ROOM_WEALTH, 0)
        self.baseInfo['roomColor'] = uiConst.ROOM_NO_COLOR.get(self.baseInfo['roomNo'], '')
        _roomWealthLv = gameglobal.rds.ui.homeCheckHouses.getWealthLv(self.baseInfo['roomWealth'])
        roomWealthLvMaxVal = gameglobal.rds.ui.homeCheckHouses.getWealthLvMaxVal(self.baseInfo['roomWealth'])
        finalDesc = '0' if not self.baseInfo['roomNo'] else '%s(%d/%d)' % (_roomWealthLv, self.baseInfo['roomWealth'], roomWealthLvMaxVal)
        self.baseInfo['roomWealthLv'] = _roomWealthLv
        self.baseInfo['wealthDesc'] = finalDesc
        self.calcHomeStr()
        _photo = self.baseInfo['curPhoto']
        if self.spaceType == PersonalSpaceProxy.VISIT_TYPE_SELF and p.profileIconStatus == gametypes.NOS_FILE_STATUS_PENDING and p.profileIconUsed == False and p.iconUpload == True and p.imageName:
            _photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + p.imageName + utils.getProfileIconSuffix()
        self.baseInfo['photo'] = _photo if _photo else DEFAULTPHOTO % str(_school * 10 + _sex)
        if not self.baseInfo['customPhoto'] or p.profileIconStatus != gametypes.NOS_FILE_STATUS_APPROVED:
            self.baseInfo['customPhoto'] = self.baseInfo['photo']
        gamelog.debug('photo', self.baseInfo['photo'])
        if self.zoneHeadIconPermission == 1:
            if not self.isFriend() and self.spaceType == PersonalSpaceProxy.VISIT_TYPE_OTHER:
                self.baseInfo['photo'] = DEFAULTPHOTO % str(_school * 10 + _sex)
        self.baseInfo['newLikeNum'] = data[const.PERSONAL_ZONE_DATA_NEW_LIKE_NUM]
        self.baseInfo['newMsgNum'] = data[const.PERSONAL_ZONE_DATA_NEW_MSG_NUM]
        self.baseInfo['weekPopularity'] = data[const.PERSONAL_ZONE_DATA_WEEK_POPULARITY]
        self.baseInfo['giftNum'] = data[const.PERSONAL_ZONE_DATA_GIFT_NUM]
        self.baseInfo['missTianyu'] = data.get(const.PERSONAL_ZONE_DATA_MISSTIANYU, False) and utils.getNow() < gameglobal.rds.configData.get('missTianyuEndtime', 0) and gameglobal.rds.configData.get('enableMissTianyu', False)
        self.baseInfo['skinId'] = data.get(const.PERSONAL_ZONE_DATA_SKIN, 1)
        self.baseInfo['photoBorderIcon'] = p.getPhotoBorderIcon(data.get(const.PERSONAL_ZONE_PHOTO_BORDER, 0), uiConst.PHOTO_BORDER_ICON_SIZE156)
        self.baseInfo['applyGroupMT'] = data.get(const.PERSONAL_ZONE_DATA_PYQ, {}).get('applyGroupMT', None)
        self.persentInfo['photo'] = True if _photo else False
        self.persentInfo['birthday'] = True if self.baseInfo.get('birthday', '') else False
        self.persentInfo['city'] = True if self.baseInfo.get('city', '') else False
        self.persentInfo['signature'] = True if self.baseInfo.get('signature', '') else False
        self.persentInfo['tags'] = True if len(self.baseInfo.get('tags', {})) else False
        enablePersonalSpaceBfData = gameglobal.rds.configData.get('enablePersonalSpaceBfData', False)
        self.detailInfo = {}
        self.detailInfo['firstCnt'] = data.get(const.PERSONAL_ZONE_DATA_BF_FIRST_NUM, 0) if enablePersonalSpaceBfData else -1
        self.detailInfo['secondCnt'] = data.get(const.PERSONAL_ZONE_DATA_BF_SECOND_NUM, 0) if enablePersonalSpaceBfData else -1
        self.detailInfo['thirdCnt'] = data.get(const.PERSONAL_ZONE_DATA_BF_THIRD_NUM, 0) if enablePersonalSpaceBfData else -1
        self.detailInfo['mvp'] = data.get(const.PERSONAL_ZONE_DATA_BF_MVP_NUM, 0) if enablePersonalSpaceBfData else -1
        self.detailInfo.setdefault('partnerNames', '')
        self.detailInfo.setdefault('simplePartnerNames', '')
        self.show()
        fromItemBorderId = data.get(const.PERSONAL_ZONE_DATA_BORDER_OP, 0)
        if fromItemBorderId:
            if not gameglobal.rds.ui.spaceHeadSetting.mediator:
                gameglobal.rds.ui.spaceHeadSetting.show(self.baseInfo.get('customPhoto', ''), self.baseInfo.get('sysPhoto', ''), self.baseInfo.get('_school', ''), self.baseInfo.get('_sex', ''), self.baseInfo.get('photo', ''), fromItemBorderId)
            else:
                gameglobal.rds.ui.spaceHeadSetting.updateBodrerPanel(fromItemBorderId)

    def isOnline(self):
        return self.baseInfo.get('isOnline', 0)

    def calcHomeStr(self):
        homeStr = '暂未拥有房屋'
        homeEntry = False
        if self.baseInfo.get('roomNo', 0) and self.baseInfo.get('floorNo', 0):
            homeStr = '妖精旅社-%d楼%s-%s' % (self.baseInfo.get('floorNo', 0), self.baseInfo.get('roomColor', ''), self.baseInfo.get('roomWealthLv', ''))
            homeEntry = True
        self.baseInfo['homeStr'] = homeStr
        self.baseInfo['homeEntry'] = homeEntry

    def updatePhotoBorderInfo(self, ownerGbId, data):
        p = BigWorld.player()
        self.baseInfo['photoBorderIcon'] = p.getPhotoBorderIcon(data.get(const.PERSONAL_ZONE_PHOTO_BORDER, 0), uiConst.PHOTO_BORDER_ICON_SIZE156)
        if self.mediator:
            self.mediator.Invoke('updatePhotoBorderInfo', GfxValue(gbk2unicode(self.baseInfo['photoBorderIcon'])))

    def updateHeadInfo(self, ownerGbId, data):
        self.baseInfo['customPhoto'] = data.get(const.PERSONAL_ZONE_DATA_CUSTOM_PHOTO, self.baseInfo.get('customPhoto', ''))
        self.baseInfo['sysPhoto'] = data.get(const.PERSONAL_ZONE_DATA_SYS_PHOTO, self.baseInfo.get('sysPhoto', ''))
        self.baseInfo['curPhoto'] = data.get(const.PERSONAL_ZONE_DATA_CURR_PHOTO, self.baseInfo.get('curPhoto', ''))
        _photo = self.baseInfo['curPhoto']
        _school = self.baseInfo['_school']
        _sex = self.baseInfo['_sex']
        p = BigWorld.player()
        if self.spaceType == PersonalSpaceProxy.VISIT_TYPE_SELF and p.profileIconStatus == gametypes.NOS_FILE_STATUS_PENDING and p.profileIconUsed == False and p.iconUpload == True and p.imageName:
            _photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + p.imageName + utils.getProfileIconSuffix()
        self.baseInfo['photo'] = _photo if _photo else DEFAULTPHOTO % str(_school * 10 + _sex)
        if not self.baseInfo['customPhoto'] or p.profileIconStatus != gametypes.NOS_FILE_STATUS_APPROVED:
            self.baseInfo['customPhoto'] = self.baseInfo['photo']
        gamelog.debug('photo', self.baseInfo['photo'])
        if self.zoneHeadIconPermission == 1:
            if not self.isFriend() and self.spaceType == PersonalSpaceProxy.VISIT_TYPE_OTHER:
                self.baseInfo['photo'] = DEFAULTPHOTO % str(_school * 10 + _sex)
        if self.mediator:
            self.mediator.Invoke('updateHeadInfo', GfxValue(gbk2unicode(self.baseInfo['photo'])))

    def getHotLv(self, _value):
        hotValue = SCD.data.get('PERSONAL_ZONE_HOT_VALUE', ())
        lv = 0
        for v in hotValue:
            if _value >= v:
                lv += 1
            else:
                break

        return lv

    def getTagsInfo(self, tags):
        ret = []
        minCount = 10000000
        maxCount = -1
        for key, value in tags.iteritems():
            count = value[0]
            if count > maxCount:
                maxCount = count
            if count < minCount:
                minCount = count
            ret.append({'name': PZTD.data.get(key, {}).get('name', ''),
             'count': count,
             'tagId': key})

        fontsize = 0
        if maxCount == minCount:
            k = 0.5
            fontsize = int((self.TAG_SIZE_MAX + self.TAG_SIZE_MIN) * 0.5)
        else:
            k = (self.TAG_SIZE_MAX - self.TAG_SIZE_MIN) * 1.0 / (maxCount - minCount)
        for i, item in enumerate(ret):
            item['size'] = random.randint(0, 4) + fontsize if fontsize else int(k * (item['count'] - minCount) + self.TAG_SIZE_MIN)
            item['color'] = self.TAG_COLOR_ARRAY[i]

        ret.sort(lambda x, y: cmp(x['size'], y['size']), reverse=True)
        return ret

    def onCalcPersent(self, *arg):
        curNum = 0
        for key in self.persentInfo:
            if self.persentInfo[key]:
                curNum += 1

        persentNum = int(float(curNum) / float(len(self.persentInfo)) * 100)
        return GfxValue(persentNum)

    def onQueryPersonalZoneInfo(self, ownerGbId, data):
        titleName = self.getActivateTitle(data)
        self.detailInfo['titleName'] = titleName
        self.detailInfo['guildName'] = data[const.PERSONAL_ZONE_DATA_GUILD_NAME]
        self.detailInfo['mentorName'] = self.calcMentorName(data.get(const.PERSONAL_ZONE_DATA_MENTOR_NAME, []))
        if not self.detailInfo['mentorName']:
            self.detailInfo['mentorName'] = self.baseInfo.get('mentorName', '')
        self.detailInfo['intimacyTgtName'] = data[const.PERSONAL_ZONE_DATA_INTIMACY_TGT_NAME]
        self.detailInfo['intimacyTgtGbid'] = data[const.PERSONAL_ZONE_DATA_INTIMACY_TGT_GBID]
        self.detailInfo['combatScore'] = int(data.get(const.PERSONAL_ZONE_DATA_COMBAT_SCORE, 0))
        self.detailInfo['achievePoint'] = data[const.PERSONAL_ZONE_DATA_ACHIEVE_POINT]
        self.detailInfo['renPin'] = data[const.PERSONAL_ZONE_DATA_HONOR_FAME]
        self.detailInfo['haoQi'] = data[const.PERSONAL_ZONE_DATA_HAO_QI]
        self.detailInfo['guiBao'] = data[const.PERSONAL_ZONE_DATA_GUI_BAO]
        self.detailInfo['arenaScore'] = data[const.PERSONAL_ZONE_DATA_ARENA_SCORE]
        self.detailInfo['socLv'] = data[const.PERSONAL_ZONE_DATA_SOCLV]
        self.detailInfo['birthday'] = self.baseInfo.get('birthday', '')
        self.detailInfo['city'] = self.baseInfo.get('city', '')
        if self.ckBoxHideMyJieqi == 1:
            self.detailInfo['intimacyTgtName'] = ''
        self.persentInfo['birthday'] = True if self.baseInfo.get('birthday', '') else False
        self.persentInfo['city'] = True if self.baseInfo.get('city', '') else False
        self.baseInfo['intimacyTgtName'] = self.detailInfo['intimacyTgtName']
        self.setDetailInfo()
        if self.mediator:
            self.mediator.Invoke('setFuDaiIcon')
        p = BigWorld.player()
        p.cell.queryPartnerMemberInfo(ownerGbId)

    def onGetPartnerInfo(self, partnerList):
        p = BigWorld.player()
        self.detailInfo['partnerNames'] = ''
        self.detailInfo['simplePartnerNames'] = ''
        template = "<font color= \'#174C66\' size = \'12\'><a href = \'event:openZoneByName%s\'><u>%s</u>;</a></font>"
        nameLength = 0
        for gbId, name in partnerList:
            strContent = ''
            try:
                strContent = name.decode(utils.defaultEncoding())
            except:
                strContent = ''

            nameLength += len(strContent)
            if gbId == self.ownerGbID:
                continue
            nameStr = ''
            if strContent and nameLength >= NAME_LEN_LIMIT:
                try:
                    nameStr = strContent[0:5]
                    nameStr = nameStr.encode(utils.defaultEncoding())
                    nameStr += '...'
                except:
                    nameStr = ''

            if not nameStr:
                nameStr = name
            self.detailInfo['simplePartnerNames'] += template % (name, nameStr)
            self.detailInfo['partnerNames'] += template % (name, name)

        self.setDetailInfo()

    def setDetailInfo(self):
        if self.mediator:
            self.mediator.Invoke('setDetailInfo', uiUtils.dict2GfxDict(self.detailInfo, True))

    def calcMentorName(self, nameArr):
        if not nameArr:
            return ''
        msg = ''
        for _name in nameArr:
            msg += "<font color= \'#174C66\'><a href = \'event:openZoneByName%s\'><u>%s</u>;</a></font>" % (_name, _name)

        return msg

    def getFuDaiNumber(self):
        if self.baseInfo.get('fuDaiBonusType', 0) > 0:
            return self.baseInfo.get('fuDaiBonusNum', 0)
        return 0

    def onGetFuDaiBtnShow(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableFuDaiProxy', False))

    def onUpdateInfo(self, ownerGbId, op, data):
        self.baseInfo['msgArray'] = data.get(const.PERSONAL_ZONE_DATA_MSG, self.baseInfo.get('msgArray', {}))
        self.baseInfo['likeNum'] = data.get(const.PERSONAL_ZONE_DATA_LIKE_NUM, self.baseInfo.get('likeNum', 0))
        self.baseInfo['touchNum'] = data.get(const.PERSONAL_ZONE_DATA_TOUCH_NUM, self.baseInfo.get('touchNum', 0))
        self.baseInfo['popularity'] = data.get(const.PERSONAL_ZONE_DATA_POPULARITY, self.baseInfo.get('popularity', 0))
        self.baseInfo['hotLv'] = self.getHotLv(self.baseInfo['popularity'])
        self.baseInfo['giftNum'] = data.get(const.PERSONAL_ZONE_DATA_GIFT_NUM, self.baseInfo.get('giftNum', 0))
        self.baseInfo['newLikeNum'] = data.get(const.PERSONAL_ZONE_DATA_NEW_LIKE_NUM, self.baseInfo.get('newLikeNum', 0))
        self.baseInfo['newMsgNum'] = data.get(const.PERSONAL_ZONE_DATA_NEW_MSG_NUM, self.baseInfo.get('newMsgNum', 0))
        self.freshTagsAddOne(self.baseInfo.get('tags', {}), data.get(const.PERSONAL_ZONE_DATA_TAGS, {}))
        self.baseInfo['tags'] = data.get(const.PERSONAL_ZONE_DATA_TAGS, self.baseInfo.get('tags', {}))
        self.baseInfo['signature'] = data.get(const.PERSONAL_ZONE_DATA_SIGNATURE, self.baseInfo.get('signature', ''))
        self.baseInfo['tagsFormat'] = self.getTagsInfo(self.baseInfo['tags'])
        self.baseInfo['isOnline'] = data.get(const.PERSONAL_ZONE_DATA_ONLINE, self.baseInfo.get('isOnline', False))
        self.baseInfo['fuDaiBonusType'] = data.get(const.PERSONAL_ZONE_DATA_BONUS_TYPE, self.baseInfo.get('fuDaiBonusType', 0))
        self.baseInfo['fuDaiBonusNum'] = data.get(const.PERSONAL_ZONE_DATA_BONUS_NUM, self.baseInfo.get('fuDaiBonusNum', 0))
        self.baseInfo['floorNo'] = data.get(const.PERSONAL_ZONE_DATA_ROOM_FLOOR_NO, self.baseInfo.get('floorNo', 0))
        self.persentInfo['tags'] = True if len(self.baseInfo['tags']) else False
        needAdjustTag = op == const.PERSONAL_ZONE_OP_ALTER_TAGS and self.spaceType == PersonalSpaceProxy.VISIT_TYPE_SELF
        self.calcHomeStr()
        if self.mediator:
            tempData = self.getSpaceaBaseInfo()
            self.mediator.Invoke('updateBaseInfo', (tempData, GfxValue(needAdjustTag)))
            self.mediator.Invoke('setFuDaiIcon')

    def onGetZoneGiftData(self, ownerGbId, data):
        self.baseInfo['giftDict'] = data.get(const.PERSONAL_ZONE_DATA_GIFT_DICT, {})
        self.baseInfo['weekGiftNum'] = data.get(const.PERSONAL_ZONE_DATA_GIFT_WEEK_NUM, 0)
        self.baseInfo['giftTop'] = data.get(const.PERSONAL_ZONE_DATA_GIFT_TOP, {})
        num = 0
        for key in self.baseInfo['giftDict']:
            num += self.baseInfo['giftDict'][key]

        self.baseInfo['giftNum'] = num
        if self.waitOpenGiftBox:
            gameglobal.rds.ui.spaceGiftBox.show(self.ownerGbID, self.baseInfo['roleName'], data, num, self.spaceType, self.hostId)
            self.waitOpenGiftBox = False
        tempData = self.getSpaceaBaseInfo()
        if self.mediator:
            self.mediator.Invoke('updateBaseInfo', (tempData, GfxValue(False)))

    def refreshMsgList(self, data, newMsgNum = 0):
        data = self.getGfxMsgArray(data, newMsgNum)
        if self.mediator:
            self.mediator.Invoke('refreshMsgList', data)

    def delZoneMsgCallback(self, ownerGbId, msgDbId):
        if ownerGbId == self.ownerGbID:
            if self.baseInfo['msgArray']:
                for item in self.baseInfo['msgArray']:
                    if item[0] == msgDbId:
                        self.baseInfo['msgArray'].remove(item)
                        break

            self.refreshMsgList(self.baseInfo['msgArray'])

    def commitZoneMsgCallback(self, ownerGbId, data):
        if ownerGbId == self.ownerGbID:
            self.baseInfo['msgArray'] = data
            self.refreshMsgList(data, 1)

    def onOpenLikeList(self, *arg):
        if self.isCrossServer(True):
            return
        p = BigWorld.player()
        if self.ownerGbID:
            p.base.getZoneLikeData(self.ownerGbID)

    def onOpenGiftList(self, *arg):
        if self.isCrossServer(True):
            return
        p = BigWorld.player()
        if self.ownerGbID:
            p.base.getZoneGiftHistory(self.ownerGbID)

    def onOpenTouchList(self, *arg):
        if self.isCrossServer(True):
            return
        p = BigWorld.player()
        if self.ownerGbID:
            p.base.getZoneTouchData(self.ownerGbID)

    def openZoneMyself(self, srcId = 0):
        p = BigWorld.player()
        self.openZoneOther(p.gbId, None, srcId)

    def openZoneOther(self, ownerGbID, roleName = None, srcId = 0, hostId = 0, autoOpenChat = False):
        self.friendSrcId = const.FRIEND_SRC_PERSONAL_ZONE
        if gameglobal.rds.configData.get('enablePersonalZone', False):
            self.autoOpenChat = autoOpenChat
            p = BigWorld.player()
            if ownerGbID:
                if formula.isBalanceArenaCrossServerML(formula.getMLGNo(p.spaceNo)):
                    p.cell.openZoneCell(ownerGbID, srcId, hostId)
                else:
                    p.base.openZone(ownerGbID, srcId, hostId)
            elif roleName:
                p.base.openZoneByName(roleName, srcId, hostId)
        else:
            gameglobal.rds.ui.systemTips.show('个人空间暂在测试，敬请期待')

    def onEditRoleFigure(self, *arg):
        if gameglobal.rds.configData.get('enableNewFigureUpload', False):
            gameglobal.rds.ui.spaceHeadSetting.show(self.baseInfo.get('customPhoto', ''), self.baseInfo.get('sysPhoto', ''), self.baseInfo.get('_school', ''), self.baseInfo.get('_sex', ''), self.baseInfo.get('photo', ''))
        else:
            gameglobal.rds.ui.systemTips.show('个人空间头像设置功能暂在测试，敬请期待')

    def getActivateTitle(self, baseData):
        name = ''
        activeTitleType = baseData.get(const.PERSONAL_ZONE_DATA_ACTIVE_TITLE, 0)
        currTitle = baseData.get(const.PERSONAL_ZONE_DATA_CURR_TITLE, []) if baseData.get(const.PERSONAL_ZONE_DATA_CURR_TITLE, []) else self.baseInfo.get('curTitle', [])
        if not activeTitleType or not currTitle:
            return name
        if activeTitleType == const.ACTIVE_TITLE_TYPE_COMMON:
            if const.TITLE_TYPE_WORLD < len(currTitle):
                prefixName = self.getTitleName(TD.data.get(currTitle[const.TITLE_TYPE_PREFIX], {}), baseData)
                colorName = self.getTitleName(TD.data.get(currTitle[const.TITLE_TYPE_COLOR], {}), baseData)
                basicName = self.getTitleName(TD.data.get(currTitle[const.TITLE_TYPE_BASIC], {}), baseData)
                name = prefixName + colorName + basicName
        elif activeTitleType == const.ACTIVE_TITLE_TYPE_WORLD:
            if const.TITLE_TYPE_WORLD < len(currTitle):
                titleData = TD.data.get(currTitle[const.TITLE_TYPE_WORLD], {})
                if titleData:
                    name = self.getTitleName(titleData, baseData)
        return name

    def getTitleName(self, tData, baseData):
        name = ''
        if tData:
            if tData.get('gId', 0) == gametypes.FAME_GROUP_GUILD:
                name = tData.get('name', '') % baseData[const.PERSONAL_ZONE_DATA_GUILD_NAME]
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_MENTOR:
                pass
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_APPRENTICE:
                pass
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_INTIMACY:
                tgtRoleName = baseData[const.PERSONAL_ZONE_DATA_INTIMACY_TGT_NAME]
                name = tData.get('name', '%s') % tgtRoleName
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_SOLE_MENTOR:
                pass
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_SOLE_APPRENTICE:
                pass
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_ENGAGE:
                _sex = self.baseInfo.get('sexType', 0)
                tgtRoleName = baseData.get(const.PERSONAL_ZONE_DATA_INTIMACY_TGT_NAME, '')
                if _sex == const.SEX_MALE:
                    name = tData.get('name', '%s %s') % (tgtRoleName, gametypes.ENGAGE_HASBAND_DESC)
                elif _sex == const.SEX_FEMALE:
                    name = tData.get('name', '%s %s') % (tgtRoleName, gametypes.ENGAGE_WIFE_DESC)
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_MARRIAGE:
                _sex = self.baseInfo.get('sexType', 0)
                tgtRoleName = baseData.get(const.PERSONAL_ZONE_DATA_INTIMACY_TGT_NAME, '')
                if _sex == const.SEX_MALE:
                    name = tData.get('name', '%s %s') % (tgtRoleName, gametypes.MARRIAGE_HASBAND_DESC)
                elif _sex == const.SEX_FEMALE:
                    name = tData.get('name', '%s %s') % (tgtRoleName, gametypes.MARRIAGE_WIFE_DESC)
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_FIGHT_FOR_LOVE:
                p = BigWorld.player()
                currTitle = baseData.get(const.PERSONAL_ZONE_DATA_CURR_TITLE, []) if baseData.get(const.PERSONAL_ZONE_DATA_CURR_TITLE, []) else self.baseInfo.get('curTitle', [])
                titleId = currTitle[const.TITLE_TYPE_WORLD]
                titleInfo = p.fightForLoveTitleInfo.get(titleId, (0, '', 0))
                name = tData.get('name', '%s') % (titleInfo[1],)
            else:
                name = tData.get('name', '')
        return name

    def onFetchMsgList(self, *arg):
        msgArray = self.baseInfo.get('msgArray', [])
        if msgArray and self.ownerGbID:
            p = BigWorld.player()
            p.base.fetchZoneMsg(self.ownerGbID, msgArray[0][0])

    def fetchZoneMsgCallback(self, ownerGbId, data):
        if self.ownerGbID == ownerGbId and data:
            msgArray = self.baseInfo.get('msgArray', [])
            if msgArray and data[-1][0] < msgArray[0][0]:
                msgArray = data + msgArray
            self.refreshMsgList(msgArray, 0)

    def sendLikeMsg(self):
        if self.ownerGbID and self.isOnline():
            p = BigWorld.player()
            desc = '表示了爱意:role'
            roleName = self.baseInfo.get('roleName', '')
            desc = utils.encodeMsgHeader(desc, {gametypes.MSG_ATTR_EGNORE_TALK_FLAG: 1})
            p.cell.chatToOne(roleName, desc)
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SINGLE, desc, roleName, False, True)

    def onDownloadSelfProfilePhoto(self, status, callbackArgs):
        p = BigWorld.player()
        p.cell.updateProfileIconStatus(status)
        p.profileIconStatus = status

    def onClickDetailItem(self, *arg):
        titleName = arg[3][0].GetString()
        roleName = self.baseInfo.get(titleName, '')
        if roleName:
            self.openZoneOther('', roleName, const.PERSONAL_ZONE_SRC_OTHER_ZONE, self.getHostId())

    def freshTagsAddOne(self, src, new):
        if self.mediator:
            for key in new:
                if src.get(key, ()) and new[key][0] > src.get(key, ())[0]:
                    self.mediator.Invoke('tagTipsAddOne')

    def onClickAddress(self, *args):
        _gbid = '#' + str(self.ownerGbID)
        uiUtils.gotoTrack(_gbid)

    def onClickVoiceItem(self, *args):
        self.voiceMc = args[3][0]
        key = args[3][1].GetString()
        player = BigWorld.player()
        player.downloadAudioFile(const.AUDIOS_DOWNLOAD_RELATIVE_DIR, key, gametypes.NOS_FILE_MP3, gameglobal.rds.ui.afterVoiceDownloaded, (self.voiceMc, key))

    def onOpenPrettyGirlFunc(self, *args):
        enabled = self.baseInfo.get('missTianyu', False) and utils.getNow() < gameglobal.rds.configData.get('missTianyuEndtime', 0) and gameglobal.rds.configData.get('enableMissTianyu', False)
        if enabled:
            p = BigWorld.player()
            ziXunUrl = SCD.data.get('ZiXunUrl', [])
            ziXunIdx = -1
            if 'personalZone' in ziXunUrl:
                ziXunIdx = ziXunUrl.index('personalZone')
                if ziXunIdx != -1:
                    personalZone = {'gbId': self.ownerGbID}
                    self.uiAdapter.ziXunInfo.show(ziXunIdx, personalZone)

    def onGetSkin(self, *args):
        skinId = 0
        if gameglobal.rds.configData.get('enablePersonalZoneSkin', False):
            p = BigWorld.player()
            skinId = self.baseInfo.get('skinId', 1)
        if not skinId:
            skinId = 1
        return GfxValue(gbk2unicode('skin' + str(skinId)))

    def isOpen(self):
        if self.mediator:
            return True
        return False

    def isApplyGroupMT(self):
        p = BigWorld.player()
        isMissTianyuClosed = p.missTianyuState == gametypes.MISS_TIANYU_CLOSE
        return self.baseInfo.get('applyGroupMT', False) == PZCD.data.get('mtSeason', 0) and not isMissTianyuClosed
