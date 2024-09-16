#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fbDeadDetailDataProxy.o
import time
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from guis import uiConst

class FbDeadDetailDataProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(FbDeadDetailDataProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'fbDeadDetailData'
        self.type = 'fbDeadDetailData'
        self.modelMap = {'getInfo': self.onGetInfo}
        self.mediator = None
        self.msgList = None
        self.maxHp = 0
        self.addHp = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FB_DEAD_DETAIL_DATA, self.hide)

    def show(self, msgList, maxHp, addHp):
        self.msgList = msgList
        self.maxHp = maxHp
        self.addHp = addHp
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FB_DEAD_DETAIL_DATA)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FB_DEAD_DETAIL_DATA:
            self.mediator = mediator

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FB_DEAD_DETAIL_DATA)

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.msgList = None
        self.maxHp = 0
        self.addHp = 0

    def onGetInfo(self, *arg):
        nowTime = self.msgList[0][0]
        gamelog.debug('jinjj---onGetInfo,msgList', self.msgList)
        msgList = self.movie.CreateArray()
        nums = 0
        for i in xrange(len(self.msgList)):
            msg = self.msgList[i]
            for item in msg[1]:
                obj = self.movie.CreateObject()
                obj.SetMember('time', GfxValue(nowTime - msg[0]))
                obj.SetMember('name', GfxValue(gbk2unicode(item[1][0] + ' ' + item[4])))
                if int(item[5]) != 0 or int(item[6]) != 0:
                    if int(item[5]) == 0:
                        obj.SetMember('status', GfxValue(0))
                        addHp = int(item[6])
                        per2 = 0
                        if self.addHp != 0:
                            per2 = '%.1f' % float(addHp * 100.0 / self.addHp)
                        addStr = '' + str(addHp) + '(' + str(per2) + '%)'
                        obj.SetMember('addAndPer', GfxValue(addStr))
                        obj.SetMember('add', GfxValue(int(item[6])))
                    else:
                        obj.SetMember('status', GfxValue(1))
                        hurt = int(item[5])
                        per1 = 0
                        if self.maxHp != 0:
                            per1 = '%.1f' % float(hurt * 100.0 / self.maxHp)
                        hurtStr = '' + str(hurt) + '(' + str(per1) + '%)'
                        obj.SetMember('hurtAndPer', GfxValue(hurtStr))
                        obj.SetMember('hurt', GfxValue(int(item[5])))
                    msgList.SetElement(nums, obj)
                    nums = nums + 1

        obj = self.movie.CreateObject()
        obj.SetMember('nowTime', GfxValue(time.strftime('%H:%M:%S', time.localtime(nowTime))))
        obj.SetMember('roleName', GfxValue(gbk2unicode(BigWorld.player().realRoleName)))
        obj.SetMember('maxHp', GfxValue(int(self.maxHp)))
        obj.SetMember('addHp', GfxValue(int(self.addHp)))
        self.mediator.Invoke('setData', obj)
        return msgList
