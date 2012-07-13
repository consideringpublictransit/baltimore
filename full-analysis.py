import TAZHelpers as TAZ
import TAZStudyLimits as LIM
import sys

'''
######################
# FINAL DB SCHEMA
# This describes the output CSV format for the entire process.
# 
# [INTEGER] means a whole number.
# [REAL] means a decimal number.

# Source TAZ number
[INTEGER] SrcTAZ 

######################
# Origin TAZ Data
######################
# Median Income for source TAZ 
[INTEGER] MedIncSrcTAZ
# Total population in the source TAZ
[REAL] SumTotPopSrcTAZ
# Population density at source TAZ
[REAL] PopDensSrcTAZ	

# Number of destination TAZs within travel limit
[INTEGER] NumDest	

######################
# Destination TAZ(s) employment data
######################
# Number of destination TAZs that have jobs
[INTEGER] JobNum
# Job density averaged across all destination TAZs
[REAL] AvgJobDensAtDests	
# Rating (scale 1-6) of the source TAZ
# with respect to access to jobs
[INTEGER] JobDensRating	
# Standard deviation of job density across all destination TAZs
[REAL] SDJobDens	

######################
# Destination TAZ(s) supermarket data
######################
# Number of destination TAZs that have food.
[INTEGER] FoodNum	
# Food density averaged across all destination TAZs
[REAL] AvgFoodDensAtDest
# Rating (scale 1-6) of the source TAZ
# with respect to access to food
[INTEGER] FoodDensRating	
# Standard deviation of food density across all destination TAZs
[REAL] SDFoodDens	

# Sum of the job and food ratings
[INTEGER] AccessRate
'''

'''
1.	Added columns JobDensRating and FoodDensRating and AccessRate to output jobs-within-30
2.	Deleted all TAZs not in study area
a.	Study area TAZs are 1-217 and 426-767 (218-425 inclusive are missing)
3.	Rated food dens on six point scale with no outlier issues (details in spreadsheet)
(Six equal ranges from min to max.)
4.	Rated emp dens on six point scale with no outlier issues (details in spreadsheet)
(Same... take total range and divide by six.)
5.	Combined scale of 12 points by adding two separate scales together 
6.	Selected those TAZs rated 2 or 3 in overall access rating 
7.	Selected only the low income TAZs from that selection (under 185% of poverty level for 2.6 people which is $31,105.90)

GOAL: Output a sheet like 2&3 LowInc. This would then be merged in a spatial GIS package. A CSV is just fine.
'''

MAXTAZ = LIM.MAXTAZ


def outputDestinationsWithinLimit(allPaths, limit):
	global MAXTAZ
	
	# First, write out the file that contains all of the destinations
	# under this time limit.
	
	# This file creates a list of origin TAZs and all of the destinations
	# that match criteria and can be reached within the time limit. 
	# Useful for exploration (creating sample maps) and understanding
	# the implications of a low (or high) travel time limit.
	dest = open ('destinations-within-%s.csv' % limit, 'w')
	
	# If there isn't a TAZ, we should just skip it gracefully.
	for start in LIM.getStudyArea():
		paths = allPaths[start]
		if len(paths[start]) > 0:

			# Output the possible destinations
			for k, v in paths.iteritems():
				dest.write("%s, %s\n" % (start, TAZ.stripBrackets(map(lambda l: l[0], v))))
	dest.close()

def calcMaxDensity (allPaths, limit, field):
	global MAXTAZ
	max = -1
	
	# If there isn't a TAZ, we should just skip it gracefully.
	for start in LIM.getStudyArea():
		paths = allPaths[start]
		if len(paths[start]) > 0:
			(num, avg, sd) = TAZ.calculateDestinationData(paths, field)
			if avg > max:
				max = avg
	
	return max

def generateResultsTable (dbName, limit):
	global MAXTAZ
	
	print "Precalculating all paths in the transporation zone."
	counter = 0 
	allPaths = {}
	for start in LIM.getStudyArea():
		paths = TAZ.getPossibleDestinations(start, limit)
		allPaths[start] = paths
		print '.',
		counter += 1
		if counter % 10 == 0:
			print
		
		if counter % 100 == 0:
			print
	
	# 	Max avg. job density:  45242.506294
	#	Max avg. food density: 2.137048
	
	# First, generate all the destinations within the time limit.
	destinationPaths = outputDestinationsWithinLimit(allPaths, limit)
	
	# Calculate maximums
	maxAverageJobDensity = calcMaxDensity(allPaths, limit, 'emp_dens')
	maxAverageFoodDensity = calcMaxDensity(allPaths, limit, 'food_store_dens')
	
	# Calculate the ranges for the rating system.
	# Why divide by six? It worked well for separating out the data.
	# Also, ArcGIS does not do well with more than 5 or 6 colors in terms
	# of visualizing data, so we limited our categorization to six.
	jobRatingDiv = maxAverageJobDensity / 6
	foodRatingDiv = maxAverageFoodDensity / 6
	
	print
	print "Max avg. job density:  %s" % maxAverageJobDensity
	print "Max avg. food density: %s" % maxAverageFoodDensity
	print
	
	# This file holds the CSV output of our calculations. 
	final = open ('final-%s.csv' % limit, 'w')

	# Write a header to the CSV file.
	final.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % \
	('SrcTAZ', 'AccessRate', \
	'MedIncSrcTAZ', 'SumTotPopSrcTAZ', 'PopDensSrcTAZ', \
	'NumDest', \
	'JobNum',  'AvgJobDensAtDests', 'JobDensRating', 'SDJobDens', \
	'FoodNum', 'AvgFoodDensAtDest', 'FoodDensRating', 'SDFoodDens' \
	))
	
	# If there isn't a TAZ, we should just skip it gracefully.
	for start in LIM.getStudyArea():

		paths = allPaths[start]
		if len(paths[start]) > 0:

			(jobNum, jobAvg, jobSD) = TAZ.calculateDestinationData(paths, 'emp_dens')
			(foodNum, foodAvg, foodSD) = TAZ.calculateDestinationData(paths, 'food_store_dens')
			(income, income_quart) = TAZ.getIncome(start)
			(sum_totpop, pop_dens) = TAZ.getPopDens(start)
 			
			# We want a rating that is an integer value. So, we use //, which means
			# "do integer division". This means that 10 // 3 = 3.
			# However, because // does a "floor" operation (meaning, it rounds down)
			jobRating  = int(jobAvg // jobRatingDiv) + 1
			foodRating = int(foodAvg // foodRatingDiv) + 1
			accessRating = jobRating + foodRating
		 	
			if LIM.isGoodRating(accessRating) and LIM.isIncomeLimit(income):
				final.write("%i,%i,%i,%i,%.2f,%i,%i,%.2f,%i,%.2f,%i,%.2f,%i,%.2f\n" % \
					(start, accessRating, \
					income, sum_totpop, pop_dens, \
					len(paths[start]), \
					jobNum, jobAvg, jobRating, jobSD, \
					foodNum, foodAvg, foodRating, foodSD))
					
	# Cleanup nicely.
	final.close()


# We should expect the user to provide the 
# name of the database, a number of minutes, and a total access rating
# on the command line.
if len(sys.argv) == 3:
	generateResultsTable(sys.argv[1], sys.argv[2])
else:
	print "Usage:"
	print "\t python full-analysis.py <db-name> <travel-time-limit>"
