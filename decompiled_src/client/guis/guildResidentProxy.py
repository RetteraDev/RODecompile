#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildResidentProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import uiConst
import const
import uiUtils
import utils
import commGuild
from ui import unicode2gbk
from uiProxy import SlotDataProxy
from helpers import guild as guildUtils
from callbackHelper import Functor
from data import guild_config_data as GCD
from data import guild_job_data as GJD
from data import guild_resident_template_data as GRTD
from data import guild_status_stype_data as GSSD
from cdata import guild_resident_lv_data as GRLD
from cdata import game_msg_def_data as GMDD
import Lyuba

class GuildResidentProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(GuildResidentProxy, self).__init__(uiAdapter)
        self.modelMap = {'changeName': self.onChangeName,
         'levelUp': self.onLevelUp,
         'recommend': self.onRecommend,
         'hire': self.onHire,
         'leave': self.onLeave,
         'dispatch': self.onDispatch,
         'fire': self.onFire,
         'rest': self.onRest,
         'dispatchInto': self.onDispatchInto}
        self.mediator = None
        self.bindType = 'guildResident'
        self.type = 'guildResident'
        self.panelType = 0
        self.residentNUID = 0
        self.resident = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RESIDENT, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_RESIDENT:
            self.mediator = mediator
            self.refreshInfo()

    def show(self, panelType, residentNUID = 0, resident = None):
        self.panelType = panelType
        self.residentNUID = residentNUID
        self.resident = resident
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_RESIDENT)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_RESIDENT)

    def reset(self):
        self.panelType = 0
        self.residentNUID = 0
        self.resident = None

    def hideByNUID(self, residentNUID):
        if self.mediator and self.residentNUID == residentNUID:
            self.hide()

    def hideByNpcId(self, npcId):
        if self.mediator and gameglobal.rds.ui.guild.residentNpcId == npcId:
            self.hide()

    def hideByPanelType(self, panelType):
        if self.mediator and self.panelType == panelType:
            self.hide()

    def refreshInfo(self, residentNUID = 0):
        if residentNUID and self.residentNUID != residentNUID:
            return
        else:
            if self.mediator:
                p = BigWorld.player()
                guild = p.guild
                resident = None
                if self.panelType == uiConst.GUILD_RESIDENT_PANEL_NEW:
                    resident = self.resident
                elif self.panelType == uiConst.GUILD_RESIDENT_PANEL_RECOMMENDED:
                    resident = guild.recommendedResident.get(self.residentNUID)
                elif self.panelType == uiConst.GUILD_RESIDENT_PANEL_HIRED:
                    resident = guild.hiredResident.get(self.residentNUID)
                elif self.panelType == uiConst.GUILD_RESIDENT_PANEL_DISPATCH:
                    resident = guild.hiredResident.get(self.residentNUID)
                if resident == None:
                    self.hide()
                    return
                baseInfo = GRTD.data.get(resident.templateId, {})
                info = {}
                info['panelType'] = self.panelType
                info['residentNUID'] = resident.nuid
                info['nameField'] = resident.name
                info['photoIcon'] = guildUtils.getPhotoPath96(baseInfo.get('icon', 0))
                _, info['qualitycolor'] = guildUtils.getResidentQuality(resident.templateId)
                info['statusStype'] = guildUtils.getStatusStypePath32(resident.statusStype)
                info['statusField'] = guildUtils.getStatusField(resident.statusType, resident.statusStype, False)
                info['propTypeField'] = gameStrings.TEXT_GUILDDISPATCHINTOPROXY_81 % Lyuba.GUILD_RESIDENT_PROP_NAME.get(baseInfo.get('propType', 0), '')
                info['propTypeFieldTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_118 % Lyuba.GUILD_RESIDENT_PROP_NAME.get(baseInfo.get('propType', 0), '')
                info['moodField'] = resident.mood
                info['moodTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_121
                info['levelField'] = resident.level
                upExp = 0 if resident.isMaxLv() else GRLD.data.get(resident.level + 1).get('upExp', 0)
                info['expField'] = 'Max' if upExp == 0 else '%d/%d' % (resident.exp, upExp)
                currentValue = 100.0
                if upExp != 0 and upExp >= resident.exp:
                    currentValue = currentValue * resident.exp / upExp
                info['expCurrentValue'] = currentValue
                info['canLvUp'] = resident.canLvUp()
                info['populationField'] = GSSD.data.get(resident.statusStype, {}).get('population', baseInfo.get('population', 0))
                jobData = GJD.data.get(resident.jobId, {})
                if resident.jobId:
                    info['locationField'] = "<font color = \'#FF8A00\'>%s-%s</font>" % (commGuild.getBuildNameByJobId(guild, resident.jobId), jobData.get('name', ''))
                else:
                    info['locationField'] = gameStrings.TEXT_GUILDRESIDENTPROXY_138
                info['bpowTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_140
                info['bagiTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_141
                info['bintTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_142
                info['bsprTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_143
                info['bpowField'] = resident.cpow
                info['bagiField'] = resident.cagi
                info['bintField'] = resident.cint
                info['bsprField'] = resident.cspr
                info['qpowTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_150
                info['qagiTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_151
                info['qintTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_152
                info['qsprTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_153
                qDict = {'S': 0,
                 'A': 0,
                 'B': 0,
                 'C': 0,
                 'D': 0,
                 'E': 0}
                info['qpowTips'] = '%.1f' % resident.qpow
                info['qpowField'], powWeight = self.getqGradeByScore(resident.qpow)
                qDict[info['qpowField']] += 1
                info['qagiTips'] = '%.1f' % resident.qagi
                info['qagiField'], agiWeight = self.getqGradeByScore(resident.qagi)
                qDict[info['qagiField']] += 1
                info['qintTips'] = '%.1f' % resident.qint
                info['qintField'], intWeight = self.getqGradeByScore(resident.qint)
                qDict[info['qintField']] += 1
                info['qsprTips'] = '%.1f' % resident.qspr
                info['qsprField'], sprWeight = self.getqGradeByScore(resident.qspr)
                qDict[info['qsprField']] += 1
                info['qevaluateField'] = self.getqevaluateGrade(qDict)
                info['qevaluateTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_170
                bevaluate = resident.cpow * powWeight + resident.cagi * agiWeight + resident.cint * intWeight + resident.cspr * sprWeight
                info['bevaluateField'] = self.getbGradeByScore(bevaluate)
                info['bevaluateTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_174
                info['salaryField'] = resident.salary
                info['salaryTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_177
                if resident.tHire == 0:
                    info['tHireTimeTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_180
                    info['tHireField'] = gameStrings.TEXT_GUILDRESIDENTPROXY_181
                else:
                    info['tHireTimeTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_183 % utils.formatDatetime(resident.tHire)[:10]
                    hireTime = p.getServerTime() - resident.tHire
                    info['tHireField'] = gameStrings.TEXT_GUILDRESIDENTPROXY_185 % int(hireTime / 86400)
                info['savvyField'] = resident.savvy
                info['savvyTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_188
                info['loyaltyField'] = '%d/%d' % (resident.loyalty, const.GUILD_MAX_LOYALTY)
                info['loyaltyTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_121
                info['tiredField'] = '%d/%d' % (resident.tired, const.GUILD_MAX_TIRED)
                info['tiredTitleTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_194
                info['tiredStateTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_196 % (commGuild.getTiredEffect(resident.tired) * 100)
                tiredType = commGuild.getTiredType(resident.tired)
                if tiredType == 0:
                    info['tiredStateField'] = gameStrings.TEXT_GUILDRESIDENTPROXY_199
                elif tiredType == 1:
                    info['tiredStateField'] = gameStrings.TEXT_GUILDRESIDENTPROXY_201
                elif tiredType == 2:
                    info['tiredStateField'] = gameStrings.TEXT_GUILDRESIDENTPROXY_203
                else:
                    info['tiredStateField'] = ''
                info['powWorkField'] = gameStrings.TEXT_GUILDRESIDENTPROXY_207 % (resident.getBaseWorkEffect(gametypes.GUILD_RESIDENT_PROP_POW) * 100)
                info['agiWorkField'] = gameStrings.TEXT_GUILDRESIDENTPROXY_208 % (resident.getBaseWorkEffect(gametypes.GUILD_RESIDENT_PROP_AGI) * 100)
                info['intWorkField'] = gameStrings.TEXT_GUILDRESIDENTPROXY_209 % (resident.getBaseWorkEffect(gametypes.GUILD_RESIDENT_PROP_INT) * 100)
                info['sprWorkField'] = gameStrings.TEXT_GUILDRESIDENTPROXY_210 % (resident.getBaseWorkEffect(gametypes.GUILD_RESIDENT_PROP_SPR) * 100)
                normalSkills = []
                famousSkills = []
                giantSkills = []
                if resident.pskills:
                    for pskill in resident.pskills.itervalues():
                        skillStatusType = resident.getPSkillStatusType(pskill.skillId)
                        if skillStatusType == gametypes.GUILD_RESIDENT_STATUS_NORMAL:
                            normalSkills.append(guildUtils.createResidentSkillInfo(pskill.skillId, pskill.level))
                        elif skillStatusType == gametypes.GUILD_RESIDENT_STATUS_FAMOUS:
                            famousSkills.append(guildUtils.createResidentSkillInfo(pskill.skillId, pskill.level))
                        elif skillStatusType == gametypes.GUILD_RESIDENT_STATUS_GIANT:
                            giantSkills.append(guildUtils.createResidentSkillInfo(pskill.skillId, pskill.level))

                info['normalSkills'] = normalSkills
                info['famousSkills'] = famousSkills
                info['giantSkills'] = giantSkills
                info['famousSkillsTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_229
                info['giantSkillsTips'] = gameStrings.TEXT_GUILDRESIDENTPROXY_230
                info['authorization'] = gameglobal.rds.ui.guild._hasPrivilege(guild.memberMe.roleId, gametypes.GUILD_ACTION_HIRE_RESIDENT)
                self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            return

    def getqevaluateGrade(self, qDict):
        grade = 'E'
        if qDict['S'] != 0:
            if qDict['S'] == 1:
                grade = gameStrings.TEXT_GUILDRESIDENTPROXY_240
            elif qDict['S'] == 2:
                grade = 'S'
            elif qDict['S'] == 3:
                grade = gameStrings.TEXT_GUILDRESIDENTPROXY_244
            else:
                grade = gameStrings.TEXT_GUILDRESIDENTPROXY_246
        elif qDict['A'] != 0:
            grade = 'A'
        elif qDict['B'] != 0:
            grade = 'B'
        elif qDict['C'] != 0:
            grade = 'C'
        elif qDict['D'] != 0:
            grade = 'D'
        return grade

    def getbGradeByScore(self, bscore):
        bScoreToGrade = GCD.data.get('bScoreToGrade', None)
        if not bScoreToGrade:
            return ''
        else:
            for i in bScoreToGrade:
                if i[0] <= bscore and bscore < i[1]:
                    return i[2]

            return ''

    def getqGradeByScore(self, qscore):
        qScoreToGrade = GCD.data.get('qScoreToGrade', None)
        if not qScoreToGrade:
            return ('E', 0)
        else:
            for i in qScoreToGrade:
                if i[0] <= qscore and qscore < i[1]:
                    return (i[2], i[3])

            return ('E', 0)

    def onChangeName(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        name = unicode2gbk(arg[3][1].GetString())
        BigWorld.player().cell.renameGuildResident(residentNUID, name)

    def onLevelUp(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        BigWorld.player().cell.upgradeGuildResident(residentNUID)

    def onRecommend(self, *arg):
        npcId = gameglobal.rds.ui.guild.residentNpcId
        if not npcId:
            return
        ent = BigWorld.entities.get(npcId)
        if not ent:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_FREE_RESIDENT_NOT_EXIST, ())
            return
        ent.cell.recommendGuildResident()
        self.hide()

    def onHire(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        BigWorld.player().cell.hireGuildResident(residentNUID)

    def onLeave(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        BigWorld.player().cell.rejectGuildResident(residentNUID)

    def onDispatch(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        gameglobal.rds.ui.guildDispatch.show(residentNUID)

    def onFire(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        msg = gameStrings.TEXT_GUILDRESIDENTPROXY_311
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.fireGuildResident, residentNUID))

    def onRest(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        guildUtils.stopWorkCheck(residentNUID)

    def onDispatchInto(self, *arg):
        residentNUID = int(arg[3][0].GetString())
        if gameglobal.rds.ui.guildDispatchInto.mediator:
            guildUtils.dispatchCheck(residentNUID, gameglobal.rds.ui.guildDispatchInto.jobId)

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (idCon[13:], idItem)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        idCon, idItem = self.getSlotID(key)
        skillLv, residentNUID = idItem.split('|')
        skillId = int(idCon)
        skillLv = int(skillLv)
        residentNUID = int(residentNUID)
        resident = None
        guild = BigWorld.player().guild
        if guild:
            if guild.recommendedResident.has_key(residentNUID):
                resident = guild.recommendedResident.get(residentNUID)
            elif guild.hiredResident.has_key(residentNUID):
                resident = guild.hiredResident.get(residentNUID)
            elif self.resident != None:
                if self.resident.nuid == residentNUID:
                    resident = self.resident
        skillInfo = guildUtils.createResidentSkillInfo(skillId, skillLv, isTips=True, resident=resident)
        return uiUtils.dict2GfxDict(skillInfo, True)
