#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldBuildingProxy.o
import BigWorld
import wingWorldUtils
import const
import uiConst
import events
import gamelog
import gametypes
import utils
from gamestrings import gameStrings
from guis import uiUtils
from guis import ui
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis.asObject import ASUtils
from guis.asObject import ASObject
from data import wing_world_city_data as WWCD
from data import wing_world_config_data as WWCFGD
from data import wing_city_building_data as WCBD
from data import wing_world_country_title_data as WWCTD
from data import wing_city_building_entity_data as WCBED
from data import region_server_config_data as RSCD
from cdata import game_msg_def_data as GMDD
POST_ID_TO_FRAME_NAME_DIC = {1: 'shengjian',
 2: 'yanchui',
 3: 'shuangji'}

class WingWorldBuildingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldBuildingProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.mapIconList = []
        self.selectedCityKey = 0
        self.widget = None
        self.lastSelectedIcon = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.selectedCityKey = 0
        if self.widget and self.widget.map:
            for iconMc in self.mapIconList:
                self.widget.map.removeChild(iconMc)

        self.widget = None

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.map.mapIcon.fitSize = True
        self.widget.map.mapIcon.loadImage('wingWorld/%s.dds' % WWCFGD.data.get('wingWorldStrategyMap', ''))
        self.widget.adminGuiildBtn.addEventListener(events.BUTTON_CLICK, self.handleAdminGuildBtnClick, False, 0, True)
        self.widget.scrollWndList.itemRenderer = 'WingWorldBuildin_ItemRender'
        self.widget.scrollWndList.labelFunction = self.labelFunction
        self.widget.scrollWndList.dataArray = []
        p = BigWorld.player()
        self.widget.campName.text = ''
        if p.isWingWorldCampMode():
            self.widget.scoreTitle.text = gameStrings.WING_WORLD_CAMP_SCORE_TITLE
            selfSide = p.wingWorld.country.getOwnCamp()
            self.widget.campName.text = utils.getWingCampName(p.wingWorldCamp)
            self.widget.adminGuiildBtn.visible = False
        else:
            self.widget.scoreTitle.text = gameStrings.WING_WORLD_CITY_SCORE_TITLE
            self.widget.adminGuiildBtn.visible = True
            selfSide = p.wingWorld.country.getOwn()
        groupId = RSCD.data.get(BigWorld.player().getOriginHostId(), {}).get('wingWorldGroupId', 0)
        self.widget.txtCityPoint.text = gameStrings.WING_WORLD_COUNTRY_POINTS % selfSide.getCityScore(groupId)
        if p.isWingWorldCampMode() or not selfSide.titleLevel:
            self.widget.titleLevel.visible = False
        else:
            self.widget.titleLevel.visible = True
            self.widget.titleLevel.gotoAndStop('titleLevel%d' % selfSide.titleLevel)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshCityMap()
        self.refreshCityInfo()

    def refreshCityMap(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            wingWorld = BigWorld.player().wingWorld
            for iconMc in self.mapIconList:
                self.widget.map.removeChild(iconMc)

            self.mapIconList = []
            p = BigWorld.player()
            for cityId, cfgData in WWCD.data.iteritems():
                iconMc = None
                if p.isWingWorldCampMode():
                    ownerCampId = wingWorldUtils.getCityOwnerHostId(cityId)
                    if p.wingWorldCamp and ownerCampId == p.wingWorldCamp:
                        iconMc = self.widget.getInstByClsName('WingWorldBuildin_Self')
                        iconMc.icon.visible = False
                    elif ownerCampId:
                        iconMc = self.widget.getInstByClsName('WingWorldBuildin_Attack')
                    else:
                        iconMc = self.widget.getInstByClsName('WingWorldBuildin_NoOwner')
                        ASUtils.setHitTestDisable(iconMc.bg, True)
                    if p.wingWorldCamp and ownerCampId == p.wingWorldCamp:
                        iconMc.addEventListener(events.MOUSE_CLICK, self.handleIconClick, False, 0, True)
                    else:
                        iconMc.removeEventListener(events.MOUSE_CLICK, self.handleIconClick)
                else:
                    ownerHostId = wingWorldUtils.getCityOwnerHostId(cityId)
                    if ownerHostId == p.getOriginHostId():
                        iconMc = self.widget.getInstByClsName('WingWorldBuildin_Self')
                        iconMc.icon.visible = False
                    elif ownerHostId:
                        iconMc = self.widget.getInstByClsName('WingWorldBuildin_Attack')
                    else:
                        iconMc = self.widget.getInstByClsName('WingWorldBuildin_NoOwner')
                        ASUtils.setHitTestDisable(iconMc.bg, True)
                    if ownerHostId == p.getOriginHostId():
                        iconMc.addEventListener(events.MOUSE_CLICK, self.handleIconClick, False, 0, True)
                    else:
                        iconMc.removeEventListener(events.MOUSE_CLICK, self.handleIconClick)
                self.widget.map.addChild(iconMc)
                iconMc.name = 'city%d' % cityId
                iconMc.data = cityId
                self.mapIconList.append(iconMc)
                pos = cfgData.get('pos', (0, 0))
                iconMc.x = pos[0] - 25
                iconMc.y = pos[1] - 70
                TipManager.addTip(iconMc.cityIcon, WWCD.data.get(cityId, {}).get('name', ''))
                self.lastSelectedIcon = iconMc

            return

    def handleIconClick(self, *args):
        e = ASObject(args[3][0])
        self.doIconClick(e.currentTarget)

    @ui.callFilter(0.5, True)
    def doIconClick(self, currentTarget):
        self.selectedCityKey = int(currentTarget.data)
        gamelog.info('jbx:queryWingWorldFullCityDTO', self.selectedCityKey)
        BigWorld.player().cell.queryWingWorldFullCityDTO(self.selectedCityKey, 0)
        self.refreshCityInfo()
        if self.lastSelectedIcon:
            self.lastSelectedIcon.cityIcon.selected = False
        self.lastSelectedIcon = currentTarget
        self.lastSelectedIcon.cityIcon.selected = True

    def getCityBuildingList(self):
        p = BigWorld.player()
        buildingList = []
        if not self.selectedCityKey:
            return []
        buildingStates = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, self.selectedCityKey).buildingStates
        now = utils.getNow()
        buildingEntList = []
        for entNo, hpInfo in buildingStates.iteritems():
            if not WCBED.data.get(entNo, {}).get('showInPanel', False):
                continue
            hp, tTime = hpInfo
            mhp = WCBED.data.get(entNo, {}).get('mhp', 900000)
            hp = hp * 1.0 / 100 * mhp
            buildingInfo = {}
            buildingId = WCBED.data.get(entNo, {}).get('buildingId', 0)
            cfgData = WCBD.data.get(buildingId, {})
            buildingInfo['linkText'] = WCBED.data.get(entNo, {}).get('linkText', '')
            buildingInfo['slot'] = uiUtils.getGfxItemById(cfgData.get('slotId', 999))
            buildingInfo['name'] = cfgData.get('name', '')
            currentHp = hp + (now - tTime) * 1.0 / 300 * WCBED.data.get(entNo, {}).get('hpRegen', 200)
            buildingInfo['hpPercent'] = min(100, 100 * currentHp / mhp)
            buildingInfo['lv'] = 1
            buildingList.append(buildingInfo)
            buildingEntList.append(entNo)

        for entNo, entData in WCBED.data.iteritems():
            if not entData.get('showInPanel', False) or entNo in buildingEntList or entData.get('cityType', 1) == const.WING_CITY_TYPE_WAR:
                continue
            if entData.has_key('cityId') and (entData['cityId'] == 0 or entData['cityId'] == self.selectedCityKey):
                buildingInfo = {}
                buildingId = WCBED.data.get(entNo, {}).get('buildingId', 0)
                cfgData = WCBD.data.get(buildingId, {})
                buildingInfo['linkText'] = WCBED.data.get(entNo, {}).get('linkText', '')
                buildingInfo['slot'] = uiUtils.getGfxItemById(cfgData.get('slotId', 999))
                buildingInfo['name'] = cfgData.get('name', '')
                buildingInfo['hpPercent'] = 100
                buildingInfo['lv'] = 1
                buildingList.append(buildingInfo)
                buildingEntList.append(entNo)

        return buildingList

    def refreshCityInfo(self):
        if not self.widget:
            return
        self.widget.txtCityname.text = WWCD.data.get(self.selectedCityKey, {}).get('name', '')
        buildingList = self.getCityBuildingList()
        if not buildingList:
            self.widget.txtCityname.text = gameStrings.WING_WORLD_TAB_STRATEGY_NOT_SELECTED
        self.widget.scrollWndList.dataArray = buildingList

    def labelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.linkText = itemData.linkText
        itemMc.itemSlot.dragable = False
        itemMc.itemSlot.setItemSlotData(itemData.slot)
        ASUtils.setHitTestDisable(itemMc.itemSlot, True)
        itemMc.txtBuildingName.text = itemData.name
        itemMc.txtLv.text = 'Lv %d' % int(itemData.lv)
        itemMc.progressBar.currentValue = int(itemData.hpPercent)
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)

    def handleItemClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.linkText:
            gamelog.info('jbx:doLinkClick', e.currentTarget.linkText)
            self.uiAdapter.doLinkClick(e.currentTarget.linkText, uiConst.LEFT_BUTTON)

    def test(self):
        p = BigWorld.player()
        buildingStates = p.wingWorld.city.getCity(0, 1).buildingStates
        buildingStates[20016] = (898000, utils.getNow() - 240)

    def handleAdminGuildBtnClick(self, *args):
        if not self.selectedCityKey:
            BigWorld.player().showGameMsg(GMDD.data.WING_WORLD_CITY_NO_SELECTED, ())
            return
        self.uiAdapter.wingWorldAdminGuild.show(self.selectedCityKey)
