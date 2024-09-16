#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBuildUpgradeProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import const
import commGuild
import uiUtils
import uiConst
from callbackHelper import Functor
from uiProxy import UIProxy
from helpers import guild as guildUtils
from cdata import game_msg_def_data as GMDD
from data import guild_building_data as GBD
from data import guild_building_upgrade_data as GBUD
from data import guild_building_marker_data as GBMD
from data import guild_scale_data as GSCD
from data import guild_job_data as GJD

class GuildBuildUpgradeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBuildUpgradeProxy, self).__init__(uiAdapter)
        self.modelMap = {'beginUpgrade': self.onBeginUpgrade,
         'cancelUpgrade': self.onCancelUpgrade,
         'clickResident': self.onClickResident,
         'clickChange': self.onClickChange}
        self.mediator = None
        self.markerId = 0
        self.buildingNUID = 0
        self.npcId = 0
        self.buildingId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BUILD_UPGRADE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_BUILD_UPGRADE:
            self.mediator = mediator
            self.setInitData()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BUILD_UPGRADE)

    def show(self, markerId = 0, buildingNUID = 0, npcId = 0, buildingId = 0):
        self.markerId = markerId
        self.buildingNUID = buildingNUID
        self.npcId = npcId
        self.buildingId = buildingId
        self._updateBuildingNUID()
        if not markerId:
            building = self._getBuilding()
            if building:
                self.markerId = building.markerId
        if self.mediator:
            if self.checkBuildingIsMaxLevel():
                self.hide()
                return
            self.setInitData()
            self.mediator.Invoke('swapPanelToFront')
        elif self.checkBuildingIsMaxLevel():
            BigWorld.player().showGameMsg(GMDD.data.GUILD_BUILDING_MAX_LEVEL, ())
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BUILD_UPGRADE)

    def clearNpcId(self):
        self.npcId = 0

    def hideByMarkerIdAndNpcId(self, markerId, npcId):
        if self.markerId == markerId and self.npcId == npcId:
            self.hide()

    def hideByNpcId(self, npcId):
        if self.npcId == npcId:
            self.hide()

    def _getBuilding(self):
        if self.buildingNUID:
            return BigWorld.player().guild.building.get(self.buildingNUID)
        else:
            return None

    def _getBuildingLevel(self):
        buildValue = self._getBuilding()
        return buildValue and buildValue.level or 0

    def _getBuildingId(self):
        if self.markerId:
            guild = BigWorld.player().guild
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID) if marker.buildingNUID else None
            if buildValue:
                return buildValue.buildingId
            elif commGuild.isMultiBuildingMarker(self.markerId):
                return self.buildingId
            else:
                return GBMD.data.get(self.markerId, {}).get('buildingId', 0)
        elif self.buildingNUID:
            buildValue = self._getBuilding()
            if buildValue:
                return buildValue.buildingId
        return 0

    def _getEntity(self):
        if self.npcId:
            e = BigWorld.entities.get(self.npcId)
            return e
        else:
            return BigWorld.player()

    def _updateBuildingNUID(self):
        if self.markerId:
            marker = BigWorld.player().guild.marker.get(self.markerId)
            if marker:
                self.buildingNUID = marker.buildingNUID

    def onBeginUpgrade(self, *arg):
        if not gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_BUILDING):
            BigWorld.player().showGameMsg(GMDD.data.GUILD_AUTHORIZATION_FAILED, ())
            return
        if self.npcId:
            e = BigWorld.entities.get(self.npcId)
            building = self._getBuilding()
            if building:
                if e.__class__.__name__ in ('GuildBuildingMarker', 'GuildDawdler'):
                    e = BigWorld.player()
                e.cell.upgradeGuildBuilding(self.buildingNUID)
            elif self.markerId and commGuild.isMultiBuildingMarker(self.markerId):
                e.cell.createBuilding(self.buildingId)
            else:
                e.cell.createBuilding(0)
        else:
            p = BigWorld.player()
            building = self._getBuilding()
            if building:
                p.cell.upgradeGuildBuilding(self.buildingNUID)
            elif self.markerId and commGuild.isMultiBuildingMarker(self.markerId):
                p.cell.createGuildBuilding(self.markerId, self.buildingId)
            else:
                p.cell.createGuildBuilding(self.markerId, 0)

    def onCancelUpgrade(self, *arg):
        marker = BigWorld.player().guild.marker.get(self.markerId)
        if marker:
            self.cancelUpgradeBuilding(marker.buildingNUID)
        elif self.buildingNUID:
            self.cancelUpgradeBuilding(self.buildingNUID)

    def cancelUpgradeBuilding(self, buildingNUID):
        if not gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_BUILDING):
            BigWorld.player().showGameMsg(GMDD.data.GUILD_AUTHORIZATION_FAILED, ())
            return
        guild = BigWorld.player().guild
        building = guild.building.get(buildingNUID)
        if not building:
            return
        buildingId = building.buildingId
        levelNext = building.level + 1
        dataNext = GBUD.data.get((buildingId, levelNext), {})
        if dataNext.get('bindCash', 0) + guild.bindCash > guild._getMaxBindCash() or dataNext.get('mojing', 0) + guild.mojing > guild._getMaxMojing() or dataNext.get('xirang', 0) + guild.xirang > guild._getMaxXirang() or dataNext.get('wood', 0) + guild.wood > guild._getMaxWood():
            msg = gameStrings.TEXT_GUILDBUILDUPGRADEPROXY_170
        else:
            msg = gameStrings.TEXT_GUILDBUILDUPGRADEPROXY_172
        e = self._getEntity()
        if not e or e.__class__.__name__ in ('GuildBuildingMarker', 'GuildDawdler'):
            e = BigWorld.player()
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(e.cell.cancelUpgradeGuildBuilding, buildingNUID))

    def setInitData(self):
        if self.mediator:
            self._updateBuildingNUID()
            self.buildingId = self._getBuildingId()
            levelNow = self._getBuildingLevel()
            baseData = GBD.data.get(self.buildingId, {})
            dataNow = GBUD.data.get((self.buildingId, levelNow), {})
            dataNext = GBUD.data.get((self.buildingId, levelNow + 1), {})
            dataList = []
            if levelNow == 0:
                dataList.append('guildBuildUpgrade/%d.dds' % dataNext.get('icon', 100))
            else:
                dataList.append('guildBuildUpgrade/%d.dds' % dataNow.get('icon', 100))
            dataList.append('guildBuildUpgrade/%d.dds' % dataNext.get('icon', 100))
            if levelNow > 0:
                nameNow = gameStrings.TEXT_FISHGROUP_126 % (baseData.get('name', ''), levelNow)
            else:
                nameNow = gameStrings.TEXT_GUILDBUILDUPGRADEPROXY_199 % baseData.get('name', '')
            dataList.append(nameNow)
            dataList.append(gameStrings.TEXT_FISHGROUP_126 % (baseData.get('name', ''), levelNow + 1))
            dataList.append(dataNow.get('description', gameStrings.TEXT_BATTLEFIELDPROXY_1605))
            dataList.append(dataNext.get('description', gameStrings.TEXT_BATTLEFIELDPROXY_1605))
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
            self.mediator.Invoke('setInitData', uiUtils.array2GfxAarry(dataList, True))
            building = self._getBuilding()
            if building and building.inUpgrading():
                self.setUpgradeProgress(building.nuid)
            else:
                self.setConditionData()

    def setConditionData(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            buildingId = self._getBuildingId()
            levelNext = self._getBuildingLevel() + 1
            dataNext = GBUD.data.get((buildingId, levelNext), {})
            info = {}
            enabledState = True
            info['cash'] = dataNext.get('bindCash', 0)
            info['cashHave'] = guild.bindCash
            if info['cash'] > info['cashHave']:
                info['cashHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['cashHaveColor'] = '0xFFFFE7'
            info['wood'] = dataNext.get('wood', 0)
            info['woodHave'] = guild.wood
            if info['wood'] > info['woodHave']:
                info['woodHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['woodHaveColor'] = '0xFFFFE7'
            info['mojing'] = dataNext.get('mojing', 0)
            info['mojingHave'] = guild.mojing
            if info['mojing'] > info['mojingHave']:
                info['mojingHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['mojingHaveColor'] = '0xFFFFE7'
            info['xirang'] = dataNext.get('xirang', 0)
            info['xirangHave'] = guild.xirang
            if info['xirang'] > info['xirangHave']:
                info['xirangHaveColor'] = '0xF43804'
                enabledState = False
            else:
                info['xirangHaveColor'] = '0xFFFFE7'
            if buildingId == gametypes.GUILD_BUILDING_MASTER_ID:
                info['levelTextField'] = gameStrings.TEXT_GM_COMMAND_WINGWORLD_490
                scale = dataNext.get('scale', 0)
                scaleHave = guild.scale
                info['level'] = GSCD.data.get(scale).get('name')
                info['levelHave'] = GSCD.data.get(scaleHave).get('name')
                if scale > scaleHave:
                    info['levelHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['levelHaveColor'] = '0xFFFFE7'
            else:
                info['levelTextField'] = gameStrings.TEXT_GUILDBUILDUPGRADEPROXY_287
                level = dataNext.get('masterBuildingLevel', 0)
                if buildingId == gametypes.GUILD_BUILDING_FARMHOUSE_ID or buildingId == gametypes.GUILD_BUILDING_HOUSE_ID:
                    level = max(level, GBMD.data.get(self.markerId, {}).get('glevel', 0))
                info['level'] = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % level
                info['levelHave'] = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % guild.level
                if level > guild.level:
                    info['levelHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['levelHaveColor'] = '0xFFFFE7'
            reqBuildingId = dataNext.get('reqBuildingId', 0)
            reqBuildingLevel = dataNext.get('reqBuildingLevel', 0)
            buildName = GBD.data.get(reqBuildingId, {}).get('name', '')
            if buildName == '':
                info['building'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                info['buildingHave'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                info['buildingHaveColor'] = '0xFFFFE7'
            else:
                marker = guild.marker.get(commGuild.getMarkerIdByBuildingId(guild, reqBuildingId), None)
                buildValue = guild.building.get(marker.buildingNUID, None) if marker else None
                ownLevel = buildValue.level if buildValue else 0
                info['building'] = gameStrings.TEXT_GUILDBUILDUPGRADEPROXY_310 % (buildName, reqBuildingLevel)
                info['buildingHave'] = gameStrings.TEXT_GUILDBUILDUPGRADEPROXY_310 % (buildName, ownLevel)
                if reqBuildingLevel > ownLevel:
                    info['buildingHaveColor'] = '0xF43804'
                    enabledState = False
                else:
                    info['buildingHaveColor'] = '0xFFFFE7'
            info['progressPoint'] = format(dataNext.get('progress', 0), ',')
            info['progressTitleTips'] = gameStrings.TEXT_GUILDBUILDUPGRADEPROXY_319
            consumeItems = dataNext.get('consumeItems', None)
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
            info['levelUpState'] = enabledState
            self.mediator.Invoke('setConditionData', uiUtils.dict2GfxDict(info, True))

    def setUpgradeProgress(self, buildingNUID):
        self._updateBuildingNUID()
        if self.mediator and self.buildingNUID == buildingNUID:
            building = self._getBuilding()
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            marker = guild.marker.get(building.markerId)
            info = {}
            progressMax = GBUD.data.get((building.buildingId, building.level + 1), {}).get('progress', 0)
            currentValue = 100.0
            if progressMax >= building.progress:
                currentValue = currentValue * building.progress / progressMax
                info['upgradeText'] = '%s/%s' % (format(building.progress, ','), format(progressMax, ','))
            else:
                info['upgradeText'] = '%s/%s' % (format(progressMax, ','), format(progressMax, ','))
            info['currentValue'] = currentValue
            info['workLoad'] = gameStrings.TEXT_GUILDASSARTPROXY_145 % marker.getWorkload(guild, ignoreTime=True)
            jobId = commGuild.getJobIdFromGJRD(self.markerId, gametypes.GUILD_JOB_DIFFICULTY_ADVANCED, gametypes.GUILD_JOB_TYPE_UPGRADE)
            info['hintText'] = GJD.data.get(jobId, {}).get('hintText', '')
            manager = marker.getManager(guild, type=gametypes.GUILD_JOB_TYPE_UPGRADE)
            if manager:
                residentManager = guildUtils.createResidentInfo(guild, manager.nuid, size=const.GUILD_RESIDENT_SIZE96)
                guildUtils.addManagerInfo(guild, manager.nuid, residentManager, jobId)
                info['residentManager'] = residentManager
            normalList = []
            for residentNUID in marker.workers:
                residentInfo = guildUtils.createResidentInfo(guild, residentNUID)
                normalList.append(residentInfo)

            info['normalList'] = normalList
            info['normalLimit'] = marker.getBuildingWorkerLimit(guild)
            self.mediator.Invoke('setUpgradeProgress', uiUtils.dict2GfxDict(info, True))

    def upgradeFinish(self, buildingNUID):
        self._updateBuildingNUID()
        if self.mediator and self.buildingNUID == buildingNUID:
            if self.checkBuildingIsMaxLevel():
                self.hide()

    def checkBuildingIsMaxLevel(self):
        building = self._getBuilding()
        buildingId = self._getBuildingId()
        if building != None:
            return building.level >= GBD.data.get(buildingId, {}).get('maxLevel', 0)
        else:
            return False

    def onClickResident(self, *arg):
        isEmpty = arg[3][0].GetBool()
        if isEmpty:
            difficulty = int(arg[3][1].GetNumber())
            jobId = commGuild.getJobIdFromGJRD(self.markerId, difficulty, gametypes.GUILD_JOB_TYPE_UPGRADE)
            gameglobal.rds.ui.guildDispatchInto.show(jobId)
        else:
            residentNUID = int(arg[3][1].GetString())
            gameglobal.rds.ui.guildResident.show(uiConst.GUILD_RESIDENT_PANEL_HIRED, residentNUID)

    def onClickChange(self, *arg):
        jobId = commGuild.getJobIdFromGJRD(self.markerId, gametypes.GUILD_JOB_DIFFICULTY_ADVANCED, gametypes.GUILD_JOB_TYPE_UPGRADE)
        gameglobal.rds.ui.guildDispatchInto.show(jobId)
