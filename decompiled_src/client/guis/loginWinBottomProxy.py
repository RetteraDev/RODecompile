#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/loginWinBottomProxy.o
import BigWorld
import Sound
import events
import keys
import uiConst
import gamelog
import gameglobal
import uiUtils
import appSetting
import game
from guis import ui
from uiProxy import UIProxy
from data import producer_member_list_data as PMLD

class LoginWinBottomProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LoginWinBottomProxy, self).__init__(uiAdapter)
        self.modelMap = {'getCkBoxInfo': self.onGetCkBoxInfo,
         'clickBottomCkBox': self.onClickBottomCkBox,
         'clickBottomBtn': self.onClickBottomBtn,
         'getMemberData': self.onGetMemberData}
        self.reset()

    def reset(self):
        self.musicDisable = appSetting.Obj.get(keys.SET_LOGIN_MUSIC, 0)

    def playLoginMusic(self):
        Sound.changeZone('music/login_tianzhao', '')
        if self.musicDisable:
            Sound.enableMusic(not self.musicDisable)

    def onGetCkBoxInfo(self, *arg):
        return uiUtils.array2GfxAarry([False, self.musicDisable])

    def onGetMemberData(self, *arg):
        data = PMLD.data
        arr = []
        for id, item in data.items():
            memberItem = {}
            memberItem['jobName'] = item.get('jobName', '')
            memberItem['member'] = item.get('member', '')
            memberItem['vip'] = item.get('vip', 0)
            arr.append(memberItem)

        return uiUtils.array2GfxAarry(arr, True)

    def onClickBottomCkBox(self, *arg):
        ckName = arg[3][0].GetString()
        selected = arg[3][1].GetBool()
        gamelog.debug('onClickBottomCkBox', ckName, selected)
        if ckName == 'closeAnimationCkbox':
            pass
        elif ckName == 'closeMusicCkbox':
            self.musicDisable = int(selected)
            Sound.enableMusic(not self.musicDisable)
            appSetting.Obj[keys.SET_LOGIN_MUSIC] = self.musicDisable
            appSetting.Obj.save()

    def onClickBottomBtn(self, *arg):
        btnName = arg[3][0].GetString()
        gamelog.debug('onClickBottomBtn', btnName)
        if btnName == 'videoSettingBtn':
            gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_VIDEO)
        elif btnName == 'quitGameBtn':
            BigWorld.quit()
        elif btnName == 'cgBtn':
            game.playTitleCg(keys.SET_TITLE_CG3, 'intro_1', game.endTitleCg)
        elif btnName == 'cg0Btn':
            game.playTitleCg(keys.SET_TITLE_CG1, 'bw', game.endTitleCg)
        elif btnName == 'nameListBtn':
            self.uiAdapter.loadWidget(uiConst.WIDGET_PRODUCER_NAME_LIST)
            Sound.changeZone('music/zone/mishizhilin', '')

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_LOGIN_WIN_RIGHT_BOTTOM)
        self.uiAdapter.loadWidget(uiConst.WIDGET_LOGIN_WIN_LEFT_BOTTOM)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_LOGIN_WIN_RIGHT_BOTTOM)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_LOGIN_WIN_LEFT_BOTTOM)
        self.hideNameList()
        if gameglobal.rds.enableBinkLogoCG:
            if gameglobal.rds.loginScene.spaceID == None:
                gameglobal.rds.loginScene.loadSpace()
        else:
            game.endTitleCg(True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_PRODUCER_NAME_LIST:
            self.hideNameList()
        else:
            UIProxy._asWidgetClose(self, widgetId, multiID)

    @ui.uiEvent(uiConst.WIDGET_PRODUCER_NAME_LIST, events.EVENT_KEY_DOWN)
    def hideNameList(self, e = None):
        if e and e.data[0] != keys.KEY_ESCAPE:
            return
        if e:
            e.stop()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PRODUCER_NAME_LIST)
        if not gameglobal.rds.enableBinkLogoCG:
            Sound.changeZone(gameglobal.NEW_LOGIN_MUSIC, '')
