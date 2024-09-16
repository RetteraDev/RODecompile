#Embedded file name: I:/bag/tmp/tw2/res/entities\common/roleSaleDataInfo.o
from roleSaleData import RoleSaleData
from userInfo import UserInfo

class RoleSaleDataInfo(UserInfo):

    def createObjFromDict(self, d):
        obj = RoleSaleData()
        data = d['data'][0]
        obj.saleStatus = data['saleStatus']
        obj.saleStatusTime = data['saleStatusTime']
        obj.salePrice = data['salePrice']
        obj.saleDays = data['saleDays']
        obj.vendeeGbId = data['vendeeGbId']
        obj.lastSaleDoneTime = data['lastSaleDoneTime']
        obj.newSaleFlag = data['newSaleFlag']
        obj.newSaleFlagStartTime = data['newSaleFlagStartTime']
        obj.ip = data['ip']
        obj.inSaleOperating = data['inSaleOperating']
        obj.unbindCoinCost = data['unbindCoinCost']
        obj.bindCoinCost = data['bindCoinCost']
        return obj

    def getDictFromObj(self, obj):
        data = {'saleStatus': obj.saleStatus,
         'saleStatusTime': obj.saleStatusTime,
         'salePrice': obj.salePrice,
         'saleDays': obj.saleDays,
         'vendeeGbId': obj.vendeeGbId,
         'lastSaleDoneTime': obj.lastSaleDoneTime,
         'newSaleFlag': obj.newSaleFlag,
         'newSaleFlagStartTime': obj.newSaleFlagStartTime,
         'ip': obj.ip,
         'inSaleOperating': obj.inSaleOperating,
         'unbindCoinCost': obj.unbindCoinCost,
         'bindCoinCost': obj.bindCoinCost}
        return {'data': [data]}

    def isSameType(self, obj):
        return type(obj) is RoleSaleData


instance = RoleSaleDataInfo()
