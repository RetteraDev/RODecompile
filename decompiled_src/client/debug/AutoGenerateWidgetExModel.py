#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/AutoGenerateWidgetExModel.o
import Tkinter as tk
from Tkinter import *
import ttk
import tkMessageBox
import os
import sys
config = {'filePath': ''}
data = [{'type': 'UIProxy',
  'keyWords': {'类名': '{NewProxy}',
               'UIConst': '{WIDGET_NEW}'},
  'codeModel': '# -*- coding:gbk -*-\nimport BigWorld\n\nimport gameglobal\nimport uiConst\n\nfrom uiProxy import UIProxy\n\n\nclass {NewProxy}(UIProxy):\n\n    def __init__(self, uiAdapter):\n        super({NewProxy}, self).__init__(uiAdapter)\n        self.widget = None\n        self.reset()\n        uiAdapter.registerEscFunc(uiConst.{WIDGET_NEW}, self.hide)\n\n    def reset(self):\n        pass\n\n    def _registerASWidget(self, widgetId, widget):\n        if widgetId == uiConst.{WIDGET_NEW}:\n            self.widget = widget\n            self.initUI()\n            self.refreshInfo()\n\n    def clearWidget(self):\n        self.widget = None\n        self.uiAdapter.unLoadWidget(uiConst.{WIDGET_NEW})\n\n    def show(self):\n        if not self.widget:\n            self.uiAdapter.loadWidget(uiConst.{WIDGET_NEW})\n\n    def initUI(self):\n        self.widget.defaultCloseBtn = self.widget.closeBtn\n        self.widget.confirmBtn.enabled = False\n\n    def refreshInfo(self):\n        if not self.widget:\n            return\n\n    def _onConfirmBtnClick(self, e):\n        print \"onConfirmBtnClick:\", e.target, e.type\n                '}, {'type': 'UITabProxy',
  'keyWords': {'类名': '{NewTabProxy}',
               'UIConst': '{WIDGET_NEW}'},
  'codeModel': '# -*- coding:gbk -*-\nimport BigWorld\n\nimport gameglobal\nimport uiConst\n\nfrom uiTabProxy import UITabProxy\n\nTAB_ONE_IDX = 0\nTAB_TWO_IDX = 1\nclass {NewTabProxy}(UITabProxy):\n    def __init__(self, uiAdapter):\n        super({NewTabProxy}, self).__init__(uiAdapter)\n        # 默认加载swf\n\n        # 如果加载class：\n        # self.tabType = UITabProxy.TAB_TYPE_CLS\n\n        self.reset()\n        uiAdapter.registerEscFunc(uiConst.{WIDGET_NEW}, self.hide)\n\n    def reset(self):\n        super({NewTabProxy}, self).reset()\n\n    def _registerASWidget(self, widgetId, widget):\n        if widgetId == uiConst.{WIDGET_NEW}:\n            self.widget = widget\n            self.initUI()\n\n    def clearWidget(self):\n        super({NewTabProxy}, self).clearWidget()\n        self.widget = None\n        self.uiAdapter.unLoadWidget(uiConst.{WIDGET_NEW})\n\n    def _getTabList(self):\n        return [\n            {\"tabIdx\": TAB_ONE_IDX, \"tabName\": \"tabBtn0\", \"view\": \"TabOneWidget\", \"proxy\": \"tabOne\"},\n            {\"tabIdx\": TAB_TWO_IDX, \"tabName\": \"tabBtn1\", \"view\": \"TabTwoWidget\", \"proxy\": \"tabTwo\"},\n        ]\n\n        # 如果加载class\n        # return [\n        #     {\"tabIdx\": TAB_ONE_IDX, \"tabName\": \"tabBtn0\", \"view\": \"PanelMC_0\", \"pos\": (x, y)},\n        #     {\"tabIdx\": TAB_TWO_IDX, \"tabName\": \"tabBtn1\", \"view\": \"panelMC_1\", \"pos\": (x, y)},\n        # ]\n\n    def show(self):\n        self.uiAdapter.loadWidget(uiConst.{WIDGET_NEW})\n\n    def initUI(self):\n        self.widget.defaultCloseBtn = self.widget.closeBtn\n        self.initTabUI()\n        if self.showTabIndex == -1:\n            self.widget.setTabIndex(TAB_ONE_IDX)\n\n    def refreshInfo(self):\n        if not self.widget:\n            return\n\n        # swf 加载\n        proxy = self.getCurrentProxy()\n        if proxy and hasattr(proxy, \"refreshInfo\"):\n            proxy.refreshInfo()\n\n    def onTabChanged(self, *args):\n        super({NewTabProxy}, self).onTabChanged(*args)\n        self.refreshInfo()\n\n    def _onTabBtn0Click(self, e):\n        print \"onTabBtn0Click\", e.target, e.type\n        '}, {'type': 'UIPanelProxy',
  'keyWords': {'类名': '{NewPanelProxy}'},
  'codeModel': '# -*- coding:gbk -*-\nimport BigWorld\n\nimport gameglobal\nfrom uiProxy import UIProxy\n\nclass {NewPanelProxy}(UIProxy):\n\n    def __init__(self, uiAdapter):\n        super({NewPanelProxy}, self).__init__(uiAdapter)\n        self.widget = None\n\n    def reset(self):\n        pass\n\n    def initPanel(self, widget):\n        self.widget = widget\n        self.initUI()\n\n    def unRegisterPanel(self):\n        self.widget = None\n\n    def initUI(self):\n        pass\n     '}]

class AutoGenerateWidgetExModel(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.keyWordListBoxes = {}
        self.initUI()

    def onClickComfirm(self):
        model = ''
        className = ''
        for proxyData in data:
            if proxyData['type'] == self.lastSelectedProxy:
                model = proxyData['codeModel']
                className = proxyData['keyWords']['类名']
                break

        keyDic = self.keyWordListBoxes[self.lastSelectedProxy].keyEnterDic
        for key, value in keyDic.items():
            if key == className:
                className = value.get()
                className = className[0].upper() + className[1:]
            model = model.replace(key, value.get())

        filePath = config.get('filePath', '')
        if not filePath:
            filePath = os.path.split(os.path.realpath(__file__))[0]
        fileName = className[0].lower() + className[1:] + '.py'
        f = open(filePath + '\\' + fileName, 'wb')
        f.write(model.encode('gbk'))
        f.close()
        tkMessageBox.showinfo('生成成功！', '路径：' + filePath + '\\' + fileName)

    def initUI(self):
        Label(self, text='选择Proxy类型').pack()
        proxyTypes = []
        self.proxyDropDown = ttk.Combobox(self)
        self.proxyDropDown.pack()
        self.proxyDropDown.bind('<<ComboboxSelected>>', self.refreshListBox)
        for proxyData in data:
            proxyTypes.append(proxyData['type'])
            listBox = Frame(self)
            listBox.pack()
            row = 0
            listBox.keyEnterDic = {}
            for key, value in proxyData['keyWords'].items():
                label = Label(listBox, text=key)
                label.grid(row=row, column=0)
                label.pack()
                v = StringVar(listBox, value=value[1:-1])
                keyEntered = Entry(listBox, width=20, textvariable=v)
                keyEntered.grid(row=row, column=1)
                keyEntered.pack()
                listBox.keyEnterDic[value] = keyEntered
                row += 1

            self.keyWordListBoxes[proxyData['type']] = listBox
            listBox.pack_forget()

        self.proxyDropDown['values'] = proxyTypes
        self.proxyDropDown.current(0)
        self.lastSelectedProxy = self.proxyDropDown.get()
        self.keyWordListBoxes[self.lastSelectedProxy].pack()
        self.comfirm = Button(self, text='确定', command=self.onClickComfirm)
        self.comfirm.pack(side=BOTTOM)

    def refreshListBox(self, event):
        self.keyWordListBoxes[self.lastSelectedProxy].pack_forget()
        self.lastSelectedProxy = self.proxyDropDown.get()
        self.keyWordListBoxes[self.lastSelectedProxy].pack()


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    root = Tk()
    root.title('框架代码自动生成')
    root.resizable(False, False)
    model = AutoGenerateWidgetExModel(master=root)
    model.mainloop()


if __name__ == '__main__':
    main()
