#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryPlanSettingProxy.o
import BigWorld
from Scaleform import GfxValue
import uiUtils
import gametypes
import gameglobal
import uiConst
import const
import pinyinConvert
import events
from ui import gbk2unicode
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASObject
from asObject import ASUtils
from callbackHelper import Functor
from data import marriage_config_data as MCDD
from data import marriage_package_data as MPD
from data import marriage_theme_data as MTD
from data import marriage_fenwei_data as MFD
from data import marriage_chedui_data as MCD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
PLAN_BTN_NUM = 4
PLAN_BTN_NUM_ENABLED = 4

class MarryPlanSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryPlanSettingProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.selectedBtn = None
        self.dropMenuDict = {}

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.mainMc.descList.itemRenderer = 'MarryPlanSetting_DescItem'
        self.widget.mainMc.descList.lableFunction = self.descListItemFunction
        self.widget.mainMc.descList.itemHeightFunction = self.descListItemHeightFunction
        self.widget.mainMc.downList.itemRenderer = 'MarryPlanSetting_DownItem'
        self.widget.mainMc.downList.lableFunction = self.downListItemFunction
        self.widget.mainMc.downList.column = 2
        self.widget.mainMc.downList.itemHeight = 28
        self.widget.mainMc.downList.itemWidth = 311
        self.widget.mainMc.downList.dataArray = []
        self.widget.mainMc.downList.addEventListener(events.SCROLL, self.handleScrollDropDown, False, 0, True)
        self.widget.mainMc.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        for i in xrange(0, PLAN_BTN_NUM):
            btn = getattr(self.widget.mainMc, 'planBtn' + str(i))
            if btn:
                btn.data = i
                btn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
                btn.enabled = i < PLAN_BTN_NUM_ENABLED

        basePackageBtn = [self.widget.mainMc.planBtn0, self.widget.mainMc.planBtn1, self.widget.mainMc.planBtn2]
        for i, btn in enumerate(basePackageBtn):
            btnName = MPD.data.get((gametypes.MARRIAGE_TYPE_PACKAGE, i + 1), {}).get('totalPrice', '')
            btn.label = btnName

        self.widget.mainMc.planBtn3.label = MPD.data.get((gametypes.MARRIAGE_TYPE_GREAT, gametypes.MARRIAGE_GREAT_SUB_TYPE_DEFAULT), {}).get('totalPrice', '')
        mType, subType = self.uiAdapter.marrySettingBg.getCurServerMarriageType()
        self.setSelIndex(self.getRealSelectType(mType, subType) - 1)

    def refreshInfo(self):
        if self.hasBaseData():
            self.refreshPlanBtn()
            self.refreshDownList()
            self.refreshDescList()

    def refreshPlanBtn(self):
        if self.hasBaseData():
            mType, subType = self.uiAdapter.marrySettingBg.getCurServerMarriageType()
            for i in xrange(0, PLAN_BTN_NUM):
                btn = getattr(self.widget.mainMc, 'planBtn' + str(i))
                if btn:
                    btn.enabled = i < PLAN_BTN_NUM_ENABLED and i >= self.getRealSelectType(mType, subType) - 1
                    btn.orderMc.visible = i == self.getRealSelectType(mType, subType) - 1

            self.widget.mainMc.planBtn3.enabled = self.widget.mainMc.planBtn3.enabled and gameglobal.rds.configData.get('enableMarriageGreat', False)

    def getCurSelectType(self):
        if self.selectedBtn:
            return int(self.selectedBtn.data) + 1

    def getDescData(self):
        dArray = []
        marriageType = self.getMarriageType()
        mData = MPD.data.get(marriageType, {})
        for i, desc in enumerate(mData.get('changeDesc', ())):
            info = {'desc': desc,
             'index': i}
            dArray.append(info)

        return dArray

    def descListItemFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if info and itemMc:
            itemMc.descTxt.htmlText = info.desc

    def descListItemHeightFunction(self, *arg):
        if self.hasBaseData():
            info = ASObject(arg[3][0])
            descItem = self.widget.getInstByClsName('MarryPlanSetting_DescItem')
            descItem.descTxt.htmlText = info.desc
            return GfxValue(descItem.descTxt.textHeight)

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def refreshDownList(self):
        if self.hasBaseData():
            dataList = self.getDownListData()
            self.widget.mainMc.downList.dataArray = dataList
            self.widget.mainMc.downList.validateNow()

    def refreshDescList(self):
        if self.hasBaseData():
            dataList = self.getDescData()
            self.widget.mainMc.descList.dataArray = dataList
            self.widget.mainMc.descList.validateNow()

    def getDownListData(self):
        return [{'type': gametypes.MARRIAGE_PACKAGE_INDEX_ZHUTI},
         {'type': gametypes.MARRIAGE_PACKAGE_INDEX_CHEDUI},
         {'type': gametypes.MARRIAGE_PACKAGE_INDEX_FENWEI},
         {'type': gametypes.MARRIAGE_PACKAGE_INDEX_XL_YIFU},
         {'type': gametypes.MARRIAGE_PACKAGE_INDEX_XN_YIFU},
         {'type': gametypes.MARRIAGE_PACKAGE_INDEX_BL_YIFU},
         {'type': gametypes.MARRIAGE_PACKAGE_INDEX_BN_YIFU}]

    def downListItemFunction(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            titleDesc = {gametypes.MARRIAGE_PACKAGE_INDEX_ZHUTI: gameStrings.MARRY_SETTING_TITLE_ZHUTI,
             gametypes.MARRIAGE_PACKAGE_INDEX_CHEDUI: gameStrings.MARRY_SETTING_TITLE_CHEDUI,
             gametypes.MARRIAGE_PACKAGE_INDEX_FENWEI: gameStrings.MARRY_SETTING_TITLE_FENWEI,
             gametypes.MARRIAGE_PACKAGE_INDEX_XL_YIFU: gameStrings.MARRY_SETTING_TITLE_XL_YIFU,
             gametypes.MARRIAGE_PACKAGE_INDEX_XN_YIFU: gameStrings.MARRY_SETTING_TITLE_XN_YIFU,
             gametypes.MARRIAGE_PACKAGE_INDEX_BL_YIFU: gameStrings.MARRY_SETTING_TITLE_BL_YIFU,
             gametypes.MARRIAGE_PACKAGE_INDEX_BN_YIFU: gameStrings.MARRY_SETTING_TITLE_BN_YIFU}
            itemMc.titleName.htmlText = titleDesc.get(info.type, '')
            zhutiData, fenweiData, xlYifuData, xnYifuData, blYifuData, bnYifuData, cheduiData = self.uiAdapter.marrySettingBg.getCurServerPackageList()
            tmpData = {gametypes.MARRIAGE_PACKAGE_INDEX_ZHUTI: zhutiData,
             gametypes.MARRIAGE_PACKAGE_INDEX_CHEDUI: cheduiData,
             gametypes.MARRIAGE_PACKAGE_INDEX_FENWEI: fenweiData,
             gametypes.MARRIAGE_PACKAGE_INDEX_XL_YIFU: xlYifuData,
             gametypes.MARRIAGE_PACKAGE_INDEX_XN_YIFU: xnYifuData,
             gametypes.MARRIAGE_PACKAGE_INDEX_BL_YIFU: blYifuData,
             gametypes.MARRIAGE_PACKAGE_INDEX_BN_YIFU: bnYifuData}
            self.dropMenuDict[info.type] = itemMc.downMenu
            itemMc.downMenu.dropDownLayer = 1
            itemMc.downMenu.addEventListener(events.INDEX_CHANGE, self.handleSelectDropMenu, False, 0, True)
            dData = self.refreshDropMenuData(info.type)
            itemMc.dataType = info.type
            itemMc.previewBtn.addEventListener(events.BUTTON_CLICK, self.handlePreviewBtnClick, False, 0, True)
            itemMc.downMenu.selectedIndex = self.getEnabledIndex(dData, tmpData.get(info.type, 1))

    def getEnabledIndex(self, dataList, index):
        for i, data in enumerate(dataList):
            if data.get('rendererEnabled', True) and data.get('index', 0) == index:
                return i

        return 0

    def handleSelectDropMenu(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.currentTarget
            itemMc = t.parent
            if itemMc.dataType == gametypes.MARRIAGE_PACKAGE_INDEX_ZHUTI:
                refreshDropMenuType = [gametypes.MARRIAGE_PACKAGE_INDEX_CHEDUI,
                 gametypes.MARRIAGE_PACKAGE_INDEX_FENWEI,
                 gametypes.MARRIAGE_PACKAGE_INDEX_XL_YIFU,
                 gametypes.MARRIAGE_PACKAGE_INDEX_XN_YIFU,
                 gametypes.MARRIAGE_PACKAGE_INDEX_BL_YIFU,
                 gametypes.MARRIAGE_PACKAGE_INDEX_BN_YIFU]
                for _type in refreshDropMenuType:
                    self.refreshDropMenuData(_type)

    def refreshDropMenuData(self, dataType):
        dData = []
        marriageType = self.getMarriageType()
        mData = MPD.data.get(marriageType, {})
        dropMenu = self.dropMenuDict.get(dataType, None)
        if not dropMenu:
            return dData
        else:
            oldIndex = dropMenu.selectedIndex
            if dataType == gametypes.MARRIAGE_PACKAGE_INDEX_ZHUTI:
                zhutiIds = mData.get('zhuti', ())
                for i, zId in enumerate(zhutiIds):
                    _data = MTD.data.get(zId, {})
                    _info = {'label': _data.get('name', ''),
                     'index': i + 1,
                     'data': zId}
                    dData.append(_info)

            curZhutiData = self.getDataFromType(gametypes.MARRIAGE_PACKAGE_INDEX_ZHUTI)
            zData = MTD.data.get(curZhutiData.data, {}) if curZhutiData else None
            if zData:
                if dataType == gametypes.MARRIAGE_PACKAGE_INDEX_CHEDUI:
                    cheduiIds = mData.get('chedui', ())
                    zCheduiIds = zData.get('chedui', ())
                    for i, cId in enumerate(cheduiIds):
                        if cId not in zCheduiIds:
                            continue
                        _data = MCD.data.get(cId, {})
                        _info = {'label': _data.get('name', ''),
                         'index': i + 1,
                         'data': cId}
                        dData.append(_info)

                elif dataType == gametypes.MARRIAGE_PACKAGE_INDEX_FENWEI:
                    fenweiIds = mData.get('fenwei', ())
                    zFenweiIds = zData.get('fenwei', ())
                    for i, fId in enumerate(fenweiIds):
                        if fId not in zFenweiIds:
                            continue
                        _data = MFD.data.get(fId, {})
                        _info = {'label': _data.get('name', ''),
                         'index': i + 1,
                         'data': fId}
                        dData.append(_info)

                elif dataType == gametypes.MARRIAGE_PACKAGE_INDEX_XL_YIFU:
                    itemIds = mData.get('xlYifu', ())
                    zItemIds = zData.get('xlYifu', ())
                    for i, itemId in enumerate(itemIds):
                        if itemId not in zItemIds:
                            continue
                        _data = ID.data.get(itemId, {})
                        _info = {'label': _data.get('name', ''),
                         'index': i + 1,
                         'data': itemId}
                        dData.append(_info)

                elif dataType == gametypes.MARRIAGE_PACKAGE_INDEX_XN_YIFU:
                    itemIds = mData.get('xnYifu', ())
                    zItemIds = zData.get('xnYifu', ())
                    for i, itemId in enumerate(itemIds):
                        if itemId not in zItemIds:
                            continue
                        _data = ID.data.get(itemId, {})
                        _info = {'label': _data.get('name', ''),
                         'index': i + 1,
                         'data': itemId}
                        dData.append(_info)

                elif dataType == gametypes.MARRIAGE_PACKAGE_INDEX_BL_YIFU:
                    itemIds = mData.get('blYifu', ())
                    zItemIds = zData.get('blYifu', ())
                    for i, itemId in enumerate(itemIds):
                        if itemId not in zItemIds:
                            continue
                        _data = ID.data.get(itemId, {})
                        _info = {'label': _data.get('name', ''),
                         'index': i + 1,
                         'data': itemId}
                        dData.append(_info)

                elif dataType == gametypes.MARRIAGE_PACKAGE_INDEX_BN_YIFU:
                    itemIds = mData.get('bnYifu', ())
                    zItemIds = zData.get('bnYifu', ())
                    for i, itemId in enumerate(itemIds):
                        if itemId not in zItemIds:
                            continue
                        _data = ID.data.get(itemId, {})
                        _info = {'label': _data.get('name', ''),
                         'index': i + 1,
                         'data': itemId}
                        dData.append(_info)

            dropMenu.menuRowCount = len(dData) if len(dData) < 5 else 5
            ASUtils.setDropdownMenuData(dropMenu, dData)
            dropMenu.selectedIndex = self.getEnabledIndex(dData, oldIndex)
            return dData

    def handleScrollDropDown(self, *arg):
        if self.hasBaseData():
            items = self.widget.mainMc.downList.items
            for itemMc in items:
                itemMc.downMenu.close()

    def setSelIndex(self, index):
        if not self.hasBaseData():
            return
        if self.selectedBtn:
            self.selectedBtn.selected = False
        btn = getattr(self.widget.mainMc, 'planBtn' + str(int(index)))
        if btn:
            self.selectedBtn = btn
            self.selectedBtn.selected = True
        self.refreshInfo()

    def handleBtnClick(self, *arg):
        e = ASObject(arg[3][0])
        t = e.target
        self.setSelIndex(t.data)

    def handleConfirmBtnClick(self, *arg):
        p = BigWorld.player()
        packageList = self.getCurSelectData()
        tgtmType, tgtSubType = self.getMarriageType()
        mType, subType = self.uiAdapter.marrySettingBg.getCurServerMarriageType()
        oPackageList = self.uiAdapter.marrySettingBg.getCurServerPackageList()
        if mType != tgtmType:
            p.showGameMsg(GMDD.data.MARRIAGE_UPGRADE_FORBID_MTYPE, ())
        elif tgtSubType != subType or packageList != oPackageList:
            p.cell.setMarriagePackageInfoCheck(tgtmType, tgtSubType, packageList)

    def getCurSelectData(self):
        items = self.widget.mainMc.downList.items
        zhutiData = 0
        fenweiData = 0
        xlYifuData = 0
        xnYifuData = 0
        blYifuData = 0
        bnYifuData = 0
        cheduiData = 0
        for i, itemMc in enumerate(items):
            info = self.widget.mainMc.downList.dataArray[i]
            data = itemMc.downMenu.dataProvider[itemMc.downMenu.selectedIndex]
            if info.type == gametypes.MARRIAGE_PACKAGE_INDEX_ZHUTI:
                zhutiData = data.index
            elif info.type == gametypes.MARRIAGE_PACKAGE_INDEX_CHEDUI:
                cheduiData = data.index
            elif info.type == gametypes.MARRIAGE_PACKAGE_INDEX_FENWEI:
                fenweiData = data.index
            elif info.type == gametypes.MARRIAGE_PACKAGE_INDEX_XL_YIFU:
                xlYifuData = data.index
            elif info.type == gametypes.MARRIAGE_PACKAGE_INDEX_XN_YIFU:
                xnYifuData = data.index
            elif info.type == gametypes.MARRIAGE_PACKAGE_INDEX_BL_YIFU:
                blYifuData = data.index
            elif info.type == gametypes.MARRIAGE_PACKAGE_INDEX_BN_YIFU:
                bnYifuData = data.index

        return [zhutiData,
         fenweiData,
         xlYifuData,
         xnYifuData,
         blYifuData,
         bnYifuData,
         cheduiData]

    def getDataFromType(self, dataType):
        dropMenu = self.dropMenuDict.get(dataType, None)
        if not dropMenu:
            return
        elif dropMenu.selectedIndex >= 0 and dropMenu.selectedIndex < len(dropMenu.dataProvider):
            return dropMenu.dataProvider[dropMenu.selectedIndex]
        else:
            return

    def handlePreviewBtnClick(self, *arg):
        if self.hasBaseData():
            e = ASObject(arg[3][0])
            t = e.currentTarget
            itemMc = t.parent
            data = itemMc.downMenu.dataProvider[itemMc.downMenu.selectedIndex]
            gameglobal.rds.ui.marryPlanPreview.show(itemMc.dataType, itemMc.downMenu.dataProvider, itemMc.downMenu.selectedIndex)

    def onUpgradeFunc(self, srcSubType, tgtSubType, deltaDict):
        p = BigWorld.player()
        srcName = MPD.data.get((1, srcSubType), {}).get('name', '')
        tgtName = MPD.data.get((1, tgtSubType), {}).get('name', '')
        marryType = self.getMarriageType()
        mType, subType = marryType[0], marryType[1]
        packageList = self.getCurSelectData()
        itemId = MCDD.data.get('costItemId', 0)
        itemData = uiUtils.getGfxItemById(itemId)
        count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
        deltaCount = deltaDict.get(itemId, 0)
        itemData['count'] = uiUtils.convertNumStr(count, deltaCount)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.MARRIAGE_UPGRADE_MSG % (srcName, tgtName), Functor(p.cell.updateMarriagePackageInfo, mType, subType, packageList), yesBtnText=gameStrings.COMMON_CONFIRM, itemData=itemData, style=uiConst.MSG_BOX_BUY_ITEM)

    def getMarriageType(self):
        if self.getCurSelectType() == 4:
            marriageType = (gametypes.MARRIAGE_TYPE_GREAT, gametypes.MARRIAGE_GREAT_SUB_TYPE_DEFAULT)
        else:
            marriageType = (gametypes.MARRIAGE_TYPE_PACKAGE, self.getCurSelectType())
        return marriageType

    def getRealSelectType(self, mType, subType):
        if mType == gametypes.MARRIAGE_TYPE_PACKAGE:
            return subType
        if mType == gametypes.MARRIAGE_TYPE_GREAT:
            return 4

    def setMenuIndex(self, dataType, selIndex):
        downMenu = self.dropMenuDict[dataType]
        if downMenu:
            downMenu.selectedIndex = selIndex
