#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldPushProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import events
import utils
import gamelog
import gameglobal
import gametypes
import formula
import const
from guis.asObject import ASUtils
from uiProxy import UIProxy
from gamestrings import gameStrings
ACTIVITY_PREPARE = 1
ACTIVITY_SIGN_UP = 2
ACTIVITY_START = 3
ACTIVITY_END = 4
ACTIVITY_END_CLOSE = 5
from data import wing_world_config_data as WWCD
from data import game_msg_data as GMD
from cdata import wing_world_schedule_data as WWSD
from cdata import game_msg_def_data as GMDD

class WingWorldPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldPushProxy, self).__init__(uiAdapter)
        self.timer = 0
        self.widget = None
        self.defaultHide = False
        self.reset()

    def reset(self):
        self.activityState = 0

    def clearAll(self):
        self.defaultHide = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_PUSH)

    def show(self):
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return
        if BigWorld.player().inWingWarCity():
            return
        p = BigWorld.player()
        groupId = p.getWingWorldGroupId()
        if not gameglobal.rds.configData.get('enableWingWarGroup%d' % groupId, False):
            return False
        if not self.widget:
            self.timer = 0
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_PUSH)

    def initUI(self):
        widget = self.widget
        ASUtils.setHitTestDisable(widget.hintEff, True)
        ASUtils.setHitTestDisable(widget.pushIcon.touMing, True)
        widget.hintEff.visible = False
        widget.pushIcon.expandBtn.visible = False
        widget.pushIcon.icon.addEventListener(events.MOUSE_CLICK, self.onOpenClick, False, 0, True)
        widget.pushIcon.endBtn.addEventListener(events.MOUSE_CLICK, self.onOpenClick, False, 0, True)
        widget.pushIcon.prepareBtn.addEventListener(events.MOUSE_CLICK, self.onOpenClick, False, 0, True)
        widget.pushIcon.signUpBtn.addEventListener(events.MOUSE_CLICK, self.onOpenClick, False, 0, True)
        ASUtils.callbackAtFrame(widget.pushIcon, 10, self.setEffectHitTestEnable)

    def setEffectHitTestEnable(self, *args):
        if not self.widget or self.widget.pushIcon.bgEff:
            return
        ASUtils.setHitTestDisable(self.widget.pushIcon.bgEff, True)

    def gotoCampSignInPage(self):
        gameglobal.rds.ui.wingWorld.show(uiConst.WING_WORLD_TAB_CAMP)

    def onOpenClick(self, *args):
        p = BigWorld.player()
        if self.getData()[0] >= ACTIVITY_END:
            p.showGameMsg(GMDD.data.WING_WORLD_BATTLE_END, ())
            return
        widget = self.widget
        widget.hintEff.visible = False
        widget.hintEff.gotoAndStop(1)
        if p.isWingWorldCampMode() and not p.wingWorldCamp:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.WING_WORLD_SIGN_IN_CONFIRM, self.gotoCampSignInPage, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1)
            return
        if not formula.spaceInWingBornIslandOrPeaceCity(p.spaceNo):
            msg = GMD.data.get(GMDD.data.TELEPORT_TO_BORN_ISLAND, {}).get('text', 'TELEPORT_TO_BORN_ISLAND')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, p.cell.enterToWingBornIslandInBattle)
            return
        cityList = self.uiAdapter.wingWorldTransport.getCityList()
        declaredCityList = self.getDeclearedCityList()
        attackCityIds, defCityIds = self.getAttackAndDefCityIdList()
        filterCityList = [ cityId for cityId in declaredCityList if not self.uiAdapter.wingWorldStrategy.isSelfCity(cityId) ]
        if not filterCityList and not cityList:
            p.showGameMsg(GMDD.data.WING_WORLD_BATTLE_END, ())
            msg = GMD.data.get(GMDD.data.CLOSE_WING_WORLD_PUSH, {}).get('text', 'CLOSE_WING_WORLD_PUSH')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.closeWingWorldPush)
        elif not gameglobal.rds.configData.get('enableWingWorldWarQueueV2', False) and p.wingWorld.state == gametypes.WING_WORLD_STATE_DECLARE_END and not defCityIds:
            p.showGameMsg(GMDD.data.WING_WORLD_NO_DEFENT_CITY_IN_PREPARE_TIME, ())
        elif not cityList:
            p.showGameMsg(GMDD.data.WING_WORLD_ATTACK_NOT_ALLOWED, ())
        else:
            self.uiAdapter.wingWorldTransport.show()
        gamelog.info('jbx:onOpenClick')

    def closeWingWorldPush(self):
        self.defaultHide = True
        self.hide()

    def getData(self):
        state, timeStr = (0, 0)
        now = utils.getNow()
        declareStartTime, battleStartTime, endTime = self.getTime()
        p = BigWorld.player()
        if not p:
            return (ACTIVITY_END_CLOSE, timeStr)
        if gameglobal.rds.configData.get('enableWingWorldWarQueueV2', False) and getattr(p, 'wingWorldQueueState', 0) in gametypes.WING_WORLD_SIGN_AND_QUEUE_SIGN_STATES:
            signStartCrontab, pullStartCrontab, signEndCrontab = self.getSignCrontab()
            signEndTime = utils.getNextCrontabTime(pullStartCrontab)
            if not utils.isSameWeek(signEndTime, utils.getNow()):
                signEndTime = utils.getPreCrontabTime(pullStartCrontab)
            time = max(0, int(signEndTime - now))
            timeStr = utils.formatTimeStr(time, 'm:s', True, 2, 2)
            return (ACTIVITY_SIGN_UP, timeStr)
        wingWorldState = BigWorld.player().wingWorld.state
        if wingWorldState <= gametypes.WING_WORLD_STATE_DECLARE:
            state = ACTIVITY_END_CLOSE
        elif wingWorldState < gametypes.WING_WORLD_STATE_OPEN:
            state = ACTIVITY_PREPARE
            time = max(0, int(battleStartTime - now))
            timeStr = utils.formatTimeStr(time, 'm:s', True, 2, 2)
        elif wingWorldState < gametypes.WING_WORLD_STATE_SETTLEMENT:
            state = ACTIVITY_START
            timeStr = utils.formatTimeStr(max(0, int(endTime - now)), 'h:m', True, 2, 2)
        elif now < endTime + WWCD.data.get('endDuration', 10):
            state = ACTIVITY_END
            timeStr = utils.formatTimeStr(0, 'm:s', True, 2, 2)
        else:
            state = ACTIVITY_END_CLOSE
        return (state, timeStr)

    def refreshInfo(self):
        if not self.widget:
            return
        state, timeStr = self.getData()
        if state == ACTIVITY_END_CLOSE:
            self.hide()
            return
        widget = self.widget
        if state != self.activityState and state == ACTIVITY_START:
            widget.hintEff.visible = True
            widget.hintEff.gotoAndPlay(1)
        self.activityState = state
        widget.pushIcon.countdown.visible = self.activityState in [ACTIVITY_START, ACTIVITY_PREPARE, ACTIVITY_SIGN_UP]
        widget.pushIcon.endBtn.visible = self.activityState == ACTIVITY_END
        widget.pushIcon.icon.visible = self.activityState == ACTIVITY_START
        widget.pushIcon.prepareBtn.visible = self.activityState == ACTIVITY_PREPARE
        widget.pushIcon.signUpBtn.visible = self.activityState == ACTIVITY_SIGN_UP
        widget.pushIcon.countdown.textField.text = timeStr
        BigWorld.callback(0.3, self.refreshInfo)

    def getTime(self):
        declareStartTime = utils.getNextCrontabTime(WWSD.data[gametypes.WING_WORLD_STATE_DECLARE]['crontab'])
        if not utils.isSameWeek(declareStartTime, utils.getNow()):
            declareStartTime = utils.getPreCrontabTime(WWSD.data[gametypes.WING_WORLD_STATE_DECLARE_END]['crontab'])
        declareEndTime = utils.getNextCrontabTime(WWSD.data[gametypes.WING_WORLD_STATE_OPEN]['crontab'])
        if not utils.isSameWeek(declareEndTime, utils.getNow()):
            declareEndTime = utils.getPreCrontabTime(WWSD.data[gametypes.WING_WORLD_STATE_OPEN]['crontab'])
        battleEndTime = utils.getNextCrontabTime(WWSD.data[gametypes.WING_WORLD_STATE_SETTLEMENT]['crontab'])
        if not utils.isSameWeek(battleEndTime, utils.getNow()):
            battleEndTime = utils.getPreCrontabTime(WWSD.data[gametypes.WING_WORLD_STATE_SETTLEMENT]['crontab'])
        return (declareStartTime + 3, declareEndTime + 3, battleEndTime + 3)

    def getSignCrontab(self):
        signStartCrontab = ''
        signEndCrontab = ''
        pullStartCrontab = ''
        for key in WWSD.data:
            info = WWSD.data.get(key, {})
            if info.get('stype', 0) == gametypes.WING_CRONTAB_STYPE_SIGN_AND_QUEUE:
                state = info.get('state', 0)
                if state == gametypes.WING_WORLD_SIGN_AND_QUEUE_STATE_SIGN:
                    signStartCrontab = info.get('crontab', '')
                elif state == gametypes.WING_WORLD_SIGN_AND_QUEUE_STATE_QUEUE:
                    signEndCrontab = info.get('crontab', '')
                elif state == gametypes.WING_WORLD_SIGN_AND_QUEUE_STATE_PULL:
                    pullStartCrontab = info.get('crontab', '')

        return (signStartCrontab, pullStartCrontab, signEndCrontab)

    def tryStartTimer(self):
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return
        declareStartTime, declareEndTime, endTime = self.getTime()
        now = utils.getNow()
        if utils.isSameWeek(declareStartTime, now):
            if now < declareStartTime:
                if self.timer:
                    BigWorld.cancelCallback(self.timer)
                    self.timer = 0
                self.timer = BigWorld.callback(declareStartTime - now, self.show)
            elif now > endTime + WWCD.data.get('endDuration', 10):
                self.hide()
            else:
                self.show()

    def checkState(self):
        p = BigWorld.player()
        state = BigWorld.player().wingWorld.state
        if not p.canOpenWingWorldUI() or p.inGuildSpace():
            self.hide()
            return
        if not BigWorld.player().inWingWarCity() and state in (gametypes.WING_WORLD_STATE_DECLARE_END, gametypes.WING_WORLD_STATE_OPEN):
            p.cell.queryWingWorldResume(p.wingWorld.state, p.wingWorld.briefVer, p.wingWorld.countryVer, p.wingWorld.cityVer, p.wingWorld.campVer)
            if p.isWingWorldCampMode():
                if p.wingWorld.country.getOwnCamp().declaredCityId2PostId or not self.defaultHide:
                    self.show()
            elif p.wingWorld.country.getOwn().declaredCityId2PostId or not self.defaultHide:
                self.show()
        else:
            self.hide()

    def getDeclearedCityList(self):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            ownCamp = p.wingWorld.country.getOwnCamp()
            declaredCityList = ownCamp.declaredCityId2PostId.keys()
        else:
            ownCountry = p.wingWorld.country.getOwn()
            declaredCityList = ownCountry.declaredCityId2PostId.keys()
        return declaredCityList

    def getAttackAndDefCityIdList(self):
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            selfSide = p.wingWorld.country.getOwnCamp()
            selfPostId = p.wingWorldPostId
        else:
            selfSide = p.wingWorld.country.getOwn()
            selfPostId = p.wingWorldPostId
        declaredCityId2PostId = selfSide.declaredCityId2PostId
        allowAttackCityIds = selfSide.allowAttackCityIds[:]
        ownedCityIds = selfSide.ownedCityIds[:]
        for declaredCityId, postId in declaredCityId2PostId.iteritems():
            if declaredCityId not in allowAttackCityIds and selfPostId == postId:
                allowAttackCityIds.append(declaredCityId)

        defCityIds = [ cityId for cityId in ownedCityIds if not p.wingWorld.city.getCity(const.WING_CITY_TYPE_WAR, cityId).isDirectSettlement ]
        return (allowAttackCityIds, defCityIds)
