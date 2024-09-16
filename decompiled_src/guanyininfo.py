#Embedded file name: /WORKSPACE/data/entities/common/guanyininfo.o
from userSoleType import UserSoleType
from guanYin import GuanYinSlotVal, GuanYinBookVal, GuanYin
import gamelog

class GuanYinInfo(UserSoleType):

    def createObjFromDict(self, dictData):
        guanYin = GuanYin()
        for child1 in dictData['slots']:
            guanYinSlotVal = GuanYinSlotVal(child1['slotId'], child1['valid'])
            guanYinSlotVal.guanYinInfo = child1['guanYinInfo']
            guanYinSlotVal.guanYinStat = child1['guanYinStat']
            guanYin[guanYinSlotVal.slotId] = guanYinSlotVal

        for child2 in dictData['books']:
            guanYinBookVal = GuanYinBookVal(child2['bookId'], child2['valid'])
            guanYinBookVal.guanYinSuperBookId = child2['guanYinSuperBookId']
            guanYinBookVal.guanYinSuperPskillExpire = child2['guanYinSuperPskillExpire']
            guanYin.addBook(guanYinBookVal)

        return guanYin

    def getDictFromObj(self, obj):
        dictData = {}
        dictData['slots'] = []
        for slotVal in obj.itervalues():
            dictData['slots'].append({'slotId': slotVal.slotId,
             'valid': slotVal.valid,
             'guanYinStat': slotVal.guanYinStat,
             'guanYinInfo': slotVal.guanYinInfo,
             'state': slotVal.state})

        dictData['books'] = []
        for bookVal in obj.books.itervalues():
            dictData['books'].append({'bookId': bookVal.bookId,
             'valid': bookVal.valid,
             'guanYinSuperBookId': bookVal.guanYinSuperBookId,
             'guanYinSuperPskillExpire': bookVal.guanYinSuperPskillExpire,
             'state': bookVal.state})

        dictData['lastApplyNum'] = obj.lastApplyNum
        dictData['combatScore'] = obj.combatScore
        return dictData

    def isSameType(self, obj):
        return type(obj) is GuanYin


instance = GuanYinInfo()
