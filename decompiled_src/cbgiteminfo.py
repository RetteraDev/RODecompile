#Embedded file name: /WORKSPACE/data/entities/common/cbgiteminfo.o
from userInfo import UserInfo
from cbgItem import CbgItem, CbgStubItem, CbgStubItemDict
from itemInfo import ItemInfo

class CbgItemInfo(UserInfo):

    def createObjFromDict(self, data):
        d = data['data']
        obj = CbgItem()
        obj.consignItem = d.get('consignItem', {})
        obj.purchaseItem = d.get('purchaseItem', {})
        return obj

    def getDictFromObj(self, obj):
        data = {'consignItem': obj.consignItem,
         'purchaseItem': obj.purchaseItem}
        return {'data': data}

    def isSameType(self, obj):
        return type(obj) is CbgItem


instance = CbgItemInfo()

class CbgStubItemInfo(UserInfo):

    def createObjFromDict(self, data):
        obj = CbgStubItemDict()
        for d in data['data']:
            itVal = CbgStubItem(gbId=d.get('gbId', 0), roleName=d.get('roleName', ''), hostId=d.get('hostId', 0), it=d.get('it', None), price=d.get('price', 0), days=d.get('days', 0), argue=d.get('argue', False), tProtect=d.get('tProtect', 0), favor=d.get('favor', 0), opNUID=d.get('opNUID', 0))
            obj[itVal.it.uuid] = itVal

        return obj

    def getDictFromObj(self, obj):
        data = []
        for itVal in obj.itervalues():
            data.append({'gbId': itVal.gbId,
             'roleName': itVal.roleName,
             'hostId': itVal.hostId,
             'it': itVal.it,
             'price': itVal.price,
             'days': itVal.days,
             'argue': itVal.argue,
             'tProtect': itVal.tProtect,
             'favor': itVal.favor,
             'opNUID': itVal.opNUID})

        return {'data': data}

    def isSameType(self, obj):
        return type(obj) is CbgStubItemDict


stubInstance = CbgStubItemInfo()

class CbgStubItemValInfo(UserInfo):

    def createObjFromDict(self, d):
        obj = CbgStubItem(gbId=d.get('gbId', 0), roleName=d.get('roleName', ''), hostId=d.get('hostId', 0), it=d.get('it', None), price=d.get('price', 0), days=d.get('days', 0), argue=d.get('argue', False), tProtect=d.get('tProtect', 0), favor=d.get('favor', 0), opNUID=d.get('opNUID', 0))
        return obj

    def getDictFromObj(self, obj):
        data = {'gbId': obj.gbId,
         'roleName': obj.roleName,
         'hostId': obj.hostId,
         'it': obj.it,
         'price': obj.price,
         'days': obj.days,
         'argue': obj.argue,
         'tProtect': obj.tProtect,
         'favor': obj.favor,
         'opNUID': obj.opNUID}
        return data

    def isSameType(self, obj):
        return type(obj) is CbgStubItem


valInstance = CbgStubItemValInfo()
