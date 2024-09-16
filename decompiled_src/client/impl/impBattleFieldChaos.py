#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impBattleFieldChaos.o
import utils
from data import chaos_battle_field_buff_lv_data as CBFBLD
from data import chaos_battle_field_config_data as CBFCD
from data import state_data as SD

class ImpBattleFieldChaos(object):

    def getMergeBuffDesc(self):
        mergeDatas = []
        data = {}
        buffLv = self.bfChaosModeDetail['bfChaosModeRandomStatesLv']
        buffType = self.bfChaosModeDetail['bfChaosModeType']
        cfgData = CBFBLD.data.get((buffLv, buffType), {})
        fixedBuffList = self.bfChaosModeDetail['bfChaosModeFixedStates']
        randomBufList = self.bfChaosModeDetail['bfChaosModeRandomStates']
        bfChaosModeNextRandomTime = self.bfChaosModeDetail['bfChaosModeNextRandomTime']
        if fixedBuffList:
            data['icon'] = 'state/40/%s.dds' % CBFCD.data.get('fixedBuffIcon', 90073)
            data['tips'] = CBFCD.data.get('fixedBuffName', 'fixedBuffName') + '\n'
            data['tips'] += '\n'.join((SD.data.get(stateId, {}).get('desc', '') for stateId in fixedBuffList))
            data['cd'] = 'N/A'
            data['fixed'] = 1
            mergeDatas.append(data)
        if randomBufList:
            randomBuffData = {}
            randomBuffData['icon'] = 'state/40/%s.dds' % cfgData.get('icon', 90073)
            randomBuffData['tips'] = cfgData.get('name', '') + '\n'
            randomBuffData['tips'] += '\n'.join((SD.data.get(stateId, {}).get('desc', '') for stateId in randomBufList))
            randomBuffData['cd'] = int(bfChaosModeNextRandomTime - utils.getNow())
            mergeDatas.append(randomBuffData)
        return mergeDatas

    def updateMergeBuff(self, addSet, delSet):
        if not self.bfChaosModeDetail['bfChaosModeType']:
            return (addSet, delSet)
        filterAddSet = set()
        filterDelSet = set()
        fixedBuffList = self.bfChaosModeDetail['bfChaosModeFixedStates']
        randomBufList = self.bfChaosModeDetail['bfChaosModeRandomStates']
        for state in addSet:
            if state in fixedBuffList or state in randomBufList:
                continue
            else:
                filterAddSet.add(state)

        for state in delSet:
            if state in fixedBuffList or state in randomBufList:
                continue
            else:
                filterDelSet.add(state)

        return (filterAddSet, filterDelSet)
