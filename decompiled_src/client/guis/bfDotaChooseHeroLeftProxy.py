#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaChooseHeroLeftProxy.o
import BigWorld
import uiUtils
import uiConst
import utils
import skillDataInfo
import gamelog
import gametypes
from uiProxy import UIProxy
from guis import ui
from guis import events
from guis.asObject import TipManager
from guis import tipUtils
from guis.asObject import ASUtils
from data import zaiju_data as ZD
MAX_MEMBER_CNT = 5

class BfDotaChooseHeroLeftProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaChooseHeroLeftProxy, self).__init__(uiAdapter)
        self._resetData()

    def _resetData(self):
        self.widget = None
        self.mcList = []

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self._initUI()
        self.refreshFrame()

    def show(self):
        if self.widget:
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_DOTA_CHOOSE_HERO_LEFT)

    def clearWidget(self):
        self._resetData()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_DOTA_CHOOSE_HERO_LEFT)

    def getFrameInfo(self):
        infoList = []
        p = BigWorld.player()
        if not p:
            return infoList
        selfSideNUID = p.bfSideNUID
        gbIdList = []
        for gbId, mInfo in p.battleFieldTeam.iteritems():
            if gbId == p.gbId:
                continue
            if mInfo['sideNUID'] == selfSideNUID:
                gbIdList.append(gbId)

        gbIdList.sort()
        info = {}
        info['zaijuId'] = p.bfDotaZaijuRecord.get(p.gbId, 0)
        zjd = ZD.data.get(info['zaijuId'], {})
        info['zaijuName'] = zjd.get('name', '')
        info['headIcon'] = uiUtils.getZaijuLittleHeadIconPathById(info['zaijuId'])
        info['roleName'] = p.roleName.split('-')[0]
        info['isSelf'] = True
        skill0, skill1 = p.bfDotaTalentSkillRecord.get(p.gbId, (10100, 10101))
        info['skills'] = ((skill0, 1), (skill1, 1))
        infoList.append(info)
        if gbIdList:
            for gbId in gbIdList:
                info = {}
                info['zaijuId'] = p.bfDotaZaijuRecord.get(gbId, 0)
                zjd = ZD.data.get(info['zaijuId'], {})
                info['zaijuName'] = zjd.get('name', '')
                info['headIcon'] = uiUtils.getZaijuLittleHeadIconPathById(info['zaijuId'])
                info['isSelf'] = False
                info['roleName'] = p.battleFieldTeam[gbId].get('roleName', '')
                skillIds = p.bfDotaTalentSkillRecord.get(gbId, (10100, 10100))
                skill0 = (skillIds[0], 1)
                skill1 = (skillIds[1], 1)
                info['skills'] = (skill0, skill1)
                infoList.append(info)

        infoList.sort(cmp=lambda x, y: cmp(x['roleName'], y['roleName']))
        return infoList

    @ui.uiEvent(uiConst.WIDGET_DOTA_CHOOSE_HERO_LEFT, (events.EVENT_TALENT_SKILL_CHANGE, events.EVENT_BF_DOTA_ZAIJU_CHANGE))
    def refreshFrame(self, event = None):
        if not self.widget:
            return
        infoList = self.getFrameInfo()
        for i in xrange(MAX_MEMBER_CNT):
            mc = self.mcList[i]
            if i >= len(infoList):
                mc.selectedEff.visible = False
                mc.selected.visible = False
                mc.headIcon.loadImage('')
                mc.bg.selectedEffect.visible = False
                mc.bg.gotoAndStop('normal')
                mc.bg.txtZaijuName.text = ''
                mc.bg.txtPlayerName.text = ''
                mc.skill0.visible = False
                mc.skill1.visible = False
            else:
                mc.skill0.visible = True
                mc.skill1.visible = True
                self.setTeammate(mc, infoList[i])

    def setTeammate(self, mc, info):
        if info['zaijuId'] == 0:
            mc.selectedEff.visible = False
            mc.selected.visible = False
            mc.headIcon.loadImage('')
            mc.bg.selectedEffect.visible = False
        else:
            mc.selectedEff.visible = True
            mc.selected.visible = True
            mc.headIcon.fitSize = True
            mc.bg.selectedEffect.visible = True
            mc.headIcon.loadImage(info['headIcon'])
        if info['isSelf']:
            mc.bg.gotoAndStop('selected')
        else:
            mc.bg.gotoAndStop('normal')
        mc.bg.txtZaijuName.text = info['zaijuName']
        mc.bg.txtPlayerName.text = info['roleName']
        try:
            skillInfo0 = skillDataInfo.ClientSkillInfo(*info['skills'][0])
            mc.skill0.fitSize = True
            mc.skill0.loadImage(uiUtils.getSkillIconPath(skillInfo0))
        except:
            gamelog.error('@jbx skillInfo', info['skills'])

        try:
            skillInfo1 = skillDataInfo.ClientSkillInfo(*info['skills'][1])
            mc.skill1.fitSize = True
            mc.skill1.loadImage(uiUtils.getSkillIconPath(skillInfo1))
        except:
            gamelog.error('@jbx skillInfo', info['skills'])

        TipManager.addTipByType(mc.skill0, tipUtils.TYPE_SKILL, info['skills'][0][0])
        TipManager.addTipByType(mc.skill1, tipUtils.TYPE_SKILL, info['skills'][1][0])

    def _initUI(self):
        for i in xrange(MAX_MEMBER_CNT):
            mc = self.widget.mainMc.getChildByName('item%d' % i)
            self.mcList.append(mc)
            ASUtils.setHitTestDisable(mc.bg.selectedEffect, True)
