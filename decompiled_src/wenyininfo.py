#Embedded file name: /WORKSPACE/data/entities/common/wenyininfo.o
from userSoleType import UserSoleType
from wenYin import WenYinVal, WenYin
from item import Item, GemSlot

class WenYinInfo(UserSoleType):

    def createObjFromDict(self, dictData):
        wenYin = WenYin()
        for child in dictData['wenYin']:
            wenYinVal = WenYinVal()
            for idx, yangData in enumerate(child['yangSlots']):
                wenYinVal.yangSlots[idx] = GemSlot.slotWithSavedData(yangData)

            for idx, yinData in enumerate(child['yinSlots']):
                wenYinVal.yinSlots[idx] = GemSlot.slotWithSavedData(yinData)

            wenYin[child['part']] = wenYinVal

        return wenYin

    def getDictFromObj(self, obj):
        dictData = dict()
        dictData['wenYin'] = []
        for part, wenYinVal in obj.iteritems():
            child = dict()
            child['part'] = part
            child['yangSlots'] = []
            for yangGem in wenYinVal.yangSlots:
                child['yangSlots'].append(yangGem.getGemData(Item.GEM_TYPE_YANG))

            child['yinSlots'] = []
            for yinGem in wenYinVal.yinSlots:
                child['yinSlots'].append(yinGem.getGemData(Item.GEM_TYPE_YIN))

            dictData['wenYin'].append(child)

        return dictData

    def isSameType(self, obj):
        return type(obj) is WenYin


instance = WenYinInfo()
