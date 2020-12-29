#CRACKING THE CODING INTERVIEW

#Q19.5
def mastermind(guess, soln):
	pseudo_hit = 0
	hit = 0
	new_guess = ""
	new_soln = ""
	
	for count, char in enumerate(guess, 0):
		if soln[count].lower() == char.lower():
			hit += 1
		else:
			new_guess += char
			new_soln += soln[count]
			
	for char in new_guess:
		if char in new_soln:
			pseudo_hit += 1
			
	
	return f"Psuedo-hits: {pseudo_hit}, Hits: {hit}"
	
	

#Q19.7
def continuous_sum(sequence):
	list_count = len(sequence)
	max = -2147483647
	sum = 0
	for position in range(0, list_count - 1):
		for value in sequence[position:]:
			sum += value
			if sum >= max:
				max = sum
			#Original (wrong) Guess:
			# else:
				# sum = 0
				# break
		sum = 0
				
	return max

#Given a string, eliminate all “b” and “ac” in the string, replace them in-place and iterate over the string once.
def string_converter(string):
	new_string = ""
	prev_char = ""
	for char in string:
		if char == 'b':
			prev_char = char
			continue
		elif prev_char == "a" and char == "c":
			new_string = new_string[:-1]
			prev_char = char
			continue

		prev_char = char
		new_string += char

	return new_string

def meta_strings(string1, string2):
	difference_count = 0
	string1_diff = ""
	string2_diff = ""
	if len(string1) != len(string2):
		return False

	for position in range(0, len(string1) - 1):

		if difference_count == 0 and string1[position] != string2[position]:
			string1_diff = string1[position]
			string2_diff = string2[position]
			difference_count += 1
			continue
		if difference_count == 1 and string1[position] != string2[position] \
				and string1[position] == string2_diff and string2[position] == string1_diff:
			difference_count += 1
			continue
		if difference_count == 2 and string1[position] != string2[position]:
			return False

	return True

# Given an input string and a dictionary of words, find out if the input string can be segmented into a
# space-separated sequence of dictionary words. See following examples for more details.
# https://practice.geeksforgeeks.org/problems/word-break/0

def word_break(word_dict, string):
	from itertools import permutations
	condenced_dict = []

	for word in word_dict:
		if word in string:
			condenced_dict.append(word)
	for permutation in permutations(condenced_dict):
		test_word = ""
		for word in permutation:
			test_word += word
			if test_word == string:
				return True
	return False

#Ugly numbers are numbers whose only prime factors are 2, 3 or 5. The sequence 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, …
# shows the first 11 ugly numbers. By convention, 1 is included. Write a program to find Nth Ugly Number.
def ugly_number(num):
	n_count = 0
	ugly = False

	for val in range(1, 2147483647):
		for factor in range(1, val):
			if val % factor == 0:
				if factor in [1, 2, 3, 5]:
					ugly = True
				else:
					ugly = False
					break
		if not ugly:
			continue
		else:
			n_count += 1
			ugly = False

		if n_count == num:
			return val

	return -1

print(ugly_number(15))