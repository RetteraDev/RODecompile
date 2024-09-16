#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impMarriage.o
import zlib
import cPickle
import BigWorld
import formula
import gameglobal
import gamelog
import gametypes
import const
import utils
from guis import ui
from guis import uiConst
from guis import uiUtils
from helpers import navigator
from helpers import editorHelper
from gamestrings import gameStrings
from data import message_desc_data as MSGDD
from data import marriage_package_data as MPD
from data import marriage_firework_data as MFD
from data import marriage_config_data as MCD
from cdata import marriage_subscribe_date_data as MSDD
from cdata import game_msg_def_data as GMDD
from data import fireworks_effect_data as FWED
from data import region_server_config_data as RSCD
from cdata import region_server_name_data as RSND
from cdata import region_server_name_to_hostId as RSNTH
from callbackHelper import Functor

class ImpMarriage(object):

    def onChooseMarriageType(self, npcId, friendId):
        gamelog.debug('@zq marriage#onChooseMarriageType:', npcId, friendId)
        self.cell.doChooseMarriageType(npcId, friendId)

    def onMarriageSkillCdUpdate(self, cdTime):
        gamelog.debug('@zq marriage#onMarriageSkillCdUpdate:', cdTime)
        self.marriageSkillTime = cdTime
        gameglobal.rds.ui.actionbar.updateSlots()
        gameglobal.rds.ui.skill.refreshIntimacyPanel()

    def onDoChooseMarriageType(self):
        """
        \xe8\xbf\x99\xe9\x87\x8c\xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe6\xa0\xa1\xe9\xaa\x8c\xe5\xae\x8c\xe6\xaf\x95\xef\xbc\x8c\xe5\x8f\xaf\xe4\xbb\xa5\xe5\xbc\xb9\xe5\x87\xba\xe5\xa9\x9a\xe7\xa4\xbc\xe5\xa5\x97\xe9\xa4\x90\xe7\x9a\x84\xe9\x80\x89\xe6\x8b\xa9\xe7\x95\x8c\xe9\x9d\xa2
        Returns:
        
        """
        gamelog.debug('@zq marriage#onDoChooseMarriageType')
        self.cell.queryMarriageSubcribeDateMap(0, gametypes.MARRIAGE_QUERY_DATE_PRECHECK)

    def onExtendGuestSuccess(self, curMarriageGuestCnt):
        gameglobal.rds.ui.marrySettingBg.onSetExtendGuest(curMarriageGuestCnt)
        gameglobal.rds.ui.marryInviteFriend.refreshExtendGuest()

    def notifyGreatMarriageFireWork(self, greatFireWork):
        gameglobal.rds.ui.marryFireWork.hide()
        gameglobal.rds.ui.marryFireWork.show()

    def syncMarriageHappyVal(self, happyVal):
        """
        \xe5\x90\x8c\xe6\xad\xa5\xe5\xb9\xb8\xe7\xa6\x8f\xe5\x80\xbc
        Args:
            happyVal:
        
        Returns:
        
        """
        gamelog.debug('@zq marriage#syncMarriageHappyVal ', happyVal)
        marriageInfo = {'happyVal': happyVal}
        self.marriageBeInvitedInfo.update(marriageInfo)
        gameglobal.rds.ui.marryHallFunc.refreshInfo()

    def notifyMarriageGreatPledge(self):
        """
        \xe5\xbc\x80\xe5\xa7\x8b\xe7\xac\xac\xe4\xb8\x80\xe6\xae\xb5\xe7\x9b\x9b\xe4\xb8\x96\xe8\x84\x9a\xe6\x9c\xac
        Returns:
        """
        BigWorld.callback(1, Functor(self.marriageGreatScenarioPlay))

    def notifyChinesePledge(self):
        """
        \xe5\xbc\x80\xe5\xa7\x8b\xe6\x92\xad\xe6\x94\xbe\xe4\xb8\xad\xe5\xbc\x8f\xe5\xa9\x9a\xe7\xa4\xbc\xe7\x9a\x84\xe5\xae\xa3\xe8\xaa\x93\xe8\x84\x9a\xe6\x9c\xac
        Returns:
        
        """
        gamelog.debug('@zq marriage#notifyChinesePledge ')
        BigWorld.callback(1, Functor(self.marriageScenarioPlay))
        gameglobal.rds.sound.playMusic(const.MARRIAGE_CHINESE_PLEDGE_MUSIC_ID)

    def notifyAmericanPledge(self):
        """
        \xe5\xbc\x80\xe5\xa7\x8b\xe6\x92\xad\xe6\x94\xbe\xe8\xa5\xbf\xe5\xbc\x8f\xe5\xa9\x9a\xe7\xa4\xbc\xe7\x9a\x84\xe5\xae\xa3\xe8\xaa\x93\xe8\x84\x9a\xe6\x9c\xac
        Returns:
        
        """
        gamelog.debug('@zq marriage#notifyAmericanPledge ')
        BigWorld.callback(1, Functor(self.marriageAmericanScenarioPlay))

    def onMarriagePledgeDone(self):
        """
        \xe5\xae\xa3\xe8\xaa\x93\xe6\x88\x90\xe5\x8a\x9f
        Returns:
        
        """
        gamelog.debug('@zq marriage#onMarriagePledgeDone ')
        BigWorld.callback(3, Functor(self.addMarriagePrompt, uiConst.MESSAGE_TYPE_MARRIAGE_PARADE))

    def notifyClientMarriageRedPacket(self):
        """
        
        Returns: \xe6\x9c\x89\xe7\xa6\xbb\xe7\xba\xbf\xe7\xba\xa2\xe5\x8c\x85\xef\xbc\x8c\xe8\xb0\x83\xe7\x94\xa8cell\xe7\x9a\x84queryMarriageRedPacketInfo\xe6\x9d\xa5\xe8\x8e\xb7\xe5\x8f\x96\xe5\x85\xa8\xe9\x83\xa8\xe6\x95\xb0\xe6\x8d\xae
        
        """
        gamelog.debug('@zq marriage#notifyClientMarriageRedPacket ')
        self.cell.queryMarriageRedPacketInfo()

    def marriageHallShareCDTime(self, lastCDTime):
        """
        \xe6\x92\x92\xe5\x96\x9c\xe7\xb3\x96\xe6\x97\xb6\xe9\x97\xb4\xe5\x90\x8c\xe6\xad\xa5
        Args:
            lastCDTime: \xe4\xb8\x8a\xe6\xac\xa1\xe6\x92\x92\xe5\x96\x9c\xe7\xb3\x96\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4
        
        Returns:
        
        """
        gamelog.debug('@zq marriage#marriageHallShareCDTime ', lastCDTime)
        self.marriageBeInvitedInfo.setdefault('lastShareCandyTime', 0)
        self.marriageBeInvitedInfo['lastShareCandyTime'] = lastCDTime

    def onGetMarriageRedPacketFail(self, sn, failedType):
        gamelog.debug('@zq marriage#onGetMarriageRedPacketFail ', sn, failedType)
        mInfo = []
        for i, rList in enumerate(self.marriageRedPacketInfo):
            rList = list(rList)
            serinalNum, money, msg, srcName, receiveType = rList
            if serinalNum == sn:
                if failedType == const.MARRIAGE_RED_PACKET_FAILED_GOT:
                    receiveType = uiConst.RECEIVE_TYPE_GOT
                elif failedType == const.MARRIAGE_RED_PACKET_FAILED_EXPIRED:
                    receiveType = uiConst.RECEIVE_TYPE_EXPIRED
                rList = [serinalNum,
                 money,
                 msg,
                 srcName,
                 receiveType]
            mInfo.append(rList)

        self.marriageRedPacketInfo = mInfo
        gameglobal.rds.ui.marryReceiveRedPacket.refreshInfo()
        self.refreshMarriageRedPacketPushMessage()

    def onGetMarriageRedPacketSucc(self, sn):
        gamelog.debug('@zq marriage#onGetMarriageRedPacketSucc ', sn)
        mInfo = []
        for i, rList in enumerate(self.marriageRedPacketInfo):
            rList = list(rList)
            serinalNum, money, msg, srcName, receiveType = rList
            if serinalNum == sn:
                receiveType = uiConst.RECEIVE_TYPE_GOT
                rList = [serinalNum,
                 money,
                 msg,
                 srcName,
                 receiveType]
                gameglobal.rds.ui.marryRedPacketResult.show(srcName, msg, money)
            mInfo.append(rList)

        self.marriageRedPacketInfo = mInfo
        gameglobal.rds.ui.marryReceiveRedPacket.refreshInfo()
        self.refreshMarriageRedPacketPushMessage()

    def receiveMarriageRedPacket(self, srcGbId, srcRole, sn, msg, money, photo):
        """
        
        Args:
            srcGbId:  \xe7\xa4\xbc\xe5\xa0\x82\xe7\xba\xa2\xe5\x8c\x85\xe5\x8f\x91\xe9\x80\x81\xe4\xba\xbagbId
            srcRole: \xe7\xa4\xbc\xe5\xa0\x82\xe7\xba\xa2\xe5\x8c\x85\xe5\x8f\x91\xe9\x80\x81\xe4\xba\xba\xe5\x90\x8d\xe5\xad\x97
            sn: \xe7\xa4\xbc\xe5\xa0\x82\xe7\xba\xa2\xe5\x8c\x85\xe5\x8f\x91\xe9\x80\x81\xe5\x94\xaf\xe4\xb8\x80\xe7\xa0\x81
            msg: \xe7\xa4\xbc\xe5\xa0\x82\xe7\xba\xa2\xe5\x8c\x85\xe7\xa5\x9d\xe7\xa6\x8f\xe8\xaf\xad
            money: \xe7\xa4\xbc\xe5\xa0\x82\xe7\xba\xa2\xe5\x8c\x85\xe9\x87\x91\xe9\xa2\x9d
            photo: \xe7\xa4\xbc\xe5\xa0\x82\xe7\xba\xa2\xe5\x8c\x85\xe5\xa4\xb4\xe5\x83\x8f
        
        Returns:
        
        """
        gamelog.debug('@zq marriage#receiveMarriageRedPacket ', srcGbId, srcRole, sn, msg, money, photo)
        self.marriageRedPacketInfo.append((sn,
         money,
         msg,
         srcRole,
         uiConst.RECEIVE_TYPE_ACCESS))
        gameglobal.rds.ui.marryReceiveRedPacket.refreshInfo()
        self.refreshMarriageRedPacketPushMessage()

    def notifyReleaseMarriageFire(self, srcGbId, srcRoleName, fireWorkType, lastCDTime):
        """
        
        Args:
            srcGbId: \xe9\x87\x8a\xe6\x94\xbe\xe7\x83\x9f\xe8\x8a\xb1\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6gbId
            srcRoleName: \xe9\x87\x8a\xe6\x94\xbe\xe7\x83\x9f\xe8\x8a\xb1\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6\xe5\x90\x8d\xe5\xad\x97
            fireWorkType: \xe7\x83\x9f\xe8\x8a\xb1\xe7\xb1\xbb\xe5\x9e\x8b, marriage_firework_data.py
            lastCDTime: \xe4\xb8\x8a\xe6\xac\xa1\xe7\x83\x9f\xe8\x8a\xb1\xe9\x87\x8a\xe6\x94\xbe\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4
        Returns:
        
        """
        gamelog.debug('@lhb marriage#notifyReleaseMarriageFire ', srcGbId, srcRoleName, fireWorkType, lastCDTime)
        fireWorkCDDict = {fireWorkType: lastCDTime}
        self.marriageBeInvitedInfo.setdefault('fireWorkCDDict', {})
        self.marriageBeInvitedInfo['fireWorkCDDict'].update(fireWorkCDDict)
        fireWorkIds = MFD.data.get(fireWorkType, {}).get('fireWorkIds', 0)
        if fireWorkIds:
            for fireWorkId in fireWorkIds:
                if fireWorkId:
                    previewDuration = FWED.data.get(fireWorkId, {}).get('duration', 0)
                    self.doFireworks(fireWorkId, previewDuration)

    def notifyDoHusbandPledge(self):
        """
        \xe4\xb8\x88\xe5\xa4\xab\xe5\xae\xa3\xe8\xaa\x93
        Returns:
        
        """
        gamelog.debug('@zq marriage#notifyDoHusbandPledge ')
        gameglobal.rds.ui.marryIdo.show(const.SEX_MALE)

    def notifyDoWifePledge(self):
        """
        \xe5\xa6\xbb\xe5\xad\x90\xe5\xae\xa3\xe8\xaa\x93
        Returns:
        
        """
        gamelog.debug('@zq marriage#notifyDoWifePledge ')
        gameglobal.rds.ui.marryIdo.show(const.SEX_FEMALE)

    def onApplyMarriageStart(self):
        gamelog.debug('@zq marriage#onApplyMarriageStart ')
        self.motionPin()

        def _unlockPlayer():
            self.motionUnpin()

        delayEnterHallInterval = MCD.data.get('delayEnterHallInterval', 0)
        BigWorld.callback(delayEnterHallInterval, Functor(_unlockPlayer))

    @ui.checkInventoryLock()
    def onSubscribeHideMarriageDoneConfirm(self, friendId):
        """
        \xe9\x98\x9f\xe9\x95\xbf\xe4\xba\x8c\xe6\xac\xa1\xe7\xa1\xae\xe8\xae\xa4\xe9\x9a\x90\xe5\xa9\x9a
        Args:
        Returns:
        
        """
        gamelog.debug('@zq marriage#onSubscribeHideMarriageDoneConfirm', self.roleName)
        gameglobal.rds.ui.marryPlanSelect.hide()
        msg = MSGDD.data.get('hideMarriageConfirmMessage', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.doSubscribeHideMarriageDone, friendId, self.cipherOfPerson), noCallback=Functor(self.cancelSubscribeMarriageHide, friendId), yesBtnText=gameStrings.COMMON_CONFIRM)

    def cancelSubscribeMarriageHide(self, friendId):
        gamelog.debug('@hjx marriage#cancelSubscribeMarriageHide', friendId)
        self.cell.onCancelSubscribeMarriageHide(friendId)

    def onQueryMarriageWifeSchool(self, school):
        gamelog.debug('@zq marriage#onQueryMarriageWifeSchool ', school)
        schoolLeaderPos = MCD.data.get('schoolLeaderPos', {})
        seekId = schoolLeaderPos.get(school, ())
        if seekId:
            uiUtils.findPosWithAlert(seekId)

    @ui.checkInventoryLock()
    def onSubscribeMarriagePackageDoneConfirm(self, friendId, mType, subType, packageList, month, day, timeIndex):
        """
        \xe9\x98\x9f\xe9\x95\xbf\xe4\xba\x8c\xe6\xac\xa1\xe7\xa1\xae\xe8\xae\xa4\xe8\x87\xaa\xe7\x94\xb1\xe5\xa5\x97\xe9\xa4\x90
        Args:
            friendId:
            mType:
            subType:
            packageList:
            month:
            day:
            timeIndex:
        
        Returns:
        
        """
        gamelog.debug('@zq marriage#onSubscribeMarriagePackageDoneConfirm:', friendId, mType, subType, packageList, month, day, timeIndex)
        msg = MSGDD.data.get('marriageConfirmMessage', '')
        packageName = MPD.data[mType, subType]['name']
        beginTimeTuple = MSDD.data[timeIndex]['beginTimeTuple']
        endTimeTuple = MSDD.data[timeIndex]['endTimeTuple']
        marriageStartTimeDesc = gameStrings.MARRY_DAY_DURATION_FORMAT % (month,
         day,
         beginTimeTuple[0],
         beginTimeTuple[1],
         endTimeTuple[0],
         endTimeTuple[1])
        modifyTimeDesc = gameStrings.MARRY_DAY_CHANGE_DEADLINE % (month,
         day,
         beginTimeTuple[0] - 1,
         beginTimeTuple[1])
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg % (packageName, marriageStartTimeDesc, modifyTimeDesc), yesCallback=Functor(self.cell.doSubscribeMarriagePackageDone, friendId, mType, subType, packageList, month, day, timeIndex, self.cipherOfPerson), noCallback=Functor(self.cancelSubscribeMarriagePackage, friendId), yesBtnText=gameStrings.COMMON_CONFIRM, textAlign='left')
        gameglobal.rds.ui.marryPlanOrder.hide()

    def cancelSubscribeMarriagePackage(self, friendId):
        gamelog.debug('@hjx marriage#cancelSubscribeMarriagePackage', friendId)
        self.cell.onCancelSubscribeMarriagePackage(friendId)

    def syncMarriageSubcribeDateMap(self, subscribeDateMap, subscribeDateVersion, qType):
        """
        \xe8\x8e\xb7\xe5\x8f\x96\xe5\xa9\x9a\xe7\xa4\xbc\xe9\xa2\x84\xe7\xba\xa6\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xe6\x83\x85\xe5\x86\xb5\xe7\x9a\x84\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe5\x9b\x9e\xe8\xb0\x83
        Args:
            subscribeDateMap:
            subscribeDateVersion:
        
        Returns:
        
        """
        gamelog.debug('@zq marriage#syncMarriageSubcribeDateMap:', subscribeDateMap, subscribeDateVersion)
        if qType == gametypes.MARRIAGE_QUERY_DATE_ORDER:
            gameglobal.rds.ui.marryPlanOrder.syncMarriageSubcribeDateMap(subscribeDateMap, subscribeDateVersion)
        elif qType == gametypes.MARRIAGE_QUERY_DATE_PRECHECK:
            result = gameglobal.rds.ui.marryTimeOrder.hasEmptyTime(subscribeDateMap)
            if result:
                gameglobal.rds.ui.marryPlanSelect.show()
            else:
                self.showGameMsg(GMDD.data.MARRIAGE_SUBSCRIBE_DATE_FULL, ())

    def onSetMarriagePackageInfoApply(self):
        """
        \xe6\x89\x93\xe5\xbc\x80\xe4\xbf\xae\xe6\x94\xb9\xe5\xa9\x9a\xe7\xa4\xbc\xe5\xa5\x97\xe9\xa4\x90\xe4\xbf\xa1\xe6\x81\xaf\xe7\x9a\x84\xe7\x95\x8c\xe9\x9d\xa2
        Returns:
        
        """
        gamelog.debug('@zq marriage#onSetMarriagePackageInfoApply')
        gameglobal.rds.ui.marrySettingBg.openMarrySetting()

    def onCheckUpdateMarriagePackageCost(self, srcSubType, tgtSubType, deltaDict):
        """
        
        Args:
            deltaDict: {itemId: deltaCount}
        
        Returns:
        
        """
        gamelog.debug('@zq marriage#onCheckUpdateMarriagePackageCost:', srcSubType, tgtSubType, deltaDict)
        gameglobal.rds.ui.marryPlanSetting.onUpgradeFunc(srcSubType, tgtSubType, deltaDict)

    def onMarriageInfoQuery(self, info):
        """
        \xe9\x82\x80\xe8\xaf\xb7\xe5\x87\xbd\xe7\x9a\x84\xe4\xbf\xa1\xe6\x81\xaf
        Args:
        info:
        {
            'member':{
                gbId:{
                'sex':self.sex,
                'school':self.school,
                'level': self.level,
                'roleName': self.roleName,
                'roleType': self.roleType,
                'photo': self.photo,
                }
            },
        
            'package':
                {
                'month':self.month,
                'day': self.day,
                'timeIndex': self.timeIndex,
                'mType': self.mType,
                'subType': self.subType,
                'packageList':self.packageList,
                }
        
            'bestmanMember':self.bestmanMember,
            'bridesmaidMember': self.bridesmaidMember,
            'guestMember': self.guestMember,
            'allowGuestCnt': self.guestAllowCnt,
            'mainHostId': self.srcHostId,
        }
        
        Returns:
        
        """
        info = cPickle.loads(zlib.decompress(info))
        gamelog.debug('@zq marriage#onMarriageInfoQuery:', info)
        if self.gbId in info.get('member', {}):
            gameglobal.rds.ui.marrySettingBg.openByMarriageInfo(marriageInfo=info)
        else:
            gameglobal.rds.ui.marryInvitationCard.show(info)

    def syncClientMarriageInfo(self, marriageInfo):
        """
        \xe5\x90\x8c\xe6\xad\xa5\xe7\xbb\x99\xe8\xbf\x9b\xe7\xa4\xbc\xe5\xa0\x82\xe7\x9a\x84\xe7\x8e\xa9\xe5\xae\xb6\xe7\x9a\x84\xe4\xbf\xa1\xe6\x81\xaf:
        marriageCoupleInfo: {'wifeGbId': gbId, 'hunsbandGbId': gbId,
                             'wifeName': roleName, 'husbandName': roleName,
                             'happyVal': happyVal, 'marriagePackageList': marriagePackageList,
                             'mType': mType, 'subType': subType,
                             'fireWorkCDDict': fireWorkCDDict,
                             'lastShareCandyTime':lastShareCandyTime,
                             'bestMan': self.bestmanDict, 'bridesmaid': self.bridesmaidDict}
        Args:
            marriageInfo:
        
        Returns:
        
        """
        marriageInfo = cPickle.loads(zlib.decompress(marriageInfo))
        gamelog.debug('@zq marriage#syncMarriageHallCoupleInfo:', marriageInfo)
        self.marriageBeInvitedInfo.update(marriageInfo)
        self.setDynamicSkybox(formula.getMapId(self.spaceNo))

    def onMarriageRedPacketInfo(self, redPacketInfo):
        """
        \xe7\xa4\xbc\xe9\x87\x91\xe4\xbf\xa1\xe6\x81\xaf [gbId:{'roleName':'xxx', 'money': 150}, ]
        Args:
            redPacketInfo:
        
        Returns:
        
        """
        redPacketDict = cPickle.loads(zlib.decompress(redPacketInfo))
        gamelog.debug('@zq marriage#onMarriageRedPacketInfo:', redPacketDict)
        gameglobal.rds.ui.marryPacketList.show(redPacketDict)

    def onSetMarriagePackage(self, mType, subType, packageList, curMarriageGuestCnt):
        """
        
        Args:
            mType:
            subType:
            packageList:
        
        Returns:
        
        """
        gamelog.debug('@zq marriage#onSetMarriagePackage:', mType, subType, packageList, curMarriageGuestCnt)
        gameglobal.rds.ui.marrySettingBg.onSetMarriagePackage(mType, subType, packageList, curMarriageGuestCnt)

    def onSetMarriageGuests(self, guestDict):
        """
        \xe8\xae\xbe\xe7\xbd\xae\xe5\xae\xbe\xe5\xae\xa2\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        Args:
            guestDict:
        
        Returns:
        
        """
        guestDict = cPickle.loads(zlib.decompress(guestDict))
        gamelog.debug('@zq marriage#onSetMarriageGuests:', guestDict)
        gameglobal.rds.ui.marrySettingBg.onSetMarriageGuests(guestDict)
        gameglobal.rds.ui.marryInviteFriend.weakRefresh()

    def onSetMarriageMaids(self, bridesmaidDict, bestmanDict):
        """
        \xe8\xae\xbe\xe7\xbd\xae\xe4\xbc\xb4\xe9\x83\x8e\xe3\x80\x81\xe4\xbc\xb4\xe5\xa8\x98\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        Args:
            bridesmaidDict:
            bestmanDict:
        
        Returns:
        
        """
        gamelog.debug('@zq marriage#onSetMarriageMaids:', bridesmaidDict, bestmanDict)
        gameglobal.rds.ui.marrySettingBg.onSetMarriageMaids(bridesmaidDict, bestmanDict)

    def onNotifyPrepareMarriage(self, tgtRoleName):
        """
        \xe5\xa9\x9a\xe7\xa4\xbc\xe5\xbc\x80\xe5\x90\xaf\xe5\x89\x8d1\xe5\xb0\x8f\xe6\x97\xb6\xef\xbc\x8c\xe7\xbb\x99\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe7\x9a\x84\xe9\x80\x9a\xe7\x9f\xa5
        Args:
            tgtRoleName:
        
        Returns:
        
        """
        gamelog.debug('@zq onNotifyPrepareMarriage', tgtRoleName)
        self.showGameMsg(GMDD.data.MARRIAGE_PREPARE_NOTIFY, (tgtRoleName,))
        gameglobal.rds.ui.marryProcess.show()

    def onMarriageQueryUnitInfo(self, qType, info):
        """
        
        Args:
            qType:
            info:
                {
                5678791530148528135L: {'roleName': '175yecha', 'photo': ''},
                5678790037513175043L: {'roleName': 'linglong175', 'photo': ''}
                }
        
        Returns:
        
        """
        info = cPickle.loads(zlib.decompress(info))
        gamelog.debug('@zq marriage#onMarriageQueryUnitInfo:', qType, info)
        gameglobal.rds.ui.marrySettingBg.onMarriageQueryFriendData(qType, info)

    def checkMarriageState(self):
        if self.marriageStage == gametypes.MARRIAGE_STAGE_PARADE and self.carrier.isMarriageMultiCarrier() and self.carrier.isRunningState() and not self.isOnCarrier():
            self.cell.applyEnterCarrier()

    def onEngageApply(self, isLogon, srcRoleName):
        """
        \xe5\xaf\xb9\xe6\x96\xb9\xe8\xa6\x81\xe6\xb1\x82\xe8\xae\xa2\xe5\xa9\x9a\xe7\x9a\x84\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe6\x8e\xa5\xe5\x8f\xa3
        Args:
            srcRoleName:
        
        Returns:
        
        """
        gamelog.debug('@zq marriage#onEngageApply:', isLogon, srcRoleName)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_MARRY_PROPOSE, {'click': Functor(self.openConfirmProposeMessage, srcRoleName)})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_MARRY_PROPOSE)
        if not isLogon:
            self.openConfirmProposeMessage(srcRoleName)

    def notifyMaidMarriageStart(self, husbandRoleName, wifeRoleName):
        """
        \xe9\x80\x9a\xe7\x9f\xa5\xe4\xbc\xb4\xe9\x83\x8e\xe3\x80\x81\xe4\xbc\xb4\xe5\xa8\x98\xe5\xa9\x9a\xe7\xa4\xbc\xe5\xbc\x80\xe5\x90\xaf\xe4\xba\x86\xef\xbc\x8c\xe5\x8f\xaf\xe4\xbb\xa5\xe4\xbc\xa0\xe9\x80\x81\xe4\xba\x86
        Args:
            husbandRoleName:
            wifeRoleName:
        
        Returns:
        
        """
        pass

    def notifyGuestMarriageStart(self, husbandRoleName, wifeRoleName):
        """
        \xe9\x80\x9a\xe7\x9f\xa5\xe5\xae\xbe\xe5\xae\xa2\xe5\xbc\x80\xe5\x90\xaf\xe4\xba\x86\xef\xbc\x8c\xe5\x8f\xaf\xe4\xbb\xa5\xe5\xaf\xbb\xe8\xb7\xaf\xe4\xba\x86
        Args:
            husbandRoleName:
            wifeRoleName:
        
        Returns:
        
        """
        pass

    def openConfirmProposeMessage(self, srcRoleName):
        msg = MSGDD.data.get('confirmProposeMessage', '%s') % srcRoleName

        def _noCallBack():
            _msg = MCD.data.get('engageRejectConfirm', '')
            self.engageRejectMessageId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(_msg, yesCallback=Functor(self.cell.rejectEngage), noCallback=Functor(self.openConfirmProposeMessage, srcRoleName), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, forbidFastKey=True, needDissMissCallBack=False)

        self.engageMessageId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onAccpetEngage, srcRoleName), noCallback=Functor(_noCallBack), yesBtnText=gameStrings.MARRIAGE_ENGAGE_ACCEPT, noBtnText=gameStrings.MARRIAGE_ENGAGE_REJECT, forbidFastKey=True, needDissMissCallBack=False)

    def onAccpetEngage(self, srcRoleName):
        intimacyTgt = None
        intimacyTgtGbId = self.friend.intimacyTgt
        if intimacyTgtGbId:
            for en in BigWorld.entities.values():
                if en.inWorld and utils.instanceof(en, 'Avatar') and en.gbId == intimacyTgtGbId:
                    intimacyTgt = en
                    break

        if intimacyTgt is None or not utils.isEntitiyInRange2D(self, intimacyTgt, 30):
            self.showGameMsg(GMDD.data.MARRIAGE_OP_FAILED_DISTANCE, ())
            self.openConfirmProposeMessage(srcRoleName)
            return
        else:
            self.cell.acceptEngage()
            return

    def onSyncRedPacketInfo(self, data):
        mInfo = []
        for i, rList in enumerate(data):
            rList = list(rList)
            rList.append(uiConst.RECEIVE_TYPE_ACCESS)
            mInfo.append(rList)

        self.marriageRedPacketInfo = mInfo
        self.refreshMarriageRedPacketPushMessage()

    def refreshMarriageRedPacketPushMessage(self):
        isValid = False
        for i, rList in enumerate(self.marriageRedPacketInfo):
            serinalNum, money, msg, srcName, receiveType = rList
            if receiveType == uiConst.RECEIVE_TYPE_ACCESS:
                isValid = True
                break

        if gameglobal.rds.ui.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_GET_MARRIAGE_RED_PACKET):
            if not isValid:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GET_MARRIAGE_RED_PACKET)
        elif isValid:
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GET_MARRIAGE_RED_PACKET, {'click': Functor(self.clickMarriageRedPacketMessage)})
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_MARRIAGE_RED_PACKET)

    def clickMarriageRedPacketMessage(self):
        gameglobal.rds.ui.marryReceiveRedPacket.show()

    def enterMarriageRoom(self):
        ins = editorHelper.instance()
        data = MCD.data.get('marriageRoom_%d' % self.mapID, {})
        if not data:
            index = 1
            while True:
                tempData = MCD.data.get('marriageRoom_%d_%d' % (self.mapID, index), {})
                if not tempData:
                    break
                data.update(tempData)
                index += 1

        if not data:
            try:
                moduleName = 'marriage_room_%d_data' % self.mapID
                module = __import__('data.%s' % moduleName, fromlist=[moduleName])
                data = module.data
            except:
                return

        self.enterMarriageRoomCallback = BigWorld.callback(1, Functor(ins.init, 0, data))

    def leaveMarriageRoom(self):
        callback = getattr(self, 'enterMarriageRoomCallback', 0)
        if callback:
            BigWorld.cancelCallback(callback)
            self.enterMarriageRoomCallback = None
        ins = editorHelper.instance()
        ins.destroy()

    @ui.scenarioCallFilter()
    def addMarriagePrompt(self, mtype):
        gamelog.debug('@zq marriage#addMarriagePrompt:', mtype)
        if mtype == uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL:
            self.enterMarriageHallMaidClick()
        elif mtype == uiConst.MESSAGE_TYPE_MARRIAGE_GUEST_HALL:
            self.enterMarriageHallGuestClick()
        elif mtype == uiConst.MESSAGE_TYPE_MARRIAGE_PARADE:
            self.applyMarriageParadeClick()
        elif mtype == uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER:
            self.applyMarriageCarrierClick()
        elif mtype == uiConst.MESSAGE_TYPE_MARRIAGE_ROOM:
            self.applyMarriageRoomClick()

    def addMarriageMessage(self, mtype):
        if mtype == uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL:
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL, {'click': Functor(self.enterMarriageHallMaidClick)})
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL)
        elif mtype == uiConst.MESSAGE_TYPE_MARRIAGE_GUEST_HALL:
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_MARRIAGE_GUEST_HALL, {'click': Functor(self.enterMarriageHallGuestClick)})
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_MARRIAGE_GUEST_HALL)
        elif mtype == uiConst.MESSAGE_TYPE_MARRIAGE_PARADE:
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_MARRIAGE_PARADE, {'click': Functor(self.applyMarriageParadeClick)})
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_MARRIAGE_PARADE)
        elif mtype == uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER:
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER, {'click': Functor(self.applyMarriageCarrierClick)})
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER)
        elif mtype == uiConst.MESSAGE_TYPE_MARRIAGE_ROOM:
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_MARRIAGE_ROOM, {'click': Functor(self.applyMarriageRoomClick)})
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_MARRIAGE_ROOM)

    def enterMarriageHallMaidClick(self):
        msg = MCD.data.get('enterMarriageHallMaidPushMessage', '')

        def _yesCallBack():
            self.cell.applyEnterMarriageHall(self.marriageNUID)
            if self.checkMarriageHallMaidMsg(True):
                self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL)

        def _noCallBack():
            if self.checkMarriageHallMaidMsg(True):
                self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL)

        mId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(_yesCallBack), noCallback=Functor(_noCallBack), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)
        self.marriageMsgDict[uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL] = mId

    def checkMarriageHallMaidMsg(self, weakCheck = False):
        mId = self.marriageMsgDict.get(uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL, 0)
        if self.marriageStage == gametypes.MARRIAGE_STAGE_ENTER_HALL and not self.inFubenType(const.FB_TYPE_MARRIAGE_HALL) and (not gameglobal.rds.ui.messageBox.hasMsgBox(mId) or weakCheck):
            return True
        return False

    def checkMarriageRoomMaidMsg(self, weakCheck = False):
        mId = self.marriageMsgDict.get(uiConst.MESSAGE_TYPE_MARRIAGE_ROOM, 0)
        if self.marriageStage == gametypes.MARRIAGE_STAGE_ENTER_RES and not self.inFubenType(const.FB_TYPE_MARRIAGE_ROOM) and (not gameglobal.rds.ui.messageBox.hasMsgBox(mId) or weakCheck):
            return True
        return False

    def checkMarriageCarrierMsg(self, weakCheck = False):
        mId = self.marriageMsgDict.get(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER, 0)
        if self.marriageStage == gametypes.MARRIAGE_STAGE_PARADE and self.carrier.isMarriageMultiCarrier() and self.carrier.isRunningState() and not self.isOnCarrier() and (not gameglobal.rds.ui.messageBox.hasMsgBox(mId) or weakCheck):
            return True
        return False

    def isOnMarriageCarrier(self):
        if self.carrier.isMarriageMultiCarrier() and self.isOnCarrier():
            return True
        return False

    def enterMarriageHallGuestClick(self):
        msg = MCD.data.get('enterMarriageHallGuestPushMessage', '')
        pos = MCD.data.get('enterMarriageHallGuestNavigatorPos', (0, 0, 0, 0))

        def _navigateNpc():
            navigator.getNav().pathFinding(pos)

        mId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(_navigateNpc), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)
        self.marriageMsgDict[uiConst.MESSAGE_TYPE_MARRIAGE_GUEST_HALL] = mId

    def applyMarriageParadeClick(self):
        msg = MCD.data.get('applyMarriageParadePushMessage', '')

        def _yesCallBack():
            self.cell.paradeMarriage(0)
            if self.marriageStage == gametypes.MARRIAGE_STAGE_ENTER_HALL:
                self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_PARADE)

        def _noCallBack():
            if self.marriageStage == gametypes.MARRIAGE_STAGE_ENTER_HALL:
                self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_PARADE)

        mId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(_yesCallBack), noCallback=Functor(_noCallBack), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)
        self.marriageMsgDict[uiConst.MESSAGE_TYPE_MARRIAGE_PARADE] = mId

    def applyMarriageCarrierClick(self):
        msg = MCD.data.get('applyMarriageCarrierPushMessage', '')

        def _yesCallBack():
            self.checkMarriageState()
            if self.checkMarriageCarrierMsg(True):
                self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER)

        def _noCallBack():
            if self.checkMarriageCarrierMsg(True):
                self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER)

        mId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(_yesCallBack), noCallback=Functor(_noCallBack), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)
        self.marriageMsgDict[uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER] = mId

    def applyMarriageRoomClick(self):
        msg = MCD.data.get('applyMarriageRoomPushMessage', '')

        def _yesCallBack():
            self.cell.applyEnterMarriagRoom(self.marriageNUID)
            if self.checkMarriageRoomMaidMsg(True):
                self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_ROOM)

        def _noCallBack():
            if self.checkMarriageRoomMaidMsg(True):
                self.addMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_ROOM)

        mId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(_yesCallBack), noCallback=Functor(_noCallBack), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)
        self.marriageMsgDict[uiConst.MESSAGE_TYPE_MARRIAGE_ROOM] = mId

    def addMarriageProgressMessage(self):
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_MARRIAGE_PROGRESS, {'click': Functor(self.showMarriageProgress)})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_MARRIAGE_PROGRESS)

    def showMarriageProgress(self):
        gameglobal.rds.ui.marryProcess.show()
        if self.inFubenType(const.FB_TYPE_MARRIAGE_HALL):
            gameglobal.rds.ui.marryHallFunc.show()
        self.removeMarriageProgressMessage()

    def removeMarriageProgressMessage(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_MARRIAGE_PROGRESS)

    def removeMarriageMessage(self, msgType):
        gameglobal.rds.ui.pushMessage.removePushMsg(msgType)
        mId = self.marriageMsgDict.get(msgType, None)
        if mId:
            gameglobal.rds.ui.messageBox.dismiss(mId, needDissMissCallBack=False)
            self.marriageMsgDict[msgType] = None

    @ui.callInCD(1)
    def queryMarriageUnitInfoEx(self, _type, serverList, needPatchData):
        if len(serverList) != len(needPatchData):
            return
        for i, hostId in enumerate(serverList):
            serverList[i] = RSND.data.get(hostId, {}).get('currentHostId', hostId)

        self.cell.queryCrossMarriageUnitInfo(_type, serverList, needPatchData)

    def isPlayingAmericanMarriageScenario(self):
        p = BigWorld.player()
        spaceNo = getattr(p, 'spaceNo', 0)
        fbNo = formula.getFubenNo(spaceNo)
        if fbNo == const.FB_NO_MARRIAGE_AMERICAN_HALL and gameglobal.SCENARIO_PLAYING:
            return True
        return False

    def inMarriageHall(self):
        p = BigWorld.player()
        spaceNo = getattr(p, 'spaceNo', 0)
        fbNo = formula.getFubenNo(spaceNo)
        if fbNo in const.FB_NO_MARRIAGE_HALL_SET:
            return True
        return False

    def isWifeOrHusband(self):
        p = BigWorld.player()
        hunsbandGbId = p.marriageBeInvitedInfo.get('hunsbandGbId', 0)
        wifeGbId = p.marriageBeInvitedInfo.get('wifeGbId', 0)
        if self.gbId == wifeGbId or self.gbId == hunsbandGbId:
            return True
        return False

    def syncMarriageIntimacyTgtEquipment(self, info):
        self.marriageTgtEquipment = info

    def getMarriageSkillCd(self):
        total = MCD.data.get('marriageCombatBuffCD', 5)
        remain = self.marriageSkillTime + total - utils.getNow() if self.marriageSkillTime else 0
        return (total, remain)
