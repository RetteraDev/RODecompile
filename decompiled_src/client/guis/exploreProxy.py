#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/exploreProxy.o
import BigWorld
from Scaleform import GfxValue
import gametypes
import gamelog
import gameglobal
import const
from guis.uiProxy import SlotDataProxy
from guis import uiConst, uiUtils, ui
from guis.ui import gbk2unicode
from data import special_life_skill_equip_data as SLSED
from cdata import game_msg_def_data as GMDD
AUTO_EXPLORE_CD = 5
EXPLORE_TIP_TIME = 3

class ExploreProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ExploreProxy, self).__init__(uiAdapter)
        self.bindType = 'explore'
        self.type = 'explore'
        self.modelMap = {'doExplore': self.onDoExplore,
         'startRefreshPos': self.onStartRefreshPos,
         'stopRefheshPos': self.onStopRefreshPos,
         'getCompassInfo': self.onGetCompassInfo,
         'getDisplayDist': self.onGetDispayDist,
         'setAutoExplore': self.onSetAutoExplore,
         'findTarget': self.onFindTarget,
         'notOnTarget': self.onNotOnTarget}
        self.refCallback = None
        self.powerRegenCallBack = None
        self.autoCallBack = None
        self.showFCallBack = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_EXPLORE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EXPLORE:
            self.med = mediator
            BigWorld.player().cell.prepareExplore()
            self.showFCallBack = BigWorld.callback(1, self.showTip)

    def reset(self):
        self.med = None
        if self.refCallback:
            BigWorld.cancelCallback(self.refCallBack)
        if self.powerRegenCallBack:
            BigWorld.cancelCallback(self.powerRegenCallBack)
        if self.autoCallBack:
            BigWorld.cancelCallback(self.autoCallBack)
        if self.showFCallBack:
            BigWorld.cancelCallback(self.showFCallBack)
        self.refCallback = None
        self.powerRegenCallBack = None
        self.showFCallBack = None
        self.autoCallBack = None
        self.cPower = 0
        self.powerRegen = 0
        self.maxPower = 0
        self.powerRecordTime = 0
        self.lastYaw = 0
        self.result = -1
        self.autoExplore = False
        self.autoExploreNeedCheckPower = False
        self.powerNeed = 0
        self.autoCDLeft = 0
        self.showTips = False

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXPLORE)
        self.removeTip()

    def show(self, *args):
        if BigWorld.player().checkExploreEquip():
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXPLORE)

    def fKeyDown(self):
        if self.med and gameglobal.rds.ui.pressKeyF.type in (const.F_EXPLORE, const.F_FIND):
            onTarget = self.med.Invoke('isOnTarget').GetBool()
            self._innerDoExplore(onTarget)

    def onDoExplore(self, *args):
        if not BigWorld.player().checkExploreEquip():
            return
        onTarget = args[3][0].GetBool()
        self._innerDoExplore(onTarget)

    def showTip(self):
        gameglobal.rds.ui.pressKeyF.isExplore = True
        gameglobal.rds.ui.pressKeyF.setType(const.F_EXPLORE)

    def removeTip(self):
        gameglobal.rds.ui.pressKeyF.isExplore = False
        gameglobal.rds.ui.pressKeyF.removeType(const.F_EXPLORE)
        gameglobal.rds.ui.pressKeyF.isFind = False
        gameglobal.rds.ui.pressKeyF.removeType(const.F_FIND)

    @ui.callFilter(1, True)
    def _innerDoExplore(self, onTarget):
        if onTarget:
            p = BigWorld.player()
            groundY = p.position[1] - p.qinggongMgr.getDistanceFromGround()
            BigWorld.player().cell.doDiscover(groundY)
        else:
            BigWorld.player().cell.doExplore()

    def onGetCompassInfo(self, *args):
        compass = BigWorld.player().exploreEquip.get(gametypes.EXPLORE_EQUIP_COMPASS)
        if compass:
            eData = SLSED.data.get(compass.id, {})
            ret = {'regen': eData.get('regen', 0),
             'maxSensePower': eData.get('sensePower', 1),
             'currentPower': eData.get('sensePower', 1),
             'targetRad': 1}
            self.maxPower = eData.get('sensePower', 1)
            self.powerRegen = eData.get('regen', 0)
            self.setPowerInfo(eData.get('sensePower', 1))
            return uiUtils.dict2GfxDict(ret)
        gamelog.error('@zhp compass is none')

    def onGetDispayDist(self, *args):
        scroll = BigWorld.player().exploreEquip.get(gametypes.EXPLORE_EQUIP_SCROLL)
        dist = 0
        if scroll:
            dist = SLSED.data.get(scroll.id, {}).get('displayDist', 0)
        return GfxValue(dist)

    def onSetAutoExplore(self, *args):
        self.autoExplore = args[3][0].GetBool()
        if self.autoExplore:
            BigWorld.player().showGameMsg(GMDD.data.EXPLORER_AUTO, ())
        self.autoCDLeft = 0
        self._innerAutoExplore()

    def onFindTarget(self, *args):
        gameglobal.rds.sound.stopSound(gameglobal.SD_439)
        gameglobal.rds.sound.playSound(gameglobal.SD_435)
        gameglobal.rds.ui.pressKeyF.isFind = True
        gameglobal.rds.ui.pressKeyF.setType(const.F_FIND)

    def onNotOnTarget(self, *args):
        gameglobal.rds.ui.pressKeyF.isFind = False
        gameglobal.rds.ui.pressKeyF.removeType(const.F_FIND)

    def onStartRefreshPos(self, *args):
        self._innerRefreshPos()

    def onStopRefreshPos(self, *args):
        if self.refCallback:
            BigWorld.cancelCallback(self.refCallBack)
            self.refCallback = None

    def refreshEquip(self):
        if self.med:
            compass = BigWorld.player().exploreEquip.get(gametypes.EXPLORE_EQUIP_COMPASS)
            if compass:
                eData = SLSED.data.get(compass.id, {})
                self.maxPower = eData.get('sensePower', 1)
                self.powerRegen = eData.get('regen', 0)
                self.cPower = self.maxPower
                self.setPowerInfo(eData.get('sensePower', 1))
                self._innerRefPower()

    def _innerAutoExplore(self):
        if self.med and self.autoExplore:
            if self.autoCDLeft <= 1:
                if self._getCurrentPower() >= self.powerNeed:
                    onTarget = self.med.Invoke('isOnTarget').GetBool()
                    self._innerDoExplore(onTarget)
                    self.autoExploreNeedCheckPower = False
                else:
                    self.autoExploreNeedCheckPower = True
                self.autoCDLeft = AUTO_EXPLORE_CD
            else:
                self.autoCDLeft -= 1
            self.med.Invoke('refreshCDText', GfxValue(gbk2unicode(str(self.autoCDLeft) + 's')))
            if self.autoCallBack:
                BigWorld.cancelCallback(self.autoCallBack)
            self.autoCallBack = BigWorld.callback(1, self._innerAutoExplore)
        elif not self.med or not self.autoExplore:
            if self.autoCallBack:
                BigWorld.cancelCallback(self.autoCallBack)
                self.autoCallBack = None

    def _innerRefreshPos(self):
        if self.med:
            p = BigWorld.player()
            isMouseMode = False
            if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.MOUSE_MODE:
                isMouseMode = True
            self.med.Invoke('setPlayerPos', uiUtils.array2GfxAarry((tuple(p.position),
             p.yaw * 180 / 3.14,
             isMouseMode,
             BigWorld.camera().direction.yaw * 180 / 3.14)))
            self.lastYaw = p.yaw
            BigWorld.callback(0.1, self._innerRefreshPos)

    def exploreResult(self, result, arg):
        gamelog.debug('@zhp exploreResult', result, arg)
        self.result = result
        tipFrame = ''
        if result == gametypes.EXPLORE_RES_FARAWARY:
            dis = arg[1]
            arg = arg[0]
            if dis > 800:
                tipFrame = 'd1'
            elif dis > 400:
                tipFrame = 'd2'
            elif dis > 200:
                tipFrame = 'd3'
            else:
                tipFrame = 'd4'
        elif result == gametypes.EXPLORE_RES_IN_RANGE1:
            tipFrame = 'd5'
        elif result == gametypes.EXPLORE_RES_IN_RANGE2:
            tipFrame = 'd6'
        elif result == gametypes.EXPLORE_RES_IN_RANGE3:
            tipFrame = 'd7'
        if result == gametypes.EXPLORE_RES_IN_SIGHT:
            arg = (arg[0][0], arg[0][2])
            gameglobal.rds.sound.stopSound(gameglobal.SD_439)
            gameglobal.rds.sound.playSound(gameglobal.SD_439)
        else:
            gameglobal.rds.sound.stopSound(gameglobal.SD_439)
            gameglobal.rds.sound.playSound(gameglobal.SD_434)
        gfxResult = {'result': result,
         'arg': arg,
         'tipFrame': tipFrame}
        if self.med:
            self.med.Invoke('setExploreResult', uiUtils.dict2GfxDict(gfxResult, True))
        self.setPowerInfo(self._getCurrentPower() - self.powerNeed)

    def refreshExplorePanel(self):
        if self.med:
            self.med.Invoke('refreshBinding')

    def getSlotID(self, key):
        return (0, BigWorld.player().exploreEquip.get(gametypes.EXPLORE_EQUIP_SCROLL))

    def getSlotValue(self, movie, idItem, idCon):
        data = self.movie.CreateObject()
        scroll = BigWorld.player().exploreEquip.get(gametypes.EXPLORE_EQUIP_SCROLL)
        if scroll:
            data.SetMember('iconPath', GfxValue(uiUtils.getItemIconFile40(scroll.id)))
            self.powerNeed = SLSED.data.get(scroll.id, {}).get('powerNeed', 0)
        else:
            data = GfxValue(1)
            data.SetNull()
            self.powerNeed = 0
        return data

    def showExploreSuc(self):
        if self.med:
            self.med.Invoke('showSucTips')
            gameglobal.rds.sound.playSound(gameglobal.SD_438)
            gameglobal.rds.ui.pressKeyF.isFind = False
            gameglobal.rds.ui.pressKeyF.removeType(const.F_FIND)

    def getScorllBindKey(self):
        return 'explore.slot0'

    def onGetToolTip(self, *arg):
        scroll = BigWorld.player().exploreEquip.get(gametypes.EXPLORE_EQUIP_SCROLL)
        return gameglobal.rds.ui.inventory.GfxToolTip(scroll)

    def setPowerInfo(self, cPower):
        self.cPower = cPower
        self.powerRecordTime = BigWorld.player().getServerTime()
        self.checkPowerRegen()

    def checkPowerRegen(self):
        if self.cPower < self.maxPower and self.powerRegen:
            if not self.powerRegenCallBack:
                self.powerRegenCallBack = BigWorld.callback(0.08, self._innerRefPower)
        elif self.powerRegenCallBack:
            BigWorld.cancelCallback(self.powerRegenCallBack)
            self.powerRegenCallBack = None

    def _innerRefPower(self):
        if self._getCurrentPower() == self.maxPower:
            if self.powerRegenCallBack:
                BigWorld.cancelCallback(self.powerRegenCallBack)
                self.powerRegenCallBack = None
        else:
            self.powerRegenCallBack = BigWorld.callback(0.08, self._innerRefPower)
        if self.med:
            self.med.Invoke('refreshPower', (GfxValue(self._getCurrentPower()), GfxValue(self.maxPower)))

    def _getCurrentPower(self):
        return min(self.cPower + (BigWorld.player().getServerTime() - self.powerRecordTime) * self.powerRegen, self.maxPower)
