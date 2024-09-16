#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/castbarProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import uiConst
import gameglobal
import skillDataInfo
from helpers import action as ACT
from ui import gbk2unicode
from uiProxy import UIProxy
from data import state_data as SD
from data import state_client_data as SCD

class CastbarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CastbarProxy, self).__init__(uiAdapter)
        self.nowtick = 0
        self.lefttick = 0
        self.Mode = uiConst.MODE_Inactive
        self.modelMap = {}
        self.pct = 0
        self.callbackHandle = []
        self.countDownCallBack = []
        self.guide = False
        self.chargePct = 0
        self.mediator = None
        self.barRef = None
        self.chargeSkillOver = False
        self.isChargeSkillBar = False
        self.stages = []
        self.chargeSkillId = 0
        self.sepRef = None
        self.animationRec = [False, False, False]
        self.autoReleaseCharge = False
        self.buffCallback = None
        self.needShowText = True

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CAST_BAR:
            self.mediator = mediator
            self.mc = self.mediator.Invoke('getWidget').GetMember('castbar')
            self.mc.GotoAndStop('begin')
            self.barRef = self.mc.GetMember('castbar0')
            self.maskRef = self.barRef.GetMember('barMask')
            self.fillRef = self.barRef.GetMember('fill')
            self.noticeRef = self.barRef.GetMember('noticeMc')
            self.timeTextRef = self.barRef.GetMember('timeMc').GetMember('timeText')
            self.shineRef = self.barRef.GetMember('castShine')
            self.sepRef = self.barRef.GetMember('chargePoint')
            self.chargeAniRef = self.barRef.GetMember('chargeAnimation')
            self.mc.SetVisible(False)
            self.shineRef.SetVisible(False)
            self.sepRef.SetVisible(False)
            self.chargeAniRef.SetVisible(False)
            self.fillStartX = self.fillRef.GetMember('x').GetNumber()
            self.fillEndX = self.fillRef.GetMember('width').GetNumber() + self.fillStartX
            self.Mode = uiConst.MODE_Inactive
            self.newBar = self.fillRef.GetMember('fill')

    def startCastBar(self, time, desc, isChargeBar = False):
        for i in self.callbackHandle:
            BigWorld.cancelCallback(i)

        self.callbackHandle = []
        for i in self.countDownCallBack:
            BigWorld.cancelCallback(i)

        self.countDownCallBack = []
        self.totaltick = BigWorld.time() + time
        self.starttick = BigWorld.time()
        self.nowtick = BigWorld.time()
        self.desc = desc
        self.isChargeSkillBar = isChargeBar
        self.mc.GotoAndStop('begin')
        self.noticeRef.GotoAndPlay('notice')
        self.noticeRef.GetMember('noticeText').SetText('')
        p = BigWorld.player()
        self.setSkillIcon(self._getSkillIcon(), self.isWuShuang(p.skillId))
        if self.isChargeSkillBar:
            self.newBar.GotoAndPlay('bar1')
        else:
            self.mediator.Invoke('clearSeperator')
            self.newBar.GotoAndPlay('normal')
        self.needShowText = True
        BigWorld.player().spellingType = BigWorld.player().getSkillSpellingType()
        self._updateCastBar()

    def _updateCastBar(self):
        self.nowtick = BigWorld.time()
        p = BigWorld.player()
        self.lefttick = self.totaltick - self.nowtick
        if self.lefttick > 0 and self.Mode != uiConst.MODE_Active:
            self._setPercent(0, self.lefttick)
            self.mc.SetVisible(True)
            self.mc.SetAlpha(100)
            self.barRef.GotoAndPlay('casting')
            self.shineRef.SetVisible(True)
            self.Mode = uiConst.MODE_Active
            self.callbackHandle.append(BigWorld.callback(0.05, self._updateCastBar))
            return
        if self.Mode == uiConst.MODE_FadeOutHold:
            if not self.isChargeSkillBar:
                if self.nowtick - self.fadetick > 0.5:
                    self.Mode = uiConst.MODE_FadeOut
            elif self.chargeSkillOver:
                if self.nowtick - self.fadetick > 0.5:
                    self.Mode = uiConst.MODE_FadeOut
            elif p.isChargeKeyDown and self.autoReleaseCharge:
                p.releaseCharge()
            self.callbackHandle.append(BigWorld.callback(0.05, self._updateCastBar))
        elif self.Mode == uiConst.MODE_FadeOut:
            fadePct = (self.nowtick - self.fadetick) * 1000 / 250
            if fadePct > 1:
                self.Mode = uiConst.MODE_Inactive
                self.barRef.GotoAndPlay('disappear')
                self.chargeAniRef.SetVisible(False)
                self.shineRef.SetVisible(False)
                if self.isChargeSkillBar:
                    gameglobal.rds.ui.actionbar.showChargeSkillShine(self.chargeSkillId, False)
            else:
                self.mc.SetAlpha((1 - fadePct) * 100)
                self.callbackHandle.append(BigWorld.callback(0.05, self._updateCastBar))
            p.isChargeKeyDown = False
            p.spellingType = ACT.S_DEFAULT
            for i in self.callbackHandle:
                BigWorld.cancelCallback(i)

            self.callbackHandle = []
            if self.guide == True:
                self.guide = False
                self.startCountDown(self.countDownTime, self.guideDesc)
        if self.lefttick > 0:
            self.pct = self._getPct()
            self._setPercent(self.pct, self.lefttick)
            self.callbackHandle.append(BigWorld.callback(0.05, self._updateCastBar))
        elif self.Mode == uiConst.MODE_Active:
            self._setPercent(1, 0)
            self.barRef.GotoAndPlay('completed')
            if self.isChargeSkillBar:
                self.mc.GotoAndPlay('begin')
                self.noticeRef.GotoAndPlay('notice')
                self.noticeRef.GetMember('noticeText').SetText(gbk2unicode(gameStrings.TEXT_CASTBARPROXY_161))
            self.shineRef.SetVisible(False)
            self.Mode = uiConst.MODE_FadeOutHold
            self.callbackHandle.append(BigWorld.callback(0.05, self._updateCastBar))
            self.fadetick = BigWorld.time()

    def _getPct(self):
        return (self.nowtick - self.starttick) / (self.totaltick - self.starttick)

    def _setPercent(self, pct, leftTicks):
        self._setPercentBar(pct, self.maskRef)
        if self.isChargeSkillBar:
            l = len(self.stages)
            for i, stage in enumerate(self.stages[::-1]):
                if stage > 0 and pct > stage:
                    self.barRef.GotoAndPlay('activated')
                    self.newBar.GotoAndPlay('bar' + str(l - i))
                    self.chargeAniRef.SetVisible(True)
                    if l == 3:
                        if not self.animationRec[0]:
                            self.chargeAniRef.GotoAndPlay('single')
                            self.animationRec[0] = True
                        self.sepRef.GetMember('sep1').GotoAndPlay('light')
                    elif l == 4:
                        if not self.animationRec[max(l - i, 2)]:
                            self.chargeAniRef.GotoAndPlay('doubleStep' + str(max(l - i, 2)))
                            self.animationRec[max(l - i, 2)] = True
                        self.sepRef.GetMember('sep' + str(max(l - i, 2))).GotoAndPlay('light')
                    break

        ct = leftTicks
        buf = '%.1f s' % ct
        if self.mediator != None:
            self.mediator.Invoke('setTimeText', GfxValue(buf))

    def _setPercentBar(self, pct, maskref):
        maskref.SetXScale((pct + 0.1) * 100)
        sx = (self.fillEndX - self.fillStartX) * (pct + 0.1) + self.fillStartX
        sx = min(sx, self.fillEndX)
        self.shineRef.SetX(sx)

    def notifyCastInterrupt(self):
        if self.barRef != None and self.Mode != uiConst.MODE_Inactive:
            self.mc.GotoAndStop('begin')
            self.chargeAniRef.SetVisible(False)
            self.noticeRef.GotoAndPlay('interrupt')
            self.newBar.GotoAndPlay('interrupt')
            self.Mode = uiConst.MODE_FadeOutHold
            self.totaltick = BigWorld.time()
            self.fadetick = BigWorld.time()
            if self.isChargeSkillBar:
                gameglobal.rds.ui.castbar.chargeSkillOver = True
                gameglobal.rds.ui.actionbar.showChargeSkillShine(self.chargeSkillId, False)
            self._updateCastBar()

    def startCountDown(self, time, desc):
        for i in self.callbackHandle:
            BigWorld.cancelCallback(i)

        self.callbackHandle = []
        for i in self.countDownCallBack:
            BigWorld.cancelCallback(i)

        self.countDownCallBack = []
        self.mc.GotoAndStop('begin')
        self.totaltick = BigWorld.time() + time
        self.starttick = BigWorld.time()
        self.nowtick = BigWorld.time()
        self.desc = desc
        p = BigWorld.player()
        self.setSkillIcon(self._getSkillIcon(), self.isWuShuang(p.skillId))
        self.newBar.GotoAndPlay('normal')
        self.noticeRef.GotoAndPlay('notice')
        self.mediator.Invoke('clearSeperator')
        self.chargeAniRef.SetVisible(False)
        self.chargeAniRef.GotoAndStop(1)
        self.countDown = False
        self.isChargeSkillBar = False
        self.needShowText = True
        self.countDownCallBack.append(BigWorld.callback(0.05, self._updateCountDown))

    def _updateCountDown(self):
        self.nowtick = BigWorld.time()
        self.lefttick = self.totaltick - self.nowtick
        if self.lefttick > 0 and self.countDown == False:
            self._setPercent(1, self.lefttick)
            self.noticeRef.GotoAndPlay('notice')
            self.Mode = uiConst.MODE_Active
            if self.needShowText:
                if BigWorld.player().guideSkillCancelMode == gameglobal.GUIDESKILL_CANCEL_ALL:
                    self.noticeRef.GetMember('noticeText').SetText(gbk2unicode(gameStrings.TEXT_CASTBARPROXY_252))
                if BigWorld.player().guideSkillCancelMode == gameglobal.GUIDESKILL_CANCEL_NOMAL:
                    self.noticeRef.GetMember('noticeText').SetText(gbk2unicode(gameStrings.TEXT_CASTBARPROXY_254))
            else:
                self.noticeRef.GetMember('noticeText').SetText(gbk2unicode(''))
            self.mc.SetVisible(True)
            self.mc.SetAlpha(100)
            self.barRef.GotoAndPlay('casting')
            self.countDown = True
            self.countDownCallBack.append(BigWorld.callback(0.05, self._updateCountDown))
            return
        if self.lefttick > 0:
            self.pct = 1 - self._getPct() - 0.1
            self._setPercent(self.pct, self.lefttick)
            self.countDownCallBack.append(BigWorld.callback(0.05, self._updateCountDown))
        else:
            self._setPercent(-0.1, 0)
            self.countDownCallBack = []

    def startGuideCastbar(self, time, desc, guideTime, guideDesc):
        self.guide = True
        self.isChargeSkillBar = False
        self.countDownTime = guideTime
        self.guideDesc = guideDesc
        self.startCastBar(time, desc)

    def startChargeBar(self, stages, desc):
        total = 0.0
        total += stages[len(stages) - 1]
        self.chargeSkillOver = False
        self.isChargeSkillBar = True
        self.stages = stages
        if len(stages) - 2 > 0:
            self.setSeperator(len(stages) - 2)
        self.animationRec = [False, False, False]
        self.startCastBar(total, desc, True)
        self.chargeAniRef.SetVisible(False)
        self.chargeAniRef.GotoAndStop(1)
        self.chargeSkillId = BigWorld.player().skillPlayer.skillID
        gameglobal.rds.ui.actionbar.showChargeSkillShine(self.chargeSkillId, True)

    def setSeperator(self, sepLen):
        if self.mediator != None:
            self.mediator.Invoke('setSeperator', GfxValue(sepLen))

    def showChargeSeperatorShine(self, stage):
        if not self.mediator:
            return
        self.mediator.Invoke('showChargeSeperatorShine', GfxValue(stage))

    def setSkillIcon(self, path, isWuShuang):
        if self.mediator != None and path:
            self.mediator.Invoke('setSkillIcon', (GfxValue(path), GfxValue(isWuShuang)))

    def easeOutCastbar(self):
        if self.barRef and self.Mode != uiConst.MODE_Inactive:
            self.mc.GotoAndStop('begin')
            self.Mode = uiConst.MODE_FadeOutHold
            self.totaltick = BigWorld.time()
            self.fadetick = BigWorld.time()
            if self.isChargeSkillBar:
                gameglobal.rds.ui.castbar.chargeSkillOver = True
                gameglobal.rds.ui.actionbar.showChargeSkillShine(self.chargeSkillId, False)
            self._updateCastBar()

    def isWuShuang(self, skillId):
        p = BigWorld.player()
        skVal = p.wsSkills.get(skillId, None)
        isWuShuang = False
        if skVal and hasattr(skVal, 'isWsSkill'):
            isWuShuang = skVal.isWsSkill
        return isWuShuang

    def _getSkillIcon(self):
        p = BigWorld.player()
        skillId = p.skillPlayer.skillID
        skillLv = 1
        if p._isOnZaijuOrBianyao():
            if gameglobal.rds.ui.zaiju.mediator:
                skills = gameglobal.rds.ui.zaiju.skills
            else:
                skills = gameglobal.rds.ui.zaijuV2.skills
            for sId, sLv in skills:
                if skillId == sId:
                    skillLv = sLv
                    break

            sd = skillDataInfo.ClientSkillInfo(skillId, skillLv)
            icon = 'skill/icon/' + str(sd.getSkillData('icon', 0)) + '.dds'
        else:
            sVal = p.getSkills().get(skillId)
            if sVal:
                skillLv = sVal.level
            icon = gameglobal.rds.ui.actionbar._getSwithIcon(skillId, skillLv)
        return icon

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CAST_BAR)

    def startBuffCountDown(self, old):
        p = BigWorld.player()
        newState = set(p.statesServerAndOwn.keys())
        oldState = set(old.keys())
        addState = newState - oldState
        delState = oldState - newState
        if addState:
            for state in addState:
                if type(state) != tuple:
                    continue
                if SCD.data.get(state, {}).get('showGuide', 0):
                    time = state[2]
                    desc = ''
                    for i in self.callbackHandle:
                        BigWorld.cancelCallback(i)

                    self.callbackHandle = []
                    for i in self.countDownCallBack:
                        BigWorld.cancelCallback(i)

                    self.countDownCallBack = []
                    self.mc.GotoAndStop('begin')
                    self.totaltick = BigWorld.time() + time
                    self.starttick = BigWorld.time()
                    self.nowtick = BigWorld.time()
                    self.desc = desc
                    icon = SD.data.get(state, {}).get('iconId', 'notFound')
                    self.setSkillIcon('state/icon/%d.dds' % icon, False)
                    self.newBar.GotoAndPlay('normal')
                    self.noticeRef.GotoAndPlay('notice')
                    self.mediator.Invoke('clearSeperator')
                    self.chargeAniRef.SetVisible(False)
                    self.chargeAniRef.GotoAndStop(1)
                    self.countDown = False
                    self.isChargeSkillBar = False
                    self.needShowText = False
                    self.countDownCallBack.append(BigWorld.callback(0.05, self._updateCountDown))
                    self.buffCallback = BigWorld.callback(time, self.easeOutCastbar)
                    break

        if delState:
            for state in delState:
                if type(state) != tuple:
                    continue
                if SCD.data.get(state, {}).get('showGuide', 0):
                    self.easeOutCastbar()
                    if self.buffCallback:
                        BigWorld.cancelCallback(self.buffCallback)
                        self.buffCallback = None
