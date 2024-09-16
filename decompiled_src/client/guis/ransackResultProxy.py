#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ransackResultProxy.o
import BigWorld
import uiConst
import events
import formula
import gamelog
import uiUtils
import const
import gametypes
from uiProxy import UIProxy
from data import summon_sprite_info_data as SSID

class RansackResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RansackResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANSACK_RESULT, self.hide)

    def reset(self):
        self.evalInfo = {}
        self.fbType = 0

    def showEvaluation(self, fbType, evalInfo):
        self.hide()
        self.evalInfo = evalInfo
        self.fbType = fbType
        self.show()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RANSACK_RESULT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RANSACK_RESULT)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_RANSACK_RESULT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if self.fbType == gametypes.SKY_WING_FB_CHALLENGE:
            self.widget.ransack.visible = False
            self.widget.challenge.visible = True
            avatarScore = self.evalInfo['skyWingChallengePlayerScore']
            spriteSocre = self.evalInfo['skyWingChallengeSpriteScore']
            timeScore = self.evalInfo['skyWingChallengeTimeScore']
            self.widget.challenge.txt0.text = str(avatarScore)
            self.widget.challenge.txt1.text = str(spriteSocre)
            self.widget.challenge.txt2.text = str(timeScore)
            self.widget.challenge.txtTotal.text = str(avatarScore + spriteSocre + timeScore)
            self.widget.challenge.yesBtn.addEventListener(events.BUTTON_CLICK, self.handleYesBtnClick, False, 0, True)
        else:
            self.widget.ransack.visible = True
            self.widget.challenge.visible = False
            avatarScore = self.evalInfo['skyWingRobPlayerScore']
            spriteSocre = self.evalInfo['skyWingRobSpriteScore']
            timeScore = self.evalInfo['skyWingRobTimeScore']
            self.widget.ransack.txt0.text = str(avatarScore)
            self.widget.ransack.txt1.text = str(spriteSocre)
            self.widget.ransack.txt2.text = str(timeScore)
            self.widget.ransack.txtTotal.text = str(avatarScore + spriteSocre + timeScore)
            self.widget.ransack.yesBtn.addEventListener(events.BUTTON_CLICK, self.handleYesBtnClick, False, 0, True)
            killAvatar = self.evalInfo['killPlayer'] > 0
            killSprite = self.evalInfo['killSprite'] > 0
            spritedId = self.evalInfo['skyWingTgtSpriteId']
            spriteVisible = True if spritedId else False
            self.widget.ransack.icon1.visible = spriteVisible
            self.widget.ransack.txtSprite.visible = spriteVisible
            self.widget.ransack.txt1.visible = spriteVisible
            sprtieData = SSID.data.get(spritedId, {})
            iconId = sprtieData.get('spriteIcon', '')
            school = self.evalInfo['skyWingTgtAvatarSchool']
            sex = self.evalInfo['skyWingTgtAvatarSex']
            nosPath = self.evalInfo['customPhoto']
            if uiUtils.isDownloadImage(nosPath):
                BigWorld.player().downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, nosPath, gametypes.NOS_FILE_PICTURE, self.onDownloadOtherPhoto, (nosPath,))
            else:
                headIcon = 'headIcon/%s.dds' % str(school * 10 + sex)
                self.widget.ransack.icon0.icon.fitSize = True
                self.widget.ransack.icon0.icon.loadImage(headIcon)
            self.widget.ransack.icon0.failedMc.visible = killAvatar
            self.widget.ransack.icon0.txtName.text = self.evalInfo['skyWingRobInfo'][1]
            self.widget.ransack.icon1.icon.fitSize = True
            self.widget.ransack.icon1.icon.loadImage('summonedSprite/icon/%s.dds' % iconId)
            self.widget.ransack.icon1.failedMc.visible = killSprite
            self.widget.ransack.icon1.txtName.text = sprtieData.get('name', '')
            self.widget.ransack.result.gotoAndStop('chengong' if killAvatar or killSprite else 'shibai')

    def onDownloadOtherPhoto(self, status, nosPath):
        if not self.widget:
            return
        photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + nosPath + '.dds'
        self.widget.ransack.icon0.icon.fitSize = True
        self.widget.ransack.icon0.icon.loadImage(photo)

    def testChallenge(self):
        import const
        evalInfo = {}
        spaceNo = const.FB_NO_SKY_WING_CHALLENGE
        evalInfo['skyWingChallengePlayerScore'] = 1
        evalInfo['skyWingChallengeSpriteScore'] = 2
        evalInfo['skyWingChallengeTimeScore'] = 4
        self.showEvaluation(spaceNo, evalInfo)

    def testRansack(self):
        import const
        evalInfo = {}
        spaceNo = const.FB_NO_SKY_WING_ROB
        evalInfo['skyWingRobPlayerScore'] = 1
        evalInfo['skyWingRobSpriteScore'] = 3
        evalInfo['skyWingRobTimeScore'] = 2
        evalInfo['killPlayer'] = 0
        evalInfo['killSprite'] = 0
        evalInfo['skyWingTgtSpriteId'] = 0
        evalInfo['skyWingRobInfo'] = (1, 'aaaa')
        evalInfo['skyWingTgtAvatarSchool'] = BigWorld.player().school
        evalInfo['skyWingTgtAvatarSex'] = BigWorld.player().physique.sex
        self.showEvaluation(spaceNo, evalInfo)

    def refreshInfo(self):
        if not self.widget:
            return

    def handleYesBtnClick(self, *args):
        gamelog.info('jbx:handleYesBtnClick')
        self.hide()
