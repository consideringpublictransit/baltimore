'''
    TAZHelpers.py -- a tool for analyzing transport zone data.
    Copyright (C) 2012  Matt Jadud, Chris Plano

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# Functions to support TAZ analysis.

import sqlite3 as sql
import os, sys
import numpy

# FUNCTION
# exe :: cursor, query -> void
# PURPOSE
# Executes a query on an SQLite cursor.
def exe (cur, query):
	# The cursor gets set for data fetch.
	cur.execute(query);

# FUNCTION
def connect (db):
	conn = None
	# DB cursors
	cur = None
	try:
		conn = sql.connect('%s.sqlite' % db)
		cur = conn.cursor()
		return (conn, cur)
	except sql.Error, e:
		print "Error %s: " % e.args[0]
		sys.exit(1)

# FUNCTION
# getPossibleDestinations :: integer integer -> (list-of (list-of integers))
# PURPOSE
# Takes an origin TAZ and a travel time limit in minutes and returns a list
# of lists of all of the TAZs which can be reached via one or more public transportation links 
# in less time than the limit given.
# 
# For example, we get back:
# 
# [1, [1, 4, 9, 25, 234], ...]
#
# showing us that the TAZ number 1 has five destinations that can be reached in under the time limit.
def getPossibleDestinations (origin, limit):
	(conn, cur) = connect('time')
	# The list we return includes ourselves in the analysis.
	# This makes sense, because people might want jobs where they live.
	exe (cur, 'select desttaz, unweight from time where (unweight < %s) and (origintaz = %s)' % (limit, origin))
	dataDone = False
	count = 0
	rows = []
	# Loop through all of the data matching the query
	# one row at a time. Append all rows found to the current row list.
	while not dataDone:
		row = cur.fetchone()
		if row == None:
			dataDone = True
		else:
			rows.append(row)
			count += 1
	paths = {}
	# Append the list to that origin TAZ.
	paths[origin] = rows
	return paths


# CONTRACT
# stripBrackets :: string -> string
# PURPOSE
# Strips the square brackets from a string.
def stripBrackets (ls):
	return str(ls).strip('[]')

# CONTRACT
# nonZero :: (list-of numbers) -> number
# PURPOSE
# Counts how many values greater than zero are in a list.
def greaterThanZero(ls):
	count = 0
	for v in ls:
		if v > 0:
			count += 1
	return count

# CONTRACT
# calculateDestinationData :: (list-of (list-of numbers)) string -> tuple
# PURPOSE
# This takes in the path data from the function 'getPossibleDestinations'. So, for example, it might
# look like:
#
# [[1, [1, 4, 9, 25, 234]], ...]
#
# This function looks at the destinations, and calculates three things:
#  - The number of destinations with an above-zero density for this field (eg. for employment or food)
#  - The average density across all of the destination TAZs
#  - The standard deviation across all of the destination TAZs
#
# This then returns a Python tuple (or, a group of three values) containing those values in that order.
def calculateDestinationData (paths, field):
	(conn, cur) = connect('taz')
	# Each v is a [taz, time] from the origin
	totalDensity = []
	for k, v in paths.iteritems():
		for dest in v:
			taz = dest[0]
			time = dest[1]
			exe (cur, 'select %s from taz where taz00 = %s' % (field, taz))
			# There should only be one density value per taz00 value.
			result = cur.fetchone()
			if result:
				totalDensity.append(result[0])
	if len(totalDensity) == 0:
		return (0.0,0.0, 0.0)
	else:
		return (greaterThanZero(totalDensity), numpy.average(totalDensity), numpy.std(totalDensity))

# CONTRACT
# getIncome :: integer -> tuple
# PURPOSE
# Takes a TAZ and retrieves the average income and income quartile from the TAZ
# database for the TAZ given.
# 
# 20120425 FIXME: We no longer use the income quartile in the final analysis.
#                 This could be removed from the code, but we have not (yet)
#                 in the event that it affects other functions.
def getIncome (taz):
	(conn, cur) = connect('taz')
	exe (cur, 'select avg_med_hh_income, income_quart from taz where taz00 = %s' % taz)
	result = cur.fetchone()
	if result:
		return (float(result[0]), int(result[1]))
	else:
		return (-1.0, -1)

# CONTRACT
# getPopDens :: integer -> tuple
# PURPOSE
# Takes a TAZ and retrieves the average population density and pop. dens. quartile from the TAZ
# database for the TAZ given.
def getPopDens (taz):
	(conn, cur) = connect('taz')
	exe (cur, 'select sum_totpop, pop_dens from taz where taz00 = %s' % taz)
	result = cur.fetchone()
	if result:
		return (float(result[0]), float(result[1]))
	else:
		return (-1.0, -1.0)
