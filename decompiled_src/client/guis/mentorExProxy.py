#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mentorExProxy.o
from gamestrings import gameStrings
import cPickle
import BigWorld
from Scaleform import GfxValue
import const
import uiConst
import uiUtils
import gameglobal
import events
import ui
import npcConst
import gametypes
import random
from gamestrings import gameStrings
from ui import unicode2gbk
from uiProxy import UIProxy
from helpers import taboo
from callbackHelper import Functor
from guis import menuManager
from guis import asObject
from guis.asObject import TipManager
from data import apprentice_new_config_data as ANCD
from data import friend_location_data as FLD
from data import intimacy_skill_data as ISD
from data import apprentice_target_data as ATD
from cdata import game_msg_def_data as GMDD
OP_MENTOR = 1
OP_APPRENTICE = 2
RECOMMEND_NUM = 6
TAB_APPRENTICE_INFO = 0
TAB_FIND_MENTOR = 1
TAB_FIND_APPRENTICE = 2
MAX_TARGET_NUM = 8
TARGET_ACTION_SEEK = 1
TARGET_ACTION_SHOW_HELP = 2

class MentorExProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MentorExProxy, self).__init__(uiAdapter)
        self.modelMap = {'getMentorInfo': self.onGetMentorInfo,
         'getExtraApprenticeInfoEx': self.onGetExtraApprenticeInfoEx,
         'getRecommendMentor': self.onGetRecommendMentor,
         'getRecommendApprentice': self.onGetRecommendApprentice,
         'clickBtn': self.onClickBtn,
         'sendMsg': self.onSendMsg,
         'applyGraduate': self.onApplyGraduate,
         'getMentorExRewardList': self.onGetMentorExRewardList,
         'mentorBtnClick': self.onMentorBtnClick,
         'apprenticeBtnClick': self.onApprenticeBtnClick,
         'gotoQuest': self.onGotoQuest,
         'openWeekTargetPanel': self.onOpenWeekTargetPanel}
        self.selectMentorGbId = 0
        self.remarks = None
        self.lastSloganMsg = {}
        self.lastGraduteMsg = ANCD.data.get('graduateDefaultRemark', '')
        self.mentorPreferenceInfo = None
        self.apprenticePreferenceInfo = None
        self.recomendRank = {OP_APPRENTICE: 0,
         OP_MENTOR: 0}
        self.recomendData = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_MENTOR_EX, self.hideMentor)
        uiAdapter.registerEscFunc(uiConst.WIDGET_MENTOREX_SEND_MSG, self.hideSendMsg)
        uiAdapter.registerEscFunc(uiConst.WIDGET_MENTOREX_GRADUATE, self.hideGraduateWidget)
        uiAdapter.registerEscFunc(uiConst.WIDGET_APPRENTICE_REMARK, self.hideRemarksWidget)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        p = BigWorld.player()
        if widgetId == uiConst.WIDGET_MENTOR_EX:
            self.mediator = mediator
            if p.apprenticeInfo:
                p.base.getApprenticeInfoByGbIdEx(p.apprenticeInfo.keys(), 'onGetApprenticeInfoEx')
            return self._getGfxMentorData()
        if widgetId == uiConst.WIDGET_MENTOREX_SEND_MSG:
            msg = self.lastSloganMsg.get(self.sendMsgType, '')
            if not msg:
                msg = random.choice(ANCD.data.get('sloganMsg', {}).get(self.sendMsgType, ['default']))
            initData = {'defaultMsg': msg,
             'maxChars': ANCD.data.get('sloganMaxChars', 50),
             'msgNumTxt': gameStrings.TEXT_MENTOREXPROXY_92 % ANCD.data.get('sloganMaxChars', 50)}
            return uiUtils.dict2GfxDict(initData, True)
        if widgetId == uiConst.WIDGET_MENTOREX_GRADUATE:
            graduateRewards = ()
            for key, val in ANCD.data.get('graduateRewards', {}).items():
                minLv, maxLv = key
                if minLv <= p.lv and p.lv <= maxLv:
                    graduateRewards = val

            info = self._getInfoByGbId(self.selectMentorGbId)
            initData = {'isPerfectGraduate': self.graduateRet == gametypes.APPRENTICE_GRADUATE_EXCELLENT,
             'remarkMaxChars': ANCD.data.get('remarkMaxChars', 50),
             'rewardItem': [ uiUtils.getGfxItemById(itemId, cnt) for itemId, cnt in graduateRewards ],
             'npcName': ANCD.data.get('apprenticeQuestNpc', 'npc'),
             'lastGraduteMsg': self.lastGraduteMsg,
             'graduateGradeDesc': ANCD.data.get('graduateGradeDesc', {}).values(),
             'msg': uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_EX_GRADUATE_REMARK_MSG, '%s') % info.get('name', '')}
            return uiUtils.dict2GfxDict(initData, True)
        if widgetId == uiConst.WIDGET_APPRENTICE_REMARK:
            remarkList = []
            if self.remarks:
                for gbId, val in self.remarks.items():
                    name, remark = val
                    remarkList.append({'gbId': str(gbId),
                     'playerName': name,
                     'remarkMsg': remark,
                     'isFriend': bool(p.getFValByGbId(gbId))})

            initData = {'list': remarkList}
            return uiUtils.dict2GfxDict(initData, True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_MENTOR_EX:
            self.hideMentor()
        elif widgetId == uiConst.WIDGET_MENTOREX_SEND_MSG:
            self.hideSendMsg()
        elif widgetId == uiConst.WIDGET_MENTOREX_GRADUATE:
            self.hideGraduateWidget()
        elif widgetId == uiConst.WIDGET_APPRENTICE_REMARK:
            self.hideRemarksWidget()

    def show(self, *args):
        if self._checkCanOpen():
            if args:
                self.tabIdx = args[0]
            else:
                p = BigWorld.player()
                if p.hasMentorEx() or p.hasApprenticeEx():
                    self.tabIdx = TAB_APPRENTICE_INFO
                elif p.lv < ANCD.data.get('minMentorLv', 49):
                    self.tabIdx = TAB_FIND_MENTOR
                else:
                    self.tabIdx = TAB_FIND_APPRENTICE
            if not self.mediator:
                self.uiAdapter.loadWidget(uiConst.WIDGET_MENTOR_EX)
                gameglobal.rds.uiLog.addOpenLog(uiConst.WIDGET_MENTOR_EX)
            else:
                self.refreshPanel()

    def showSendMsg(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_MENTOREX_SEND_MSG)

    def showGraduateWidget(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_MENTOREX_GRADUATE)

    @ui.uiEvent(uiConst.WIDGET_MENTOR_EX, (events.EVENT_ADD_APPRENTICE_IFNO, events.EVENT_REMOVE_APPRENTICE_IFNO))
    @ui.callAfterTime(1)
    def refreshPanel(self):
        if self.mediator:
            self.mediator.Invoke('refreshPanel', self._getGfxMentorData())

    def refreshRecommendList(self, res, isMentor):
        if self.mediator:
            ret = self.getRecommendList(res, isMentor)
            self.mediator.Invoke('refreshRecommendList', (GfxValue(isMentor), uiUtils.array2GfxAarry(ret, True)))

    def clearWidget(self):
        self.hideMentor()

    def reset(self):
        self.mediator = None
        self.sendMsgType = 0
        self.tabIdx = 0
        self.getExtraInfos = {}
        self.recomendRank = {OP_APPRENTICE: 0,
         OP_MENTOR: 0}
        self.targetPanel = None

    def hideMentor(self):
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MENTOR_EX)
        self.hideSendMsg()
        self.hideGraduateWidget()
        self.hideRemarksWidget()
        self.reset()

    def clearAll(self):
        self.reset()
        self.apprenticePreferenceInfo = None
        self.mentorPreferenceInfo = None
        self.recomendRank = {OP_APPRENTICE: 0,
         OP_MENTOR: 0}
        self.recomendData = {}

    def hideSendMsg(self):
        self.sendMsgType = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MENTOREX_SEND_MSG)

    def hideGraduateWidget(self):
        self.selectMentorGbId = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MENTOREX_GRADUATE)

    def hideRemarksWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_APPRENTICE_REMARK)
        self.remarks = None

    def onGetMentorInfo(self, *args):
        p = BigWorld.player()
        ret = {}
        mentorList = []
        maxApprenticeNum = ANCD.data.get('maxApprenticeNum', 5)
        curApprenticeNum = maxApprenticeNum
        for gbId, val in p.apprenticeInfo.items():
            graduateList = []
            unGraduateList = []
            mentorInfo = self._getInfoByGbId(gbId)
            if not mentorInfo:
                continue
            mentorInfo['isSole'] = getattr(p, 'soleMentorGbId') == gbId
            mentorInfo['appleySoleLabel'] = gameStrings.TEXT_MENTOREXPROXY_233 if p.soleMentorGbId == gbId else gameStrings.TEXT_MENTOREXPROXY_233_1
            extraInfo = self.getExtraInfos.get(gbId, (0, 0, '', 0, '', 0))
            intimacyName = extraInfo[4]
            soleGbId = extraInfo[5]
            if intimacyName:
                mentorInfo['isJieQi'] = True
                mentorInfo['jieQiTip'] = gameStrings.TEXT_MENTOREXPROXY_240 % intimacyName
            else:
                mentorInfo['isJieQi'] = False
                mentorInfo['jieQiTip'] = gameStrings.TEXT_MENTOREXPROXY_243
            mentorInfo['mentorOnlineTxt'] = uiUtils.getLastOnlineTxt(extraInfo[3])
            fameId = ANCD.data.get('apprenticeFameID', 454)
            fameLv = uiUtils.getFameLv(fameId, extraInfo[1])
            mentorInfo['fame'] = fameLv
            mentorInfo['fameTip'] = ANCD.data.get('fameLvTips', {}).get(fameLv, '')
            pullId = ANCD.data.get('pullMentorSkillId', 0)
            limit = ISD.data.get((pullId, 1), {}).get('useLimit', 0)
            if pullId and p.intimacySkills.has_key(pullId) and limit > 0:
                cnt = p.intimacySkills.get(pullId).useCnt
                mentorInfo['pullMentorLabel'] = gameStrings.TEXT_MENTOREXPROXY_253 % (cnt, limit)
                mentorInfo['pullMentorEnable'] = cnt < limit
            else:
                mentorInfo['pullMentorLabel'] = gameStrings.TEXT_CONST_5282
                mentorInfo['pullMentorEnable'] = True
            for mateGbId, isGraduate in val.get('mates'):
                info = self._getInfoByGbId(mateGbId)
                if not info:
                    continue
                info['isSole'] = soleGbId == mateGbId
                if info:
                    if isGraduate:
                        graduateList.append(info)
                        info['graduate'] = True
                    else:
                        info['graduate'] = False
                        unGraduateList.append(info)

            tmp = []
            for i in xrange(maxApprenticeNum):
                if i + 1 > len(unGraduateList):
                    if i + 1 > curApprenticeNum:
                        state = uiConst.APPRNETICE_STATE_LOCK
                    else:
                        state = uiConst.APPRNETICE_STATE_EMPTY
                    tmp.append({'state': state,
                     'graduate': False})

            unGraduateList.extend(tmp)
            unGraduateList.extend(graduateList)
            mentorInfo['mateInfo'] = unGraduateList
            mentorList.append(mentorInfo)

        ret['mentorList'] = mentorList
        apprenticeList = []
        apprenticeInfo = {'apprenticeVal': gameStrings.TEXT_MENTOREXPROXY_286 % p.apprenticeVal.get('totalVal', 0),
         'weekApprenticeVal': gameStrings.TEXT_MENTOREXPROXY_287 % p.apprenticeVal.get('weeklyVal', 0),
         'apprenticeValTips': ANCD.data.get('apprenticeValTips', '1'),
         'weekApprenticeValTips': ANCD.data.get('weekApprenticeValTips', '2')}
        graduate = []
        unGraduate = []
        empty = []
        for gbId, isGraduate in p.apprenticeGbIds:
            info = self._getInfoByGbId(gbId)
            if info:
                fVal = p.friend.get(gbId, None)
                tips = gameStrings.TEXT_MENTOREXPROXY_298 % p.apprenticeVal.get(gbId, 0)
                if fVal:
                    tips += gameStrings.TEXT_MENTOREXPROXY_300 % fVal.intimacy
                info['tips'] = tips
                info['graduate'] = isGraduate
                info['state'] = 0
                info['isSole'] = p.soleApprenticeGbId == gbId
                if isGraduate:
                    graduate.append(info)
                else:
                    unGraduate.append(info)

        curApprenticeNum = p.getMaxApprenticeNum()
        for i in xrange(maxApprenticeNum):
            if i + 1 > len(unGraduate):
                if i + 1 > curApprenticeNum:
                    state = uiConst.APPRNETICE_STATE_LOCK
                else:
                    state = uiConst.APPRENTICE_STATE_ADD
                empty.append({'state': state,
                 'tips': ANCD.data.get('lockApprenticeTips', {}).get(i + 1, '')})

        apprenticeList.extend(unGraduate)
        apprenticeList.extend(empty)
        if not graduate:
            graduate.append({'state': uiConst.APPRNETICE_STATE_EMPTY})
        apprenticeList.extend(graduate)
        if p.soleApprenticeGbId:
            apprenticeInfo['soleApprentice'] = self._getInfoByGbId(p.soleApprenticeGbId)
        apprenticeInfo['apprenticeList'] = apprenticeList
        ret['apprenticeInfo'] = apprenticeInfo
        reward = []
        for val in ANCD.data.get('apprentiveValRewards', []):
            reward.append({'desc': val.get('desc', ''),
             'rewards': [ uiUtils.getGfxItemById(itemId, cnt) for itemId, cnt in val.get('items', []) ]})

        ret['reward'] = reward
        ret['addMentorTip'] = ANCD.data.get('addMentorTip', '')
        ret['rewardDesc'] = ANCD.data.get('weekApprenticeValRewardDesc', '')
        ret['hasMentor'] = p.hasMentorEx()
        ret['hasApprentice'] = p.hasApprenticeEx()
        return uiUtils.dict2GfxDict(ret, True)

    def onGetApprenticeInfo(self, *args):
        p = BigWorld.player()
        graduate = []
        unGraduate = []
        ret = {'apprenticeVal': p.apprenticeVal.get('totalVal', 0),
         'weekApprenticeVal': p.apprenticeVal.get('weeklyVal', 0)}
        for gbId, isGraduate in p.apprenticeGbIds:
            info = self._getInfoByGbId(gbId)
            if info:
                fVal = p.friend.get(gbId, None)
                tips = gameStrings.TEXT_MENTOREXPROXY_298 % p.apprenticeVal.get(gbId, 0)
                if fVal:
                    tips += gameStrings.TEXT_MENTOREXPROXY_300 % fVal.intimacy
                info['tips'] = tips
                if isGraduate:
                    graduate.append(info)
                else:
                    unGraduate.append(info)

        ret['graduateInfo'] = {'title': gameStrings.TEXT_MENTOREXPROXY_372 % len(graduate),
         'list': graduate}
        ret['ungraduateInfo'] = {'title': gameStrings.TEXT_MENTOREXPROXY_374 % len(unGraduate),
         'list': unGraduate}
        reward = []
        for val in ANCD.data.get('apprentiveValRewards', []):
            reward.append({'desc': val.get('desc', ''),
             'rewards': [ uiUtils.getGfxItemById(itemId, cnt) for itemId, cnt in val.get('items', []) ]})

        ret['reward'] = reward
        return uiUtils.dict2GfxDict(ret, True)

    def onGetExtraApprenticeInfoEx(self, *args):
        gbId = int(args[3][0].GetString())
        p = BigWorld.player()
        if gbId not in self.getExtraInfos:
            p.base.getApprenticeInfoByGbIdEx((gbId,), 'onGetApprenticeInfoEx')

    def onGetRecommendMentor(self, *args):
        return uiUtils.dict2GfxDict(self.getRecommendInfo(OP_MENTOR), True)

    def onGetRecommendApprentice(self, *args):
        return uiUtils.dict2GfxDict(self.getRecommendInfo(OP_APPRENTICE), True)

    def getRecommendInfo(self, opType):
        data = self.recomendData.get(opType, None)
        preferenceInfo = self.mentorPreferenceInfo if opType == OP_MENTOR else self.apprenticePreferenceInfo
        ret = {'list': []}
        hadSetPreferenceInfo = True
        if gameglobal.rds.configData.get('enableUSRecommendApprentice', False):
            if not preferenceInfo:
                hadSetPreferenceInfo = False
            if preferenceInfo:
                ret['preferenceInfo'] = preferenceInfo
            msg = self.lastSloganMsg.get(opType, '')
            if not msg:
                msg = random.choice(ANCD.data.get('sloganMsg', {}).get(opType, ['default']))
            ret['slogonTxt'] = msg
            ret['sexProvider'] = gameStrings.SEX_DROPMENU_PROVIDER
            ret['maxChars'] = ANCD.data.get('sloganMaxChars', 50)
            if opType == OP_MENTOR:
                ret['sendMsgLabel'] = gameStrings.SEND_MENTOR_PREFERENCE_BTN_TXT
            else:
                ret['sendMsgLabel'] = gameStrings.SEND_APPRENTICE_PREFERENCE_BTN_TXT
        elif opType == OP_MENTOR:
            ret['sendMsgLabel'] = gameStrings.SEND_MENTOR_SLOGON_BTN_TXT
        else:
            ret['sendMsgLabel'] = gameStrings.SEND_APPRENTICE_SLOGON_BTN_TXT
        if data:
            ret['list'] = self.getRecommendList(data, opType == OP_MENTOR)
        rank = self.recomendRank.get(opType, 0)
        if hadSetPreferenceInfo and rank == 0:
            if opType == OP_MENTOR:
                BigWorld.player().base.getRecommendMentorsEx(rank)
            else:
                BigWorld.player().base.getRecommendApprenticesEx(rank)
        return ret

    def onGetMentorExRewardList(self, *args):
        ret = []
        rewardList = []
        for val in ANCD.data.get('apprenticeRewards', []):
            info = {'label': val.get('label', ''),
             'rewardIdx': len(rewardList)}
            for rewardItem in val.get('rewardList', []):
                obj = {'type': rewardItem.get('type', ''),
                 'desc': rewardItem.get('desc', ''),
                 'title': rewardItem.get('title', '')}
                if rewardItem.get('type', '') == 2:
                    obj['rewardItem'] = [ uiUtils.getGfxItemById(itemId, cnt) for itemId, cnt in rewardItem.get('items', []) ]
                if rewardItem.get('type', '') == 3:
                    obj['img'] = rewardItem.get('img')
                rewardList.append(obj)

            ret.append(info)

        data = {'list': ret,
         'rewardList': rewardList}
        return uiUtils.dict2GfxDict(data, True)

    def onClickBtn(self, *args):
        btnName = unicode2gbk(args[3][0].GetString())
        gbId = unicode2gbk(args[3][1].GetString())
        roleName = unicode2gbk(args[3][2].GetString())
        opType = args[3][3].GetNumber()
        p = BigWorld.player()
        if btnName == 'changeBtn':
            rank = self.recomendRank.get(opType, 0) + RECOMMEND_NUM
            if opType == OP_APPRENTICE:
                p.base.getRecommendApprenticesEx(rank)
            elif opType == OP_MENTOR:
                p.base.getRecommendMentorsEx(rank)
        elif btnName == 'applyBtn' and roleName:
            if opType == OP_APPRENTICE:
                p.base.applyApprenticeEx(roleName)
            elif opType == OP_MENTOR:
                p.base.applyMentorEx(roleName)
        elif btnName == 'sendMsgBtn':
            self.sendMsgType = opType
            self.showSendMsg()
        elif btnName == 'comfirmPreferenceBtn':
            preferenceInfo = self._getCurrentSettingPreference()
            if self._checkSlogan(preferenceInfo.get('slogan', '')):
                preferenceInfoDump = cPickle.dumps(preferenceInfo, -1)
                preferenceType = gametypes.APPRENTICE_PREFERENCE_MENTOR if opType == OP_MENTOR else gametypes.APPRENTICE_PREFERENCE_APPRENTICE
                p.base.setApprenticePreference(preferenceType, preferenceInfoDump)

    def onSendMsg(self, *args):
        msg = unicode2gbk(args[3][0].GetString())
        p = BigWorld.player()
        if self._checkSlogan(msg):
            if msg not in ANCD.data.get('sloganMsg', {}).get(self.sendMsgType, []):
                self.lastSloganMsg[self.sendMsgType] = msg
            if self.sendMsgType == OP_MENTOR:
                p.base.setBeApprenticeSloganEx(msg)
                self.hideSendMsg()
            elif self.sendMsgType == OP_APPRENTICE:
                p.base.setBeMentorSloganEx(msg)
                self.hideSendMsg()

    def _checkSlogan(self, slogan):
        p = BigWorld.player()
        if len(slogan):
            isNormal, msg = taboo.checkDisbWord(slogan)
            if not isNormal:
                p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
                return False
            flag, msg = self.uiAdapter.chat._tabooCheck(const.CHAT_CHANNEL_WORLD, msg)
            if not flag:
                p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
                return False
        else:
            p.showGameMsg(GMDD.data.APPRENTICE_SLOGON_IS_EMPTY, ())
            return False
        return True

    def onApplyGraduate(self, *args):
        remark = unicode2gbk(args[3][0].GetString())
        grade = int(args[3][1].GetNumber())
        p = BigWorld.player()
        isNormal, remark = taboo.checkDisbWord(remark)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
            return
        isNormal, remark = taboo.checkBSingle(remark)
        if not isNormal:
            p.showGameMsg(GMDD.data.FRIEND_CHAT_MSG_TABOO, ())
        self.lastGraduteMsg = remark
        BigWorld.player().base.apprenticeGraduateAfterConfirmEx(self.selectMentorGbId, grade, remark)
        self.hideGraduateWidget()

    def onMentorBtnClick(self, *args):
        btnName = unicode2gbk(args[3][0].GetString())
        roleName = unicode2gbk(args[3][1].GetString())
        gbId = int(unicode2gbk(args[3][2].GetString()))
        p = BigWorld.player()
        if btnName == 'graduateBtn':
            self.hideGraduateWidget()
            self.selectMentorGbId = gbId
            p.base.applyGraduateEx(self.selectMentorGbId)
        elif btnName == 'killMentorBtn':
            p.kickMentorCheckSoleEx(gbId)
        elif btnName == 'viewEquipBtn' or btnName == 'viewEquip':
            p.cell.getEquipment(roleName)
        elif btnName == 'viewRoleInfo':
            p.getPersonalSysProxy().openZoneOther(gbId, None, const.PERSONAL_ZONE_SRC_MENTOR)
        elif btnName == 'addFriend':
            menuManager.getInstance().menuTarget.apply(roleName, gbId=gbId)
            menuManager.getInstance().addFriend()
        elif btnName == 'viewMsg':
            p.base.getGraduateRemarkByGbIdEx(gbId)
        elif btnName == 'baishi':
            if gameglobal.rds.configData.get('enableUSRecommendApprentice'):
                lv = int(args[3][3].GetNumber())
                p.base.applyMentorByGbIdEx(roleName, gbId, lv)
            else:
                p.base.applyMentorEx(roleName)
        elif btnName == 'viewZoneBtn':
            p.getPersonalSysProxy().openZoneOther(gbId, None, const.PERSONAL_ZONE_SRC_MENTOR)
        elif btnName == 'applyBtn':
            if p.soleMentorGbId == gbId:
                self.applySoleDismissEx(gbId)
            else:
                self.applySoleMentorEx(gbId)
        elif btnName == 'inviteTeam':
            menuManager.getInstance().menuTarget.apply(roleName)
            menuManager.getInstance().inviteTeam()
        elif btnName == 'privateChat':
            menuManager.getInstance().menuTarget.apply(roleName)
            menuManager.getInstance().privateChat()
        elif btnName == 'copyName':
            BigWorld.setClipBoardText(roleName)
        elif btnName == 'kickMentor':
            p.base.kickMentorEx(gbId)
        elif btnName == 'callBtn':
            pullId = ANCD.data.get('pullMentorSkillId')
            if pullId:
                p.cell.useIntimacySkill(pullId, (str(gbId),))

    def onApprenticeBtnClick(self, *args):
        btnName = unicode2gbk(args[3][0].GetString())
        roleName = unicode2gbk(args[3][1].GetString())
        gbId = int(unicode2gbk(args[3][2].GetString()))
        p = BigWorld.player()
        if btnName in ('addSoleBtn', 'addSoleBtn1'):
            playerList = []
            for gbId, isGraduate in p.apprenticeGbIds:
                if isGraduate:
                    continue
                info = self._getInfoByGbId(gbId)
                if not info:
                    continue
                info['desc'] = 'Lv.%s' % info.get('lv', 0)
                playerList.append(info)

            if playerList:
                self.uiAdapter.playerSelect.show(playerList, gameStrings.TEXT_MENTOREXPROXY_593, self.onSelSoleApprentice)
            else:
                p.showGameMsg(GMDD.data.NO_APPRENTICE_FOR_SOLE, ())
        elif btnName == 'viewEquip':
            p.cell.getEquipment(roleName)
        elif btnName == 'addFriend':
            menuManager.getInstance().menuTarget.apply(roleName, gbId=gbId)
            menuManager.getInstance().addFriend()
        elif btnName == 'viewRoleInfo' or btnName == 'viewProfile':
            p.getPersonalSysProxy().openZoneOther(gbId, None, const.PERSONAL_ZONE_SRC_MENTOR)
        elif btnName == 'shoutu':
            if gameglobal.rds.configData.get('enableUSRecommendApprentice'):
                lv = int(args[3][3].GetNumber())
                p.base.applyApprenticeByGbIdEx(roleName, gbId, lv)
            else:
                p.base.applyApprenticeEx(roleName)
        elif btnName == 'dismissSoleBtn':
            self.applySoleDismissEx(gbId)
        elif btnName == 'inviteTeam':
            menuManager.getInstance().menuTarget.apply(roleName)
            menuManager.getInstance().inviteTeam()
        elif btnName == 'privateChat':
            menuManager.getInstance().menuTarget.apply(roleName)
            menuManager.getInstance().privateChat()
        elif btnName == 'copyName':
            BigWorld.setClipBoardText(roleName)
        elif btnName == 'remarksBtn':
            p.base.getGraduateRemarkByGbIdEx(p.gbId)
        elif btnName == 'setWeekGoal':
            if not gameglobal.rds.configData.get('enableApprenticeTarget'):
                p.showGameMsg(GMDD.data.STILL_UNDER_DEVELOPING, ())
            else:
                self.uiAdapter.apprenticeTarget.show()

    def onGotoQuest(self, *args):
        seekId = ANCD.data.get('apprenticeQuestNpcSeekerId', 0)
        if seekId:
            uiUtils.gotoTrack(seekId)

    def onOpenWeekTargetPanel(self, *args):
        self.targetPanel = asObject.ASObject(args[3][0])
        self.initTargetPanel()

    def onGetRecommendApprenticesEx(self, res, isMentor):
        if not self.mediator:
            return
        opType = OP_MENTOR if isMentor else OP_APPRENTICE
        self.recomendData[opType] = res
        self.recomendRank[opType] = self.recomendRank[opType] + RECOMMEND_NUM
        self.refreshRecommendList(res, isMentor)

    def getRecommendList(self, res, isMentor = False):
        ret = []
        for gbId, name, lv, school, sex, fsex, photo, slogan in res:
            if not photo:
                photo = 'headIcon/%s.dds' % str(school * 10 + sex)
            opType = OP_APPRENTICE if isMentor else OP_MENTOR
            obj = {'gbId': str(gbId),
             'roleName': name,
             'lvTxt': 'Lv.%s' % lv,
             'lv': lv,
             'school': school,
             'schoolTxt': const.SCHOOL_DICT.get(school),
             'schoolDesc': uiConst.SCHOOL_FRAME_DESC.get(school),
             'sex': fsex,
             'sexTxt': const.SEX_NAME.get(fsex),
             'headIcon': photo,
             'msg': slogan if slogan else random.choice(ANCD.data.get('sloganMsg', {}).get(opType, ['']))}
            ret.append(obj)

        return ret

    def onApplyGraduateEx(self, apprenticeGbId, apprenticeName):
        curPush = self.uiAdapter.pushMessage.getDataList(uiConst.MESSAGE_TYPE_APPLY_GRADUATE)
        pushData = {'data': (apprenticeGbId, apprenticeName)}
        for val in curPush:
            if val == pushData:
                return

        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_APPLY_GRADUATE, pushData)

    def onClickGraduateExPush(self):
        pushData = self.uiAdapter.pushMessage.getLastData(uiConst.MESSAGE_TYPE_APPLY_GRADUATE)
        apprenticeGbId, apprenticeName = pushData.get('data')
        msg = ANCD.data.get('applyGraduateMsg', '%s applyGraduate') % apprenticeName
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.confirmGraduateEx, apprenticeGbId, apprenticeName), noBtnText=gameStrings.TEXT_MENTOREXPROXY_679)

    def confirmGraduateEx(self, apprenticeGbId, apprenticeName):
        pushData = {'data': (apprenticeGbId, apprenticeName)}
        self.uiAdapter.pushMessage.removeData(uiConst.MESSAGE_TYPE_APPLY_GRADUATE, pushData)
        BigWorld.player().base.onApplyGraduateConfirmEx(apprenticeGbId, True)

    def onApprenticeGraduateEx(self, mentorGbId, ret):
        self.selectMentorGbId = mentorGbId
        self.graduateRet = ret
        self.showGraduateWidget()

    def _getGfxMentorData(self):
        p = BigWorld.player()
        mData = {'tabIdx': self.tabIdx,
         'hasMentor': True,
         'hasApprentice': True}
        hasApprenticeTarget = bool(gameglobal.rds.configData.get('enableApprenticeTarget') and p.apprenticeInfo)
        mData['hasApprenticeTarget'] = hasApprenticeTarget
        return uiUtils.dict2GfxDict(mData, True)

    def _getInfoByGbId(self, gbId):
        p = BigWorld.player()
        if gbId == p.gbId:
            photoBorderIcon40 = p.getPhotoBorderIcon(p.photoBorder.borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
            photoBorderIcon108 = p.getPhotoBorderIcon(p.photoBorder.borderId, uiConst.PHOTO_BORDER_ICON_SIZE108)
            return {'name': p.realRoleName,
             'gbId': str(gbId),
             'school': p.school,
             'sex': p.physique.sex,
             'lv': p.lv,
             'sexTxt': const.SEX_NAME.get(p.physique.sex),
             'online': True,
             'onlineTxt': gameStrings.TEXT_FRIENDPROXY_293_1,
             'headIcon': p._getFriendPhoto(p),
             'schoolTxt': const.SCHOOL_DICT.get(p.school),
             'guild': p.guildName if p.guildName else gameStrings.TEXT_MENTOREXPROXY_711,
             'state': 0,
             'photoBorderIcon40': photoBorderIcon40,
             'photoBorderIcon108': photoBorderIcon108}
        friendVal = p.friend.get(gbId)
        if friendVal:
            guildName = ''
            online = friendVal.state in gametypes.FRIEND_VISIBLE_STATES
            if self.getExtraInfos.has_key(gbId):
                extraInfo = self.getExtraInfos.get(gbId, (0, 0, '', 0, ''))
                online = extraInfo[3] == 0
                guildName = extraInfo[2]
            photoBorderIcon40 = p.getPhotoBorderIcon(friendVal.borderId, uiConst.PHOTO_BORDER_ICON_SIZE40)
            photoBorderIcon108 = p.getPhotoBorderIcon(friendVal.borderId, uiConst.PHOTO_BORDER_ICON_SIZE108)
            return {'name': friendVal.name,
             'gbId': str(gbId),
             'school': friendVal.school,
             'sex': friendVal.sex,
             'lv': friendVal.level,
             'online': online,
             'headIcon': p._getFriendPhoto(friendVal),
             'onlineTxt': gameStrings.TEXT_FRIENDPROXY_293_1 if online else gameStrings.TEXT_UIUTILS_1414,
             'sexTxt': const.SEX_NAME.get(friendVal.sex),
             'schoolTxt': const.SCHOOL_DICT.get(friendVal.school),
             'guild': guildName if guildName else gameStrings.TEXT_MENTOREXPROXY_711,
             'apprenticeVal': p.apprenticeVal.get(gbId, 0),
             'state': 0,
             'photoBorderIcon40': photoBorderIcon40,
             'photoBorderIcon108': photoBorderIcon108}
        return {}

    def _checkCanOpen(self):
        p = BigWorld.player()
        return p.enableNewApprentice()

    def onSelSoleApprentice(self, gbId, roleName):
        self.applySoleApprenticeEx(gbId)

    @ui.checkInventoryLock()
    def applySoleApprenticeEx(self, gbId):
        BigWorld.player().base.applySoleApprenticeEx(gbId, BigWorld.player().cipherOfPerson)

    @ui.checkInventoryLock()
    def applySoleDismissEx(self, gbId):
        p = BigWorld.player()
        p.base.applySoleDismissEx(gbId, p.cipherOfPerson)

    @ui.checkInventoryLock()
    def applySoleMentorEx(self, gbId):
        p = BigWorld.player()
        p.base.applySoleMentorEx(gbId, p.cipherOfPerson)

    def onApplySoleMentorEx(self, apprenticeGbId, apprenticeName):
        pushData = {'data': (apprenticeGbId, apprenticeName)}
        if not self.uiAdapter.pushMessage.hasPushData(uiConst.MESSAGE_TYPE_APPLY_SOLE_MENTOR, pushData):
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_APPLY_SOLE_MENTOR, pushData)

    def onApplySoleApprenticeEx(self, mentorGbId, mentorName):
        pushData = {'data': (mentorGbId, mentorName)}
        if not self.uiAdapter.pushMessage.hasPushData(uiConst.MESSAGE_TYPE_APPLY_SOLE_APPRENTICE, pushData):
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_APPLY_SOLE_APPRENTICE, pushData)

    def onApplySoleDismissEx(self, gbId, name):
        pushData = {'data': (gbId, name)}
        if not self.uiAdapter.pushMessage.hasPushData(uiConst.MESSAGE_TYPE_DISMISS_SOLE, pushData):
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_DISMISS_SOLE, pushData)

    def onApplySoleClick(self, msgType):
        data = self.uiAdapter.pushMessage.getLastData(msgType)
        if not data:
            return
        self.uiAdapter.pushMessage.removeData(msgType, data)
        gbId, name = data.get('data', (0, ''))
        p = BigWorld.player()
        if msgType == uiConst.MESSAGE_TYPE_APPLY_SOLE_MENTOR:
            msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_APPLY_SOLE_MENTOR_MSG, '%s') % name
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(p.base.applySoleMentorConfirmedEx, gbId, 1), noCallback=Functor(p.base.applySoleMentorConfirmedEx, gbId, 0), noBtnText=gameStrings.TEXT_IMPSHUANGXIU_26)
        elif msgType == uiConst.MESSAGE_TYPE_APPLY_SOLE_APPRENTICE:
            msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_APPLY_SOLE_APPRENTICE_MSG, '%s') % name
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(p.base.applySoleApprenticeConfirmedEx, gbId, 1), noCallback=Functor(p.base.applySoleApprenticeConfirmedEx, gbId, 0), noBtnText=gameStrings.TEXT_IMPSHUANGXIU_26)
        elif msgType == uiConst.MESSAGE_TYPE_DISMISS_SOLE:
            msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_DISMISS_SOLE_MSG, '%s') % name
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(p.base.applySoleDismissConfirmedEx, gbId, 1), noCallback=Functor(p.base.applySoleDismissConfirmedEx, gbId, 0), noBtnText=gameStrings.TEXT_IMPSHUANGXIU_26)

    def onGetGraduateRemarkByGbIdEx(self, gbId, res):
        self.hideRemarksWidget()
        self.remarks = res
        if self.remarks:
            self.uiAdapter.loadWidget(uiConst.WIDGET_APPRENTICE_REMARK)
        else:
            BigWorld.player().showGameMsg(GMDD.data.APPRENTICE_GRADUATE_REMARKS_EMPTY, ())

    def enableApprenticeQulificationEx(self):
        if not self.uiAdapter.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_APPRENTICE_QULIFICATION_EX):
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_APPRENTICE_QULIFICATION_EX)

    def onClickApprenticeQulificationEx(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_APPRENTICE_QULIFICATION_EX)
        msg = uiUtils.getTextFromGMD(GMDD.data.APPRENTICE_QULIFICATION_EX_MSG)
        self.uiAdapter.messageBox.showMsgBox(msg, Functor(self.show, 1))

    def enableMentorQulificationEx(self):
        if not self.uiAdapter.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_MENTOR_QULIFICATION_EX):
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_MENTOR_QULIFICATION_EX)

    def onClickMentorQulificationEx(self):
        self.show(TAB_FIND_APPRENTICE)
        self.uiAdapter.mentor.showCertification()

    def onSetBeMentorSloganEx(self, slogan):
        self.lastSloganMsg[OP_APPRENTICE] = slogan

    def onSetBeApprenticeSloganEx(self, slogan):
        self.lastSloganMsg[OP_MENTOR] = slogan

    def sendApprenticePreferenceInfo(self, mentorPreferenceInfo, apprenticePreferenceInfo):
        if mentorPreferenceInfo:
            self.mentorPreferenceInfo = mentorPreferenceInfo
        if apprenticePreferenceInfo:
            self.apprenticePreferenceInfo = apprenticePreferenceInfo
        if self.mediator:
            currentView = asObject.ASObject(self.mediator.Invoke('getCurrentView'))
            currentView.refreshView()

    def _getCurrentSettingPreference(self):
        info = {}
        if self.mediator:
            currentView = asObject.ASObject(self.mediator.Invoke('getCurrentView'))
            info['slogan'] = unicode2gbk(currentView.slogonInput.gfxVal.GetMember('text').GetString())
            info['sex'] = currentView.sexDropMenu.selectedIndex
            schools = []
            for school in const.SCHOOL_SET:
                btn = currentView.getChildByName('school%s' % school)
                if btn and btn.selected:
                    schools.append(school)

            info['school'] = schools
            lvs = []
            for x in xrange(6):
                btn = currentView.getChildByName('lv%s' % x)
                if btn and btn.selected:
                    lvs.append(x)

            info['lv'] = lvs
            info['sameCity'] = int(currentView.isSameCity.selected)
        return info

    @ui.checkInventoryLock()
    def apprenticeGrowthLevelRewardApply(self, npc, funcType):
        p = BigWorld.player()
        if funcType == npcConst.NPC_FUNC_APPRENTICE_GROWTH_LEVEL_REWARD_APPLY:
            npc.cell.apprenticeGrowthLevelRewardApply(p.cipherOfPerson)
        elif funcType == npcConst.NPC_FUNC_APPRENTICE_GROWTH_GRADUATE_REWARD_APPLY:
            npc.cell.apprenticeGrowthGraduateRewardApply(p.cipherOfPerson)

    def apprenticeGrowthRewardQuery(self):
        BigWorld.player().base.queryApprenticeGrowthFeedBack()

    def initTargetPanel(self):
        p = BigWorld.player()
        maxMentorNum = ANCD.data.get('maxMentorNum', 3)
        self.targetPanel.targetDesc.htmlText = ANCD.data.get('targetDesc', '')
        self.targetPanel.chatToMentor.addEventListener(events.BUTTON_CLICK, self.handleChatToMentor)
        for x in xrange(maxMentorNum):
            btn = self.targetPanel.getChildByName('mentor%s' % x)
            btn.gotoAndStop('type%d' % int(x < len(p.apprenticeInfo)))
            if x < len(p.apprenticeInfo):
                mentorBtn = btn.btn
                gbId = p.apprenticeInfo.keys()[x]
                mentorInfo = self._getInfoByGbId(gbId)
                mentorBtn.label = mentorInfo.get('name')
                mentorBtn.schoolTxt.text = '%s Lv%s' % (mentorInfo.get('schoolTxt'), mentorInfo.get('lv'))
                mentorBtn.onlineIcon.gotoAndStop('type%s' % int(mentorInfo.get('online', 0)))
                mentorBtn.gbId = gbId
                mentorBtn.addEventListener(events.BUTTON_CLICK, self.handleTargetMentorSelect)
                if x == 0:
                    self.setTargetMentorBtnSelect(mentorBtn)
                mentorBtn.validateNow()
                mentorBtn.mouseChildren = True
                TipManager.addTip(mentorBtn.onlineIcon, mentorInfo.get('onlineTxt'))
            else:
                btn.addBtn.addEventListener(events.BUTTON_CLICK, self.handleGotoFindMentor)

    def handleTargetMentorSelect(self, *args):
        targetBtn = asObject.ASObject(args[3][0]).currentTarget
        if targetBtn.selected:
            return
        self.setTargetMentorBtnSelect(targetBtn)

    def setTargetMentorBtnSelect(self, mentorBtn):
        for x in xrange(ANCD.data.get('maxMentorNum', 3)):
            btn = self.targetPanel.getChildByName('mentor%s' % x)
            if btn.btn:
                btn.btn.selected = btn.btn == mentorBtn

        self.initTargetView(long(mentorBtn.gbId))

    def initTargetView(self, gbId):
        self.targetPanel.currentId = gbId
        val = self._getInfoByGbId(gbId)
        p = BigWorld.player()
        targets = getattr(p, 'apprenticeTargets', {}).get(long(gbId), ({}, False, 0))[0]
        targets = sorted(targets.items(), key=lambda x: x[1])
        if not targets:
            self.targetPanel.targetTitleDesc.text = ANCD.data.get('noTargetTitleDesc', '')
        else:
            self.targetPanel.targetTitleDesc.text = ANCD.data.get('targetTitleDesc', '%s %s') % (val.get('name'), len(targets))
        for x in xrange(MAX_TARGET_NUM):
            mc = self.targetPanel.getChildByName('item%s' % x)
            mc.visible = x < len(targets)
            if x < len(targets):
                self.initTargetItem(mc, targets[x])

    def initTargetItem(self, mc, data):
        targetId, finished = data
        targetData = ATD.data.get(targetId, {})
        mc.focusable = False
        mc.validateNow()
        mc.mouseChildren = True
        mc.label = targetData.get('name')
        mc.desc.htmlText = targetData.get('desc')
        mc.item.setItemSlotData(uiUtils.getGfxItemById(int(targetData.get('itemId', 0))))
        mc.stateIcon.visible = finished
        mc.btn.visible = not finished
        if not finished:
            action = targetData.get('itemAction')
            if action:
                mc.btn.label = action[2]
                mc.btn.data = action
                mc.btn.addEventListener(events.BUTTON_CLICK, self.handleTargetAction)
            else:
                mc.btn.visible = False

    def handleTargetAction(self, *args):
        aType, param, _ = asObject.ASObject(args[3][0]).currentTarget.data
        if aType == TARGET_ACTION_SEEK:
            uiUtils.findPosById(param)
        elif aType == TARGET_ACTION_SHOW_HELP:
            self.uiAdapter.help.show(param)

    def handleGotoFindMentor(self, *args):
        self.targetPanel.gotoTab(1)

    def handleChatToMentor(self, *args):
        fid = long(self.targetPanel.currentId)
        p = BigWorld.player()
        fVal = p.getFValByGbId(fid)
        if not self.uiAdapter.chatToFriend.isShowed(fid):
            self.uiAdapter.chatToFriend.show(None, p._createFriendData(fVal), False)
        else:
            self.uiAdapter.chatToFriend.swapPanelToFront(fid)
