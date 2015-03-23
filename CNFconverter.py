import sys
from collections import defaultdict

operators = ['not', 'and', 'or', 'implies', 'iff']

def convertNF(mylist):
	if mylist[0] not in operators:
		return mylist[0]
	else :
		if mylist[0] == 'not' :
			return ['not', convertNF(mylist[1]) ]
			
		elif mylist[0] == "or":
			orOperands = ['or']
			for i in range(1,len(mylist)):
				orOperands.append(convertNF(mylist[i]))
			return orOperands
			
		elif mylist[0] == "and":
			andOperands = ['and']
			for i in range(1,len(mylist)):
				andOperands.append(convertNF(mylist[i]))
			return andOperands
			
		elif mylist[0] == "implies":
			return ['or', ['not', convertNF(mylist[1])], convertNF(mylist[2]) ]
		
		elif mylist[0] == 'iff':
			return ['and', convertNF(['implies',mylist[1],mylist[2]]), convertNF(['implies',mylist[2],mylist[1]])]
		

def deMorganAndInvolution(mylist):	
	if mylist[0] not in operators:
		return mylist
		
	else :
		if (mylist[0] == 'not'):
			result = deMorganAndInvolution(mylist[1])
			if result[0] == 'not':
				return result[1]
			elif result[0] == 'or':
				return ['and', deMorganAndInvolution(['not',result[1]]), deMorganAndInvolution(['not',result[2]])]
			elif result[0] == 'and':
				return ['or', deMorganAndInvolution(['not',result[1]]), deMorganAndInvolution(['not',result[2]])]
			else:
				return ['not',result[0]]
		
		elif (mylist[0] == 'or'):
			evalResultList = ['or']
			resultList = ['or']
			for i in range(1, len(mylist)) :
				resultList.append(deMorganAndInvolution(mylist[i]))
			
			for result in resultList[1:len(resultList)]:
				modified = False
				if(result[0] == 'or'):
					modified = True
					for i in range(len(result) - 1) :
						result[i] = result[i+1];
					del result[-1]
				
				if(not(modified)):
					evalResultList.append(result)
				else:
					for variables in result:
						evalResultList.append(variables)
			return evalResultList
		
		elif (mylist[0] == 'and'):
			evalResultList = ['and']
			resultList = ['and']
			for i in range(1, len(mylist)) :
				resultList.append(deMorganAndInvolution(mylist[i]))
			
			for result in resultList[1:len(resultList)]:
				modified = False
				if(result[0] == 'and'):
					modified = True
					for i in range(len(result) - 1) :
						result[i] = result[i+1];
					del result[-1]
				
				if(not(modified)):
					evalResultList.append(result)
				else:
					for variables in result:
						evalResultList.append(variables)
			return evalResultList


def operandListEquality(list1, list2):
	test = False
	if(len(list1) != len(list2)):
		return False
	if(isinstance(list1,list) and isinstance(list2,list)):
		test = True
		for x in list1:
			if x not in list2:
				test = False
				break;
				
	elif ((not(isinstance(list1,list))) and (not(isinstance(list2,list)))):
		if (list1 == list2) :
			test = True
	
	return test
	
def isMember(mylist, element):
	test = False
	for x in mylist:
		if (operandListEquality(x,element)):
				test = True
				break;
	return test
	
def idempotency(mylist):
	returnList = [mylist[0]]
	if(mylist[0] in operators):
		if(len(mylist) == 3):
			mylist[1] = idempotency(mylist[1])
			mylist[2] = idempotency(mylist[2])
			if(operandListEquality(mylist[1],mylist[2])):
				return mylist[1]
				
		for i in range(1,len(mylist)):
			if(isinstance(mylist[i],list)):
				mylist[i] = idempotency(mylist[i])
				
		returnList.append(mylist[1])
		for i in range(2, len(mylist)):
			if ( (not(isMember(returnList, mylist[i]) ))):
				returnList.append(mylist[i])
		
		if(len(returnList)==2 and mylist[0] != 'not'):
			return returnList[1]
		return returnList
	
	else:
		return mylist		
		
def checkDNFClause(mylist):
	for j in range(len(mylist)):
		if(isinstance(mylist[j],list)):
			mylist[j] = checkDNFClause(mylist[j])
			
	if(mylist[0] == 'or'):
		for i in range(1,len(mylist)):
			if(isinstance(mylist[i],list)):
				element = mylist[i]
				if(element[0] == 'and' and mylist[0] == 'or'): 
					andTerms = []
					orTerms = []
					for andLiteral in mylist[i]:
						if andLiteral not in operators:
							andTerms.append(andLiteral)
					for orLiteral in mylist:
						if((orLiteral not in operators) and (not(operandListEquality(orLiteral,mylist[i])))):
							orTerms.append(orLiteral)
					mylist = distributeOrOverAnd(andTerms,orTerms)
					break;
		return mylist
	
	return mylist

		
def distributeOrOverAnd(andTerms, orTerms):
	returnList = ['and']
	tempList = []
	for andLiteral in andTerms:
		tempList.append(checkDNFClause(['or',andLiteral]+orTerms))
	returnList += tempList
	return returnList
	
			
inputFile = open(sys.argv[2])
outputFile = open("sentences_CNF.txt","w")

linenum = 1;
clauseCount = -1;
numClauses = 0
for line in inputFile:
	if(clauseCount == -1):
		numClauses = eval(line)
	clauseCount += 1

	
inputFile.seek(0,0)

if(clauseCount == numClauses):
	linenum = 1
	for line in inputFile:
		if (linenum == 1):
			linenum += 1
			continue
		mylist = eval(line)
		nf = convertNF(mylist)
		dinf = deMorganAndInvolution(nf)
		inf = idempotency(dinf)
		cnf = idempotency(deMorganAndInvolution(checkDNFClause(inf)))
		if(len(cnf)==1):
			outputFile.write('\''+str(cnf)+'\'\n')
		else:
			outputFile.write(str(cnf)+"\n")   
else:
	print "Clauses count do no match with the number of clauses mentioned in the file"

inputFile.close()
outputFile.close()

	
	
