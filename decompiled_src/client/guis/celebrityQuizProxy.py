#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/celebrityQuizProxy.o
import BigWorld
from Scaleform import GfxValue
import events
import gameglobal
import uiConst
import utils
import const
import gametypes
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import pinyinConvert
from asObject import ASObject
from asObject import ASUtils
from data import hall_of_fame_config_data as HOFCD
from cdata import game_msg_def_data as GMDD
TOP_PROXY_TYPE_MAP = {const.PROXY_KEY_HALL_OF_FAME_XIUWEI: gametypes.TOP_TYPE_HALL_OF_FAME_XIUWEI,
 const.PROXY_KEY_HALL_OF_FAME_SHENBING: gametypes.TOP_TYPE_HALL_OF_FAME_SHENBING,
 const.PROXY_KEY_HALL_OF_FAME_HONGYAN: gametypes.TOP_TYPE_HALL_OF_FAME_HONGYAN,
 const.PROXY_KEY_HALL_OF_FAME_YINGCAI: gametypes.TOP_TYPE_HALL_OF_FAME_YINGCAI,
 const.PROXY_KEY_HALL_OF_FAME_GUIBAO: gametypes.TOP_TYPE_HALL_OF_FAME_GUIBAO,
 const.PROXY_KEY_HALL_OF_FAME_QIAOJIANG: gametypes.TOP_TYPE_HALL_OF_FAME_QIAOJIANG,
 const.PROXY_KEY_HALL_OF_FAME_MINGSHI: gametypes.TOP_TYPE_HALL_OF_FAME_MINGSHI}

class CelebrityQuizProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CelebrityQuizProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.dataCache = {}
        self.currentTopType = 0
        self.key = ''
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CELEBRITY_QUIZ, self.hide)

    def clearAll(self):
        self.currentTopType = 0
        self.key = ''
        self.dataCache = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CELEBRITY_QUIZ:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CELEBRITY_QUIZ)

    def show(self):
        if self.widget:
            return
        BigWorld.player().base.getHallOfFameQuizTop()
        self.uiAdapter.loadWidget(uiConst.WIDGET_CELEBRITY_QUIZ)

    def initUI(self):
        self.getData()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.awardSlot.dragable = False
        self.widget.confirmBtn.enabled = False
        self.widget.inputMc.labelFunction = self.labelFunction
        self.widget.inputMc.selectItemFunction = self.selectItem
        self.widget.inputMc.labelField = None
        self.widget.inputMc.addEventListener(events.EVENT_CHANGE, self.handleInputChange, False, 0, True)

    def getData(self):
        if self.currentTopType and self.key:
            dataChache = self.dataCache.get((self.currentTopType, self.key), {})
            ver = dataChache.get('ver', 0)
            szKey = gametypes.ALL_LV_TOP_RANK_KEY
            tSplit = self.key.split('_')
            if len(tSplit) > 1:
                szKey = '%s_%s' % (tSplit[0], tSplit[1])
            BigWorld.player().base.getTopHallOfFame(self.currentTopType, ver, szKey, const.SCHOOL_DEFAULT)

    def refreshInfo(self):
        if not self.widget:
            return
        from guis import uiUtils
        itemData = uiUtils.getGfxItemById(HOFCD.data.get('quizCorretBonusId', 0))
        self.widget.awardSlot.setItemSlotData(itemData)

    def _onConfirmBtnClick(self, e):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(HOFCD.data.get('quizConfirmMsg', ''), yesCallback=self.onConfirmAnswer)

    def onConfirmAnswer(self):
        if not self.widget:
            return
        for data in self.dataCache.get((self.currentTopType, self.key), {}).get('data', {}):
            checkInfo = '{name} - {server}'.format(name=data.get('roleName', ''), server=data.get('serverName', ''))
            if self.widget.inputMc.text.strip() == checkInfo:
                BigWorld.player().base.hallOfFameQuiz(data.get('gbid', 0))
                self.hide()
                return

        BigWorld.player().showGameMsg(GMDD.data.HALL_OF_FAME_NAME_NOT_IN_QUIZ, ())

    def onGetTopType(self, topType, key):
        self.currentTopType = topType
        self.key = key

    def updateData(self, info):
        topType = TOP_PROXY_TYPE_MAP.get(info.get('proxyId', 0), 0)
        topKey = info.get('key', '')
        if info.get('data', []) and topType and topKey:
            self.dataCache[topType, topKey] = info

    def handleInputChange(self, *args):
        self.widget.confirmBtn.enabled = False
        if not self.widget.inputMc.text or self.widget.inputMc.text.isspace():
            return
        dataCache = self.dataCache.get((self.currentTopType, self.key), {}).get('data', {})
        inputText = pinyinConvert.strPinyin(self.widget.inputMc.text)
        if not dataCache:
            self.getData()
            return
        if not inputText:
            return
        self.widget.confirmBtn.enabled = True
        inputText = inputText.lower()
        searchResult = []
        for data in dataCache:
            name = data.get('roleName', '')
            fName = data.setdefault('fName', pinyinConvert.strPinyin(name).lower())
            sName = data.setdefault('sName', pinyinConvert.strPinyinFirst(name).lower())
            if inputText in fName or inputText in sName:
                searchResult.append(data)

        if searchResult:
            ASUtils.setDropdownMenuData(self.widget.inputMc, searchResult)
        else:
            self.widget.inputMc.close()

    def labelFunction(self, *args):
        item = ASObject(args[3][0])
        showName = '{name} - {server}'.format(name=item.roleName, server=item.serverName)
        return GfxValue(gbk2unicode(showName))

    def selectItem(self, *args):
        item = ASObject(args[3][0])
        showName = '{name} - {server}'.format(name=item.roleName, server=item.serverName)
        return GfxValue(gbk2unicode(showName))
