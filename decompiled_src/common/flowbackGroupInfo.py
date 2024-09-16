#Embedded file name: I:/bag/tmp/tw2/res/entities\common/flowbackGroupInfo.o
import copy
import cPickle
from userInfo import UserInfo
from flowbackGroup import FlowbackGroup

class FlowbackGroupInfo(UserInfo):

    def createObjFromDict(self, d):
        obj = FlowbackGroup()
        if d.has_key('flowbackGroupData'):
            dict = d['flowbackGroupData']
            if dict.has_key('flowbackGroupType'):
                obj.flowbackGroupType = dict['flowbackGroupType']
            if dict.has_key('startTime'):
                obj.startTime = dict['startTime']
            if dict.has_key('endTime'):
                obj.endTime = dict['endTime']
            if dict.has_key('rechargeOp'):
                obj.rechargeOp = dict['rechargeOp']
            if dict.has_key('totalExp'):
                obj.totalExp = dict['totalExp']
            if dict.has_key('restExp'):
                obj.restExp = dict['restExp']
            if dict.has_key('totalBindCash'):
                obj.totalBindCash = dict['totalBindCash']
            if dict.has_key('restBindCash'):
                obj.restBindCash = dict['restBindCash']
            if dict.has_key('targetPoints'):
                obj.targetPoints = dict['targetPoints']
            if dict.has_key('targetPointsRewards'):
                obj.targetPointsRewards = copy.deepcopy(dict['targetPointsRewards'])
            if dict.has_key('targetsStateInfo'):
                obj.targetsStateInfo = copy.deepcopy(dict['targetsStateInfo'])
            if dict.has_key('flowbackGroupGoalVars'):
                obj.flowbackGroupGoalVars = copy.deepcopy(dict['flowbackGroupGoalVars'])
            if dict.has_key('flowbackGroupDailyGoalVarNames'):
                obj.flowbackGroupDailyGoalVarNames = copy.deepcopy(dict['flowbackGroupDailyGoalVarNames'])
            if dict.has_key('flowbackGroupAlreadyFinishedGoalIds'):
                obj.flowbackGroupAlreadyFinishedGoalIds = copy.deepcopy(dict['flowbackGroupAlreadyFinishedGoalIds'])
            if dict.has_key('privilegesInfo'):
                obj.privilegesInfo = copy.deepcopy(dict['privilegesInfo'])
            if dict.has_key('rechargeAmount'):
                obj.rechargeAmount = dict['rechargeAmount']
            if dict.has_key('rechargeRewards'):
                obj.rechargeRewards = copy.deepcopy(dict['rechargeRewards'])
        if d.has_key('auraEndTimerId'):
            obj.auraEndTimerId = d['auraEndTimerId']
        return obj

    def getDictFromObj(self, obj):
        d = {}
        d['flowbackGroupType'] = obj.flowbackGroupType
        d['startTime'] = obj.startTime
        d['endTime'] = obj.endTime
        d['rechargeOp'] = obj.rechargeOp
        d['totalExp'] = obj.totalExp
        d['restExp'] = obj.restExp
        d['totalBindCash'] = obj.totalBindCash
        d['restBindCash'] = obj.restBindCash
        d['targetPoints'] = obj.targetPoints
        d['targetPointsRewards'] = obj.targetPointsRewards
        d['targetsStateInfo'] = obj.targetsStateInfo
        d['flowbackGroupGoalVars'] = obj.flowbackGroupGoalVars
        d['flowbackGroupDailyGoalVarNames'] = obj.flowbackGroupDailyGoalVarNames
        d['flowbackGroupAlreadyFinishedGoalIds'] = obj.flowbackGroupAlreadyFinishedGoalIds
        d['privilegesInfo'] = obj.privilegesInfo
        d['rechargeAmount'] = obj.rechargeAmount
        d['rechargeRewards'] = obj.rechargeRewards
        return {'flowbackGroupData': d,
         'auraEndTimerId': obj.auraEndTimerId}

    def isSameType(self, obj):
        return type(obj) is FlowbackGroup


instance = FlowbackGroupInfo()
