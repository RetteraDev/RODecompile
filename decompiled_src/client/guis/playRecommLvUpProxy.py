#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/playRecommLvUpProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import utils
import gametypes
from uiProxy import UIProxy
from guis import ui
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import play_recomm_activity_data as PRAD
from data import play_recomm_config_data as PRCD
PLAY_RECOMM_PATH = 'playRecomm/'
PLAY_RECOMM_TIPS_BG = 'scheduleBg/'
PLAY_RECOMM_ACTIVITY_ICON = PLAY_RECOMM_PATH + 'activityIcon/'
ITEM_PATH = 'item/icon64/'

class PlayRecommLvUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PlayRecommLvUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.selectedId = 0
        self.dataArray = []
        self.prId2DataDic = {}

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.uiAdapter.playRecommActivation.hideActivityTips()
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.lvupPanel.itemList.itemRenderer = 'PlayRecommV2LvUp_PlayRecomm_LvUpItemH'
        self.widget.lvupPanel.itemList.dataArray = []
        self.widget.lvupPanel.itemList.lableFunction = self.fillLvUpPanelItemH
        gameglobal.rds.uiLog.addClickLog(uiConst.WIDGET_PLAY_RECOMM * 100 + 2)

    def getLvUpData(self, *args):
        lvupItems = {}
        pradd = PRAD.data
        for k, aData in pradd.iteritems():
            displayType = aData.get('displayType', ())
            if not displayType:
                continue
            for dType in displayType:
                aList = lvupItems.setdefault(dType, [])
                aItem = self.uiAdapter.playRecomm.genLvUpItemInfo(aData, dType, k)
                if aItem and len(aItem) > 1:
                    aList.append(aItem)

        ret = []
        typeOrder = PRCD.data.get('prActivityTypeOrder', ())
        typeNames = PRCD.data.get('prActivityTypeName', {})
        typeIconBg = PRCD.data.get('prActivityTypeIconBg', {})
        for dType in typeOrder:
            itemList = lvupItems.get(dType, [])
            if not itemList:
                continue
            itemList.sort(self.lvupItemsSortFunc)
            typeInfo = {}
            typeInfo['displayType'] = dType
            typeInfo['displayName'] = typeNames.get(dType, gameStrings.TEXT_PLAYRECOMMLVUPPROXY_81)
            typeInfo['displayIconBg'] = typeIconBg.get(dType, 'blue')
            typeInfo['itemList'] = itemList
            ret.append(typeInfo)

        return ret

    def lvupItemsSortFunc(self, item1, item2):
        preview1 = int(item1.get('preview', 0))
        preview2 = int(item2.get('preview', 0))
        if preview1 > preview2:
            return 1
        if preview1 < preview2:
            return -1
        startOrder1 = item1.get('starOrder', 0)
        startOrder2 = item2.get('starOrder', 0)
        if startOrder1 > startOrder2:
            return -1
        if startOrder1 < startOrder2:
            return 1
        prId1 = item1.get('prId', 0)
        prId2 = item2.get('prId', 0)
        if prId1 > prId2:
            return 1
        if prId1 < prId2:
            return -1
        return 1

    def refreshInfo(self):
        if not self.widget:
            return
        lvUpData = self.getLvUpData()
        self.refreshLvUpPanel(lvUpData)

    @property
    def tipsMc(self):
        return self.uiAdapter.playRecommActivation.tipsMc

    def refreshLvUpPanel(self, lvUpData):
        if not self.widget:
            return
        maxItemNum = 0
        for i in xrange(len(lvUpData)):
            maxItemNum = max(maxItemNum, len(lvUpData[i]['itemList']))

        self.widget.lvupPanel.itemList.maxItemNum = maxItemNum
        self.dataArray = lvUpData
        self.widget.lvupPanel.itemList.dataArray = range(len(lvUpData))
        self.widget.lvupPanel.itemList.validateNow()
        self.widget.lvupPanel.itemList.refreshWidth()

    def fillLvUpPanelItemH(self, *args):
        index = int(args[3][0].GetNumber())
        lvUpData = self.dataArray[index]
        lvUpItem = ASObject(args[3][1])
        itemList = lvUpData['itemList']
        itemWidth = 0
        lvUpItem.typeName.text = lvUpData['displayName']
        self.widget.removeAllInst(lvUpItem.activityList)
        for i, itemData in enumerate(itemList):
            itemMc = self.widget.getInstByClsName('PlayRecommV2LvUp_PlayRecomm_LvUpActivityItem')
            itemMc.x = i * itemMc.width
            itemMc.y = 0
            itemWidth = itemMc.width
            itemMc.activityName.text = itemData['name']
            itemMc.iconSlot.colorBg.gotoAndStop(lvUpData['displayIconBg'])
            itemMc.iconSlot.icon.setItemSlotData(itemData)
            itemMc.iconSlot.icon.prId = itemData['prId']
            self.prId2DataDic[itemData['prId']] = itemData
            itemMc.iconSlot.icon.dragable = False
            itemMc.iconSlot.icon.fitSize = True
            itemMc.closeFlag.visible = itemData['closeFlag']
            itemMc.activationIcon.visible = itemData['activation']['visible']
            itemMc.iconSlot.addEventListener(events.MOUSE_ROLL_OUT, self.rollOverListener, False, 0, True)
            itemMc.iconSlot.addEventListener(events.MOUSE_ROLL_OUT, self.rollOutListener, False, 0, True)
            itemMc.iconSlot.addEventListener(events.MOUSE_CLICK, self.mouseClickListener, False, 0, True)
            lvUpItem.activityList.addChild(itemMc)
            if self.tipsMc and self.tipsMc.refMc and self.tipsMc.activityId == itemData['prId']:
                self.tipsMc.tipData = itemData
            if itemMc.completeFlag:
                itemMc.completeFlag.visible = False
            if itemMc.recommendFlag:
                itemMc.recommendFlag.visible = True if itemData.get('recommendFlag', None) else False
            if itemMc.previewLv:
                itemMc.previewLv.visible = itemData['preview']
                itemMc.previewLv.text = str(itemData['needLv']) + gameStrings.TEXT_MANUALEQUIPPROXY_171
            itemMc.fubenProgress.visible = False
            if not itemData['preview']:
                if itemData['showProgress'] and not itemData['closeFlag'] and itemData['isShowFubenProgress']:
                    progressStr = ''
                    if itemData['periodType'] == 1:
                        progressStr += gameStrings.TEXT_PLAYRECOMMPROXY_848_6 + ' '
                    else:
                        progressStr += gameStrings.TEXT_GAMETYPES_10547 + ' '
                    progressStr += str(itemData['completeCnt']) + '/' + str(itemData['periodCnt'])
                    itemMc.fubenProgress.text = progressStr
                    itemMc.fubenProgress.visible = True
                    ASUtils.setHitTestDisable(itemMc.fubenProgress, True)
            if self.selectedId == 0:
                self.selectedId = itemData['prId']
            if self.selectedId == itemData['prId']:
                self.uiAdapter.playRecommActivation.showActivityTips(itemMc.iconSlot, itemData)

        lvUpItem.bgImage.width = max(720, lvUpItem.activityList.x + self.widget.lvupPanel.itemList.maxItemNum * itemWidth)

    def rollOverListener(self, *args):
        ui.set_cursor('cursor_click', 'cursor_click')

    def rollOutListener(self, *args):
        ui.set_cursor('arrow_normal', 'arrow_normal')

    def mouseClickListener(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.tipsMc and self.tipsMc.refMc == itemMc:
            self.uiAdapter.playRecommActivation.hideActivityTips()
        else:
            data = self.prId2DataDic.get(int(itemMc.icon.prId), None)
            if data:
                self.uiAdapter.playRecommActivation.showActivityTips(itemMc.iconSlot, data)
        self.selectedId = int(itemMc.icon.prId)
