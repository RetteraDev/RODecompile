#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/BfDotaItemAndPropProxy.o
import BigWorld
import uiUtils
import uiConst
import events
import ui
import formula
import logicInfo
import gametypes
import gamelog
import utils
import gameglobal
import clientUtils
from callbackHelper import Functor
from uiProxy import SlotDataProxy
from guis import hotkey as HK
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis import tipUtils
from guis.asObject import ASUtils
from data import duel_config_data as DCD
from data import zaiju_data as ZD
from data import role_panel_attr_data as RPAD
from data import equip_data as ED
from data import item_data as ID
from data import skill_general_data as SGD
from cdata import game_msg_def_data as GMDD
from cdata import pskill_data as PSD
BAG_MAX_CNT = 6
PROP_MAX_CNT = 8
TEAMMATE_MAX_CNT = 5
GEM_ZERO_POS = 24
GEM_FULL_POS = 9.0

class BfDotaItemAndPropProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(BfDotaItemAndPropProxy, self).__init__(uiAdapter)
        self.bindType = 'bfDotaItem'
        self.type = 'bfDotaItem'
        self._resetData()

    def _resetData(self):
        self.widget = None
        self.keyArr = [''] * BAG_MAX_CNT
        self.itemMcList = []
        self.callbackHandler = {}
        self.propMcList = []
        self.selfSideMcList = []
        self.enemySideMcList = []
        self.isShowProp = False
        self.enemyInfoList = []
        self.isAddTip = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId != uiConst.WIDGET_BF_DOTA_ITEM_AND_PROP:
            return
        self.widget = widget
        self._initUI()
        self.refreshFrame()
        self.updateTick()

    def createKeyText(self):
        keyArr = [ HK.HKM[x].getBrief() for x in HK.BfDotaItemHotkeyList ]
        self.keyArr = keyArr

    def show(self):
        if self.widget:
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_ITEM_AND_PROP)

    def clearWidget(self):
        for id, value in self.callbackHandler.iteritems():
            BigWorld.cancelCallback(value)

        self._resetData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_DOTA_ITEM_AND_PROP)

    def refreshCash(self):
        self.uiAdapter.bfDotaShop.refreshCash()
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.mainMc.menu.money.txtNum.text = str(p.battleFieldDotaCash)

    def setPropsVisible(self, visible):
        if not self.widget:
            return
        self.isShowProp = visible
        self.widget.mainMc.props.visible = visible
        if visible:
            self.widget.mainMc.menu.showHideProp.mc.gotoAndStop('zhankai')
        else:
            self.widget.mainMc.menu.showHideProp.mc.gotoAndStop('shousuo')
        if visible:
            self.refreshAttrs()

    @ui.uiEvent(uiConst.WIDGET_BF_DOTA_ITEM_AND_PROP, events.EVNET_PRIMARY_PROP_CHANGE)
    def refreshAttrs(self, event = None):
        if not self.widget:
            return
        if not self.widget.mainMc.props.visible:
            return
        attrsInfo = self.getAttrsInfo()
        for i in xrange(PROP_MAX_CNT):
            if i >= len(attrsInfo):
                return
            info = attrsInfo[i]
            mc = self.propMcList[i]
            details = info[0].split('  ')
            details[1] = details[1].split('-')[0]
            mc.txtProp.htmlText = details[1]
            keys = info[1].split(',')
            if not self.isAddTip:
                mc.keys = (int(keys[0]), int(keys[1]))
                TipManager.addTipByFunc(mc, self.propTipFunc, mc, False)

        self.isAddTip = True

    def propTipFunc(self, *args):
        mc = ASObject(args[3][0])
        keys = (int(mc.keys[0]), int(mc.keys[1]))
        tipContent = self.uiAdapter.roleInfo.getPropsTipContent(keys).get('tipContent', '')
        tipMc = TipManager.getInstance().getDefaultTipMc(tipContent, tipUtils.TYPE_DEFAULT_BLACK)
        TipManager.showImediateTip(mc, tipMc)

    def refreshItemSlots(self, list = None):
        self.uiAdapter.bfDotaShop.refreshBagItems()
        self.createKeyText()
        self.uiAdapter.bfDotaItemAndProp.refreshAttrs()
        if not self.widget:
            return
        if not list:
            list = range(BAG_MAX_CNT)
        for i in list:
            self.setItemMc(i)

        self.refreshItemCooldown(list)
        self.refreshKeyText()
        self.uiAdapter.bfDotaShopPush.refreshInfo()

    def onKeyDown(self, event):
        for index, keyDef in enumerate(HK.BfDotaItemHotkeyList):
            key, mods = event.data
            if keyDef.key == key:
                self.useItem(index, True, byBfDota=True)
                return

    def setItemMc(self, i):
        p = BigWorld.player()
        mc = self.itemMcList[i]
        mapId = p.mapID
        mc.keyBind.text = self.keyArr[i]
        mc.binding = ''
        mc.binding = 'bfDotaItem.slot%d' % i
        mc.validateNow()
        if formula.inDotaBattleField(mapId):
            item = p.battleFieldBag.get(i, None)
        else:
            item = p.inv.getQuickVal(0, i)
        if not item:
            mc.lock.visible = True
            mc.dragable = False
            TipManager.removeTip(mc)
        else:
            mc.lock.visible = False
            mc.dragable = True
            TipManager.addItemTipById(mc, item.id)
        self.setItemCoolDown(i)

    def refreshFrame(self):
        if not self.widget:
            return
        self.refreshCash()
        self.refreshItemSlots()
        self.refreshItemCooldown()
        self.setPropsVisible(self.isShowProp)
        self.refreshAttrs()

    def _initUI(self):
        self.widget.hit.alpha = 0
        ASUtils.setHitTestDisable(self.widget.mainMc.menu.shopEff, True)
        ASUtils.setHitTestDisable(self.widget.mainMc.menu.menuBg, True)
        self.itemMcList = []
        for i in xrange(BAG_MAX_CNT):
            mc = self.widget.mainMc.bagItems.getChildByName('item%d' % i)
            self.itemMcList.append(mc)
            ASUtils.setMcData(mc, 'slotIdx', i)
            mc.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)

        self.widget.mainMc.menu.btnShop.addEventListener(events.MOUSE_CLICK, self.handleShopClick, False, 0, True)
        for i in xrange(PROP_MAX_CNT):
            mc = self.widget.mainMc.props.list.getChildByName('prop%d' % i)
            mc.propIcon.gotoAndStop('att%d' % i)
            self.propMcList.append(mc)

        for i in xrange(TEAMMATE_MAX_CNT):
            mySide = self.widget.mainMc.members.getChildByName('teammate%d' % i)
            enemySide = self.widget.mainMc.members.getChildByName('enemy%d' % i)
            enemySide.gotoAndStop('si')
            enemySide.gem.visible = False
            enemySide.headIcon.fitSize = True
            enemySide.visible = False
            mySide.gem.gotoAndStop('full')
            self.selfSideMcList.append(mySide)
            self.enemySideMcList.append(enemySide)

        self.widget.mainMc.menu.showHideProp.addEventListener(events.MOUSE_CLICK, self.handleShopProp, False, 0, True)
        self.widget.mainMc.menu.btnShoes.addEventListener(events.MOUSE_CLICK, self.handleReturnHome, False, 0, True)

    def handleReturnHome(self, *args):
        p = BigWorld.player()
        if not p:
            return
        if formula.inDotaBattleField(p.mapID):
            p.cell.onGoHome()

    def handleShopProp(self, *args):
        self.setPropsVisible(not self.isShowProp)

    def handleItemClick(self, *args):
        e = ASObject(args[3][0])
        slotId = int(e.currentTarget.slotIdx)
        p = BigWorld.player()
        mapId = p.mapID
        if formula.inDotaBattleField(mapId):
            self.doUseDotaItem(slotId)

    def doUseDotaItem(self, slotId):
        p = BigWorld.player()
        item = p.battleFieldBag.get(slotId, None)
        if item:
            remain, total = logicInfo.getItemCooldDownTime(item.id)
            if remain > 0:
                if item.isEquip():
                    p.showGameMsg(GMDD.data.SKILL_NOT_READY, ())
                else:
                    p.showGameMsg(GMDD.data.ITEM_NOT_READY, ())
                return
            if item.isEquip():
                skillId = ED.data.get(item.id, {}).get('skillId', 0)
                if skillId:
                    p.cell.useEquipmentSkill(slotId, skillId, p.id)
            else:
                p.cell.useDotaBattleFieldItem(item.id, slotId)

    def refreshItemCooldown(self, list = None):
        if not self.widget:
            return
        list = list if list else range(BAG_MAX_CNT)
        for i in list:
            self.setItemCoolDown(i)

    def setItemCoolDown(self, index):
        p = BigWorld.player()
        mc = self.itemMcList[index]
        item = p.battleFieldBag.get(index, None)
        if not item:
            mc.stopCooldown()
            return
        else:
            remain, total = logicInfo.getItemCooldDownTime(item.id)
            pSkillRemain, pSkillTotal = self.getPskillCd(item)
            if remain > 0:
                self.itemPlayPlayCoolDown(index, mc, remain, total)
            elif pSkillRemain > 0:
                self.itemPlayPlayCoolDown(index, mc, pSkillRemain, pSkillTotal)
            else:
                mc.stopCooldown()
            return

    def itemPlayPlayCoolDown(self, i, mc, remain, total):
        remain = int(remain)
        total = int(total)
        mc.playCooldown(total * 1000, (total - remain) * 1000)
        if self.callbackHandler.get(i, None):
            BigWorld.cancelCallback(self.callbackHandler[i])
        self.callbackHandler[i] = BigWorld.callback(remain, Functor(self.afterItemEndCooldown, i))

    def getPskillCd(self, item):
        p = BigWorld.player()
        extraDotaPskillIds = ID.data.get(item.id, {}).get('extraDotaPskillIds', [])
        remainTime = 0
        maxRemainTimeSkillId = 0
        maxRemainTimeSkillLv = 0
        for skillId, lv in extraDotaPskillIds:
            if skillId not in p.triggerPSkills:
                continue
            cd = p.triggerPSkills[skillId].nextTriggerTime - utils.getNow()
            if cd > remainTime:
                maxRemainTimeSkillId = skillId
                maxRemainTimeSkillLv = lv
                remainTime = cd

        total = PSD.data.get((maxRemainTimeSkillId, maxRemainTimeSkillLv), {}).get('triggerCD', 0)
        return (remainTime, total)

    def useItem(self, idx, isDown, isKeyMode = True, byBfDota = False):
        if not isDown:
            return
        p = BigWorld.player()
        if formula.inDotaBattleField(p.mapID) and not byBfDota:
            return
        if not formula.inDotaBattleField(p.mapID) and byBfDota:
            return
        p = BigWorld.player()
        mapId = p.mapID
        if formula.inDotaBattleField(mapId):
            self.doUseDotaItem(idx)

    def afterItemEndCooldown(self, index):
        if not self.widget:
            return
        self.itemMcList[index].endCooldown()

    def handleShopClick(self, *args):
        self.doOpenShopClick()

    def doOpenShopClick(self):
        p = BigWorld.player()
        if not p:
            return
        if not self.uiAdapter.bfDotaShop.widget:
            shopId = DCD.data.get('BF_DOTA_COMPOSITE_SHOP_ID', 0)
            p.base.openPrivateShop(0, shopId)
        elif self.uiAdapter.bfDotaShop.widget.visible:
            self.uiAdapter.bfDotaShop.setVisible(False)
        else:
            self.uiAdapter.bfDotaShop.setVisible(True)

    def onCloseClick(self, *args):
        self.hide()

    def getSlotValue(self, movie, idItem, idCon):
        p = BigWorld.player()
        mapId = p.mapID
        data = {}
        if formula.inDotaBattleField(mapId):
            item = p.battleFieldBag.get(idItem, None)
        else:
            item = p.inv.getQuickVal(0, idItem)
        if item != None:
            data = uiUtils.getGfxItem(item)
        else:
            data['iconPath'] = 'notFound'
        return uiUtils.dict2GfxDict(data)

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (0, int(idItem[4:]))

    def onNotifySlotMouseDown(self, *arg):
        p = BigWorld.player()
        key = arg[3][0].GetString()
        _, slotId = self.getSlotID(key)
        item = p.battleFieldBag.get(slotId, None)
        if not item:
            return
        else:
            p.cell.useDotaBattleFieldItem(item.id, slotId)
            return

    def updateTick(self):
        if not self.widget:
            return
        try:
            p = BigWorld.player()
            if p.bianshen[1]:
                self.refreshTeamMatesInfo()
                self.refreshEnemyInfo()
                self.refreshAttrs()
        except Exception as e:
            import traceback
            traceback.print_exc()
            gamelog.error('@jbx:error', Exception, e)

        BigWorld.callback(0.5, self.updateTick)

    def hadInitSkill(self, gbId):
        notifySkillId = 0
        p = BigWorld.player()
        zaijuId = p.bfDotaZaijuRecord.get(gbId, 0)
        if not zaijuId:
            return False
        else:
            for skillId, lv in ZD.data.get(zaijuId, {}).get('skills', ()):
                if SGD.data.get((skillId, 1), {}).get('notifyDotaSkillCD', 0):
                    notifySkillId = skillId
                    break

            if gbId == p.gbId:
                return self.uiAdapter.zaijuV2.serverSkills.get(skillId, (0, 0))[1] > 0
            return p.bfDotaSkillInitRecord.get(gbId, {}).get(notifySkillId, False)

    def refreshTeamMatesInfo(self, event = None):
        p = BigWorld.player()
        if not p:
            return
        else:
            infoList = []
            idList = []
            selfSideNUID = p.bfSideNUID
            for gbId, mInfo in p.battleFieldTeam.iteritems():
                if gbId == p.gbId:
                    continue
                if mInfo['sideNUID'] == selfSideNUID:
                    idList.append(gbId)

            info = {}
            memItem = p.getMemInfoByGbId(p.gbId)
            info['gbId'] = p.gbId
            info['reliveTime'] = uiUtils.getBFReliveTime(memItem, p.gbId)
            info['hp'] = p.hp
            info['mhp'] = p.mhp
            info['mp'] = p.mp
            info['mmp'] = p.mmp
            info['name'] = p.roleName
            data = ZD.data.get(p.bianshen[1], {})
            info['energyType'] = data.get('bfDotaZaijuEnergyType', 0)
            info['headIcon'] = uiUtils.getZaijuLittleHeadIconPathById(p.bianshen[1])
            info['lv'] = p.getPlayerDotaLv(p.gbId)
            info['hadInitSkill'] = self.hadInitSkill(p.gbId)
            infoList.append(info)
            for gbId in idList:
                info = self.getTeamInfoByGbId(gbId)
                if info:
                    infoList.append(info)

            infoList.sort(cmp=lambda x, y: cmp(x['name'], y['name']))
            for i in xrange(TEAMMATE_MAX_CNT):
                info = infoList[i] if i < len(infoList) else None
                self.setTeammateMc(self.selfSideMcList[i], info, i)

            return

    def refreshKeyText(self):
        if not self.widget:
            return
        self.widget.mainMc.menu.btnShoes.label = HK.HKM[HK.KEY_DOTA_RETURN_HOME].getDesc()
        self.widget.mainMc.menu.btnShop.label = HK.HKM[HK.KEY_DOTA_OPEN_SHOP].getDesc()

    def getTeamInfoByGbId(self, gbId):
        p = BigWorld.player()
        memItem = p.getMemInfoByGbId(gbId)
        info = {}
        info['reliveTime'] = uiUtils.getBFReliveTime(memItem, gbId)
        zaijuId = p.bfDotaZaijuRecord.get(gbId, 0)
        data = ZD.data.get(zaijuId, {})
        info['headIcon'] = uiUtils.getZaijuLittleHeadIconPathById(zaijuId)
        info['energyType'] = data.get('bfDotaZaijuEnergyType', 0)
        info['cdTime'] = (0, 10)
        entityId = p.battleFieldTeam.get(gbId, {}).get('id', 0)
        entity = BigWorld.entities.get(entityId, None)
        info['gbId'] = gbId
        info['name'] = p.battleFieldTeam.get(gbId, {}).get('roleName', '')
        info['hadInitSkill'] = self.hadInitSkill(gbId)
        if not entity:
            rawInfo = p.bfTeammateInfo.get(gbId, None)
            if rawInfo:
                info['hp'] = rawInfo.get(gametypes.TEAM_SYNC_PROPERTY_HP, 0)
                info['mhp'] = rawInfo.get(gametypes.TEAM_SYNC_PROPERTY_MHP, 0)
                info['mp'] = rawInfo.get(gametypes.TEAM_SYNC_PROPERTY_MP, 0)
                info['mmp'] = rawInfo.get(gametypes.TEAM_SYNC_PROPERTY_MMP, 0)
                info['lv'] = p.getPlayerDotaLv(gbId)
            else:
                return
        else:
            info['hp'] = entity.hp
            info['mhp'] = entity.mhp
            info['mp'] = entity.mp
            info['mmp'] = entity.mmp
            info['lv'] = p.getPlayerDotaLv(gbId)
        return info

    def refreshEnemyInfo(self):
        p = BigWorld.player()
        idList = p.getEnemyGbIdList()
        infoList = []
        for gbId in idList:
            info = {}
            memItem = p.getMemInfoByGbId(gbId)
            info['reliveTime'] = uiUtils.getBFReliveTime(memItem, gbId)
            if info['reliveTime'] <= 0:
                continue
            info['gbId'] = gbId
            zaijuId = p.bfDotaZaijuRecord.get(gbId, 0)
            info['headIcon'] = uiUtils.getZaijuLittleHeadIconPathById(zaijuId)
            infoList.append(info)

        infoList.sort(key=lambda x: x['reliveTime'])
        for index, info in enumerate(infoList):
            mc = self.enemySideMcList[index]
            mc.visible = True
            mc.txtCountDown.text = str(info['reliveTime'])
            mc.headIcon.fitSize = True
            mc.headIcon.loadImage(info['headIcon'])

        for i in xrange(len(infoList), TEAMMATE_MAX_CNT):
            mc = self.enemySideMcList[i]
            mc.visible = False

    def setTeammateMc(self, mc, info, index):
        if not info:
            mc.visible = False
            return
        mc.visible = True
        if info['gbId'] == BigWorld.player().gbId:
            self.uiAdapter.zaijuV2.setReliveCountDown(info['reliveTime'])
        if info['reliveTime'] > 0:
            mc.gotoAndStop('si')
            mc.txtCountDown.text = str(info['reliveTime'])
            return
        mc.gotoAndStop('huo')
        mc.hpBar.currentValue = info['hp']
        mc.hpBar.maxValue = info['mhp']
        mc.hpBar.lableVisible = False
        mc.mpBar.currentValue = info['mp']
        mc.mpBar.maxValue = info['mmp']
        mc.mpBar.lableVisible = False
        mc.headIcon.fitSize = True
        mc.headIcon.loadImage(info['headIcon'])
        mc.lv.txtLv.text = info['lv']
        if mc.gem.visible and not info['hadInitSkill']:
            mc.gem.visible = False
        elif not mc.gem.visible and info['hadInitSkill']:
            mc.gem.visible = True
        mc.gbId = info['gbId']

    def playSkillCdCoolDown(self, gbId, skillId, skillLv, skillCdTime):
        for mc in self.selfSideMcList:
            if mc.visible and mc.gbId and int(mc.gbId) == gbId:
                mc.gem.gotoAndStop('charge')
                mc.gem.gemMask.y = GEM_ZERO_POS
                tweenData = {}
                tweenData['time'] = skillCdTime
                tweenData['transition'] = 'linear'
                tweenData['y'] = GEM_FULL_POS
                tweenData['onCompleteParams'] = (gbId,)
                ASUtils.addTweener(mc.gem.gemMask, tweenData, self.endTweenCallBack)

    def endTweenCallBack(self, *args):
        gbId = int(args[3][0].GetString())
        BigWorld.player().args = args
        for mc in self.selfSideMcList:
            if mc.visible and mc.gbId and int(mc.gbId) == gbId:
                mc.gem.gotoAndStop('full')
                break

    def enemyReliveCountDonw(self, mc, time, key):
        mc.txtCountDown.text = str(time)
        if time > 0:
            fun = Functor(self.enemyReliveCountDonw, mc, time - 1, key)
            self.callbackHandler[key] = BigWorld.callback(1, fun)
        else:
            mc.visible = False

    def getAttrsInfo(self):
        attrsInfo = []
        attrKeys = DCD.data.get('zaiju_shows_attr_types', ())
        if attrKeys:
            info = [ RPAD.data[key] for key in attrKeys if RPAD.data.has_key(key) ]
            attrsInfo = self.uiAdapter.roleInfo.createArr(info, True, False)
        return attrsInfo
