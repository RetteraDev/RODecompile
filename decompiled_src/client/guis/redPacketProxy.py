#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/redPacketProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import utils
import gamelog
import time
import gametypes
from helpers import taboo
from callbackHelper import Functor
from guis import uiConst
from guis import uiUtils
from guis import pinyinConvert
from guis import ui
from ui import unicode2gbk
from uiProxy import UIProxy
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
from data import red_packet_config_data as RPCD

class RedPacketProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RedPacketProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRedPacketInfo': self.onGetRedPacketInfo,
         'sendRedPacket': self.onSendRedPacket,
         'openRedPacket': self.onOpenRedPacket,
         'sendToChannel': self.onSendToChannel,
         'viewPacketInfo': self.onViewPacketInfo,
         'resendPacket': self.onResendPacket,
         'getMineRedPacket': self.onGetMineRedPacket}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SEND_RED_PACKET, self.hideSendRedPacket)
        uiAdapter.registerEscFunc(uiConst.WIDGET_RECEIVE_RED_PACKET, self.hideReceiveRedPacket)
        uiAdapter.registerEscFunc(uiConst.WIDGET_VIEW_PACKET_INFO, self.hidePacketInfo)
        self.allPacketInfo = {}
        self.allLuckyPacketMoney = {}
        self.totalRev = (0, 0)
        self.totalSend = (0, 0)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SEND_RED_PACKET:
            initData = {'tabIndex': self.sendRPTab}
            return uiUtils.dict2GfxDict(initData, True)
        if widgetId == uiConst.WIDGET_RECEIVE_RED_PACKET:
            self.recvMed = mediator
            if self.packetInfo:
                sn = self.packetInfo[0]
                pType = self.packetInfo[1]
                if self.allPacketInfo.has_key(sn):
                    ok, sn, pType, srcGbID, srcName, money = self.allPacketInfo[sn]
                    self.onGetRedPacket(ok, sn, pType, srcGbID, srcName, money)
                else:
                    return uiUtils.dict2GfxDict(self.getPacketBasicInfo(), True)
        elif widgetId == uiConst.WIDGET_VIEW_PACKET_INFO:
            self.packetInfoMed = mediator
            if self.guildRedPacketSn:
                initData = self.getGuildRedPacketInfo()
            else:
                initData = self.getPacketBasicInfo()
                if self.packetAssignInfo:
                    initData['endTime'] = self.packetAssignInfo.get('addTime', 0) + RPCD.data.get('redTtl', 0)
                    initData['assginList'] = self.packetAssignInfo.get('assignInfo', ())
                    initData['money'] = self.packetAssignInfo.get('money', 0)
                    initData['cnt'] = self.packetAssignInfo.get('cnt', 0)
                    initData['isDone'] = len(initData['assginList']) == int(initData['cnt'])
                    if self.packetAssignInfo.get('photo'):
                        initData['photo'] = self.packetAssignInfo.get('photo', '')
                    initData['msg'] = self.packetAssignInfo.get('msg', '')
                    leftCnt = initData['cnt'] - len(initData['assginList'])
                    leftMoney = initData['money'] - sum([ x[2] for x in initData['assginList'] ])
                    initData['leftMoneyTxt'] = gameStrings.RED_PACKET_LEFT_MONEY_TXT % (leftCnt, leftMoney)
                    initData['canResend'] = initData['opType'] == const.RED_PACKET_OP_TYPE_SEND and initData['channel'] not in (const.CHAT_FRIEND,)
            if initData:
                return uiUtils.dict2GfxDict(initData, True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_SEND_RED_PACKET:
            self.hideSendRedPacket()
        elif widgetId == uiConst.WIDGET_RECEIVE_RED_PACKET:
            self.hideReceiveRedPacket()
        elif widgetId == uiConst.WIDGET_VIEW_PACKET_INFO:
            self.hidePacketInfo()

    def show(self, *args):
        if not self.enableRedPacket():
            return
        if args:
            self.sendRPTab = args
        self.uiAdapter.loadWidget(uiConst.WIDGET_SEND_RED_PACKET)
        BigWorld.player().base.queryMyRedPacket()

    def showReceivePacket(self):
        if not self.enableRedPacket():
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_RECEIVE_RED_PACKET)

    def showPacketInfo(self):
        if not self.enableRedPacket():
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_VIEW_PACKET_INFO)

    def hideSendRedPacket(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SEND_RED_PACKET)
        self.sendRPTab = 0
        self.mineRedPackets = None

    def hideReceiveRedPacket(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RECEIVE_RED_PACKET)
        self.recvMed = None

    def hidePacketInfo(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VIEW_PACKET_INFO)
        self.packetInfoMed = None

    def clearWidget(self):
        self.hideSendRedPacket()
        self.hideReceiveRedPacket()

    def reset(self):
        self.sendRPTab = 0
        self.recvMed = None
        self.packetInfoMed = None
        self.redPacketState = 0
        self.packetInfo = None
        self.guildRedPacketSn = ''
        self.packetAssignInfo = None
        self.mineRedPackets = None

    def enableRedPacket(self):
        return gameglobal.rds.configData.get('enableRedPacket', False)

    def clickRedPacket(self, packetRichText):
        info = utils.parsePacketRichText(packetRichText)
        if not info:
            return
        if info[1] in (const.RED_PACKET_TYPE_GUILD, const.RED_PACKET_TYPE_ACHIEVE, const.RED_PACKET_TYPE_GUILD_MERGER_CLAP):
            if BigWorld.player().guild:
                rp = BigWorld.player().guild.redPacket.get(info[0])
                if not rp:
                    rp = BigWorld.player().guild.getRedPacket(info[0])
                    rp.sn, rp.pType, rp.msg, rp.photo, rp.srcName, rp.amount, rp.cnt, rp.tWhen = info
            self.uiAdapter.guildRedPacketRec.show(info[0])
            if self.recvMed:
                self.hideReceiveRedPacket()
            return
        if self.uiAdapter.guildRedPacketRec.widget:
            self.uiAdapter.guildRedPacketRec.hide()
        if self.packetInfo and self.packetInfo[0] == info[0] and self.recvMed:
            return
        self.packetInfo = info + (0, const.RED_PACKET_OP_TYPE_RECEIVE)
        if self.packetInfo and self.packetInfo[0]:
            self.redPacketState = uiConst.RED_PACKET_STATE_UNOPEN
            sn = self.packetInfo[0]
            pType = self.packetInfo[1]
            if self.recvMed:
                if self.allPacketInfo.has_key(sn):
                    ok, sn, pType, srcGbID, srcName, money = self.allPacketInfo[sn]
                    self.onGetRedPacket(ok, sn, pType, srcGbID, srcName, money)
                else:
                    self.recvMed.Invoke('refreshPackInfo', uiUtils.dict2GfxDict(self.getPacketBasicInfo(), True))
                    self.queryLuckyTotalMoney(pType, sn)
            else:
                self.uiAdapter.loadWidget(uiConst.WIDGET_RECEIVE_RED_PACKET)
                self.queryLuckyTotalMoney(pType, sn)
            gameglobal.rds.sound.playSound(gameglobal.SD_7)
        else:
            gamelog.error('@zhp red packet sn error', packetRichText)

    def queryLuckyTotalMoney(self, pType, sn):
        if pType == const.RED_PACKET_TYPE_SNOWBALL:
            ver = self.allLuckyPacketMoney.get(sn, {}).get('ver', 0)
            BigWorld.player().base.queryLuckyRedPacket(sn, ver)

    def getPacketBasicInfo(self):
        if self.packetInfo:
            sn, pType, msg, photo, roleName, money, cnt, pTime, channel, opType = self.packetInfo
            expiredTime = pTime + RPCD.data.get('redTtl', 0)
            failMsg = RPCD.data.get('luckyRedFailMsg', '') if pType == const.RED_PACKET_TYPE_SNOWBALL else RPCD.data.get('failMsg', '')
            data = {'sn': sn,
             'pTime': pTime,
             'opType': opType,
             'pType': pType,
             'msg': msg,
             'photo': photo,
             'money': money,
             'cnt': cnt,
             'state': self.redPacketState,
             'viewOtherMsg': RPCD.data.get('viewOtherMsg', ''),
             'roleName': roleName,
             'failMsg': failMsg,
             'openGlobalPacketMsg': RPCD.data.get('openGlobalPacketMsg', ''),
             'packetNoOneOpenMsg': RPCD.data.get('packetNoOneOpenMsg', ''),
             'isExpired': pTime > 0 and expiredTime <= utils.getNow(),
             'endTime': expiredTime,
             'expiredMsg': RPCD.data.get('expiredMsg', '%s') % time.strftime('%Y.%m.%d %H:%M', time.localtime(expiredTime)),
             'maxBlessChar': RPCD.data.get('serverRedDescLimit', 10),
             'helpKey': const.RED_PACKET_HELP_KEYS.get(pType, 0),
             'channel': channel}
            if pType == const.RED_PACKET_TYPE_SNOWBALL:
                data['totalMoney'] = self.allLuckyPacketMoney.get(sn, {}).get('totalMoney', money)
                luckyName = self.allLuckyPacketMoney.get(sn, {}).get('luckyName', '')
                data['luckyName'] = luckyName
                if data['luckyName']:
                    if luckyName == BigWorld.player().roleName:
                        data['state'] = uiConst.RED_PACKET_STATE_OPEN_SUCC
                        data['getMoney'] = data['totalMoney']
                    else:
                        data['state'] = uiConst.RED_PACKET_STATE_OPEN_FAIL
                        data['failMsg'] = RPCD.data.get('luckyRedDoneMsg', '')
            return data

    def onGetRedPacket(self, ok, sn, pType, srcGbID, srcName, money, fromServer = False):
        if ok and pType == const.RED_PACKET_TYPE_SNOWBALL or pType != const.RED_PACKET_TYPE_SNOWBALL:
            self.allPacketInfo[sn] = (ok,
             sn,
             pType,
             srcGbID,
             srcName,
             money)
        if not self.packetInfo:
            return
        if self.packetInfo[0] != sn:
            return
        if not self.recvMed:
            return
        if ok:
            self.redPacketState = uiConst.RED_PACKET_STATE_OPEN_SUCC
            gameglobal.rds.sound.playSound(3975)
        elif pType == const.RED_PACKET_TYPE_SNOWBALL:
            self.redPacketState = uiConst.RED_PACKET_STATE_UNOPEN
            self.queryLuckyTotalMoney(pType, sn)
        else:
            self.redPacketState = uiConst.RED_PACKET_STATE_OPEN_FAIL
        data = self.getPacketBasicInfo()
        data['getMoney'] = money
        data['fromServer'] = fromServer
        self.recvMed.Invoke('refreshPackInfo', uiUtils.dict2GfxDict(data, True))

    def onQueryRedPacketAssignInfo(self, sn, data):
        if not self.packetInfo:
            return
        if self.packetInfo[0] != sn:
            return
        self.guildRedPacketSn = ''
        self.packetAssignInfo = data
        self.showPacketInfo()
        self.hideReceiveRedPacket()

    def onQueryGuildRedPacket(self, sn):
        if self.uiAdapter.guildRedPacketRec.widget:
            self.uiAdapter.guildRedPacketRec.hide()
        self.guildRedPacketSn = sn
        if self.packetInfoMed:
            self.packetInfoMed.Invoke('refreshView', uiUtils.dict2GfxDict(self.getGuildRedPacketInfo(), True))
            self.packetInfoMed.Invoke('swapPanelToFront')
        else:
            self.showPacketInfo()

    def getGuildRedPacketInfo(self):
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return None
        else:
            redPacket = guild.getRedPacket(self.guildRedPacketSn)
            leftCnt = redPacket.cnt - len(redPacket.assignInfo)
            leftMoney = redPacket.amount - sum(redPacket.data)
            itemInfo = {'pType': redPacket.pType,
             'msg': uiUtils.getRedPacketSourceName(redPacket.pType, redPacket.subType),
             'isDone': redPacket.state == gametypes.GUILD_RED_PACKET_STATE_DONE,
             'isExpired': redPacket.isExpired(),
             'cnt': redPacket.cnt,
             'money': redPacket.amount,
             'leftMoneyTxt': gameStrings.RED_PACKET_LEFT_MONEY_TXT % (leftCnt, leftMoney),
             'canResend': False}
            if redPacket.pType in (const.RED_PACKET_TYPE_GUILD, const.RED_PACKET_TYPE_GUILD_MERGER_CLAP):
                icon, _ = uiUtils.getGuildFlag(p.guildFlag)
                itemInfo['photo'] = uiUtils.getGuildIconPath(icon)
                itemInfo['roleName'] = guild.name
                itemInfo['packetNoOneOpenMsg'] = (RPCD.data.get('packetNoOneOpenGuildSignInMsg', ''),)
            else:
                itemInfo['photo'] = redPacket.photo
                itemInfo['roleName'] = redPacket.srcName
                itemInfo['packetNoOneOpenMsg'] = (RPCD.data.get('packetNoOneOpenAchieveMsg', ''),)
            assginList = []
            for i, (gbId, roleName) in enumerate(redPacket.assignInfo):
                assginList.append([gbId, roleName, redPacket.data[i]])

            itemInfo['assginList'] = assginList
            return itemInfo

    def onQueryMyRedPacket(self, redPackets, totalSendCash, totalSendCoin, totalRevCash, totalRevCoin):
        self.mineRedPackets = redPackets
        self.totalRev = (totalRevCash, totalRevCoin)
        self.totalSend = (totalSendCash, totalSendCoin)

    def onQueryLuckyRedPacket(self, sn, res):
        self.allLuckyPacketMoney[sn] = res
        if self.recvMed and self.packetInfo and self.packetInfo[0] == sn:
            if res.get('luckyName', ''):
                self.recvMed.Invoke('refreshPackInfo', uiUtils.dict2GfxDict(self.getPacketBasicInfo(), True))
            else:
                self.recvMed.Invoke('refreshTotalMoney', GfxValue(res.get('totalMoney', 0)))

    def _checkCanSend(self, pType, money, cnt, msg):
        p = BigWorld.player()
        if utils.needDisableUGC() and (cnt in const.FORBID_NUMBERS or money in const.FORBID_NUMBERS):
            p.showGameMsg(GMDD.data.CHATROOM_MSG_TABOO, ())
            return (False, msg)
        if pType == const.RED_PACKET_TYPE_GLOBAL_COIN:
            if p.unbindCoin < money:
                p.showGameMsg(GMDD.data.NO_ENOUGH_UNBINDCOIN_SEND_REDPACKET, ())
                return (False, msg)
            moneyLimit = RPCD.data.get('minServerRedCoinLimit', 10000)
            if money < moneyLimit:
                p.showGameMsg(GMDD.data.RED_PACKET_FAILED_AMOUNT_MIN_LIMIT, (moneyLimit,))
                return (False, msg)
        if pType == const.RED_PACKET_TYPE_GLOBAL_CASH:
            moneyLimit = RPCD.data.get('minServerRedCashLimit', 10000)
            if money < moneyLimit:
                p.showGameMsg(GMDD.data.RED_PACKET_FAILED_AMOUNT_MIN_LIMIT, (moneyLimit,))
                return (False, msg)
            if p.cash < money:
                p.showGameMsg(GMDD.data.NO_ENOUGH_CASH_SEND_REDPACKET, ())
                return (False, msg)
        if pType == const.RED_PACKET_TYPE_SNOWBALL:
            if not p.guildNUID:
                p.showGameMsg(GMDD.data.NO_GUILD_SEND_REDPACKET, ())
                return (False, msg)
            moneyLimit = RPCD.data.get('minLuckyRedLimit', 10000)
            if money < moneyLimit:
                p.showGameMsg(GMDD.data.RED_PACKET_FAILED_AMOUNT_MIN_LIMIT, (moneyLimit,))
                return (False, msg)
        if cnt <= 0:
            p.showGameMsg(GMDD.data.REDPACKET_CNT_ZERO, ())
            return (False, msg)
        if money < cnt:
            p.showGameMsg(GMDD.data.PACKET_NUM_TOO_MUCH, ())
            return (False, msg)
        isNormal, msg = taboo.checkDisbWord(msg)
        if not isNormal:
            p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return (False, msg)
        flag, msg = self.uiAdapter.chat._tabooCheck(const.CHAT_CHANNEL_WORLD, msg)
        if not flag:
            p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return (False, msg)
        msg = msg.replace('<', '&lt;').replace('>', '&gt;')
        msg = msg.replace('_', '-')
        return (True, msg)

    def onGetRedPacketInfo(self, *args):
        p = BigWorld.player()
        pType = args[3][0].GetNumber()
        defaultMsg = RPCD.data.get('redDefaultDesc', '')
        msgMaxChars = RPCD.data.get('redDescLimit', '')
        data = {'max': 1000000,
         'msgMaxChars': msgMaxChars,
         'defaultMsg': defaultMsg,
         'defaultInputTxt': gameStrings.TEXT_REDPACKETPROXY_412,
         'packetTip': RPCD.data.get('packetTips', {}).get(pType, '')}
        if pType == const.RED_PACKET_TYPE_SNOWBALL:
            data['max'] = RPCD.data.get('maxLuckyRedLimit', 1000000)
            costItemId = RPCD.data.get('redSendConsume', 0)
            cnt = uiUtils.convertNumStr(p.inv.countItemInPages(costItemId, enableParentCheck=True), 1)
            data['costItem'] = uiUtils.getGfxItemById(costItemId, cnt)
            data['money'] = RPCD.data.get('minLuckyRedLimit', 0)
        elif pType in (const.RED_PACKET_TYPE_GLOBAL_CASH, const.RED_PACKET_TYPE_GLOBAL_COIN):
            costItemIds = (RPCD.data.get('redSendConsume', 0), RPCD.data.get('serverRedSendConsume', (0,)))
            costItems = []
            for itemId in costItemIds:
                if itemId == costItemIds[1]:
                    totalCnt = 0
                    for id in itemId:
                        totalCnt += p.inv.countItemInPages(id)
                        if p._isSoul() and gameglobal.rds.configData.get('enableCrossServerBag', False):
                            totalCnt += p.crossInv.countItemInPages(id)

                    cnt = uiUtils.convertNumStr(totalCnt, 1)
                    costItems.append(uiUtils.getGfxItemById(itemId[0], cnt))
                else:
                    cnt = uiUtils.convertNumStr(p.inv.countItemInPages(itemId, enableParentCheck=True), 1)
                    costItems.append(uiUtils.getGfxItemById(itemId, cnt))

            data['costItem'] = costItems
            data['maxPacketNum'] = RPCD.data.get('serverRedNumLimit', 100)
            if pType == const.RED_PACKET_TYPE_GLOBAL_CASH:
                data['max'] = RPCD.data.get('maxServerRedCashLimit', 1000000)
                data['money'] = RPCD.data.get('minServerRedCashLimit', 0)
            else:
                data['max'] = RPCD.data.get('maxServerRedCoinLimit', 1000000)
                data['money'] = RPCD.data.get('minServerRedCoinLimit', 0)
        elif pType in (const.RED_PACKET_TYPE_COMMON, const.RED_PACKET_TYPE_LUCKY):
            costItemId = RPCD.data.get('redSendConsume', 0)
            cnt = uiUtils.convertNumStr(p.inv.countItemInPages(costItemId, enableParentCheck=True), 1)
            data['costItem'] = uiUtils.getGfxItemById(costItemId, cnt)
            data['hasGuild'] = p.guildNUID > 0
            data['hasClan'] = p.clanNUID > 0
            data['enableClan'] = gameglobal.rds.configData.get('enableClan', False)
            friends = []
            for gbId, fVal in p.friend.items():
                if p.friend.isFriendGroup(fVal.group) and fVal.acknowledge and not fVal.deleted:
                    friends.append({'gbId': str(gbId),
                     'roleName': fVal.getFullName(),
                     'isOn': p.friend.isVisible(fVal.state),
                     'pinYinNames': (pinyinConvert.strPinyinFirst(fVal.getFullName()), pinyinConvert.strPinyin(fVal.getFullName())),
                     'intimacy': fVal.intimacy})

            friends.sort(cmp=lambda x, y: (cmp(y['intimacy'], x['intimacy']) if x['isOn'] == y['isOn'] else cmp(y['isOn'], x['isOn'])))
            data['friendList'] = friends
            data['maxPacketNum'] = RPCD.data.get('redPacketNumLimit', [100] * 5)
            data['max'] = RPCD.data.get('friendRedTimeLimit', 1000000)
            data['packetNumMsg'] = RPCD.data.get('packetNumMsg', '%s')
            data['allSelectTip'] = RPCD.data.get('allSelectTip', '')
            data['randomSelectTip'] = RPCD.data.get('randomSelectTip', '')
            data['clearSelectTip'] = RPCD.data.get('clearSelectTip', '')
            data['friendSendBonusRate'] = RPCD.data.get('friendSendBonusCash', 0.05)
            targetArray = []
            targetArray.append(uiConst.RED_PACKET_TARGET_GUILD)
            if p.clanNUID > 0 and gameglobal.rds.configData.get('enableClan', False):
                targetArray.append(uiConst.RED_PACKET_TARGET_CLAN)
            targetArray.append(uiConst.RED_PACKET_TARGET_FRIEND)
            targetArray.append(uiConst.RED_PACKET_TARGET_TEAM)
            targetArray.append(uiConst.RED_PACKET_TARGET_GROUP)
            data['targetArray'] = [ {'type': x,
             'label': gameStrings.RED_PACKET_TARGET_LABLES.get(x, '')} for x in targetArray ]
        return uiUtils.dict2GfxDict(data, True)

    @ui.callFilter(1, True)
    @ui.checkInventoryLock()
    def onSendRedPacket(self, *args):
        pType = args[3][0].GetMember('type').GetNumber()
        p = BigWorld.player()
        num = args[3][0].GetMember('num').GetNumber()
        msg = unicode2gbk(args[3][0].GetMember('msg').GetString())
        gfxCnt = args[3][0].GetMember('cnt')
        if gfxCnt:
            cnt = gfxCnt.GetNumber()
        else:
            cnt = 1
        canSend, msg = self._checkCanSend(pType, num, cnt, msg)
        if not canSend:
            return
        if pType == const.RED_PACKET_TYPE_SNOWBALL:
            p.base.addRedPacketBase(pType, num, 1, 0, msg, [], [], p.cipherOfPerson)
        elif pType in (const.RED_PACKET_TYPE_GLOBAL_CASH, const.RED_PACKET_TYPE_GLOBAL_COIN):
            if pType == const.RED_PACKET_TYPE_GLOBAL_CASH:
                p.base.addRedPacketBase(pType, num, cnt, 0, msg, [], [], p.cipherOfPerson)
            else:
                p.base.addRedPacketBase(pType, num, cnt, 0, msg, [], [], p.cipherOfPerson)
        elif pType in (const.RED_PACKET_TYPE_COMMON, const.RED_PACKET_TYPE_LUCKY):
            sendTarget = int(args[3][0].GetMember('targetType').GetNumber())
            if sendTarget == uiConst.RED_PACKET_TARGET_GUILD:
                channel = const.CHAT_CHANNEL_GUILD
            elif sendTarget == uiConst.RED_PACKET_TARGET_CLAN:
                channel = const.CHAT_CHANNEL_CLAN
            elif sendTarget == uiConst.RED_PACKET_TARGET_FRIEND:
                channel = const.CHAT_FRIEND
            elif sendTarget == uiConst.RED_PACKET_TARGET_TEAM:
                channel = const.CHAT_CHANNEL_TEAM
            elif sendTarget == uiConst.RED_PACKET_TARGET_GROUP:
                channel = const.CHAT_CHANNEL_GROUP
            else:
                channel = const.CHAT_CHANNEL_WORLD_EX
            tgtGbIds = []
            tgtNames = []
            gfxGbIds = args[3][0].GetMember('friendGbIds')
            size = gfxGbIds.GetArraySize()
            for i in range(size):
                tgtGbIds.append(int(unicode2gbk(gfxGbIds.GetElement(i).GetString())))

            gfxNames = args[3][0].GetMember('friendNames')
            size = gfxNames.GetArraySize()
            for i in range(size):
                tgtNames.append(unicode2gbk(gfxNames.GetElement(i).GetString()))

            if len(tgtGbIds) != cnt and sendTarget == uiConst.RED_PACKET_TARGET_FRIEND:
                p.showGameMsg(GMDD.data.REDPACKET_FRIENDS_NUM_ERROR, ())
                return
            p.base.addRedPacketBase(pType, num, cnt, channel, msg, tgtGbIds, tgtNames, p.cipherOfPerson)

    def onOpenRedPacket(self, *args):
        if self.packetInfo:
            sn = self.packetInfo[0]
            pType = self.packetInfo[1]
            money = self.packetInfo[5]
            msg = unicode2gbk(args[3][0].GetString())
            p = BigWorld.player()
            if pType in (const.RED_PACKET_TYPE_GLOBAL_CASH, const.RED_PACKET_TYPE_GLOBAL_COIN):
                if len(msg):
                    isNormal, msg = taboo.checkDisbWord(msg)
                    if not isNormal:
                        p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
                        return
                    flag, msg = self.uiAdapter.chat._tabooCheck(const.CHAT_CHANNEL_WORLD, msg)
                    if not flag:
                        p.showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
                        return
            if pType == const.RED_PACKET_TYPE_SNOWBALL:
                cost = int(money * RPCD.data.get('luckyRedOpenConsumeRatio', 0.1))
                msg = RPCD.data.get('openSnowBallMsg', '') % cost
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(p.base.getRedPacket, sn, pType, msg, money))
            elif pType in (const.RED_PACKET_TYPE_GUILD, const.RED_PACKET_TYPE_ACHIEVE):
                pass
            else:
                p.base.getRedPacket(sn, pType, msg, money)

    def onSendToChannel(self, *args):
        pass

    def onResendPacket(self, *args):
        if self.packetInfo:
            sn, pType, msg, photo, roleName, money, cnt, pTime, channel, _ = self.packetInfo
            p = BigWorld.player()
            if pType == const.RED_PACKET_TYPE_SNOWBALL:
                p.base.resendRedPacket(sn)
                return
            chatChannel = utils.getRedPacketChatChannel(pType, channel)
            msg = utils.getRedPacketRichText(sn, pType, msg, roleName, money, cnt, photo, pTime)
            if chatChannel == const.CHAT_CHANNEL_GUILD:
                if p.guildNUID:
                    p.cell.chatToGuild(msg, True)
                else:
                    p.showGameMsg(GMDD.data.CHAT_NOT_IN_GUILD, ())
            elif chatChannel == const.CHAT_CHANNEL_WORLD_EX:
                p.cell.chatToWorldEx(msg, p.operation.get('curLabaId', 0), const.NORMAL_CHAT_MSG, '')
            elif chatChannel == const.CHAT_CHANNEL_CLAN:
                if p.clanNUID:
                    p.cell.chatToClan(msg)
                else:
                    p.showGameMsg(GMDD.data.CLAN_NOT_JOINED_CLAN, ())
            elif chatChannel == const.CHAT_CHANNEL_GROUP:
                if p.isInGroup():
                    p.cell.chatToGroup(msg)
                else:
                    p.showGameMsg(GMDD.data.CHAT_NOT_IN_GROUP, ())
            elif chatChannel == const.CHAT_CHANNEL_TEAM:
                if p.isInTeam():
                    p.cell.chatToTeamGroup(msg)
                else:
                    p.showGameMsg(GMDD.data.CHAT_NOT_IN_TEAM, ())

    def onGetMineRedPacket(self, *args):
        opType = args[3][0].GetNumber()
        packetList = []
        p = BigWorld.player()
        if self.mineRedPackets:
            for key, val in self.mineRedPackets.items():
                sn = key[0]
                if val[0] == const.RED_PACKET_OP_TYPE_RECEIVE:
                    tmpOpType, pType, money, channel, srcName, pTime, photo = val
                    msg = ''
                    cnt = 0
                else:
                    tmpOpType, pType, money, cnt, channel, msg, _, pTime = val
                    packetName = RPCD.data.get('packetName', {})
                    if packetName.has_key(pType):
                        srcName = packetName.get(pType, '')
                    else:
                        srcName = packetName.get((pType, channel), '%s_%s' % (pType, channel))
                    photo = p._getFriendPhoto(p)
                timeStr = time.strftime('%m-%d', time.localtime(pTime))
                if val[0] == const.RED_PACKET_OP_TYPE_SEND:
                    if self._isRedPacketExpired(pTime):
                        timeStr = uiUtils.toHtml(gameStrings.TEXT_REDPACKETPROXY_623, '#D10000')
                if opType == val[0]:
                    packetList.append({'sn': sn,
                     'opType': tmpOpType,
                     'pType': pType,
                     'money': money,
                     'roleName': srcName,
                     'time': timeStr,
                     'photo': photo,
                     'msg': msg,
                     'money': money,
                     'cnt': cnt,
                     'channel': channel,
                     'pTime': pTime})

        if opType == const.RED_PACKET_OP_TYPE_RECEIVE:
            sumPacketMsg = gameStrings.TEXT_REDPACKETPROXY_638 % len(packetList)
            cash, coin = self.totalRev
        else:
            sumPacketMsg = gameStrings.TEXT_REDPACKETPROXY_641 % len(packetList)
            cash, coin = self.totalSend
        packetList.sort(cmp=lambda x, y: cmp(y['pTime'], x['pTime']))
        data = {'cash': cash,
         'photo': p._getFriendPhoto(p),
         'roleName': p.roleName,
         'coin': coin,
         'sumPacketMsg': sumPacketMsg,
         'packetList': packetList}
        return uiUtils.dict2GfxDict(data, True)

    def onViewPacketInfo(self, *args):
        sn = unicode2gbk(args[3][0].GetMember('sn').GetString())
        pType = int(args[3][0].GetMember('pType').GetNumber())
        msg = unicode2gbk(args[3][0].GetMember('msg').GetString())
        photo = unicode2gbk(args[3][0].GetMember('photo').GetString())
        roleName = unicode2gbk(args[3][0].GetMember('roleName').GetString())
        money = int(args[3][0].GetMember('money').GetNumber())
        cnt = int(args[3][0].GetMember('cnt').GetNumber())
        channel = int(args[3][0].GetMember('channel').GetNumber())
        opType = int(args[3][0].GetMember('opType').GetNumber())
        pTime = int(args[3][0].GetMember('pTime').GetNumber())
        self.packetInfo = (sn,
         pType,
         msg,
         photo,
         roleName,
         money,
         cnt,
         pTime,
         channel,
         opType)
        if self.packetInfo:
            sn = self.packetInfo[0]
            self.hidePacketInfo()
            BigWorld.player().base.queryRedPacketAssignInfo(sn, -1)

    def _isRedPacketExpired(self, pTime):
        return pTime > 0 and pTime + +RPCD.data.get('redTtl', 0) <= utils.getNow()
