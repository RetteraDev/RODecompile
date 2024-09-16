#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bossInfoProxy.o
import BigWorld
from VirtualMonster import VirtualMonster
from Monster import Monster
import gameglobal
import gametypes
import uiConst
import uiUtils
from uiProxy import UIProxy
from ui import gbk2unicode
from data import boss_client_data as BCD

class BossInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BossInfoProxy, self).__init__(uiAdapter)
        self.modelMap = {'getBossInfo': self.onGetBossInfo}
        self.mediator = None
        self.callbackHandler = None

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BOSS_INFO)

    def reset(self):
        pass

    def show(self):
        p = BigWorld.player()
        if isinstance(p.targetLocked, VirtualMonster):
            target = p.targetLocked
            master = BigWorld.entities.get(target.masterMonsterID)
            if not master:
                return
        elif isinstance(p.targetLocked, Monster):
            master = p.targetLocked
        else:
            return
        masterData = BCD.data.get(master.charType, None)
        if masterData is None:
            return
        else:
            showBlood = uiUtils._isNeedShowBossBlood(master.charType)
            if showBlood == 1 and not master.inDying or master.inDying and showBlood == 2:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BOSS_INFO)
            return

    def review(self):
        if self.mediator:
            self.mediator.Invoke('resetView')

    def getVMName(self, mCharType, charType):
        data = BCD.data.get(mCharType)
        if data is not None:
            if data['vm1Info'][1] == charType:
                return (data['vm1Info'][2], data['vm1Info'][0])
            if data['vm2Info'][1] == charType:
                return (data['vm2Info'][2], data['vm2Info'][0])
            if data['vm3Info'][1] == charType:
                return (data['vm3Info'][2], data['vm3Info'][0])
        return (None, None)

    def onGetBossInfo(self, *arg):
        p = BigWorld.player()
        if isinstance(p.targetLocked, VirtualMonster):
            target = p.targetLocked
            master = BigWorld.entities.get(target.masterMonsterID)
            if not master:
                return
        elif isinstance(p.targetLocked, Monster):
            master = p.targetLocked
        else:
            return
        Info = []
        vmItemInfo = []
        masterInfo = []
        vmInfo = []
        masterData = BCD.data.get(master.charType)
        Info.append(gbk2unicode(masterData['monsterName']))
        Info.append(gbk2unicode(masterData.get('monsterTitle', '')))
        Info.append(gbk2unicode(masterData.get('characterDesc', '')))
        Info.append(gbk2unicode(masterData.get('swfName', '')))
        if master.specialStateMaxVal[0] != 0:
            masterInfo.append([3, float(master.specialStateVal[0]) / master.specialStateMaxVal[0] * 100])
        if master.specialStateMaxVal[1] != 0:
            masterInfo.append([1, float(master.specialStateVal[1]) / master.specialStateMaxVal[1] * 100])
        if master.specialStateMaxVal[2] != 0:
            masterInfo.append([4, float(master.specialStateVal[2]) / master.specialStateMaxVal[2] * 100])
        Info.append(masterInfo)
        if master.syncUnits:
            for item in master.syncUnits.items():
                vmItemInfo = []
                vmCharType = item[0]
                vmName, vmNum = self.getVMName(master.charType, vmCharType)
                if not vmName:
                    return
                vm = BigWorld.entities.get(item[1][0])
                if vm is not None and vm.life == gametypes.LIFE_ALIVE:
                    if vm.specialStateMaxVal[0] != 0:
                        vmItemInfo.append([3, float(vm.specialStateVal[0]) / vm.specialStateMaxVal[0] * 100])
                    if vm.specialStateMaxVal[3] != 0:
                        vmItemInfo.append([2, float(vm.specialStateVal[3]) / vm.specialStateMaxVal[3] * 100])
                vmInfo.append([gbk2unicode(vmName), vmNum, vmItemInfo])

            Info.append(vmInfo)
        return uiUtils.array2GfxAarry(Info)
