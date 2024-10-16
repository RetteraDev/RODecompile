#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\google\protobuf\internal/containers.o
"""Contains container classes to represent different protocol buffer types.

This file defines container classes which represent categories of protocol
buffer field types which need extra maintenance. Currently these categories
are:
  - Repeated scalar fields - These are all repeated fields which aren't
    composite (e.g. they are of simple types like int32, string, etc).
  - Repeated composite fields - Repeated fields which are composite. This
    includes groups and nested messages.
"""
__author__ = 'petar@google.com (Petar Petrov)'

class BaseContainer(object):
    """Base container class."""
    __slots__ = ['_message_listener', '_values']

    def __init__(self, message_listener):
        """
        Args:
          message_listener: A MessageListener implementation.
            The RepeatedScalarFieldContainer will call this object's
            Modified() method when it is modified.
        """
        self._message_listener = message_listener
        self._values = []

    def __getitem__(self, key):
        """Retrieves item by the specified key."""
        return self._values[key]

    def __len__(self):
        """Returns the number of elements in the container."""
        return len(self._values)

    def __ne__(self, other):
        """Checks if another instance isn't equal to this one."""
        return not self == other

    def __hash__(self):
        raise TypeError('unhashable object')

    def __repr__(self):
        return repr(self._values)

    def sort(self, *args, **kwargs):
        if 'sort_function' in kwargs:
            kwargs['cmp'] = kwargs.pop('sort_function')
        self._values.sort(*args, **kwargs)


class RepeatedScalarFieldContainer(BaseContainer):
    """Simple, type-checked, list-like container for holding repeated scalars."""
    __slots__ = ['_type_checker']

    def __init__(self, message_listener, type_checker):
        """
        Args:
          message_listener: A MessageListener implementation.
            The RepeatedScalarFieldContainer will call this object's
            Modified() method when it is modified.
          type_checker: A type_checkers.ValueChecker instance to run on elements
            inserted into this container.
        """
        super(RepeatedScalarFieldContainer, self).__init__(message_listener)
        self._type_checker = type_checker

    def append(self, value):
        """Appends an item to the list. Similar to list.append()."""
        self._type_checker.CheckValue(value)
        self._values.append(value)
        if not self._message_listener.dirty:
            self._message_listener.Modified()

    def insert(self, key, value):
        """Inserts the item at the specified position. Similar to list.insert()."""
        self._type_checker.CheckValue(value)
        self._values.insert(key, value)
        if not self._message_listener.dirty:
            self._message_listener.Modified()

    def extend(self, elem_seq):
        """Extends by appending the given sequence. Similar to list.extend()."""
        if not elem_seq:
            return
        new_values = []
        for elem in elem_seq:
            self._type_checker.CheckValue(elem)
            new_values.append(elem)

        self._values.extend(new_values)
        self._message_listener.Modified()

    def MergeFrom(self, other):
        """Appends the contents of another repeated field of the same type to this
        one. We do not check the types of the individual fields.
        """
        self._values.extend(other._values)
        self._message_listener.Modified()

    def remove(self, elem):
        """Removes an item from the list. Similar to list.remove()."""
        self._values.remove(elem)
        self._message_listener.Modified()

    def __setitem__(self, key, value):
        """Sets the item on the specified position."""
        self._type_checker.CheckValue(value)
        self._values[key] = value
        self._message_listener.Modified()

    def __getslice__(self, start, stop):
        """Retrieves the subset of items from between the specified indices."""
        return self._values[start:stop]

    def __setslice__(self, start, stop, values):
        """Sets the subset of items from between the specified indices."""
        new_values = []
        for value in values:
            self._type_checker.CheckValue(value)
            new_values.append(value)

        self._values[start:stop] = new_values
        self._message_listener.Modified()

    def __delitem__(self, key):
        """Deletes the item at the specified position."""
        del self._values[key]
        self._message_listener.Modified()

    def __delslice__(self, start, stop):
        """Deletes the subset of items from between the specified indices."""
        del self._values[start:stop]
        self._message_listener.Modified()

    def __eq__(self, other):
        """Compares the current instance with another one."""
        if self is other:
            return True
        if isinstance(other, self.__class__):
            return other._values == self._values
        return other == self._values


class RepeatedCompositeFieldContainer(BaseContainer):
    """Simple, list-like container for holding repeated composite fields."""
    __slots__ = ['_message_descriptor']

    def __init__(self, message_listener, message_descriptor):
        """
        Note that we pass in a descriptor instead of the generated directly,
        since at the time we construct a _RepeatedCompositeFieldContainer we
        haven't yet necessarily initialized the type that will be contained in the
        container.
        
        Args:
          message_listener: A MessageListener implementation.
            The RepeatedCompositeFieldContainer will call this object's
            Modified() method when it is modified.
          message_descriptor: A Descriptor instance describing the protocol type
            that should be present in this container.  We'll use the
            _concrete_class field of this descriptor when the client calls add().
        """
        super(RepeatedCompositeFieldContainer, self).__init__(message_listener)
        self._message_descriptor = message_descriptor

    def add(self, **kwargs):
        """Adds a new element at the end of the list and returns it. Keyword
        arguments may be used to initialize the element.
        """
        new_element = self._message_descriptor._concrete_class(**kwargs)
        new_element._SetListener(self._message_listener)
        self._values.append(new_element)
        if not self._message_listener.dirty:
            self._message_listener.Modified()
        return new_element

    def extend(self, elem_seq):
        """Extends by appending the given sequence of elements of the same type
        as this one, copying each individual message.
        """
        message_class = self._message_descriptor._concrete_class
        listener = self._message_listener
        values = self._values
        for message in elem_seq:
            new_element = message_class()
            new_element._SetListener(listener)
            new_element.MergeFrom(message)
            values.append(new_element)

        listener.Modified()

    def MergeFrom(self, other):
        """Appends the contents of another repeated field of the same type to this
        one, copying each individual message.
        """
        self.extend(other._values)

    def remove(self, elem):
        """Removes an item from the list. Similar to list.remove()."""
        self._values.remove(elem)
        self._message_listener.Modified()

    def __getslice__(self, start, stop):
        """Retrieves the subset of items from between the specified indices."""
        return self._values[start:stop]

    def __delitem__(self, key):
        """Deletes the item at the specified position."""
        del self._values[key]
        self._message_listener.Modified()

    def __delslice__(self, start, stop):
        """Deletes the subset of items from between the specified indices."""
        del self._values[start:stop]
        self._message_listener.Modified()

    def __eq__(self, other):
        """Compares the current instance with another one."""
        if self is other:
            return True
        if not isinstance(other, self.__class__):
            raise TypeError('Can only compare repeated composite fields against other repeated composite fields.')
        return self._values == other._values
