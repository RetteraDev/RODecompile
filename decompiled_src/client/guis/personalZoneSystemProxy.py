#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/personalZoneSystemProxy.o
from gamestrings import gameStrings
import random
import re
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
import utils
import gametypes
import const
import formula
import events
import gameconfigCommon
from uiTabProxy import UITabProxy
from guis import uiConst
from guis import uiUtils
from guis import ui
from asObject import TipManager
from asObject import Tweener
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.ui import unicode2gbk
from guis.ui import gbk2unicode
from guis import richTextUtils
from helpers import taboo
from helpers import pyq_interface
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
from data import pyq_bonus_data as PBDD
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
BIRTH_NO_EDITING = 0
BIRTH_EDITING = 1
SHARE_LEFT_POS = -344
SHARE_MID_POS = -293

class PersonalZoneSystemProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(PersonalZoneSystemProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PERSONAL_ZONE_SYSTEM, self.hide)

    def reset(self):
        super(PersonalZoneSystemProxy, self).reset()
        self.serverInfo = {}
        self.baseInfo = {}
        self.persentInfo = {}
        self.detailInfo = {}
        self.spaceType = 0
        self.replyGbId = 0
        self.replyDbId = 0
        self.replyName = None
        self.ownerGbID = 0
        self.friendSrcId = const.FRIEND_SRC_PERSONAL_ZONE
        self.hostId = 0
        self.cityEditState = BIRTH_NO_EDITING
        self.birthdEditState = BIRTH_NO_EDITING
        self.cityDict = self.getProvinceCity()
        self.selbirdayMonth = -1
        self.selbirdayDay = -1
        self.selProvince = -1
        self.selCity = -1
        self.isFollowing = -1
        self.fansNum = -1
        self.shareBtnSub = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PERSONAL_ZONE_SYSTEM:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(PersonalZoneSystemProxy, self).clearWidget()
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PERSONAL_ZONE_SYSTEM)

    def _getTabList(self):
        return [{'tabIdx': uiConst.PERSONAL_ZONE_TAB_FIENDS_IDX,
          'tabName': 'friendBtn',
          'view': 'PersonalZoneFriendWidget',
          'proxy': 'personalZoneFriend',
          'pos': (125, 0)}, {'tabIdx': uiConst.PERSONAL_ZONE_TAB_MESSAGE_IDX,
          'tabName': 'messageTabBtn',
          'view': 'PersonalZoneDetailWidget',
          'proxy': 'personalZoneDetail',
          'pos': (125, 0)}, {'tabIdx': uiConst.PERSONAL_ZONE_TAB_DETIAL_IDX,
          'tabName': 'moreDetailTabBtn',
          'view': 'PersonalZoneDetailWidget',
          'proxy': 'personalZoneDetail',
          'pos': (125, 0)}]

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_PERSONAL_ZONE_SYSTEM)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.getProfile(self.ownerGbID)
        skinId = self.getSkin()
        self.widget.gotoAndPlay(skinId)
        ASUtils.setHitTestDisable(self.widget.bgMc, True)
        self.widget.titleNameMc.titleName.text = gameStrings.PERSONAL_ZONE_TITLE % (self.baseInfo.get('relativeTitle', ''),)
        ASUtils.setHitTestDisable(self.widget.titleNameMc, True)
        self.widget.reportBtn.addEventListener(events.MOUSE_CLICK, self.onReportBtnClick, False, 0, True)
        self.widget.spaceSettingBtn.addEventListener(events.BUTTON_CLICK, self.onSpaceSettingBtnClick, False, 0, True)
        self.initTabUI()
        p = BigWorld.player()
        pyqOpenLv = PZCD.data.get('pyqOpenLv', 0)
        enablePYQ = self.baseInfo.get('enablePYQ', 0) and gameconfigCommon.enablePYQ() and p.lv >= pyqOpenLv and self.baseInfo.get('lv', 0) >= pyqOpenLv
        if not enablePYQ:
            self.setTabVisible(uiConst.PERSONAL_ZONE_TAB_FIENDS_IDX, False, True)
        if self.showTabIndex == -1:
            if enablePYQ:
                self.widget.setTabIndex(uiConst.PERSONAL_ZONE_TAB_FIENDS_IDX)
            else:
                self.widget.setTabIndex(uiConst.PERSONAL_ZONE_TAB_MESSAGE_IDX)

    def refreshInfo(self):
        if not self.widget:
            return
        if self.spaceType == VISIT_TYPE_SELF:
            self.widget.reportBtn.visible = False
            self.widget.spaceSettingBtn.visible = True
        elif self.spaceType == VISIT_TYPE_OTHER:
            self.widget.reportBtn.visible = True
            self.widget.spaceSettingBtn.visible = False
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    def onTabChanged(self, *args):
        self.cityEditState = BIRTH_NO_EDITING
        self.birthdEditState = BIRTH_NO_EDITING
        self.selbirdayMonth = -1
        self.selbirdayDay = -1
        self.selProvince = -1
        self.selCity = -1
        super(PersonalZoneSystemProxy, self).onTabChanged(*args)
        self.refreshInfo()

    def onReportBtnClick(self, *arg):
        srcId = uiConst.MENU_CHAT
        gameglobal.rds.ui.prosecute.show(self.baseInfo.get('roleName', ''), srcId)

    def onSpaceSettingBtnClick(self, *arg):
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_PERSONAL)

    def onOpenZone(self, ownerGbId, data, hostId = 0):
        p = BigWorld.player()
        if p._isSoul():
            if p.gbId == ownerGbId:
                p.showGameMsg(GMDD.data.FORBIDDEN_ON_CROSS, ())
                return
        self.serverInfo.update(data)
        self._onOpenZone(ownerGbId, data, hostId)

    def _onOpenZone(self, ownerGbId, data, hostId = 0):
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
            self.spaceType = VISIT_TYPE_SELF
        else:
            self.spaceType = VISIT_TYPE_OTHER
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
        self.baseInfo['roleName'] = data[const.PERSONAL_ZONE_DATA_NAME]
        self.baseInfo['hostId'] = self.hostId
        _school = data[const.PERSONAL_ZONE_DATA_SCHOOL]
        self.baseInfo['_school'] = data[const.PERSONAL_ZONE_DATA_SCHOOL]
        self.baseInfo['schoolName'] = const.SCHOOL_DICT[_school]
        self.baseInfo['schoolState'] = uiConst.SCHOOL_FRAME_DESC[_school]
        self.baseInfo['lv'] = data[const.PERSONAL_ZONE_DATA_LV]
        self.baseInfo['_sex'] = data[const.PERSONAL_ZONE_DATA_SEX]
        self.baseInfo['enablePYQ'] = data.get(const.PERSONAL_ZONE_DATA_PYQ, {}).get('isOpen', False)
        self.baseInfo['applyGroupMT'] = data.get(const.PERSONAL_ZONE_DATA_PYQ, {}).get('applyGroupMT', None)
        self.baseInfo['fansTitleNameMT'] = data.get(const.PERSONAL_ZONE_DATA_PYQ, {}).get('fansTitleNameMT', '')
        self.baseInfo['aidTeamName'] = data.get(const.PERSONAL_ZONE_DATA_AID_TITLE_ARGS, tuple())
        self.baseInfo['fans'] = data.get(const.PERSONAL_ZONE_DATA_FANS, 0)
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
            self.baseInfo['relativeTitle'] = gameStrings.PERSONAL_ZONE_ME
        elif _sex == const.SEX_MALE:
            self.baseInfo['relativeTitle'] = gameStrings.PERSONAL_ZONE_HE
        elif _sex == const.SEX_FEMALE:
            self.baseInfo['relativeTitle'] = gameStrings.PERSONAL_ZONE_SHE
        else:
            self.baseInfo['relativeTitle'] = gameStrings.PERSONAL_ZONE_HE
        self.baseInfo['spaceType'] = self.spaceType
        self.baseInfo['signature'] = data.get(const.PERSONAL_ZONE_DATA_SIGNATURE, 0)
        self.baseInfo['likeNum'] = data.get(const.PERSONAL_ZONE_DATA_LIKE_NUM, 0)
        self.baseInfo['touchNum'] = data.get(const.PERSONAL_ZONE_DATA_TOUCH_NUM, 0)
        self.baseInfo['msgArray'] = data.get(const.PERSONAL_ZONE_DATA_MSG, [])
        self.baseInfo['popularity'] = data.get(const.PERSONAL_ZONE_DATA_POPULARITY, 0)
        self.baseInfo['hotLv'] = self.getHotLv(self.baseInfo.get('popularity', 0))
        self.baseInfo['intimacy'] = data.get(const.PERSONAL_ZONE_DATA_INTIMACY, 0)
        self.baseInfo['birthday'] = data.get(const.PERSONAL_ZONE_DATA_BIRTHDAY, '')
        self.baseInfo['city'] = data.get(const.PERSONAL_ZONE_DATA_CITY, '')
        self.baseInfo['tags'] = data.get(const.PERSONAL_ZONE_DATA_TAGS, 0)
        self.baseInfo['tagsFormat'] = self.getTagsInfo(self.baseInfo.get('tags', 0))
        self.baseInfo['curTitle'] = data.get(const.PERSONAL_ZONE_DATA_CURR_TITLE, [0,
         0,
         0,
         0])
        self.baseInfo['isOnline'] = data.get(const.PERSONAL_ZONE_DATA_ONLINE, False)
        self.baseInfo['customPhotoNos'] = data.get(const.PERSONAL_ZONE_DATA_CUSTOM_PHOTO, '')
        self.baseInfo['customPhoto'] = data.get(const.PERSONAL_ZONE_DATA_CUSTOM_PHOTO, '')
        self.baseInfo['sysPhoto'] = data.get(const.PERSONAL_ZONE_DATA_SYS_PHOTO, '')
        self.baseInfo['curPhoto'] = data.get(const.PERSONAL_ZONE_DATA_CURR_PHOTO, '')
        self.baseInfo['mentorName'] = self.calcMentorName(data.get(const.PERSONAL_ZONE_DATA_MENTOR_NAME, []))
        _audiokey = data.get(const.PERSONAL_ZONE_DATA_AUDIO_KEY, '')
        self.baseInfo['audioKey'] = _audiokey if _audiokey != '0' and gameglobal.rds.configData.get('enablePersonalZoneVoice', False) else ''
        self.baseInfo['audioTip'] = gameStrings.PERSONAL_ZONE_AUDIO_TIP
        self.baseInfo['floorNo'] = data.get(const.PERSONAL_ZONE_DATA_ROOM_FLOOR_NO, 0)
        self.baseInfo['roomNo'] = data.get(const.PERSONAL_ZONE_DATA_ROOM_NO, 0)
        self.baseInfo['roomWealth'] = data.get(const.PERSONAL_ZONE_DATA_ROOM_WEALTH, 0)
        self.baseInfo['roomColor'] = uiConst.ROOM_NO_COLOR.get(self.baseInfo.get('roomNo', 0), '')
        self.baseInfo['topic'] = data.get(const.PERSONAL_ZONE_DATA_PYQ_BONUS, {})
        _roomWealthLv = gameglobal.rds.ui.homeCheckHouses.getWealthLv(self.baseInfo.get('roomWealth', 0))
        roomWealthLvMaxVal = gameglobal.rds.ui.homeCheckHouses.getWealthLvMaxVal(self.baseInfo.get('roomWealth', 0))
        finalDesc = '0' if not self.baseInfo.get('roomNo', 0) else '%s(%d/%d)' % (_roomWealthLv, self.baseInfo.get('roomWealth', 0), roomWealthLvMaxVal)
        self.baseInfo['roomWealthLv'] = _roomWealthLv
        self.baseInfo['wealthDesc'] = finalDesc
        self.calcHomeStr()
        _photo = self.baseInfo['curPhoto']
        if self.spaceType == VISIT_TYPE_SELF and p.profileIconStatus == gametypes.NOS_FILE_STATUS_PENDING and p.profileIconUsed == False and p.iconUpload == True and p.imageName:
            _photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + p.imageName + utils.getProfileIconSuffix()
        self.baseInfo['photo'] = _photo if _photo else DEFAULTPHOTO % str(_school * 10 + _sex)
        if not self.baseInfo['customPhoto'] or p.profileIconStatus != gametypes.NOS_FILE_STATUS_APPROVED:
            self.baseInfo['customPhoto'] = self.baseInfo['photo']
        gamelog.debug('photo', self.baseInfo['photo'])
        if p.zoneHeadIconPermission == 1:
            if not self.isFriend() and self.spaceType == VISIT_TYPE_OTHER:
                self.baseInfo['photo'] = DEFAULTPHOTO % str(_school * 10 + _sex)
        self.baseInfo['newLikeNum'] = data[const.PERSONAL_ZONE_DATA_NEW_LIKE_NUM]
        self.baseInfo['newMsgNum'] = data[const.PERSONAL_ZONE_DATA_NEW_MSG_NUM]
        self.baseInfo['weekPopularity'] = data[const.PERSONAL_ZONE_DATA_WEEK_POPULARITY]
        self.baseInfo['giftNum'] = data[const.PERSONAL_ZONE_DATA_GIFT_NUM]
        self.baseInfo['missTianyu'] = data.get(const.PERSONAL_ZONE_DATA_MISSTIANYU, False) and utils.getNow() < gameglobal.rds.configData.get('missTianyuEndtime', 0) and gameglobal.rds.configData.get('enableMissTianyu', False)
        self.baseInfo['skinId'] = data.get(const.PERSONAL_ZONE_DATA_SKIN, 1)
        self.baseInfo['photoBorderIcon'] = p.getPhotoBorderIcon(data.get(const.PERSONAL_ZONE_PHOTO_BORDER, 0), uiConst.PHOTO_BORDER_ICON_SIZE156)
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

    def onQueryPersonalZoneInfo(self, ownerGbId, data):
        p = BigWorld.player()
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
        if p.ckBoxHideMyJieqi == 1:
            self.detailInfo['intimacyTgtName'] = ''
        self.persentInfo['birthday'] = True if self.baseInfo.get('birthday', '') else False
        self.persentInfo['city'] = True if self.baseInfo.get('city', '') else False
        self.baseInfo['intimacyTgtName'] = self.detailInfo['intimacyTgtName']
        self.setDetailInfo()
        self.setFuDaiIcon()
        p.cell.queryPartnerMemberInfo(ownerGbId)

    def onUpdateInfo(self, ownerGbId, op, data):
        self.baseInfo['msgArray'] = data.get(const.PERSONAL_ZONE_DATA_MSG, self.baseInfo.get('msgArray', []))
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
        needAdjustTag = op == const.PERSONAL_ZONE_OP_ALTER_TAGS and self.spaceType == VISIT_TYPE_SELF
        self.calcHomeStr()
        curProxy = self.getCurrentProxy()
        if hasattr(curProxy, 'setUpdateInfo'):
            curProxy.setUpdateInfo(needAdjustTag=needAdjustTag)

    def setDetailInfo(self):
        if not self.hasBaseData():
            return
        self.uiAdapter.personalZoneDetail.setDetailInfo()

    def freshTagsAddOne(self, src, new):
        curProxy = self.getCurrentProxy()
        if hasattr(curProxy, 'freshTagsAddOne'):
            curProxy.freshTagsAddOne(src, new)
        self.tagTipsAddOne(src, new)

    def tagTipsAddOne(self, src, new):
        mainMc = self.getMainMc()
        if mainMc:
            for key in new:
                if src.get(key, ()) and new[key][0] > src.get(key, ())[0]:
                    mainMc.labelLikeAddOneMc.visible = True
                    mainMc.labelLikeAddOneMc.gotoAndPlay('addOne')
                    return

    def onDownloadSelfProfilePhoto(self, status, callbackArgs):
        p = BigWorld.player()
        p.cell.updateProfileIconStatus(status)
        p.profileIconStatus = status

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
            fontsize = int((TAG_SIZE_MAX + TAG_SIZE_MIN) * 0.5)
        else:
            k = (TAG_SIZE_MAX - TAG_SIZE_MIN) * 1.0 / (maxCount - minCount)
        for i, item in enumerate(ret):
            item['size'] = random.randint(0, 4) + fontsize if fontsize else int(k * (item['count'] - minCount) + TAG_SIZE_MIN)
            item['color'] = TAG_COLOR_ARRAY[i]

        ret.sort(lambda x, y: cmp(x['size'], y['size']), reverse=True)
        return ret

    def calcMentorName(self, nameArr):
        if not nameArr:
            return ''
        msg = ''
        for _name in nameArr:
            msg += "<font color= \'#174C66\'><a href = \'event:openZoneByName%s\'><u>%s</u>;</a></font>" % (_name, _name)

        return msg

    def getProvinceCity(self):
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
        return tempData

    def calcHomeStr(self):
        homeStr = gameStrings.PERSONAL_ZONE_NO_HOME
        homeEntry = False
        if self.baseInfo.get('roomNo', 0) and self.baseInfo.get('floorNo', 0):
            homeStr = gameStrings.PERSONAL_ZONE_FLOOR_NO % (self.baseInfo.get('floorNo', 0), self.baseInfo.get('roomColor', ''), self.baseInfo.get('roomWealthLv', ''))
            homeEntry = True
        self.baseInfo['homeStr'] = homeStr
        self.baseInfo['homeEntry'] = homeEntry

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
            elif tData.get('gId', 0) == gametypes.TITLE_GROUP_MISS_TIANYU_FANS:
                name = tData.get('name', '%s') % self.baseInfo['fansTitleNameMT']
            elif tData.get('gId', 0) in gametypes.TITLE_GROUP_AID_TITLE:
                name = tData.get('name', '%s') % self.baseInfo['aidTeamName']
            else:
                name = tData.get('name', '')
        return name

    def getSkin(self):
        skinId = 0
        if gameglobal.rds.configData.get('enablePersonalZoneSkin', False):
            p = BigWorld.player()
            skinId = self.baseInfo.get('skinId', 1)
        if not skinId:
            skinId = 1
        return 'skin' + str(skinId)

    @ui.callFilter(time=2)
    def openZoneOther(self, ownerGbID, roleName = None, srcId = 0, hostId = 0, autoOpenChat = False):
        if self.widget:
            self.hide()
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
            gameglobal.rds.ui.systemTips.show(gameStrings.PERSONAL_ZONE_TEST_MSG)

    def onEditRoleFigure(self, *arg):
        if gameglobal.rds.configData.get('enableNewFigureUpload', False):
            gameglobal.rds.ui.spaceHeadSetting.show(self.baseInfo.get('customPhoto', ''), self.baseInfo.get('sysPhoto', ''), self.baseInfo.get('_school', ''), self.baseInfo.get('_sex', ''), self.baseInfo.get('photo', ''))
        else:
            gameglobal.rds.ui.systemTips.show(gameStrings.PERSONAL_ZONE_HEAD_SETTING_TEST_MSG)

    def sendSignature(self, msg):
        p = BigWorld.player()
        if not msg:
            msg = gameStrings.PERSONAL_ZONE_SIGNATURE_DEFAULT
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

    def initMainMc(self, mc):
        mc.labelLikeAddOneMc.visible = False
        mc.queryRoleBtn.addEventListener(events.BUTTON_CLICK, self.handleClickQueryRole, False, 0, True)
        mc.inputSignature.addEventListener(events.CLIK_EVENT_FOCUS_IN, self.handleInputSignatureIn, False, 0, True)
        mc.inputSignature.addEventListener(events.CLIK_EVENT_FOCUS_OUT, self.handleInputSignatureOut, False, 0, True)
        mc.inputSignature.addEventListener(events.MOUSE_ROLL_OVER, self.handleRollOverSig, False, 0, True)
        mc.inputSignature.addEventListener(events.MOUSE_ROLL_OUT, self.handleRollOutSig, False, 0, True)
        mc.makeFriendBtn.addEventListener(events.BUTTON_CLICK, self.handleClickMakeFriend, False, 0, True)
        mc.shareBtns.shareBtn.addEventListener(events.BUTTON_CLICK, self.handleClickShare, False, 0, True)
        mc.shareBtns.addEventListener(events.MOUSE_ROLL_OVER, self.handleShareBtnRollOver, False, 0, True)
        mc.shareBtns.addEventListener(events.MOUSE_ROLL_OUT, self.handleShaerBtnRollOut, False, 0, True)
        mc.shareBtns.shareBtnSub.shareSpaceBtn.addEventListener(events.BUTTON_CLICK, self.handleClickShare, False, 0, True)
        mc.shareBtns.shareBtnSub.shareHomeBtn.addEventListener(events.BUTTON_CLICK, self.handleClickShareHome, False, 0, True)
        mc.shareBtns.shareBtnSub.visible = False

    def setFuDaiIcon(self):
        if not self.hasBaseData():
            return
        self.uiAdapter.personalZoneDetail.setFuDaiIcon()
        self.uiAdapter.personalZoneFriend.setFuDaiIcon()

    def setPrettyGirlBtn(self):
        if not self.hasBaseData():
            return
        self.uiAdapter.personalZoneFriend.setPrettyGirlBtn()

    def getFuDaiNumber(self):
        if self.baseInfo.get('fuDaiBonusType', 0) > 0:
            return self.baseInfo.get('fuDaiBonusNum', 0)
        return 0

    def getFuDaiTips(self):
        tmpText = ''
        if self.getFuDaiNumber() <= 0:
            tmpText = gameStrings.PERSONAL_ZONE_NO_SET_FUDAI
        else:
            name = PZBD.data.get(self.baseInfo['fuDaiBonusType'], {}).get('name', '')
            tmpText = gameStrings.PERSONAL_ZONE_SET_FUDAI % (name, self.baseInfo['fuDaiBonusNum'])
        return tmpText

    def setMainMc(self, mc):
        if not self.hasBaseData():
            return
        self.setHeadMc(mc)
        self.setMainInfo(mc)
        self.setCityInfo(mc)
        self.setPopularityInfo(mc)
        self.setTagInfo(mc)
        self.setPrettyGirlBtn()

    def setMainInfo(self, mc):
        mc.lvText.text = gameStrings.PERSONAL_ZONE_LV_TXT + str(self.baseInfo.get('lv', 0))
        mc.nameText.text = self.baseInfo.get('roleName', '')
        mc.isOnlineText.text = gameStrings.PERSONAL_ZONE_ONLINE_TXT if self.baseInfo.get('isOnline', 0) else gameStrings.PERSONAL_ZONE_OUTLINE_TXT
        mc.isOnlineText.x = mc.nameText.x + mc.nameText.textWidth
        mc.Sex.gotoAndPlay(self.baseInfo.get('sex', 'man'))
        audioKey = self.baseInfo.get('audioKey', '')
        mc.voiceMc.data = audioKey
        TipManager.addTip(mc.jobMc, self.baseInfo.get('schoolName'))
        mc.jobMc.gotoAndPlay(self.baseInfo.get('schoolState'))
        if self.isSelfZone():
            mc.shareBtns.x = SHARE_MID_POS
            mc.queryRoleBtn.visible = False
            mc.makeFriendBtn.visible = False
            ASUtils.setHitTestDisable(mc.signatureText, True)
            mc.labelEditBtn.visible = True
            mc.inputSignature.visible = True
        else:
            mc.shareBtns.x = SHARE_LEFT_POS
            mc.labelEditBtn.visible = False
            mc.queryRoleBtn.visible = True
            mc.makeFriendBtn.visible = True
            mc.makeFriendBtn.label = gameStrings.PERSONAL_ZONE_TALK_TXT if self.isFriend() else gameStrings.PERSONAL_ZONE_MAKE_FRIEND_TXT
            mc.inputSignature.visible = False
        signatureTxt = self.baseInfo.get('signature', '')
        mc.signatureText.text = signatureTxt if signatureTxt else gameStrings.PERSONAL_ZONE_DEFAULT_SIGNATURE_TXT
        if audioKey:
            mc.voiceMc.voice.enabled = True
        else:
            mc.voiceMc.voice.enabled = False
            mc.voiceMc.voice.mouseEnabled = True
            TipManager.addTip(mc.voiceMc, self.baseInfo.get('audioTip', ''))

    def isFriend(self):
        p = BigWorld.player()
        if p.isGobalFirendGbId(self.ownerGbID):
            return True
        else:
            fVal = p.friend.get(self.ownerGbID, None)
            if fVal and hasattr(fVal, 'acknowledge'):
                return fVal.acknowledge
            return False

    def _createFriendData(self):
        return {'id': str(self.ownerGbID),
         'name': self.baseInfo.get('roleName', ''),
         'photo': self.baseInfo.get('photo', ''),
         'signature': self.baseInfo.get('signature', ''),
         'state': 1,
         'yixinOpenId': 0,
         'photoBorderIcon': self.baseInfo.get('photoBorderIcon', ''),
         'level': self.baseInfo.get('lv', ''),
         'school': self.baseInfo.get('_school', '')}

    def talk2Me(self):
        gameglobal.rds.ui.chatToFriend.show(None, self._createFriendData(), False)

    def addFriend(self):
        group = gametypes.FRIEND_GROUP_FRIEND
        p = BigWorld.player()
        if self.isCrossServer():
            p.base.addRemoteFriendRequest(self.hostId, self.ownerGbID)
        else:
            p.base.addContactByGbId(self.ownerGbID, group, self.friendSrcId)

    def handleClickMakeFriend(self, *arg):
        if self.isFriend():
            self.talk2Me()
        else:
            self.addFriend()

    def handleClickQueryRole(self, *arg):
        if self.baseInfo.get('roleName'):
            p = BigWorld.player()
            p.cell.getEquipment(self.baseInfo['roleName'])

    def handleShareBtnRollOver(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        if not self.hasBaseData():
            return
        t.shareBtnSub.visible = True
        Tweener.removeTweens(t.shareBtnSub)
        t.shareBtnSub.alpha = 1.0

    def handleShaerBtnRollOut(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        if not self.hasBaseData():
            return
        if t:
            Tweener.addTween(t.shareBtnSub, {'time': 1.0,
             'alpha': 0.0,
             'transition': 'linear',
             'onComplete': self.hideShareBtnSub})

    def hideShareBtnSub(self, *arg):
        mainMc = self.getMainMc()
        if mainMc:
            mainMc.shareBtns.shareBtnSub.visible = False

    def handleClickShare(self, *arg):
        self.shareZone()

    def handleClickShareHome(self, *arg):
        self.shareHome()

    def shareZone(self):
        if not self.ownerGbID:
            return
        if not self.baseInfo:
            return
        pyqBonusDict = self.baseInfo.get('topic', {})
        msg = ''
        color = ''
        for topicId, likeNum in pyqBonusDict.iteritems():
            tpData = PBDD.data.get(topicId, {})
            tStart, tEnd = tpData.get('tStart', ''), tpData.get('tEnd', '')
            tStart, tEnd = utils.getTimeSecondFromStr(tStart), utils.getTimeSecondFromStr(tEnd)
            if tStart <= utils.getNow() < tEnd:
                msg = tpData.get('shareMsg', gameStrings.PERSONAL_ZONE_TITLE)
                if not color:
                    color = tpData.get('msgColor', '')
                break

        if not msg:
            msg = PZCD.data.get('PERSONAL_ZONE_LINK_MSG', gameStrings.PERSONAL_ZONE_TITLE)
        msg = msg % self.baseInfo.get('roleName', '')
        isMissTianyu = self.isApplyGroupMT()
        if isMissTianyu:
            missTianyuPrefix = PZCD.data.get('shareLinkPrefix', gameStrings.TEXT_PERSONALZONESYSTEMPROXY_835)
            msg = missTianyuPrefix + ' ' + msg
            if not color:
                color = '#ff3aff'
        if not color and self.getFuDaiNumber() > 0:
            color = uiUtils.getColorValueByQuality(uiConst.QUALITY_ORANGE)
        if not color:
            color = '#ffe566'
        msgFormat = "<font color= \'%s\'>[<a href = \'event:shareZone-%d-%d\'><u>%s</u></a>]</font>"
        msg = msgFormat % (color,
         self.ownerGbID,
         self.getHostId(),
         msg)
        audioKey = self.baseInfo['audioKey']
        if audioKey:
            msg = richTextUtils.voiceRichText(audioKey) + msg
        gameglobal.rds.ui.sendLink(msg)

    def shareHome(self):
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

    def getHostId(self):
        if self.hostId:
            return self.hostId
        return int(gameglobal.rds.gServerid)

    def getFuDaiNumber(self):
        if self.baseInfo.get('fuDaiBonusType', 0) > 0:
            return self.baseInfo.get('fuDaiBonusNum', 0)
        return 0

    def setPopularityInfo(self, mainMc):
        mainMc.popularityArea.hotValueText.text = gameStrings.PERSONAL_ZONE_POPULARITY_TXT % self.baseInfo.get('popularity', 0)
        mainMc.popularityArea.hotIcon.x = mainMc.popularityArea.hotValueText.x + mainMc.popularityArea.hotValueText.width / 2 + mainMc.popularityArea.hotValueText.textWidth / 2 + 5
        mainMc.popularityArea.hotIcon.visible = False
        TipManager.addTip(mainMc.popularityArea.hotValueText, gameStrings.PERSONAL_ZONE_POPULARITY_TIP_TXT)
        mainMc.popularityArea.bgMc.gotoAndPlay('color' + str(self.baseInfo.get('hotLv', 0)))
        self.refreshFansMc()

    def getLabelTips(self, tagId):
        tmpText = ''
        if len(self.baseInfo.get('tags', {}).get(tagId, [])) > 0:
            if self.baseInfo['tags'][tagId][0] > 0:
                i = 0
                while i < 3 and i < len(self.baseInfo['tags'][tagId][1]):
                    if i == 2 or i == len(self.baseInfo['tags'][tagId][1]) - 1:
                        tmpText += self.baseInfo['tags'][tagId][1][i]
                    else:
                        tmpText += self.baseInfo['tags'][tagId][1][i] + gameStrings.TEXT_CHATPROXY_403
                    i += 1

                if self.baseInfo['tags'][tagId][0] == 1:
                    tmpText = tmpText + gameStrings.PERSONAL_ZONE_PRAISE_TAG_1
                else:
                    tmpText = tmpText + gameStrings.PERSONAL_ZONE_LINK_WORD + str(self.baseInfo['tags'][tagId][0]) + gameStrings.PERSONAL_ZONE_PRAISE_TAG_2
            else:
                tmpText = gameStrings.PERSONAL_ZONE_NO_PRAISE_TAG
        return tmpText

    def callLabelSetting(self, tags):
        gameglobal.rds.ui.spaceLabelSetting.show(tags)

    def handleClickEditTag(self, *arg):
        tags = self.baseInfo.get('tags', {})
        self.callLabelSetting(tags)

    def openPrettyGirlFunc(self):
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

    def setTagInfo(self, mainMc):
        mainMc.labelEditBtn.addEventListener(events.BUTTON_CLICK, self.handleClickEditTag, False, 0, True)
        mainMc.editTagMc.editTab.visible = False
        canvas = mainMc.editTagMc.tagLayer.canvas
        for i in xrange(6):
            labelItem = getattr(canvas, 't' + str(i), None)
            if labelItem:
                labelItem.visible = False

        l = len(self.baseInfo.get('tagsFormat', []))
        mainMc.editTagMc.tagDesc.visible = l == 0
        indexArray = [0,
         1,
         2,
         3,
         4,
         5]
        indexArray = random.shuffle(indexArray)
        for i in xrange(l):
            labelItem = getattr(canvas, 't' + str(i), None)
            if labelItem:
                labelItem.visible = True
                tmpData = self.baseInfo.get('tagsFormat', [])[i]
                labelItem.setData(tmpData.get('name', ''), tmpData.get('color', 0), tmpData.get('size', 22))
                labelItem.tagId = tmpData['tagId']
                TipManager.addTip(labelItem, self.getLabelTips(tmpData.get('tagId', 0)))
                labelItem.addEventListener(events.MOUSE_CLICK, self.handleClickTag, False, 0, True)

        t0 = canvas.t0
        t1 = canvas.t1
        t2 = canvas.t2
        t3 = canvas.t3
        t4 = canvas.t4
        t5 = canvas.t5
        offsetX = 0
        if t0.y + t0.height > mainMc.editTagMc.height:
            t0.y = mainMc.editTagMc.height - t0.height
        t5.x = t0.x - t5.width
        if t5.x < offsetX:
            offsetX = t5.x
        t4.y = t5.y - t4.height
        t4.x = t0.x - t4.width
        if t4.x < offsetX:
            offsetX = t4.x
        t2.y = t0.y - t2.height
        t1.y = t0.y - t1.height
        t1.x = t2.x - t1.width
        t3.y = min(t2.y - t3.height, t1.y - t3.height)
        t3.x = random.randint(1, 10)
        if offsetX < 0:
            canvas.x = -offsetX
        canvas.y = 0

    def handleClickTag(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget
        self.likePersonTag(int(t.tagId))

    def likePersonTag(self, tagId):
        p = BigWorld.player()
        p.base.likePersonalZoneTag(self.ownerGbID, tagId)

    def setCityInfo(self, mc):
        mc.saveCityBtn.addEventListener(events.BUTTON_CLICK, self.handleClickSaveCity, False, 0, True)
        mc.changeCityBtn.addEventListener(events.BUTTON_CLICK, self.handleClickChangeCity, False, 0, True)
        self.refreshCityBar()

    def refreshCityBar(self):
        mainMc = self.getMainMc()
        if not mainMc:
            return
        if self.cityEditState == BIRTH_NO_EDITING:
            mainMc.cityTxt.visible = True
            mainMc.cityEditMc.visible = False
            mainMc.saveCityBtn.visible = False
            mainMc.changeCityBtn.visible = self.baseInfo.get('spaceType', 0) == VISIT_TYPE_SELF
            self.refreshCityNoEdit()
        elif self.cityEditState == BIRTH_EDITING:
            mainMc.cityTxt.visible = False
            mainMc.cityEditMc.visible = True
            mainMc.saveCityBtn.visible = True
            mainMc.changeCityBtn.visible = False
            self.refreshCityEdit()
            mainMc.cityEditMc.menuProvince.selectedIndex = self.selProvince
            mainMc.cityEditMc.menuCity.selectedIndex = self.selCity

    def refreshCityNoEdit(self):
        mainMc = self.getMainMc()
        if mainMc:
            provinceCity = self.baseInfo.get('city', '-1|-1').split('|')
            serverP = -1
            serverC = -1
            if len(provinceCity) == 2:
                serverP = provinceCity[0]
                serverC = provinceCity[1]
            self.selProvince = self.simpleSelectFunc(self.selProvince, serverP)
            self.selCity = self.simpleSelectFunc(self.selCity, serverC)
            _textP = ''
            if self.selProvince > -1 and self.selProvince < len(self.cityDict['province']) - 1:
                _textP = self.getStrFormat(self.cityDict['province'], self.selProvince)
            _textC = ''
            if self.selCity > -1 and self.selCity < len(self.cityDict['city'][self.selProvince]) - 1:
                _textC = self.getStrFormat(self.cityDict['city'][self.selProvince], self.selCity)
            if _textP == '' or _textC == '':
                mainMc.cityTxt.text = gameStrings.PERSONAL_ZONE_DEFAULT_SETTTING_TXT
            else:
                txt = ''
                if _textP:
                    txt += _textP
                else:
                    txt += gameStrings.PERSONAL_ZONE_DEFAULT_SETTING_PROVINCE_TXT
                if _textC:
                    txt += _textC
                else:
                    txt += gameStrings.PERSONAL_ZONE_DEFAULT_SETTING_CITY_TXT
                mainMc.cityTxt.text = txt
            mainMc.changeCityBtn.x = mainMc.cityTxt.x + min(mainMc.cityTxt.width, mainMc.cityTxt.textWidth)

    def simpleSelectFunc(self, src, goal):
        if not goal:
            return -1
        if src == -1:
            if int(goal) >= 0:
                return int(goal)
            else:
                return -1
        else:
            return src

    def getStrFormat(self, data, index, isStringIndex = False):
        if not data:
            return ''
        elif index == -1:
            return ''
        else:
            return data[index]

    def refreshCityEdit(self):
        mainMc = self.getMainMc()
        if mainMc:
            provinceArr = []
            for i in xrange(len(self.cityDict['province'])):
                provinceArr.append({'label': str(self.cityDict.get('province', [])[i])})

            ASUtils.setDropdownMenuData(mainMc.cityEditMc.menuProvince, provinceArr)
            mainMc.cityEditMc.menuProvince.validateNow()
            mainMc.cityEditMc.menuProvince.addEventListener(events.EVENT_SELECT, self.handleSelectProvince, False, 0, True)
            mainMc.cityEditMc.menuCity.addEventListener(events.EVENT_SELECT, self.handleSelectCity, False, 0, True)
            self.refreshCityList()

    def handleSelectProvince(self, *arg):
        e = ASObject(arg[3][0])
        if e.currentTarget.selectedIndex >= 0:
            self.selProvince = e.currentTarget.selectedIndex
            self.refreshCityList()

    def handleSelectCity(self, *arg):
        e = ASObject(arg[3][0])
        if e.currentTarget.selectedIndex >= 0:
            self.selCity = e.currentTarget.selectedIndex

    def refreshCityList(self):
        mainMc = self.getMainMc()
        if not mainMc:
            return
        if self.selProvince == -1:
            return
        cityArr = []
        for i in xrange(len(self.cityDict.get('city', [])[self.selProvince])):
            cityArr.append({'label': str(self.cityDict.get('city', [])[self.selProvince][i])})

        ASUtils.setDropdownMenuData(mainMc.cityEditMc.menuCity, cityArr)
        mainMc.cityEditMc.menuCity.validateNow()

    def setBirthInfo(self, cityStr, saveType):
        keyList = []
        if saveType == TYPE_SAVEBIRTHDAY:
            keyList = [const.PERSONAL_ZONE_DATA_BIRTHDAY]
            self.baseInfo['birthday'] = cityStr
        elif saveType == TYPE_SAVECITY:
            keyList = [const.PERSONAL_ZONE_DATA_CITY]
            self.baseInfo['city'] = cityStr
        valueList = [cityStr]
        p = BigWorld.player()
        p.base.setPersonalZoneInfo(keyList, valueList)

    def handleClickSaveCity(self, *arg):
        self.cityEditState = BIRTH_NO_EDITING
        mainMc = self.getMainMc()
        if mainMc:
            self.selProvince = mainMc.cityEditMc.menuProvince.selectedIndex
            self.selCity = mainMc.cityEditMc.menuCity.selectedIndex
            cityStr = ''.join((str(self.selProvince), '|', str(self.selCity)))
            self.setBirthInfo(cityStr, TYPE_SAVECITY)
            self.baseInfo['city'] = cityStr
            self.refreshCityBar()

    def handleClickChangeCity(self, *arg):
        self.cityEditState = BIRTH_EDITING
        self.refreshCityBar()

    def getProfile(self, gbId):
        p = BigWorld.player()

        def _callBack(rStatus, content):
            self.onGetProfile(rStatus, content)

        pyq_interface.getProfile(_callBack, gbId)

    def onGetProfile(self, rStatus, content):
        if not self.hasBaseData():
            return
        if not content:
            return
        if rStatus != const.NET_CODE_SUCCESS:
            return
        if not content.get('code', 0):
            data = content.get('data', {})
            self.isFollowing = data.get('isFollowing', 0)
            self.fansNum = data.get('fansNum', 0)
            self.refreshFansMc()
            if self.currentTabIndex == uiConst.PERSONAL_ZONE_TAB_FIENDS_IDX:
                proxy = self.getCurrentProxy()
                proxy.refreshFollowBtn()

    def refreshFansMc(self):
        mainMc = self.getMainMc()
        if not mainMc:
            return
        fansNum = self.fansNum + self.baseInfo.get('fans', 0)
        if fansNum != -1:
            mainMc.fansArea.visible = True
            mainMc.fansArea.hotValueText.text = gameStrings.PERSONAL_ZONE_FANS_NUM_TXT % (fansNum,)
            mainMc.fansArea.hotIcon.x = mainMc.fansArea.hotValueText.x + mainMc.fansArea.hotValueText.width / 2 + mainMc.fansArea.hotValueText.textWidth / 2 + 5
            mainMc.fansArea.hotIcon.visible = False
            hotLv = self.getHotLv(fansNum)
            mainMc.fansArea.bgMc.gotoAndPlay('color' + str(hotLv))
        else:
            mainMc.fansArea.visible = False

    def setHeadMc(self, mc):
        mc.headArea.editHeadMc.button.visible = False
        mc.headArea.editHeadMc.button.addEventListener(events.BUTTON_CLICK, self.handleClickEditHead, False, 0, True)
        self.updatePhotoInfo()
        self.updatePhotoBorderInfo()
        if self.isSelfZone():
            mc.headArea.editHeadMc.visible = True
            mc.headArea.addEventListener(events.MOUSE_ROLL_OVER, self.handleRollOverHead, False, 0, True)
            mc.headArea.addEventListener(events.MOUSE_ROLL_OUT, self.handleRollOutHead, False, 0, True)
        else:
            mc.headArea.editHeadMc.visible = False

    def updatePhotoInfo(self):
        mc = self.getMainMc()
        if mc:
            mc.headArea.headIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
            mc.headArea.headIcon.fitSize = True
            mc.headArea.headIcon.serverId = self.baseInfo.get('hostId', 0)
            mc.headArea.headIcon.url = self.baseInfo.get('photo', '')

    def updatePhotoBorderInfo(self):
        mc = self.getMainMc()
        if mc and mc.headArea.borderImg:
            mc.headArea.borderImg.fitSize = True
            mc.headArea.borderImg.loadImage(self.baseInfo.get('photoBorderIcon', ''))

    def handleInputSignatureIn(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        mainMc = self.getMainMc()
        if e.target == mainMc.inputSignature:
            mainMc.signatureText.visible = False
            e.currentTarget.text = mainMc.signatureText.text

    def handleInputSignatureOut(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        mainMc = self.getMainMc()
        if e.target == mainMc.inputSignature:
            mainMc.signatureText.visible = True
            replyStr = e.currentTarget.text
            replyStr = replyStr.decode('gbk')
            replyStr = replyStr[:30]
            replyStr = replyStr.encode('gbk')
            self.uiAdapter.personalZoneSystem.sendSignature(replyStr)
            e.currentTarget.text = ''

    def handleRollOverSig(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        if e.currentTarget.focused:
            return
        e.currentTarget.gotoAndPlay('over')

    def handleRollOutSig(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        if e.currentTarget.focused:
            return
        e.currentTarget.gotoAndPlay('default')

    def handleClickEditHead(self, *arg):
        self.uiAdapter.personalZoneSystem.onEditRoleFigure()

    def handleRollOverHead(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget
        t.editHeadMc.gotoAndPlay('go')
        t.editHeadMc.button.visible = True

    def handleRollOutHead(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget
        t.editHeadMc.button.visible = False

    def getMainMc(self):
        mc = None
        proxy = self.getCurrentProxy()
        if hasattr(proxy, 'getMainMc'):
            mc = proxy.getMainMc()
        return mc

    def isOpen(self):
        if self.widget:
            return True
        return False

    def isSelfZone(self):
        return self.spaceType == VISIT_TYPE_SELF

    def delFont(self, matchobj):
        return matchobj.group(1)

    def analysisChatMsg(self, msg):
        msg = gameglobal.rds.ui.chat.parseMessage(msg)
        reFormat = re.compile('<FONT COLOR=\"#BFB499\">(.*?)</FONT>', re.DOTALL)
        msg = reFormat.sub(self.delFont, msg)
        msg = re.compile('!\\$([0-9]{1})').sub('#\\1', msg)
        msg = re.compile('#([0-9]{1})').sub('!$\\1', msg, uiConst.CHAT_MAX_FACE_CNT)
        msg = re.compile('\"!\\$([A-Fa-f0-9]{6})\"').sub('\"#\\1\"', msg)
        return msg

    def isCrossServer(self, showMsg = False):
        if self.hostId and self.hostId != int(gameglobal.rds.gServerid):
            if showMsg:
                p = BigWorld.player()
                p.showGameMsg(GMDD.data.FUNC_FORBID_IN_CROSS_SERVER_ZONE, ())
            return True
        return False

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def isApplyGroupMT(self):
        p = BigWorld.player()
        isMissTianyuClosed = p.missTianyuState == gametypes.MISS_TIANYU_CLOSE
        return self.baseInfo.get('applyGroupMT', False) == PZCD.data.get('mtSeason', 0) and not isMissTianyuClosed

    def syncPYQBonusData(self, pyqBonus):
        self.baseInfo['topic'] = pyqBonus
