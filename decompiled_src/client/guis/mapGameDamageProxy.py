#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameDamageProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from guis import uiUtils
from gamestrings import gameStrings
import clientUtils
from data import map_game_config_data as MGCD
MAX_REWARD_NUM = 5
PROGRESSBAR_MARGINS_UI_LENGTH_DATA = [34,
 77,
 77,
 77,
 77]
PROGRESSBAR_MARGINS_LENGTH = 342

class MapGameDamageProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameDamageProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_DAMAGE, self.hide)

    def reset(self):
        self.bossGridID = 0
        self.damage = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_DAMAGE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_DAMAGE)

    def show(self, id):
        self.bossGridID = id
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_DAMAGE)
        self.getFirstBossReward()

    def getFirstBossReward(self):
        mapGameBossGridIdList = MGCD.data.get('mapGameBossGridIdList', {})
        p = BigWorld.player()
        if mapGameBossGridIdList:
            firstBossId = mapGameBossGridIdList.get('trueBoss')
            if self.bossGridID == firstBossId:
                return
            bossInfo = p.grids.get(firstBossId, {})
            secondBossId = bossInfo.secondId
            if self.bossGridID == secondBossId:
                mapGameBossDamage = p.mapGameBossDamage
                bossDamage = mapGameBossDamage.get(firstBossId, 0) if mapGameBossDamage else 0
                receivedReward = p.mapGameBossReward.get(firstBossId, {})
                damageMargins = MGCD.data.get('mapGameDamageMargins', (10000, 20000, 30000, 40000, 50000))
                leftReward = False
                for index in xrange(len(damageMargins)):
                    margin = damageMargins[index]
                    if bossDamage >= margin and index not in receivedReward.keys():
                        leftReward = True

                if leftReward:
                    p.cell.getMapGameBossReward(firstBossId)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        mapGameDamageMargins = MGCD.data.get('mapGameDamageMargins', (10000, 20000, 30000, 40000, 50000))
        mapGameDamageBonusIds = MGCD.data.get('mapGameDamageBonusIds', {}).get(self.bossGridID, ())
        for i in xrange(len(mapGameDamageMargins)):
            valueMc = self.widget.getChildByName('value%d' % i)
            valueMc.text = '%dW' % (mapGameDamageMargins[i] / 10000)
            itemMc = self.widget.getChildByName('item%d' % i)
            itemId, cnt = clientUtils.genItemBonus(mapGameDamageBonusIds[i])[0]
            itemMc.dragable = False
            itemMc.setItemSlotData(uiUtils.getGfxItemById(itemId, cnt))

        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleClickConfirmBtn, False, 0, True)

    def handleClickConfirmBtn(self, *args):
        BigWorld.player().cell.getMapGameBossReward(self.bossGridID)

    def refreshInfo(self):
        if not self.widget:
            return
        bossProxy = gameglobal.rds.ui.mapGameBoss
        bossProxy.refreshRewardBtn()
        mapGameBossDamage = BigWorld.player().mapGameBossDamage
        bossDamage = mapGameBossDamage.get(self.bossGridID, 0) if mapGameBossDamage else 0
        mapGameDamageMargins = MGCD.data.get('mapGameDamageMargins', (10000, 20000, 30000, 40000, 50000))
        if bossDamage >= mapGameDamageMargins[-1]:
            self.widget.progressBar.maxValue = mapGameDamageMargins[-1]
            self.widget.progressBar.currentValue = bossDamage
        else:
            self.widget.progressBar.maxValue = 1.0
            marginUIIdx = 0
            for mapGameDamageMargin in mapGameDamageMargins:
                if bossDamage <= mapGameDamageMargin:
                    break
                else:
                    marginUIIdx += 1

            lastMargins = 0 if marginUIIdx == 0 else mapGameDamageMargins[marginUIIdx - 1]
            subPercent = (bossDamage * 1.0 - lastMargins) / (mapGameDamageMargins[marginUIIdx] - lastMargins)
            realUILen = 0
            for idx, marginUILen in enumerate(PROGRESSBAR_MARGINS_UI_LENGTH_DATA):
                if idx == marginUIIdx:
                    break
                realUILen += marginUILen

            allPercent = realUILen * 1.0 / PROGRESSBAR_MARGINS_LENGTH
            tempPercent = PROGRESSBAR_MARGINS_UI_LENGTH_DATA[marginUIIdx] * 1.0 / PROGRESSBAR_MARGINS_LENGTH
            self.widget.progressBar.currentValue = allPercent + tempPercent * subPercent

    def setConfirmBtn(self, enabled):
        if not self.widget:
            return
        self.widget.confirmBtn.enabled = enabled
