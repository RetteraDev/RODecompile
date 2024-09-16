#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/celebrityRankProxy.o
import BigWorld
import gameglobal
import uiConst
import keys
import const
import utils
import gametypes
import random
from uiTabProxy import UITabProxy
from gameStrings import gameStrings
from guis.asObject import TipManager
from guis import uiUtils
from appSetting import Obj as AppSettings
from guis.asObject import MenuManager
from data import hall_of_fame_config_data as HOFCD
from cdata import game_msg_def_data as GMDD
TAB_XIUWEI_IDX = 0
TAB_EQUIPMENT_IDX = 1
TAB_BEAUTY_IDX = 2
TAB_HANDSOME_IDX = 3
TAB_GUIBAO_IDX = 4
TAB_HOUSERICH_IDX = 5
TAB_TEACHER_IDX = 6
VOTE_TAB_TOP_TYPE_MAP = {TAB_BEAUTY_IDX: [gametypes.TOP_TYPE_HALL_OF_FAME_HONGYAN, const.PROXY_KEY_HALL_OF_FAME_HONGYAN],
 TAB_HANDSOME_IDX: [gametypes.TOP_TYPE_HALL_OF_FAME_YINGCAI, const.PROXY_KEY_HALL_OF_FAME_YINGCAI],
 TAB_GUIBAO_IDX: [gametypes.TOP_TYPE_HALL_OF_FAME_GUIBAO, const.PROXY_KEY_HALL_OF_FAME_GUIBAO],
 TAB_HOUSERICH_IDX: [gametypes.TOP_TYPE_HALL_OF_FAME_QIAOJIANG, const.PROXY_KEY_HALL_OF_FAME_QIAOJIANG],
 TAB_TEACHER_IDX: [gametypes.TOP_TYPE_HALL_OF_FAME_MINGSHI, const.PROXY_KEY_HALL_OF_FAME_MINGSHI]}
PANEL_POS = (24, 12)

class CelebrityRankProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(CelebrityRankProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CELEBRITY_RANK, self.hide)
        self.rankState = None
        self.timer = None
        self.pushedRewardIcon = False
        self.bHofState = True

    def reset(self):
        super(CelebrityRankProxy, self).reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CELEBRITY_RANK:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(CelebrityRankProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CELEBRITY_RANK)

    def _getTabList(self):
        return [{'tabIdx': TAB_XIUWEI_IDX,
          'tabName': 'xiuweiBtn',
          'view': 'CelebrityRankPanelWidget',
          'proxy': 'celebrityXiuWeiRank'},
         {'tabIdx': TAB_EQUIPMENT_IDX,
          'tabName': 'equipmentBtn',
          'view': 'CelebrityRankPanelWidget',
          'proxy': 'celebrityEquipmentRank'},
         {'tabIdx': TAB_BEAUTY_IDX,
          'tabName': 'beautyBtn',
          'view': 'CelebrityRankPanelWidget',
          'proxy': 'celebrityVoteRank'},
         {'tabIdx': TAB_HANDSOME_IDX,
          'tabName': 'handsomeBtn',
          'view': 'CelebrityRankPanelWidget',
          'proxy': 'celebrityVoteRank'},
         {'tabIdx': TAB_GUIBAO_IDX,
          'tabName': 'guibaoBtn',
          'view': 'CelebrityRankPanelWidget',
          'proxy': 'celebrityVoteRank'},
         {'tabIdx': TAB_HOUSERICH_IDX,
          'tabName': 'houseRichBtn',
          'view': 'CelebrityRankPanelWidget',
          'proxy': 'celebrityVoteRank'},
         {'tabIdx': TAB_TEACHER_IDX,
          'tabName': 'teacherBtn',
          'view': 'CelebrityRankPanelWidget',
          'proxy': 'celebrityVoteRank'}]

    def show(self):
        if not gameglobal.rds.configData.get('enableHallOfFame', False):
            self.hide()
            return
        if not self.bHofState:
            BigWorld.player().showGameMsg(GMDD.data.HALL_OF_FAME_CLOSED, ())
            return
        if self.widget:
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_CELEBRITY_RANK)

    def pushIcon(self):
        self.stopTimeCheck()
        if not gameglobal.rds.configData.get('enableHallOfFame', False):
            return
        if self.pushedRewardIcon and AppSettings.get(keys.SET_UI_CELEBRITY_RANK_START_PUSH, False):
            return
        beginTime = HOFCD.data.get('hofRewardPushTime', {}).get('beginTime', '')
        endTime = HOFCD.data.get('hofRewardPushTime', {}).get('stopTime', '')
        if utils.getDisposableCronTabTimeStamp(endTime) < utils.getNow():
            return
        if utils.inCrontabRangeWithYear(beginTime, endTime) and not self.pushedRewardIcon:
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_CELEBRITY_REWARD, {'click': self.onClickRewardPushIcon})
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CELEBRITY_REWARD)
            self.pushedRewardIcon = True
        beginTime = HOFCD.data.get('hofStartPushTime', {}).get('beginTime', '')
        endTime = HOFCD.data.get('hofStartPushTime', {}).get('stopTime', '')
        if utils.inCrontabRangeWithYear(beginTime, endTime) and not AppSettings.get(keys.SET_UI_CELEBRITY_RANK_START_PUSH, False):
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_CELEBRITY_START, {'click': self.onClickStartPushIcon})
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CELEBRITY_START)
            AppSettings[keys.SET_UI_CELEBRITY_RANK_START_PUSH] = True
        self.timer = BigWorld.callback(5, self.pushIcon)

    def clearAll(self):
        self.pushedRewardIcon = False
        self.bHofState = True
        self.stopTimeCheck()
        self.uiAdapter.celebrityXiuWeiRank.clearAll()
        self.uiAdapter.celebrityVoteRank.clearAll()
        self.uiAdapter.celebrityEquipmentRank.clearAll()
        self.uiAdapter.celebrityQuiz.clearAll()

    def stopTimeCheck(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if not gameglobal.rds.configData.get('enableHallOfFameAll', False):
            self.widget.awardBtn.visible = False
            self.widget.rulesBtn.visible = False
            self.widget.quizBtn.visible = False
        self.updateFameTabBtnState(not gameglobal.rds.configData.get('enableHallOfFameDisableTabBtn', False))
        self.refreshInfo()
        self.initTabUI()
        if self.showTabIndex == -1:
            self.widget.setTabIndex(TAB_XIUWEI_IDX)

    def refreshInfo(self):
        if not self.widget:
            return
        if self.getCurrentQuizState() == gametypes.HALL_OF_FAME_QUIZ_STATE_OPEN:
            self.widget.quizBtn.disabled = False
            TipManager.removeTip(self.widget.quizBtn)
        else:
            self.widget.quizBtn.disabled = True
            TipManager.addTip(self.widget.quizBtn, HOFCD.data.get('quizNotInTimeMsg', ''))

    def genNeededInfo(self, info):
        realInfo = {}
        realInfo['ver'] = info[0]
        realInfo['key'] = info[3]
        realInfo['myRank'] = 0
        dataList = info[1]
        realDataList = []
        dataList.sort(cmp=lambda x, y: (cmp(y[3], x[3]) if x[3] != y[3] else cmp(x[4], y[4])))
        if self.getCurrentBlockState():
            dataList = self.updateDataList(dataList)
        for i, data in enumerate(dataList):
            infoMap = {}
            infoMap['index'] = i + 1
            infoMap['gbid'] = data[0]
            infoMap['roleName'] = utils.getRoleNameFromNameWithHostIdStr(data[1])
            infoMap['schoolName'] = uiUtils.getSchoolNameById(data[2])
            infoMap['value'] = data[3][0]
            infoMap['hostId'] = utils.getHostIdFromNameWithHostIdStr(data[1])
            infoMap['serverName'] = utils.getServerName(infoMap['hostId'])
            if infoMap['gbid'] == BigWorld.player().gbId:
                realInfo['myRank'] = i + 1
            realDataList.append(infoMap)

        realInfo['data'] = realDataList
        return realInfo

    def updateDataList(self, dataList):
        shieldList = []
        realList = []
        for data in dataList:
            if data[3][0] == -1:
                shieldList.append(data)
            else:
                realList.append(data)

        random.shuffle(shieldList)
        return shieldList + realList

    def getCurrentMainState(self):
        if self.rankState:
            return self.rankState[0]
        else:
            return None

    def getCurrentBlockState(self):
        if self.rankState:
            return self.rankState[1]
        else:
            return None

    def getCurrentQuizState(self):
        if self.rankState:
            return self.rankState[2]
        else:
            return None

    def updateData(self, data, proxyID):
        self.rankState = data[4]
        self.refreshInfo()
        info = self.genNeededInfo(data)
        info['proxyId'] = proxyID
        key = info.get('key', '')
        if proxyID == const.PROXY_KEY_HALL_OF_FAME_XIUWEI:
            if key != gametypes.ALL_LV_TOP_RANK_KEY:
                gameglobal.rds.ui.celebrityXiuWeiRank.updateData(info)
        elif proxyID == const.PROXY_KEY_HALL_OF_FAME_SHENBING:
            if key != gametypes.ALL_LV_TOP_RANK_KEY:
                gameglobal.rds.ui.celebrityEquipmentRank.updateData(info)
        elif proxyID in [const.PROXY_KEY_HALL_OF_FAME_HONGYAN,
         const.PROXY_KEY_HALL_OF_FAME_YINGCAI,
         const.PROXY_KEY_HALL_OF_FAME_QIAOJIANG,
         const.PROXY_KEY_HALL_OF_FAME_GUIBAO,
         const.PROXY_KEY_HALL_OF_FAME_MINGSHI]:
            gameglobal.rds.ui.celebrityVoteRank.updateData(info)
        gameglobal.rds.ui.celebrityQuiz.updateData(info)

    def updateShuffleData(self, dataList):
        shieldList = []
        realList = []
        for data in dataList:
            if data.get('value', 0) == -1:
                shieldList.append(data)
            else:
                realList.append(data)

        random.shuffle(shieldList)
        realList.sort(key=lambda x: x.get('index', 0))
        return shieldList + realList

    def refreshCommonView(self, widget, info):
        data = info.get('data', [])
        myRank = info.get('myRank', 0) if not self.getCurrentBlockState() else '**'
        widget.myRankText.text = gameStrings.RANK_NOT_IN_TEXT if myRank == 0 else myRank
        if not self.getCurrentBlockState():
            data.sort(key=lambda x: x.get('index', 0))
        else:
            data = self.updateShuffleData(data)
        widget.scrollWndList.dataArray = data

    def listItemCommonFunc(self, itemMc):
        data = itemMc.data
        itemMc.topIcon.visible = False
        if self.getCurrentBlockState() and data.get('value', 0) == -1:
            itemMc.rank.text = '**'
            itemMc.rankValue.text = '*****'
        elif data.get('index', 1) <= 3:
            itemMc.topIcon.visible = True
            itemMc.topIcon.gotoAndStop('type%d' % int(data.get('index', 1)))
        MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_RANK, {'roleName': data.roleName,
         'hostId': data.hostId,
         'gbId': data.gbid})

    def getLvBtnInfoList(self):
        return [{'name': 'lv0',
          'lvKey': '1_69'}, {'name': 'lv1',
          'lvKey': '70_89'}]

    def getLvBtnInfoMap(self):
        return {'lv0': '1_69',
         'lv1': '70_79'}

    def getListItemInfoMap(self):
        return {'rank': 'index',
         'roleName': 'roleName',
         'schoolName': 'schoolName',
         'rankValue': 'value',
         'serverName': 'serverName'}

    def getInitLvMcName(self):
        lv = BigWorld.player().lv
        if 1 <= lv <= 69:
            return 'lv0'
        if 70 <= lv <= 89:
            return 'lv1'

    def getCurrentVoteRank(self):
        return VOTE_TAB_TOP_TYPE_MAP.get(self.currentTabIndex, 0)

    def _onQuizBtnClick(self, e):
        gameglobal.rds.ui.celebrityQuiz.show()

    def _onRulesBtnClick(self, e):
        gameglobal.rds.ui.celebrityRankRules.show()

    def _onAwardBtnClick(self, e):
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'handleClickAwardBtn'):
            proxy.handleClickAwardBtn()

    def onClickStartPushIcon(self):
        self.show()
        gameglobal.rds.ui.celebrityRankRules.show()

    def onClickRewardPushIcon(self):
        gameglobal.rds.ui.celebrityGloryPalace.show()

    def checkMainIconCanShow(self):
        return gameglobal.rds.configData.get('enableHallOfFame', False) and not gameglobal.rds.configData.get('enableHideHallOfFameBtn', False)

    def updateHofLock(self):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def updateFameTabBtnState(self, disable):
        if not self.widget:
            return
        btnList = [self.widget.beautyBtn,
         self.widget.handsomeBtn,
         self.widget.guibaoBtn,
         self.widget.houseRichBtn,
         self.widget.teacherBtn]
        for btn in btnList:
            btn.enabled = disable
            btn.mouseEnabled = True
            if disable:
                TipManager.removeTip(btn)
            else:
                TipManager.addTip(btn, HOFCD.data.get('enableTabBtnTip', ''))

    def recordHallOfFameState(self, bHofState):
        self.bHofState = bHofState
