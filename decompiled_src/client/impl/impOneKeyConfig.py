#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impOneKeyConfig.o
import gameglobal
import gamelog

class ImpOneKeyConfig(object):

    def sendAllOneKeyConfigScheme(self, schemes, currSchemeNo):
        gamelog.debug('yedawang### sendAllOneKeyConfigScheme', schemes, currSchemeNo)
        quickReplaceEquipment = gameglobal.rds.ui.quickReplaceEquipment
        if gameglobal.rds.configData.get('enableQuickReplaceEquipmentV2', False):
            quickReplaceEquipment = gameglobal.rds.ui.quickReplaceEquipmentV2
        quickReplaceEquipment.setSchemeInfo(currSchemeNo, schemes)
        quickReplaceEquipment.refreshInfo()

    def sendSingleOneKeyConfigScheme(self, schemeNo, scheme):
        gamelog.debug('yedawang### sendSingleOneKeyConfigScheme', schemeNo, scheme)
        gameglobal.rds.ui.quickReplaceEquipment.addSingleSchemeInfo(schemeNo, scheme)

    def notifySwitchOneKeyConfigSchemeDone(self, schemeNo):
        gamelog.debug('yedawang### notifySwitchOneKeyConfigSchemeDone', schemeNo)
        quickReplaceEquipment = gameglobal.rds.ui.quickReplaceEquipment
        if gameglobal.rds.configData.get('enableQuickReplaceEquipmentV2', False):
            quickReplaceEquipment = gameglobal.rds.ui.quickReplaceEquipmentV2
        if quickReplaceEquipment.currSchemeNo == schemeNo:
            quickReplaceEquipment.refreshInfo()

    def onOneKeyConfigPushMsg(self):
        gameglobal.rds.ui.quickReplaceEquipment.pushOneKeyConfigMessage()
