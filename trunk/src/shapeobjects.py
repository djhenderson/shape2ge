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

#global modules
import shapelibc
import dbflibc
import sys

#my modules
from xmlwriter import *        #AUTO_REMOVED by make
from vec import *              #AUTO_REMOVED by make

def castSpecific(shpobj):
    """
    if given a SHPObject, this will return a more
    specific version like SHPPointObject depending
    on the SHPType of the given object
    """
    if shpobj._SHPType == shapelibc.SHPT_POINT:
	obj = SHPPointObject()
	obj.createFromObject(shpobj)
	return obj
    elif shpobj._SHPType == shapelibc.SHPT_ARCZ:
	obj = SHPArcZObject()
	obj.createFromObject(shpobj)
	return obj
    elif shpobj._SHPType == shapelibc.SHPT_ARC:
	obj = SHPArcObject()
	obj.createFromObject(shpobj)
	return obj
    elif shpobj._SHPType == shapelibc.SHPT_POLYGONZ:
	obj = SHPPolygonZObject()
	obj.createFromObject(shpobj)
	return obj
    elif shpobj._SHPType == shapelibc.SHPT_POLYGON:
	obj = SHPPolygonObject()
	obj.createFromObject(shpobj)
	return obj
    

class WrongShapeObjectError(Exception):
    """
    Thrown when trying to instantiate say a
    SHPPointOPbject from file, and the file
    returns a different type
    """
    pass

class SHPObject():

    def __init__(self,SHPType = shapelibc.SHPT_NULL,SHPId = -1,Verts = [[]],Label="",Desc = ""):
	self._SHPType = SHPType
	self._SHPId = SHPId
	self._Verts = Verts
	self._Label = Label
	self._Desc = Desc

    def createFromFile(self,filestream,shapenum):
	"""
	The filestream should already be opened
	with shapelibc.open() before calling this
	"""
	shp = shapelibc.ShapeFile_read_object(filestream,shapenum)
	SHPObject.__init__(self,shapelibc.SHPObject_type_get(shp),
			    shapelibc.SHPObject_id_get(shp),
			    shapelibc.SHPObject_vertices(shp))

    def makeDescriptionFromFile(self,filestream,shapenum):
	"""
	The filestream should already be opened
	with dbflibc.open() before calling this
	"""
	numfields = dbflibc.DBFFile_field_count(filestream) 
	for i in range(0,numfields):
	    field_name = str(dbflibc.DBFFile_field_info(filestream,i)[1]).upper()
	    field_data = str(dbflibc.DBFFile_read_attribute(filestream,shapenum,i)).lower()
	    self._Desc = self._Desc + "<b>" + field_name + ": </b>" + field_data + "<br>"

class SHPPointObject(SHPObject):

    def __init__(self,SHPId = -1,Verts = [[]],Label="",Desc=""):
	SHPObject.__init__(self,shapelibc.SHPT_POINT,SHPId,Verts,Label,Desc)

    def createFromFile(self,filestream,shapenum):
	SHPObject.createFromFile(self,filestream,shapenum)
	if self._SHPType != shapelibc.SHPT_POINT:
	    raise WrongShapeObjectError()

    def createFromObject(self,shpobject):
	if shpobject._SHPType != shapelibc.SHPT_POINT:
	    raise WrongShapeObjectError()
	SHPPointObject.__init__(self,shpobject._SHPId,shpobject._Verts,shpobject._Label,shpobject._Desc)

    def toKML(self,out,styleUrl="",indentstr = '\t'):
	kmlwriter = BetterXMLWriter(out,indentstr)
	kmlwriter.openElement("Placemark")
	kmlwriter.openElement("name")
	if self._Label == "":
	    kmlwriter.addData(str(self._SHPId))
	else:
	    kmlwriter.addData(str(self._Label))
	kmlwriter.closeLast()
	kmlwriter.openElement("styleUrl")
	kmlwriter.addData(str(styleUrl))
	kmlwriter.closeLast()
	kmlwriter.openElement("description")
	kmlwriter.addCData(self._Desc)
	kmlwriter.closeLast()
	kmlwriter.openElement("Point")
	kmlwriter.openElement("coordinates")
	for i,j in self._Verts:
	    kmlwriter.addData(str(i)+","+str(j)+",0 ")

	kmlwriter.endDocument()

class SHPArcZObject(SHPObject):

    def __init__(self,SHPId = -1,Verts = [[]],Label="",Desc=""):
	SHPObject.__init__(self,shapelibc.SHPT_ARCZ,SHPId,Verts,Label,Desc)

    def createFromFile(self,filestream,shapenum):
	SHPObject.createFromFile(self,filestream,shapenum)
	if self._SHPType != shapelibc.SHPT_ARCZ:
	    raise WrongShapeObjectError()

    def createFromObject(self,shpobject):
	if shpobject._SHPType != shapelibc.SHPT_ARCZ:
	    raise WrongShapeObjectError()
	SHPArcZObject.__init__(self,shpobject._SHPId,shpobject._Verts,shpobject._Label,shpobject._Desc)

    def toKML(self,out,styleUrl="",indentstr = '\t'):
	kmlwriter = BetterXMLWriter(out,indentstr)
	kmlwriter.openElement("Placemark")
	kmlwriter.openElement("name")
	if self._Label == "":
	    kmlwriter.addData(str(self._SHPId))
	else:
	    kmlwriter.addData(str(self._Label))
	kmlwriter.closeLast()
	kmlwriter.openElement("styleUrl")
	kmlwriter.addData(str(styleUrl))
	kmlwriter.closeLast()
	kmlwriter.openElement("description")
	kmlwriter.addCData(self._Desc)
	kmlwriter.closeLast()
	kmlwriter.openElement("LineString")
	kmlwriter.openElement("tessellate")
	kmlwriter.addData("1")
	kmlwriter.closeLast()
	kmlwriter.openElement("coordinates")
	#shapelibc does not populate _Verts properly, 
	#so we need to check for the Z coordinate
	#even if this is an ArcZ
	if len(self._Verts[0][0]) == 2: 
	    #we only have x and y
	    for i,j in self._Verts[0]:
		kmlwriter.addData(str(i)+","+str(j)+",0 ")
	elif len(self._Verts[0][0]) == 3:
	    #we have x, y and z
	    for i,j,k in self._Verts[0]:
		kmlwriter.addData(str(i)+","+str(j)+","+str(k)+" ")
	elif len(self._Verts[0][0]) == 4:
	    #we have x,y,z and m
	    #I don't know what to do with m at this stage
	    for i,j,k,l in self._Verts[0]:
		kmlwriter.addData(str(i)+","+str(j)+","+str(k)+" ")

	kmlwriter.endDocument()

class SHPArcObject(SHPArcZObject):

    def __init__(self,SHPId = -1,Verts = [[]],Label="",Desc=""):
	SHPObject.__init__(self,shapelibc.SHPT_ARC,SHPId,Verts,Label,Desc)

    def createFromFile(self,filestream,shapenum):
	SHPObject.createFromFile(self,filestream,shapenum)
	if self._SHPType != shapelibc.SHPT_ARC:
	    raise WrongShapeObjectError()

    def createFromObject(self,shpobject):
	if shpobject._SHPType != shapelibc.SHPT_ARC:
	    raise WrongShapeObjectError()
	SHPArcObject.__init__(self,shpobject._SHPId,shpobject._Verts,shpobject._Label,shpobject._Desc)

class SHPPolygonZObject(SHPObject):

    def __init__(self,SHPId = -1,Verts = [[]],Label="",Desc=""):
	SHPObject.__init__(self,shapelibc.SHPT_POLYGONZ,SHPId,Verts,Label,Desc)

    def createFromFile(self,filestream,shapenum):
	SHPObject.createFromFile(self,filestream,shapenum)
	if self._SHPType != shapelibc.SHPT_POLYGONZ:
	    raise WrongShapeObjectError()

    def createFromObject(self,shpobject):
	if shpobject._SHPType != shapelibc.SHPT_POLYGONZ:
	    raise WrongShapeObjectError()
	SHPPolygonZObject.__init__(self,shpobject._SHPId,shpobject._Verts,shpobject._Label,shpobject._Desc)

    def toKML(self,out,styleUrl="",indentstr = '\t'):
	kmlwriter = BetterXMLWriter(out,indentstr)
	kmlwriter.openElement("Placemark")
	kmlwriter.openElement("name")
	if self._Label == "":
	    kmlwriter.addData(str(self._SHPId))
	else:
	    kmlwriter.addData(str(self._Label))
	kmlwriter.closeLast()
	kmlwriter.openElement("styleUrl")
	kmlwriter.addData(str(styleUrl))
	kmlwriter.closeLast()
	kmlwriter.openElement("description")
	kmlwriter.addCData(self._Desc)
	kmlwriter.closeLast()
	kmlwriter.openElement("Polygon")
	kmlwriter.openElement("extrude")
	kmlwriter.addData("0")
	kmlwriter.closeLast()
	kmlwriter.openElement("tessellate")
	kmlwriter.addData("1")
	kmlwriter.closeLast()
	#polygons may have multiple parts
	#in the shapefile, a part is an outer boundary if the
	#poly is wound clockwise, and an inner boundary if it
	#is wound anticlockwise.
	#we use winding_number in vec.py to figure this out

	for part,coords in enumerate(self._Verts):
	    dir = winding_number(coords)   #winding_number is from vec.py
	    if dir > 0:
		kmlwriter.openElement("outerBoundaryIs")
	    elif dir < 0:
		kmlwriter.openElement("innerBoundaryIs")

	    kmlwriter.openElement("LinearRing")
	    kmlwriter.openElement("coordinates")
	    #shapelibc does not populate _Verts properly, 
	    #so we need to check for the Z coordinate
	    #even if this is a PolygonZ
	    if len(self._Verts[part][0]) == 2: 
		#we only have x and y
		for i,j in self._Verts[part]:
		    kmlwriter.addData(str(i)+","+str(j)+",0 ")
	    elif len(self._Verts[part][0]) == 3:
		#we have x, y and z
		for i,j,k in self._Verts[part]:
		    kmlwriter.addData(str(i)+","+str(j)+","+str(k)+" ")
	    elif len(self._Verts[part][0]) == 4:
		#we have x,y,z and m
		#I don't know what to do with m at this stage
		for i,j,k,l in self._Verts[part]:
		    kmlwriter.addData(str(i)+","+str(j)+","+str(k)+" ")

	    kmlwriter.closeLast() #coordinates
	    kmlwriter.closeLast() #LinearRing
	    kmlwriter.closeLast() #outer/innerBoudary


	kmlwriter.endDocument()

class SHPPolygonObject(SHPPolygonZObject):
    def __init__(self,SHPId = -1,Verts = [[]],Label="",Desc=""):
	SHPObject.__init__(self,shapelibc.SHPT_POLYGON,SHPId,Verts,Label,Desc)

    def createFromFile(self,filestream,shapenum):
	SHPObject.createFromFile(self,filestream,shapenum)
	if self._SHPType != shapelibc.SHPT_POLYGON:
	    raise WrongShapeObjectError()

    def createFromObject(self,shpobject):
	if shpobject._SHPType != shapelibc.SHPT_POLYGON:
	    raise WrongShapeObjectError()
	SHPPolygonObject.__init__(self,shpobject._SHPId,shpobject._Verts,shpobject._Label,shpobject._Desc)

