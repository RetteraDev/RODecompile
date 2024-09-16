#Embedded file name: I:/bag/tmp/tw2/res/entities\client/NoticeBoard.o
import BigWorld
import const
import gamelog
import gametypes
import gameglobal
import utils
import commGuild
from helpers import modelServer
from callbackHelper import Functor
from guis import zhanQiMorpherFactory
from guis import ui
from guis import cursor
from helpers import tintalt as TA
from iClient import IClient
from data import item_data as ID
from data import game_msg_data as GMD
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD

class NoticeBoard(IClient):

    def __init__(self):
        super(NoticeBoard, self).__init__()
        self.hp = 1000
        self.mhp = 1000
        self.mp = 1000
        self.mmp = 1000
        self.lv = 1
        self.roleName = '公告板'

    def enterWorld(self):
        super(NoticeBoard, self).enterWorld()
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())

    def afterModelFinish(self):
        super(NoticeBoard, self).afterModelFinish()
        self.downloadAdvertise()
        self.model.setModelNeedHide(0, 0.5)
        self.setTargetCapsUse(True)
        if not len(self.approvedAdvertiseKey):
            TA.ta_reset([self.model])

    def leaveWorld(self):
        super(NoticeBoard, self).leaveWorld()

    def uploadAdvertise(self, filePath):
        player = BigWorld.player()
        if not self.checkPermission():
            return
        uploadCD = GCD.data.get('NoticeBoardUploadCD', 0)
        current = utils.getNow()
        if self.uploadTime + uploadCD > current:
            cleanUploadCDItemId = GCD.data.get('cleanNoticeBoardUploadCDItemId')
            amount = GCD.data.get('cleanNoticeBoardUploadCDItemAmount', 0)
            itemCnt = commGuild.getNoticeBoardItemCnt(self, amount, uploadCD)
            left = self.uploadTime + uploadCD - current
            if cleanUploadCDItemId:
                msg = GMD.data.get(GMDD.data.GUILD_NOS_FILE_TIME_LIMIT_NOTIFY, {}).get('text', '%s %d %s')
                itemName = ID.data.get(cleanUploadCDItemId, {}).get('name', '')
                msg = msg % (utils.formatDuration(left), itemCnt, itemName)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self._doUploadNosFileCheck, filePath), yesBtnText='强制上传')
            else:
                player.showGameMsg(GMDD.data.NOTICE_BOARD_UPLOAD_FAIL_CD, (utils.formatDuration(left),))
        else:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox('是否确定上传公告板图片？上传公告板图片的时间间隔为%s' % utils.formatDuration(GCD.data.get('NoticeBoardUploadCD', 0)), Functor(self._doUploadNosFile, filePath))

    def _doUploadNosFile(self, filePath):
        player = BigWorld.player()
        player.uploadNOSFile(filePath, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_NOTICEBOARD_ADVERTISE, {'gbId': player.gbId,
         'guildNUID': player.guildNUID,
         'guildName': player.guildName}, self.onUploadAdvertise)

    def _doUploadNosFileCheck(self, filePath):
        p = BigWorld.player()
        cleanUploadCDItemId = GCD.data.get('cleanNoticeBoardUploadCDItemId')
        amount = GCD.data.get('cleanNoticeBoardUploadCDItemAmount', 0)
        uploadCD = GCD.data.get('NoticeBoardUploadCD', 0)
        itemCnt = commGuild.getNoticeBoardItemCnt(self, amount, uploadCD)
        if cleanUploadCDItemId and not p.inv.canRemoveItems({cleanUploadCDItemId: itemCnt}, enableParentCheck=True):
            itemName = ID.data.get(cleanUploadCDItemId, {}).get('name', '')
            p.showGameMsg(GMDD.data.NOS_UPLOAD_FAILED_NO_SUCH_ITEM, (itemCnt, itemName))
            return
        p.uploadNOSFile(filePath, gametypes.NOS_FILE_PICTURE, gametypes.NOS_FILE_SRC_NOTICEBOARD_ADVERTISE, {'gbId': p.gbId,
         'guildNUID': p.guildNUID,
         'guildName': p.guildName}, self.onUploadAdvertise)

    def onUploadAdvertise(self, advertiseKey):
        if advertiseKey == None:
            gamelog.error('@szh NoticeBoard.uploadAdvertise fail: key=%s' % advertiseKey)
            return
        player = BigWorld.player()
        player.cell.uploadNoticeBoardAdvertise(self.id, advertiseKey)

    def downloadAdvertise(self):
        player = BigWorld.player()
        fileKey = self.approvedAdvertiseKey
        if len(fileKey) > 0:
            player.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, fileKey, gametypes.NOS_FILE_PICTURE, self.onDownloadApprovedAdvertise, ())
        elif self.model:
            TA.ta_reset([self.model])
        fileKey = self.advertiseKey
        if len(fileKey) > 0:
            player.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, fileKey, gametypes.NOS_FILE_PICTURE, self.onDownloadAdvertise, ())

    def refreshAdvertise(self):
        BigWorld.player().refreshNOSFileStatus(const.IMAGES_DOWNLOAD_RELATIVE_DIR, self.advertiseKey, gametypes.NOS_FILE_PICTURE, self.onDownloadAdvertise, ())

    def onDownloadApprovedAdvertise(self, status):
        gamelog.debug('@szh onDownloadApprovedAdvertise', self.id, status)
        if not self.inWorld:
            return
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            texturePath = '%s/%s.dds' % (const.IMAGES_DOWNLOAD_DIR, self.approvedAdvertiseKey)
            dyeMorpher = zhanQiMorpherFactory.NoticeBoardMorpher(self.model)
            dyeMorpher.read(texturePath)
            dyeMorpher.apply()
        elif status == gametypes.NOS_FILE_STATUS_PENDING:
            pass
        elif status == gametypes.NOS_FILE_STATUS_ILLEGAL:
            pass
        else:
            gamelog.info('@szh NoticeBoard.onDownloadApprovedAdvertise fail: status=%d key=%s' % (status, self.approvedAdvertiseKey))

    def onDownloadAdvertise(self, status):
        gamelog.debug('@szh onDownloadAdvertise', self.id, status)
        if not self.inWorld:
            return
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            gameglobal.rds.ui.guildBillBoard.setError(0)
            self.cell.onAdvertiseApproved()
        elif status == gametypes.NOS_FILE_STATUS_PENDING:
            gameglobal.rds.ui.guildBillBoard.setError(1)
        elif status == gametypes.NOS_FILE_STATUS_ILLEGAL:
            gameglobal.rds.ui.guildBillBoard.setError(2)
        else:
            gameglobal.rds.ui.guildBillBoard.setError(3)
            gamelog.info('@szh NoticeBoard.onDownloadAdvertise fail: status=%d key=%s' % (status, self.advertiseKey))

    def set_approvedAdvertiseKey(self, old):
        self.downloadAdvertise()

    def set_advertiseKey(self, old):
        self.downloadAdvertise()

    def getItemData(self):
        return {'model': gameglobal.NOTICE_BOARD_MODEL,
         'modelScale': 1}

    def use(self):
        if not self.inWorld:
            return
        gameglobal.rds.ui.guildBillBoard.show(self.fortId, self)

    def checkClickPermission(self):
        if not self.inWorld:
            return False
        p = BigWorld.player()
        fort = p.clanWar.fort.get(self.fortId, {})
        if fort and fort.ownerGuildNUID == p.guildNUID and p.guild and p.guild.leaderGbId == p.gbId:
            return True
        return False

    def checkPermission(self):
        if not self.inWorld:
            return False
        p = BigWorld.player()
        fort = p.clanWar.fort.get(self.fortId, {})
        if not (fort and fort.ownerGuildNUID == p.guildNUID and p.guild and p.guild.leaderGbId == p.gbId):
            return False
        if not gameglobal.rds.configData.get('enableNOSCustom', False):
            p.showGameMsg(GMDD.data.UPLOAD_ADVERTISE_UNAVAILABLE, ())
            return False
        return True

    def onTargetCursor(self, enter):
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                if (self.position - BigWorld.player().position).length > cursor.TALK_DISTANCE:
                    ui.set_cursor(cursor.talk_dis)
                else:
                    ui.set_cursor(cursor.talk)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()
