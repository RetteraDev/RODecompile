#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import gameglobal
import uiConst
import keys
import formula
import gamelog
import wingWorldUtils
from guis import events
from gamestrings import gameStrings
from appSetting import Obj as AppSettings
from guis.uiTabProxy import UITabProxy
from commonWingWorld import WWArmyPostVal
from data import wing_world_config_data as WWCD
from data import push_data as PushMsgConfig
TAB_BTN_MAX_CNT = 6

class WingWorldProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(WingWorldProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_BG, self.hide)
        self.animName = None

    def reset(self):
        pass

    def clearAll(self):
        pass

    def appendTab(self, tabList, view, proxy, label = '', visible = True, enable = None):
        tabLen = len(tabList)
        tabList.append({'tabIdx': tabLen,
         'tabName': 'tabBtn%d' % tabLen,
         'view': view,
         'proxy': proxy,
         'visible': visible,
         'label': label,
         'enable': enable})

    def _getTabList(self):
        p = BigWorld.player()
        tabList = []
        self.appendTab(tabList, 'WingWorldOverViewPanel', 'wingWorldOverView', gameStrings.WING_WORLD_TAB_OVER_VIEW, enable=self.getWingCampOverviewCampVisible)
        strategyTabVisible = not p._isSoul() or p.inWingCity()
        self.appendTab(tabList, 'WingWorldStrategyPanel', 'wingWorldStrategy', gameStrings.WING_WORLD_TAB_STRATEGY, strategyTabVisible)
        self.appendTab(tabList, 'WingWorldResourcePanel', 'wingWorldResource', gameStrings.WING_WORLD_TAB_RESOURCES)
        self.appendTab(tabList, 'WingWorldBuildingPanel', 'wingWorldBuilding', gameStrings.WING_WORLD_TAB_BUILDING, not p.inWingWarCity())
        self.appendTab(tabList, 'WingWorldArmyWidget', 'wingWorldArmy', gameStrings.WING_WORLD_TAB_ARMY, enable=self.getWingCampArmyVisible)
        self.appendTab(tabList, 'WingWorldCampWidget', 'wingWorldCamp', gameStrings.WING_WORLD_TAB_CAMP, p.isWingWorldCamp())
        return tabList

    def getWingCampOverviewCampVisible(self):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            return p.isInWingWorldCamp()
        return True

    def getWingCampArmyVisible(self):
        p = BigWorld.player()
        if p.isWingWorldCampMode() and p.isWingWorldCampArmy():
            return p.isInWingWorldCamp()
        return True

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_BG:
            self.widget = widget
            self.initUI()
            self.initTabUI()
            self.widget.defaultCloseBtn = self.widget.closeBtn
            self.widget.setTabIndex(self.showTabIndex)
            self.reflowTabBtns()
            self.refreshInfo()

    def reflowTabBtns(self):
        if not self.widget:
            return
        tabList = self.tabList
        tabLen = len(tabList)
        y = 59
        for tabIdx in xrange(TAB_BTN_MAX_CNT):
            tabBtn = getattr(self.widget, 'tabBtn%d' % tabIdx)
            if tabIdx < tabLen:
                tabBtn.visible = self.tabList[tabIdx]['visible']
                if self.tabList[tabIdx]['enable']:
                    tabBtn.enabled = self.tabList[tabIdx]['enable']()
                else:
                    tabBtn.enabled = True
                tabBtn.label = self.tabList[tabIdx]['label']
                if tabBtn.visible:
                    tabBtn.y = y
                    y += 84
            else:
                tabBtn.visible = False

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_BG)
        currentProxy = self.getCurrentProxy()
        currentProxy and currentProxy.unRegisterPanel()
        collectPanel = gameglobal.rds.ui.wingWorldResource.collectPanel
        if collectPanel:
            collectPanel.resetHeadGen()

    def initUI(self):
        collectPanel = gameglobal.rds.ui.wingWorldResource.collectPanel
        if collectPanel:
            collectPanel.initHeadGen()

    def show(self, tabId = uiConst.WING_WORLD_TAB_OVER_VIEW):
        p = BigWorld.player()
        if tabId == uiConst.WING_WORLD_TAB_OVER_VIEW and p.isWingWorldCampMode() and not p.isInWingWorldCamp():
            tabId = uiConst.WING_WORLD_TAB_CAMP
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_BG)
            self.showTabIndex = tabId
            p.cell.queryWingWorldArmy(p.wingWorld.armyVer, p.wingWorld.armyOnlineVer)
        else:
            self.widget.setTabIndex(tabId)

    def refreshInfo(self):
        if not self.widget:
            return

    def getAppointData(self):
        p = BigWorld.player()
        appointedList = []
        val = p.wingWorld.getArmyByGbId(p.gbId)
        if val:
            mgrPostIds = list(val.mgrPostIds)
            mgrPostIds.sort()
            for subPostId in mgrPostIds:
                if subPostId in wingWorldUtils.wingPostIdData.ARMY_SPECIAL_POST_ID:
                    pVal = p.wingWorld.getArmyByPostId(subPostId)
                    if pVal:
                        appointedList.append({'gbId': pVal.gbId,
                         'photo': pVal.photo,
                         'combatScore': pVal.combatScore,
                         'name': pVal.name,
                         'school': pVal.school,
                         'sex': pVal.sex})
                else:
                    for i in xrange(9):
                        pVal = p.wingWorld.getArmyByPostId(subPostId, i)
                        if pVal:
                            appointedList.append({'gbId': pVal.gbId,
                             'photo': pVal.photo,
                             'combatScore': pVal.combatScore,
                             'name': pVal.name,
                             'school': pVal.school,
                             'sex': pVal.sex})

        return appointedList

    def getArmyMgrInfo(self):
        p = BigWorld.player()
        generalList = []
        for army in p.wingWorld.army.values():
            if WWArmyPostVal.isLeadersEx(army.postId) or army.postId in wingWorldUtils.wingPostIdData.ARMY_SPECIAL_POST_ID:
                generalList.append(army)

        return generalList

    def getSupportSoldierInfo(self, postId):
        soldierList = []
        soldierPostId = 0
        p = BigWorld.player()
        val = p.wingWorld.getArmyByPostId(postId)
        if val:
            mgrPostIds = list(val.mgrPostIds)
            mgrPostIds.sort()
            for subPostId in mgrPostIds:
                if subPostId not in wingWorldUtils.wingPostIdData.ARMY_SPECIAL_POST_ID:
                    soldierPostId = subPostId

        for army in p.wingWorld.army.values():
            if army.postId == soldierPostId:
                soldierList.append(army)

        return soldierList

    def getLeaderAndGeneralInfo(self):
        p = BigWorld.player()
        generalList = []
        for army in p.wingWorld.army.values():
            if WWArmyPostVal.isLeadersEx(army.postId) or WWArmyPostVal.isGeneralEx(army.postId):
                generalList.append(army)

        return generalList

    def getSupportArmyInfo(self, postId):
        generalList = []
        p = BigWorld.player()
        for army in p.wingWorld.army.values():
            supportTgt = army.ownerLeaderGbId if army.ownerLeaderGbId else army.supportTgt
            if army.postId == postId:
                generalList.append(army)
            elif supportTgt != 0 and army.postId not in wingWorldUtils.wingPostIdData.ARMY_SUPER_MGR_POST_IDS:
                support = p.wingWorld.getArmyByGbId(supportTgt)
                if support.postId == postId:
                    generalList.append(army)

        return generalList

    def getVoteArmyInfo(self):
        voteList = []
        sortList = {}
        canVote = False
        p = BigWorld.player()
        for army in p.wingWorld.army.values():
            if p.wingWorld.isPlayerGeneral(army.gbId):
                if p.gbId == army.gbId and p.wingWorld.armyState == gametypes.WING_WORLD_ARMY_STATE_VOTE:
                    canVote = True
                supportTgt = army.supportTgt
                sortList[army.gbId] = {'canVote': False,
                 'name': army.name,
                 'guildName': army.guildName,
                 'source': gameStrings.TEXT_WINGWORLDPROXY_233 % (army.srcRank[0] + 1, gametypes.GUILD_ROLE_DICT.get(army.srcRank[1])),
                 'votes': 0,
                 'votesInfo': [],
                 'supportTgt': supportTgt,
                 'gbId': army.gbId}

        if p.gbId in p.wingWorld.extraCanVoteGbIds and p.wingWorld.armyState == gametypes.WING_WORLD_ARMY_STATE_VOTE:
            canVote = True
        for army in sortList.values():
            army['canVote'] = canVote
            if army['supportTgt'] and army['supportTgt'] in sortList:
                supporter = sortList[army['supportTgt']]
                supporter['votes'] = supporter['votes'] + 1
                supporter['votesInfo'].append(army)

        for gbId, WWArmyGuildVoteVal in p.wingWorld.extraCanVoteGbIds.iteritems():
            if WWArmyGuildVoteVal.tgtGbId in sortList:
                army = {'guildName': WWArmyGuildVoteVal.guildName,
                 'name': WWArmyGuildVoteVal.name}
                sortList[WWArmyGuildVoteVal.tgtGbId]['votesInfo'].append(army)
                sortList[WWArmyGuildVoteVal.tgtGbId]['votes'] += 1

        voteList = sorted(sortList.items(), key=lambda x: x[1]['votes'], reverse=True)
        tempArmy = None
        for i, army in enumerate(voteList):
            army[1]['index'] = i + 1
            if army[1]['gbId'] == p.wingWorldArmyVoteGbId:
                tempArmy = army

        if tempArmy:
            voteList.remove(tempArmy)
            voteList.insert(0, tempArmy)
        return voteList

    def onClickPushMsg(self):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.WING_WORLD_ANIM_PUSH_MSG, self._playAnim, gameStrings.WING_WORLD_DIALOG_YES_BTN_TEXT, None, gameStrings.WING_WORLD_DIALOG_NO_BTN_TEXT, title=gameStrings.WING_WORLD_DIALOG_TITLE, forbidFastKey=True)

    def _playAnim(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_ANIM)
        if self.animName:
            p = BigWorld.player()
            p.scenarioPlay(self.animName + '.xml', 0)
            p.cell.setPlayedScriptNames(self.animName)

    def _isAnimPlayedEver(self):
        p = BigWorld.player()
        if p is None or self.animName is None:
            return True
        else:
            if p.playedFubenAniScripts:
                playedScripts = p.playedFubenAniScripts.split('#')
            else:
                playedScripts = AppSettings.get(keys.SET_PLAYED_SCRIPTS, '').split('#')
            return self.animName in playedScripts

    def onGetWingWorldOpenProgress(self, stage, isOpen, openDonate, openDonateLimit):
        if not gameglobal.rds.configData.get('enableWingWorldAnimPush', False):
            return
        if stage <= 1:
            return
        lastCompletedStage = stage - 1
        self.animName = WWCD.data.get('wingWorldScriptAnimDict', {}).get(lastCompletedStage, 'ytl11b')
        if self._isAnimPlayedEver():
            return
        if formula.getMLGNo(BigWorld.player().spaceNo) in WWCD.data.get('wingWorldDGList', []):
            self._playAnim()
        else:
            if uiConst.MESSAGE_TYPE_WING_WORLD_ANIM not in PushMsgConfig.data:
                PushMsgConfig.data[uiConst.MESSAGE_TYPE_WING_WORLD_ANIM] = {'iconId': 11201,
                 'soundIdx': 404,
                 'once': 0,
                 'tooltip': 'wing world open animation',
                 'canUse': 1}
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_ANIM)

    def clearAllPlayedAnim(self):
        animNameList = []
        for _, animName in WWCD.data.get('wingWorldScriptAnimDict', {}).iteritems():
            animNameList.append(animName)

        if animNameList:
            BigWorld.player().cell.clearPlayedScript('#'.join(animNameList))
        gamelog.info('@ljh clear all played anims of wing world:', animNameList)
