import re

# Addition of two numbers
def add(a,b):
	# if re.search(r'\d+', a) and re.search(r'\d+',b):
	if (type(a) ==int) and (type(b) ==int):
		print ("The Addition of {} and {} is {}".format(a,b,a+b))
	else:
		print ('both number should be integers')


# add(12,3)
# add('a',5)
# add(34,'b')
# add(23)
# add(1,2)

## Reverse of the given string
def reverse(string):
	print ('The original string is : {}'.format(string))

	string = list(string)
	for i in range(len(string)/2):
		string[i], string[len(string)-1-i] = string[len(string)-1-i], string[i]

	rev = ''.join(string)

	print ('Reverse string is : {}'.format(rev))

# reverse('Saurabh        Maheshwari')


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

	# print (a)
# add_sorted_list1()


## Add the sorted list in other sorted list. Remove the duplicate if its there.
def add_sorted_list(a,b):

	print ('Before Merge : {} and {}'.format(a,b))
	i = j = 0

	# while (j<len(b) and i<len(a)):
	while (i < len(a) and j < len(b)):
		if a[i] > b[j]:
			a.insert(i, b[j])
			j +=1
		elif (a[i] < b[j]):
			i +=1
		else:
			i +=1
			j +=1
	while j<len(b):
		a.append(b[j])
		j+=1

	print ('The final list after merge\n {}'.format(a))

a = [1,3,5,7,9,23,55]
b = [1,3,5,7,19,20,24,100]
# add_sorted_list(a,b)


a = [1,1,1,7,90,231,551]
b = [1,3,5,7,19,20,24,100]
# add_sorted_list(a,b)



def get_first_letter_from_words():
	import re
	res = ''
	line = '      this is my first      p.  age      of letter      from amazon.'
	line = list(line)
	for i in range(len(line)):
		if line[i] == ' ' and re.search(r'[a-zA-Z]+',line[i+1]):
			print (line[i+1])

# get_first_letter_from_words()

def toggle():
	name = 'Saurabh1213$%@#@#@    Maheshwari Shri JAG MOhan LAl MAHESwarI'
	print ('Original Name : {}'.format(name))
	name = list(name)

	for i in range(len(name)):
		if re.search(r'[a-z]', name[i]):
			name[i] = chr(ord(name[i]) - 32)
		elif re.search(r'[A-Z]', name[i]):
			name[i] = chr(ord(name[i]) + 32)

	name = ''.join(name)

	print ('Result : {}'.format(name))

# toggle()


# swaping the adjacents letter from the sentence

def swapping_letters():
	line = 'this is my test case. the '
	# line = [1,3,4,6,8,9]
	print ('Original : {}'.format(line))
	line = list(line)
	i = 0
	while (i < len(line)):
		if re.search(r'[a-zA-Z]', line[i]) and re.search(r'[a-zA-Z]', line[i+1]):
			line[i], line[i+1] = line[i+1], line[i]
			i +=2
		else:
			i+=1

	line = ''.join(line)

	print ('Result : {}'.format(line))

# swapping_letters()

# Frequency of letters - 

def freq_of_letters():
	line = 'This is my test case to find out the frequecy of letters'

	res_dict = dict()
	line = list(line)

	for c in line:
		try:
			res_dict[c] +=1
		except:
			res_dict[c] = 1 
	print ('letter freq : {}'.format(res_dict) )

# freq_of_letters()

# find the second largest number
def second_larget():
	numbers = [2,4,12,454,23,4656,2323,6567,2323,6643]
	numbers = [1,3]

	first = second = 0
	for num in numbers:
		if num > first:
			second = first
			first = num
		elif num <first and num > second:
			second = num

	print ('first {} and second  {} largest numbers '.format(first, second))

second_larget()

# find the 3rd largest number from the list

def third_largest():

	numbers = [1,3,5,233,567,332,574]

	first = second = third = 0
	for num in numbers:
		if num > first:
			third = second
			second = first
			first = num
		elif num < first and num > second:
			third = second
			second = num
		elif num>third and num < second: 
			third = num

	print ('first {}, second  {} and third {} largest numbers '.format(first, second,third))

# third_largest()

# Given an array. Iterate it for the given number of times. And then return the summation of the resultant elements.

# Ex: Array is { 1,2,5,6}, N=2

# After 1st iteration: {2-1, 5-2, 6-5}={1,3,1}

# After 2nd : {3-1, 1-3}={2,-2}

# Sum is 2  + (-2) = 0


def summation():
	n = 3
	a = [1,3,15]
	b = list()

	for i in range(n):
		if len(a) > 1:
			for j in range(len(a)-1):
				t = a[j+1] - a[j]
				b.append(t)
			a = b
			b = []
			print ('A : {}'.format(a))

	s = 0
	for num in a:
		s += num
	print ('sum : {}'.format(s))

# summation()


# swapping the vowels with first and last
def swap_vowels():
	line = 'once upon a time there was a king'
	print ('original line : {}'.format(line))
	line = list(line)
	n = len(line)

	i = 0
	j = n-1
	while (i < j):
		if line[i] not in 'aeiouAEIOU':
			i = i + 1 
		elif line[j] not in 'aeiouAEIOU':
			j = j - 1
		else:
			line[i], line[j] = line[j], line[i]
			i = i + 1
			j = j - 1
		# print ('line : {}'.format(line))
	line = ''.join(line)

	print ('Result : {}'.format(line))

# swap_vowels()


# print Fibbonacie series till n numbers
#0,1,1,2,3,5,8,13

def fibbo(n):
	a = 0
	b = 1

	print (a)
	print (b)

	for i in range(n-2):
		c = a+b
		a = b
		b = c
		print c

# fibbo(10)

def fibbo1(a=0, b=1, n=10):
	c = a + b
	a = b
	b = c
	print (c)
	n = n - 1
	if n == 0:
		return
	fibbo1(a,b,n)

# fibbo1(a=5,b=7,n=5)


# check weather the given string is anagram or not.
# all characters from first string is present in second string
# both string should same if we do sort them.

def anagram():
	str1 = 'aaabcce'
	str2 = 'aabaccd'

	status = True
	str1 = sorted(list(str1))
	str2 = sorted(list(str2))

	if len(str1) != len(str2):
		print ('strings are not anagram')
		return

	for i in range(len(str1)):
		if str1[i] != str2[i]:
			status = False
			break

	if status:
		print ('Given strings are anagram')
	else:
		print('Given strings are not anagram')

# anagram()
import math
def isPrime(n):

	if n < 2:
		# print ('given number {} is not prime'.format(n))
		return
	elif n == 2:
		print ('Gieve number {} is prime'.format(n))
		return
	elif n % 2 == 0:
		# print ('given number {} is not prime'.format(n))
		return
	j = 3
	while (j <= math.sqrt(n)):
		if n % j == 0:
			# print ('given number {} is not prime'.format(n))
			return
		else:
			j += 2
	print ('Gieve number {} is prime'.format(n))

# isPrime(0)
# isPrime(-1)
# isPrime(1)
# isPrime(2)
# isPrime(3)
# isPrime(9) 

# for i in range(100):
# 	isPrime(i)


def isPalindrom():
	s = 'abc123321cba'
	s = list(s)
	l = len(s)

	i = 0
	while (i < l):
		if s[i] != s[l-1]:
			print ('Given string - {} is not palindrom'.format(''.join(s)))
			return
		else:
			i +=1
			l -=1
	print ('Given string is Palindrom')


# isPalindrom()


import re
def palindrom_test():
	a = 'a123#*bcdcb321a'
	a = list(a)

	l = len(a)
	i = 0
	while (i < l):
		if not re.search(r'[a-zA-Z0-9]', a[i]):
			i +=1
		elif not re.search(r'[a-zA-Z0-9]', a[l-1]):
			l -=1
		elif a[i] != a[l-1]:
			print ('Given string is not palindrom')
			return
		else:
			i +=1
			l -=1
	print ('String is Palindrom')

# palindrom_test()


def rotation(a, n):
	print ('Before Rotation : {}'.format(a))
	for i in range(n):
		a = a[1:] + a[:1]
		print ('A : {}'.format(a))
	print ('After rotation of numbers : {}'.format(a))

# rotation([1,2,3,4,5,6,7,8], 5)

def rotation2(a,n):
	print ('Before Rotation : {}'.format(a))
	for i in range(n):
		t = a.pop(0)
		a.append(t)
		print ('A : {}'.format(a))
	print ('After rotation of numbers : {}'.format(a))

# rotation2([1,2,3,4,5,6,7,8], 5)

# swap the elements in an array with the next following greater number of it from right side of the element.
def replace_number():
	a = [12,4,5,41,44,50,1,2,3,78,4,3,5,13]

	a = [1,2,3,4,5]
	a = [5,4,3,2,1]
	a = [12,4,5,41,44]
	print ('Original : {}'.format(a))

	i = 0
	l = len(a)

	while (i<l):
		if a[i] > a[i-1]:
			l -=1
		else:
			a[i], a[l-1] = a[l-1], a[i]
			i +=1
			l -=1
		print ('Final     : {}'.format(a))

# replace_number()

# class MyClassA(object):
# 	def __init__(self, data):
# 		self.data = data

# 	def setData(self,d):
# 		self.data = d

# 	def display(self):
# 		print ('My data is : {}'.format(self.data))

# class MyClassB(MyClassA):
# 	def display(self):
# 		print ('B data : {}'.format(self.data))

# s = MyClassB('Amitesh')
# s.display()
# s.setData('Saurabh')
# s.display()
# s.setData('Aaryan')
# s.display()

# def uppercase(func):
# 	def wrapper(*name):
# 		print ('Starting the function')
# 		res = func(*name)
# 		modified = res.upper()
# 		return modified
# 		print ('End of function')
# 	return wrapper

# @uppercase
# def greet(name):
# 	return 'hello !! {}'.format(name)

# print greet ('saurabh')


# def add_extra_10(func):
# 	def wrapper(a,b):
# 		print ('Start of the funcßtion')
# 		res = func(a,b)
# 		res = res + 10
# 		return res
# 	return wrapper


# def test1():
# 	cities = {'San Francisco': 'US', 'London':'UK',
#         'Manchester':'UK', 'Paris':'France',
#         'Los Angeles':'US', 'Seoul':'Korea'}
# 	d1 = dict()
# 	for k, v in cities.items():
# 		try:
# 			d1[v].append(k)
# 		except:
# 			d1[v] = k
# 	print (d1)

# # test1()
# from collections import defaultdict
# def test2():
# 	nums = [1,2,4,8,16,32,64,128,256,512,1024,32768,65536,4294967296]
# 	# d1 = dict()
# 	d1 = defaultdict(list)
# 	for num in nums:
# 		# try:
# 		d1[len(str(num))].append(num)
# 		# except:
# 		# 	d1[len(str(num))] = num

# 	print (d1)

# test2()

def f(n):
	for i in range(n):
		yield i**3

f(5)

import os

def file_list(dir): 
    basedir = dir
    subdir_list = []
    for item in os.listdir(dir):
        fullpath = os.path.join(basedir,item)
        if os.path.isdir(fullpath):
            subdir_list.append(fullpath)
        else:
            print fullpath

    for d in subdir_list:
        file_list(d)

file_list('/dir')
