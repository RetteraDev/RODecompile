#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\pyasn1\type/constraint.o
"""
   ASN.1 subtype constraints classes.

   Constraints are relatively rare, but every ASN1 object
   is doing checks all the time for whether they have any
   constraints and whether they are applicable to the object.

   What we're going to do is define objects/functions that
   can be called unconditionally if they are present, and that
   are simply not present if there are no constraints.

   Original concept and code by Mike C. Fletcher.
"""
import types
import string
from pyasn1.type import error

class AbstractConstraint:
    """Abstract base-class for constraint objects
    
       Constraints should be stored in a simple sequence in the
       namespace of their client Asn1Item sub-classes.
    """

    def __init__(self, *values):
        self._valueMap = {}
        self._setValues(values)
        self.__hashedValues = None

    def __call__(self, value, idx = None):
        try:
            self._testValue(value, idx)
        except error.ValueConstraintError as why:
            raise error.ValueConstraintError('%s failed at: %s' % (self, why))

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, string.join(map(lambda x: str(x), self._values), ', '))

    def __cmp__(self, other):
        return self is other and 0 or cmp((self.__class__, self._values), other)

    def __eq__(self, other):
        return self is other or not cmp((self.__class__, self._values), other)

    def __hash__(self):
        if self.__hashedValues is None:
            self.__hashedValues = hash((self.__class__, self._values))
        return self.__hashedValues

    def _setValues(self, values):
        self._values = values

    def _testValue(self, value, idx):
        raise error.ValueConstraintError(value)

    def getValueMap(self):
        return self._valueMap

    def isSuperTypeOf(self, otherConstraint):
        return otherConstraint.getValueMap().has_key(self) or otherConstraint is self or otherConstraint == self

    def isSubTypeOf(self, otherConstraint):
        return self._valueMap.has_key(otherConstraint) or otherConstraint is self or otherConstraint == self


class SingleValueConstraint(AbstractConstraint):
    """Value must be part of defined values constraint"""

    def _testValue(self, value, idx):
        if value not in self._values:
            raise error.ValueConstraintError(value)


class ContainedSubtypeConstraint(AbstractConstraint):
    """Value must satisfy all of defined set of constraints"""

    def _testValue(self, value, idx):
        for c in self._values:
            c(value, idx)


class ValueRangeConstraint(AbstractConstraint):
    """Value must be within start and stop values (inclusive)"""

    def _testValue(self, value, idx):
        if value < self.start or value > self.stop:
            raise error.ValueConstraintError(value)

    def _setValues(self, values):
        if len(values) != 2:
            raise error.PyAsn1Error('%s: bad constraint values' % (self.__class__.__name__,))
        self.start, self.stop = values
        if self.start > self.stop:
            raise error.PyAsn1Error('%s: screwed constraint values (start > stop): %s > %s' % (self.__class__.__name__, self.start, self.stop))
        AbstractConstraint._setValues(self, values)


class ValueSizeConstraint(ValueRangeConstraint):
    """len(value) must be within start and stop values (inclusive)"""

    def _testValue(self, value, idx):
        l = len(value)
        if l < self.start or l > self.stop:
            raise error.ValueConstraintError(value)


class PermittedAlphabetConstraint(SingleValueConstraint):
    pass


class InnerTypeConstraint(AbstractConstraint):
    """Value must satisfy type and presense constraints"""

    def _testValue(self, value, idx):
        if self.__singleTypeConstraint:
            self.__singleTypeConstraint(value)
        elif self.__multipleTypeConstraint:
            if not self.__multipleTypeConstraint.has_key(idx):
                raise error.ValueConstraintError(value)
            constraint, status = self.__multipleTypeConstraint[idx]
            if status == 'ABSENT':
                raise error.ValueConstraintError(value)
            constraint(value)

    def _setValues(self, values):
        self.__multipleTypeConstraint = {}
        self.__singleTypeConstraint = None
        for v in values:
            if type(v) == types.TupleType:
                self.__multipleTypeConstraint[v[0]] = (v[1], v[2])
            else:
                self.__singleTypeConstraint = v

        AbstractConstraint._setValues(self, values)


class ConstraintsExclusion(AbstractConstraint):
    """Value must not fit the single constraint"""

    def _testValue(self, value, idx):
        try:
            self._values[0](value, idx)
        except error.ValueConstraintError:
            return

        raise error.ValueConstraintError(value)

    def _setValues(self, values):
        if len(values) != 1:
            raise error.PyAsn1Error('Single constraint expected')
        AbstractConstraint._setValues(self, values)


class AbstractConstraintSet(AbstractConstraint):
    """Value must not satisfy the single constraint"""

    def __getitem__(self, idx):
        return self._values[idx]

    def __add__(self, value):
        return self.__class__(self, value)

    def __radd__(self, value):
        return self.__class__(self, value)

    def __len__(self):
        return len(self._values)

    def _setValues(self, values):
        self._values = values
        for v in values:
            self._valueMap[v] = 1
            self._valueMap.update(v.getValueMap())


class ConstraintsIntersection(AbstractConstraintSet):
    """Value must satisfy all constraints"""

    def _testValue(self, value, idx):
        for v in self._values:
            v(value, idx)


class ConstraintsUnion(AbstractConstraintSet):
    """Value must satisfy at least one constraint"""

    def _testValue(self, value, idx):
        for v in self._values:
            try:
                v(value, idx)
            except error.ValueConstraintError:
                pass
            else:
                return

        raise error.ValueConstraintError('all of %s failed for %s' % (self._values, value))
