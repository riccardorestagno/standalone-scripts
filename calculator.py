import math

def mult(num1, num2):
	num1 = float(num1)
	num2 = float(num2)
	print (num1*num2)

def div(num1, num2):
	num1 = float(num1)
	num2 = float(num2)
	print (num1/num2)
	
def add(num1, num2):
	num1 = float(num1)
	num2 = float(num2)
	print (num1+num2)

def sub(num1, num2):
	num1 = float(num1)
	num2 = float(num2)
	print (num1-num2)

def exp(num1, num2):
	num1 = float(num1)
	num2 = float(num2)
	print(math.pow(num1, num2))

myCalc = input()

while myCalc!="end": 
	if "^" in myCalc:
		inp1,inp2 = myCalc.split('^')
		exp(inp1,inp2)
	elif myCalc.startswith('sqrt'):
		useless,inp2 = myCalc.split('t')
		if int(inp2)<0:
			print("Error")
		else:
			root = math.sqrt(int(inp2)) 
			print(root)
	elif "/" in myCalc:
		inp1,inp2 = myCalc.split('/')
		div(inp1,inp2)
	elif "+" in myCalc:
		inp1,inp2 = myCalc.split('+')
		add(inp1,inp2)
	elif "*" in myCalc:
		inp1,inp2 = myCalc.split('*')
		mult(inp1,inp2)
	elif "--" in myCalc:
		inp1,inp2 = myCalc.split('--')
		add(inp1,inp2)
	elif myCalc.startswith('-'):
		empty,inp1,inp2 = myCalc.split('-')
		result1 = float(inp1)+float(inp2)
		mult(-1,result1)
	elif "-" in myCalc:
		inp1,inp2 = myCalc.split('-')
		sub(inp1,inp2)	
	else:
		print("There is an error in your input.")
	myCalc = input()