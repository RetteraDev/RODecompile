#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/debateProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy
from helpers import capturePhoto
from guis import uiUtils
from data import quest_debate_data as QDD
from data import npc_model_client_data as NCD

class DebateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DebateProxy, self).__init__(uiAdapter)
        self.modelMap = {'getDebateInfo': self.onGetDebateInfo,
         'clickCloseBtn': self.onClickCloseBtn,
         'getFirstId': self.onGetFirstId}
        self.npcId = None
        self.entityId = None
        self.firstId = None
        self.modelId = 0
        self.isShow = False
        self.headGen = None

    def onGetDebateInfo(self, *arg):
        npc = BigWorld.entity(self.entityId)
        self.initHeadGen(npc)
        if len(arg) > 3:
            idx = int(arg[3][0].GetNumber())
        else:
            idx = self.firstId
        if idx == -1 or idx == -2:
            npc = BigWorld.entities.get(self.entityId)
            if npc is not None:
                npc.onShowDebateWindow(idx)
            return
        else:
            debateInfo = QDD.data[idx]
            ret = self.movie.CreateObject()
            ret.SetMember('chat', GfxValue(gbk2unicode(debateInfo['content'])))
            ret.SetMember('roleName', GfxValue(gbk2unicode(NCD.data[self.npcId]['name'])))
            ret.SetMember('title', GfxValue(gbk2unicode(gameStrings.TEXT_DEBATEPROXY_52)))
            ret.SetMember('icon', GfxValue(''))
            ret.SetMember('debateType', GfxValue(uiConst.DEBATE_MODE))
            opt = self.movie.CreateArray()
            i = 0
            if debateInfo.get('option0', None):
                ar = self.movie.CreateObject()
                ar.SetMember('name', GfxValue(gbk2unicode(debateInfo.get('option0'))))
                ar.SetMember('res', GfxValue(debateInfo.get('res0')))
                opt.SetElement(i, ar)
                i += 1
            if debateInfo.get('option1', None):
                ar = self.movie.CreateObject()
                ar.SetMember('name', GfxValue(gbk2unicode(debateInfo.get('option1'))))
                ar.SetMember('res', GfxValue(debateInfo.get('res1')))
                opt.SetElement(i, ar)
                i += 1
            if debateInfo.get('option2', None):
                ar = self.movie.CreateObject()
                ar.SetMember('name', GfxValue(gbk2unicode(debateInfo.get('option2'))))
                ar.SetMember('res', GfxValue(debateInfo.get('res2')))
                opt.SetElement(i, ar)
                i += 1
            ret.SetMember('debateOptions', opt)
            return ret

    def onGetDebateInfoPy(self, idx = 0):
        if not idx:
            idx = self.firstId
        if idx == -1 or idx == -2:
            npc = BigWorld.entities.get(self.entityId)
            if npc is not None:
                npc.onShowDebateWindow(idx)
            return
        else:
            debateInfo = QDD.data[idx]
            ret = {}
            ret['chat'] = debateInfo['content']
            ret['roleName'] = NCD.data[self.npcId]['name']
            ret['title'] = gameStrings.TEXT_DEBATEPROXY_52
            ret['icon'] = ''
            ret['debateType'] = uiConst.DEBATE_MODE
            opt = []
            if debateInfo.get('option0', None):
                ar = {}
                ar['name'] = debateInfo.get('option0')
                ar['res'] = debateInfo.get('res0')
                opt.append(ar)
            if debateInfo.get('option1', None):
                ar = {}
                ar['name'] = debateInfo.get('option1')
                ar['res'] = debateInfo.get('res1')
                opt.append(ar)
            if debateInfo.get('option2', None):
                ar = {}
                ar['name'] = debateInfo.get('option2')
                ar['res'] = debateInfo.get('res2')
                opt.append(ar)
            ret['debateOptions'] = opt
            ret['npcId'] = self.entityId
            return ret

    def onClickCloseBtn(self, *arg):
        self.closeDebatePanel()

    def openDebatePanel(self, npcId, entityId, firstId):
        self.npcId = npcId
        self.entityId = entityId
        self.firstId = firstId
        self.uiAdapter.openQuestWindow(uiConst.NPC_DEBATE)

    def closeDebatePanel(self):
        if gameglobal.rds.ui.quest.isShow:
            self.uiAdapter.closeQuestWindow()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()

    def onGetFirstId(self, *arg):
        return GfxValue(self.firstId)

    def initHeadGen(self, npc):
        if not self.headGen:
            self.headGen = capturePhoto.LargePhotoGen.getInstance('gui/taskmask.tga', 700)
        uiUtils.takePhoto3D(self.headGen, npc, npc.npcId)

    def resetHeadGen(self):
        if self.headGen:
            self.headGen.endCapture()
