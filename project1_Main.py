##############################################################################################
#CS325 - Project 1 
#Contributors - Cierra Shawe, Grant Smith, Gerald Gale
#Instructions: 
#	- README.txt contains all of the instructions needed to run this file successfully 
#	- This file will run both random number generation and proof of correctness
#		+ Select the one you want with the command line: 'python project1_Main.py -c'
#		+ Default program in correctness if command line is entered in wrong
##############################################################################################
import time
import random 
import csv
import sys


#########################
# START - Algorithms
#########################

#############################
#Algorithm 1 - Enumeration 
#############################
''' Gerald - Algo#1'''
def mssAlgorithm1(array):
	arrayLength = len(array)
	max = array[0]

	for i in range(0, arrayLength):
		sum = 0
		for j in range(i, arrayLength):
			sum += array[j]
			if sum > max:
				max = sum

	return max

'''Grant - Algo#1
def mssAlgorithm1(array):
	sumSoFar = 0
	endOfArray = len(array) - 1

	for i in range(0, endOfArray):
		sumTest = array[i] + array[endOfArray]
		if(sumTest > sumSoFar):
			sumSoFar = sumTest

	return sumSoFar'''

'''Cierra - Algo#1
def mssAlgorithm1(array):
	maxValue = array[0]
	nElements = len(array)

	for i in range(0, nElements):
		for j in range(0, nElements):
			maxSum = 0
			for k in range(j, i):
				maxSum += array[k]

			if(maxSum > maxValue):
				maxValue = maxSum

	return maxValue'''



########################################
#Algorithm 2 - Better Enumeration 
########################################
''' Gerald - Algo#2'''
def mssAlgorithm2(array):
	arrayLength = len(array)
	max = array[0]

	for i in range(0, arrayLength):
		sum = 0
		j = i
		for j in range(j, arrayLength):
			sum += array[j]
			if sum > max:
				max = sum

	return max



########################################
#Algorithm 3 - Divide & Conquer 
########################################
''' Gerald - Algo#3'''
def mssAlgorithm3(array, leftEnd, rightEnd):
	if leftEnd > rightEnd:
		return 0 

	if leftEnd == rightEnd: 
		return array[leftEnd]

	middle = ((leftEnd + rightEnd) / 2)

	leftEndMax = array[middle]
	leftEndSum = 0

	i = middle
	for i in range(i, leftEnd, -1):
		leftEndSum += array[i]
		if leftEndSum > leftEndMax:
			leftEndMax = leftEndSum

	rightEndMax = array[middle + 1]
	rightEndSum = 0

	j = middle + 1
	for j in range(j, rightEnd):
		rightEndSum += array[j]
		if rightEndSum > rightEndMax:
			rightEndMax = rightEndSum

	return max((leftEndMax+rightEndMax), mssAlgorithm3(array, leftEnd, middle), mssAlgorithm3(array, (middle + 1), rightEnd))



#############################
#Algorithm 4 - Linear-Time 
#############################
''' Gerald - Algo#4'''
def mssAlgorithm4(array):
	arrayLength = len(array)
	maxsum = maxhere = array[0]

	for i in range(1, arrayLength):
		if maxhere <= 0:
			maxhere = array[i]
		else:
			maxhere += array[i]

		if maxhere > maxsum:
			maxsum = maxhere

	return maxsum


#########################
# END - Algorithms
#########################




#########################
# START - Programs 
#########################

#########################################################################
# 	ParseInputFile
#	+ Is THE function called that is used for grading
#	+ It reads in MSS_Problems.txt
#	+ Crunches the sum for all for algorithms
#	+ Outputs the result onto the screen AND MSS_Results.txt for grading 
#########################################################################
def ParseInputFile(lineNumber):
	print "\nYou are now calculating line #" + str(lineNumber + 1)
	f = open("MSS_Problems.txt", "r")

	rowValue = f.readlines()
	singleRow = rowValue[lineNumber]

	newArray = []
	newValue = ""
	i = 0
	isDone = False
	while isDone == False:
		if singleRow[i].isdigit() == True or singleRow[i] == '-':
			newValue = str(newValue) + str(singleRow[i])
		elif singleRow[i] == ',' or singleRow[i] == ']':
			tempNumber = int(newValue)
			newArray.append(tempNumber)
		else:
			newValue = ""
		
		if singleRow[i] == ']':
			isDone = True
		
		i +=1
	
	algo1Reult = mssAlgorithm1(newArray)
	finalStatement1 = "Algorithm1 result is: " + str(algo1Reult) + "\n"
	print finalStatement1
	
	algo2Reult = mssAlgorithm2(newArray)
	finalStatement2 = "Algorithm2 result is: " + str(algo2Reult) + "\n"
	print finalStatement2

	testingAmount = len(newArray)
	arrayLastElement = testingAmount - 1
#	print newArray[arrayLastElement]
	algo3Reult = mssAlgorithm3(newArray, 0, arrayLastElement)
	finalStatement3 = "Algorithm3 result is: " + str(algo3Reult) + "\n"
	print finalStatement3
	
	algo4Reult = mssAlgorithm4(newArray)
	finalStatement4 = "Algorithm4 result is: " + str(algo4Reult) + "\n"
	print finalStatement4

	#Output final results to MSS_Results.txt' for grading
	with open('MSS_Results.txt', 'a') as myFile:
		myFile.write("You are now calculating input data from line #" + str(lineNumber + 1) + "\n")
		myFile.write(finalStatement1)
		myFile.write(finalStatement2)
		myFile.write(finalStatement3)
		myFile.write(finalStatement4 + "\n")	

##########################################
# 	FileLineCount
#	+ Gets line count of MSS_Problems.txt
##########################################
def FileLineCount():
	lineCount = sum(1 for line in open('MSS_Problems.txt'))
	return lineCount

#######################################################
# 	CreateRandomNumber
#	+ Creates the random # for the running time tests
#	+ Does check to make sure there is at least 1 >0 #
#######################################################
def CreateRandomNumber(newArraySize):
	midwayPoint = (newArraySize / 2)

	randomArray = []
	for i in range(0,newArraySize):
		#insures there is at least 1 positive number in the array 
		if i == midwayPoint:
			number = random.randint(1, 100)
		else:
			number = random.randint(-100, 100)

		randomArray.append(number)

	lengthOfTest = len(randomArray)
	return randomArray


###########################################################
# 	ComputeRunTimeAlgorithms
#	+ Is the function for Experimental Analysis 
#	+ Computes running time for each algorithm 
#	+ Is called for each array of each n size
#	+ Prints results to screen AND runTimeResults.csv file
###########################################################
def ComputeRunTimeAlgorithms(calculatedArray, sizeOfN):
		startTime = time.time()
		algo1Reult = mssAlgorithm1(calculatedArray)
		finishTime = time.time()
		totalRunTime1 = (finishTime - startTime)

		finalStatement1 = "1: " + str(algo1Reult) + " :: " + str(totalRunTime1) + " seconds" 
		print finalStatement1
		
		startTime = time.time()
		algo2Reult = mssAlgorithm2(calculatedArray)
		finishTime = time.time()
		totalRunTime2 = (finishTime - startTime)

		finalStatement2 = "2: " + str(algo2Reult) + " :: " + str(totalRunTime2) + " seconds" 
		print finalStatement2

		testingAmount = len(calculatedArray)
		arrayLastElement = testingAmount - 1
	#	print newArray[arrayLastElement]
		startTime = time.time()
		algo3Reult = mssAlgorithm3(calculatedArray, 0, arrayLastElement)
		finishTime = time.time()
		totalRunTime3 = (finishTime - startTime)

		finalStatement3 = "3: " + str(algo3Reult) + " :: " + str(totalRunTime3) + " seconds" 
		print finalStatement3
		
		startTime = time.time()
		algo4Reult = mssAlgorithm4(calculatedArray)
		finishTime = time.time()
		totalRunTime4 = (finishTime - startTime)

		finalStatement4 = "4: " + str(algo4Reult) + " :: " + str(totalRunTime4) + " seconds" 
		print finalStatement4

		runTimeDataFile = open('runTimeResults.csv', 'a')
		writer = csv.writer(runTimeDataFile)
		writer.writerow( ("", "", "", "") )
		writer.writerow( ( sizeOfN, 1, algo1Reult, totalRunTime1) )
		writer.writerow( ( sizeOfN, 2, algo2Reult, totalRunTime2) )
		writer.writerow( ( sizeOfN, 3, algo3Reult, totalRunTime3) )
		writer.writerow( ( sizeOfN, 4, algo4Reult, totalRunTime4) )
		runTimeDataFile.close()

##################################
# 	CreateRandomArrays
#	+ Creates the random arrays 
#	+ 10 for each n size 
##################################
def CreateRandomArrays():
	testArraySizes = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
	runTimeDataFile = open('runTimeResults.csv', 'w')
	writer = csv.writer(runTimeDataFile)
	writer.writerow( ("Size of n", "Algorithm #", "Max Sum", "Run Time (s)") )
	runTimeDataFile.close()

	for i in range(0, 10):
		tenRandomArrays = []
		for j in range(0, 10):
			j = CreateRandomNumber(testArraySizes[i])
			tenRandomArrays.append(j)
		
		for k in range(0, 10):
		#	print tenRandomArrays[k]
			print "\nThis is the " + str(k + 1) + " array of element size :" + str(testArraySizes[i])
			ComputeRunTimeAlgorithms(tenRandomArrays[k], testArraySizes[i])


#######################################################
# 	TestExample
#	+ Tests the array first stated in the assignment 
#	+ Best used as accuracy check 
#######################################################
def TestExample():
	exampleArray = [31, -41, 59, 26, -53, 58, 97, -93, -23, 84]
	print "Algo 1 sum: " + str(mssAlgorithm1(exampleArray))
	print "Algo 1 sum: " + str(mssAlgorithm2(exampleArray))
	testingAmount = len(exampleArray)
	arrayLastElement = testingAmount - 1
	print "Algo 1 sum: " + str(mssAlgorithm3(exampleArray, 0, arrayLastElement))
	print "Algo 1 sum: " + str(mssAlgorithm4(exampleArray))

#######################################################
# 	TestRunTime
#	+ Tests run time for Experimental Analysis
#######################################################
def TestRunTime():
	CreateRandomArrays()

##########################################################
# 	TestCorrectness
#	+ Tests Correctness - Is used for calculating Grade!
##########################################################
def TestCorrectness():
	numberOfArraysToCalculate = FileLineCount()

	i = 0
	while i < numberOfArraysToCalculate:
		ParseInputFile(i)
		i += 1

########################################
# END - Programs 
########################################



########################################
# MAIN
########################################
if ( len(sys.argv) > 1 ):
	if (sys.argv[1] == "-r"):
		#TEST - RUN TIME!!!
		TestRunTime()
	elif (sys.argv[1] == "-c"):
		#TEST - CORRECTNESS!!!
		TestCorrectness()
	elif (sys.argv[1] == "-e"):
		#TEST - EXAMPLE!!!
		TestExample()
	else:
		print "You did not enter the correct arguments\n\nEnter 'python project1_Main.py -c'"
else:
	#Default to correctness in case note enough arguments are entered - needed for assignment 
	TestCorrectness()

