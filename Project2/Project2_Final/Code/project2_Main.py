##############################################################################################
#CS325 - Project 2
#Contributors - Cierra Shawe, Grant Smith, Gerald Gale
#Instructions: 
#	- README.txt contains all of the instructions needed to run this file successfully 
#	- This file will run both any type of change funcion you need, including accuracy tests, 
#	- and experimental tests for data 
##############################################################################################
import sys
import os.path
import time
import random 
import csv
import math
import re

sys.setrecursionlimit(10000)
#########################
# START - Algorithms
#########################

#############################
#Algorithm 1 - Slow
#############################
# 	+ Helper Function: Handles the recursive calls externally for Change_Slow

def changeSlow(array, change):
	solution = []
	result  = []
	for i in range(0,len(array)+1):
		solution.append(0)
	
	minChange = change
	print change/array[-1]
	
	for i in range(0, change/array[-1]+1): #1
		for j in range(0, change/array[-2]+1):#2
				for k in range(0, change/array[-3]+1):#3
					for l in range(0, change/array[-4]+1):#4
						if len(array) >= 5:
							for m in range(0, change/array[-5]+1):#5
								if (i*array[4] + j*array[3]+ k*array[2]+l*array[1]+m*array[0]) == change:
									solution[0] = m
									solution[1] = l
									solution[2] = k
									solution[3] = j
									solution[4] = i
									solution[5] = i+j+k+l+m
									if solution[5] < minChange:
										minChange = solution[5]
						else:
							if (i*array[3] + j*array[2] + k*array[1]+ l*array[0]) == change:
								solution[0] = l
								solution[1] = k
								solution[2] = j
								solution[3] = i
								solution[4] = i+j+k+l
								if solution[4] < minChange:
									minChange = solution[4]
									result = solution
										
	return result
'''else: 
        min_length = 0
        min_configuration = []
        for coin in coins:
            results = slowChange(k - coin, coins, cache)
            if results != []:
                if min_length == 0 or (1 + len(results)) < len(min_configuration):
                    min_configuration = [coin] + results
                    min_length = len(min_configuration)
                    cache[k] = min_configuration
        #print "second print", cache
        return cache

def changeSlow(coinValueList,change):
	minCoins = change
	if c in coinValueList:
		knownResults[c] = 1
		return 1
	elif knownResults[change] > 0:
		return knownResults[change]
	else:
		for i in (c for c in coinValueList if c <= change):
			numCoins = 1 + changeSlow(coinValueList, change-i, knownResults)
		if numCoins < minCoins:
			minCoins = numCoins
			knownResults[change] = minCoins
	coinValueList.append(minCoins)
	return coinValueList
	

def slowChange(coins, k, cache = []):
    if k in cache:
        return cache[k]
		
    elif k in coins:  
		# if k in coins, nothing to do but return.
        cache[k] = [k]
        return cache[k]
		
    elif min(coins) > k:  
		# if the largest coin is greater then the k, there's nothing we can do.
        cache[k] = []
        return cache[k]
		
    else:  # check for each coin, keep track of the minimun configuration, then return it.
        min_length = 0
        min_configuration = []
        for coin in coins:
            results = slowChange(k - coin, coins, cache)
            if results != []:
                if min_length == 0 or (1 + len(results)) < len(min_configuration):
                    min_configuration = [coin] + results
                    min_length = len(min_configuration)
                    cache[k] = min_configuration
        #print "second print", cache
        return cache
		
'''

########################################
#Algorithm 2 - Greedy 
########################################

def changeGreedy(currencyValuesArray, amountToReturn):
	numArray = [0] * len(currencyValuesArray)
	total = 0
	for i in range(len(currencyValuesArray)-1,-1,-1):
		if(currencyValuesArray[i] <= amountToReturn):
			num = amountToReturn / currencyValuesArray[i]
			numArray[i] = numArray[i] + num
			total = total + num
			amountToReturn -= num * currencyValuesArray[i]

	numArray.append(total) 
	return numArray
	
########################################
#Algorithm 3 - Dynamic  
########################################

def changeDP(currencyValuesArray, amountToReturn):
	minArray = [0]
	firstCoinArray = [0]
	coin = 0
	
	for j in range(1, amountToReturn+1):
		min = -1
		for i in range(0, len(currencyValuesArray)):
			if currencyValuesArray[i] <= j:
				if min == -1:
					min = 1 + minArray[j - currencyValuesArray[i]]
					coin = i
				elif 1 + minArray[j - currencyValuesArray[i]] < min:
					min = 1 + minArray[j - currencyValuesArray[i]]
					coin = i
		minArray.append(min)
		firstCoinArray.append(coin)
		
	coins = []
	while amountToReturn > 0:
		coins.append(currencyValuesArray[firstCoinArray[amountToReturn]])
		amountToReturn = amountToReturn - currencyValuesArray[firstCoinArray[amountToReturn]]
		
	numberOfCoins = len(coins)
	
	result = []
	for coin in currencyValuesArray:
		result.append(coins.count(coin))
		
	result.append(numberOfCoins)
	
	return result
	
#########################
# END - Algorithms
#########################




#########################
# START - Programs 
#########################

###############################################################
# 	RunProgram
#	+ Get input file and starts to run the needed program
###############################################################
def writeOutput(array, result, filename, time):
	file = open(filename, "a") #we want to append, not truncate
	file.write(str(array) + "\n")
	file.write(str(result) + "\n")
	#file.write(str(time) + "\n") #timing write for plotting run time
	file.close()

def parser():
	vals = []
	change = []

	inputFile = open(sys.argv[1], "r")
	
	while True:
		lineValue = inputFile.readline()
		if lineValue:
			lineValue = lineValue.replace('[', '')
			lineValue = lineValue.replace(']', '')
			tempArray = lineValue.split(',')
			temp2 = []
			for i in tempArray:
				temp2.append(int(i))

			vals.append(temp2)

			lineValue = inputFile.readline()
			change.append(int(lineValue))
		else:
			break

	inputFile.close()
	return (vals, change)

def funRun(funName, vals, change, fname):
	
	for i in range(0, len(vals)):
		startTime = time.time()
		currencyValues = sorted(vals[i])
		amount = change[i]
		array = funName(currencyValues, amount)
		finishTime = time.time()
		runtime = (finishTime - startTime)
		result = array.pop()
		writeOutput(array, result, fname, runtime*1000000)
		
		
def runProgram(arg):
	values = []
	ammountToChange = []
	(values, ammountToChange) = parser()
	#this is for writing, so we only have to compile regex once
	name = re.sub('(.txt)', '', sys.argv[1])
	outputFile = name + "change.txt"
	#this just resets the file at the first run
	file = open(outputFile, "w")
	file.close()
	
	if arg == 1: #slow
		funRun(changeSlow, values, ammountToChange, outputFile)	
			
	elif arg == 2: #greedy
		funRun(changeGreedy, values, ammountToChange, outputFile)

	elif arg == 3: #dp
		funRun(changeDP, values, ammountToChange, outputFile)
		
	elif arg == 4: #test
		print "This doesn't do anything right now."
		
	elif arg == 5: #experiment aka all
		#writeOutput("Slow:", "", outputFile)
		#funRun(changeSlow, values, ammountToChange, outputFile)
		writeOutput("Greedy:", "", outputFile, "")
		funRun(changeGreedy, values, ammountToChange, outputFile)
		writeOutput("\nDP:", "", outputFile, "")
		funRun(changeDP, values, ammountToChange, outputFile)

########################################
# END - Programs 
########################################


########################################
# 	MAIN
#	+ Declaring "main"
#	+ Usage 'python project2_Main.py input_file.txt { -runBrute | -runGreedy | -runDP | -runTestCorrect| -runExperiment }'
########################################
def CheckFirstArg():
	if (os.path.isfile(sys.argv[1]) == True):
		return True
	else:
		print str(sys.argv[1]), " is not a file in this directory."
		return False

def CheckSecondArg():
	if ( len(sys.argv) > 2 ):
		if (sys.argv[2] == "-greedy"):
			return 2
		elif (sys.argv[2] == "-dp"):
			return 3
		elif (sys.argv[2] == "-exp"):
			return 5
		else:
			print "\n", str(sys.argv[2]), " is not a valid 2nd arugument."
			return False
	else:
		print "\nYou did not enter a 2nd argument"
		return False


if __name__ == "__main__":
	if ( len(sys.argv) > 1 ):
		if (CheckFirstArg() == False):
			print "\nUsage: 'python project2_Main.py input_file.txt { -greedy | -dp | -exp }'"
		else:
			arg = CheckSecondArg()
			if (arg == False):
				print "\nUsage: 'python project2_Main.py input_file.txt { -greedy | -dp | -exp }'"
			else:
				print "\nValid Input, let's go!\n"
				runProgram(arg)
	else:
		print "\nYou do not have enough arguments.\n"
		print "\nUsage: 'python project2_Main.py input_file.txt { -greedy | -dp | -exp }'" 
