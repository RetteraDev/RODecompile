#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bookProxy.o
from uiProxy import UIProxy
import gameglobal
from guis import uiConst
from guis import uiUtils
from data import book_content_data as BCD
from Scaleform import GfxValue
from ui import gbk2unicode
BOOK_TYPE = 1
PICTURE_TYPE = 2

class BookProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BookProxy, self).__init__(uiAdapter)
        self.modelMap = {'initContent': self.initContent,
         'getContent': self.onGetContent,
         'getFormat': self.onGetFormat,
         'getType': self.onGetType}
        self.bookId = -1
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_BOOK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BOOK:
            self.mediator = mediator

    def show(self, bookId):
        if self.bookId != bookId:
            self.bookId = bookId
            self.initContent()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BOOK)

    def getContent(self, page = 1):
        pageList = BCD.data.get(self.bookId, [])
        contentList = []
        pageSet = set()
        for pageData in pageList:
            if pageData.get('Page', 0) == page:
                contentList.append(pageData)
            pageSet.add(pageData.get('Page', 0))

        contentList.sort(cmp=lambda a, b: cmp(a.get('MultiContent', 0), b.get('MultiContent', 0)))
        return (contentList, len(pageSet))

    def initContent(self, *arg):
        ret = []
        if self.bookId != -1:
            contentList, totalPage = self.getContent()
            if len(contentList) == 0:
                return
            picName = contentList[0].get('PicName', None)
            bType = PICTURE_TYPE if picName and gameglobal.rds.configData.get('enableBookPictureShow', False) else BOOK_TYPE
            title = contentList[0].get('Name', '')
            if len(contentList) == 1:
                content = contentList[0].get('Content', '')
            else:
                content = [ d.get('Content', '') for d in contentList ]
            picStr = 'book/%s' % contentList[0].get('PicName', '1.dds')
            ret = [self.bookId,
             1,
             totalPage,
             title,
             content,
             bType,
             picStr]
            if self.mediator != None:
                self.mediator.Invoke('setContent', uiUtils.array2GfxAarry(ret, True))

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BOOK)

    def onGetContent(self, *arg):
        page = int(arg[3][1].GetNumber())
        contentList, pageSize = self.getContent(page)
        if len(contentList) == 1:
            content = contentList[0]['Content']
            return GfxValue(gbk2unicode(content))
        else:
            content = [ d['Content'] for d in contentList ]
            return uiUtils.array2GfxAarry(content, True)

    def onGetFormat(self, *args):
        format = {}
        page = int(args[3][0].GetNumber())
        contentList, pageSize = self.getContent(page)
        if len(contentList) == 1:
            format['letterSpacing'] = contentList[0].get('letterSpacing', 1)
            format['indent'] = contentList[0].get('indent', 0)
            format['leading'] = contentList[0].get('leading', 15)
            format['align'] = contentList[0].get('align', 'justify')
            return uiUtils.dict2GfxDict(format)
        else:
            formatList = []
            for content in contentList:
                format = {}
                format['letterSpacing'] = content.get('letterSpacing', 1)
                format['indent'] = content.get('indent', 0)
                format['leading'] = content.get('leading', 15)
                format['align'] = content.get('align', 'justify')
                formatList.append(format)

            return uiUtils.array2GfxAarry(formatList)

    def onGetType(self, *args):
        pageList = BCD.data.get(self.bookId, [])
        if pageList:
            return GfxValue(pageList[0].get('displayType', 1))
        return GfxValue(1)
