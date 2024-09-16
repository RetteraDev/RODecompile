#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaWaitProxy.o
import BigWorld
from Scaleform import GfxValue
import const
import uiConst
import gameglobal
import gamelog
import uiUtils
import formula
from ui import gbk2unicode
from uiProxy import UIProxy
SHIWU = 1
SANSHI = 2
XUEZHAN = 3
SHUANGREN = 4
A1v1 = 1
A3v3 = 2
A5v5 = 3
A2v2 = 4

class ArenaWaitProxy(UIProxy):
    INTERVAL = 5.0

    def __init__(self, uiAdapter):
        super(ArenaWaitProxy, self).__init__(uiAdapter)
        self.modelMap = {'getArenaType': self.onGetArenaType,
         'getTeamInfo': self.onGetTeamInfo}
        self.isShow = False
        self.mc = None
        self.mcLeft = None
        self.mcRight = None
        self.reset()

    def reset(self):
        self.info = None
        self.leftFlag = 0
        self.teamNum = 0

    def onGetArenaType(self, *arg):
        if self.info:
            type, vs = self.getArenaType(self.info['arenaMode'])
            return uiUtils.array2GfxAarry([type, vs])

    def getArenaType(self, mode):
        if mode == const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA:
            return (SHUANGREN, A2v2)
        if formula.isBalanceArenaMode(mode):
            return (XUEZHAN, A3v3)
        if mode == const.ARENA_MODE_SS_ROUND_1V1 or mode == const.ARENA_MODE_MS_ROUND_1V1 or mode == const.ARENA_MODE_CROSS_MS_ROUND_1V1:
            return (XUEZHAN, A1v1)
        if mode == const.ARENA_MODE_TDM_3V3 or mode == const.ARENA_MODE_CROSS_MS_TDM_3V3:
            return (SHIWU, A3v3)
        if mode == const.ARENA_MODE_TDM_5V5:
            return (SANSHI, A5v5)
        if mode == const.ARENA_MODE_ROUND_3V3_1 or mode == const.ARENA_MODE_ROUND_3V3_2 or mode == const.ARENA_MODE_CROSS_MS_ROUND_3V3 or mode == const.ARENA_MODE_CROSS_MS_ROUND_3V3_PRACTISE:
            return (XUEZHAN, A3v3)
        if mode == const.ARENA_MODE_ROUND_5V5 or mode == const.ARENA_MODE_CROSS_MS_ROUND_5V5:
            return (XUEZHAN, A5v5)
        return (0, 0)

    def onGetTeamInfo(self, *arg):
        obj = self.movie.CreateObject()
        p = BigWorld.player()
        mode = self.info['arenaMode']
        p.tempArenaInfo = self.info
        if mode in (const.ARENA_MODE_SS_ROUND_1V1, const.ARENA_MODE_MS_ROUND_1V1, const.ARENA_MODE_CROSS_MS_ROUND_1V1):
            self.teamNum = 1
        elif mode in const.ARENA_MODE_3V3 or mode in (const.ARENA_MODE_CROSS_MS_TDM_3V3,):
            self.teamNum = 3
        elif mode in (const.ARENA_MODE_TDM_5V5, const.ARENA_MODE_ROUND_5V5, const.ARENA_MODE_CROSS_MS_ROUND_5V5):
            self.teamNum = 5
        elif mode == const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA:
            self.teamNum = 2
        obj.SetMember('num', GfxValue(self.teamNum))
        leftArray = self.movie.CreateArray()
        rightArray = self.movie.CreateArray()
        array = [leftArray, rightArray]
        self.leftFlag = 0
        for key, value in self.info.items():
            if key == 'arenaMode':
                continue
            for i, item in enumerate(value):
                temp = self.movie.CreateObject()
                temp.SetMember('nameText', GfxValue(gbk2unicode(item['roleName'])))
                temp.SetMember('school', GfxValue(item['school']))
                temp.SetMember('lv', GfxValue(item['level']))
                temp.SetMember('sex', GfxValue(item['sex']))
                temp.SetMember('bodyType', GfxValue(item['bodyType']))
                temp.SetMember('arenaScore', GfxValue(item['arenaScore']))
                temp.SetMember('frameName', GfxValue(uiUtils.getArenaBadge(item['arenaScore'])))
                if item['roleName'] == p.realRoleName:
                    self.leftFlag = key
                array[key].SetElement(i, temp)

        obj.SetMember('leftArray', array[self.leftFlag])
        obj.SetMember('rightArray', array[1 - self.leftFlag])
        return obj

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ARENA_WAIT_BG:
            self.mc = mediator
        elif widgetId == uiConst.WIDGET_ARENA_WAIT_LEFT:
            self.mcLeft = mediator
        elif widgetId == uiConst.WIDGET_ARENA_WAIT_RIGHT:
            self.mcRight = mediator

    def _updateMember(self, info):
        for key, value in info.items():
            if key == 'arenaMode':
                continue
            diff = []
            for item in value:
                if item not in self.info[key]:
                    diff.append(item)

            for item in diff:
                obj = self.movie.CreateObject()
                obj.SetMember('nameText', GfxValue(gbk2unicode(item['roleName'])))
                obj.SetMember('school', GfxValue(item['school']))
                obj.SetMember('lv', GfxValue(item['level']))
                obj.SetMember('sex', GfxValue(item['sex']))
                obj.SetMember('bodyType', GfxValue(item['bodyType']))
                obj.SetMember('arenaScore', GfxValue(item['arenaScore']))
                obj.SetMember('frameName', GfxValue(uiUtils.getArenaBadge(item['arenaScore'])))
                if key == self.leftFlag:
                    obj.SetMember('isLeft', GfxValue(True))
                    if self.mcLeft:
                        self.mcLeft.Invoke('joinPlayer', obj)
                else:
                    obj.SetMember('isLeft', GfxValue(False))
                    if self.mcRight:
                        self.mcRight.Invoke('joinPlayer', obj)
                gameglobal.rds.sound.playSound(gameglobal.SD_86)

        self.info = info

    def openArenaWait(self, info):
        gamelog.debug('openArenaWait', BigWorld.player().id)
        if self.uiAdapter.quest.isShow:
            self.uiAdapter.quest.close()
        if self.isShow:
            self._updateMember(info)
        else:
            self.info = info
            self.isShow = True
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENA_WAIT_BG)
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENA_WAIT_LEFT)
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENA_WAIT_RIGHT)
            self.uiAdapter.arena.closeTips()

    def closeArenaWait(self):
        self.hide()

    def setProgress(self, value):
        if self.mc:
            self.mc.Invoke('setProgress', GfxValue(value))

    def endArenaWait(self, callback = None):
        if self.mcLeft:
            self.mcLeft.Invoke('fadeOut')
        if self.mcRight:
            self.mcRight.Invoke('fadeOut')
        if callback:
            callback()

    def clearWidget(self):
        self.isShow = False
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENA_WAIT_BG)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENA_WAIT_LEFT)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENA_WAIT_RIGHT)
        self.mc = None
        self.mcLeft = None
        self.mcRight = None

    def test(self):
        a = {0: [{'school': 7,
              'bodyType': 2,
              'level': 60,
              'arenaScore': 1388,
              'sex': 2,
              'roleName': 'sdgad'}],
         1: [],
         'arenaMode': 2}
        self.openArenaWait(a)
