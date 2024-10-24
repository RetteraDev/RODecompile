#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\xml\sax/__init__.o
"""Simple API for XML (SAX) implementation for Python.

This module provides an implementation of the SAX 2 interface;
information about the Java version of the interface can be found at
http://www.megginson.com/SAX/.  The Python version of the interface is
documented at <...>.

This package contains the following modules:

handler -- Base classes and constants which define the SAX 2 API for
           the 'client-side' of SAX for Python.

saxutils -- Implementation of the convenience classes commonly used to
            work with SAX.

xmlreader -- Base classes and constants which define the SAX 2 API for
             the parsers used with SAX for Python.

expatreader -- Driver that allows use of the Expat parser with SAX.
"""
from xmlreader import InputSource
from handler import ContentHandler, ErrorHandler
from _exceptions import SAXException, SAXNotRecognizedException, SAXParseException, SAXNotSupportedException, SAXReaderNotAvailable

def parse(source, handler, errorHandler = ErrorHandler()):
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    parser.parse(source)


def parseString(string, handler, errorHandler = ErrorHandler()):
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

    if errorHandler is None:
        errorHandler = ErrorHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    inpsrc = InputSource()
    inpsrc.setByteStream(StringIO(string))
    parser.parse(inpsrc)


default_parser_list = ['xml.sax.expatreader']
_false = 0
if _false:
    import xml.sax.expatreader
import os, sys
if 'PY_SAX_PARSER' in os.environ:
    default_parser_list = os.environ['PY_SAX_PARSER'].split(',')
del os
_key = 'python.xml.sax.parser'
if sys.platform[:4] == 'java' and sys.registry.containsKey(_key):
    default_parser_list = sys.registry.getProperty(_key).split(',')

def make_parser(parser_list = []):
    """Creates and returns a SAX parser.
    
    Creates the first parser it is able to instantiate of the ones
    given in the list created by doing parser_list +
    default_parser_list.  The lists must contain the names of Python
    modules containing both a SAX parser and a create_parser function."""
    for parser_name in parser_list + default_parser_list:
        try:
            return _create_parser(parser_name)
        except ImportError as e:
            import sys
            if parser_name in sys.modules:
                raise
        except SAXReaderNotAvailable:
            pass

    raise SAXReaderNotAvailable('No parsers found', None)


if sys.platform[:4] == 'java':

    def _create_parser(parser_name):
        from org.python.core import imp
        drv_module = imp.importName(parser_name, 0, globals())
        return drv_module.create_parser()


else:

    def _create_parser(parser_name):
        drv_module = __import__(parser_name, {}, {}, ['create_parser'])
        return drv_module.create_parser()


del sys
