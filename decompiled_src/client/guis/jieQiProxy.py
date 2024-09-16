#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/jieQiProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
from Scaleform import GfxValue
import gameglobal
import utils
import const
import gametypes
from guis import uiConst
from guis import uiUtils
from data import intimacy_data as IND
from data import intimacy_config_data as ICD
from data import school_data as SD
from data import intimacy_func_data as IFD
from data import intimacy_sys_event_data as ISED
from data import quest_data as QD
from data import message_desc_data as MSGDD
from data import intimacy_numeric_data as CIND

class JieQiProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(JieQiProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInitData': self.onGetInitData,
         'getIntroData': self.onGetIntroData,
         'showJieQiNickName': self.onShowJieQiNickname,
         'gotoFightForLove': self.onGotoFightForLove}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_JIEQI, self.hide)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def show(self):
        p = BigWorld.player()
        if p.friend.intimacyTgt != 0:
            self.showWindow()
            p.cell.queryIntimacyEvent(self.version)
        else:
            self.showWindow()

    def showWindow(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_JIEQI)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_JIEQI)

    def reset(self):
        self.version = 0
        self.mediator = None

    def onGetIntroData(self, *args):
        self.downLoadFriendPhoto()
        ret = IFD.data.items()
        sorted(ret, key=lambda d: d[0])
        return uiUtils.array2GfxAarry(ret, True)

    def refresh(self, version):
        self.version = version
        if self.mediator:
            self.mediator.Invoke('initView')

    def onGetInitData(self, *args):
        ret = {}
        p = BigWorld.player()
        if p.friend.intimacyTgt == 0:
            ret['hasJieQi'] = False
        else:
            ret['hasJieQi'] = True
            if not gameglobal.rds.configData.get('enableIntimacyTgtNickName', False):
                ret['bNicknameBtn'] = False
            else:
                ret['bNicknameBtn'] = True
        playerInfo = {}
        playerInfo['name'] = p.roleName
        school = SD.data.get(p.physique.school, {}).get('name', '')
        playerInfo['lv'] = school + ' Lv' + str(p.lv)
        playerInfo['sex'] = p.physique.sex
        ret['playerInfo'] = playerInfo
        if p.friend.intimacyTgt:
            fVal = p.getFValByGbId(p.friend.intimacyTgt)
            if fVal:
                info = {}
                info['name'] = fVal.name
                school = SD.data.get(fVal.school, {}).get('name', '')
                info['sex'] = fVal.sex
                info['lv'] = school + ' Lv' + str(fVal.level)
                info['intimacy'] = fVal.intimacy
                info['intimacyMaxLv'] = ICD.data.get('MAX_INTIMACY_LV', 9)
                info['isFamiIconUp'] = CIND.data.get(1, {}).get('minVal', 0) <= fVal.intimacy
                intimacyUpLv = gameglobal.rds.ui.friend.getFamiUpIntimacyLv(fVal.intimacy)
                if info['isFamiIconUp'] and intimacyUpLv:
                    info['intimacyLv'] = intimacyUpLv
                    info['intimacyName'] = CIND.data.get(intimacyUpLv, {}).get('name', gameStrings.TEXT_FRIENDPROXY_1789)
                    info['intimacyFull'] = CIND.data.get(intimacyUpLv, {}).get('maxVal', 0) <= fVal.intimacy
                else:
                    info['intimacyLv'] = fVal.intimacyLv
                    info['intimacyName'] = IND.data.get(fVal.intimacyLv, {}).get('name', gameStrings.TEXT_FRIENDPROXY_1789)
                    info['intimacyFull'] = IND.data.get(fVal.intimacyLv, {}).get('maxVal', 0) <= fVal.intimacy
                info['jieQiDays'] = utils.diffYearMonthDayInt(int(uiUtils._getTodayDate()), utils.getYearMonthDayInt(p.friend.tBuildIntimacy))
                ret['targetInfo'] = info
        timeLineInfo = []
        if hasattr(p, 'intimacyEvent') and p.intimacyEvent:
            for key in p.intimacyEvent:
                for event in p.intimacyEvent[key]:
                    intimacyEventDesc = self.getDescByMsg(event.msgType, event.msg)
                    if gameglobal.rds.configData.get('enableNotifyBuildIntimacyCnt', False) and p.getBuildIntimacyCnt() > 0 and event.msgType == gametypes.INTIMACY_EVENT_TYPE_SYS and int(event.msg) == 0:
                        if p.isOldBuildIntimacy:
                            cnt = p.getBuildIntimacyCnt() + 100 - p.getBuildIntimacyCnt() % 100
                            extraMsg = MSGDD.data.get('LAST_BUILD_INTIMACY_CNT_MSG', gameStrings.TEXT_JIEQIPROXY_123)
                        else:
                            cnt = p.getBuildIntimacyCnt()
                            extraMsg = MSGDD.data.get('BUILD_INTIMACY_CNT_MSG', gameStrings.TEXT_JIEQIPROXY_126)
                        intimacyEventDesc += extraMsg % cnt
                    timeLineInfo.append({'time': self.getTimeByWhen(key),
                     'desc': intimacyEventDesc,
                     'when': event.when})

            timeLineInfo = sorted(timeLineInfo, key=lambda d: d['when'], reverse=True)
        ret['timeLineInfo'] = timeLineInfo
        return uiUtils.dict2GfxDict(ret, True)

    def getDescByMsg(self, mType, msg):
        desc = ''
        p = BigWorld.player()
        if mType == gametypes.INTIMACY_EVENT_TYPE_SYS:
            desc = ISED.data.get(int(msg)).get('desc', '')
        elif mType == gametypes.INTIMACY_EVENT_TYPE_DESC:
            desc = msg
        elif mType == gametypes.INTIMACY_EVENT_TYPE_BIRTHDAY:
            fVal = p.getFValByGbId(p.friend.intimacyTgt)
            if fVal:
                desc = ICD.data.get('INTIMACY_BIRTH_DESC', '') % fVal.name
        elif mType == gametypes.INTIMACY_EVENT_TYPE_QUEST:
            questId = int(msg)
            desc = ICD.data.get('INTIMACY_QUEST_DESC', '') % QD.data.get(questId, {}).get('name', '')
        return desc

    def downLoadFriendPhoto(self):
        p = BigWorld.player()
        if p.profileIcon != '':
            p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, p.profileIcon, gametypes.NOS_FILE_PICTURE, self.onDownloadSelfProfilePhoto, (None,))
        else:
            defaultPhoto = 'headIcon/%s.dds' % str(p.school * 10 + p.physique.sex)
            if self.mediator:
                self.mediator.Invoke('setPlayerIcon', GfxValue(defaultPhoto))
        if p.friend.intimacyTgt:
            fVal = p.getFValByGbId(p.friend.intimacyTgt)
            photo = p._getFriendPhoto(fVal)
            if uiUtils.isDownloadImage(photo):
                p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, photo, gametypes.NOS_FILE_PICTURE, self.onDownloadOtherPhoto, (None,))
            elif self.mediator:
                self.mediator.Invoke('setTargetIcon', GfxValue(photo))

    def getTimeByWhen(self, when):
        return str(when[1]) + '.' + str(when[2])

    def onDownloadOtherPhoto(self, status, callbackArgs):
        p = BigWorld.player()
        fVal = p.getFValByGbId(p.friend.intimacyTgt)
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + fVal.photo + '.dds'
            if self.mediator:
                self.mediator.Invoke('setTargetIcon', GfxValue(photo))

    def onDownloadSelfProfilePhoto(self, status, callbackArgs):
        p = BigWorld.player()
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + p.friend.photo + '.dds'
            if self.mediator:
                self.mediator.Invoke('setPlayerIcon', GfxValue(photo))

    def onShowJieQiNickname(self, *args):
        if not gameglobal.rds.ui.jieQiNickname.widget:
            gameglobal.rds.ui.jieQiNickname.show()

    def onGotoFightForLove(self, *args):
        p = BigWorld.player()
        p.seekFightForLoveNpc()
