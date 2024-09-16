#Embedded file name: /WORKSPACE/data/entities/client/helpers/guitextfactory.o
import BigWorld
import GUI

class GUITextFactory(object):

    def __init__(self, cacheSize = 100):
        self.guiTextCache = []
        self.allCacheSize = cacheSize
        self.curIdx = -1

    def getGUIText(self):
        self.curIdx += 1
        if self.curIdx >= self.allCacheSize:
            self.curIdx = 0
        if len(self.guiTextCache) <= self.curIdx:
            guiText = GUI.Text('0')
            self.guiTextCache.append(guiText)
            return guiText
        else:
            return self.guiTextCache[self.curIdx]
