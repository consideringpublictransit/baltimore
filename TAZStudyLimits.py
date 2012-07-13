'''
    TAZStudyLimits.py -- a tool for analyzing transport zone data.
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

MAXTAZ = 800
	
def isIncomeLimit(income):
	if income < 31105.90:
		return True
	else:
		return False
	
# This function dictates what ratings will be 
# output to the final table.
def isGoodRating(rating):
	if (rating == 2) or (rating == 3):
		return True
	else:
		# In all other cases, return false
		return False

# This decides which TAZs are in the study.
# If this function says no, we will not use
# it in any calculations.		
def isInStudy(taz):

	if (taz >= 1) and (taz <= 217):
		return True
	elif (taz >= 426) and (taz <= 767):
		return True
	else:
		# In all other cases, return false
		return False

# This generates a list of valid TAZ zones
# based on isInStudy.
def getStudyArea ():
	valid = []
	for taz in range (1, MAXTAZ):
		if isInStudy(taz):
			valid.append(taz)
	return valid
