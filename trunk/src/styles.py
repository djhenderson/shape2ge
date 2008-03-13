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

#my modules
from xmlwriter import *            #AUTO_REMOVED by make

class Icon():
    def __init__(self,href=''):
	self._href = href

    def getIcon(self):
	return self._href

    def setIcon(self,href):
	self._href = href

    def toKML(self,out,indentstr = '\t'):
	kmlwriter = BetterXMLWriter(out,indentstr)
	kmlwriter.openElement("Icon")
	kmlwriter.openElement("href")
	kmlwriter.addData(str(self._href))
	kmlwriter.closeLast()
	kmlwriter.closeLast()

class hotspot():

    def __init__(self,x=0,y=0,xunits="pixels",yunits="pixels"):
	self._x = x
	self._y = y
	self._xunits = xunits
	self._yunits = yunits

    def getX(self):
	return self._x

    def setX(self,x):
	self._x = x

    def getY(self):
	return self._y

    def setY(self,y):
	self._y = y

    def getXunits(self):
	return self._xunits

    def setXunits(self,x):
	self._xunits = xunits

    def getYunits(self):
	return self._yunits

    def setYunits(self,y):
	self._yunits = yunits

    def toKML(self,out,indentstr = '\t'):
	kmlwriter = BetterXMLWriter(out,indentstr)
	kmlwriter.openElement("hotspot",{"x":str(self._x),"y":str(self._y),"xunits":str(self._xunits),"yunits":str(self._yunits)})

class ColorStyle():

    def __init__(self,color="",colorMode=""):
	self._color = color
	self._colorMode = colorMode

    def getColor(self):
	return self._color

    def setColor(self,color):
	self._color = color

    def getColorMode(self):
	return self._colorMode

    def setColorMode(self,colorMode):
	self._colorMode = colorMode

class IconStyle(ColorStyle):

    def __init__(self,color="",colorMode="",scale="",heading="",theIcon=Icon(),thehotspot=hotspot()):
	self._color = color
	self._colorMode = colorMode
	self._scale = scale
	self._heading = heading
	self._Icon = theIcon
	self._hotspot = thehotspot

    def getScale(self):
	return self._scale

    def setScale(self,scale):
	self._scale = scale

    def getIcon(self):
	return self._Icon

    def setIcon(self,theIcon):
	self._Icon = theIcon

    def getHeading(self):
	return self._heading

    def setHeading(self,heading):
	self._Icon = theIcon

    def getHotspot(self):
	return self._hotspot

    def setHotspot(self,thehotspot):
	self._hotspot = thehotspot

    def toKML(self,out,indentstr = '\t'):
	kmlwriter = BetterXMLWriter(out,indentstr)
	kmlwriter.openElement("IconStyle")
	kmlwriter.openElement("color")
	kmlwriter.addData(str(self._color))
	kmlwriter.closeLast()
	kmlwriter.openElement("colorMode")
	kmlwriter.addData(str(self._colorMode))
	kmlwriter.closeLast()
	kmlwriter.openElement("scale")
	kmlwriter.addData(str(self._scale))
	kmlwriter.closeLast()
	kmlwriter.openElement("heading")
	kmlwriter.addData(str(self._heading))
	kmlwriter.closeLast()
	self._Icon.toKML(out,indentstr)
	self._hotspot.toKML(out,indentstr)
	kmlwriter.closeLast()

class LabelStyle(ColorStyle):

    def __init__(self,color="",colorMode="",scale=""):
	self._color = color
	self._colorMode = colorMode
	self._scale = scale

    def getScale(self):
	return self._scale

    def setScale(self,scale):
	self._scale = scale

    def toKML(self,out,indentstr = '\t'):
	kmlwriter = BetterXMLWriter(out,indentstr)
	kmlwriter.openElement("LabelStyle")
	kmlwriter.openElement("color")
	kmlwriter.addData(str(self._color))
	kmlwriter.closeLast()
	kmlwriter.openElement("colorMode")
	kmlwriter.addData(str(self._colorMode))
	kmlwriter.closeLast()
	kmlwriter.openElement("scale")
	kmlwriter.addData(str(self._scale))
	kmlwriter.closeLast()
	kmlwriter.closeLast()

class LineStyle(ColorStyle):

    def __init__(self,color="",colorMode="",width=""):
	self._color = color
	self._colorMode = colorMode
	self._width = width

    def getWidth(self):
	return self._width

    def setWidth(self,width):
	self._width = width

    def toKML(self,out,indentstr = '\t'):
	kmlwriter = BetterXMLWriter(out,indentstr)
	kmlwriter.openElement("LineStyle")
	kmlwriter.openElement("color")
	kmlwriter.addData(str(self._color))
	kmlwriter.closeLast()
	kmlwriter.openElement("colorMode")
	kmlwriter.addData(str(self._colorMode))
	kmlwriter.closeLast()
	kmlwriter.openElement("width")
	kmlwriter.addData(str(self._width))
	kmlwriter.closeLast()
	kmlwriter.closeLast()

class PolyStyle(ColorStyle):

    def __init__(self,color="",colorMode="",fill="",outline=""):
	self._color = color
	self._colorMode = colorMode
	self._fill = fill
	self._outline = outline

    def getFill(self):
	return self._fill

    def setFill(self,fill):
	self._fill = fill

    def getOutline(self):
	return self._outline

    def setOutline(self,outline):
	self._outline = outline

    def toKML(self,out,indentstr = '\t'):
	kmlwriter = BetterXMLWriter(out,indentstr)
	kmlwriter.openElement("PolyStyle")
	kmlwriter.openElement("color")
	kmlwriter.addData(str(self._color))
	kmlwriter.closeLast()
	kmlwriter.openElement("colorMode")
	kmlwriter.addData(str(self._colorMode))
	kmlwriter.closeLast()
	kmlwriter.openElement("fill")
	kmlwriter.addData(str(self._fill))
	kmlwriter.closeLast()
	kmlwriter.openElement("outline")
	kmlwriter.addData(str(self._outline))
	kmlwriter.closeLast()
	kmlwriter.closeLast()
