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

#systemwide modules
import os
import glob
import math
import shapelibc
import dbflibc
import sys
import getopt
import readline

#my modules
from xmlwriter import *      #AUTO_REMOVED by make
from styles import *         #AUTO_REMOVED by make


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
    print "This is shape2ge 0.1 (c) Johann Haarhoff"
    print ""
    return

def initGlobalsFromFile(filename):
    """
    At this stage we are defaulting the filename to sys.argv[1],
    but this should really be done with getopt
    """
    shpfile = shapelibc.open(str(sys.argv[1]),"rb")
    minbounds = shapelibc.ShapeFile_info(shpfile)[2]
    maxbounds = shapelibc.ShapeFile_info(shpfile)[2]
    dbffile = dbflibc.open(str(sys.argv[1]),"rb")
    numrecords = dbflibc.DBFFile_record_count(dbffile)
    numfields = dbflibc.DBFFile_field_count(dbffile)
    return

def usage():
    printBanner()
    print "This is how to use me"


def nodbf_handler():
    global numrecords
    numrecords = shapelibc.ShapeFile_info(shpfile)[0]

###############################################################################
# main 
###############################################################################

# globals
verbose = False
inputfile = ""
outputfile = ""

#parse our commandline options
try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
except getopt.GetoptError, err:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
output = None
verbose = False
for o, a in opts:
    if o == "-v":
	verbose = True
    elif o in ("-h", "--help"):
	usage()
	sys.exit()
    elif o in ("-o", "--output"):
	outputfile = a
    else:
	assert False, "unhandled option"


#if no outputfile was specced, give it a name
if outputfile == "":
    outputfile = "shape2ge-conf.xml"


#try and figure out what was passed to us
#if we were passed something with a .shp extension, try and find a dbf
#if not, try and find a .shp and a dbf
inputfile = args[0]

#if the dude added the .shp we strip it
if inputfile[-4:0].upper() == ".SHP":
    inputfile = inputfile[:len(inputfile)-4]

#see if we can open it
try:
    shpfile = shapelibc.open(inputfile,"rb")
except IOError,err:
    #if we cannot open the shpfile we should die
    print str(err)
    sys.exit(2)

#we got this far, now try the dbf

nodbf=False
try:
    dbffile = dbflibc.open(inputfile,"rb")
except IOError,err:
    print """You did not supply a dbf file, all objects of the same type
    will be considered equal."""
    nodbf = True

# find out how many records we have
# if there is a dbf file we will consider it authorative
if nodbf == True:
    #do the whole thing for no dbf
    nodbf_handler()
    sys.exit(0)

numrecords = dbflibc.DBFFile_record_count(dbffile)
numfields = dbflibc.DBFFile_field_count(dbffile)

print "I found " + str(numfields) + " fields in the dbf file."
print "These are the field descriptions as they appear in"
print "the file."
print ""

for i in range(0,numfields):
    print str(i) + ": " + str(dbflibc.DBFFile_field_info(dbffile,i)[1])

print ""
print "Could you tell me which field refers to the type of"
print "feature you would like to split the data by. You will"
print "be able to assign different styles to features split "
print "in this step"

feattype = sanitizeIntFromKeyboard(raw_input("Which field refers to the feature type: "),0,30000)[1]

features = []

for i in range(0,numrecords):
    features.append(dbflibc.DBFFile_read_attribute(dbffile,i,feattype))

uniqfeatures = set(features)
uniqfeatures = sorted(uniqfeatures)

print "I found the following unique feature types in the file:"
print ""
for i,feat in enumerate(uniqfeatures):
    print str(i) + ": " + str(feat)

print "we will now proceed to create styles for these feature types"

stylelist = {}
for i,feat in enumerate(uniqfeatures):
    feat = str(feat).replace(" ","_")
    count = 0
    for j in range(0,numrecords):
	currentfeat = dbflibc.DBFFile_read_attribute(dbffile,j,feattype)
	if currentfeat == feat:
	    count = j
	    break

    shpobj = shapelibc.ShapeFile_read_object(shpfile,count)
    shptype = shapelibc.SHPObject_type_get(shpobj)

    if shptype in [shapelibc.SHPT_ARCZ,shapelibc.SHPT_ARC]:
	#make linestyle
	stylelist[feat] = []
	print str(feat)+" is an ARC, we are making a LineStyle..."
	color = raw_input("Give me the color quadlet (e.g. FF0000FF): ")
	colorMode = raw_input("Give me the color mode (e.g. normal): ")
	width = sanitizeFloatFromKeyboard(raw_input("Give me the line width (0.0-4.0): "),0,4)[1]
	stylelist[feat].append(LineStyle(color,colorMode,width))
    elif shptype in [shapelibc.SHPT_POLYGONZ,shapelibc.SHPT_POLYGON]:
	#make linestyle
	stylelist[feat] = []
	print str(feat)+""" is a POLY, we are making a LineStyle & PolyStyle...
	LineStyle first..."""
	color = raw_input("Give me the color quadlet (e.g. FF0000FF): ")
	colorMode = raw_input("Give me the color mode (e.g. normal): ")
	width = sanitizeFloatFromKeyboard(raw_input("Give me the line width (0.0-4.0): "),0,4)[1]
	stylelist[feat].append(LineStyle(color,colorMode,width))
	#make polystyle
	print "Now the PolyStyle..."
	color = raw_input("Give me the color quadlet (e.g. FF0000FF): ")
	colorMode = raw_input("Give me the color mode (e.g. normal): ")
	fill = sanitizeIntFromKeyboard(raw_input("Do you want the poly filled? (0:No 1:Yes): "),0,1)[1]
	outline = sanitizeIntFromKeyboard(raw_input("Do you want the poly outlined? (0:No 1:Yes): "),0,1)[1]
	stylelist[feat].append(PolyStyle(color,colorMode,fill,outline))
    elif shptype in [shapelibc.SHPT_POINTZ,shapelibc.SHPT_POINT]:
	#make iconstyle
	pass
    
kmlfile = open(outputfile,"w")
kmlwriter = BetterXMLWriter(kmlfile,"    ")
kmlwriter.startDocument()
kmlwriter.openElement("shp2kml")
kmlwriter.openElement("styles")

for s in stylelist.iteritems():
    kmlwriter.openElement("Style",{"id":s[0]})
    for j in s[1]:
	j.toKML(kmlfile)
    kmlwriter.closeLast()

kmlwriter.closeLast()
kmlwriter.openElement("feattype")
kmlwriter.openElement("feat_id")
kmlwriter.addData(str(feattype))
kmlwriter.closeLast()
kmlwriter.openElement("feat_name")
kmlwriter.addData("unknown")
kmlwriter.closeLast()
kmlwriter.closeLast()


x_scale = sanitizeFloatFromKeyboard(raw_input("What is the lattitude (x) Scale? : "),0,99999)[1]
y_scale = sanitizeFloatFromKeyboard(raw_input("What is the longitude (y) Scale? : "),0,99999)[1]

kmlwriter.openElement("scale")
kmlwriter.openElement("x_scale")
kmlwriter.addData(str(x_scale))
kmlwriter.closeLast()
kmlwriter.openElement("y_scale")
kmlwriter.addData(str(y_scale))
kmlwriter.closeLast()
kmlwriter.closeLast()

x_offset = sanitizeFloatFromKeyboard(raw_input("What is the lattitude (x) offset? : "),-99999,99999)[1]
y_offset = sanitizeFloatFromKeyboard(raw_input("What is the longitude (y) offset? : "),-99999,99999)[1]

kmlwriter.openElement("offset")
kmlwriter.openElement("x_offset")
kmlwriter.addData(str(x_offset))
kmlwriter.closeLast()
kmlwriter.openElement("y_offset")
kmlwriter.addData(str(y_offset))
kmlwriter.closeLast()
kmlwriter.closeLast()

kmlwriter.endDocument()
