#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/createTeamV2Proxy.o
import BigWorld
import copy
import gameglobal
import uiConst
import const
import events
import gametypes
import utils
from helpers import taboo
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import groupDetailFactory
from guis import richTextUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.teamGoalMenuHelper import TeamGoalMenuHelper
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import group_label_data as GLD
SCHOOL_CHECK_BOX_START_POS = (35, 288)
SCHOOL_CHECK_BOX_ROW_NUM = 5
SCHOOL_CHECK_BOX_ROW_OFFSET = 84
SCHOOL_CHECK_BOX_COLUMN_OFFSET = 35
MAX_HOTLABEL_CNT = 8

class CreateTeamV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CreateTeamV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.actTypeData = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CREATE_TEAM_V2, self.hide)

    def reset(self):
        self.teamGoalMenu = None
        self.schoolMcs = list()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CREATE_TEAM_V2:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CREATE_TEAM_V2)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CREATE_TEAM_V2)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.addEvent(events.EVENT_TEAM_GOAL_CHANGED, self.onTeamGoalChanged)
        self.addEvent(events.EVENT_CHANGE_GROUP_HEADER, self.onTeamHeaderChanged)
        self.initSchoolCheckBox()
        self.initHotLabel()
        self.initTeamGoal()
        self.initRestrictDetail()
        self.initShareInfo()

    def initSchoolCheckBox(self):
        self.schoolMcs = list()
        idx = 0
        for school in const.ALL_SCHOOLS:
            schoolCheckBoxMc = self.widget.getInstByClsName('M12_DefaultCheckBoxShen')
            self.widget.addChild(schoolCheckBoxMc)
            schoolCheckBoxMc.label = const.SCHOOL_DICT.get(school, '')
            schoolCheckBoxMc.selected = False
            schoolCheckBoxMc.name = str(school)
            row = idx // SCHOOL_CHECK_BOX_ROW_NUM
            colunm = idx % SCHOOL_CHECK_BOX_ROW_NUM
            schoolCheckBoxMc.x = SCHOOL_CHECK_BOX_START_POS[0] + SCHOOL_CHECK_BOX_ROW_OFFSET * colunm
            schoolCheckBoxMc.y = SCHOOL_CHECK_BOX_START_POS[1] + SCHOOL_CHECK_BOX_COLUMN_OFFSET * row
            idx += 1
            self.schoolMcs.append(schoolCheckBoxMc)

    def initHotLabel(self):
        labelInfo = self.getHotLabelInfo()
        hotLabelCnt = len(labelInfo)
        for i in xrange(MAX_HOTLABEL_CNT):
            hotLabel = getattr(self.widget, 'hotLabel%d' % i)
            if hotLabel is None:
                break
            if i < hotLabelCnt:
                hotLabel.label = labelInfo[i].get('name')
                hotLabel.type = labelInfo[i].get('type')
                hotLabel.index = labelInfo[i].get('index')
                hotLabel.addEventListener(events.BUTTON_CLICK, self.handleHotLabelClick, False, 0, True)
                hotLabel.visible = True
            else:
                hotLabel.visible = False

    def getHotLabelInfo(self):
        gldd = GLD.data
        ret = []
        actAvlData = groupDetailFactory.getActAvlData()
        for type, data in actAvlData.items():
            for i in range(0, len(data)):
                item = gldd.get(data[i], {})
                if item.get('hot', 0):
                    label = {}
                    label['type'] = type
                    label['index'] = i
                    label['name'] = item.get('name', '')
                    label['order'] = item.get('order', 0)
                    ret.append(label)

        ret.sort(key=lambda x: x['order'], reverse=True)
        return ret

    def initTeamGoal(self):
        self.teamGoalMenu = TeamGoalMenuHelper(self.widget.goalTypeMenu, self.widget.goal1Menu, self.widget.goal2Menu)
        self.teamGoalMenu.initTeamGoal()
        self.widget.goalTypeMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)
        self.widget.goal1Menu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)
        self.widget.goal2Menu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleGoalChange, False, 0, True)

    def initRestrictDetail(self):
        self.initLvLimit()
        self.refreshSchoolLimit()

    def initLvLimit(self):
        self.widget.minLv.textField.restrict = '0-9'
        self.widget.maxLv.textField.restrict = '0-9'
        p = BigWorld.player()
        self.widget.minLv.text = p.detailInfo.get('lvMin')
        self.widget.maxLv.text = p.detailInfo.get('lvMax')
        self.widget.minLv.addEventListener(events.EVENT_CHANGE, self.handleLvInputChange, False, 0, True)
        self.widget.maxLv.addEventListener(events.EVENT_CHANGE, self.handleLvInputChange, False, 0, True)

    def refreshLvLimit(self):
        lvMin, lvMax = self.teamGoalMenu.getGoalLvLimit()
        self.widget.minLv.text = lvMin
        self.widget.maxLv.text = lvMax

    def refreshSchoolLimit(self):
        p = BigWorld.player()
        if not hasattr(p, 'detailInfo'):
            for schoolMc in self.schoolMcs:
                schoolMc.selected = True

        else:
            schoolReqs = p.detailInfo.get('schoolReq', [])
            for schoolMc in self.schoolMcs:
                schoolMc.selected = int(schoolMc.name) in schoolReqs

    def initShareInfo(self):
        self.widget.shareContentInput.maxChars = SCD.data.get('teamShareMaxText', 20)
        self.widget.shareContentInput.text = utils.getTeamName()
        self.widget.shareContentInput.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleShareInputStateChange, False, 0, True)
        self.widget.shareContentInput.addEventListener(events.EVENT_CHANGE, self.handleShareInputChange, False, 0, True)

    def handleGoalChange(self, *args):
        self.refreshLvLimit()

    def handleShareInputChange(self, *args):
        e = ASObject(args[3][0])
        curWordCnt = e.currentTarget.textField.length
        retWordCnt = SCD.data.get('teamShareMaxText', 20) - curWordCnt
        self.widget.inputHintTf.text = gameStrings.TEAM_SHARETEXTCNT_HINT % retWordCnt

    def handleShareInputStateChange(self, *args):
        if self.widget.shareContentInput.defaultState != 'focused':
            self.widget.inputHintTf.visible = False
        else:
            self.widget.inputHintTf.visible = True
            retWordCnt = SCD.data.get('teamShareMaxText', 20) - self.widget.shareContentInput.textField.length
            self.widget.inputHintTf.text = gameStrings.TEAM_SHARETEXTCNT_HINT % retWordCnt

    def handleLvInputChange(self, *args):
        e = ASObject(args[3][0])
        inputLv = e.currentTarget.text
        if not inputLv:
            return
        inputLv = int(inputLv)
        calibrateLv = min(max(inputLv, const.MIN_CURRENT_LEVEL), const.MAX_CURRENT_LEVEL)
        e.currentTarget.text = calibrateLv

    def handleHotLabelClick(self, *args):
        e = ASObject(args[3][0])
        hotLabelBtn = e.currentTarget
        goalType = const.GROUP_GOAL_RELAXATION
        goal1Idx = hotLabelBtn.type
        goal2Idx = hotLabelBtn.index + 1
        self.teamGoalMenu.refreshTeamGoal(goalType, goal1Idx, goal2Idx)
        self.refreshLvLimit()

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        p = BigWorld.player()
        warnningId = self.getGoalWarnning()
        if warnningId:
            p.showGameMsg(warnningId, ())
            return
        info = self.getTeamGoalDetailByUI()
        BigWorld.player().setGroupDetails(info)
        self.hide()

    def _onCancelBtnClick(self, e):
        self.hide()

    def getGoalWarnning(self):
        teamName = self.widget.shareContentInput.text
        isNormal = taboo.checkDisbWordNoReplace(teamName)
        if not isNormal:
            return GMDD.data.GROUP_NAME_INVALID
        elif richTextUtils.isSysRichTxt(teamName):
            return GMDD.data.GROUP_NAME_INVALID
        lvMin = int(self.widget.minLv.text)
        lvMax = int(self.widget.maxLv.text)
        if lvMin > lvMax:
            return GMDD.data.WRONG_RANGE
        schoolReqs = self.getSchoolReqs()
        if not schoolReqs:
            return GMDD.data.TEAM_WRONG_SCHOOL_REQ
        else:
            return None

    def getTeamGoalDetailByUI(self):
        if not self.widget:
            return None
        else:
            warnningId = self.getGoalWarnning()
            if warnningId:
                return None
            teamName = self.widget.shareContentInput.text
            lvMin = int(self.widget.minLv.text)
            lvMax = int(self.widget.maxLv.text)
            schoolReqs = self.getSchoolReqs()
            extraInfo = {'teamName': teamName,
             'lvMin': lvMin,
             'lvMax': lvMax,
             'schoolReq': schoolReqs}
            return self.teamGoalMenu.updateTeamGoalInfo(extraInfo=extraInfo)

    def getSchoolReqs(self):
        if not self.widget:
            return []
        return [ int(schoolMc.name) for schoolMc in self.schoolMcs if schoolMc.selected ]

    def onTeamGoalChanged(self):
        if not self.widget:
            return
        if self.teamGoalMenu:
            goalType = self.teamGoalMenu.getTeamGoalType()
            goal1Idx, goal2Idx, _ = self.teamGoalMenu.getTeamGoalMenuIdx(goalType)
            self.teamGoalMenu.refreshTeamGoal(goalType, goal1Idx, goal2Idx)

    def onTeamHeaderChanged(self):
        if not self.widget:
            return
        if not BigWorld.player().isTeamLeader():
            self.hide()
