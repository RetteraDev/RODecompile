#Embedded file name: /WORKSPACE/data/entities/common/zmjstarbossinfo.o
from userInfo import UserInfo
from zmjStarBoss import ZMJRoleVal, ZMJStarBossVal, ZMJStarBoss

class ZMJStarBossInfo(UserInfo):

    def createObjFromDict(self, dictData):
        obj = ZMJStarBoss()
        for child in dictData['items']:
            founder = child['founder']
            roleObj = ZMJRoleVal(founder['gbId'], founder['roleName'], founder['lv'], founder['photo'], founder['borderId'])
            boss = ZMJStarBossVal(child['fbNo'], child['star'], child['tExpire'], child['tValid'], roleObj, child['candidates'], child['ownerGbId'], child['ownerName'], child['killer'])
            obj[child['nuid']] = boss

        return obj

    def getDictFromObj(self, obj):
        items = []
        for nuid, boss in obj.iteritems():
            founder = {'gbId': boss.founder.gbId,
             'roleName': boss.founder.roleName,
             'lv': boss.founder.lv,
             'photo': boss.founder.photo,
             'borderId': boss.founder.borderId}
            items.append({'nuid': nuid,
             'fbNo': boss.fbNo,
             'star': boss.star,
             'founder': founder,
             'tExpire': boss.tExpire,
             'tValid': boss.tValid,
             'candidates': boss.candidates,
             'ownerGbId': boss.ownerGbId,
             'ownerName': boss.ownerName,
             'killer': boss.killer})

        return {'items': items}

    def isSameType(self, obj):
        return type(obj) is ZMJStarBoss


starBossInstance = ZMJStarBossInfo()

class ZMJStarBossValInfo(UserInfo):

    def createObjFromDict(self, dictData):
        founder = dictData['founder']
        roleObj = ZMJRoleVal(founder['gbId'], founder['roleName'], founder['lv'], founder['photo'], founder['borderId'])
        obj = ZMJStarBossVal(dictData['fbNo'], dictData['star'], dictData['tExpire'], dictData['tValid'], roleObj, dictData['candidates'], dictData['ownerGbId'], dictData['ownerName'], dictData['killer'])
        return obj

    def getDictFromObj(self, obj):
        founder = {'gbId': obj.founder.gbId,
         'roleName': obj.founder.roleName,
         'lv': obj.founder.lv,
         'photo': obj.founder.photo,
         'borderId': obj.founder.borderId}
        item = {'nuid': 0,
         'fbNo': obj.fbNo,
         'star': obj.star,
         'founder': founder,
         'tExpire': obj.tExpire,
         'tValid': obj.tValid,
         'candidates': obj.candidates,
         'ownerGbId': obj.ownerGbId,
         'ownerName': obj.ownerName,
         'killer': obj.killer}
        return item

    def isSameType(self, obj):
        return type(obj) is ZMJStarBossVal


starBossValInstance = ZMJStarBossValInfo()
