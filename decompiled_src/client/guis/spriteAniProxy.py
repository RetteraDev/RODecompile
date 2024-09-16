#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spriteAniProxy.o
import random
import BigWorld
import gameglobal
import uiConst
import const
import keys
import utils
from crontab import CronTab
from appSetting import Obj as AppSettings
from uiProxy import UIProxy
from uiUtils import gbk2unicode
from Scaleform import GfxValue
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import sprite_pop_data as SPD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class SpriteAniProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SpriteAniProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickSpriteAni': self.onClickSpriteAni}
        self.mediator = None
        self.notifyTimer = None
        self.msgList = []
        self.callback = None
        self.timeCallback = None
        self.curPrior = 0
        self.isOpenBloodTips = True

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        self._cycleNotify()
        self.showLeftMsg()

    def showLeftMsg(self):
        if len(self.msgList):
            msg = self.msgList[0]
            showTime = self.msgList[1]
            priority = self.msgList[2]
            self.msgList = []
            self.setPopMsg(msg, priority, showTime)
            if self.callback:
                BigWorld.cancelCallback(self.callback)
            self.callback = BigWorld.callback(showTime, Functor(self.disappear, False))

    def onClickSpriteAni(self, *arg):
        if self.mediator.Invoke('isMsgShow', ()).GetBool():
            if len(self.msgList):
                msg = self.msgList[0]
                startPos = msg.find('uiShow')
                nextMsg = msg[startPos + len('uiShow:'):]
                endPos = nextMsg.find(')')
                evalMsg = nextMsg[:endPos + 1]
                if startPos != -1:
                    eval('gameglobal.rds.ui.' + evalMsg)
                    return
        gameglobal.rds.ui.help.show()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        BigWorld.cancelCallback(self.notifyTimer)
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.msgList = []
        self.callback = None
        self.isOpenBloodTips = True
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SPRITE_ANI)

    def show(self, needSave = True):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SPRITE_ANI)
            if needSave:
                self.saveSetting(1)
            return
        self.mediator.Invoke('show')
        if needSave:
            self.saveSetting(1)
        self.showLeftMsg()

    def disappear(self, needSave = True):
        if self.mediator:
            self.mediator.Invoke('outOfStage')
            if needSave:
                self.saveSetting(0)

    def saveSetting(self, isShow):
        if int(AppSettings.get(keys.SET_UI_SPRITEANI, 1)) != isShow:
            AppSettings[keys.SET_UI_SPRITEANI] = isShow
            AppSettings.save()

    def getSetting(self):
        p = BigWorld.player()
        spriteLv = SCD.data.get('showSprite', 17)
        if p.lv < spriteLv:
            return False
        isShow = AppSettings.get(keys.SET_UI_SPRITEANI, 1)
        return isShow

    def setPopMsg(self, msg, priority = const.SPRITE_POPO_MSG_SELF, time = 5):
        if priority < self.curPrior:
            return
        self.curPrior = priority
        self.msgList = [msg, time, priority]
        if self.mediator:
            isShow = self.mediator.Invoke('isSpriteShow', ()).GetBool()
            if not isShow:
                self.show(False)
            else:
                self.mediator.Invoke('setPopMsg', (GfxValue(gbk2unicode(msg)), GfxValue(time)))
                if self.timeCallback:
                    BigWorld.cancelCallback(self.timeCallback)
                self.timeCallback = BigWorld.callback(time, self.resetPrior)
        else:
            self.show(False)

    def resetPrior(self):
        self.curPrior = 0

    def propTipMsgHp(self, old):
        p = BigWorld.player()
        spritePopHp = SCD.data.get('spritePopHp', 0.3)
        msg = None
        if p.mhp and old / float(p.mhp) >= spritePopHp and p.hp / float(p.mhp) < spritePopHp and self.isOpenBloodTips:
            msg = GMD.data.get(GMDD.data.SPRITE_POP_HP, {}).get('text', '')
        if msg:
            self.setPopMsg(msg, const.SPRITE_POPO_MSG_NORMAL)

    def propTipMsgMp(self, old):
        p = BigWorld.player()
        spritePopMp = SCD.data.get('spritePopMp', 0.3)
        msg = None
        if p.mmp and old / float(p.mmp) >= spritePopMp and p.mp / float(p.mmp) < spritePopMp:
            msg = GMD.data.get(GMDD.data.SPRITE_POP_MP, {}).get('text', '')
        if msg:
            self.setPopMsg(msg, const.SPRITE_POPO_MSG_NORMAL)

    def _cycleNotify(self):
        p = BigWorld.player()
        if not p or not p.inWorld:
            return
        nextNotifyTime = 0
        current = utils.getNow()
        findId = 0
        for notifyId, msgData in SPD.data.iteritems():
            if msgData.has_key('notifyTime'):
                if msgData['notifyTime'] - current <= 0.1:
                    findId = notifyId
                    del msgData['notifyTime']
            if msgData.has_key('notifyTime'):
                tmpNextNotifyTime = msgData['notifyTime']
            else:
                cronTime = msgData['time']
                tmpNextNotifyTime = current + CronTab(cronTime).next(utils.getNow()) + 2.0
                msgData['notifyTime'] = tmpNextNotifyTime
            if nextNotifyTime == 0 or tmpNextNotifyTime < nextNotifyTime:
                nextNotifyTime = tmpNextNotifyTime

        if findId:
            msgSet = SPD.data.get(findId).get('msgSet')
            time = SPD.data.get(findId).get('showtime', 5)
            lv = SPD.data.get(findId).get('showlv')
            msgId = random.sample(msgSet, 1)[0]
            msg = GMD.data.get(msgId, {}).get('text')
            if lv and p.lv > lv[0] and p.lv < lv[1]:
                self.setPopMsg(msg, const.SPRITE_POPO_MSG_SELF, time)
        self.notifyTimer = BigWorld.callback(nextNotifyTime - current, self._cycleNotify)

    def refreshMenu(self):
        if self.mediator:
            self.mediator.Invoke('refreshMenu', GfxValue(self.isOpenBloodTips))
