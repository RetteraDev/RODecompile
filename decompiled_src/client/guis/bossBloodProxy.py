#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bossBloodProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import utils
from VirtualMonster import VirtualMonster
from guis import uiUtils
from guis import events
from uiProxy import DataProxy
from ui import gbk2unicode
import uiConst
from gameStrings import gameStrings
from data import boss_client_data as BCD
from data import monster_model_client_data as MMCD
from data import monster_random_prop_data as MRPD
from cdata import prop_def_data as PDD
from data import prop_data as PD
from data import sys_config_data as SCD
BOSS_ICON_PRE_PATH = 'bossbloodicon/%d.dds'

class BossBloodProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(BossBloodProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerBossBlood': self.onRegisterBossBlood,
         'targetSelect': self.onTargetSelect,
         'selectVM': self.onSelectVM,
         'getTargetEntId': self.onGetTargetEntId}
        self.mc = None
        self.bloodOwner = None
        self.boss2tar = None
        self.addEvent(events.EVENT_TARGET_DISTANCE_UPDATE, self.setDir)

    def onRegisterBossBlood(self, *arg):
        self.mc = arg[3][0]
        self.mc.SetVisible(False)
        self.mc.Invoke('setHideHPNum', GfxValue(0))
        self.mc.Invoke('setDetailPersent', GfxValue(0))

    def reset(self):
        self.mc = None

    def clearWidget(self):
        self.mc = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BOSSBLOOD)

    def onGetTargetEntId(self, *arg):
        target = BigWorld.player().targetLocked
        if isinstance(target, VirtualMonster):
            master = BigWorld.entities.get(target.masterMonsterID)
        else:
            master = target
        if not master:
            return GfxValue(0)
        return GfxValue(master.id)

    def onSelectVM(self, *arg):
        charType = arg[3][0].GetNumber()
        p = BigWorld.player()
        target = p.targetLocked
        if not hasattr(target, 'masterMonsterID'):
            return
        master = BigWorld.entities.get(target.masterMonsterID)
        if master and master.syncUnits.get(charType):
            entId = master.syncUnits[charType][0]
            ent = BigWorld.entities.get(entId)
            p.lockTarget(ent)

    def _getVMType(self, mCharType, charType):
        data = BCD.data.get(mCharType)
        if data is not None:
            if data['vm1Info'][1] == charType:
                return data['vm1Info'][4]
            if data['vm2Info'][1] == charType:
                return data['vm2Info'][4]
            if data['vm3Info'][1] == charType:
                return data['vm3Info'][4]

    def selectVMBtn(self, charType):
        self.mc.Invoke('selectVMBtn', GfxValue(charType))

    def setHideHpNum(self, hide):
        if self.mc:
            self.mc.Invoke('setHideHPNum', GfxValue(hide))

    def setDetailPersent(self, detail):
        if self.mc:
            self.mc.Invoke('setDetailPersent', GfxValue(detail))

    def setVMBtn(self):
        arr = []
        p = BigWorld.player()
        if not isinstance(p.targetLocked, VirtualMonster):
            self.mc.Invoke('setPartBtn', uiUtils.array2GfxAarry(arr))
            return
        target = p.targetLocked
        master = BigWorld.entities.get(target.masterMonsterID)
        if master.syncUnits:
            for item in master.syncUnits.items():
                vmCharType = item[0]
                btnType = self._getVMType(master.charType, vmCharType)
                arr.append([gbk2unicode(btnType), vmCharType])

            data = BCD.data.get(master.charType)
            self.mc.Invoke('setPartBtn', uiUtils.array2GfxAarry(arr))

    def initHp(self, hp, mhp, iconPath, isDmgMode = False):
        if self.mc:
            self.mc.Invoke('initHp', (GfxValue(float(hp)),
             GfxValue(float(mhp)),
             GfxValue(iconPath),
             GfxValue(isDmgMode)))

    def minusBlood(self, val):
        self.mc.Invoke('minusBlood', GfxValue(int(val)))

    def showBossBlood(self, owner, visible):
        if self.mc:
            self.bloodOwner = owner
            self.mc.SetVisible(visible)
            self.setHideBloodNumState()
            self.mc.Invoke('setHideHPNum', GfxValue(0))
            self.mc.Invoke('setDetailPersent', GfxValue(0))
        else:
            return
        gameglobal.rds.ui.target.hideTargetUnitFrame()
        self.setVMBtn()
        self.setTargetQiJue()
        master = BigWorld.entities.get(owner)
        data = MMCD.data.get(getattr(master, 'charType', 0), {})
        equipTag = BigWorld.player().mapID in data.get('equipTagMapList', [])
        self.setHideHpNum(data.get('hideHpNum', 0))
        self.setDetailPersent(data.get('showDetailPersent', 0))
        self.setBossTargetRandProps()
        self.showEquipTagIcon(equipTag)
        self.setBossIcon(data.get('bossBloodIcon', 0))
        self.showBossInfoTips(master)
        equipTag and gameglobal.rds.tutorial.onLoadedWidgetTrigger(uiConst.WIDGET_BOSSBLOOD)

    def setBossIcon(self, iconId):
        if not self.mc:
            return
        iconPath = BOSS_ICON_PRE_PATH % iconId if iconId else ''
        self.mc.Invoke('setBossIcon', GfxValue(iconPath))

    def setBossTargetRandProps(self):
        if not self.mc:
            return
        p = BigWorld.player()
        t = p.targetLocked
        if not t:
            return
        randProps = getattr(t, 'randProps', ())
        propsList = []
        for props in randProps:
            if props in MRPD.data:
                name = MRPD.data[props].get('name', '')
                type = MRPD.data[props].get('colorType', 1)
                propsList.append((name, type))

        self.mc.Invoke('setBossTargetRandProps', uiUtils.array2GfxAarry(propsList, True))

    def setTargetQiJue(self):
        target = BigWorld.player().targetLocked
        if target and hasattr(target, 'specialStateVal'):
            if target.specialStateMaxVal[0] != 0:
                val = float(target.specialStateVal[0]) / target.specialStateMaxVal[0]
                self.setQiJue(val, 1)
            elif len(target.specialStateMaxVal) == 4 and target.specialStateMaxVal[3] != 0:
                val = float(target.specialStateVal[3]) / target.specialStateMaxVal[3]
                self.setQiJue(val, 2)
            else:
                self.setQiJue(-1, 1)

    def hideBossBlood(self):
        if gameglobal.rds.ui.isHideAllUI():
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_BOSSBLOOD, False)
            return
        else:
            if self.mc:
                self.mc.SetVisible(False)
            else:
                return
            self.bloodOwner = None
            target = BigWorld.player().targetLocked
            if not utils.instanceof(target, 'SpawnPoint') and not utils.instanceof(target, 'DroppedItem') and not utils.instanceof(target, 'QuestBox') and not utils.instanceof(target, 'Transport') and not utils.instanceof(target, 'TreasureBox'):
                gameglobal.rds.ui.target.showTargetUnitFrame()
                if gameglobal.rds.ui.bossInfo.mediator:
                    gameglobal.rds.ui.bossInfo.hide()
            return

    def hit(self):
        if self.mc != None:
            self.mc.Invoke('beHitInDying')

    def setName(self, name):
        if self.mc:
            nameMc = self.mc.GetMember('bossUF').GetMember('tf_Name')
            nameMc and self.mc.Invoke('setName', GfxValue(gbk2unicode(name)))

    def setPartName(self, name):
        if self.mc and self.mc.GetMember('bossUF'):
            self.setTargetQiJue()
            partNameText = self.mc.GetMember('bossUF').GetMember('tf_PartName')
            if partNameText:
                partNameText.SetText(gbk2unicode(name))
            self.setShortName()

    def setShortName(self):
        p = BigWorld.player()
        if self.mc:
            if not isinstance(p.targetLocked, VirtualMonster):
                self.mc.Invoke('setVmName', GfxValue(''))
            else:
                master = BigWorld.entities.get(p.targetLocked.masterMonsterID)
                if not master:
                    return
                shortName = self._getVMType(master.charType, p.targetLocked.charType)
                self.mc.Invoke('setVmName', GfxValue(gbk2unicode(shortName)))

    def setLevel(self, monster):
        lv = monster.lv
        show = True
        if hasattr(monster, 'needHideTargetProxyLv') and monster.needHideTargetProxyLv():
            show = False
        if self.mc and self.mc.GetMember('bossUF'):
            lvMc = self.mc.GetMember('bossUF').GetMember('tf_Level')
            lv = 'Lv ' + str(lv) if show else ''
            lvMc and self.mc.Invoke('setLv', GfxValue(gbk2unicode(lv)))

    def changeStateIcon(self, addData, delData):
        if self.mc:
            self.mc.Invoke('changeState', (uiUtils.array2GfxAarry(addData), uiUtils.array2GfxAarry(delData)))

    def delMasterStateIcon(self, id):
        if self.mc:
            self.mc.Invoke('delBuff', GfxValue(id))

    def clearMasterStateIcon(self):
        if self.mc:
            self.mc.Invoke('clearBuff')

    def changePartStateIcon(self, addData, delData):
        if self.mc:
            self.mc.Invoke('changeState', (uiUtils.array2GfxAarry(addData), uiUtils.array2GfxAarry(delData)))

    def delPartStateIcon(self, id):
        if self.mc:
            self.mc.Invoke('delBuff', GfxValue(id))

    def clearPartStateIcon(self):
        if self.mc:
            self.mc.Invoke('clearBuff')

    def setBossTargetName(self, roleName):
        if self.mc:
            self.mc.Invoke('setBossTargetName', GfxValue(gbk2unicode(roleName)))

    def setBossTargetVisible(self, flag):
        if self.mc:
            self.mc.Invoke('setBossTargetVisible', GfxValue(flag))

    def setBossTargetLockName(self, id):
        ent = BigWorld.entities.get(id, None)
        if ent == None or ent.roleName == None:
            self.setBossTargetVisible(False)
        else:
            self.boss2tar = ent
            if getattr(ent, 'roleName', None):
                if getattr(ent, 'jctSeq', 0) and BigWorld.player().inClanCourier():
                    self.setBossTargetName(ent.getJCTRoleName())
                else:
                    self.setBossTargetName(ent.roleName)
            if hasattr(ent, 'hp'):
                self.setTargetHp(ent.hp)
            if hasattr(ent, 'mhp'):
                self.setTargetMhp(ent.mhp)

    def onTargetSelect(self, *arg):
        self.mc.SetVisible(False)
        uiUtils.onTargetSelect(self.boss2tar)

    def setTargetHp(self, value):
        if self.mc != None:
            if not value:
                value = 0
            self.mc.Invoke('setT2THp', GfxValue(float(value)))

    def setTargetMhp(self, value):
        if self.mc != None:
            if not value:
                value = 0
            self.mc.Invoke('setT2TMhp', GfxValue(float(value)))

    def setQiJue(self, value, tipType):
        if self.mc != None:
            self.mc.Invoke('setQiJue', (GfxValue(value), GfxValue(tipType)))

    def setDir(self, event):
        if self.mc != None:
            self.mc.Invoke('setDir', GfxValue(event.data))

    def showEquipTagIcon(self, isShow):
        if self.mc and self.mc.GetMember('bossUF'):
            equipTagIconMc = self.mc.GetMember('bossUF').GetMember('equipTag')
            equipTagIconMc and self.mc.Invoke('setEquipTag', GfxValue(isShow))

    def setHideBloodNumState(self):
        if self.mc == None or not self.bloodOwner:
            return
        else:
            monster = BigWorld.entities.get(self.bloodOwner, None)
            if not monster:
                return
            isHideBloodNum = getattr(monster, 'isHideBloodNum', False)
            isTarget2HideBloodNumState = False
            if monster.lockedId and BigWorld.entities.get(monster.lockedId, None):
                isTarget2HideBloodNumState = getattr(BigWorld.entities[monster.lockedId], 'isHideBloodNum', False)
            self.mc.Invoke('setHideBloodNumState', uiUtils.array2GfxAarry((isHideBloodNum, isTarget2HideBloodNumState)))
            if not isHideBloodNum:
                self.initHp(getattr(monster, 'hp', 0), getattr(monster, 'mhp', 1), '', getattr(monster, 'isDmgMode', False))
            if not isTarget2HideBloodNumState:
                self.mc.Invoke('updateTar2TarHealBar')
            return

    def showBossInfoTips(self, entity):
        showData = dict()
        showData['isShow'] = True
        if hasattr(entity, 'pveQuota') and entity.pveQuota > 0:
            showData['isShow'] = True
            showData['mainInfoTxt'] = gameStrings.COMMON_KEY_VALUE % (self.getMonstarPropsSpecialName(PDD.data.PROPERTY_PVE_QUOTA, ''), str(entity.pveQuota))
            showData['allInfoTxt'] = self.getMonsterPropsSpecialTip(PDD.data.PROPERTY_PVE_QUOTA, '')
        else:
            showData['isShow'] = False
        if self.mc:
            self.mc.Invoke('showBossInfoTips', uiUtils.dict2GfxDict(showData, True))

    def getMonstarPropsSpecialName(self, propId, defaultResult):
        monsterPropsSpecialInfo = SCD.data.get('monsterPropsSpecialInfo')
        result = monsterPropsSpecialInfo.get(propId, {}).get('name', None)
        if not result:
            result = PD.data.get(propId, {}).get('chName', defaultResult)
        return result

    def getMonsterPropsSpecialTip(self, propId, defaultResult):
        monsterPropsSpecialInfo = SCD.data.get('monsterPropsSpecialInfo')
        result = monsterPropsSpecialInfo.get(propId, {}).get('tip', defaultResult)
        return result
