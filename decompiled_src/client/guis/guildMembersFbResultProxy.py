#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMembersFbResultProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import utils
import const
import formula
from uiProxy import UIProxy
from helpers import capturePhoto
from guis import events
from guis import uiUtils
from guis.asObject import MenuManager
from guis.asObject import TipManager
from data import guild_config_data as GCD
from data import achievement_data as AD
MAX_CARD_NUMBER = 5
MAX_RANK = 30

class GuildMembersFbResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMembersFbResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.fbResult = {}
        self.myRank = 0
        self.myRankExpired = 0
        self.headGen = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MEMBERS_FB_RESULT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_MEMBERS_FB_RESULT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.resetHeadGen()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_MEMBERS_FB_RESULT)

    def reset(self):
        self.fbResult = {}
        self.myRank = 0

    def show(self, fbNo, evalInfo):
        self.fbResult = evalInfo.get('guildFubenData', {})
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_MEMBERS_FB_RESULT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.openRank.addEventListener(events.BUTTON_CLICK, self.handleOpenRankClick, False, 0, True)
        self.widget.damageName.textField.text = ''
        self.widget.hurtedName.textField.text = ''
        self.widget.cureName.textField.text = ''
        self.initHeadGen()
        self.takePhoto3D()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if not p.guild:
            return
        self.widget.timeCost.textField.text = utils.formatTimeStr(self.fbResult.get('conquerTime', 0), 'h:m:s', True, 2, 2, 2)
        maxValues = self.fbResult.get('maxValue', ((0, 0), (0, 0), (0, 0)))
        maxDamageGbid = maxValues[0][0]
        maxHurtedGbid = maxValues[1][0]
        maxCureGbid = maxValues[2][0]
        if maxDamageGbid in p.guild.member:
            self.widget.damageName.textField.text = p.guild.member[maxDamageGbid].role
        if maxHurtedGbid in p.guild.member:
            self.widget.hurtedName.textField.text = p.guild.member[maxHurtedGbid].role
        if maxCureGbid in p.guild.member:
            self.widget.cureName.textField.text = p.guild.member[maxCureGbid].role
        if self.myRankExpired < utils.getNow():
            self.myRank = 0
        if self.isEliteFb():
            self.widget.rank.visible = True
            self.widget.openRank.visible = True
            self.widget.achieveNum.visible = True
            self.udpateAchieve()
            if self.myRank <= MAX_RANK and self.myRank != 0:
                self.widget.rank.textFieldOut.visible = False
                self.widget.rank.textFieldRank.visible = True
                self.widget.rank.textFieldRank.text = self.myRank
            else:
                self.widget.rank.textFieldOut.visible = True
                self.widget.rank.textFieldRank.visible = False
        else:
            self.widget.rank.visible = False
            self.widget.openRank.visible = False
            self.widget.achieveNum.visible = False
        self.updataCards()

    def isEliteFb(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if fbNo == const.FB_NO_GUILD_FUBEN_ELITE:
            return True
        return False

    def udpateAchieve(self):
        achieveData = self.fbResult.get('achieve', {})
        finishNum = 0
        for value in achieveData.values():
            if value[1]:
                finishNum += 1

        self.widget.achieveNum.achieveText.text = gameStrings.TEXT_GUILDMEMBERSFBRESULTPROXY_127 % (finishNum, MAX_CARD_NUMBER)
        if finishNum > 0:
            self.widget.achieveNum.stateIcon.gotoAndStop('bright')
        else:
            self.widget.achieveNum.stateIcon.gotoAndStop('grey')
        bigTipMc = self.widget.getInstByClsName('GuildMembersFbResult_AchieveBigTip')
        for i, bossId in enumerate(achieveData):
            tipMc = bigTipMc.getChildByName('tipMc%d' % i)
            adValue = achieveData.get(bossId, (0, 0, 0))
            achieveId = adValue[0]
            adData = AD.data.get(achieveId, {})
            name = adData.get('name', '')
            desc = adData.get('desc', '')
            if adValue[1]:
                color = '#FCEDCE'
                tipMc.finishT.visible = True
                tipMc.timeT.visible = True
                tipMc.timeT.text = '-%d' % adValue[2]
            else:
                color = '#676767'
                tipMc.finishT.visible = False
                tipMc.timeT.visible = False
            tipMc.nameT.htmlText = uiUtils.toHtml(name, color)
            tipMc.descT.text = desc

        TipManager.addTipByMc(self.widget.achieveNum, bigTipMc, 'over', 'upLeft')

    def updataCards(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        bossData = self.fbResult.get('bossData', {})
        bossIdList = sorted(bossData.keys())
        achieveData = self.fbResult.get('achieve', {})
        for i in xrange(1, MAX_CARD_NUMBER + 1):
            card = self.widget.getChildByName('card%d' % i)
            if i <= len(bossIdList):
                card.gotoAndStop('open')
                bossId = bossIdList[i - 1]
                killBossTime = bossData.get(bossId, 0)
                iconId = GCD.data.get('guildBossResultIcon', {}).get(fbNo, {}).get(bossId, 0)
                iconPath = 'fubenResultPic/%d.dds' % iconId
                card.image.loadImage(iconPath)
                card.consumeTime.text = utils.formatTimeStr(killBossTime, 'h:m:s', True, 2, 2, 2)
                adValue = achieveData.get(bossId, (0, 0, 0))
                achieveId = adValue[0]
                adData = AD.data.get(achieveId, {})
                name = adData.get('name', '')
                desc = adData.get('desc', '')
                if self.isEliteFb():
                    card.achieveMc.visible = True
                    smallTipMc = self.widget.getInstByClsName('GuildMembersFbResult_AchieveSmallTip')
                    if adValue[1]:
                        card.achieveMc.stateIcon.gotoAndStop('bright')
                        color = '#FCEDCE'
                        smallTipMc.finishT.visible = True
                        smallTipMc.timeT.visible = True
                        smallTipMc.timeT.text = '-%ds' % adValue[2]
                    else:
                        card.achieveMc.stateIcon.gotoAndStop('grey')
                        color = '#676767'
                        smallTipMc.finishT.visible = False
                        smallTipMc.timeT.visible = False
                    card.achieveMc.achieveText.htmlText = uiUtils.toHtml(name, color)
                    smallTipMc.nameT.htmlText = uiUtils.toHtml(name, color)
                    smallTipMc.descT.text = desc
                    TipManager.addTipByMc(card.achieveMc, smallTipMc)
                else:
                    card.achieveMc.visible = False
            else:
                card.gotoAndStop('unOpen')

    def handleOpenRankClick(self, *args):
        p = BigWorld.player()
        p.base.queryGuildBossEliteTopData('')

    def updateMyFbRank(self, rank):
        self.myRank = rank
        self.myRankExpired = utils.getNow() + 60
        if not self.widget:
            return
        self.refreshInfo()

    def takePhoto3D(self):
        if not self.headGen:
            self.headGen = capturePhoto.GuildMembersFbPhotoGen.getInstance('gui/taskmask.tga', 400)
        self.headGen.startCapture(0, None, ('1101',))

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.GuildMembersFbPhotoGen.getInstance('gui/taskmask.tga', 400)
        self.headGen.initFlashMesh()
