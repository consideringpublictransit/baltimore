
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
