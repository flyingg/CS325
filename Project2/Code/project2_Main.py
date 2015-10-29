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
def changeSlow(currencyValuesArray, amountToReturn):
	coins = Change_SlowPrepare(currencyValuesArray, amountToReturn)

	result = []
	for coin in currencyValuesArray:
		result.append(coins.count(coin))

	result.append(len(coins))

	return result


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
def writeOutput(array, result, filename):
	file = open(filename, "a") #we want to append, not truncate
	file.write(str(array) + "\n")
	file.write(str(result) + "\n")
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
		currencyValues = sorted(vals[i])
		amount = change[i]
		array = funName(currencyValues, amount)
		result = array.pop()
		print array
		print result
		writeOutput(array, result, fname)
		
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
		writeOutput("Greedy:", "", outputFile)
		funRun(changeGreedy, values, ammountToChange, outputFile)
		writeOutput("\nDP:", "", outputFile)
		funRun(changeGreedy, values, ammountToChange, outputFile)

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
		if (sys.argv[2] == "-brute"):
			return 1
		elif (sys.argv[2] == "-greedy"):
			return 2
		elif (sys.argv[2] == "-dp"):
			return 3
		elif (sys.argv[2] == "-test"):
			return 4
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
			print "\nUsage: 'python project2_Main.py input_file.txt { -brute | -greedy | -dp | -test| -exp }'"
		else:
			arg = CheckSecondArg()
			if (arg == False):
				print "\nUsage: 'python project2_Main.py input_file.txt { -brute | -greedy | -dp | -test| -exp }'"
			else:
				print "\nValid Input, let's go!\n"
				runProgram(arg)
	else:
		print "\nYou do not have enough arguments.\n"
		print "\nUsage: 'python project2_Main.py input_file.txt { -brute | -greedy | -dp | -test| -exp }'" 