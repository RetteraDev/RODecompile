#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\google\protobuf/descriptor_database.o
"""Provides a container for DescriptorProtos."""
__author__ = 'matthewtoia@google.com (Matt Toia)'

class DescriptorDatabase(object):
    """A container accepting FileDescriptorProtos and maps DescriptorProtos."""

    def __init__(self):
        self._file_desc_protos_by_file = {}
        self._file_desc_protos_by_symbol = {}

    def Add(self, file_desc_proto):
        """Adds the FileDescriptorProto and its types to this database.
        
        Args:
          file_desc_proto: The FileDescriptorProto to add.
        """
        self._file_desc_protos_by_file[file_desc_proto.name] = file_desc_proto
        package = file_desc_proto.package
        for message in file_desc_proto.message_type:
            self._file_desc_protos_by_symbol.update(((name, file_desc_proto) for name in _ExtractSymbols(message, package)))

        for enum in file_desc_proto.enum_type:
            self._file_desc_protos_by_symbol['.'.join((package, enum.name))] = file_desc_proto

    def FindFileByName(self, name):
        """Finds the file descriptor proto by file name.
        
        Typically the file name is a relative path ending to a .proto file. The
        proto with the given name will have to have been added to this database
        using the Add method or else an error will be raised.
        
        Args:
          name: The file name to find.
        
        Returns:
          The file descriptor proto matching the name.
        
        Raises:
          KeyError if no file by the given name was added.
        """
        return self._file_desc_protos_by_file[name]

    def FindFileContainingSymbol(self, symbol):
        """Finds the file descriptor proto containing the specified symbol.
        
        The symbol should be a fully qualified name including the file descriptor's
        package and any containing messages. Some examples:
        
        'some.package.name.Message'
        'some.package.name.Message.NestedEnum'
        
        The file descriptor proto containing the specified symbol must be added to
        this database using the Add method or else an error will be raised.
        
        Args:
          symbol: The fully qualified symbol name.
        
        Returns:
          The file descriptor proto containing the symbol.
        
        Raises:
          KeyError if no file contains the specified symbol.
        """
        return self._file_desc_protos_by_symbol[symbol]


def _ExtractSymbols(desc_proto, package):
    """Pulls out all the symbols from a descriptor proto.
    
    Args:
      desc_proto: The proto to extract symbols from.
      package: The package containing the descriptor type.
    
    Yields:
      The fully qualified name found in the descriptor.
    """
    message_name = '.'.join((package, desc_proto.name))
    yield message_name
    for nested_type in desc_proto.nested_type:
        for symbol in _ExtractSymbols(nested_type, message_name):
            yield symbol

        for enum_type in desc_proto.enum_type:
            yield '.'.join((message_name, enum_type.name))
