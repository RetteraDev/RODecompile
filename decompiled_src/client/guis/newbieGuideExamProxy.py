#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newbieGuideExamProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import gametypes
from uiProxy import UIProxy
from callbackHelper import Functor
from data import novice_boost_score_type_data as NBSTD
from data import novice_boost_score_condition_data as NBSCD
from cdata import game_msg_def_data as GMDD

class NewbieGuideExamProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewbieGuideExamProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.typeId = 0
        self.resInfo = {}
        self.selfFlag = True
        self.otherTypeId = 0
        self.otherInfo = {}
        self.otherLv = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_NEWBIE_GUIDE_EXAM, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_NEWBIE_GUIDE_EXAM:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NEWBIE_GUIDE_EXAM)

    def reset(self):
        self.typeId = 0

    def show(self, typeId):
        self.typeId = typeId
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NEWBIE_GUIDE_EXAM)

    def setInfo(self, resInfo):
        self.resInfo = resInfo

    def getResInfo(self):
        return self.resInfo

    def setOtherType(self, otherTypeId):
        self.otherTypeId = otherTypeId

    def showOther(self, otherInfo, level):
        self.selfFlag = False
        self.otherInfo = otherInfo
        self.otherLv = level
        self.show(self.otherTypeId)

    def refreshInfo(self):
        if self.mediator:
            if self.selfFlag:
                examInfo = self.resInfo.get(self.typeId, {})
            else:
                examInfo = self.otherInfo.get(self.typeId, {})
            info = {}
            baseData = NBSTD.data.get(self.typeId, {})
            maxLv = baseData.get('maxLv', 0) - 1
            info['nameTitle'] = baseData.get('topic', '')
            curScore = examInfo.get('score', 0)
            info['curScore'] = format(curScore, ',')
            score = baseData.get('score', 0)
            fineScore = baseData.get('fineScore', 1)
            currentValue = 100.0
            if fineScore >= curScore:
                currentValue = currentValue * curScore / fineScore
            info['progressBarText'] = '%s/%s' % (format(curScore, ','), format(fineScore, ','))
            info['currentValue'] = currentValue
            info['bonus'] = uiUtils.getGfxItemById(baseData.get('scoreIcon', 0))
            info['bonusPos'] = 1.0 * score / fineScore
            info['fineBonus'] = uiUtils.getGfxItemById(baseData.get('fineScoreIcon', 0))
            info['fineBonusPos'] = 1.0
            graduateState = examInfo.get('graduateState', 0)
            if graduateState == gametypes.NOVICE_TYPE_GRADUATE_NONE:
                if maxLv < BigWorld.player().realLv:
                    info['btnLabel'] = gameStrings.TEXT_NEWBIEGUIDEEXAMPROXY_100
                    info['bonusState'] = 'waitFinish'
                    info['fineBonusState'] = 'waitFinish'
                else:
                    info['btnLabel'] = gameStrings.TEXT_NEWBIEGUIDEEXAMPROXY_104
                    info['bonusState'] = 'going'
                    info['fineBonusState'] = 'going'
            elif graduateState == gametypes.NOVICE_TYPE_GRADUATE_DONE:
                info['btnLabel'] = gameStrings.TEXT_NEWBIEGUIDEEXAMPROXY_108
                info['bonusState'] = 'get'
                info['fineBonusState'] = 'finish'
            elif graduateState == gametypes.NOVICE_TYPE_GRADUATE_PERFECT:
                info['btnLabel'] = gameStrings.TEXT_NEWBIEGUIDEEXAMPROXY_112
                info['bonusState'] = 'get'
                info['fineBonusState'] = 'get'
            elif graduateState == gametypes.NOVICE_TYPE_GRADUATE_FAIL:
                info['btnLabel'] = gameStrings.TEXT_NEWBIEGUIDEEXAMPROXY_116
                info['bonusState'] = 'finish'
                info['fineBonusState'] = 'finish'
            btnEnabled = graduateState == gametypes.NOVICE_TYPE_GRADUATE_NONE
            info['hint'] = uiUtils.getTextFromGMD(GMDD.data.NEWBIE_GUIDE_EXAM_HINT, '%d') % maxLv
            finishedAchievements = examInfo.get('finishedAchievements', [])
            curMustNum = 0
            allMustNum = 0
            mustList = []
            optionalList = []
            for value in NBSCD.data.itervalues():
                if value.get('type', 0) != self.typeId:
                    continue
                if not value.get('optional', 0):
                    allMustNum += 1
                    if value.get('id', 0) in finishedAchievements:
                        curMustNum += 1
                    else:
                        btnEnabled = False
                itemInfo = {}
                itemInfo['state'] = 'finish' if value.get('id', 0) in finishedAchievements else 'going'
                itemInfo['title'] = value.get('title', '')
                itemInfo['desc'] = value.get('desc', '')
                itemInfo['score'] = gameStrings.TEXT_NEWBIEGUIDEEXAMPROXY_142 % format(value.get('score', 0), ',')
                itemInfo['sortId'] = value.get('sortId', 0)
                if value.get('optional', 0):
                    optionalList.append(itemInfo)
                else:
                    mustList.append(itemInfo)

            if curMustNum < allMustNum:
                info['curMust'] = gameStrings.TEXT_NEWBIEGUIDEEXAMPROXY_150 % (curMustNum, allMustNum)
            else:
                info['curMust'] = gameStrings.TEXT_NEWBIEGUIDEEXAMPROXY_152 % (curMustNum, allMustNum)
            mustList.sort(key=lambda x: x['sortId'], reverse=False)
            optionalList.sort(key=lambda x: x['sortId'], reverse=False)
            info['mustList'] = mustList
            info['optionalList'] = optionalList
            if graduateState == gametypes.NOVICE_TYPE_GRADUATE_NONE and maxLv < BigWorld.player().realLv:
                info['btnEnabled'] = True
            else:
                if btnEnabled:
                    btnEnabled = curScore >= score
                if btnEnabled:
                    info['bonusState'] = 'reach'
                    if curScore >= fineScore:
                        info['fineBonusState'] = 'reach'
                info['btnEnabled'] = btnEnabled
            info['btnVisible'] = self.selfFlag
            if self.selfFlag:
                info['greyVisible'] = maxLv < BigWorld.player().realLv
            else:
                info['greyVisible'] = maxLv < self.otherLv
            self.selfFlag = True
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def checkCanFinish(self, typeId):
        examInfo = self.resInfo.get(typeId, {})
        baseData = NBSTD.data.get(typeId, {})
        maxLv = baseData.get('maxLv', 0) - 1
        curScore = examInfo.get('score', 0)
        score = baseData.get('score', 0)
        graduateState = examInfo.get('graduateState', 0)
        btnEnabled = graduateState == gametypes.NOVICE_TYPE_GRADUATE_NONE
        finishedAchievements = examInfo.get('finishedAchievements', [])
        for value in NBSCD.data.itervalues():
            if value.get('type', 0) != typeId:
                continue
            if not value.get('optional', 0):
                if value.get('id', 0) not in finishedAchievements:
                    btnEnabled = False

        if graduateState == gametypes.NOVICE_TYPE_GRADUATE_NONE and maxLv < BigWorld.player().realLv:
            btnEnabled = True
        elif btnEnabled:
            btnEnabled = curScore >= score
        return btnEnabled

    def onConfirm(self, *arg):
        p = BigWorld.player()
        examInfo = self.resInfo.get(self.typeId, {})
        baseData = NBSTD.data.get(self.typeId, {})
        if baseData.get('maxLv', 0) > p.realLv and examInfo.get('score', 0) < baseData.get('fineScore', 0):
            msg = uiUtils.getTextFromGMD(GMDD.data.NEWBIE_GUIDE_EXAM_APPLY_HINT, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.applyNoviceLevelUpAndAward, self.typeId))
        else:
            p.cell.applyNoviceLevelUpAndAward(self.typeId)

    def needNotExam(self, typeId):
        return NBSTD.data.get(typeId, {}).get('maxLv', 0) <= BigWorld.player().realLv

    def fineFinishExam(self, typeId):
        return self.resInfo.get(typeId, {}).get('graduateState', 0) == gametypes.NOVICE_TYPE_GRADUATE_PERFECT

    def finishExam(self, typeId):
        return self.resInfo.get(typeId, {}).get('graduateState', 0) == gametypes.NOVICE_TYPE_GRADUATE_DONE

    def failExam(self, typeId):
        return self.resInfo.get(typeId, {}).get('graduateState', 0) == gametypes.NOVICE_TYPE_GRADUATE_FAIL
