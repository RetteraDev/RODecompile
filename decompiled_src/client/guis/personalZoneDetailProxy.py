#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/personalZoneDetailProxy.o
import random
import copy
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
import utils
import gametypes
import const
import formula
from uiProxy import UIProxy
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

class PersonalZoneDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PersonalZoneDetailProxy, self).__init__(uiAdapter)
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
        self.widget = None
        self.replyMsgMed = None
        self.reset()

    @property
    def baseInfo(self):
        return self.uiAdapter.personalZoneSystem.baseInfo

    @baseInfo.setter
    def baseInfo(self, value):
        self.uiAdapter.personalZoneSystem.baseInfo = value

    @property
    def persentInfo(self):
        return self.uiAdapter.personalZoneSystem.persentInfo

    @persentInfo.setter
    def persentInfo(self, value):
        self.uiAdapter.personalZoneSystem.persentInfo = value

    @property
    def detailInfo(self):
        return self.uiAdapter.personalZoneSystem.detailInfo

    @detailInfo.setter
    def detailInfo(self, value):
        self.uiAdapter.personalZoneSystem.detailInfo = value

    @property
    def replyGbId(self):
        return self.uiAdapter.personalZoneSystem.replyGbId

    @replyGbId.setter
    def replyGbId(self, value):
        self.uiAdapter.personalZoneSystem.replyGbId = value

    @property
    def replyDbId(self):
        return self.uiAdapter.personalZoneSystem.replyDbId

    @replyDbId.setter
    def replyDbId(self, value):
        self.uiAdapter.personalZoneSystem.replyDbId = value

    @property
    def replyName(self):
        return self.uiAdapter.personalZoneSystem.replyName

    @replyName.setter
    def replyName(self, value):
        self.uiAdapter.personalZoneSystem.replyName = value

    @property
    def ownerGbID(self):
        return self.uiAdapter.personalZoneSystem.ownerGbID

    @ownerGbID.setter
    def ownerGbID(self, value):
        self.uiAdapter.personalZoneSystem.ownerGbID = value

    @property
    def friendSrcId(self):
        return self.uiAdapter.personalZoneSystem.friendSrcId

    @friendSrcId.setter
    def friendSrcId(self, value):
        self.uiAdapter.personalZoneSystem.friendSrcId = value

    @property
    def hostId(self):
        return self.uiAdapter.personalZoneSystem.hostId

    @hostId.setter
    def hostId(self, value):
        self.uiAdapter.personalZoneSystem.hostId = value

    @property
    def spaceType(self):
        return self.uiAdapter.personalZoneSystem.spaceType

    @hostId.setter
    def spaceType(self, value):
        self.uiAdapter.personalZoneSystem.spaceType = value

    def reset(self):
        self.waitOpenGiftBox = False
        self.voiceMc = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ZONE_MSG_REPLY:
            self.replyMsgMed = mediator
        if hasattr(self, 'autoOpenChat'):
            if self.autoOpenChat:
                self.openChatWnd()
            self.autoOpenChat = False

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        self.widget.initPanel()
        if self.uiAdapter.personalZoneSystem.currentTabIndex == uiConst.PERSONAL_ZONE_TAB_MESSAGE_IDX:
            self.widget.mainMc.messageView.visible = True
            self.widget.mainMc.moreDetailView.visible = False
        elif self.uiAdapter.personalZoneSystem.currentTabIndex == uiConst.PERSONAL_ZONE_TAB_DETIAL_IDX:
            self.widget.mainMc.messageView.visible = False
            self.widget.mainMc.moreDetailView.visible = True

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
        else:
            fVal = p.friend.get(self.ownerGbID, None)
            if fVal and hasattr(fVal, 'acknowledge'):
                return fVal.acknowledge
            return False

    def onSendSignature(self, *arg):
        msg = unicode2gbk(arg[3][0].GetString())
        self.uiAdapter.personalZoneSystem.sendSignature(msg)

    def onOpenSetting(self, *arg):
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_PERSONAL)

    def onShareZone(self, *arg):
        self.uiAdapter.personalZoneSystem.shareZone()

    def onShareHome(self, *arg):
        self.uiAdapter.personalZoneSystem.shareHome()

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
        tmpText = self.uiAdapter.personalZoneSystem.getLabelTips(tagId)
        return GfxValue(gbk2unicode(tmpText))

    def onLikePerson(self, *arg):
        if self.isCrossServer(True):
            return
        if self.ownerGbID:
            p = BigWorld.player()
            p.base.likePersonalZone(self.ownerGbID)

    def onLikePersonTag(self, *arg):
        tagId = int(arg[3][0].GetNumber())
        self.uiAdapter.personalZoneSystem.likePersonTag(tagId)

    def isCrossServer(self, showMsg = False):
        self.uiAdapter.personalZoneSystem.isCrossServer(showMsg)

    def getHostId(self):
        if self.hostId:
            return self.hostId
        return int(gameglobal.rds.gServerid)

    def onAddFriend(self, *arg):
        self.uiAdapter.personalZoneSystem.addFriend()

    def onTalk2Me(self, *arg):
        self.uiAdapter.personalZoneSystem.talk2Me()

    def onGetZodiac(self, *arg):
        month = int(arg[3][0].GetNumber()) + 1
        day = int(arg[3][1].GetNumber()) + 1
        if month <= 0 or day <= 0:
            return GfxValue(gbk2unicode(''))
        n = gameStrings.PERSONAL_ZONE_ZODIAC
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
        return self.uiAdapter.personalZoneSystem._createFriendData()

    def onGetSpaceInfo(self, *arg):
        tempData = self.getSpaceaBaseInfo(True)
        return tempData

    def onSetBirthInfo(self, *arg):
        value = unicode2gbk(arg[3][0].GetString())
        _type = int(arg[3][1].GetNumber())
        self.uiAdapter.personalZoneSystem.setBirthInfo(value, _type)

    def onGetDetailInfo(self, *arg):
        if self.ownerGbID:
            p = BigWorld.player()
            p.base.getPersonalZoneInfo(self.ownerGbID, self.hostId)

    def onGetFuDaiTips(self, *arg):
        tmpText = self.uiAdapter.personalZoneSystem.getFuDaiTips()
        return GfxValue(gbk2unicode(tmpText))

    def onCallLabelSetting(self, *arg):
        tags = self.baseInfo.get('tags', {})
        self.uiAdapter.personalZoneSystem.callLabelSetting(tags)

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
        tempData = self.uiAdapter.personalZoneSystem.getProvinceCity()
        return uiUtils.dict2GfxDict(tempData, True)

    def getSpaceaBaseInfo(self, bGfx = False):
        msgArray = self.baseInfo.get('msgArray', [])
        newMsgNum = self.baseInfo.get('newMsgNum', 0)
        _msgArray = self.getGfxMsgArray(msgArray, newMsgNum, bGfx)
        if bGfx:
            ret = uiUtils.dict2GfxDict(self.baseInfo, True)
            ret.SetMember('msgArray', _msgArray)
            return ret
        else:
            ret = copy.deepcopy(self.baseInfo)
            ret['msgArray'] = _msgArray
            return ret

    def getValue(self, key):
        if key == '':
            return uiUtils.array2GfxAarry([], True)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PERSONAL_SPACE)

    def clearWidget(self):
        if self.replyMsgMed:
            self.onCloseReplyMsg()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PERSONAL_SPACE)

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
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.PERSONAL_ZONE_DELETE_MSG, Functor(self.realDelZoneMsg, gbId, dbId))

    def realDelZoneMsg(self, gbId, dbId):
        p = BigWorld.player()
        p.base.delZoneMsg(self.ownerGbID, dbId)

    def getGfxMsgArray(self, msgArray, newMsgNum, bGfx = False):
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
                try:
                    borderId = int(borderId)
                except:
                    borderId = 0

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
                    item['nameTxt'] = gameStrings.PERSONAL_ZONE_REPLY_MSG % (mName, replyName)
                else:
                    item['nameTxt'] = mName
                ret.append(item)

            ret.reverse()
        if len(ret) < MSG_LIST_ITEM_NUM:
            for n in xrange(len(ret), MSG_LIST_ITEM_NUM):
                item = {'isShow': 0}
                ret.append(item)

        if bGfx:
            return uiUtils.array2GfxAarry(ret, True)
        else:
            return ret

    def onGetReplyMsgInfo(self, *arg):
        ret = {'replyName': self.replyName,
         'msgMaxNum': MSG_MAX_NUM}
        return uiUtils.dict2GfxDict(ret, True)

    def onCommitReplyMsg(self, *arg):
        p = BigWorld.player()
        if p.zoneMsgPermission == 1:
            if not self.isFriend() and self.spaceType == VISIT_TYPE_OTHER:
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
        self.uiAdapter.personalZoneSystem.onOpenZone(ownerGbId, data, hostId)

    def isOnline(self):
        return self.baseInfo.get('isOnline', 0)

    def updatePhotoBorderInfo(self, ownerGbId, data):
        p = BigWorld.player()
        self.baseInfo['photoBorderIcon'] = p.getPhotoBorderIcon(data.get(const.PERSONAL_ZONE_PHOTO_BORDER, 0), uiConst.PHOTO_BORDER_ICON_SIZE156)
        if self.widget:
            self.widget.updatePhotoBorderInfo(self.baseInfo['photoBorderIcon'])
        self.uiAdapter.personalZoneSystem.updatePhotoBorderInfo()

    def updateHeadInfo(self, ownerGbId, data):
        self.baseInfo['customPhoto'] = data.get(const.PERSONAL_ZONE_DATA_CUSTOM_PHOTO, self.baseInfo.get('customPhoto', ''))
        self.baseInfo['sysPhoto'] = data.get(const.PERSONAL_ZONE_DATA_SYS_PHOTO, self.baseInfo.get('sysPhoto', ''))
        self.baseInfo['curPhoto'] = data.get(const.PERSONAL_ZONE_DATA_CURR_PHOTO, self.baseInfo.get('curPhoto', ''))
        _photo = self.baseInfo['curPhoto']
        _school = self.baseInfo['_school']
        _sex = self.baseInfo['_sex']
        p = BigWorld.player()
        if self.spaceType == VISIT_TYPE_SELF and p.profileIconStatus == gametypes.NOS_FILE_STATUS_PENDING and p.profileIconUsed == False and p.iconUpload == True and p.imageName:
            _photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + p.imageName + utils.getProfileIconSuffix()
        self.baseInfo['photo'] = _photo if _photo else DEFAULTPHOTO % str(_school * 10 + _sex)
        if not self.baseInfo['customPhoto'] or p.profileIconStatus != gametypes.NOS_FILE_STATUS_APPROVED:
            self.baseInfo['customPhoto'] = self.baseInfo['photo']
        gamelog.debug('photo', self.baseInfo['photo'])
        if p.zoneHeadIconPermission == 1:
            if not self.isFriend() and self.spaceType == VISIT_TYPE_OTHER:
                self.baseInfo['photo'] = DEFAULTPHOTO % str(_school * 10 + _sex)
        if self.widget:
            self.widget.updateHeadInfo(self.baseInfo['photo'])
        self.uiAdapter.personalZoneSystem.updatePhotoInfo()

    def onCalcPersent(self, *arg):
        curNum = 0
        for key in self.persentInfo:
            if self.persentInfo[key]:
                curNum += 1

        persentNum = int(float(curNum) / float(len(self.persentInfo)) * 100)
        return GfxValue(persentNum)

    def onQueryPersonalZoneInfo(self, ownerGbId, data):
        self.uiAdapter.personalZoneSystem.onQueryPersonalZoneInfo(ownerGbId, data)

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
        if self.widget:
            self.widget.setDetailInfo(self.detailInfo)

    def getFuDaiNumber(self):
        return self.uiAdapter.personalZoneSystem.getFuDaiNumber()

    def onGetFuDaiBtnShow(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableFuDaiProxy', False))

    def onUpdateInfo(self, ownerGbId, op, data):
        self.uiAdapter.personalZoneSystem.onUpdateInfo(ownerGbId, op, data)

    def setUpdateInfo(self, needAdjustTag = False):
        if self.widget:
            tempData = self.getSpaceaBaseInfo()
            self.widget.updateBaseInfo(tempData, needAdjustTag)
            self.widget.setFuDaiIcon()

    def onGetZoneGiftData(self, ownerGbId, data):
        self.baseInfo['giftDict'] = data.get(const.PERSONAL_ZONE_DATA_GIFT_DICT, {})
        self.baseInfo['weekGiftNum'] = data.get(const.PERSONAL_ZONE_DATA_GIFT_WEEK_NUM, 0)
        self.baseInfo['giftTop'] = data.get(const.PERSONAL_ZONE_DATA_GIFT_TOP, {})
        num = 0
        for key in self.baseInfo['giftDict']:
            num += self.baseInfo['giftDict'][key]

        self.baseInfo['giftNum'] = num
        if self.waitOpenGiftBox:
            gameglobal.rds.ui.spaceGiftBox.show(self.ownerGbID, self.baseInfo.get('roleName', ''), data, num, self.spaceType, self.hostId)
            self.waitOpenGiftBox = False
        tempData = self.getSpaceaBaseInfo()
        if self.widget:
            self.widget.updateBaseInfo(tempData, False)

    def refreshMsgList(self, data, newMsgNum = 0):
        data = self.getGfxMsgArray(data, newMsgNum)
        if self.widget:
            self.widget.refreshMsgList(data)

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
        self.uiAdapter.personalZoneSystem.openZoneOther(ownerGbID, roleName, srcId, hostId, autoOpenChat)

    def onEditRoleFigure(self, *arg):
        self.uiAdapter.personalZoneSystem.onEditRoleFigure()

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
            desc = gameStrings.PERSONAL_ZONE_LIKE_MSG
            roleName = self.baseInfo.get('roleName', '')
            desc = utils.encodeMsgHeader(desc, {gametypes.MSG_ATTR_EGNORE_TALK_FLAG: 1})
            p.cell.chatToOne(roleName, desc)
            gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SINGLE, desc, roleName, False, True)

    def onClickDetailItem(self, *arg):
        titleName = arg[3][0].GetString()
        roleName = self.baseInfo.get(titleName, '')
        if roleName:
            self.openZoneOther('', roleName, const.PERSONAL_ZONE_SRC_OTHER_ZONE, self.getHostId())

    def freshTagsAddOne(self, src, new):
        if self.widget:
            for key in new:
                if src.get(key, ()) and new[key][0] > src.get(key, ())[0]:
                    self.widget.tagTipsAddOne()

    def onClickAddress(self, *args):
        _gbid = '#' + str(self.ownerGbID)
        uiUtils.gotoTrack(_gbid)

    def onClickVoiceItem(self, *args):
        self.voiceMc = args[3][0]
        key = args[3][1].GetString()
        player = BigWorld.player()
        player.downloadAudioFile(const.AUDIOS_DOWNLOAD_RELATIVE_DIR, key, gametypes.NOS_FILE_MP3, gameglobal.rds.ui.afterVoiceDownloaded, (self.voiceMc, key))

    def onOpenPrettyGirlFunc(self, *args):
        self.uiAdapter.personalZoneSystem.openPrettyGirlFunc()

    def onGetSkin(self, *args):
        skinId = 0
        if gameglobal.rds.configData.get('enablePersonalZoneSkin', False):
            p = BigWorld.player()
            skinId = self.baseInfo.get('skinId', 1)
        if not skinId:
            skinId = 1
        return GfxValue(gbk2unicode('skin' + str(skinId)))

    def setFuDaiIcon(self):
        if not self.hasBaseData():
            return
        self.widget.setFuDaiIcon()

    def isOpen(self):
        return self.uiAdapter.personalZoneSystem.isOpen()

    def hide(self):
        self.uiAdapter.personalZoneSystem.hide()

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def syncPYQBonusData(self, pyqBonus):
        self.uiAdapter.personalZoneSystem.syncPYQBonusData(pyqBonus)
