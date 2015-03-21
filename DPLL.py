import sys

inputFile = open(sys.argv[2])
outputFile = open("CNF_sastisfiability.txt", "w")

operators = ["not", "and", "or"]

def extractLiterals(clause):
	returnList = []
	if(isinstance(clause,list)):
		for literal in clause:
			if (literal not in operators):
				returnList += literal
	else:
		returnList = clause
		
	return returnList
			
def checkComplement(literal):
	test = False
	symbol = "A"
	if(isinstance(literal,list)):
		test = True
		symbol = literal[1]
	else:
		test = False
		symbol = literal
		
	return test,symbol
		
			
def findPureSymbol(symbols,clauses,model):
	returnList = []
	pureList = []
	for symbol in symbols:
		pureList += [symbol,0]
	
	for clause in clauses:
		literalInClause = extractLiterals(clause)
		for element in literalInClause:
			test, literal = checkComplement(element)
			symbol = pureList[pureList.index(literal)]
			if(test==true and symbol[1]==0):
				pureList[pureList.index(literal)] = [literal,1]
			elif(test==false and symbol[1]==0):
				pureList[pureList.index(literal)] == [literal,2]
			elif (test==false and symbol[1]==1) or (test==true and symbol[1]==2):
				pureList[pureList.index(literal)] == [literal,3]
	
	for element in pureList:
		if element[1] == 1 :
			returnList += [element[0],True]
		elif element[1] == 2:
			returnList += [element[0],False]
			
	return returnList
	
symbols = []
def getSymbols(model):
	global symbols
	for element in model:
		if(not(isinstance(element,list)) and element not in operators):
			if(element not in symbols):
				symbols += element
		elif (isinstance(element,list)):
			getSymbols(element)
	
def getClauses(model):
	global clauses
	for element in model:
		if(element != 'and' and element != 'or'):
			clauses.append(element)

linenum = 1
sentCount = -1
numSent = 0
for line in inputFile:
	if (sentCount == -1):
		numSent = eval(line)
	sentCount += 1
	
if(sentCount != numSent):
	print "The number of propositional sentence is not equal to the number of lines"

else:
	linenum = 1
	print "hi"
	inputFile.seek(0,0)
	for line in inputFile:
		if(linenum == 1):
			linenum = 2
			continue
		model = eval(line)
		symbols = []
		clauses = []
		getSymbols(model)
		getClauses(model)
		print "symbols", symbols
		print "clauses", clauses