#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/relivePosSelectProxy.o
from gamestrings import gameStrings
import BigWorld
import formula
import uiConst
import uiUtils
import const
import gameglobal
import gametypes
import gamelog
from uiProxy import UIProxy
from data import relive_pos_data as RPD

class RelivePosSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RelivePosSelectProxy, self).__init__(uiAdapter)
        self.modelMap = {'selectRelivePos': self.onSelectRelivePos,
         'clickReliveBtn': self.onClickReliveBtn}
        uiAdapter.registerEscFunc(uiConst.WIDGET_RELIVE_SELECT_POS, self.hide)
        self.reset()

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_RELIVE_SELECT_POS)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RELIVE_SELECT_POS)

    def reset(self):
        self.med = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RELIVE_SELECT_POS:
            if self.uiAdapter.deadAndRelive.canSelectRelivePos():
                self.med = mediator
                p = BigWorld.player()
                ww = p.worldWar
                spaceNo = formula.getMapId(p.spaceNo)
                reliveData = RPD.data.get(spaceNo, {})
                relivePos = []
                iconStates = []
                for icon in reliveData.get('icons', []):
                    if p.inWingWarCity():
                        entNo = icon[4]
                        wingWorldCityBuildingMinMap = p.wingWorldMiniMap.buildDic.get(entNo, None)
                        camp = 0
                        selfHostId = p.getOriginHostId()
                        if wingWorldCityBuildingMinMap:
                            camp = 1 if selfHostId == wingWorldCityBuildingMinMap.ownHostId else 2
                        if camp == 1:
                            relivePos.append(icon)
                            iconStates.append(camp)
                        continue
                    if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
                        if p.tempCamp and p.tempCamp == p.bfFortInfo.get(icon[5], {}).get('camp', 0):
                            relivePos.append(icon)
                    else:
                        relivePos.append(icon)
                    if p.inWorldWarEx():
                        reliveBoardId = icon[4]
                        camp = 0
                        hostId = ww.reliveBoard.get(reliveBoardId, 0)
                        if hostId:
                            camp = ww.getCountry(hostId).currCamp
                        iconStates.append(camp)

                initData = {'mapPath': 'relivePosMap/%s.dds' % reliveData.get('res', 0),
                 'relivePos': relivePos,
                 'iconStates': iconStates}
                if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT) or p.inWingWarCity():
                    initData['showReliveBtn'] = True
                    initData['reliveBtnLabel'] = gameStrings.TEXT_RELIVEPOSSELECTPROXY_74
                return uiUtils.dict2GfxDict(initData, True)

    def onSelectRelivePos(self, *args):
        index = int(args[3][0].GetNumber())
        p = BigWorld.player()
        if p.inWorldWarEx():
            p.cell.worldWarReliveTo(index)
        elif p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
            p.cell.reliveInFortBattleField(index)
        elif p.inWingWarCity():
            if p.life == gametypes.LIFE_DEAD:
                gamelog.info('jbx:cell.wingWorldWarReliveTo', index)
                p.cell.wingWorldWarReliveTo(index)
            else:
                gamelog.info('jbx:wingWorldWarTeleportToOwnerReliveBoard', index)
                p.cell.wingWorldWarTeleportToOwnerReliveBoard(index)
        else:
            p.cell.reliveToPosition(index)
        self.hide()

    def onClickReliveBtn(self, *args):
        self.hide()
        p = BigWorld.player()
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
            gameglobal.rds.ui.deadAndRelive.reliveInCommonBattleField()
        elif p.inWingWarCity():
            p.cell.wingWorldWarReliveTo(p.wingWorldMiniMap.hostMinMap.defaultReliveBoardEntNo)
