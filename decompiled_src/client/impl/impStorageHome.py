#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impStorageHome.o
import gamelog
import gameglobal

class ImpStorageHome(object):

    def inv2StorageHomeRes(self, isOK, srcPage, srcPos, srcIt, dstPage, dstPos, dstIt, newVersion):
        gamelog.debug('@yj .. inv2StorageHomeRes', isOK, srcPage, srcPos, srcIt, dstPage, dstPos, dstIt, newVersion)
        stroageVersion = gameglobal.rds.ui.homeTermsStorage.getStorageVersion()
        curPage = gameglobal.rds.ui.homeTermsStorage.getPage()
        gamelog.debug('@yj .. inv2StorageHomeRes_curStroageVersion_And_curPage', stroageVersion, curPage)
        if isOK:
            if stroageVersion + 1 == newVersion:
                gameglobal.rds.ui.homeTermsStorage.setStorageVersion(newVersion)
                gameglobal.rds.ui.homeTermsStorage.updateItem(dstIt, dstPage, dstPos)
                if dstIt:
                    gameglobal.rds.ui.inventory.addItem(srcIt, srcPage, srcPos)
                else:
                    gameglobal.rds.ui.inventory.removeItem(srcPage, srcPos)
            else:
                self._doPullStorageHomePageInfo(curPage, newVersion - 1)
        elif stroageVersion != newVersion:
            self._doPullStorageHomePageInfo(curPage, newVersion - 1)

    def storageHome2InvRes(self, isOK, srcPage, srcPos, srcIt, dstPage, dstPos, dstIt, newVersion):
        gamelog.debug('@yj .. storageHome2InvRes', isOK, srcPage, srcPos, srcIt, dstPage, dstPos, dstIt, newVersion)
        stroageVersion = gameglobal.rds.ui.homeTermsStorage.getStorageVersion()
        curPage = gameglobal.rds.ui.homeTermsStorage.getPage()
        gamelog.debug('@yj .. storageHome2InvRes_curStroageVersion_And_curPage', stroageVersion, curPage)
        if isOK:
            if stroageVersion + 1 == newVersion:
                gameglobal.rds.ui.homeTermsStorage.setStorageVersion(newVersion)
                if dstIt:
                    gameglobal.rds.ui.inventory.addItem(dstIt, dstPage, dstPos)
                else:
                    gameglobal.rds.ui.inventory.removeItem(dstPage, dstPos)
                gameglobal.rds.ui.homeTermsStorage.updateItem(srcIt, srcPage, srcPos)
            else:
                self._doPullStorageHomePageInfo(curPage, newVersion - 1)
        elif stroageVersion != newVersion:
            self._doPullStorageHomePageInfo(curPage, newVersion - 1)

    def storageHomeChangePosRes(self, isOK, srcPage, srcPos, srcIt, dstPage, dstPos, dstIt, newVersion):
        gamelog.debug('@yj .. storageHomeChangePosRes', isOK, srcPage, srcPos, srcIt, dstPage, dstPos, dstIt, newVersion)
        stroageVersion = gameglobal.rds.ui.homeTermsStorage.getStorageVersion()
        curPage = gameglobal.rds.ui.homeTermsStorage.getPage()
        gamelog.debug('@yj .. storageHomeChangePosRes_curStroageVersion_And_curPage', stroageVersion, curPage)
        if isOK:
            if stroageVersion + 1 == newVersion:
                gameglobal.rds.ui.homeTermsStorage.setStorageVersion(newVersion)
                gameglobal.rds.ui.homeTermsStorage.updateItem(dstIt, dstPage, dstPos)
                gameglobal.rds.ui.homeTermsStorage.updateItem(srcIt, srcPage, srcPos)
            else:
                self._doPullStorageHomePageInfo(curPage, newVersion - 1)
        elif stroageVersion != newVersion:
            self._doPullStorageHomePageInfo(curPage, newVersion - 1)

    def onGetStorageHomePageInfo(self, isOK, allPageCnt, curPage, itemsList, version):
        gamelog.debug('@yj .. onGetStorageHomePageInfo', isOK, allPageCnt, curPage, itemsList, version)
        if isOK:
            self.bRefresh = False
            gameglobal.rds.ui.homeTermsStorage.show(curPage, itemsList, version)
        elif not getattr(self, 'bRefresh', False) and version != 0:
            self.bRefresh = True
            gameglobal.rds.ui.homeTermsStorage.setStorageVersion(0)
            self._doPullStorageHomePageInfo(curPage, 0)
        else:
            gameglobal.rds.ui.homeTermsStorage.setStorageVersion(0)
            gamelog.error('@yj .. onGetStorageHomePageInfo .. error', isOK, allPageCnt, curPage, itemsList, version)

    def _doInv2StorageHome(self, srcPage, srcPos, srcAmount, dstPage, dstPos, cipher, version):
        gamelog.debug('@yj .. inv2StorageHome', srcPage, srcPos, srcAmount, dstPage, dstPos, cipher, version)
        self.cell.inv2StorageHome(srcPage, srcPos, srcAmount, dstPage, dstPos, cipher, version)

    def _doStorageHome2Inv(self, srcPage, srcPos, srcAmount, dstPage, dstPos, cipher, version):
        gamelog.debug('@yj .. storageHome2Inv', srcPage, srcPos, srcAmount, dstPage, dstPos, cipher, version)
        self.cell.storageHome2Inv(srcPage, srcPos, srcAmount, dstPage, dstPos, cipher, version)

    def _doSortStorageHome(self):
        self.cell.sortStorageHome()

    def _doPullStorageHomePageInfo(self, page, version):
        gamelog.debug('@yj .. pullStorageHome', page, version)
        self.cell.pullStorageHome(page, version)

    def _doStorageHomeChangePos(self, srcPage, srcPos, srcAmount, dstPage, dstPos, version):
        gamelog.debug('@yj .. storageHomeChangePos', srcPage, srcPos, srcAmount, dstPage, dstPos, version)
        self.cell.storageHomeChangePos(srcPage, srcPos, srcAmount, dstPage, dstPos, version)
