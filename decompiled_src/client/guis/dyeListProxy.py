#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/dyeListProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import utils
from guis import events
from data import mall_config_data as MCFD
from data import sys_config_data as SCD
from data import item_data as ID
from guis.asObject import DisplayObjectUtils
from guis.asObject import ASObject
from helpers import aspectHelper
from gamestrings import gameStrings
from uiProxy import UIProxy
import uiUtils
from cdata import game_msg_def_data as GMDD
PREVIEW_COLOR_NUM = 5
NAVIGATOR_TARGET = (110151611, 110152559, 110152560)
LIST_POS_RONGGUANG = 108
LIST_POS_NORONGGUANG = 94

class DyeListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DyeListProxy, self).__init__(uiAdapter)
        self.widget = None
        self.item = None
        self.equipPos = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_DYE_LIST, self.hide)

    def registerEvents(self):
        BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onEquipChanged)
        BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.onEquipChanged)

    def onEquipChanged(self, params):
        kind, page, pos, item = params
        if kind == const.RES_KIND_EQUIP:
            if item == None:
                if self.equipPos == pos:
                    self.hide()

    def onWearSucess(self, pos, uuid):
        p = BigWorld.player()
        equipments = p.equipment
        item = None
        for i in xrange(len(equipments)):
            equip = equipments[i]
            if equip and equip.uuid == uuid:
                item = equip

        if item and item.isStorageByWardrobe() and item.isCanDye():
            if gameglobal.rds.ui.wardrobe.widget:
                self.show(pos, item)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_DYE_LIST:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        aspectHelper.getInstance().clearDyeList()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DYE_LIST)

    def show(self, pos, item = None):
        if not gameglobal.rds.configData.get('enableWardrobeMultiDyeScheme', False):
            return
        if item:
            if not item.isCanDye():
                self.hide()
                return
        else:
            self.hide()
            return
        self.item = item
        self.equipPos = pos
        if not self.widget or not self.widget.stage:
            self.uiAdapter.loadWidget(uiConst.WIDGET_DYE_LIST)
        else:
            self.refreshInfo()

    def initDyeColor(self):
        dyeLists = MCFD.data.get('dyeLists', [(), ('255,0,0,255', '255,0,0,255'), ('0,255,0,255', '0,255,0,255')])
        for i in xrange(PREVIEW_COLOR_NUM):
            previewMc = self.widget.getChildByName('review%d' % i)
            previewMc.data = i
            previewMc.addEventListener(events.BUTTON_CLICK, self.onColorBtnClick, False, 0, True)
            if len(dyeLists) > i:
                dyeList = dyeLists[i]
                if dyeList:
                    previewMc.visible = True
                    color = dyeList[0]
                    color = color.split(',')
                    color = [ (int(item) if int(item) <= 255 else 255) for item in color ]
                    color = (color[0] << 16) + (color[1] << 8) + color[2]
                    DisplayObjectUtils.fillMcColor(previewMc.colorMc.colorMc, color)
            else:
                previewMc.visible = False

    def onColorBtnClick(self, *args):
        e = ASObject(args[3][0])
        index = int(e.target.data)
        dyeLists = MCFD.data.get('prbDyeLists', [(), ('255,0,0,255', '255,0,0,255'), ('0,255,0,255', '0,255,0,255')])
        dyeList = dyeLists[index]
        aspectHelper.getInstance().previewDye(self.equipPos, dyeList)

    def onGoDyeBtnClick(self, *args):
        targetData = SCD.data.get('dyeNavigatorId', NAVIGATOR_TARGET)
        uiUtils.findPosWithAlert(targetData)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.goDye.addEventListener(events.BUTTON_CLICK, self.onGoDyeBtnClick, False, 0, True)
        self.widget.dyeList.itemRenderer = 'DyeList_dyeItem'
        self.widget.dyeList.labelFunction = self.dyeListLabelFunc
        self.initDyeColor()
        self.addEvent(events.EVENT_ITEM_DYE_SCHEME_CHANGED, self.refreshDyeScheme)

    def refreshDyeScheme(self, param):
        item = param.data
        if item.uuid == self.item.uuid:
            self.item = item
            self.refreshInfo()

    def openExpandWnd(self):
        gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_WARDROBE_DYE_EXPAND, 0)

    def dyeListLabelFunc(self, *args):
        dyeData = ASObject(args[3][0])
        dyeMc = ASObject(args[3][1])
        dyeMc.bgBtn.label = dyeData.label
        dyeMc.bgBtn.selected = self.item.dyeCurrIdx == dyeData.idx
        dyeMc.rongGuangTxt.visible = False
        dyeMc.idx = dyeData.idx
        dyeMc.addEventListener(events.MOUSE_CLICK, self.onDyeListItemClick, False, 0, True)

    def onDyeListItemClick(self, *args):
        e = ASObject(args[3][0])
        schemeIdx = e.currentTarget.idx
        if schemeIdx == -1:
            return
        p = BigWorld.player()
        wearPart = p.getWardrobeItemWearPart(self.item.uuid)
        if wearPart == -1:
            p.base.requireSwitchItemDyeScheme(const.RES_KIND_WARDROBE_BAG, 0, self.item.uuid, schemeIdx)
        else:
            p.base.requireSwitchItemDyeScheme(const.RES_KIND_EQUIP, 0, str(wearPart), schemeIdx)

    def refreshInfo(self):
        if not self.widget or not self.widget.stage:
            return
        self.widget.dyeList.dataArray = self.getSchemInfoArray(self.item)
        rongGuangTxt = self.getRongGuangTxt(self.item)
        if not rongGuangTxt:
            self.widget.rongGuangTxt.visible = False
            self.widget.dyeList.y = LIST_POS_NORONGGUANG
        else:
            self.widget.rongGuangTxt.visible = True
            self.widget.rongGuangTxt.text = rongGuangTxt
            self.widget.dyeList.y = LIST_POS_RONGGUANG

    def getSchemInfoArray(self, item, isAppendAdd = False):
        dyeMaterialsScheme = item.dyeMaterialsScheme
        dyeData = []
        for idx in dyeMaterialsScheme:
            materials = dyeMaterialsScheme.get(idx)
            if idx == 1:
                label = gameStrings.WARDROBE_DYE_DEFAULT
            else:
                label = gameStrings.WARDROBE_DYE_FANGAN % (idx - 1) + self.getDyeDesc(item, materials)
            info = {'label': label,
             'idx': idx}
            dyeData.append(info)

        nextSchemeIdx = item.getNextDyeSchemeIdx()
        if isAppendAdd and nextSchemeIdx:
            info = {'label': gameStrings.WARDROBE_EXPAND_TXT,
             'idx': -1,
             'expandIdx': nextSchemeIdx - 3}
            dyeData.append(info)
        return dyeData

    def getRongGuangTxt(self, i):
        dyeTTLExpireTime = ''
        now = utils.getNow()
        if hasattr(i, 'dyeTTLExpireTime') and i.dyeTTLExpireTime:
            if now < i.dyeTTLExpireTime:
                str = utils.formatDuration(i.dyeTTLExpireTime - now)
                dyeTTLExpireTime = gameStrings.DYELIST_RONGGUANG_REST_TIME + str
        if hasattr(i, 'rongGuangExpireTime') and i.rongGuangExpireTime and now < i.rongGuangExpireTime:
            if dyeTTLExpireTime:
                dyeTTLExpireTime += '\n'
            str = utils.formatDuration(i.rongGuangExpireTime - now)
            dyeTTLExpireTime += gameStrings.DYELIST_RONGGUANG + str
        elif i.isCanRongGuang():
            if dyeTTLExpireTime:
                dyeTTLExpireTime += '\n'
            dyeTTLExpireTime += gameStrings.DYELIST_CAN_RONGGUANG
        return dyeTTLExpireTime

    def getDyeDesc(self, item, materials):
        if item.isFashionEquip():
            dyeDesc = self.addDyeTypeFromChannel(materials, (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_TEXTURE))
        else:
            dyeDesc = self.addDyeTypeFromChannel(materials, (const.DYE_CHANNEL_TEXTURE,))
            if not dyeDesc:
                dyeDesc = self.addDyeTypeFromChannel(materials, (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3))
        return dyeDesc

    def addDyeTypeFromChannel(self, materials, channels):
        dyeDesc = ''
        descArray = ['', '', '']
        lastIndex = -1
        for i, channel in enumerate(channels):
            if channel == const.DYE_CHANNEL_1:
                lastIndex = i
                desc = gameStrings.WARDROBE_ZHU + gameStrings.WARDROBE_NOT_DYE
                descArray[i] = desc
            elif channel == const.DYE_CHANNEL_2:
                lastIndex = i
                desc = gameStrings.WARDROBE_FU + gameStrings.WARDROBE_NOT_DYE
                descArray[i] = desc
            for material in materials:
                if channel == material[0]:
                    lastIndex = i
                    dyeItemId = material[1]
                    dyeMethod = material[2]
                    desc = ID.data.get(dyeItemId, {}).get('name', gameStrings.WARDROBE_NOT_DYE)
                    if dyeMethod == const.DYE_BLEND:
                        desc += gameStrings.WARDROBE_DIEJIA
                    if channel == const.DYE_CHANNEL_1:
                        desc = gameStrings.WARDROBE_ZHU + desc
                    elif channel == const.DYE_CHANNEL_2:
                        desc = gameStrings.WARDROBE_FU + desc
                    descArray[i] = desc
                    break

        if lastIndex != -1:
            dyeDesc = '+'.join(descArray[0:lastIndex + 1])
        return dyeDesc
