#Embedded file name: I:/bag/tmp/tw2/res/entities\client/iDisplay.o
import BigWorld
import const
import gametypes
import gameglobal

class IDisplay(object):

    def getOpacityValue(self):
        if not self.inWorld:
            return (gameglobal.OPACITY_HIDE, False)
        if getattr(self, 'IsAvatar', False):
            return (gameglobal.OPACITY_FULL, True)
        player = BigWorld.player()
        if self.visibility == const.VISIBILITY_HIDE:
            return (gameglobal.OPACITY_HIDE, False)
        if hasattr(self, 'validInBianyao'):
            if self._invisiableOnYaoli():
                return (gameglobal.OPACITY_HIDE, False)
        visibleGroupNUID = getattr(self, 'visibleGroupNUID', 0)
        visibleGbId = getattr(self, 'visibleGbId', 0)
        if visibleGroupNUID > 0 or visibleGbId > 0:
            if visibleGroupNUID > 0 and visibleGroupNUID == player.groupNUID or visibleGbId > 0 and visibleGbId == player.gbId:
                return (gameglobal.OPACITY_FULL, True)
            else:
                return (gameglobal.OPACITY_HIDE, False)
        return (gameglobal.OPACITY_FULL, True)

    def _invisiableOnYaoli(self):
        player = BigWorld.player()
        return self.validInBianyao == gametypes.FUNCTION_INVALID_FOR_YAO and player._isInBianyao() or self.validInBianyao == gametypes.FUNCTION_VALID_ONLY_FOR_YAO and not player._isInBianyao()

    def set_visibility(self, old):
        self.refreshOpacityState()
