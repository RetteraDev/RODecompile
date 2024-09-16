#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mentorProxy.o
from gamestrings import gameStrings
import BigWorld
import const
import uiConst
import uiUtils
import gameglobal
import events
import ui
import utils
import gametypes
from ui import unicode2gbk
from uiProxy import UIProxy
from data import apprentice_config_data as ACD
from data import friend_location_data as FLD
from data import fame_data as FD
from cdata import game_msg_def_data as GMDD

class MentorProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MentorProxy, self).__init__(uiAdapter)
        self.modelMap = {'showInfo': self.onShowInfo,
         'agreeApply': self.onAgreeApply,
         'rejectApply': self.onRejectApply,
         'showTitleList': self.onShowTitleList,
         'selectTitle': self.onSelectTilte,
         'getRecommendApprentices': self.onGetRecommendApprentices,
         'getRecommendMentors': self.onGetRecommendMentors}
        uiAdapter.registerEscFunc(uiConst.WIDGET_MENTOR_LETTER, self.hideLetter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_MENTOR_CERTIFICATION, self.hideCertification)
        uiAdapter.registerEscFunc(uiConst.WIDGET_MENTOR_TITLE_LIST, self.hideTitleList)
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MENTOR_LETTER:
            self.letterMed = mediator
            initData = {'type': self.letterType}
            pushType = None
            content = ''
            if self.letterType == uiConst.MENTOR_LETTER_BAISHI:
                pushType = uiConst.MESSAGE_TYPE_BE_MENTOR
                content = uiUtils.getTextFromGMD(GMDD.data.BAI_SHI_MESSAGE)
            elif self.letterType == uiConst.MENTOR_LETTER_SHOUTU:
                pushType = uiConst.MESSAGE_TYPE_BE_APPRENTICE
                content = content = uiUtils.getTextFromGMD(GMDD.data.SHOU_TU_MESSAGE)
            else:
                initData['content'] = uiUtils.getTextFromGMD(GMDD.data.CHU_SHI_MESSAGE)
            if pushType:
                pushData = self.uiAdapter.pushMessage.getLastData(pushType)
                applyData = pushData.get('data')
                if applyData:
                    if content:
                        initData['content'] = content % applyData.get('name', '')
                    initData['name'] = applyData.get('name', '')
                    initData['htmlName'] = '<u>%s</u>' % uiUtils.toHtml(initData['name'], '#217aa6')
                    initData['gender'] = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_303 % const.SEX_NAME.get(applyData.get('sex', 1), '')
                    initData['school'] = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_351 % const.SCHOOL_DICT.get(applyData.get('school', 0), '')
                    initData['lvl'] = gameStrings.TEXT_MENTORPROXY_67 % applyData.get('lv', '')
                    initData['guild'] = gameStrings.TEXT_MENTORPROXY_68 % applyData.get('guild', gameStrings.TEXT_BATTLEFIELDPROXY_1605)
                    initData['desc'] = gameStrings.TEXT_MENTORPROXY_69 % applyData.get('desc', '')
                    initData['gbId'] = str(applyData.get('gbId', ''))
            return uiUtils.dict2GfxDict(initData, True)
        elif widgetId == uiConst.WIDGET_MENTOR_CERTIFICATION:
            initData = {'content': uiUtils.getTextFromGMD(GMDD.data.SHOUYE_ZHIGE_RENZHENG)}
            return uiUtils.dict2GfxDict(initData, True)
        elif widgetId == uiConst.WIDGET_MENTOR_TITLE_LIST:
            titleData = {'selectedId': BigWorld.player().apprenticeTitleMentor}
            titleList = ACD.data.get('apprenticeTitleList', {})
            data = []
            for id, info in titleList.items():
                data.append({'id': id,
                 'label': info.get('name', ''),
                 'titleName': '%s&%s' % (info.get('mentor', ''), info.get('apprentice', ''))})

            titleData['titleList'] = data
            return uiUtils.dict2GfxDict(titleData, True)
        else:
            return

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_MENTOR_LETTER:
            self.hideLetter()
        elif widgetId == uiConst.WIDGET_MENTOR_CERTIFICATION:
            self.hideCertification()
        elif widgetId == uiConst.WIDGET_MENTOR_TITLE_LIST:
            self.hideTitleList()

    def show(self, *args):
        pass

    def showMentorLetter(self, type):
        if self._checkCanOpen():
            self.hideLetter()
            self.uiAdapter.loadWidget(uiConst.WIDGET_MENTOR_LETTER)
            self.letterType = type

    def showCertification(self):
        if self._checkCanOpen():
            self.hideCertification()
            self.uiAdapter.loadWidget(uiConst.WIDGET_MENTOR_CERTIFICATION)

    def dismissRelation(self, gbId):
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_DISMISS_MENTOR_RELATION, {'data': gbId})

    def showDismissMsg(self):
        pushData = self.uiAdapter.pushMessage.getLastData(uiConst.MESSAGE_TYPE_DISMISS_MENTOR_RELATION)
        if pushData:
            gbId = pushData.get('data', '')
            name = ''
            info = self._getInfoByGbId(gbId)
            if info:
                name = info.get('name', '')
            msg = uiUtils.getTextFromGMD(GMDD.data.DISMISS_MENTOR_RELATION) % utils.getDisplayName(name)
            self.uiAdapter.messageBox.showAlertBox(msg)
            self.uiAdapter.pushMessage.removeLastData(uiConst.MESSAGE_TYPE_DISMISS_MENTOR_RELATION)

    def clearWidget(self):
        self.hideCertification()
        self.hideLetter()

    def reset(self):
        self.mediator = None
        self.letterMed = None
        self.letterType = 0
        self.recommendType = 0
        self.recommendRes = None

    def hideLetter(self):
        self.letterMed = None
        self.letterType = 0
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MENTOR_LETTER)

    def hideCertification(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MENTOR_CERTIFICATION)

    def hideTitleList(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MENTOR_TITLE_LIST)

    def onShowInfo(self, *args):
        gbId = int(args[3][0].GetString())
        if BigWorld.player().gbId == gbId:
            self.uiAdapter.friend.showProfile()
        else:
            self.uiAdapter.friend.viewFriendProfile(gbId)

    def onAgreeApply(self, *args):
        name = unicode2gbk(args[3][0].GetString())
        p = BigWorld.player()
        if self.letterType == uiConst.MENTOR_LETTER_BAISHI:
            if p.enableNewApprentice():
                p.base.onApplyMentorConfirmedEx(name, True)
            else:
                p.base.onApplyMentorConfirmed(name, True)
            self.uiAdapter.pushMessage.removeLastData(uiConst.MESSAGE_TYPE_BE_MENTOR)
        elif self.letterType == uiConst.MENTOR_LETTER_SHOUTU:
            if p.enableNewApprentice():
                p.base.onApplyApprenticeConfirmedEx(name, True)
            else:
                p.cell.onApplyApprenticeConfirmed(name, True)
            self.uiAdapter.pushMessage.removeLastData(uiConst.MESSAGE_TYPE_BE_APPRENTICE)
        self.hideLetter()

    def onRejectApply(self, *args):
        name = args[3][0].GetString()
        name = unicode2gbk(name)
        p = BigWorld.player()
        if self.letterType == uiConst.MENTOR_LETTER_BAISHI:
            if p.enableNewApprentice():
                p.base.onApplyMentorConfirmedEx(name, False)
            else:
                p.base.onApplyMentorConfirmed(name, False)
            self.uiAdapter.pushMessage.removeLastData(uiConst.MESSAGE_TYPE_BE_MENTOR)
        elif self.letterType == uiConst.MENTOR_LETTER_SHOUTU:
            if p.enableNewApprentice:
                p.base.onApplyApprenticeConfirmedEx(name, False)
            else:
                p.cell.onApplyApprenticeConfirmed(name, False)
            self.uiAdapter.pushMessage.removeLastData(uiConst.MESSAGE_TYPE_BE_APPRENTICE)
        self.hideLetter()

    def onShowTitleList(self, *args):
        self.uiAdapter.loadWidget(uiConst.WIDGET_MENTOR_TITLE_LIST)

    def onSelectTilte(self, *args):
        id = int(args[3][0].GetNumber())
        self.hideTitleList()
        BigWorld.player().base.setMentorTitle(id)

    @ui.callFilter(5, True)
    def onGetRecommendApprentices(self, *args):
        if BigWorld.player():
            BigWorld.player().cell.getRecommendApprentices()

    @ui.callFilter(5, True)
    def onGetRecommendMentors(self, *args):
        if BigWorld.player():
            BigWorld.player().cell.getRecommendMentors()

    def _getInfoByGbId(self, gbId):
        p = BigWorld.player()
        if gbId == p.gbId:
            return {'name': p.realRoleName,
             'gbId': str(gbId),
             'school': p.school,
             'sex': p.physique.sex,
             'lv': p.lv,
             'schoolName': uiConst.SCHOOL_FRAME_DESC.get(p.school, '')}
        friendVal = p.friend.get(gbId)
        if friendVal:
            return {'name': friendVal.name,
             'gbId': str(gbId),
             'school': friendVal.school,
             'sex': friendVal.sex,
             'lv': friendVal.level,
             'schoolName': uiConst.SCHOOL_FRAME_DESC.get(friendVal.school, '')}

    def _checkCanOpen(self):
        return self.enableApprentice() or BigWorld.player().enableNewApprentice()

    def enableApprentice(self):
        return gameglobal.rds.configData.get('enableApprentice', False)

    def enableApprenticePool(self):
        return gameglobal.rds.configData.get('enableApprenticePool', False)
