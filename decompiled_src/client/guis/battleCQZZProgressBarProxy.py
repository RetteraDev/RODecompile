#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/battleCQZZProgressBarProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import const
from guis import uiUtils
from guis import events
from uiProxy import UIProxy
from helpers import tickManager
from guis.asObject import ASObject
from data import battle_field_data as BFD
from data import duel_config_data as DCD
from gamestrings import gameStrings
CAMPS = [1, 2]
MAX_FLAG_NUM = 3
BLOOD_MASK_LEN = 154

class BattleCQZZProgressBarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BattleCQZZProgressBarProxy, self).__init__(uiAdapter)
        self.widget = None
        self.tickId = 0
        self.reset()

    def reset(self):
        self.campInfo = {}
        self.flagersInfo = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BATTLE_CQZZ_RPGRESS_BAR:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = 0
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BATTLE_CQZZ_RPGRESS_BAR)

    def isSelfCamp(self, camp):
        p = BigWorld.player()
        return p.tempCamp == camp

    def onGetFlagInfo(self, camp, cnt):
        if not self.campInfo.has_key(camp):
            self.campInfo[camp] = {}
        self.campInfo[camp]['cnt'] = cnt
        self.refreshFlagInfo()

    def onRefreshFlagerInfo(self, gbId, flagerInfo):
        if not self.flagersInfo.has_key(gbId):
            return
        self.flagersInfo[gbId].update(flagerInfo)
        self.refreshPlayerInfo()

    def resetFlagerInfo(self, camp, gbId):
        if not self.campInfo.has_key(camp):
            self.campInfo[camp] = {}
        self.campInfo[camp]['flagerId'] = 0
        self.refreshPlayerInfo()

    def onSetFlagerInfo(self, camp, gbId, flagerInfo):
        if not self.campInfo.has_key(camp):
            self.campInfo[camp] = {}
        self.flagersInfo[gbId] = flagerInfo
        if flagerInfo:
            self.campInfo[camp]['flagerId'] = gbId
        else:
            self.campInfo[camp]['flagerId'] = 0
        self.refreshPlayerInfo()

    def onFlagPicked(self, camp, gbId):
        if not self.campInfo.has_key(camp):
            self.campInfo[camp] = {}
        self.campInfo[camp]['flagerId'] = gbId
        self.refreshPlayerInfo()

    def onFlagFall(self, camp, gbID):
        if not self.campInfo.has_key(camp):
            self.campInfo[camp] = {}
        self.campInfo[camp]['flagerId'] = 0
        self.refreshPlayerInfo()

    def refreshFlagInfo(self):
        if not self.widget:
            return
        for camp in CAMPS:
            cnt = self.campInfo.get(camp, {}).get('cnt', 0)
            if camp == 1:
                flagName = 'bFlag'
            else:
                flagName = 'rFlag'
            for i in xrange(MAX_FLAG_NUM):
                flagMc = self.widget.getChildByName(flagName + str(i))
                if i < cnt:
                    flagMc.gotoAndStop('normal')
                else:
                    flagMc.gotoAndStop('dark')

    def setBlood(self, bloodMc, percent):
        bloodLen = BLOOD_MASK_LEN * percent
        bloodMc.t2tMask.width = bloodLen

    def refreshPlayerInfo(self):
        if not self.widget:
            return
        for camp in CAMPS:
            flagerId = self.campInfo.get(camp, {}).get('flagerId', 0)
            if camp == 1:
                playerMcName = 'bPlayer'
            else:
                playerMcName = 'rPlayer'
            playerMc = self.widget.getChildByName(playerMcName)
            if flagerId and self.flagersInfo.get(flagerId, {}):
                playerInfo = self.flagersInfo.get(flagerId, {})
                playerMc.visible = True
                playerMc.textField.text = playerInfo.get('name', '')
                bloodPercent = playerInfo.get('hp', 1.0) * 1.0 / playerInfo.get('mhp', 1.0)
                self.setBlood(playerMc.blood, bloodPercent)
                photo = playerInfo.get('photo', '')
                if uiUtils.isDownloadImage(photo):
                    playerMc.head.photo.fitSize = True
                    playerMc.head.photo.imgType = uiConst.IMG_TYPE_NOS_FILE
                    playerMc.head.photo.serverId = playerInfo.get('hostID', 0)
                    playerMc.head.photo.url = photo
                else:
                    school = playerInfo.get('school', 0)
                    sex = playerInfo.get('sex', 0)
                    if not photo:
                        photo = utils.getDefaultPhoto(school, sex)
                    playerMc.head.photo.fitSize = True
                    playerMc.head.photo.loadImage(photo)
                playerMc.gbId = flagerId
                playerMc.addEventListener(events.MOUSE_CLICK, self.onPlayerMcClick)
            else:
                playerMc.visible = False

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BATTLE_CQZZ_RPGRESS_BAR)

    def refreshCampNames(self):
        campNames = DCD.data.get('battleCqzzCampNames', gameStrings.BATTLE_CQZZ_CAMPNAMES)
        self.widget.bName.text = campNames.get(1)
        self.widget.rName.text = campNames.get(2)

    def onPlayerMcClick(self, *args):
        e = ASObject(args[3][0])
        targetId = long(e.currentTarget.gbId)
        p = BigWorld.player()
        if targetId == p.id:
            return
        if targetId:
            for en in BigWorld.entities.values():
                if en.IsAvatar and en.gbId == targetId:
                    p.lockTarget(en)
                    self.refreshSelectInfo()

    def initUI(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.widget.flagTimer.text = '00:00'
        self.tickId = tickManager.addTick(1, self.refreshTimer)
        self.widget.goHomeBtn.addEventListener(events.BUTTON_CLICK, self.handleClickGoHome)
        self.widget.statsBtn.addEventListener(events.BUTTON_CLICK, self.handleClickStats)

    def handleClickStats(self, *args):
        gameglobal.rds.ui.battleField.onOpenStatsClick()

    def handleClickGoHome(self, *args):
        BigWorld.player().bfGoHome()

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshFlagInfo()
        self.refreshCampNames()
        self.refreshPlayerInfo()
        self.refreshSelectInfo()

    def formateTime(self, time):
        minute = int(time / 60)
        sec = time - minute * 60
        return '%02d:%02d' % (minute, sec)

    def refreshTimer(self):
        p = BigWorld.player()
        if hasattr(p, 'bfEnd') and p.bfEnd:
            return
        totalTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
        if not p.bfTimeRec:
            countTime = 0
        else:
            countTime = totalTime - int(p.getServerTime() - p.bfTimeRec['tReady'])
            countTime = abs(countTime)
        self.widget.flagTimer.text = self.formateTime(countTime)
        self.refreshSelectInfo()

    def refreshSelectInfo(self):
        p = BigWorld.player()
        self.widget.bPlayer.selectMc.visible = False
        self.widget.rPlayer.selectMc.visible = False
        en = p.targetLocked
        if en and en.IsAvatar and en.gbId:
            for camp in CAMPS:
                flagerId = self.campInfo.get(camp, {}).get('flagerId', 0)
                if flagerId == en.gbId:
                    if camp == 1:
                        playerMcName = 'bPlayer'
                    else:
                        playerMcName = 'rPlayer'
                    playerMc = self.widget.getChildByName(playerMcName)
                    playerMc.selectMc.visible = True

    def checkBattleCQZZ(self):
        p = BigWorld.player()
        return gameglobal.rds.configData.get('enableCqzzBf', False) and p.inFubenType(const.FB_TYPE_BATTLE_FIELD_CQZZ)

    def getAvatarCampName(self, en):
        sideNames = DCD.data.get('battleCqzzCampTopNames', gameStrings.BATTLE_CQZZ_TOPLOG_CAMPNAMES)
        targetCamp = getattr(en, 'tempCamp', 0)
        campName = '%s%s' % (sideNames.get(targetCamp, ''), en.roleName)
        return campName
