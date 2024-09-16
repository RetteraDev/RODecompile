#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/skillSchemeV2Proxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import uiUtils
import const
import gamelog
import time
import utils
import formula
from gamestrings import gameStrings
from ui import unicode2gbk
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import region_server_config_data as RSCD
from cdata import game_msg_def_data as GMDD

class SkillSchemeV2Proxy(UIProxy):
    PVP_SKILL_SCHEME_TAB = const.SKILL_SCHEME_ARENA
    WW_SKILL_SCHEME_TAB = const.SKILL_SCHEME_WINGWORLD
    SKILL_SCHEME_CROSS_BF = const.SKILL_SCHEME_CROSS_BF

    def __init__(self, uiAdapter):
        super(SkillSchemeV2Proxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'getPropSchemes': self.onGetPropSchemes,
         'usePropScheme': self.onUsePropScheme,
         'getCurrentSchemeNum': self.getCurrentSchemeNum,
         'buyScheme': self.buyScheme,
         'setSchemeName': self.setSchemeName,
         'enableAutoApply': self.onEnableAutoApply,
         'getPVPSchemeVisible': self.onGetPVPSchemeVisible,
         'getCrossBFVisible': self.onGetCrossBFVisible,
         'getWingWorldVisible': self.onGetWingWorldVisible}
        self.mediator = None
        self.resetMediator = None
        self.editorIndex = self.PVP_SKILL_SCHEME_TAB
        uiAdapter.registerEscFunc(uiConst.WIDGET_SKILL_SCHEME_V2, self.clearWidget)

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
            if curNo == self.WW_SKILL_SCHEME_TAB:
                return GfxValue(curNo)
            if curNo == self.SKILL_SCHEME_CROSS_BF and not formula.isCrossServerBattleField(p.mapID):
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
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SKILL_SCHEME_V2)
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_UPDATE_SKILL_SCHEME, self.onPropSchemeChange)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SKILL_SCHEME_V2)

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
        if not scheme.has_key(self.WW_SKILL_SCHEME_TAB):
            scheme[self.WW_SKILL_SCHEME_TAB] = {}
        if not scheme.has_key(self.SKILL_SCHEME_CROSS_BF):
            scheme[self.SKILL_SCHEME_CROSS_BF] = {}
        scheme[self.PVP_SKILL_SCHEME_TAB]['schemeName'] = SCD.data.get('PVP_SCHEME_NAME', 'pvpArena')
        schemeData = utils.getArenaSkillSchemeData(p.realLv)
        scheme[self.PVP_SKILL_SCHEME_TAB]['descText'] = gameStrings.SKILL_SCHEME_DESC % (schemeData.get('arenaSkillPoint', 0), schemeData.get('arenaEnhancePoint', 0))
        scheme[self.PVP_SKILL_SCHEME_TAB]['autoApplyCheckBox'] = p.useArenaSkillScheme
        scheme[self.PVP_SKILL_SCHEME_TAB]['jjcSpaceDesc'] = gameStrings.SKILL_SCHEME_ONLY_JJC
        scheme[self.PVP_SKILL_SCHEME_TAB]['jjcAutoSwitch'] = gameStrings.SKILL_SCHEME_JJC_AUTO_SWITCH
        scheme[self.WW_SKILL_SCHEME_TAB]['schemeName'] = SCD.data.get('WWW_SCHEME_NAME', 'wingWorld')
        schemeData = utils.getWingWorldSkillSchemaData(p.getWingWorldGroupId())
        scheme[self.WW_SKILL_SCHEME_TAB]['descText'] = gameStrings.SKILL_SCHEME_DESC % (schemeData.get('wingSkillPoint', 0), schemeData.get('wingEnhancePoint', 0))
        scheme[self.WW_SKILL_SCHEME_TAB]['autoApplyCheckBox'] = p.useWingWorldSkillScheme
        scheme[self.WW_SKILL_SCHEME_TAB]['wwSpaceDesc'] = gameStrings.SKILL_SCHEME_ONLY_WINGWORLD
        scheme[self.WW_SKILL_SCHEME_TAB]['wwAutoSwitch'] = gameStrings.SKILL_SCHEME_WING_WORLD_AUTO_SWITCH
        scheme[self.WW_SKILL_SCHEME_TAB]['groupType'] = 'group%d' % p.getWingWorldGroupId()
        scheme[self.SKILL_SCHEME_CROSS_BF]['schemeName'] = SCD.data.get('CROSS_BF_SCHEME_NAME', 'CROSS_BF_SCHEME_NAME')
        schemeData = utils.getCrossBFSkillSchemaData(p.lv)
        scheme[self.SKILL_SCHEME_CROSS_BF]['descText'] = gameStrings.SKILL_SCHEME_DESC % (schemeData.get('skillPoint', 0), schemeData.get('enhancePoint', 0))
        scheme[self.SKILL_SCHEME_CROSS_BF]['autoApplyCheckBox'] = p.useCrossBFSkillScheme
        scheme[self.SKILL_SCHEME_CROSS_BF]['crossServerBFDesc'] = gameStrings.SKILL_SCHEME_ONLY_CROSS_BF_WINGWORLD
        scheme[self.SKILL_SCHEME_CROSS_BF]['crossServerBFAutoSwitch'] = gameStrings.SKILL_SCHEME_CROSS_BF_AUTO_SWITCH
        return uiUtils.dict2GfxDict(scheme, True)

    def onUsePropScheme(self, *arg):
        idx = int(arg[3][0].GetNumber())
        if idx == BigWorld.player().skillPointSchemeIndex:
            self.clearWidget()
            return
        if BigWorld.player().checkSkillSchemeOutOfDate(idx) == True:
            if idx in (self.PVP_SKILL_SCHEME_TAB, self.SKILL_SCHEME_CROSS_BF):
                gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.SKILL_SCHEME_CONFIRM)
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
            gamelog.debug('jbx:------setSchemeName-----', idx, name)
            BigWorld.player().base.updateSkillSchemeName(idx, name)
        if idx in (self.PVP_SKILL_SCHEME_TAB, self.WW_SKILL_SCHEME_TAB, self.SKILL_SCHEME_CROSS_BF):
            self.hide()
            self.editorIndex = idx
            self.uiAdapter.skill.enterEditMode()

    def onEnableAutoApply(self, *arg):
        tabIdx = int(arg[3][0].GetNumber())
        selected = arg[3][1].GetBool()
        p = BigWorld.player()
        if p.getSkillSchemeById(tabIdx):
            if tabIdx == const.SKILL_SCHEME_ARENA:
                p.cell.setUseSkillScheme(const.SKILL_SCHEME_ARENA, selected)
            elif tabIdx == const.SKILL_SCHEME_CROSS_BF:
                p.cell.setUseSkillScheme(const.SKILL_SCHEME_CROSS_BF, selected)
            else:
                p.cell.setUseSkillScheme(const.SKILL_SCHEME_WINGWORLD, selected)
        else:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.SKILL_SCHEME_CONFIRM)

    def onGetPVPSchemeVisible(self, *arg):
        value = gameglobal.rds.configData.get('enableArenaSkillScheme', True)
        p = BigWorld.player()
        schemeData = utils.getArenaSkillSchemeData(p.realLv)
        needShow = schemeData.get('arenaSkillPoint', 0) + schemeData.get('arenaEnhancePoint', 0) != 0
        return GfxValue(value and needShow)

    def onGetCrossBFVisible(self, *args):
        value = gameglobal.rds.configData.get('enableCrossBFSkillScheme', True)
        p = BigWorld.player()
        schemeData = utils.getCrossBFSkillSchemaData(p.realLv)
        needShow = schemeData.get('skillPoint', 0) + schemeData.get('enhancePoint', 0) != 0
        return GfxValue(value and needShow)

    def onGetWingWorldVisible(self, *args):
        p = BigWorld.player()
        schemeData = utils.getWingWorldSkillSchemaData(p.getWingWorldGroupId())
        needShow = schemeData.get('wingSkillPoint', 0) + schemeData.get('wingEnhancePoint', 0) != 0
        return GfxValue(needShow)
