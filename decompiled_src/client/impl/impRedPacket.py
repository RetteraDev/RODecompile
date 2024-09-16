#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impRedPacket.o
import gameglobal

class ImpRedPacket(object):

    def addRedPacketDone(self, ok, sn, pType, money, cnt, channel, msg, extra):
        gameglobal.rds.ui.redPacket.hideSendRedPacket()

    def onGetRedPacket(self, ok, sn, pType, srcGbID, srcName, money):
        gameglobal.rds.ui.redPacket.onGetRedPacket(ok, sn, pType, srcGbID, srcName, money, True)

    def onQueryRedPacketAssignInfo(self, sn, data):
        gameglobal.rds.ui.redPacket.onQueryRedPacketAssignInfo(sn, data)

    def onQueryMyRedPacket(self, redPackets, totalSendCash, totalSendCoin, totalRevCash, totalRevCoin):
        gameglobal.rds.ui.redPacket.onQueryMyRedPacket(redPackets, totalSendCash, totalSendCoin, totalRevCash, totalRevCoin)

    def onQueryLuckyRedPacket(self, sn, res):
        gameglobal.rds.ui.redPacket.onQueryLuckyRedPacket(sn, res)
