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

###############################################################################
# imports
###############################################################################

#global modules
import os
import glob
import math
import shapelibc
import dbflibc
from xml.dom import minidom
import xml.dom
import sys
import getopt

#my modules
from xmlwriter import *           #AUTO_REMOVED by make
from styles import *              #AUTO_REMOVED by make
from shapeobjects import *        #AUTO_REMOVED by make

###############################################################################
# global vars
###############################################################################

# these are filled from the shapefile
numrecords = 0
numfields = 0
minbounds = 0
maxbounds = 0
shpfile = None	    # global shapefile object
dbffile	= None    # global dbffile object
configfile = ""
outputfile = ""

# these are filled by the user or config file
x_offset = 0   # shapefile x offset relative to earth coords
y_offset = 0   # shapefile y offset relative to earth coords
z_offset = 0
x_scale = 1.0    # shapefile x scale to get to proper earth coords
y_scale = 1.0    # shapefile y scale to get to proper earth coords
z_scale = 1.0
feattype = 0	    # field num for differentiating different styles
featname = ""
verbose = False	    #verbose output

# these are derived from other conditions
configfile = ""
noconfig = False
nodbf = False

stylelist = {}

###############################################################################
# utility functions 
###############################################################################

def sanitizeIntFromKeyboard(s,range_start=0,range_end=0):
    """
    input sanitazation, makes sure that whatever is passed in s is an int in the
    range given
    """
    try:
	x = int(s)
    except ValueError:
	err = 1
	return err,0

    if (x >= range_start) and (x <= range_end):
	err = 0
        return err,x
    else:
	err = 1
	return err,x

def sanitizeFloatFromKeyboard(s,range_start=0,range_end=0):
    """
    input sanitazation, makes sure that whatever is passed in s is a float in the
    range given
    """
    try:
	x = float(s)
    except ValueError:
	err = 1
	return err,0

    if (x >= range_start) and (x <= range_end):
	err = 0
        return err,x
    else:
	err = 1
	return err,x

def sanitizeStrFromKeyboard(s):
    return str(s)

###############################################################################
# program functions 
###############################################################################

def printBanner():
    print "This is shape2ge 0.1 (c) Johann Haarhoff 2008"
    print ""
    return

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def usage():
    printBanner()

def parseCommandLine():
    global configfile
    global outputfile
    global noconfig
    global nodbf
    global shpfile
    global dbffile
    global verbose
    try:
	opts, args = getopt.getopt(sys.argv[1:], "hc:o:v", ["help", "configfile=" ,"output=", "verbose"])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            outputfile = a
	elif o in ("-c", "--config"):
	    configfile = a
        else:
            assert False, "unhandled option"

    if configfile == "":
	noconfig = True;

    #try and figure out what was passed to us
    #if we were passed something with a .shp extension, try and find a dbf
    #if not, try and find a .shp and a dbf
    inputfile = args[0]

    #if the dude added the .shp we strip it
    if inputfile[-4:0].upper() == ".SHP":
	inputfile = inputfile[:len(inputfile)-4]

    #if no outputfile was specced, give it a name
    outputfile = inputfile + ".kml"

    #see if we can open it
    try:
	shpfile = shapelibc.open(inputfile,"rb")
    except IOError,err:
	#if we cannot open the shpfile we should die
	print str(err)
	sys.exit(2)

    #we got this far, now try the dbf

    try:
	dbffile = dbflibc.open(inputfile,"rb")
    except IOError,err:
	print """You did not supply a dbf file, all objects of the same type
	will be considered equal."""
	nodbf = True


def parseConfigFile(filename):
    global x_offset   # shapefile x offset relative to earth coords
    global y_offset   # shapefile y offset relative to earth coords
    global z_offset   # shapefile z offset relative to earth coords
    global x_scale    # shapefile x scale to get to proper earth coords
    global y_scale    # shapefile y scale to get to proper earth coords
    global z_scale    # shapefile z scale to get to proper earth coords
    global feattype	    # field num for differentiating different styles
    global featname	    # field num for differentiating different styles
    global stylelist

    #fill a dict with styles
    dom = minidom.parse(filename)
    styl = dom.getElementsByTagName("styles")
    for st in styl:
	for style in st.getElementsByTagName("Style"):
	    id = style.getAttribute("id")
	    stylelist[id] = []
	    lstyles = style.getElementsByTagName("LineStyle")
	    for l in lstyles:
		tmp = l.getElementsByTagName("color")
		color = getText(tmp[0].childNodes)
		tmp = l.getElementsByTagName("colorMode")
		colorMode = getText(tmp[0].childNodes)
		tmp = l.getElementsByTagName("width")
		width = getText(tmp[0].childNodes)
		stylelist[id].append(LineStyle(color,colorMode,width))

	    pstyles = style.getElementsByTagName("PolyStyle")
	    for l in pstyles:
		tmp = l.getElementsByTagName("color")
		color = getText(tmp[0].childNodes)
		tmp = l.getElementsByTagName("colorMode")
		colorMode = getText(tmp[0].childNodes)
		tmp = l.getElementsByTagName("fill")
		fill = getText(tmp[0].childNodes)
		tmp = l.getElementsByTagName("outline")
		outline = getText(tmp[0].childNodes)
		stylelist[id].append(PolyStyle(color,colorMode,fill,outline))

    #get the feat type and name
    feat = dom.getElementsByTagName("feattype")
    for f in feat:
	tmp = f.getElementsByTagName("feat_id")
	feattype = int(getText(tmp[0].childNodes))
	tmp = f.getElementsByTagName("feat_name")
	featname = getText(tmp[0].childNodes)

    #get the offset and scales
    offsets = dom.getElementsByTagName("offset")
    for offset in offsets:
	tmp = offset.getElementsByTagName("x_offset")
	x_offset = float(getText(tmp[0].childNodes))
	tmp = offset.getElementsByTagName("y_offset")
	y_offset = float(getText(tmp[0].childNodes))

    scales = dom.getElementsByTagName("scale")
    for scale in scales:
	tmp = scale.getElementsByTagName("x_scale")
	x_scale = float(getText(tmp[0].childNodes))
	tmp = scale.getElementsByTagName("y_scale")
	y_scale = float(getText(tmp[0].childNodes))

    return

def getGlobalsFromShapeFile():
    global minbounds
    global maxbounds
    global numrecords
    minbounds = shapelibc.ShapeFile_info(shpfile)[2]
    maxbounds = shapelibc.ShapeFile_info(shpfile)[2]
    if nodbf:
	numrecords = shapelibc.ShapeFile_info(file)[0] 
    else:
        numrecords = dbflibc.DBFFile_record_count(dbffile)
    

def initGlobals():
    """
    parse the commandline, and see if we can open the conf and shp files
    """
    parseCommandLine()
    if not noconfig:
        parseConfigFile(configfile)
    getGlobalsFromShapeFile()

    

###############################################################################
# main 
###############################################################################

#offset_x = -0.000162
#offset_y = -0.000045

initGlobals()

kmlfile = open(outputfile,"w")
kmlwriter = BetterXMLWriter(kmlfile,"    ")
kmlwriter.startDocument()
kmlwriter.openElement("kml")
kmlwriter.openElement("Document")

#outputting styles

for s in stylelist.iteritems():
    kmlwriter.openElement("Style",{"id":s[0]})
    for j in s[1]:
	j.toKML(kmlfile)
    kmlwriter.closeLast()

#create a list of specobs
s = []
features = []
for i in range(0,numrecords):
    shpobj = SHPObject()
    shpobj.createFromFile(shpfile,i)
    shpobj.makeDescriptionFromFile(dbffile,i)
    s = castSpecific(shpobj)
    s._Label = "Shape Nr. "+str(i)
    
    features.append(dbflibc.DBFFile_read_attribute(dbffile,i,feattype))

    #scale first then offset
    if len(s._Verts[0][0]) == 2: 
	for p_index,p in enumerate(s._Verts):
	    for n_index,n in enumerate(s._Verts[p_index]):
		s._Verts[p_index][n_index] = ((s._Verts[p_index][n_index][0]*x_scale)+x_offset,
						(s._Verts[p_index][n_index][1]*y_scale)+y_offset)
    elif len(s._Verts[0][0]) > 2: 
	for p_index,p in enumerate(s._Verts):
	    for n_index,n in enumerate(s._Verts[p_index]):
		s._Verts[p_index][n_index] = ((s._Verts[p_index][n_index][0]*x_scale)+x_offset,
						(s._Verts[p_index][n_index][1]*y_scale)+y_offset,
						(s._Verts[p_index][n_index][2]*z_scale)+z_offset)

    #output the KML
    s.toKML(kmlfile,styleUrl="#"+str(features[i]).replace(" ","_"),indentstr = "    ")

kmlwriter.endDocument()
    
