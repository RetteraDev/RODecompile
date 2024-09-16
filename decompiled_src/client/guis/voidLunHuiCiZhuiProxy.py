#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidLunHuiCiZhuiProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import tipUtils
from guis import events
from guis.asObject import TipManager
from guis import voidLunHuiHelper
from data import fb_data as FD
from data import team_endless_config_data as TECD
from gamestrings import gameStrings
MAX_PROP_NUM = 4
MAX_PROP_LINE_NUM = 4

class VoidLunHuiCiZhuiProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoidLunHuiCiZhuiProxy, self).__init__(uiAdapter)
        self.widget = None
        self.fbId = 0
        self.propList = []
        self.nextFbId = 0
        self.nextPropList = []
        self.rank = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_LUNHUI_CIZHUI, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_LUNHUI_CIZHUI:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VOID_LUNHUI_CIZHUI)

    def show(self, rank):
        self.rank = rank
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_VOID_LUNHUI_CIZHUI)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.okBtn.addEventListener(events.BUTTON_CLICK, self.onOkBtnClick)

    def onOkBtnClick(self, *args):
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        teamEndlessGlobalInfo = getattr(p, 'teamEndlessGlobalInfo', {})
        fbType = teamEndlessGlobalInfo.get('fbType', 0)
        nextFbType = teamEndlessGlobalInfo.get('nextFbType', 0)
        self.fbId = voidLunHuiHelper.getInstance().getFbIdBytype(fbType, self.rank)
        self.nextFbId = voidLunHuiHelper.getInstance().getFbIdBytype(nextFbType, self.rank)
        self.propList = teamEndlessGlobalInfo.get('affix', [])
        self.nextPropList = teamEndlessGlobalInfo.get('nextAffix', [])
        self.widget.cizhuiInfo.canvas.thisFuben.title.text = gameStrings.VOID_LUNHUI_THISWEEK_FB
        self.widget.cizhuiInfo.canvas.thisFuben.textField.text = FD.data.get(self.fbId, {}).get('name', '')
        self.widget.cizhuiInfo.canvas.nextFuben.textField.text = FD.data.get(self.nextFbId, {}).get('name', '')
        self.widget.cizhuiInfo.canvas.nextFuben.title.text = gameStrings.VOID_LUNHUI_NEXTWEEK_FB
        self.refreshPropList()

    def refreshPropList(self):
        diffIdxs = TECD.data.get('affix', {}).keys()
        diffIdxs.sort()
        for i in xrange(MAX_PROP_LINE_NUM):
            levelMc = self.widget.cizhuiInfo.canvas.getChildByName('level%d' % i)
            nextLevelMc = self.widget.cizhuiInfo.canvas.getChildByName('nextLevel%d' % i)
            levelMc.rewardDark.visible = False
            nextLevelMc.rewardDark.visible = False
            if i < len(diffIdxs):
                levelMc.visible = True
                nextLevelMc.visible = True
                self.setDiffText(levelMc, i, diffIdxs)
                self.setDiffText(nextLevelMc, i, diffIdxs)
                self.setPropList(levelMc, diffIdxs[i], self.propList)
                self.setPropList(nextLevelMc, diffIdxs[i], self.nextPropList)
            else:
                levelMc.visible = False
                nextLevelMc.visible = False

    def setPropList(self, itemMc, diffIdx, allProps):
        propList = []
        diffIdxs = TECD.data.get('affix', {}).keys()
        diffIdxs.sort()
        for idx in diffIdxs:
            if idx <= diffIdx:
                for propId in TECD.data.get('affix', {}).get(idx, []):
                    if propId in allProps:
                        propList.append(propId)

            else:
                break

        for i in xrange(MAX_PROP_NUM):
            propMc = itemMc.rewardBright.getChildByName('buff%d' % i)
            if i < len(propList):
                propMc.visible = True
                voidLunHuiHelper.getInstance().setCiZhuiInfo(propMc.icon, propList[i])
            else:
                propMc.visible = False

    def setDiffText(self, itemMc, index, diffIdxs):
        fromLv = diffIdxs[index]
        if index != len(diffIdxs) - 1 and len(diffIdxs) > 0:
            toLv = diffIdxs[index + 1]
            itemMc.rewardBright.progressText.text = gameStrings.VOID_LUNHUI_DIFFTEXT % (fromLv, toLv)
        else:
            itemMc.rewardBright.progressText.text = gameStrings.VOID_LUNHUI_END_DIFFTEXT % fromLv
