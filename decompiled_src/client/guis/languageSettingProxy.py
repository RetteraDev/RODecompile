#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/languageSettingProxy.o
import locale
import uiConst
import keys
import gamelog
import gameglobal
from guis import uiUtils
from uiProxy import UIProxy
from appSetting import Obj as AppSettings
from cdata import game_msg_def_data as GMDD
ALL_LANGUAGE = ['fr',
 'en',
 'de',
 'it',
 'tr',
 'pl',
 'es',
 'zh']

class LanguageSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LanguageSettingProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_LANGUAGE_SETTING, self.hide)

    def show(self, *args):
        if not gameglobal.rds.configData.get('enableChatMultiLanguage', False):
            return False
        self.uiAdapter.loadWidget(uiConst.WIDGET_LANGUAGE_SETTING)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_LANGUAGE_SETTING)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_LANGUAGE_SETTING:
            self.widget = widget
            self.initUI()

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        val = locale.getdefaultlocale()
        lan = val[0] if val else 'en'
        currentSetting = AppSettings.get(keys.SET_CHAT_LANGUAGES, lan)
        for l in ALL_LANGUAGE:
            gamelog.debug('zhp@LanguageSettingProxy.initUI', l, lan, currentSetting)
            getattr(self.widget, '%sBox' % l).selected = l in currentSetting

    def _onConfirmBtnClick(self, e):
        selectLan = []
        for l in ALL_LANGUAGE:
            if getattr(self.widget, '%sBox' % l).selected:
                selectLan.append(l)

        if selectLan:
            AppSettings[keys.SET_CHAT_LANGUAGES] = ','.join(selectLan)
            AppSettings.save()
            self.hide()
        else:
            txt = uiUtils.getTextFromGMD(GMDD.data.LANGUAGE_SETTING_IS_NONE)
            self.uiAdapter.messageBox.showAlertBox(txt)

    def checkSetting(self):
        if not gameglobal.rds.configData.get('enableChatMultiLanguage', False):
            return
        if not AppSettings.get(keys.SET_CHAT_LANGUAGES, ''):
            self.show()
