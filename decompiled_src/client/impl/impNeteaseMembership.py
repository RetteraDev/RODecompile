#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNeteaseMembership.o
import BigWorld
import gamelog
import gameglobal
from data import netease_membership_config_data as NMCD
from neteaseMembershipInfo import NeteaseMembership

class ImpNeteaseMembership(object):

    def onUpdateMallVIPPrivilege(self, info):
        gamelog.info('@hqx__onUpdateMallVIPPrivilege', info)
        self.mallPrivilegeData = info
        self.updateTianYuMallVipPrivilegeInfo()
        if gameglobal.rds.ui.tianyuMall.tianyuAppVipPanel:
            gameglobal.rds.ui.tianyuMall.tianyuAppVipPanel.refreshInfo()
        if gameglobal.rds.ui.welfareAppVip:
            gameglobal.rds.ui.welfareAppVip.refreshInfo()
            gameglobal.rds.ui.welfare.refreshInfo()

    def onUpdateNeteaseMembershipInfo(self, neteaseMembershipInfo):
        self.neteaseMembershipInfo = neteaseMembershipInfo
        if gameglobal.rds.ui.tianyuMall.tianyuAppVipPanel:
            gameglobal.rds.ui.tianyuMall.tianyuAppVipPanel.refreshInfo()
        if gameglobal.rds.ui.welfareAppVip:
            gameglobal.rds.ui.welfareAppVip.refreshInfo()
            gameglobal.rds.ui.welfare.refreshInfo()

    def updateTianYuMallVipPrivilegeInfo(self):
        if not hasattr(self, 'statsInfo'):
            return
        if not hasattr(self, 'mallPrivilegeData'):
            self.mallPrivilegeData = {}
        mallVIPPrivilegeTaskReq = NMCD.data.get('mallVIPPrivilegeTaskReq', {})
        for key in mallVIPPrivilegeTaskReq:
            taskReqire = mallVIPPrivilegeTaskReq.get(key, {})
            privilegeIndexs = taskReqire.get('index', ())
            attrName = taskReqire.get('name', ())
            for index in privilegeIndexs:
                if self.mallPrivilegeData.has_key(index):
                    self.mallPrivilegeData.get(index)['value'] = self.statsInfo.get(attrName, 0)
                else:
                    self.mallPrivilegeData[index] = {'state': 0,
                     'value': self.statsInfo.get(attrName, 0)}

        if gameglobal.rds.ui.tianyuMall.tianyuAppVipPanel:
            gameglobal.rds.ui.tianyuMall.tianyuAppVipPanel.refreshInfo()
        if gameglobal.rds.ui.welfareAppVip:
            gameglobal.rds.ui.welfareAppVip.refreshInfo()
            gameglobal.rds.ui.welfare.refreshInfo()

    def onGetAvatarBirthInDbTime(self, birthInDB):
        self.birthInDB = birthInDB
