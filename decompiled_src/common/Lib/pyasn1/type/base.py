#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\pyasn1\type/base.o
try:
    from sys import version_info
except ImportError:
    version_info = (0, 0)

from operator import getslice, setslice, delslice
from string import join
from types import SliceType
from pyasn1.type import constraint
from pyasn1 import error

class Asn1Item:
    pass


class Asn1ItemBase(Asn1Item):
    tagSet = ()
    subtypeSpec = constraint.ConstraintsIntersection()

    def __init__(self, tagSet = None, subtypeSpec = None):
        if tagSet is None:
            self._tagSet = self.tagSet
        else:
            self._tagSet = tagSet
        if subtypeSpec is None:
            self._subtypeSpec = self.subtypeSpec
        else:
            self._subtypeSpec = subtypeSpec

    def _verifySubtypeSpec(self, value, idx = None):
        self._subtypeSpec(value, idx)

    def getSubtypeSpec(self):
        return self._subtypeSpec

    def getTagSet(self):
        return self._tagSet

    def getTypeMap(self):
        return {self._tagSet: self}

    def isSameTypeWith(self, other):
        return self is other or self._tagSet == other.getTagSet() and self._subtypeSpec == other.getSubtypeSpec()

    def isSuperTypeOf(self, other):
        """Returns true if argument is a ASN1 subtype of ourselves"""
        return self._tagSet.isSuperTagSetOf(other.getTagSet()) and self._subtypeSpec.isSuperTypeOf(other.getSubtypeSpec())


class __NoValue:

    def __getattr__(self, attr):
        raise error.PyAsn1Error('No value for %s()' % attr)


noValue = __NoValue()

class AbstractSimpleAsn1Item(Asn1ItemBase):
    defaultValue = noValue

    def __init__(self, value = None, tagSet = None, subtypeSpec = None):
        Asn1ItemBase.__init__(self, tagSet, subtypeSpec)
        if value is None or value is noValue:
            value = self.defaultValue
        if value is None or value is noValue:
            self.__hashedValue = value = noValue
        else:
            value = self.prettyIn(value)
            self._verifySubtypeSpec(value)
            self.__hashedValue = hash(value)
        self._value = value

    def __repr__(self):
        if self._value is noValue:
            return self.__class__.__name__ + '()'
        else:
            return self.__class__.__name__ + '(' + repr(self.prettyOut(self._value)) + ')'

    def __str__(self):
        return str(self._value)

    def __cmp__(self, value):
        return cmp(self._value, value)

    def __hash__(self):
        return self.__hashedValue

    def __nonzero__(self):
        if self._value:
            return 1
        else:
            return 0

    def clone(self, value = None, tagSet = None, subtypeSpec = None):
        if value is None and tagSet is None and subtypeSpec is None:
            return self
        if value is None:
            value = self._value
        if tagSet is None:
            tagSet = self._tagSet
        if subtypeSpec is None:
            subtypeSpec = self._subtypeSpec
        return self.__class__(value, tagSet, subtypeSpec)

    def subtype(self, value = None, implicitTag = None, explicitTag = None, subtypeSpec = None):
        if value is None:
            value = self._value
        if implicitTag is not None:
            tagSet = self._tagSet.tagImplicitly(implicitTag)
        elif explicitTag is not None:
            tagSet = self._tagSet.tagExplicitly(explicitTag)
        else:
            tagSet = self._tagSet
        if subtypeSpec is None:
            subtypeSpec = self._subtypeSpec
        else:
            subtypeSpec = subtypeSpec + self._subtypeSpec
        return self.__class__(value, tagSet, subtypeSpec)

    def prettyIn(self, value):
        return value

    def prettyOut(self, value):
        return str(value)

    def prettyPrint(self, scope = 0):
        return self.prettyOut(self._value)

    def prettyPrinter(self, scope = 0):
        return self.prettyPrint(scope)


class AbstractConstructedAsn1Item(Asn1ItemBase):
    componentType = None
    sizeSpec = constraint.ConstraintsIntersection()

    def __init__(self, componentType = None, tagSet = None, subtypeSpec = None, sizeSpec = None):
        Asn1ItemBase.__init__(self, tagSet, subtypeSpec)
        if componentType is None:
            self._componentType = self.componentType
        else:
            self._componentType = componentType
        if sizeSpec is None:
            self._sizeSpec = self.sizeSpec
        else:
            self._sizeSpec = sizeSpec
        self._componentValues = []

    def __repr__(self):
        r = self.__class__.__name__ + '()'
        for idx in range(len(self)):
            if self._componentValues[idx] is None:
                continue
            r = r + '.setComponentByPosition(%s, %s)' % (idx, repr(self._componentValues[idx]))

        return r

    def __cmp__(self, other):
        return cmp(self._componentValues, other)

    def getComponentTypeMap(self):
        raise error.PyAsn1Error('Method not implemented')

    def _cloneComponentValues(self, myClone, cloneValueFlag):
        pass

    def clone(self, tagSet = None, subtypeSpec = None, sizeSpec = None, cloneValueFlag = None):
        if tagSet is None:
            tagSet = self._tagSet
        if subtypeSpec is None:
            subtypeSpec = self._subtypeSpec
        if sizeSpec is None:
            sizeSpec = self._sizeSpec
        r = self.__class__(self._componentType, tagSet, subtypeSpec, sizeSpec)
        if cloneValueFlag:
            self._cloneComponentValues(r, cloneValueFlag)
        return r

    def subtype(self, implicitTag = None, explicitTag = None, subtypeSpec = None, sizeSpec = None, cloneValueFlag = None):
        if implicitTag is not None:
            tagSet = self._tagSet.tagImplicitly(implicitTag)
        elif explicitTag is not None:
            tagSet = self._tagSet.tagExplicitly(explicitTag)
        else:
            tagSet = self._tagSet
        if subtypeSpec is None:
            subtypeSpec = self._subtypeSpec
        else:
            subtypeSpec = subtypeSpec + self._subtypeSpec
        if sizeSpec is None:
            sizeSpec = self._sizeSpec
        else:
            sizeSpec = sizeSpec + self._sizeSpec
        r = self.__class__(self._componentType, tagSet, subtypeSpec, sizeSpec)
        if cloneValueFlag:
            self._cloneComponentValues(r, cloneValueFlag)
        return r

    def _verifyComponent(self, idx, value):
        pass

    def verifySizeSpec(self):
        self._sizeSpec(self)

    def getComponentByPosition(self, idx):
        raise error.PyAsn1Error('Method not implemented')

    def setComponentByPosition(self, idx, value):
        raise error.PyAsn1Error('Method not implemented')

    def getComponentType(self):
        return self._componentType

    def __getitem__(self, idx):
        return self._componentValues[idx]

    def __len__(self):
        return len(self._componentValues)

    def clear(self):
        self._componentValues = []
