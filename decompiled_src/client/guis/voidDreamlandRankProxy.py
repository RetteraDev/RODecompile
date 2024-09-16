#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidDreamlandRankProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import const
from uiProxy import UIProxy
from helpers import capturePhoto
from guis import uiUtils
MAX_NUM_PALYER = 5

class VoidDreamlandRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoidDreamlandRankProxy, self).__init__(uiAdapter)
        self.widget = None
        self.headGen = None
        self.resultInfo = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_DREAMLAND_RANK, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_DREAMLAND_RANK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            gameglobal.rds.sound.playSound(gameglobal.SD_4)

    def show(self, resultInfo):
        self.resultInfo = resultInfo
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VOID_DREAMLAND_RANK)

    def clearWidget(self):
        self.widget = None
        self.resetHeadGen()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_VOID_DREAMLAND_RANK)
        gameglobal.rds.sound.playSound(gameglobal.SD_5)

    def reset(self):
        self.resultInfo = {}
        self.headGen = None

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        friendTopInfo = self.resultInfo.get('friendTopInfo', [])
        friendTopInfo.sort(cmp=lambda x, y: y[0] - x[0] or x[1] - y[1])
        oldFriendRank = self.resultInfo.get('oldFriendRank', 0)
        newFriendRank = self.resultInfo.get('newFriendRank', 0)
        progress = self.resultInfo.get('progress', 0)
        useTime = self.resultInfo.get('useTime', 0)
        topRank = self.resultInfo.get('topRank', 0)
        result = self.resultInfo.get('result', False)
        self.updatePlayerPhoto3D(result)
        self.updateMyScoreAndUsedTime(progress, result, useTime)
        self.updateMineRankNum(topRank)
        self.updateFriendTopRank(friendTopInfo, oldFriendRank, newFriendRank)

    def _onConfirmBtnClick(self, e):
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        self.hide()

    def _onOpenRankBtnClick(self, e):
        gameglobal.rds.ui.ranking.showHuanjingRankPanel(const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND)

    def updatePlayerPhoto3D(self, result):
        self.initHeadGen()
        self.takePhoto3D()
        if result:
            self.widget.resultState.gotoAndStop('success')
        else:
            self.widget.resultState.gotoAndStop('fail')
        gameglobal.rds.sound.playSound(gameglobal.SD_474)

    def updateMyScoreAndUsedTime(self, progress, result, useTime):
        self.widget.score.textField.text = progress
        if not result:
            self.widget.evaluate.gotoAndStop('fail')
        else:
            self.widget.evaluate.gotoAndStop('sucess')
        self.widget.evaluate.textField.htmlText = self.updateTimeStr(useTime)

    def updateTimeStr(self, timeStr):
        return utils.formatTimeStr(timeStr, 'h:m:s', True, 2, 2, 2)

    def updateMineRankNum(self, topRank):
        if topRank > 0:
            self.widget.rankValue.noneRank.visible = False
            self.widget.rankValue.rankText.visible = True
            self.widget.rankValue.rankText.text = topRank
        else:
            self.widget.rankValue.noneRank.visible = True
            self.widget.rankValue.rankText.visible = False

    def updateFriendTopRank(self, friendTopInfo, oldFriendRank, newFriendRank):
        p = BigWorld.player()
        for i in range(MAX_NUM_PALYER):
            playerMc = self.widget.getChildByName('player%d' % i)
            if i < len(friendTopInfo):
                tInfo = friendTopInfo[i]
                playerMc.visible = True
                if p.gbId == int(tInfo[7]):
                    playerMc.gotoAndStop('me')
                    playerMc.rankText.text = newFriendRank
                    playerMc.upIcon.visible = False
                    if newFriendRank < oldFriendRank:
                        playerMc.upIcon.visible = True
                else:
                    playerMc.gotoAndStop('friend')
                    playerMc.upIcon.visible = False
                    playerMc.rankText.text = i + 1
                photo = tInfo[3]
                if uiUtils.isDownloadImage(photo):
                    photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
                if not photo:
                    photo = p.friend.getDefaultPhoto(tInfo[4], tInfo[5])
                playerMc.playerIcon.icon.clear()
                playerMc.playerIcon.icon.fitSize = True
                playerMc.playerIcon.icon.loadImage(photo)
                playerMc.playerName.text = tInfo[6]
                playerMc.diffScore.text = tInfo[0]
                playerMc.useTime.text = self.updateTimeStr(tInfo[1])
                if i == 0:
                    playerMc.rankText.visible = False
                    playerMc.rankIcon.gotoAndStop('gold')
                elif i == 1:
                    playerMc.rankText.visible = False
                    playerMc.rankIcon.gotoAndStop('silver')
                elif i == 2:
                    playerMc.rankText.visible = False
                    playerMc.rankIcon.gotoAndStop('copper')
                else:
                    playerMc.rankText.visible = True
                    playerMc.rankIcon.visible = False
            else:
                playerMc.visible = False

    def takePhoto3D(self):
        if not self.headGen:
            self.headGen = capturePhoto.VoidDreamlandPhotoGen.getInstance('gui/taskmask.tga', 400)
        self.headGen.startCapture(0, None, ('1101',))

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.VoidDreamlandPhotoGen.getInstance('gui/taskmask.tga', 400)
        self.headGen.initFlashMesh()
