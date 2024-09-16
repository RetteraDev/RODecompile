#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/flyUpChallengeProxy.o
import BigWorld
import gameglobal
import const
from uiProxy import UIProxy
from helpers import flyUpHelper
from guis import events
from guis.asObject import ASObject
from data import fly_up_challenge_data as FUCD
from data import fly_up_exp_data as FUED
from data import quest_data as QD
from gamestrings import gameStrings
TAB_NUM = 8

class FlyUpChallengeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FlyUpChallengeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currentSection = 0
        self.currentChapter = 0

    def reset(self):
        self.currentSection = 0
        self.currentChapter = 0

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.lvUpBtn.addEventListener(events.BUTTON_CLICK, self.onButtonClick, False, 0, True)
        self.widget.detailMc.goChallengeBtn.addEventListener(events.BUTTON_CLICK, self.onButtonClick, False, 0, True)

    def onButtonClick(self, *args):
        e = ASObject(args[3][0])
        btnName = e.currentTarget.name
        if btnName == 'lvUpBtn':
            flyUpHelper.getInstance().flyUpLvUp()
        elif btnName == 'goChallengeBtn':
            gameglobal.rds.ui.questLog.showTaskLog()

    def refreshInfo(self):
        if not self.widget:
            return
        sectionInfo = flyUpHelper.getInstance().getPlayerFlyUpInfo()
        self.widget.progress.maxValue = sectionInfo.get('exp', 0)
        self.widget.progress.currentValue = sectionInfo.get('totalExp', 0)
        self.widget.lvText.text = sectionInfo.get('flyDec', '')
        self.refreshCahpterInfo()

    def refreshCahpterInfo(self):
        chapters = []
        p = BigWorld.player()
        for flyLv in FUCD.data.keys():
            if flyLv % const.SUB_FLYUP_NUM == 1:
                sectionInfo = FUCD.data.get(flyLv)
                exInfo = FUED.data.get(flyLv)
                chapterInfo = {'name': sectionInfo.get('mainQuestName', ''),
                 'lv': exInfo.get('lv', 0),
                 'isOpen': flyLv <= p.flyUpLv + 1,
                 'isFinish': flyLv + const.SUB_FLYUP_NUM <= p.flyUpLv}
                chapters.append(chapterInfo)

        for i in xrange(TAB_NUM):
            chapterInfo = chapters[i]
            tabMc = self.widget.getChildByName('tab%d' % i)
            requireText = ''
            if not chapterInfo.get('isOpen', False):
                if p.lv < chapterInfo.get('lv', 0):
                    requireText = gameStrings.FLAY_UP_LV_REQ_TEXT % chapterInfo.get('lv', 0)
                else:
                    requireText = gameStrings.FLAY_UP_REQ_TEXT
            tabMc.labels = [requireText, chapterInfo.get('name', '')]
            tabMc.finishFlag.visible = chapterInfo.get('isFinish', False)
            tabMc.selected = self.currentChapter == i
            tabMc.index = i
            tabMc.addEventListener(events.BUTTON_CLICK, self.onTabBtnClick, False, 0, True)

        self.refreshSections()

    def onTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        index = e.currentTarget.index
        self.currentChapter = index
        for i in xrange(TAB_NUM):
            tabMc = self.widget.getChildByName('tab%d' % i)
            if index != i:
                tabMc.selected = False
            else:
                tabMc.selected = True

        self.refreshSections()

    def refreshSections(self):
        chapterIndex = self.currentChapter
        p = BigWorld.player()
        startLv = chapterIndex * const.SUB_FLYUP_NUM
        currentLv = p.flyUpLv
        self.currentSection = 0
        for i in xrange(const.SUB_FLYUP_NUM):
            flyLv = startLv + i + 1
            sectionMc = self.widget.detailMc.getChildByName('section%d' % i)
            sectionInfo = FUCD.data.get(flyLv, {})
            sectionMc.label = sectionInfo.get('subQuestName', '')
            isFinish = flyLv <= currentLv or flyUpHelper.getInstance().isChallengeFinished(flyLv)
            isLocked = p.lv <= sectionInfo.get('lv', 0) or flyLv > currentLv + 1
            sectionMc.finishFlag.visible = isFinish
            sectionMc.lockMc.visible = isLocked
            if i == self.currentSection:
                sectionMc.selected = True
            sectionMc.index = i
            sectionMc.addEventListener(events.BUTTON_CLICK, self.onSectionClick, False, 0, True)

        self.refreshChallengeInfo()

    def onSectionClick(self, *args):
        e = ASObject(args[3][0])
        index = e.currentTarget.index
        self.currentSection = index
        self.refreshChallengeInfo()

    def refreshChallengeInfo(self):
        flyLv = self.currentChapter * const.SUB_FLYUP_NUM + self.currentSection + 1
        challengeInfo = flyUpHelper.getInstance().getFlyUpChallengeInfo(flyLv)
        self.widget.detailMc.tipText.text = challengeInfo.get('resultDesc', '')
        self.widget.detailMc.bonusText.text = challengeInfo.get('bonusInfo', '')
        self.widget.detailMc.title.text = challengeInfo.get('subQuestName', '')
        currentQuest = challengeInfo.get('currentQuest', 0)
        questInfo = QD.data.get(currentQuest, {})
        self.widget.detailMc.desc.text = questInfo.get('desc', '')
        p = BigWorld.player()
        if not flyUpHelper.getInstance().isChallengeFinished(flyLv):
            self.widget.detailMc.goChallengeBtn.visible = False
            self.widget.detailMc.overtext.visible = flyLv == p.flyUpLv + 1
            self.widget.detailMc.overtext.text = gameStrings.FLY_UP_FINISH_TEXT
        else:
            self.widget.detailMc.goChallengeBtn.visible = True
            self.widget.detailMc.overtext.visible = False
