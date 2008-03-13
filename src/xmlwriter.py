###############################################################################
# Copyright (C) 2008 Johann Haarhoff <johann.haarhoff@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of Version 2 of the GNU General Public License as
# published by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
###############################################################################
#
# Originally written:
#    2008      Johann Haarhoff, <johann.haarhoff@gmail.com>
# Modifications:
#
###############################################################################

import sys, string

from xml.sax import saxutils, handler, make_parser

#
#  define the errors we use
#

class Error(Exception):
    """
    Just Extending Exception
    """
    pass

class OutOfOrderError(Error):
    """
    Thrown when you close a xml tag before
    all its children are closed
    """
    pass

class TagNotOpenError(Error):
    """
    Thrown when trying to close a tag that is
    not open
    """

class BasicXMLWriter(handler.ContentHandler):
    """
    This just inherits from handler.ContentHandler and
    allows basic output with indents etc.
    """

    def __init__(self, out = sys.stdout,indentstr = '\t'):
        handler.ContentHandler.__init__(self)
        self._out = out
	self._indentlevel = 0
	self._printnl = 1
	self._indentstr = indentstr

    # ContentHandler methods

    def startDocument(self):
        self._out.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')

    def startElement(self, name, attrs):
        self._out.write('\n'+self._indentstr*self._indentlevel + '<' + name)
        for (name, value) in attrs.items():
            self._out.write(' %s="%s"' % (name, saxutils.escape(value)))
        self._out.write('>')
	self._indentlevel = self._indentlevel + 1

    def endElement(self, name):
	self._indentlevel = self._indentlevel - 1

	if self._printnl:
            self._out.write('\n' + self._indentstr*self._indentlevel + '</%s>' % name)
	else:
            self._out.write('</%s>' % name)

	self._printnl=1

    def characters(self, content):
        self._out.write(saxutils.escape(content))
	self._printnl = 0;

    def ignorableWhitespace(self, content):
        self._out.write(content)

    def processingInstruction(self, target, data):
        self._out.write('<?%s %s?>' % (target, data))


class BetterXMLWriter(BasicXMLWriter):
    """
    This makes life a bit easier by making sure the xml
    is relatively intact, it checks for closing tags
    out of order, and closing tags that have not been
    opened
    It also overrides endDocument to close the remaining
    open tags in the correct order.
    """

    def __init__(self, out = sys.stdout,indentstr = '\t'):
        BasicXMLWriter.__init__(self,out,indentstr)
	self._openElements = []

    def openElement(self,name,attrs={}):
	self.startElement(name,attrs)
	self._openElements.append(name)

    def closeLast(self):
	"""
	Closes the last open tag
	"""
	self.endElement(self._openElements.pop())

    def closeElement(self,name):
	if not (name in self._openElements):
	    raise TagNotOpenError()
	    #print 'TagNotOpenError()'
	elif not (name == self._openElements[len(self._openElements)-1]):
	    raise OutOfOrderError()
	    #print 'OutOfOrderError()'
	else:
	    self.endElement(name)
	    self._openElements.pop()

    def addData(self,content):
	"""
        this is truly just here because i think addData()
	is more descriptive than characters
	"""
	self.characters(content)

    def addCData(self,content):
	"""
	allows us to add CDATA sections
	"""
	self._out.write('<![CDATA[')
        self._out.write(content)
	self._out.write(']]>')


    def endDocument(self):
	for i in range(0,len(self._openElements)):
	    self.endElement(self._openElements.pop())


