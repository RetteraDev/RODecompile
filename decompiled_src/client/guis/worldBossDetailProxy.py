#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldBossDetailProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
from guis.asObject import ASObject
from guis import uiUtils
from guis import events
from uiProxy import UIProxy
from guis.asObject import ASUtils
from guis import worldBossHelper
from guis.asObject import ASObject
from data import duel_config_data as DCD
from gamestrings import gameStrings
from helpers import tickManager
TAB_GUILD_RANK = 0
TAB_PERSONAL_RANK = 1
RANK_NUM = 3
REWARD_NUM = 3
QUERY_ATTEND_INTERVAL = 8

class WorldBossDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WorldBossDetailProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currRefIdx = 0
        self.currRefId = 0
        self.bossList = []
        self.currentTab = TAB_GUILD_RANK
        self.refreshTimeTick = 0
        self.lastQueryAttendTime = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WORLD_BOSS_DETAIL, self.hide)

    def reset(self):
        if self.refreshTimeTick:
            tickManager.stopTick(self.refreshTimeTick)
            self.refreshTimeTick = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WORLD_BOSS_DETAIL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WORLD_BOSS_DETAIL)

    def queryRankData(self):
        if not self.currRefId:
            return
        if self.currentTab == TAB_GUILD_RANK:
            worldBossHelper.getInstance().queryBossRankInfo(self.currRefId)
        else:
            worldBossHelper.getInstance().queryBossRankInfo(self.currRefId, False)

    def queryAttendNum(self):
        p = BigWorld.player()
        p.base.queryGuildJoinCnt()

    def show(self, refId = 0):
        worldBossHelper.getInstance().queryWorldBossInfo()
        bossList = worldBossHelper.getInstance().getWorldBossRefList()
        if not bossList:
            return
        self.setBossListData(bossList, refId)
        self.queryRankData()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WORLD_BOSS_DETAIL)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.leftBtn.addEventListener(events.BUTTON_CLICK, self.onLeftBtnClick)
        self.widget.rightBtn.addEventListener(events.BUTTON_CLICK, self.onRightBtnClick)
        self.widget.guildBtn.addEventListener(events.BUTTON_CLICK, self.onTabBtnClick)
        self.widget.personBtn.addEventListener(events.BUTTON_CLICK, self.onTabBtnClick)
        self.widget.rewardMc.rewardBtn.addEventListener(events.BUTTON_CLICK, self.onRewardBtnClick)
        if self.refreshTimeTick:
            tickManager.stopTick(self.refreshTimeTick)
        self.refreshTimeTick = tickManager.addTick(1, self.refreshRemainTime)

    def setBossListData(self, bossList, refId):
        self.bossList = bossList
        self.currRefIdx = 0
        if refId and refId in self.bossList:
            self.currRefId = refId
            self.currRefIdx = self.bossList.index(refId)
        else:
            rareBossIdx = self.getLiveRareBossIdx(bossList)
            if rareBossIdx >= 0:
                self.currRefIdx = rareBossIdx
            self.currRefId = self.bossList[self.currRefIdx]

    def getLiveRareBossIdx(self, bossList):
        for i, refId in enumerate(bossList):
            bossInfo = worldBossHelper.getInstance().getWorldBossInfo(refId)
            if worldBossHelper.getInstance().isRareBoss(bossInfo.get('bossType', 0)):
                if bossInfo.get('isLive', False):
                    return i

        return -1

    def refreshInfo(self):
        if not self.widget:
            return
        bossList = worldBossHelper.getInstance().getWorldBossRefList()
        if not bossList:
            self.hide()
            return
        if bossList != self.bossList:
            self.setBossListData(bossList, self.currRefId)
        self.widget.leftBtn.enabled = self.currRefIdx > 0
        self.widget.rightBtn.enabled = self.currRefIdx < len(self.bossList) - 1
        self.currRefId = self.bossList[self.currRefIdx]
        self.refreshDropDown()
        self.refreshBossInfo()
        self.refreshRank()
        self.refreshReward()
        self.refreshAttendNum()
        self.refreshRemainTime()

    def refreshDropDown(self):
        ASUtils.setDropdownMenuData(self.widget.bossDrop, self.getDropData())
        self.widget.bossDrop.removeEventListener(events.INDEX_CHANGE, self.onDropIndexChange)
        self.widget.bossDrop.selectedIndex = self.currRefIdx
        self.widget.bossDrop.addEventListener(events.INDEX_CHANGE, self.onDropIndexChange)

    def getDropData(self):
        data = []
        for refId in self.bossList:
            info = worldBossHelper.getInstance().getWorldBossInfo(refId)
            data.append({'label': info.get('bossName', '')})

        return data

    def onDropIndexChange(self, *args):
        e = ASObject(args[3][0])
        self.currRefIdx = e.currentTarget.selectedIndex
        self.refreshInfo()

    def onLeftBtnClick(self, *args):
        if self.currRefIdx > 0:
            self.currRefIdx -= 1
        self.refreshInfo()

    def onRightBtnClick(self, *args):
        if self.currRefIdx < len(self.bossList) - 1:
            self.currRefIdx += 1
        self.refreshInfo()

    def onTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        mcName = e.currentTarget.name
        if mcName == 'guildBtn':
            self.currentTab = TAB_GUILD_RANK
        else:
            self.currentTab = TAB_PERSONAL_RANK
        self.queryRankData()
        self.refreshRank()

    def onRewardBtnClick(self, *args):
        gameglobal.rds.ui.generalReward.show(DCD.data.get('worldBossRewardId', 0))

    def getSelfGuildDmgText(self, bossDetail):
        p = BigWorld.player()
        if not p.guildNUID:
            return ''
        guildRankInfo = bossDetail.get('guildRank', [])
        for rankInfo in guildRankInfo:
            if long(rankInfo[3]) == long(p.guildNUID):
                name, per, dmg, _ = rankInfo
                valueText = '%s(%s)' % (utils.convertNum(dmg), per)
                dmgText = gameStrings.WORLD_BOSS_GUILD_TOTAL_DMG % valueText
                return dmgText

        return ''

    def refreshRank(self, refId = 0):
        if not self.widget:
            return
        if refId and refId != self.currRefId:
            return
        self.widget.guildBtn.selected = False
        self.widget.personBtn.selected = False
        self.widget.rankArea.noTip.visible = False
        for i in xrange(RANK_NUM):
            rankMc = self.widget.rankArea.getChildByName('item%d' % i)
            rankMc.visible = False

        bossDetail = worldBossHelper.getInstance().getWorldBossDetail(self.currRefId)
        if self.currentTab == TAB_GUILD_RANK:
            self.widget.guildBtn.selected = True
            self.widget.rankArea.title1.text = gameStrings.GUILD_NAME
            guildRankInfo = bossDetail.get('guildRank', [])
            if not guildRankInfo:
                self.widget.rankArea.noTip.visible = True
            else:
                for i in xrange(RANK_NUM):
                    rankMc = self.widget.rankArea.getChildByName('item%d' % i)
                    if i < len(guildRankInfo):
                        rankMc.visible = True
                        name, per, dmg, _ = guildRankInfo[i]
                        rankMc.attr0.text = i + 1
                        rankMc.attr1.text = name
                        rankMc.attr2.text = '%s(%s)' % (utils.convertNum(dmg), per)

        else:
            self.widget.personBtn.selected = True
            self.widget.rankArea.title1.text = gameStrings.PLAYER_NAME
            personRankInfo = bossDetail.get('personalRank', [])
            if not personRankInfo:
                self.widget.rankArea.noTip.visible = True
            else:
                for i in xrange(RANK_NUM):
                    rankMc = self.widget.rankArea.getChildByName('item%d' % i)
                    if i < len(personRankInfo):
                        rankMc.visible = True
                        name, dmg = personRankInfo[i]
                        rankMc.attr0.text = i + 1
                        rankMc.attr1.text = name
                        rankMc.attr2.text = utils.convertNum(dmg)

        totalDmg = bossDetail.get('totalDmg', 0)
        if totalDmg:
            self.widget.bossIcon.totalDmg.htmlText = gameStrings.WORLD_BOSS_TOTAL_DMG % utils.convertNum(totalDmg)
        else:
            self.widget.bossIcon.totalDmg.htmlText = ''
        if bossDetail.get('isLive', False):
            self.widget.deadIcon.visible = False
        else:
            self.widget.deadIcon.visible = True
        self.widget.totalGuildDmg.text = self.getSelfGuildDmgText(bossDetail)

    def refreshAttendNum(self):
        if self.widget:
            p = BigWorld.player()
            attendNum = getattr(p, 'worldBossAttendNum', 0)
            if attendNum:
                self.widget.attendNum.text = gameStrings.WORLD_BOSS_GUILD_ATTEND_NUM % p.worldBossAttendNum
            else:
                self.widget.attendNum.text = ''

    def refreshBossInfo(self):
        p = BigWorld.player()
        bossDetail = worldBossHelper.getInstance().getWorldBossDetail(self.currRefId)
        if not bossDetail:
            return
        self.widget.bossIcon.icon.fitSize = True
        self.widget.bossIcon.icon.loadImage(bossDetail.get('bossIcon', ''))
        position = bossDetail.get('position', (0, 0, 0))
        firstAttacker = bossDetail.get('firstAttacker', {})
        self.widget.bossIcon.positionText.htmlText = gameStrings.WORLD_BOSS_POS % (1,
         position[0],
         position[1],
         position[2],
         position[0],
         position[1],
         position[2])
        if not firstAttacker:
            self.widget.playerInfo.visible = False
            self.widget.noTip.visible = True
        else:
            self.widget.playerInfo.visible = True
            self.widget.noTip.visible = False
            self.widget.playerInfo.playerName.text = firstAttacker.get('playerName', '')
            guildName = firstAttacker.get('guildName', '')
            if guildName:
                self.widget.playerInfo.guildName.text = gameStrings.BELONES_TO_GUILD % guildName
            else:
                self.widget.playerInfo.guildName.text = ''
            headIcon = self.widget.playerInfo.playerHead.headIcon
            borderImg = self.widget.playerInfo.playerHead.borderImg
            photoUrl = firstAttacker.get('photo', '')
            borderIconPath = BigWorld.player().getPhotoBorderIcon(firstAttacker.get('borderId', 1), uiConst.PHOTO_BORDER_ICON_SIZE108)
            borderImg.fitSize = True
            borderImg.loadImage(borderIconPath)
            if photoUrl:
                headIcon.fitSize = True
                headIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
                headIcon.serverId = p.getOriginHostId()
                headIcon.setContentUnSee()
                headIcon.url = photoUrl
            else:
                photoUrl = utils.getDefaultPhoto(firstAttacker.get('school', 0), firstAttacker.get('sex', 0))
                headIcon.fitSize = True
                headIcon.imgType = uiConst.IMG_TYPE_HTTP_IMG
                headIcon.loadImage(photoUrl)

    def refreshReward(self):
        rewardList = worldBossHelper.getInstance().getWorldBossRewards(self.currRefId)
        for i in xrange(REWARD_NUM):
            rewardSlot = self.widget.rewardMc.getChildByName('slot%d' % i)
            if i < len(rewardList):
                rewardSlot.visible = True
                rewardSlot.dragable = False
                itemId, num = rewardList[i]
                itemInfo = uiUtils.getGfxItemById(itemId, num)
                rewardSlot.setItemSlotData(itemInfo)
            else:
                rewardSlot.visible = False

    def formateTime(self, time):
        minute = int(time / 60)
        sec = time - minute * 60
        return '%02d:%02d' % (minute, sec)

    def refreshRemainTime(self):
        bossDetail = worldBossHelper.getInstance().getWorldBossDetail(self.currRefId)
        remainTime = max(bossDetail['ttl'] - (utils.getNow() - bossDetail['startTime']), 0)
        if remainTime > 0:
            self.widget.bossIcon.remainTime.text = gameStrings.WORLD_BOSS_REMAIN % self.formateTime(remainTime)
        else:
            self.widget.bossIcon.remainTime.text = ''
        if utils.getNow() - self.lastQueryAttendTime > QUERY_ATTEND_INTERVAL:
            self.lastQueryAttendTime = utils.getNow()
            self.queryAttendNum()
