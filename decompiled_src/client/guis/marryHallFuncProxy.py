#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryHallFuncProxy.o
import BigWorld
from Scaleform import GfxValue
import math
import utils
import uiUtils
import gametypes
import gameglobal
import uiConst
import const
import events
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from asObject import ASUtils
from callbackHelper import Functor
from data import marriage_config_data as MCD
from data import marriage_package_data as MPD
from data import marriage_theme_data as MTD
from data import marriage_firework_data as MFD
BTN_NUM_PER_ROW = 5
BTN_OFFSET_X = 45
BTN_OFFSET_Y = 55
BTN_TYPE_CANDY = 1
BTN_TYPE_REDPACKET = 2
BTN_TYPE_FIREWORK = 3
BG_INIT_HEIGHT = 30

class MarryHallFuncProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryHallFuncProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.reset()

    def reset(self):
        self.funcInfo = None
        self.cancelTimer()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_HALL_FUNC:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_HALL_FUNC)

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_HALL_FUNC)

    def initUI(self):
        self.initData()
        self.initSate()
        self.refreshInfo()

    def initData(self):
        pass

    def initSate(self):
        happyValMax = MCD.data.get('marriageHappyLimit', 520)
        self.widget.happyVal.maxValue = happyValMax
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)
        self.initBtn()

    def initBtn(self):
        p = BigWorld.player()
        marriageBeInvitedInfo = getattr(p, 'marriageBeInvitedInfo', {})
        wifeGbId = marriageBeInvitedInfo.get('wifeGbId', 0)
        hunsbandGbId = marriageBeInvitedInfo.get('hunsbandGbId', 0)
        self.widget.removeAllInst(self.widget.btnCanvas)
        index = 0
        btn = self.widget.getInstByClsName('MarryHallFunc_CandyShareBtn')
        btn.x = index % BTN_NUM_PER_ROW * BTN_OFFSET_X
        btn.y = index / BTN_NUM_PER_ROW * BTN_OFFSET_Y
        btn.name = 'candyBtn'
        btn.funcType = BTN_TYPE_CANDY
        self.widget.btnCanvas.addChild(btn)
        btn.realBtn.addEventListener(events.BUTTON_CLICK, self.handleCandyBtnClick, False, 0, True)
        index += 1
        btn = self.widget.getInstByClsName('MarryHallFunc_RedPacketBtn')
        btn.x = index % BTN_NUM_PER_ROW * BTN_OFFSET_X
        btn.y = index / BTN_NUM_PER_ROW * BTN_OFFSET_Y
        btn.name = 'redPacketBtn'
        btn.funcType = BTN_TYPE_REDPACKET
        self.widget.btnCanvas.addChild(btn)
        btn.realBtn.addEventListener(events.BUTTON_CLICK, self.handleRedPacketBtnClick, False, 0, True)
        index += 1
        mType, subType = marriageBeInvitedInfo.get('mType', 0), marriageBeInvitedInfo.get('subType', 0)
        marriagePackageList = marriageBeInvitedInfo.get('marriagePackageList', ())
        if marriagePackageList:
            zhutiData, fenweiData, xlYifuData, xnYifuData, blYifuData, bnYifuData, cheduiData = marriagePackageList
            zhutiList = MPD.data.get((mType, subType), {}).get('zhuti', [])
            if zhutiList:
                themeId = zhutiList[zhutiData - 1]
                fireWorkList = MTD.data.get(themeId, {}).get('fireWorkTypes', ())
                for i, fId in enumerate(fireWorkList):
                    fData = MFD.data.get(fId, {})
                    btn = self.widget.getInstByClsName('MarryHallFunc_FireWorkBtn')
                    btn.x = index % BTN_NUM_PER_ROW * BTN_OFFSET_X
                    btn.y = index / BTN_NUM_PER_ROW * BTN_OFFSET_Y
                    btn.name = 'fireWorkBtn' + str(fId)
                    btn.funcType = BTN_TYPE_FIREWORK
                    btn.fId = fId
                    btn.realBtn.label = fData.get('name', '')
                    self.widget.btnCanvas.addChild(btn)
                    btn.realBtn.addEventListener(events.BUTTON_CLICK, self.handleFireWorkBtnClick, False, 0, True)
                    index += 1

        self.widget.bg.height = BG_INIT_HEIGHT + BTN_OFFSET_Y * math.ceil(index * 1.0 / BTN_NUM_PER_ROW)

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        self.updateTime()

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def updateCooldown(self, mc, per):
        coolDown = mc.coolDown
        if coolDown:
            ASUtils.setHitTestDisable(coolDown, True)
            frame = 1 if per == 1 else math.floor((coolDown.totalFrames - 2) * per) + 3
            coolDown.gotoAndStop(frame)

    def onEnterFrame(self, *args):
        pass

    def cancelTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def updateTime(self):
        if self.hasBaseData():
            self.updatePanelInfo()
            self.cancelTimer()
            self.timer = BigWorld.callback(0.1, self.updateTime)

    def updatePanelInfo(self):
        p = BigWorld.player()
        marriageBeInvitedInfo = getattr(p, 'marriageBeInvitedInfo', {})
        if marriageBeInvitedInfo:
            happyVal = marriageBeInvitedInfo.get('happyVal', 0)
            self.widget.happyVal.currentValue = happyVal
            shareCandyCD = MCD.data.get('marriageCandyInterval', 60)
            lastShareCandyTime = marriageBeInvitedInfo.get('lastShareCandyTime', 0)
            candyBtn = self.widget.btnCanvas.getChildByName('candyBtn')
            if candyBtn:
                passTime = p.getServerTime() - lastShareCandyTime
                passPer = min(passTime * 1.0 / shareCandyCD, 1) if lastShareCandyTime else 1
                self.updateCooldown(candyBtn, min(passTime / shareCandyCD, 1))
            redPacketBtn = self.widget.btnCanvas.getChildByName('redPacketBtn')
            if redPacketBtn:
                tReady = marriageBeInvitedInfo.get('tReady', 0)
                if tReady:
                    marriageHallDuringTime = MCD.data.get('marriageHallDuringTime', 1800)
                    now = utils.getNow()
                    if p._isSoul() or now > tReady + marriageHallDuringTime - const.TIME_INTERVAL_MINUTE:
                        redPacketBtn.realBtn.enabled = False
                    else:
                        redPacketBtn.realBtn.enabled = True
                else:
                    redPacketBtn.realBtn.enabled = True
            mType, subType = marriageBeInvitedInfo.get('mType', 0), marriageBeInvitedInfo.get('subType', 0)
            marriagePackageList = marriageBeInvitedInfo.get('marriagePackageList', ())
            if marriagePackageList:
                zhutiData, fenweiData, xlYifuData, xnYifuData, blYifuData, bnYifuData, cheduiData = marriagePackageList
                zhutiList = MPD.data.get((mType, subType), {}).get('zhuti', [])
                if zhutiList:
                    themeId = zhutiList[zhutiData - 1]
                    fireWorkList = MTD.data.get(themeId, {}).get('fireWorkTypes', ())
                    for fId in fireWorkList:
                        fireWorkBtn = self.widget.btnCanvas.getChildByName('fireWorkBtn' + str(fId))
                        if fireWorkBtn:
                            fData = MFD.data.get(fId, {})
                            cdTime = fData.get('cdTime', '')
                            fireWorkCDDict = marriageBeInvitedInfo.get('fireWorkCDDict', {})
                            if fireWorkCDDict:
                                lastFireWorkTime = fireWorkCDDict.get(fId, 0)
                                passTime = utils.getNow() - lastFireWorkTime
                                passTime = p.getServerTime() - lastFireWorkTime
                                passPer = min(passTime * 1.0 / cdTime, 1) if lastFireWorkTime else 1
                                self.updateCooldown(fireWorkBtn, passPer)

    def handleCandyBtnClick(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.target
            p = BigWorld.player()
            msg = gameStrings.MARRIAGE_RELEASE_CANDY_RELEASE
            marriageCandyReduceYunChui = MCD.data.get('marriageCandyReduceYunChui', 0)
            bonusIcon = {'bonusType': 'yunChui',
             'value': str(marriageCandyReduceYunChui)}
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.cell.applyShareMarriageHallExposed), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, bonusIcon=bonusIcon, style=uiConst.MSG_BOX_BUY_ITEM)

    def handleRedPacketBtnClick(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.target
            self.uiAdapter.marryRedPacket.show()

    def handleFireWorkBtnClick(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.target
            self.confirmFireRelease(t.parent.fId)

    def confirmFireRelease(self, fId):
        p = BigWorld.player()
        fData = MFD.data.get(fId, {})
        name = fData.get('name', '')
        reduceYunChui = fData.get('reduceYunChui', 0)
        msg = gameStrings.MARRIAGE_FIREWORK_RELEASE % name
        bonusIcon = {'bonusType': 'yunChui',
         'value': str(reduceYunChui)}
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.cell.applyReleaseFireWork, fId), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, bonusIcon=bonusIcon, style=uiConst.MSG_BOX_BUY_ITEM)
