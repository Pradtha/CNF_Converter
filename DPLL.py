import sys

inputFile = open(sys.argv[2])
outputFile = open("CNF_sastisfiability.txt", "w")

operators = ["not", "and", "or"]
	
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
	
def checkComplementarity(element):
	complemented = False
	variable = ""
	if(not(isinstance(element,list))):
		complemented = False
		variable = element
	
	else:
		if(element[0] == 'not'):
			complemented = True
			variable = element[1]

	#print "com,var", complemented,variable
	return complemented,variable
	
def updateValueList(complemented, value, index):
	#print "value[index]: ",value[index]
	if(complemented == False and value[index] == 0):
		return 1
	if(complemented == True and value[index] == 0):
		return 2
	if((complemented == False and value[index] == 2) or (complemented == True and value[index] == 1)):
		return 3
	return value[index]
	
		
def findPureSymbols(clauses,symbols):
	pureList = []
	value = []
	
	for symbol in symbols:
		value.append(0)
	
	#print "clauses", clauses
	for clause in clauses:
		#print "inival", value
		if(not(isinstance(clause,list))):
			#print "literal"
			index = symbols.index(clause)
			#print index
			value[index] = updateValueList(False,value,index)
		
		else:
			if(clause[0] == 'not'):
				#print "com"
				index = symbols.index(clause[1])
				#print index
				value[index] = updateValueList(True,value,index)
			
			else:
				for element in clause[1:len(clause)]:
					#print "or"
					complemented, variable = checkComplementarity(element)
					index = symbols.index(variable)
					#print "index", index
					value[index] = updateValueList(complemented,value,index)
					#print "val[ind]",value[index]
					
	
	#print "value", value
	for i in range(len(symbols)):
		if(value[i] == 1):
			pureList.append([symbols[i],True])
		elif(value[i] == 2):
			pureList.append([symbols[i],False])
	
	#print pureList
	return pureList
		
		
def DPLL(clauses,symbols,var):
	result = False
	trueClauses = []
	#print symbols,"   ", clauses,"     ", var
	result = True
	for clause in clauses:
		#print var, booleanStringClause(clause), eval(booleanStringClause(clause))
		if(eval(booleanStringClause(clause)) == False):
			result = False;
			break;
		elif(eval(booleanStringClause(clause)) == True):
			trueClauses.append(clause)
		else:
			result = False
			break;
			
	if(result == True):
		return var
	
	else:
		#print "asdf"
		#print "end of sentence"
		pureList = findPureSymbols(clauses,symbols)
		#print "pure list",pureList
		trueSymbols = []
		if(len(pureList)>0):
			for i in range(len(pureList)):
				element = pureList[i]
				index = symbols.index(element[0]);
				trueSymbols.append(element[0])
				var[index] = element[1]
				
			reqClauses = [x for x in clauses if not(x in trueClauses)]
			reqSymbols = [x for x in trueSymbols if not(x in symbols)]
			return DPLL(reqClauses,reqSymbols,var)
			
		
		
	
	
def DPLL_Satisfiable(sentence):
	symbols = getSymbols(sentence)
	clauses = getClauses(sentence)
	var = []
	for symbol in symbols:
			var.append('True')
	return DPLL(clauses,symbols,var), symbols

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
		print DPLL_Satisfiable(sentence)
		#print booleanStringSenstence(sentence)
		
'''ua = ""
if(eval('ua or ua')):
	print "a"
elif(eval('ua or ua')==False):
	print "b"
print eval('not(ua)')'''