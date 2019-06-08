# Write a function that takes in two sorted lists and outputs a sorted list that is their union.
import re

def add_sorted_list():
	a = [1,3,5,7,9,23,55]
	b = [1,3,5,7,19,20,24,100]

	i = 0
	j = 0
	outcome = list()
	while (i < len(a) and j < len(b)):
		if a[i] > b[j]:
			outcome.append(b[j])
			j = j+1
		elif a[i] < b[j]:
			outcome.append(a[i])
			i = i+1
		else:
			outcome.append((a[i]))
			i = i+1
			j = j + 1

	if i < len(a):
		for k in range(i,len(a)):
			outcome.append(a[k])
	if j < len(b):
		for k in range(j,len(b)):
			outcome.append(b[k])

	print (outcome)



def add_sorted_list1():
	a = [1,3,5,7,9,23,55]
	b = [1,3,5,7,19,20,24,100]

	i = 0
	j = 0
	while (i < len(a) and j < len(b)):
		if a[i] > b[j]:
			a.insert(i, b[j])
			j = j+1
		elif a[i] < b[j]:
			i = i+1
		else:
			i = i+1
			j = j + 1

	if j < len(b):
		for k in range(j,len(b)):
			a.append(b[k])

	print (a)
add_sorted_list1()


# Write a memory efficient string reverse function
def reverse():
	a = 'abcddcba'
	a = list(a)

	for i in range(len(a)/2):
		a[i], a[len(a)-1-i] = a[len(a)-1-i], a[i]
	a = ''.join(a)
	print (a)

reverse()

# A sentence is given which contains lowercase English letters and spaces. It may contain multiple spaces. Get first letter of every word and return the result as a string. The result should not contain any space. 

def get_first_letter_from_words():
	import re
	res = ''
	line = '      this is my first      p.  age      of letter      from amazon.'
	if line[0] != ' ':
		res = line[0]
	n = len(line)
	for i in range(n-1):
		if re.search(r'[a-z]', line[i+1]) and line[i] ==' ':
			res = res + line[i+1]
	print (res)

get_first_letter_from_words()

# swaping the adjacents letter from the sentence

def swapping_letters():
	line = 'this is my test case. the '
	# line = [1,3,4,6,8,9]
	print ('Original : {}'.format(line))
	if type(line) == str:
		line = list(line)
	res = ''
	n = len(line)
	i = 0
	# for i in range(0, n, 2):
	while (i < n):
		if re.search(r'[a-z]', line[i]) and re.search(r'[a-z]', line[i+1]):
			line[i], line[i+1] = line[i+1], line[i]
			i += 2
		else:
			i += 1
	if type(line) != int:
		line = ''.join(line)
	print (line)

swapping_letters()

# Given an array. Iterate it for the given number of times. And then return the summation of the resultant elements.

# Ex: Array is { 1,2,5,6}, N=2

# After 1st iteration: {2-1, 5-2, 6-5}={1,3,1}

# After 2nd : {3-1, 1-3}={2,-2}

# Sum is 2  + (-2) = 0

def summation():
	n = 5
	a = [1,2]
	b = list()
	sum1 = 0
	for i in range(n):
		if len(a) > 1:
			for j in range(len(a)-1):
				t = a[j+1] - a[j]
				b.append(t)
			print ('b : {}'.format(b))
			a = b
			b = []

	for num in a:
		sum1 += num
	print ('sum is : {}'.format(sum1))

summation()


# Swap adjacent nodes in the linked list. Change the links, not the data. Complete the method.

# Ex:1, 2, 3, 4
# o/P: 2, 1, 4, 3

# ex: 1,2,3,4,5
# op: 2, 1, 4, 3, 5

def swap_adjacents():
	a = [1,2,3,4,5,7,9]
	i = 0
	if len(a)%2 == 0:
		count = len(a)
	else:
		count = len(a) - 1
	while (i < count):
		a[i], a[i+1] = a[i+1], a[i]
		i +=2
	print (a)

swap_adjacents()


# find the second largest number
def second_largest():
	a = [1,4,5,33,22,56,43,98]
	first = second = a[0]
	for num in a:
		if num > first:
			second = first
			first = num
	print (second)

second_largest()

# find the nth number from the list
def nth_largest(n):
	a = [4,3,6,8,2,44,22,556]
	b = list()

	if len(a) < n:
		print ('invalid inputs')
		exit()
	def largest(a, b):
		m = a[0]
		for num in a:
			if num > m and num not in b:
				m = num
		return m


	for i in range(n):
		big = largest(a, b)
		print ('big : {}'.format(big))
		b.append(big)
	print ('nth largest number is : {}'.format(b[-1]))

nth_largest(5)

# swapping the vowels with first and last
def swap_vowels():
	line = 'once upon a time there was a king'
	print ('original line : {}'.format(line))
	line = list(line)
	n = len(line)
	i = 0
	j = n -1
	while i < j: 
		if line[i] not in 'aeiouAEIOU':
			i = i+1
		elif line[j] not in 'aeiouAEIOU':
			j -= 1
		else:
			line[i], line[j] = line[j], line[i]
			i += 1
			j -= 1
	line = ''.join(line)

	print ('updated line : {}'.format(line))

swap_vowels()

# sorting the numbers
def sorting():
	a = [3,2,4,5,6,3,2,1,3,56,23,6]
	a = 'saurabh'
	a = list(a)
	n = len(a)
	i = 0
	while (i < n-1):
		j = i+1
		while (j < n):
			if a[i] > a[j]:
				a[i], a[j] = a[j], a[i]
			j +=1
		i += 1
	print ('sorted list : {}'.format(a))

sorting()

# linear search
def linear_search(num):
	find = False
	a = [34, 23, 45, 5, 6,7,2]
	for i in a:
		if i == num:
			find  = True
	if find:
		print ('{} is present in list {}'.format(num, a))
	else:
		print ('{} is not present in list {}'.format(num, a))

linear_search(45)
linear_search(46)


# print Fibbonacie series till n numbers
#0,1,1,2,3,5,8,13

def fibbonaci(n):
	fibbo = list()
	a = 0
	b = 1
	fibbo.append(a)
	fibbo.append(b)
	# print a
	# print b
	for i in range(n-2):
		c = a + b
		# print c
		fibbo.append(c)
		a = b
		b = c
	print (fibbo)
fibbonaci(10)

# fibbonacy series through recursion
def fibbo(a = 0, b = 1, n = 10):
	if n == 0:
		return
	c = a + b
	a = b
	b = c
	print c
	n = n-1
	fibbo(a, b, n)

# fibbo()

def binary_search(num=0):
	num = 19
	print ('start binary search')
	a = range(20)
	print (a)
	start = 0
	end = len(a) 
	found = False
	while start < end and not found:
		mid = (start + end)/2
		if a[mid] > num:
			end  = mid - 1
		elif a[mid] < num:
			start = mid + 1
		elif a[mid] == num:
			found = True
		print ('number : {}'.format(a[mid]))
	if found:
		print ('found')
	else:
		print ('not found')

binary_search()

# Find the row with maximum number of 1s
def matrix():
	a = [[1,1,1,1],
		[1,9,1,1],
		[0,0,0,0],
		[1,1,1,1],
		[0,1,1,0]]

	m = len(a)
	n = len(a[0])
	print ('number of rows : {}'.format(m))
	print ('number of columns : {}'.format(n))
	print ('read elements : {}'.format(a[1][1]))

	res = dict()
	for i in range(m):
		count_1 = 0
		for j in range(n):
			if a[i][j] == 1:
				count_1 +=1
		res[i] = count_1
	print ('result: {}'.format(res))

	max1 = 0

	for key in res:
		if res[key] > max1:
			myraw = key
			max1 = res[key]

	print ('Maximun numbers of ones in : {}'.format(myraw))

matrix()


# check weather the given string is anagram or not.
# all characters from first string is present in second string
# both string should same if we do sort them.

def anagram():
	str1 = 'aacbcdc'
	str2 = 'aabccdc'

	if len(str1) != len(str2):
		print ('given strings are not anagram')
		return
	str1 = sorted(list(str1))
	str2 = sorted(list(str2))

	print (str1)
	print (str2)

	for i in range(len(str1)):
		if str1[i] != str2[i]:
			print ('strings are not anagram')
			return

	print ('strings are anagram')

anagram()

def isPrime(num):
	status = True
	if num == 0 or num == 1:
		print ('0 or 1 are not in prime numbers category')
		return
	elif num == 2:
		print ('number is prime')
	elif num%2 == 0:
		print ('number is not prime')

	else:
		for i in range(3, int(math.sqrt(num) + 1), 2):
			if num % i == 0:
				status = False
				break
	if status:
		print ('{} is a prime number'.format(num))
	else:
		print ('{} is not a prime number'.format(num))

isPrime(0)

def prime_numbers():
	status = True
	prime_list = list()
	for i in range(2,100):
		status = True
		for j in range(2,i/2):
			if i % j == 0:
				status = False
				break
		if status:
			prime_list.append(i)
	print prime_list

prime_numbers()

def isPalindrom():
	string1 = 'abcddcba'
	string = list(string1)
	print (string)
	l = len(string)
	i = 0
	status  = True
	while (i < l):
		if string[i] != string[l-1]:
			print ('given string is not palindrom')
			status = False
			break
		else:
			i += 1
			l -= 1
	if status:
		print ('string is palindrom')

isPalindrom()

import re
def palindrom_test():
	a = 'a123#*bcdcb321a'
	a = list(a)
	l = len(a)
	i = 0
	status = True
	while (i<l):
		if not re.search(r'[a-zA-Z0-9]',a[i]):
			print ('a : {}'.format(a[i]))
			i +=1
		elif not re.search(r'[a-zA-Z0-9]',a[l-1]):
			l -=1
		elif a[i] != a[l-1]:
			status = False
			break
		else:
			i +=1
			l -=1
		print ('a : {} and l : {}'.format(a[i], a[l-1]))
	if not status:
		print ('string is not palindrom')
	else:
		print ('palindrom')
palindrom_test()


def reverse_string():
	string = 'aaaaba'
	print ('original : {}'.format(string))
	string = list(string)
	l = len(string)
	i = 0

	while (i < l):
		string[i], string[l-1] = string[l-1], string[i]
		i += 1
		l -= 1
	string = ''.join(string)
	print ('reverse string : {}'.format(string))

reverse_string()

# find out the third max number from the list.
def third_max_number():
	a = [4,3,-500,66,77,33,54,430]
	print ('original list : {}'.format(a))
	first = second = third = 0
	for num in a:
		if num > first:
			third = second
			second = first
			first = num
		elif num > second and num <first:
			third = second
			second = first
		elif num > third and num < second:
			num = third

	print ('first : {}'.format(first))
	print ('second : {}'.format(second))
	print ('third : {}'.format(third))

third_max_number()

# Program for array rotation
def rotation(a, n):
	print ('original : {}'.format(a))
	for i in range(n):
		x = a.pop(0)
		a.append(x)
	print ('updated list after rotation: {}'.format(a))
rotation([1,2,3,4,5,6],5)


def rotation2(a, n):
	for i in range(n):
		a = a[1:] + a[:1]
		print (a)
print ('************************')
rotation2([1,2,3,4,5,6],3)
print ('************************')


# Sum of all elements repeating k times in an array
def frequency_sum(k):
	a = [3,4,5,33,3,3,4,5,1]
	num_dict = dict()
	freq_sum = 0

	for num in a:
		try:
			num_dict[num] += 1
		except:
			num_dict[num] = 1
	for key in num_dict:
		if num_dict[key] == k:
			freq_sum += key

	print ('sum is : {}'.format(freq_sum))

frequency_sum(2)

# Longest subarray such that the difference of max and min is at-most one
def array_sum_mix_max_diff_1():
	# a = [3, 3, 1,4, 4, 5, 6]
	# a = [7, 7, 7]
	a = [1,9,2, 8, 8, 9, 9, 10]
	min1 = a[0]
	counter = 0
	sub_list = list()

	for i in range(len(a)-1):
		diff  = a[i+1] - a[i]
		if diff < 0:
			diff  = diff * (-1)
		if diff <= 1:
			if len(sub_list) > 0:
				min1 = min(sub_list)
				if a[i] - min1 <=1:
					counter +=1
					sub_list.append(a[i])
			else:
				counter +=1
				sub_list.append(a[i])	
		else:
			sub_list = list()			

	print ('subarray couter is {} and the array is {}'.format(counter, sub_list))

array_sum_mix_max_diff_1()

# Maximum sum in circular array such that no two elements are adjacent
def sum_of_non_adjacents():
	a = [1, 2, 3, 4, 5, 6, 7, 8, 1]
	sub_list = list()
	enter = False
	sub_list.append(a[0])

	for num in a:
		for ele in sub_list:
			if num - ele > 1:
				enter = True
			else:
				enter = False
		if enter:
			sub_list.append(num)
	print (sub_list)
	s = 0
	for num in sub_list:
		s +=num
	print ('non adjacent sum is : {}'.format(s))

sum_of_non_adjacents()

# Given a character string, display the characters that appear more than once in that string.
def string_freq():
	a = 'this is my test message'
	a = list(a)
	d = dict()
	for char in a:
		# if char == ' ':
		if re.search(r'\s+',char):
			continue
		try:
			d[char] += 1
		except:
			d[char] = 1
	print (d)

	for key in d:
		if d[key] >1:
			print d[key], key

string_freq()

# 2. Rotate a matrix 90 degrees to right
def rotate_matrix_right():
	a = [[1,2,3],
		[4,5,6],
		[7,8,9]]

	# res = [[7,4,1],
	# 		[8,5,2],
	# 		[9,6,3]]

	m = len(a)
	n = len(a[0])

	b = list()
	t = list()
	for i in range(m):
		t = list()
		for j in range(n-1,-1,-1):
			t.append(a[j][i])
		b.append(t)
	print (a)
	print (b)

rotate_matrix_right()

# Two strings S and S1. Remove all chars from S which are present in S1.
# Remove the letters from a which are present in b
def remove_duplicate():
	a = 'abcdefrghik'
	print (a)
	b = 'cdghtikmnopqrstuv'
	a = list(a)
	b = list(b)

	for char in a:
		if char in b:
			a.remove(char)
	a = ''.join(a)

	print (a)

remove_duplicate()

# Replace the elements in an array with the next following greater number of it from right side of the element.
def replace_number():
	a = [12,4,5,41,44,50,1,2,3,78,4,3,5,13]
	# outcome should be : [50,44,41,41,44,50,1,2,3]

	l = len(a)
	i = 0

	while(i < l):
		if a[l-1] < a[i]:
			l -=1
		else:
			a[i] = a[l-1]
			i +=1
			l -=1
	print (a)

replace_number()

# Write a program to remove duplicates from array of prime numbers.
def remove_dub_num():
	a = [1,3,5,3,3,7,11,3,5,3,2,2,3,11]
	print ('A : {}'.format(a))
	l = len(a)
	for i in range(len(a)-1):
		j = i+1
		while (j<len(a)-1):
			if a[i] == a[j]:
				k = j
				while (k < len(a)-1):
					a[k] = a[k+1]
					k += 1
				a.pop(k)
				print (a)
			else:
				j +=1
	print ('after remove the duplicates : {}'.format(a))

remove_dub_num()

def a_power_b(a,b):
	s = 1
	for i in range(b):
		s = s*a
	print ('{} to the power {} is {}'.format(a,b,s))
	return s
print ('saurabh')

a_power_b(2,5)

print map(a_power_b,[1,2,3,4,5],[1,2,3,4,5])



# top 10 elements from the list of intergers

def top10_elements():
	a = [3,4,6,22,44,67,899,33,554,234,967,12,5678,90,545,34,23,121,1000]
	res = list()
	def find_max(a):
		m = 0
		for num in a:
			if num > m:
				m = num
		return m
	for i in range(10):
		t = find_max(a)
		res.append(t)
		a.remove(t)

	print ('top 10 elements : {}'.format(res))

top10_elements()


def uppercase(func):
	def wrapper(*name):
		print ('Starting the function')
		res = func(*name)
		modified = res.upper()
		return modified
		print ('End of function')
	return wrapper

@uppercase
def greet(name):
	return 'hello !! {}'.format(name)

print greet('Saurabh')

def checker(func):
	def wrapper(a,b):
		print ('Start')
		res = func(a,b)
		if res > 0:
			print ('sum of {} and {} is {}'.format(a,b,res))
		else:
			print ('sum is negative')
	return wrapper

@checker
def add1(a,b):
	return a+b

add1(10,-30)

## use of map function:

def useofmap():
	a = [1,2,3,4,5]
	b = [6,7,8,9,10]
	def sum(x,y):
		return x+y
	print map(sum,a,b)
useofmap()


# Given array, find all possible sets of elements which add up to a given integer K
# def subset_add_sum():
# 	a = [2, 3, 5, 6, 8, 10]
# 	expected_sum = 10
# 	a = sorted(a)
# 	print (a)

# 	l = len(a)
# 	i = 0
# 	for i in range(l-1,-1,-1):
# 		if a[i]
# 		for j in range(l-2,-1,-1):
# 			if a[]


# subset_add_sum()

# Check if is possible to get given sum from a given set of elements
# Input : arr[] = { 2, 3}
#          q[]  = {8, 7}
# Output : Yes Yes
# Explanation : 
# 2 + 2 + 2 + 2 = 8
# 2 + 2 + 3 = 7

# def get_element_sum():
# 	a = [2,3]



# Subarray whose sum is closest to K

# Input: a[] = { -5, 12, -3, 4, -15, 6, 1 }, K = 2
# Output: 1
# The subarray {-3, 4} or {1} has sum = 1 which is the closest to K.

# Input: a[] = { 2, 2, -1, 5, -3, -2 }, K = 7
# Output: 6
# Here the output can be 6 or 8
# The subarray {2, 2, -1, 5} gives sum as 8 which has abs(8-7) = 1 which is same as that of the subarray {2, -1, 5} which has abs(6-7) = 1.
# for i in range(0,10,2):
# 	print (i)

# for i in range(10,-1,-1):
# 	print (i),


# Given a sequence of words, print all anagrams together | Set 1


# Lambda - done
# zip - use of zip function to give the list of tuples. it applied on the list of items - done
# decorator - done 
# map - done
# **args, *arg - done
# sets - done
# read and write a file - done
# class and object - done
# inheritance and data
# iterator and 
# static and class method - done

# decorator - write a decorator which will add 10 extra in the addition of sum of two numbers.

def extra_10_plus(func):
	def wrapper(a,b):
		print ('start of the function ')
		print ('first function second line')
		func(a,b)
		print ('Adding 10 extra in addtion of {} and {}'.format(a,b))
		res = res + 10
		return res
	return wrapper

def end_message(func):
	def wrapper(a,b):
		res = func(a,b)
		print ('end of the function')
		return res
	return wrapper

@end_message
@extra_10_plus
def sum10(a,b):
	print 'the sum of a and b is {}'.format(a+b)

sum10(10,20)

print map(lambda x: x ** 4,[1,2,3,4,5])

def useofzip():
	name = [ "Manjeet", "Nikhil", "Shambhavi", "Astha" ]
	roll_no = [ 4, 1, 3, 2 ]
	marks = [ 40, 50, 60, 70 ]
	zipped = zip(name,roll_no, marks)
	print (zipped)

	n, r, m = zip(*zipped)
	print (n, r, m)

useofzip()

def my_args(*args,**kwargs):
	for arg in args:
		print (arg)

	for k, v in kwargs.items():
		print (k,v)
d = {}
d['a'] = 1
d['b'] = 2
my_args(1,2,3,4,5,6,'saurabh', d)

def my_file_test():
	with open('ttest.txt', 'w') as f:
		f.write('This is my first file\n')
		f.write('this is my second line\n')
		f.write('this is my third line\n')

	with open('ttest.txt', 'r') as f:
		for line in f:
			print (line.upper())
my_file_test()

class Student(object):
	def __init__(self, name):
		self.name = name

	def set_name(self, name):
		self.name = name

	def get_name(self):
		return self.name

st = Student('Saurabh')
st.set_name('Aaryan')

print st.get_name()


class Customer(object):
	def __init__(self, name, balance = 0.0):
		self.name = name
		self.balance = balance

	def deposite(self, amount):

		self.balance += amount

	def withdraw(self, amount):
		if self.balance < amount:
			raise Exception ('{} is asking more amount then deposite'.format(self.name))
		self.balance -=amount
		return self.balance

	def display(self):
		print ('{} has {} amount in the bank'.format(self.name, self.balance))

cust = Customer('Ajay', 1000)
cust.display()

cust.deposite(1023)
cust.display()

cust.withdraw(2000)
cust.display()


# a good question which may ask in interview
class b:
	def __init__(self):
		print ('i am init')
	def __call__(self):
		print ('Hi, i am call')

c = b()
a = c()


# json loads -> returns an object from a string representing a json object.

# json dumps -> returns a string representing a json object from an object.

# load and dump -> read/write from/to file instead of string

# json dumps -> returns a string representing a json object from a dict. That's close, but it doesn't have to be a dict you pass in to json.dumps(). You can pass a list, or a string, or a boolean.





