import sys

inputFile = open(sys.argv[2])
outputFile = open("CNF_sastisfiability.txt", "w")

operators = ["not", "and", "or"]

class index(object):
	i=0

	
def booleanStringClause(clause):
	if(not(isinstance(clause,list))):
		return "var["+str(symbols.index(clause))+"]"
	
	else:
		if(clause[0] == 'not'):
			return "not(var["+str(symbols.index(clause[1]))+"])"
		else:
			temp = "( "+booleanStringClause(clause[1]);
			for i in range (2,len(clause)):
				temp += " or " + booleanStringClause(clause[i])
			temp += " )"
			return temp
			

def getSymbols(model):
	global symbols

	for element in model:
		if(not(isinstance(element,list)) and element not in operators):
			if(element not in symbols):
				symbols += element
		elif (isinstance(element,list)):
			symbols = getSymbols(element)
	
	return symbols
	
def getClauses(model):
	clauses = []
	if(model[0] == 'and'):
		for i in range(1,len(model)):
			clauses.append(model[i])
	else:
		clauses.append(model)
		
	return clauses
		
def findPureSymbols(symbols,clauses,model):
	symbols = getSymbols(model)
	clauses = getClauses(model)
	pureList = []
	value = []
	for symbol in symbols:
		pureList.append(symbol)
		value.append(0)
		
		
def DPLL(clauses,symbols,model):
	result = False
	#print symbols, clauses
	for clause in clauses:
		print clause,"   ", booleanStringClause(clause)
		
	print "end of sentence"
	
	
def DPLL_Satisfiable(sentence):
	symbols = getSymbols(sentence)
	clauses = getClauses(sentence)
	#print symbols, clauses
	return DPLL(clauses,symbols,sentence)

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
		sentence = eval(line)
		symbols = []
		clauses = []
		model = []
		variable = []
		index.i=0
		DPLL_Satisfiable(sentence)
		#print booleanStringSenstence(sentence)
