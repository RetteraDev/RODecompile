#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSpriteGrowth.o
from gamestrings import gameStrings
import BigWorld
import gamelog
import utils
import gameglobal
from data import sprite_growth_entry_data as SGED
from cdata import sprite_growth_category_data as SGCD
from cdata import game_msg_def_data as GMDD

class ImpSpriteGrowth(object):
    """
    \xe8\x8b\xb1\xe7\x81\xb5\xe4\xbf\xae\xe7\x82\xbc
    spriteGrowthInfo\xe4\xbf\x9d\xe5\xad\x98\xe7\x9a\x84\xe8\x8b\xb1\xe7\x81\xb5\xe4\xbf\xae\xe7\x82\xbc\xe4\xbf\xa1\xe6\x81\xaf
    
    spriteGrowthInfo = {
    categoryId: {
    'scores': scores,
    'isAvailable': bool
    'entries': {
            entryId: { 'lv': lv, 'lvUpLimit': lvUpLimit, }
            }
    }
    
    [I]\xe6\x95\xb4\xe5\x9e\x8b\xe6\x95\xb0 [F]\xe6\xb5\xae\xe7\x82\xb9\xe6\x95\xb0 [S]\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2 [D]\xe5\xad\x97\xe5\x85\xb8 [T]\xe5\x85\x83\xe7\xbb\x84 [L]\xe5\x88\x97\xe8\xa1\xa8 [B]\xe5\xb8\x83\xe5\xb0\x94
    categoryId [I] \xe5\x8d\xb7ID
    scores [F] \xe5\x8d\xb7\xe8\xaf\x84\xe5\x88\x86
    entries [D] \xe4\xbf\xae\xe7\x82\xbc\xe6\x9d\xa1\xe7\x9b\xae
    entryId [I] \xe6\x9d\xa1\xe7\x9b\xaeID
    lv [I] \xe4\xbf\xae\xe7\x82\xbc\xe7\xad\x89\xe7\xba\xa7
    lvUpLimit [I] \xe5\x8f\xaf\xe4\xbf\xae\xe7\x82\xbc\xe7\xad\x89\xe7\xba\xa7\xe4\xb8\x8a\xe9\x99\x90
    """

    def updateSpriteGrowthInfo(self, dictData):
        gameStrings.TEXT_IMPSPRITEGROWTH_35
        self.spriteGrowthInfo = dictData

    def _updateSpriteGrowthCategoryScore(self, categoryId, scores):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe4\xbf\xae\xe7\x82\xbc\xe5\x88\x86\xe5\x8d\xb7\xe8\xaf\x84\xe5\x88\x86\xe4\xbf\xa1\xe6\x81\xaf
        :param categoryId: \xe5\x8d\xb7ID
        :param scores: \xe8\xaf\x84\xe5\x88\x86
        :return:
        """
        if not self.spriteGrowthInfo.has_key(categoryId):
            return
        self.spriteGrowthInfo[categoryId]['scores'] = scores

    def _updateSpriteGrowthEntry(self, categoryId, entryId, entry):
        """
        \xe6\x9b\xb4\xe6\x96\xb0\xe4\xbf\xae\xe7\x82\xbc\xe6\x9d\xa1\xe7\x9b\xae\xe4\xbf\xa1\xe6\x81\xaf
        :param categoryId: \xe5\x8d\xb7ID
        :param entryId: \xe6\x9d\xa1\xe7\x9b\xaeID
        :param entry: \xe6\x9d\xa1\xe7\x9b\xae\xe5\xad\x97\xe5\x85\xb8\xe6\x95\xb0\xe6\x8d\xae
        :return:
        """
        if not self.spriteGrowthInfo.has_key(categoryId):
            return
        if not self.spriteGrowthInfo[categoryId]['entries'].has_key(entryId):
            return
        self.spriteGrowthInfo[categoryId]['entries'][entryId].update(entry)

    def _addSpriteGrowthCategory(self, categoryId):
        gameStrings.TEXT_IMPSPRITEGROWTH_66
        if self.spriteGrowthInfo.has_key(categoryId):
            return
        self.spriteGrowthInfo[categoryId] = {'scores': 0,
         'entries': {},
         'isAvailable': True}
        entryIds = SGCD.data.get(categoryId, {}).get('entrys', ())
        for id in entryIds:
            self.spriteGrowthInfo[categoryId]['entries'][id] = {'lv': 0,
             'lvUpLimit': utils.spriteGrowthUpLimitInit(id)}

    def _updateCategoryAvailable(self, categoryIds):
        for cId, cVal in self.spriteGrowthInfo.iteritems():
            if cId in categoryIds:
                cVal['isAvailable'] = True
            else:
                cVal['isAvailable'] = False

    def onUnlockSpriteGrowthCategory(self, categoryId):
        """
        \xe8\xa7\xa3\xe9\x94\x81\xe4\xba\x86\xe4\xb8\x80\xe4\xb8\xaa\xe5\x88\x86\xe5\x8d\xb7
        :param categoryId: \xe5\x8d\xb7ID
        :return:
        """
        gamelog.debug('@zhangkuo onUnlockSpriteGrowthCategory [categoryId]', categoryId)
        self._addSpriteGrowthCategory(categoryId)
        gameglobal.rds.ui.summonedWarSpriteXiuLian.updateSpriteGrowthEntryLvUp()

    def onRaiseGrowthEntryUpLimit(self, categoryId, entryId, lvUpLimit):
        """
        \xe4\xbd\xbf\xe7\x94\xa8\xe8\x8b\xb1\xe7\x81\xb5\xe4\xbf\xae\xe7\x82\xbc\xe7\xaa\x81\xe7\xa0\xb4\xe9\x81\x93\xe5\x85\xb7\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param categoryId: \xe5\x8d\xb7ID
        :param entryId: \xe6\x9d\xa1\xe7\x9b\xaeID
        :param lvUpLimit: \xe7\xaa\x81\xe7\xa0\xb4\xe4\xb9\x8b\xe5\x90\x8e\xe7\x9a\x84\xe5\x8f\xaf\xe4\xbf\xae\xe7\x82\xbc\xe7\xad\x89\xe7\xba\xa7\xe4\xb8\x8a\xe9\x99\x90
        :return:
        """
        gamelog.debug('@zhangkuo onRaiseGrowthEntryUpLimit [categoryId][entryId][lvUpLimit]', categoryId, entryId, lvUpLimit)
        self._updateSpriteGrowthEntry(categoryId, entryId, {'lvUpLimit': lvUpLimit})
        entries = self.spriteGrowthInfo[categoryId]['entries']
        curLv = entries[entryId]['lv']
        entryName = SGED.data.get((entryId, curLv), {}).get('name', '')
        self.showGameMsg(GMDD.data.SPRITE_XIU_LIAN_GROWTH_UP_SUCCESS, (entryName, lvUpLimit))
        gameglobal.rds.ui.summonedWarSpriteXiuLian.spriteLvUpLimitSuccess(categoryId, entryId)

    def onSpriteGrowthEntryLvUp(self, categoryId, entryId, lv, scores, categoryIds):
        """
        \xe8\x8b\xb1\xe7\x81\xb5\xe4\xbf\xae\xe7\x82\xbc\xe6\x9d\xa1\xe7\x9b\xae\xe5\x8d\x87\xe7\xba\xa7\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param categoryId: \xe5\x88\x86\xe5\x8d\xb7ID
        :param entryId: \xe6\x9d\xa1\xe7\x9b\xaeID
        :param lv: \xe5\x8d\x87\xe7\xba\xa7\xe4\xb9\x8b\xe5\x90\x8e\xe8\xaf\xa5\xe6\x9d\xa1\xe7\x9b\xae\xe4\xbf\xae\xe7\x82\xbc\xe7\xad\x89\xe7\xba\xa7
        :param scores: \xe5\x8d\x87\xe7\xba\xa7\xe4\xb9\x8b\xe5\x90\x8e\xe8\xaf\xa5\xe5\x88\x86\xe5\x8d\xb7\xe7\x9a\x84\xe4\xbf\xae\xe7\x82\xbc\xe8\xaf\x84\xe5\x88\x86
        :param categoryIds: \xe5\x8d\x87\xe7\xba\xa7\xe4\xb9\x8b\xe5\x90\x8e\xe5\x8f\xaf\xe7\x94\xa8\xe7\x9a\x84\xe4\xbf\xae\xe7\x82\xbc\xe5\x8d\xb7ID
        :return:
        """
        gamelog.debug('@zhangkuo [categoryId] [entryId] [lv] [scores]', categoryId, entryId, lv, scores, categoryIds)
        entryName = SGED.data.get((entryId, lv), {}).get('name', '')
        self.showGameMsg(GMDD.data.SPRITE_XIU_LIAN_SUCCESS, (lv, entryName))
        self._updateSpriteGrowthEntry(categoryId, entryId, {'lv': lv})
        self._updateSpriteGrowthCategoryScore(categoryId, scores)
        self._updateCategoryAvailable(categoryIds)
        gameglobal.rds.ui.summonedWarSpriteXiuLian.updateSpriteGrowthEntryLvUp()

    def onRecoverSpriteGrowthEntry(self, categoryId, entryId, curLv, curLimit, scores, availableCategoryIds):
        """
        \xe8\x8b\xb1\xe7\x81\xb5\xe4\xbf\xae\xe7\x82\xbc\xe5\x9b\x9e\xe9\x80\x80\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        :param categoryId: \xe5\x88\x86\xe5\x8d\xb7ID
        :param entryId: \xe6\x9d\xa1\xe7\x9b\xaeID
        :param curLv: \xe4\xbf\xae\xe7\x82\xbc\xe7\xad\x89\xe7\xba\xa7
        :param curLimit: \xe4\xb8\x8a\xe9\x99\x90
        :param scores: \xe4\xbf\xae\xe7\x82\xbc\xe8\xaf\x84\xe5\x88\x86
        :param availableCategoryIds: \xe5\x8f\xaf\xe7\x94\xa8\xe7\x9a\x84\xe4\xbf\xae\xe7\x82\xbc\xe5\x88\x86\xe5\x8d\xb7ID
        :return:
        """
        gamelog.debug('@zhangkuo [categoryId][entryId][curLv][curLimit][scores][availableCategoryIds]', categoryId, entryId, curLv, curLimit, scores, availableCategoryIds)
        self._updateSpriteGrowthEntry(categoryId, entryId, {'lv': curLv,
         'lvUpLimit': curLimit})
        self._updateSpriteGrowthCategoryScore(categoryId, scores)
        self._updateCategoryAvailable(availableCategoryIds)
        gameglobal.rds.ui.summonedWarSpriteXiuLian.updateSpriteGrowthEntryLvUp()
