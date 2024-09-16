#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/abilityTreeProxy.o
from gamestrings import gameStrings
import copy
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gametypes
from callbackHelper import Functor
from guis import uiConst
from uiProxy import UIProxy
from guis.ui import gbk2unicode
from guis import uiUtils
from data import ability_tree_data as ATD
from data import ability_tree_phase_data as ATPD
from data import ability_data as AD
from data import ability_tree_node_reverse_data as ATNRD
from data import life_skill_data as LSD
from data import life_skill_resource_data as LSRD
from data import life_skill_collection_data as LSCD
from data import life_skill_manufacture_data as LSMD

class AbilityTreeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AbilityTreeProxy, self).__init__(uiAdapter)
        self.modelMap = {'getFameData': self.onGetFameData,
         'getTreeBaseData': self.onGetTreeBaseData,
         'getTreePhaseBaseData': self.onGetTreePhaseBaseData,
         'getTreeData': self.onGetTreeData,
         'getHint': self.onGetHint,
         'clickActivate': self.onClickActivate,
         'clickClose': self.onClickClose}
        self.mediator = None
        self.abilityFameWeiWang = 0
        self.needShowHint = False
        self.hitAnNo = 0
        self.messageBoxId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_ABILITY_TREE, self.hide)

    def reset(self):
        self.mediator = None
        self.needShowHint = False
        self.messageBoxId = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ABILITY_TREE:
            self.mediator = mediator

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ABILITY_TREE)

    def onClickClose(self, *arg):
        self.hide()

    def onGetFameData(self, *arg):
        p = BigWorld.player()
        self.setFame(const.ABILITY_FAME_TANSUO, p.getFame(const.ABILITY_FAME_TANSUO))
        self.setFame(const.ABILITY_FAME_WEIWANG, p.getFame(const.ABILITY_FAME_WEIWANG))

    def onGetTreeBaseData(self, *arg):
        ret = {}
        for id, data_item in ATD.data.iteritems():
            temp = copy.deepcopy(data_item)
            abilities = data_item.get('abilities', ())
            for i in xrange(len(abilities)):
                for j in xrange(len(abilities[i])):
                    if abilities[i][j] in AD.data:
                        adInfo = AD.data.get(abilities[i][j], {})
                        info = {}
                        info['name'] = adInfo.get('name', '')
                        info['description'] = adInfo.get('description', '')
                        info['icon'] = adInfo.get('icon', 0)
                        if adInfo:
                            sid = adInfo.get('sid', 0)
                            atype = adInfo.get('atype', 0)
                            resourceId = 0
                            if atype == gametypes.ABILITY_LS_COLLECTION_SUB_ON:
                                resourceId = LSCD.data.get(sid, {}).get('resourceId', 0)
                            elif atype == gametypes.ABILITY_LS_MANUFACTURE_SUB_ON:
                                resourceId = LSMD.data.get(sid, {}).get('resourceId', 0)
                            reqSkills = LSRD.data.get(resourceId, {}).get('reqSkills', [])
                            if reqSkills:
                                extraName = ''
                                for key in reqSkills:
                                    skillInfo = LSD.data.get(key, {})
                                    extraName += ' (%sLv.%d)' % (skillInfo.get('name', ''), skillInfo.get('lv', ''))

                                info['name'] += extraName
                        temp[abilities[i][j]] = info

            ret[id] = temp

        return uiUtils.dict2GfxDict(ret, True)

    def onGetTreePhaseBaseData(self, *arg):
        return uiUtils.array2GfxAarry(ATPD.data.items(), True)

    def onGetTreeData(self, *arg):
        p = BigWorld.player()
        for key in p.abilityTree:
            self.setTreeNodeData(key, p.abilityTree[key])

    def onClickActivate(self, *arg):
        needValue = int(arg[3][0].GetNumber())
        anNo = int(arg[3][1].GetNumber())
        star = int(arg[3][2].GetNumber())
        if needValue <= self.abilityFameWeiWang:
            msg = gameStrings.TEXT_ABILITYTREEPROXY_109 % needValue
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.enableAbilityNode, anNo, star))
        else:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_ABILITYTREEPROXY_112)

    def setFame(self, fameId, value):
        if fameId == const.ABILITY_FAME_TANSUO:
            self.refreshTopBar(value)
        elif fameId == const.ABILITY_FAME_WEIWANG:
            if self.mediator:
                self.mediator.Invoke('setAbilityFameId2', (GfxValue(value), GfxValue(self.abilityFameWeiWang != value)))
                self.abilityFameWeiWang = value

    def refreshTopBar(self, value):
        if self.mediator:
            hideMark = True
            xTmp = 0
            xMax = 0
            phase = 0
            phaseX = 0
            phaseBonus = ''
            valueMax = 0
            sizeLast = 0
            for id, data_item in ATPD.data.iteritems():
                if data_item.get('isOpen', 0) == 0:
                    xMax += sizeLast * 100
                    break
                reqValue = data_item.get('reqValue', 0)
                if hideMark:
                    if value >= valueMax + reqValue:
                        phase = id
                        xTmp += sizeLast * 100
                    else:
                        xTmp += (value - valueMax) * sizeLast * 100.0 / reqValue
                        hideMark = False
                    phaseX += sizeLast
                    phaseBonus = gameStrings.TEXT_ABILITYTREEPROXY_146 % (data_item.get('name', ''), data_item.get('bonus', 0))
                valueMax += reqValue
                xMax += sizeLast * 100
                sizeLast = data_item.get('size', 0)

            xTmp = xTmp * 100.0 / xMax if xTmp < xMax else 100.0
            if hideMark == False:
                phaseX = phaseX * 210 - 9
            self.mediator.Invoke('setAbilityFameId1', (GfxValue(value),
             GfxValue(phase),
             GfxValue(phaseX),
             GfxValue(hideMark),
             GfxValue(gbk2unicode(phaseBonus)),
             GfxValue(xTmp)))

    def setTreeNodeData(self, anNo, star):
        if self.mediator:
            self.mediator.Invoke('setTreeNodeData', (GfxValue(anNo), GfxValue(star)))

    def showTreeNodeEffect(self, anNo):
        if self.mediator:
            self.mediator.Invoke('showTreeNodeEffect', GfxValue(anNo))

    def onGetHint(self, *arg):
        ret = [self.needShowHint, self.hitAnNo]
        return uiUtils.array2GfxAarry(ret, True)

    def showHint(self, anNo):
        self.needShowHint = True
        self.hitAnNo = anNo
        if self.mediator:
            self.mediator.Invoke('showHintEffect', GfxValue(anNo))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ABILITY_TREE)
        self.clearMessageBoxId()

    def clearMessageBoxId(self):
        self.messageBoxId = 0

    def hint(self, key1, key2):
        anNo = ATNRD.data.get((key1, key2), 0)
        if anNo > 0 and self.messageBoxId == 0:
            msg = gameStrings.TEXT_ABILITYTREEPROXY_185
            self.messageBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.showHint, anNo), gameStrings.TEXT_IMPPLAYERTEAM_644, Functor(self.clearMessageBoxId), gameStrings.TEXT_AVATAR_2876_1)
