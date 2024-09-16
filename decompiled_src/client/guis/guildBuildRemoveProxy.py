#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBuildRemoveProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import uiUtils
import uiConst
from uiProxy import UIProxy
from callbackHelper import Functor
from data import guild_building_data as GBD
from data import guild_building_upgrade_data as GBUD
from data import guild_building_marker_data as GBMD

class GuildBuildRemoveProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBuildRemoveProxy, self).__init__(uiAdapter)
        self.modelMap = {'levelDown': self.onLevelDown}
        self.mediator = None
        self.markerId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BUILD_REMOVE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_BUILD_REMOVE:
            self.mediator = mediator
            self.setInitData()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BUILD_REMOVE)

    def reset(self):
        self.markerId = 0

    def hideByMarkerId(self, markerId):
        if self.mediator and self.markerId == markerId:
            self.hide()

    def show(self, markerId):
        self.markerId = markerId
        guild = BigWorld.player().guild
        if not guild:
            return
        else:
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID) if marker.buildingNUID else None
            if not buildValue or buildValue.level <= 0:
                return
            if buildValue.buildingId not in (gametypes.GUILD_BUILDING_FARMHOUSE_ID, gametypes.GUILD_BUILDING_HOUSE_ID):
                return
            if self.mediator:
                self.setInitData()
                self.mediator.Invoke('swapPanelToFront')
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BUILD_REMOVE)
            return

    def setInitData(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID) if marker.buildingNUID else None
            if not buildValue or buildValue.level <= 0:
                return
            levelNow = buildValue.level
            baseData = GBD.data.get(buildValue.buildingId, {})
            baseMarkerData = GBMD.data.get(self.markerId, {})
            dataNow = GBUD.data.get((buildValue.buildingId, levelNow), {})
            dataNext = GBUD.data.get((buildValue.buildingId, levelNow - 1), {})
            dataList = []
            dataList.append('guildBuildUpgrade/%d.dds' % dataNow.get('icon', 100))
            if levelNow > 1:
                dataList.append('guildBuildUpgrade/%d.dds' % dataNext.get('icon', 100))
            else:
                dataList.append('guildBuildUpgrade/%d.dds' % baseMarkerData.get('icon', 100))
            dataList.append(gameStrings.TEXT_FISHGROUP_126 % (baseData.get('name', ''), levelNow))
            if levelNow > 1:
                nameNext = gameStrings.TEXT_FISHGROUP_126 % (baseData.get('name', ''), levelNow - 1)
            else:
                nameNext = baseMarkerData.get('name', '')
            dataList.append(nameNext)
            dataList.append(dataNow.get('description', gameStrings.TEXT_BATTLEFIELDPROXY_1605))
            if levelNow > 1:
                desNext = dataNext.get('description', gameStrings.TEXT_BATTLEFIELDPROXY_1605)
            else:
                desNext = baseMarkerData.get('desc', '')
            dataList.append(desNext)
            costNow = {}
            costNow['cash'] = dataNow.get('maintainBindCash', 0)
            costNow['wood'] = dataNow.get('maintainWood', 0)
            costNow['mojing'] = dataNow.get('maintainMojing', 0)
            costNow['xirang'] = dataNow.get('maintainXirang', 0)
            dataList.append(costNow)
            costNext = {}
            costNext['cash'] = dataNext.get('maintainBindCash', 0)
            costNext['wood'] = dataNext.get('maintainWood', 0)
            costNext['mojing'] = dataNext.get('maintainMojing', 0)
            costNext['xirang'] = dataNext.get('maintainXirang', 0)
            dataList.append(costNext)
            dataList.append(gameStrings.TEXT_GUILDBUILDREMOVEPROXY_113 % (gameStrings.TEXT_GUILDBUILDREMOVEPROXY_113_1 if levelNow > 1 else gameStrings.TEXT_GUILDBUILDREMOVEPROXY_113_2))
            dataList.append(gameStrings.TEXT_GUILDBUILDREMOVEPROXY_114 if levelNow > 1 else gameStrings.TEXT_GUILDBUILDREMOVEPROXY_114_1)
            self.mediator.Invoke('setInitData', uiUtils.array2GfxAarry(dataList, True))
            self.setConditionData()

    def setConditionData(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID) if marker.buildingNUID else None
            if not buildValue or buildValue.level <= 0:
                return
            baseData = GBD.data.get(buildValue.buildingId, {})
            info = {}
            enabledState = True
            info['stability'] = baseData.get('removeStability', 0)
            info['stabilityHave'] = guild.stability
            if info['stability'] > info['stabilityHave']:
                info['stabilityHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['stabilityHaveColor'] = '0xFFFFE7'
            consumeItems = baseData.get('removeConsumeItems', None)
            if consumeItems:
                itemId, itemNum = consumeItems[0]
                itemNumHave = p.inv.countItemInPages(itemId, enableParentCheck=True)
                info['itemNum'] = 'x%d' % itemNum
                info['itemNumHave'] = 'x%d' % itemNumHave
                if itemNum > itemNumHave:
                    info['itemNumHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['itemNumHaveColor'] = '0xFFFFE7'
                info['itemId'] = itemId
                info['itemName'] = uiUtils.getItemColorName(itemId)
            else:
                info['itemNum'] = 0
            hint = ''
            if buildValue.buildingId == gametypes.GUILD_BUILDING_FARMHOUSE_ID:
                nowNum = guild._getPopulation()
                needNum = guild._getMaxPopulation(-1)
                if nowNum > needNum:
                    hint = uiUtils.toHtml(gameStrings.TEXT_GUILDBUILDREMOVEPROXY_165 % needNum, '#F43804')
                    enabledState = False
                else:
                    hint = uiUtils.toHtml(gameStrings.TEXT_GUILDBUILDREMOVEPROXY_165 % needNum, '#79C725')
            elif buildValue.buildingId == gametypes.GUILD_BUILDING_HOUSE_ID:
                nowNum = len(guild.member)
                needNum = guild._getMaxMember(-1)
                if nowNum > needNum:
                    hint = uiUtils.toHtml(gameStrings.TEXT_GUILDBUILDREMOVEPROXY_173 % needNum, '#F43804')
                    enabledState = False
                else:
                    hint = uiUtils.toHtml(gameStrings.TEXT_GUILDBUILDREMOVEPROXY_173 % needNum, '#79C725')
            info['hint'] = hint if hint != '' else gameStrings.TEXT_BATTLEFIELDPROXY_1605
            info['levelDownState'] = enabledState
            self.mediator.Invoke('setConditionData', uiUtils.dict2GfxDict(info, True))

    def onLevelDown(self, *arg):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_GUILDBUILDREMOVEPROXY_184, Functor(BigWorld.player().cell.removeGuildBuilding, self.markerId))
