#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qrCodeShareAchievementProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
from uiProxy import UIProxy
from guis import uiUtils
from data import qr_code_share_data as QCSD
from data import school_data as SD
BG_PATH = 'shareAchievementBG/%s.dds'

class QrCodeShareAchievementProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QrCodeShareAchievementProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_QRCODE_ACHIEVEMENT_SHARE, self.hide)

    def reset(self):
        self.qrCodeId = -1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_QRCODE_ACHIEVEMENT_SHARE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_QRCODE_ACHIEVEMENT_SHARE)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_QRCODE_ACHIEVEMENT_SHARE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.mainMC.closeBtn
        self.widget.mainMC.rewardSlot.dragable = False

    def refreshInfo(self):
        if not self.widget:
            return
        showData = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_ACHIEVEMENT_SHARE)
        self.qrCodeId = showData.get('data', {}).get('qrCodeId', 0)
        data = QCSD.data.get(self.qrCodeId, {})
        mainMC = self.widget.mainMC
        mainMC.achievementInfo.achievementName.text = data.get('achievementName', '')
        mainMC.achievementInfo.achievementDesc.htmlText = data.get('shareDesc', '')
        mainMC.achievementInfo.serverInfo.htmlText = utils.getServerName(utils.getHostId())
        if data.has_key('topNumberDesc'):
            mainMC.achievementInfo.topInfo.htmlText = data.get('topNumberDesc', '%d') % showData.get('data', {}).get('realTriggerCnt', 0)
        else:
            mainMC.achievementInfo.topInfo.htmlText = ''
        mainMC.achievementInfo.roleInfo.htmlText = data.get('playerInfo', '%s %d %s') % (BigWorld.player().realRoleName, BigWorld.player().lv, SD.data.get(BigWorld.player().realSchool, {}).get('name', ''))
        mainMC.bgPic.loadImage(BG_PATH % data.get('bgImgPath', ''))
        realTriggerCnt = showData.get('data', {}).get('realTriggerCnt', 0)
        if not realTriggerCnt or realTriggerCnt > 1:
            mainMC.rewardSlot.visible = False
            mainMC.rewardTitle.visible = False
        else:
            mainMC.rewardSlot.visible = True
            mainMC.rewardTitle.visible = True
            itemData = uiUtils.getGfxItemById(data.get('rewardId', 0))
            mainMC.rewardSlot.setItemSlotData(itemData)
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_ACHIEVEMENT_SHARE, showData)

    def pushShareIcon(self, qrCodeId, realTriggerCnt):
        if not gameglobal.rds.configData.get('enableQRCode', False):
            return
        qcsdData = QCSD.data.get(qrCodeId, {})
        if not qcsdData:
            return
        pushType = qcsdData.get('pushType', 0)
        pushPriority = qcsdData.get('pushPriority', 0)
        pushMsgList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_ACHIEVEMENT_SHARE)
        for msg in pushMsgList:
            data = msg.get('data', {})
            if data.get('qrCodeId', 0) == qrCodeId:
                gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_ACHIEVEMENT_SHARE, msg)
                break
            if pushType != 0 and data.get('pushType', 0) == pushType:
                if data.get('pushPriority', 0) <= pushPriority:
                    gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_ACHIEVEMENT_SHARE, msg)
                    break
                else:
                    return

        showData = {'data': {'qrCodeId': qrCodeId,
                  'realTriggerCnt': realTriggerCnt,
                  'pushType': pushType,
                  'pushPriority': pushPriority}}
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ACHIEVEMENT_SHARE, showData)

    def _onShareBtnClick(self, e):
        bgMC = self.widget.mainMC.bgPic
        info = gameglobal.rds.ui.qrCodeAppScanShare.createShareInfoInstance()
        info.qrCodeId = self.qrCodeId
        info.uiRange = uiUtils.getMCTopBottomOnWidget(self.widget, bgMC)
        gameglobal.rds.ui.qrCodeAppScanShare.show(info)
