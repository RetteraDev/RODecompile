#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenDegreeProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import formula
import gameglobal
import uiConst
import gametypes
from uiProxy import UIProxy
from guis import uiUtils
from guis.ui import gbk2unicode
from callbackHelper import Functor
from guis.messageBoxProxy import MBButton
from data import fb_data as FD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class FubenDegreeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FubenDegreeProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'getData': self.onGetData,
         'selectMode': self.onSelectMode,
         'helpModeEnter': self.onHelpModeEnter}
        self.reset()
        self.shishenModeInfo = []
        self.isOutOfFb = False
        self.isOpenAsPop = False
        self.enterMode = 0
        self.helpMode = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FUBEN_DEGREE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FUBEN_DEGREE:
            self.mediator = mediator

    def open(self, fbId, enterMode, helpMode):
        self.isOutOfFb = True
        self.isOpenAsPop = True
        self.enterMode = enterMode
        self.helpMode = helpMode
        self.fbId = fbId
        fd = FD.data.get(fbId, {})
        noShishenModeSelect = fd.get('noShishenModeSelect', 0)
        if noShishenModeSelect and helpMode:
            fbName = formula.whatFubenName(fbId)
            buttons = [MBButton(gameStrings.TEXT_FUBENDEGREEPROXY_52, Functor(self.onHelpModeEnter), True, True), MBButton(gameStrings.TEXT_FUBENDEGREEPROXY_153, Functor(self.enterShishenFb), True, True), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1)]
            msg = uiUtils.getTextFromGMD(GMDD.data.ENTER_FUBEN_COMFIRM_TIAOZHAN_MODE, gameStrings.TEXT_FUBENDEGREEPROXY_55) % fbName
            gameglobal.rds.ui.messageBox.show(False, gameStrings.TEXT_FUBENDEGREEPROXY_56, msg, buttons)
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_DEGREE, True, True)

    def show(self, isOutOfFb = False, helpMode = False, isOpenAsPop = False, enterMode = 0):
        self.isOutOfFb = isOutOfFb
        self.isOpenAsPop = isOpenAsPop
        self.helpMode = helpMode
        self.enterMode = enterMode
        if isOutOfFb:
            self.fbId = gameglobal.rds.ui.fubenLogin.selectedFb
            fbInfo = gameglobal.rds.ui.fubenLogin.fbInfo
            self.shishenModeInfo = list(fbInfo.get('shishenModeInfo', {}).get(self.fbId, []))
            if 0 in self.shishenModeInfo:
                self.shishenModeInfo.remove(0)
        else:
            self.fbId = formula.getFubenNo(BigWorld.player().spaceNo)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_DEGREE, True, True)

    def clearWidget(self):
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_DEGREE)

    def reset(self):
        self.mediator = None
        self.fbId = 0
        self.shishenAimMode = 0
        self.shishenModeInfo = []
        self.isOutOfFb = False
        self.isOpenAsPop = False
        self.enterMode = 0
        self.helpMode = 0

    def onConfirm(self, *args):
        self.shishenAimMode = int(args[3][0].GetNumber())
        p = BigWorld.player()
        if not self.isOutOfFb:
            self.selectModeInFb()
        elif self.isOpenAsPop:
            self.enterShishenFb()
        else:
            loginProxy = gameglobal.rds.ui.fubenLogin
            p.cell.fbModeSelected(loginProxy.transportEntId, loginProxy.selectedFb, 0, 0, self.shishenAimMode)
            self.hide()

    def enterShishenFb(self):
        p = BigWorld.player()
        if p.inCombat:
            p.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_INCOMBAT, ())
        elif p.life == gametypes.LIFE_DEAD:
            p.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_DEAD, ())
        elif formula.spaceInFuben(p.spaceNo):
            p.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_INFB, ())
        elif formula.spaceInDuel(p.spaceNo):
            p.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_IN_BATTLEFIELD, ())
        else:
            BigWorld.player().cell.enterFubenAfterHeaderApply(self.fbId, False)
            self.hide()

    def selectModeInFb(self):
        p = BigWorld.player()
        modeStr = SCD.data.get('fubenModeNames', ['',
         gameStrings.TEXT_QUESTTRACKPROXY_1748,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_1,
         gameStrings.TEXT_QUESTTRACKPROXY_1748_2,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_3])
        currentMode = gameglobal.rds.ui.currentShishenMode
        if currentMode == 0:
            p.showTopMsg(gameStrings.TEXT_FUBENDEGREEPROXY_124)
            return
        if self.shishenAimMode == currentMode:
            BigWorld.player().showTopMsg(gameStrings.TEXT_FUBENDEGREEPROXY_127 % modeStr[self.shishenAimMode])
            return
        if currentMode > self.shishenAimMode:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_FUBENDEGREEPROXY_130 % modeStr[self.shishenAimMode], Functor(self.comfirmSetShishenMode))
        else:
            BigWorld.player().showTopMsg(gameStrings.TEXT_FUBENDEGREEPROXY_132)

    def comfirmSetShishenMode(self):
        if self.shishenAimMode == 0:
            return
        BigWorld.player().cell.setShishenMode(self.shishenAimMode)
        self.hide()

    def onGetData(self, *args):
        p = BigWorld.player()
        currentMode = self._getCurrentMode()
        self.getItem(currentMode)
        self.getDesc(currentMode)
        modeStr = SCD.data.get('fubenModeNames', ['',
         gameStrings.TEXT_QUESTTRACKPROXY_1748,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_1,
         gameStrings.TEXT_QUESTTRACKPROXY_1748_2,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_3])
        data = {}
        isTeamLeader = p.isInTeamOrGroup() and p.isTeamLeader() or not p.isInTeamOrGroup()
        data['isTeamLeader'] = isTeamLeader
        data['isOutOfFb'] = self.isOutOfFb
        data['isOpenAsPop'] = self.isOpenAsPop
        data['enterBtnLabel'] = gameStrings.TEXT_FUBENDEGREEPROXY_153 if self.isOpenAsPop or not isTeamLeader else gameStrings.TEXT_FUBENDEGREEPROXY_153_1
        data['avaliableModes'] = self.shishenModeInfo
        data['currentMode'] = currentMode
        data['modeStr'] = [modeStr[1], modeStr[2], modeStr[3]]
        data['showModeSetButton'] = gameglobal.rds.ui.currentShishenMode > 0 and gameglobal.rds.ui.currentShishenMode < 4 and p.isInTeamOrGroup() and p.isTeamLeader()
        enableHelpMode = gameglobal.rds.configData.get('enableFubenHelpMode', False)
        data['enableHelp'] = enableHelpMode and self.helpMode
        data['fubenName'] = self._getFbName(self.fbId, currentMode)
        data['fubenBangDaiTips'] = SCD.data.get('fubenBangDaiTips', gameStrings.TEXT_FUBENDEGREEPROXY_161)
        data['fubenNormalTips'] = SCD.data.get('fubenNormalTips', gameStrings.TEXT_FUBENDEGREEPROXY_162)
        return uiUtils.dict2GfxDict(data, True)

    def _getCurrentMode(self):
        currentMode = 0
        if not self.isOutOfFb:
            currentMode = gameglobal.rds.ui.currentShishenMode
        elif self.isOpenAsPop:
            currentMode = self.enterMode
        elif len(self.shishenModeInfo) == 0:
            currentMode = 0
        elif len(self.shishenModeInfo) > 0:
            currentMode = self.shishenModeInfo[len(self.shishenModeInfo) - 1]
        return currentMode

    def onSelectMode(self, *args):
        mode = int(args[3][0].GetNumber())
        if self.shishenAimMode == mode:
            return
        self.shishenAimMode = mode
        self.getItem(self.shishenAimMode)
        self.getDesc(self.shishenAimMode)

    def getItem(self, mode):
        itemArray = []
        itemList = FD.data.get(self.fbId, {}).get('awardItems', [])
        if not itemList:
            return
        for item in itemList[mode - 1]:
            ret = {}
            itemId = item[0]
            itemNum = item[1]
            ret['itemId'] = itemId
            ret['iconPath'] = uiUtils.getItemIconFile64(itemId)
            ret['count'] = itemNum
            ret['color'] = uiUtils.getItemColor(itemId)
            itemArray.append(ret)

        if self.mediator:
            self.mediator.Invoke('setAwardItem', uiUtils.array2GfxAarry(itemArray))

    def getDesc(self, mode):
        fd = FD.data.get(self.fbId, {})
        desc = fd.get('modeDesc', [])
        fubenName = self._getFbName(self.fbId, mode)
        if not desc:
            return
        if self.mediator:
            self.mediator.Invoke('setDesc', (GfxValue(gbk2unicode(desc[mode - 1])), GfxValue(gbk2unicode(fubenName))))

    def leaveAndClear(self):
        if self.mediator:
            self.hide()

    def _getFbName(self, spaceNo, currentMode):
        fbName = ''
        fbData = FD.data.get(spaceNo, {})
        baseName = fbData.get('name', '')
        fbName += baseName
        primaryLevelName = fbData.get('primaryLevelName', '')
        fbName += gameStrings.TEXT_HELPPROXY_512 + primaryLevelName
        shishenModeLevel = SCD.data.get('fubenModeNames', ['',
         gameStrings.TEXT_QUESTTRACKPROXY_1748,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_1,
         gameStrings.TEXT_QUESTTRACKPROXY_1748_2,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_3])
        if currentMode > 4:
            currentMode = 4
        modeName = fbData.get('modeName', '')
        if modeName:
            fbName += '(%s)' % modeName
        if currentMode > 0:
            fbName += gameStrings.TEXT_FUBENDEGREEPROXY_238 % shishenModeLevel[currentMode]
        return fbName

    def onHelpModeEnter(self, *arg):
        msg = SCD.data.get('fubenBangDaiMsg', gameStrings.TEXT_FUBENDEGREEPROXY_243)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.yesHelpModeEnter)

    def yesHelpModeEnter(self):
        p = BigWorld.player()
        if p.inCombat:
            p.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_INCOMBAT, ())
        elif p.life == gametypes.LIFE_DEAD:
            p.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_DEAD, ())
        elif formula.spaceInFuben(p.spaceNo):
            p.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_INFB, ())
        elif formula.spaceInDuel(p.spaceNo):
            p.showGameMsg(GMDD.data.FB_ENTER_FORBIDDEN_IN_BATTLEFIELD, ())
        else:
            BigWorld.player().cell.enterFubenAfterHeaderApply(self.fbId, True)
            self.hide()
