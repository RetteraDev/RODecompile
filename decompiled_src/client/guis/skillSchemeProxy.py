#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillSchemeProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import uiUtils
import const
import gamelog
import time
import utils
from ui import unicode2gbk
from uiProxy import UIProxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class SkillSchemeProxy(UIProxy):
    PVP_SKILL_SCHEME_TAB = const.SKILL_SCHEME_ARENA

    def __init__(self, uiAdapter):
        super(SkillSchemeProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'getPropSchemes': self.onGetPropSchemes,
         'usePropScheme': self.onUsePropScheme,
         'getCurrentSchemeNum': self.getCurrentSchemeNum,
         'buyScheme': self.buyScheme,
         'setSchemeName': self.setSchemeName,
         'enableAutoApply': self.onEnableAutoApply,
         'getPVPSchemeVisible': self.onGetPVPSchemeVisible}
        self.mediator = None
        self.resetMediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_SCHEME, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        BigWorld.player().registerEvent(const.EVENT_UPDATE_SKILL_SCHEME, self.onPropSchemeChange)

    def onPropSchemeChange(self, params):
        data = self.onGetPropSchemes(None)
        self.mediator.Invoke('setPropSchemes', data)

    def getCurrentSchemeNum(self, *args):
        if len(args[3]):
            curNo = int(args[3][0].GetNumber())
            p = BigWorld.player()
            if curNo == self.PVP_SKILL_SCHEME_TAB and not p._isSoul():
                return GfxValue(curNo)
        return GfxValue(BigWorld.player().skillPointSchemeIndex)

    def buyScheme(self, *args):
        idx = int(args[3][0].GetNumber())
        if idx == 1 or idx == 2:
            gameglobal.rds.ui.propSchemeResume.show(idx, 1)
        else:
            gameglobal.rds.ui.tianyuMall.showMallTab(10001, 0)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SKILL_SCHEME)
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_UPDATE_SKILL_SCHEME, self.onPropSchemeChange)

    def show(self):
        if gameglobal.rds.configData.get('enableWingWorldSkillScheme', False):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_SCHEME_V2)
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_SCHEME)

    def onClosePanel(self, *arg):
        self.hide()

    def onGetPropSchemes(self, *arg):
        p = BigWorld.player()
        now = p.getServerTime()
        scheme = p.getAllSkillScheme()
        for i in xrange(4):
            if scheme.has_key(i):
                scheme[i]['nowTime'] = now
                if scheme[i]['expireTime']:
                    scheme[i]['expireTimeText'] = time.strftime('%Y.%m.%d  %H:%M', time.localtime(scheme[i]['expireTime']))
                else:
                    scheme[i]['expireTimeText'] = ''

        if not scheme.has_key(self.PVP_SKILL_SCHEME_TAB):
            scheme[self.PVP_SKILL_SCHEME_TAB] = {}
        scheme[self.PVP_SKILL_SCHEME_TAB]['schemeName'] = SCD.data.get('PVP_SCHEME_NAME', gameStrings.TEXT_SKILLSCHEMEPROXY_103)
        schemeData = utils.getArenaSkillSchemeData(p.realLv)
        scheme[self.PVP_SKILL_SCHEME_TAB]['descText'] = gameStrings.TEXT_SKILLSCHEMEPROXY_105 % (schemeData.get('arenaSkillPoint', 0), schemeData.get('arenaEnhancePoint', 0))
        scheme[self.PVP_SKILL_SCHEME_TAB]['autoApplyCheckBox'] = p.useArenaSkillScheme
        return uiUtils.dict2GfxDict(scheme, True)

    def onUsePropScheme(self, *arg):
        idx = int(arg[3][0].GetNumber())
        if idx == BigWorld.player().skillPointSchemeIndex:
            self.clearWidget()
            return
        if BigWorld.player().checkSkillSchemeOutOfDate(idx) == True:
            if idx == self.PVP_SKILL_SCHEME_TAB:
                gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_SKILLSCHEMEPROXY_119)
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.SCHEME_SWITCH_OVERDUE, '')
                gameglobal.rds.ui.messageBox.showMsgBox(msg)
            BigWorld.player().dispatchEvent(const.EVENT_UPDATE_SKILL_SCHEME, ())
            return
        gamelog.debug('jinjj-----idx', idx)
        BigWorld.player().base.switchSkillPointScheme(idx)
        self.clearWidget()

    def setSchemeName(self, *args):
        idx = int(args[3][0].GetNumber())
        name = unicode2gbk(args[3][1].GetString())
        nowName = BigWorld.player().getSkillSchemeName(idx)
        if nowName != name:
            gamelog.debug('jinjj------setSchemeName-----', idx, name)
            BigWorld.player().base.updateSkillSchemeName(idx, name)
        if idx == self.PVP_SKILL_SCHEME_TAB:
            self.hide()
            self.uiAdapter.skill.enterEditMode()

    def onEnableAutoApply(self, *arg):
        selected = arg[3][0].GetBool()
        p = BigWorld.player()
        if p.getSkillSchemeById(self.PVP_SKILL_SCHEME_TAB):
            p.cell.setUseSkillScheme(const.SKILL_SCHEME_ARENA, selected)
        else:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_SKILLSCHEMEPROXY_119)

    def onGetPVPSchemeVisible(self, *arg):
        value = gameglobal.rds.configData.get('enableArenaSkillScheme', True)
        p = BigWorld.player()
        schemeData = utils.getArenaSkillSchemeData(p.realLv)
        needShow = schemeData.get('arenaSkillPoint', 0) + schemeData.get('arenaEnhancePoint', 0) != 0
        return GfxValue(value and needShow)
