#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/buffListenerSettingProxy.o
import cPickle
import zlib
import BigWorld
from Scaleform import GfxValue
import const
import gameglobal
import uiConst
import copy
import events
from asObject import ASObject
from gamestrings import gameStrings
from uiProxy import UIProxy
from data import base_card_data as BCD
from data import advance_card_data as ACD
from data import conditional_prop_data as CPD
from cdata import pskill_data as PDD
from cdata import game_msg_def_data as GMDD
from guis import uiUtils
from data import prop_ref_data as PRD
from data import game_msg_data as GMD
CARD_SLOT_TYPE_1 = 1
CARD_SLOT_TYPE_2 = 2

class BuffListenerSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BuffListenerSettingProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BUFF_LISTENER_SETTING, self.hide)

    def reset(self):
        self.tempId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BUFF_LISTENER_SETTING:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BUFF_LISTENER_SETTING)

    @property
    def cardBag(self):
        p = BigWorld.player()
        cardBag = p.allCardBags.get(self.tempId, {})
        return cardBag

    @property
    def listenerBuffData(self):
        p = BigWorld.player()
        return p.listenerBuffData

    @listenerBuffData.setter
    def listenerBuffData(self, value):
        p = BigWorld.player()
        p.listenerBuffData = value

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BUFF_LISTENER_SETTING)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.samllIconBtn.groupName = 'sizeBtn'
        self.widget.samllIconBtn.data = 1
        self.widget.bigIconBtn.groupName = 'sizeBtn'
        self.widget.bigIconBtn.data = 2
        self.widget.eventList.itemRenderer = 'BuffListenerSetting_BuffItem'
        self.widget.eventList.labelFunction = self.propertyItemFunc
        self.widget.eventList.itemHeightFunction = self.propListItemHeightFunction
        self.widget.eventList.dataArray = []
        self.widget.samllIconBtn.addEventListener(events.MOUSE_CLICK, self.handleSamllIconBtnClick, False, 0, True)
        self.widget.bigIconBtn.addEventListener(events.MOUSE_CLICK, self.handleBigIconBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        buffListenerConfig = p.buffListenerConfig
        widgetSize = buffListenerConfig.get('size', uiConst.BUFF_LISTENER_SIZE_1)
        if widgetSize == uiConst.BUFF_LISTENER_SIZE_1:
            self.widget.samllIconBtn.selected = True
        elif widgetSize == uiConst.BUFF_LISTENER_SIZE_2:
            self.widget.bigIconBtn.selected = True
        listenerData = self.genListenerBuffData()
        self.widget.eventList.dataArray = listenerData

    def propertyItemFunc(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            if info.isTitle:
                itemMc.gotoAndPlay('title')
                itemMc.titleTxt.text = info.txt
                itemMc.isTitle = True
                itemMc.listenerId = 0
                itemMc.listenerType = 0
            else:
                itemMc.gotoAndPlay('content')
                listenerId = info.listenerId
                itemMc.listenerId = listenerId
                itemMc.isTitle = False
                itemMc.listenerType = info.listenerType
                self.refreshContentItemInfo(itemMc)

    def refreshContentItemInfo(self, itemMc):
        listenerId = itemMc.listenerId
        if listenerId:
            condData = self.listenerBuffData.get(listenerId, {})
            icon = condData.get('icon', 0)
            propVal = condData.get('propVal', 0)
            bListener = condData.get('bListener', 0)
            condPropData = CPD.data.get(listenerId, {})
            conPropType = condPropData.get('conPropType', 1)
            if not icon:
                if conPropType == const.COND_PROP_TYPE_ATTACK:
                    icon = uiConst.BUFF_LISTENER_DEFAULT_ICON_1
                elif conPropType == const.COND_PROP_TYPE_DEFENSE:
                    icon = uiConst.BUFF_LISTENER_DEFAULT_ICON_2
            iconPath = uiConst.MACRO_COMMON_ICON % icon
            itemData = {'iconPath': iconPath}
            itemMc.contentMc.soundBtn.visible = False
            itemMc.contentMc.selectedBox.selected = bListener
            itemMc.contentMc.buffIcon.setItemSlotData(itemData)
            itemMc.contentMc.buffIcon.dragable = False
            itemMc.contentMc.descTxt.htmlText = self.formatCondStr(listenerId, propVal)
            itemMc.contentMc.selectedBox.addEventListener(events.EVENT_SELECT, self.handleSelectedBoxClick, False, 0, True)
            itemMc.contentMc.settingBtn.addEventListener(events.BUTTON_CLICK, self.handleSettingBtnClick, False, 0, True)

    def propListItemHeightFunction(self, *arg):
        if self.hasBaseData():
            info = ASObject(arg[3][0])
            item = self.widget.getInstByClsName('BuffListenerSetting_BuffItem')
            height = 0
            if info.isTitle:
                item.gotoAndPlay('title')
                height = item.height + 5
            else:
                item.gotoAndPlay('content')
                height = item.height
            return GfxValue(height)

    def handleSelectedBoxClick(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        e = ASObject(arg[3][0])
        t = e.target
        listenerId = t.parent.parent.listenerId
        listenerType = t.parent.parent.listenerType
        if listenerId in self.listenerBuffData:
            if t.selected and not self.checkBuffCanEnableListen():
                t.selected = False
                return
            self.listenerBuffData[listenerId]['bListener'] = int(t.selected)
            buffListenerConfig = copy.deepcopy(p.buffListenerConfig)
            buffListenerConfig.setdefault('buffConfig', {})
            buffListenerConfig['buffConfig'].setdefault(listenerType, {})
            buffListenerConfig['buffConfig'][listenerType][listenerId] = self.listenerBuffData[listenerId]
            serverData = self.packConfigData(buffListenerConfig)
            p.base.setStateMonitorClientConfig(serverData)

    def checkBuffCanEnableListen(self, showError = True):
        p = BigWorld.player()
        if len(p.listeningBuffShowData) >= const.BUFF_LISTENER_NUM_MAX:
            p.showGameMsg(GMDD.data.BUFF_LISTENER_NUM_LIMIT, ())
            return False
        return True

    def handleSettingBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        listenerId = t.parent.parent.listenerId
        listenerType = t.parent.parent.listenerType
        self.uiAdapter.buffListenerIconSelect.show(listenerType, listenerId)

    def genListenerBuffData(self):
        p = BigWorld.player()
        dataRet = []
        self.listenerBuffData = {}
        dataIndex = 0
        titleData = {'index': dataIndex,
         'isTitle': True,
         'txt': gameStrings.CARD_COMMON_NAME}
        dataIndex += 1
        dataRet.append(titleData)
        equipSlot = self.cardBag.get('equipSlot', 0)
        cardSlots = self.cardBag.get('cardSlots', {})
        for cardId, cData in BCD.data.iteritems():
            cardObj = p.getCard(cardId, True)
            if not cardObj:
                continue
            if not cardObj.isValidCard():
                continue
            activePskillProp, activeConProp = gameglobal.rds.ui.cardSystem.getCardSkillsOpenLv(cardObj, False)
            condInfos = self.calcCondPropData(activePskillProp, activeConProp)
            for condData in condInfos:
                condId = condData.get('condId', 0)
                propVal = condData.get('propVal', 0)
                openLv = condData.get('openLv', 0)
                if cardObj.advanceLvEx < openLv:
                    continue
                dataRet = self.addMainBuffData(dataRet, condId, propVal, const.LISTENER_TYPE_CARD_CONDITION)

            if cardObj.slot:
                if not gameglobal.rds.ui.cardSystem.checkCardValidInSlot(cardObj):
                    continue
                slotPskillProp, slotConProp = gameglobal.rds.ui.cardSystem.getCardSkillsOpenLv(cardObj, True)
                condInfos = self.calcCondPropData(slotPskillProp, slotConProp)
                for condData in condInfos:
                    condId = condData.get('condId', 0)
                    propVal = condData.get('propVal', 0)
                    openLv = condData.get('openLv', 0)
                    if cardObj.advanceLvEx < openLv:
                        continue
                    dataRet = self.addMainBuffData(dataRet, condId, propVal, const.LISTENER_TYPE_CARD_CONDITION)

                for k, v in cardObj.washProps.iteritems():
                    washGroupId = v.get('washGroupId', 0)
                    sequence = k
                    stage = v.get('stage', 0)
                    sType = v.get('sType', 0)
                    sId = v.get('sId', 0)
                    sNum = v.get('sNum', 0)
                    fullProp = v.get('fullProp', False)
                    tips = ''
                    if sType == const.CARD_PROP_TYPE_CONDITIONAL_PROPS:
                        dataRet = self.addMainBuffData(dataRet, sId, sNum, const.LISTENER_TYPE_CARD_CONDITION)

        sceneType = p.getCardSceneType()
        propertyData = []
        propType = 0
        suitInfo = self.uiAdapter.cardSlot.getPskillEffects(equipSlot)
        if not gameglobal.rds.configData.get('enableChangeCardSuit', 0):
            for k, v in suitInfo.iteritems():
                for eff, lv in v:
                    pData = PDD.data.get((eff, lv), {})
                    pskillConds = pData.get('conditionalProps', ())
                    for condId, propVal in pskillConds:
                        dataRet = self.addMainBuffData(dataRet, condId, propVal, const.LISTENER_TYPE_CARD_CONDITION)

        else:
            curSuitId, curSuitRank = self.cardBag.get('equipSuit', {}).get(equipSlot, (0, 0))
            effect = suitInfo.get((curSuitId, curSuitRank), ())
            for eff, lv in effect:
                pData = PDD.data.get((eff, lv), {})
                pskillConds = pData.get('conditionalProps', ())
                for condId, propVal in pskillConds:
                    dataRet = self.addMainBuffData(dataRet, condId, propVal, const.LISTENER_TYPE_CARD_CONDITION)

        return dataRet

    def addMainBuffData(self, dataRet, condId, propVal, listenerType):
        bAppendData = condId not in self.listenerBuffData
        self.setCondDataInfo(condId, propVal, listenerType)
        if bAppendData:
            cData = {'isTitle': False,
             'listenerId': condId,
             'listenerType': listenerType}
            dataRet.append(cData)
        return dataRet

    def setCondDataInfo(self, condId, propVal, listenerType):
        p = BigWorld.player()
        buffListenerConfig = p.buffListenerConfig
        buffConfigData = buffListenerConfig.get('buffConfig', {})
        cardCondConfigData = buffConfigData.get(listenerType, {})
        configData = cardCondConfigData.get(condId, {})
        icon = configData.get('icon', 0)
        bListener = configData.get('bListener', 0)
        self.listenerBuffData.setdefault(condId, {'propVal': 0,
         'icon': 0,
         'bListener': 0})
        self.listenerBuffData[condId]['propVal'] += propVal
        self.listenerBuffData[condId]['icon'] = icon
        self.listenerBuffData[condId]['bListener'] = bListener

    def calcCondPropData(self, passivity, condSkill):
        condArr = []

        def _appendCondProp(condId, propVal, openLv):
            info = {'condId': condId,
             'propVal': propVal,
             'openLv': openLv}
            condArr.append(info)

        for (skillId, lv), openLv in passivity.iteritems():
            pData = PDD.data.get((skillId, lv), {})
            pskillConds = pData.get('conditionalProps', ())
            for condId, propVal in pskillConds:
                _appendCondProp(condId, propVal, openLv)

        for (condId, propVal), openLv in condSkill.iteritems():
            _appendCondProp(condId, propVal, openLv)

        condArr.sort(key=lambda x: x.get('openLv', 0))
        return condArr

    def formatCondStr(self, condId, propVal):
        condData = CPD.data.get(condId, {})
        formatType = int(condData.get('formatType', 0))
        desc = condData.get('specialDesc', '')
        desc = desc.replace('<', '&lt;').replace('>', '&gt;')
        return desc % ()

    def handleSamllIconBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        buffListenerConfig = copy.deepcopy(p.buffListenerConfig)
        buffListenerConfig['size'] = uiConst.BUFF_LISTENER_SIZE_1
        serverData = self.packConfigData(buffListenerConfig)
        p.base.setStateMonitorClientConfig(serverData)

    def handleBigIconBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        buffListenerConfig = copy.deepcopy(p.buffListenerConfig)
        buffListenerConfig['size'] = uiConst.BUFF_LISTENER_SIZE_2
        serverData = self.packConfigData(buffListenerConfig)
        p.base.setStateMonitorClientConfig(serverData)

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def packConfigData(self, data):
        return zlib.compress(cPickle.dumps(data))
