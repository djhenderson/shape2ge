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

from math import sqrt,acos,pi
from random import uniform
import decimal
from decimal import Decimal

def dot(vec1,vec2):
    return sum(x*y for x,y in zip(vec1,vec2))

def cross(vec1,vec2):
    """
    2d vectors only
    this tells us whether the direction vector
    is in or out of the 2d plane
    """
    #for 2d stuff, the first two terms dissapear, leaving us
    #only with the "z" term
    #return [(vec1[1]*0 - 0*vec2[1]), (0*vec2[0] - vec1[0]*0), (vec1[0]*vec2[1]-vec1[1]*vec2[0])]
    return (vec1[0]*vec2[1]-vec1[1]*vec2[0])

def magnitude(vec1):
    """
    2d vectors only
    """
    return sqrt(vec1[0]**2 + vec1[1]**2)

def unit_vec(vec1):
    return [vec1[0]/magnitude(vec1),vec1[1]/magnitude(vec1)]

def winding_number(poly):
    """
    poly is a [[x1,y1],[x2,y2]...,[x1,y1]]
    """
    #compute extents
    xmin = poly[0][0];
    ymin = poly[0][1];
    xmax = poly[0][0];
    ymax = poly[0][1];
    for i,j in poly:
	if i < xmin:
	    xmin = i;
	elif i > xmax:
	    xmax = i;

	if j < ymin:
	    ymin = j;
	elif j > ymax:
	    ymax = j;

    p = [0,0]
    angle = 0

    while Decimal(str(angle/(2*pi))).quantize(Decimal('1.'), rounding=decimal.ROUND_HALF_UP) == Decimal(0):
	# now we must try and find a point inside the polygon,
	# we do this by shooting a random point within the
	# extents
	p[0] = uniform(xmin,xmax)
	p[1] = uniform(ymin,ymax)
	angle = 0
	for i in range(0,len(poly) - 1):
	    vec1 = [poly[i][0] - p[0],poly[i][1] - p[1]]
	    vec2 = [poly[i+1][0] - p[0],poly[i+1][1] - p[1]]
	    dir = cross(vec1,vec2)
	    dp = dot(unit_vec(vec1),unit_vec(vec2))
	    # this next if is to handle precision errors
	    # since acos barfs on anything just slightly
	    # out of range
	    if dp > 1:
		dp = 1
	    elif dp < -1:
		dp = -1
	    newangle = acos(dp)
	    if dir > 0:
		newangle = -newangle
	    angle = angle + newangle
	    
    return Decimal(str(angle/(2*pi))).quantize(Decimal('1.'), rounding=decimal.ROUND_HALF_UP)
    
