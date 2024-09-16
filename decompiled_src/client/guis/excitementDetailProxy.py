#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/excitementDetailProxy.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
import ui
import clientUtils
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from asObject import ASUtils
from guis.asObject import TipManager
from gameStrings import gameStrings
from callbackHelper import Functor
from data import excitement_data as ED
from data import quest_data as QD
from cdata import excitement_quest_list_data as EQLD
from data import play_recomm_config_data as PRCD
NOR_COLOR = '#CC2929'
COM_COLOR = '#7ACC29'

class ExcitementDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ExcitementDetailProxy, self).__init__(uiAdapter)
        self.exId = 0
        self.widget = None
        self.pos = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_EXCITEMENT_DETAIL, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_EXCITEMENT_DETAIL:
            self.widget = widget
            self.initUI()

    def show(self, exId, pos = (0, 0)):
        if self.exId == exId:
            self.hide()
            return
        self.exId = exId
        self.pos = pos
        if self.widget:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXCITEMENT_DETAIL)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXCITEMENT_DETAIL)
        self.widget = None

    def reset(self):
        self.exId = 0
        self.pos = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.mainMc.closeBtn
        self.widget.mainMc.visible = False
        self.refreshInfo()

    def resetPos(self):
        if self.widget and not self.widget.visible:
            _x, _y = self.pos
            gamelog.debug('@zq resetPos', self.pos, self.widget.x, self.widget.y)
            self.widget.mainMc.x = _x - self.widget.x - 125
            self.widget.mainMc.y = _y - self.widget.y + 75
            self.widget.mainMc.visible = True
            self.widget.visible = True

    def onEnterFrame(self, *args):
        self.resetPos()

    @ui.callAfterTime()
    def refreshInfo(self):
        if self.hasBaseData():
            p = BigWorld.player()
            eData = ED.data.get(self.exId, {})
            name = eData.get('name', '')
            openlv = eData.get('openlv', '')
            conditionTxt = eData.get('conditionTxt', '')
            cType, cParam = eData.get('condition', (0, 0))
            sType, sParam = eData.get('seekId', (0, 0))
            iconNum = eData.get('icon', None)
            desc = eData.get('desc', '')
            self.widget.mainMc.excitementNameTxt.text = name
            self.widget.mainMc.titleMc.titleName.text = name
            if iconNum:
                self.widget.mainMc.excitementIcon.visible = True
                self.widget.mainMc.excitementIcon.fitSize = True
                self.widget.mainMc.excitementIcon.loadImage(uiConst.EXCITEMENT_IMPAGE_PATH % iconNum)
            else:
                self.widget.mainMc.excitementIcon.visible = False
            questName = ''
            if cType:
                self.widget.mainMc.conditionTxt2.visible = True
                questName = QD.data.get(cParam, {}).get('name', '')
            else:
                self.widget.mainMc.conditionTxt2.visible = False
            self.widget.mainMc.descTxt.text = desc
            self.widget.mainMc.conditionTxt.text = conditionTxt
            color1 = NOR_COLOR if p.lv < openlv else COM_COLOR
            color2 = NOR_COLOR if not p.isQuestCompleted(cParam) else COM_COLOR
            self.widget.mainMc.conditionTxt1.htmlText = uiUtils.toHtml(gameStrings.ECXITEMENT_DETAIL_TEXT_1 % openlv, color1)
            self.widget.mainMc.conditionTxt2.htmlText = uiUtils.toHtml(gameStrings.ECXITEMENT_DETAIL_TEXT_2 % questName, color2)
            bonusId = eData.get('bonusId', 0)
            rewardItems = clientUtils.genItemBonus(bonusId)
            itemId, num = rewardItems[0]
            gfxItem = uiUtils.getGfxItemById(itemId, num)
            self.widget.mainMc.rewardSlot.setItemSlotData(gfxItem)
            self.widget.mainMc.rewardSlot.dragable = False
            self.widget.mainMc.confirmBtn.enabled = True
            state = self.getCurState()
            buttonTxt = ''
            if state == uiConst.EXCITEMENT_DETAIL_STATE_CANT_OPEN:
                buttonTxt = eData.get('buttonTxt2', '')
                self.widget.mainMc.confirmBtn.enabled = False
            else:
                buttonTxt = eData.get('buttonTxt' + str(state), '')
            self.widget.mainMc.confirmBtn.label = buttonTxt
            self.widget.mainMc.visible = True

    def hasBaseData(self):
        if self.widget and self.exId:
            return True
        else:
            return False

    def _onConfirmBtnClick(self, e):
        gamelog.debug('@zq _onConfirmBtnClick')
        p = BigWorld.player()
        curState = self.getCurState()
        if curState == uiConst.EXCITEMENT_DETAIL_STATE_LVUP:
            self.uiAdapter.playRecomm.show()
            self.hide()
        elif curState == uiConst.EXCITEMENT_DETAIL_STATE_OPEN:
            p.cell.applyExciteReward([self.exId], True)
        elif curState == uiConst.EXCITEMENT_DETAIL_STATE_GOTO:
            seekId = self.getCurGotoSeekId()
            uiUtils.findPosById(seekId)
            self.hide()

    def getCurGotoSeekId(self):
        p = BigWorld.player()
        eData = ED.data.get(self.exId, {})
        sType, sParam = eData.get('seekId', (0, 0))
        seekId = 0
        if sType == uiConst.EXCITEMENT_SEEK_TYPE_SIMPLE_QUEST:
            seekId = sParam
        elif sType == uiConst.EXCITEMENT_SEEK_TYPE_QUEST_LIST:
            questIds = EQLD.data.get(sParam, {}).get('content', ())
            for qId in questIds:
                if p.isQuestCompleted(qId):
                    continue
                else:
                    seekId = 0
                    if p.isQuestComplete(qId):
                        seekId = QD.data.get(qId, {}).get('comNpcTk', 0)
                    else:
                        seekId = QD.data.get(qId, {}).get('acNpcTk', 0)
                    break

        return seekId

    def getCurState(self):
        p = BigWorld.player()
        eData = ED.data.get(self.exId, {})
        cType, cParam = eData.get('condition', (0, 0))
        openlv = eData.get('openlv', '')
        state = 0
        if p.lv < openlv:
            if p.lv < PRCD.data.get('playRecommShowLv', 20):
                state = uiConst.EXCITEMENT_DETAIL_STATE_CANT_OPEN
            else:
                state = uiConst.EXCITEMENT_DETAIL_STATE_LVUP
        elif cType:
            if p.isQuestCompleted(cParam):
                state = uiConst.EXCITEMENT_DETAIL_STATE_OPEN
            else:
                state = uiConst.EXCITEMENT_DETAIL_STATE_GOTO
        else:
            state = uiConst.EXCITEMENT_DETAIL_STATE_OPEN
        return state
