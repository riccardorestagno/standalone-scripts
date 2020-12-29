def recursive_fib(n, a, b):
	if n == 1:
		return a, b
	else:
		# return recursive_fib(n-1, b, long_addition(a,b))
		return recursive_fib(n-1, b, b+a)


def long_addition(num1, num2):
	
	num1 = '0' + num1
	num2 = '0' + num2

	newnum = ''
	carry = 0
	current_coefficient = 0
	
	while len(num1) != len(num2):
		num1 = '0' + num1
	
	for i in range(1, len(num1)+1):
		current_coefficient = int(num1[i*-1]) + int(num2[i*-1]) + carry
		if current_coefficient > 9:
			carry = 1
		else:
			carry = 0
		newnum = str(current_coefficient%10) + newnum
	while newnum.startswith('0'):
		newnum = newnum[1:]

	return newnum


if __name__ == "__main__":
	n = 356152
	a = 0
	b = 1
	while n > 500:
		a, b = recursive_fib(501, a, b)
		n -= 500
	print(len(str(recursive_fib(n, a, b)[0])))