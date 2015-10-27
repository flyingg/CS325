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


#########################
# START - Algorithms
#########################

#############################
#Algorithm 1 - Slow
#############################
# 	+ Helper Function: Handles the recursive calls externally for Change_Slow
def Change_SlowPrepare(currencyValuesArray, amountToReturn):
	if amountToReturn == 0:
		return []
	for coin in currencyValuesArray:
		if coin == amountToReturn:
			return [coin]

	minimumCoins = -1
	coins = []
	for i in range(1, amountToReturn/2 + 1):
		temp = []
		temp.extend(Change_SlowPrepare(currencyValuesArray, i))
		temp.extend(Change_SlowPrepare(currencyValuesArray, amountToReturn - i))
		numberOfCoins = len(temp)

		if minimumCoins == -1:
			minimumCoins = numberOfCoins
			coins = temp
		elif numberOfCoins < minimumCoins:
			minimumCoins = numberOfCoins
			coins = temp
	return coins

#Final slow algorithm
def Change_Slow(currencyValuesArray, amountToReturn):
	coins = Change_SlowPrepare(currencyValuesArray, amountToReturn)

	result = []
	for coin in currencyValuesArray:
		result.append(coins.count(coin))

	result.append(len(coins))

	return result


########################################
#Algorithm 2 - Greedy 
########################################

def Change_Greedy(currencyValuesArray, amountToReturn):
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

def Change_Dynamic(currencyValuesArray, amountToReturn):
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

def RunProgram():
	values = []
	ammountToChange = []

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

			values.append(temp2)

			lineValue = inputFile.readline()
			ammountToChange.append(int(lineValue))
		else:
			break

	inputFile.close()

	for i in range(0, len(values)):
		currencyValuesValues = sorted(values[i])
		amount = ammountToChange[i]
		#slowResult = Change_Slow(currencyValuesValues, amount)
		greedyResult = Change_Greedy(currencyValuesValues, amount)
		dpResult = Change_Dynamic(currencyValuesValues, amount)
		print "\nGreedy value is: ", str(greedyResult), "\nDynamic Result is: ", str(dpResult)
		
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
		if (sys.argv[2] == "-runBrute"):
			RunProgram()
			return True
		elif (sys.argv[2] == "-runGreedy"):
			RunProgram()
			return True
		elif (sys.argv[2] == "-runDP"):
			RunProgram()
			return True
		elif (sys.argv[2] == "-runTestCorrect"):
			RunProgram()
			return True
		elif (sys.argv[2] == "-runExperiment"):
			RunProgram()
			return True
		else:
			print "\n", str(sys.argv[2]), " is not a valid 2nd arugument."
			return False
	else:
		print "\nYou did not enter a 2nd argument"
		return False


if __name__ == "__main__":
	if ( len(sys.argv) > 1 ):
		if (CheckFirstArg() == False):
			print "\nUsage: 'python project2_Main.py input_file.txt { -runBrute | -runGreedy | -runDP | -runTestCorrect| -runExperiment }'"
		elif (CheckSecondArg() == False):
			print "\nUsage: 'python project2_Main.py input_file.txt { -runBrute | -runGreedy | -runDP | -runTestCorrect| -runExperiment }'"
		else:
			print "\nEverything is OK!\n"
	else:
		print "\nYou do not have enough arguments.\n"