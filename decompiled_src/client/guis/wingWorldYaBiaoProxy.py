#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldYaBiaoProxy.o
import BigWorld
import utils
import gamelog
import formula
import uiConst
import events
import clientUtils
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis import uiUtils
from data import wing_world_config_data as WWCFD
from data import map_config_data as MCD
from data import wing_world_city_data as WWCD
from data import wing_world_yabiao_private_goods_bonus as WWYPGD
ITEM_MAX_CNT = 4
RESOURCE_MAX_CNT = 3

class WingWorldYaBiaoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldYaBiaoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_YABIAO, self.hide)

    def reset(self):
        self.isZhanKai = False
        self.lastHp = 0
        self.lastHpUpdateTime = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_YABIAO:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_YABIAO)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_YABIAO)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.mainMc.closeBtn
        ASUtils.setHitTestDisable(self.widget.mainMc.txtTitleName, True)
        self.widget.mainMc.changeRouteBtn.addEventListener(events.BUTTON_CLICK, self.handleChangeRouteBtnClick, False, 0, True)
        self.widget.mainMc.transportBtn.addEventListener(events.BUTTON_CLICK, self.handleTransportBtnClick, False, 0, True)
        self.widget.mainMc.zhanKaiBtn.addEventListener(events.BUTTON_CLICK, self.handleZhanKaiBtnClick, False, 0, True)
        self.widget.mainMc.zhanKaiTxt.addEventListener(events.MOUSE_CLICK, self.handleZhanKaiBtnClick, False, 0, True)
        self.isZhanKai = False

    def handleChangeRouteBtnClick(self, *args):
        gamelog.info('jbx:handleChangeRouteBtnClick')
        self.uiAdapter.wingWorldYaBiaoRoute.show()

    def handleTransportBtnClick(self, *args):
        p = BigWorld.player()
        gamelog.info('jbx:applyTeleportToWingWorldYabiaoZaiju', p.wingWorldYabiaoData.yabiaoSpaceNo, p.wingWorldYabiaoData.yabiaoPostion)
        p.cell.applyTeleportToWingWorldYabiaoZaiju(p.wingWorldYabiaoData.yabiaoSpaceNo, p.wingWorldYabiaoData.yabiaoPostion)

    def getDaKaCount(self):
        return len([ id for id in BigWorld.player().wingWorldYabiaoData.yabiaoDakaSeq if id ])

    def refreshZhanKaiContent(self):
        if not self.isZhanKai:
            return
        items = []
        yabiaoDakaRangeRewardsByLv = WWCFD.data.get('yabiaoDakaRangeRewardsByLv', {})
        for i in xrange(ITEM_MAX_CNT):
            bonusItems = clientUtils.genItemBonusEx(yabiaoDakaRangeRewardsByLv.get(i + 1, 0))
            bonusItems and items.append(bonusItems[0])

        for i in xrange(ITEM_MAX_CNT):
            itemMc = self.widget.mainMc.getChildByName('item%d' % i)
            if i < len(items):
                itemMc.visible = True
                itemMc.dragable = False
                itemMc.setItemSlotData(uiUtils.getGfxItemById(items[i][0], items[i][1]))
                itemMc.setItemSlotData(uiUtils.getGfxItemById(*items[i]))
            else:
                itemMc.visible = False

    def handleZhanKaiBtnClick(self, *args):
        gamelog.info('jbx:zhanKaiBtnClick')
        self.widget.mainMc.gotoAndStop('zhankai')
        self.isZhanKai = True
        self.widget.mainMc.txtDesc.htmlText = WWCFD.data.get('yaBiaoDesc', 'yaBiaoDesc')
        self.refreshZhanKaiContent()
        self.widget.mainMc.shousuoBtn.addEventListener(events.BUTTON_CLICK, self.handleShouSuoBtnClick, False, 0, True)
        self.widget.mainMc.shouLongTxt.addEventListener(events.MOUSE_CLICK, self.handleShouSuoBtnClick, False, 0, True)

    def handleShouSuoBtnClick(self, *args):
        gamelog.info('jbx:handleShouSuoBtnClick')
        self.widget.mainMc.gotoAndStop('shoulong')
        self.isZhanKai = False
        self.widget.mainMc.zhanKaiBtn.addEventListener(events.BUTTON_CLICK, self.handleZhanKaiBtnClick, False, 0, True)
        self.widget.mainMc.zhanKaiTxt.addEventListener(events.MOUSE_CLICK, self.handleZhanKaiBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        wingWorldYabiaoData = p.wingWorldYabiaoData
        positon = wingWorldYabiaoData.yabiaoPostion
        spaceNo = wingWorldYabiaoData.yabiaoSpaceNo
        if wingWorldYabiaoData.yabiaoBrokenBeginTime:
            endTime = wingWorldYabiaoData.yabiaoBrokenBeginTime + wingWorldYabiaoData.getWingWorldYabiaoBrokenDura()
            wudiEndTime = wingWorldYabiaoData.yabiaoBrokenBeginTime + wingWorldYabiaoData.getWingWorldYabiaoBrokenDura()
            wuDiDuration = wingWorldYabiaoData.getWingWorldYabiaoBrokenDura()
        else:
            endTime = wingWorldYabiaoData.yabiaoBeginTime + WWCFD.data.get('wingWorldYabiaoDura', 1200)
            wudiEndTime = wingWorldYabiaoData.zaijuInvincibleEndTime
            wuDiDuration = WWCD.data.get('yabiaoZaijuInvincibleDura', 600)
        hp = wingWorldYabiaoData.yabiaoZaijuHp
        hpMax = wingWorldYabiaoData.yabiaoZaijuMaxHp
        hpMax = max(hp, hpMax)
        dakaCnt = self.getDaKaCount()
        resourcesCnts = [wingWorldYabiaoData.get(0, 0), wingWorldYabiaoData.get(1, 0), wingWorldYabiaoData.get(2, 0)]
        wingWorldYabiaoPrivateGoods = getattr(p.guild, 'wingWorldYabiaoPrivateGoods', 0)
        isCoin = False
        if wingWorldYabiaoPrivateGoods:
            if WWYPGD.data.get(wingWorldYabiaoPrivateGoods, {}).has_key('coinCash'):
                siHuoCnt = WWYPGD.data.get(wingWorldYabiaoPrivateGoods, {}).get('coinCash', 0)
                isCoin = True
            else:
                siHuoCnt = WWYPGD.data.get(wingWorldYabiaoPrivateGoods, {}).get('costCash', 0)
        else:
            siHuoCnt = 0
        transportCost = WWCFD.data.get('wingWorldYabiaoTeleportCost', 1000)
        zaijuDriverGbId = wingWorldYabiaoData.yabiaoZaijuOwnerGbId
        dstCityId = wingWorldYabiaoData.yabiaoDestination
        hpPercent = hp * 1.0 / hpMax * 100 if hpMax else 0
        if self.lastHp != hp or utils.getNow() - self.lastHpUpdateTime > 10:
            TipManager.addTip(self.widget.mainMc.progressBar, '%d/%d' % (hp, hpMax))
            self.lastHp = hp
            self.lastHpUpdateTime = utils.getNow()
        wudiPercent = max(0, (wudiEndTime - utils.getNow()) * 1.0 / wuDiDuration * 100)
        ASUtils.setHitTestDisable(self.widget.mainMc.effect, True)
        self.widget.mainMc.effect.visible = wudiEndTime > utils.getNow()
        mapId = formula.getMapId(spaceNo)
        self.widget.mainMc.txtPosition.htmlText = gameStrings.WING_WORLD_YABIAO_GOTO % (spaceNo,
         positon[0],
         positon[1],
         positon[2],
         MCD.data.get(mapId, {}).get('name', ''))
        self.widget.mainMc.txtLeftTime.text = utils.formatTimeStr(max(0, endTime - utils.getNow()), 'm:s', True, 2, 2)
        self.widget.mainMc.progressBar.currentValues = (hpPercent, wudiPercent)
        leftWudiTime = max(0, wudiEndTime - utils.getNow())
        if leftWudiTime:
            self.widget.mainMc.txtWuDiTime.text = utils.formatTimeStr(leftWudiTime, 'm:s', True, 2, 2)
            self.widget.mainMc.txtWuDi.visible = True
        else:
            self.widget.mainMc.txtWuDiTime.text = ''
            self.widget.mainMc.txtWuDi.visible = False
        self.widget.mainMc.txtResource0.text = ''
        if not dakaCnt:
            self.widget.mainMc.txtResource0.text = gameStrings.WING_WORLD_RESOURCE_NOT_ADD % WWCFD.data.get('restype1', '')
            self.widget.mainMc.txtResource1.text = gameStrings.WING_WORLD_RESOURCE_NOT_ADD % WWCFD.data.get('restype2', '')
            self.widget.mainMc.txtResource2.text = gameStrings.WING_WORLD_RESOURCE_NOT_ADD % WWCFD.data.get('restype3', '')
            self.widget.mainMc.txtSiHuo.text = gameStrings.WING_WORLD_TECHAN_NOT_ADD
        else:
            self.widget.mainMc.txtResource0.text = gameStrings.WING_WORLD_RESOURCE_ADD % (WWCFD.data.get('restype1', ''), dakaCnt)
            self.widget.mainMc.txtResource1.text = gameStrings.WING_WORLD_RESOURCE_ADD % (WWCFD.data.get('restype2', ''), dakaCnt)
            self.widget.mainMc.txtResource2.text = gameStrings.WING_WORLD_RESOURCE_ADD % (WWCFD.data.get('restype3', ''), dakaCnt)
            self.widget.mainMc.txtSiHuo.text = gameStrings.WING_WORLD_TECHAN_ADD % dakaCnt
        self.widget.mainMc.txtCount0.text = str(resourcesCnts[0])
        self.widget.mainMc.txtCount1.text = str(resourcesCnts[1])
        self.widget.mainMc.txtCount2.text = str(resourcesCnts[2])
        self.widget.mainMc.txtSiHuoCount.text = siHuoCnt
        self.widget.mainMc.cash0.bonusType = 'cash' if not isCoin else 'tianBi'
        self.widget.mainMc.txtDestination.text = WWCD.data.get(dstCityId, {}).get('name', '')
        self.widget.mainMc.txtCost.text = str(transportCost)
        self.widget.mainMc.changeRouteBtn.enabled = p.gbId == zaijuDriverGbId
        self.widget.mainMc.transportBtn.enabled = p.gbId != zaijuDriverGbId
        BigWorld.callback(1, self.refreshInfo)

    def addPushIcon(self):
        if not self.uiAdapter.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_WING_WORLD_YABIAO):
            gamelog.info('jbx:addPushIcon')
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_YABIAO)
            self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WING_WORLD_YABIAO, {'click': self.show})

    def delPushIcon(self):
        if self.uiAdapter.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_WING_WORLD_YABIAO):
            gamelog.info('jbx:delPushIcon')
            self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_YABIAO)
