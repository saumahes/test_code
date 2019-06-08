import re

def reverse(s=None):
	try:
		if len(s) == 0:
			print ('There is no string for testing')
			return 
	except:
		print ('There is no string for testing')
		return 

	if len(s) == 1:
		print ('Reverse of the string is : {}'.format(s))
		return
	print ('Original String : {}'.format(s))
	s = list(s)
	i = 0
	l = len(s)

	while (i < l):
		s[i], s[l-1] = s[l-1] , s[i]
		i +=1
		l -=1
	s = ''.join(s)

	print ('Reverse String : {}'.format(s))

reverse('Saurabh')
reverse()
reverse('s')
reverse('SaurabhMaheshwari')

# Needs to add elements from B to A in the sorted way. No duplicate should be in the list.
def add_sorted_list():
	a = [1,3,5,7,9,23,55]
	b = [1,3,5,7,19,20,24,100]

	i = 0
	j = 0

	l = len(a)
	m = len(b)
	while (i < len(a) and j < len(b)):
		if a[i] < b[j]:
			i +=1
		elif a[i] > b[j]:
			a.insert(i, b[j])
			j +=1
		else:
			i +=1
			j +=1

	while (j<m):
		a.append(b[j])
		j+=1

	print ('Final A : {}'.format(a))

add_sorted_list()

# get the first letter from each word from the senternce
def get_first_letter_from_words():
	import re
	res = ''
	line = '      this is my first      p.  age      of letter      from amazon.'

	l = len(line)
	i = 0

	while i < l-1:
		if re.search(r'\s',line[i]) and re.search(r'\S',line[i+1]):
			print (line[i+1])
			i +=2
		else:
			i +=1

get_first_letter_from_words()


# Toggle the letter from the sentence.
def toggle_letters():
	line = 'Saurabh1213$%@#@#@    Maheshwari Shri JAG MOhan LAl MAHESwarI'
	print ('Original Name : {}'.format(line))

	line = list(line)

	i = 0
	while (i < len(line)):
		if re.search(r'[a-z]', line[i]):
			line[i] = chr(ord(line[i])-32)
		elif re.search(r'[A-Z]', line[i]):
			line[i] = chr(ord(line[i])+32)
		i +=1

	line = ''.join(line)
	print ('After Toggle : {}'.format(line))

toggle_letters() 

# swaping the adjacents letter from the sentence
def swapping_letters():
	line = 'this is a my test case. ##$ &%$%^ SCXDS @#$ S#$# <><>'
	print ('original line : {}'.format(line))
	line = list(line)

	i = 0
	l = len(line)

	while i < l-1:
		if re.search(r'\S',line[i]) and re.search(r'\S', line[i+1]):
			line[i], line[i+1] = line[i+1], line[i]
			i +=2
		else:
			i +=1

	line = ''.join(line)

	print('Result : {}'.format(line))

swapping_letters()

# needs to swap the vowels with first and last
def swapping_vowels():
	line = 'this is the test line for swap vowels'
	print ('Original : {}'.format(line))
	line = list(line)
	i = 0
	l = len(line)

	while (i < l):
		if not line[i] in 'aeiouAEIOU':
			i +=1
		elif not line[l-1] in 'aeiouAEIOU':
			l -=1
		else:
			line[i],line[l-1] = line[l-1], line[i]
			i +=1
			l -=1
	line = ''.join(line)

	print ('Result : {}'.format(line))

swapping_vowels()

def second_largest():
	a = [234,656,334,678,43434,7878,343,54,232,56]
	first = second = min(a)

	for num in a:
		if num > first:
			second = first
			first = num
		elif num > second:
			second = num

	print ('second largest number is : {}'.format(second))

second_largest()

def third_largest():
	a = [234,656,334,678,43434,7878,343,54,232,56]
	first = second = third = None

	for num in a:
		if num > first:
			third = second
			second = first
			first = num
		elif num > second:
			third = second
			second = num
		elif num > third:
			third = num

	print ('third largest number is : {}'.format(third))

third_largest()


def rotation(a,n):
	print ('Original String - {}'.format(a))
	for i in range(n):
		a.append(a.pop(0))
	print ('After rotation of list {} -'.format(a))

a = [1,2,3,4,5,6,7,8,9]
n = 5
rotation(a,n)


def rotation_forward(a,n):
	print ('Original : {}'.format(a))
	change = False
	if type(a) !=list:
		change = True
		a = list(a)

	for i in range(n):
		a = a[1:] + a[:1]
	if change:
		a = ''.join(a)

	print ('Result : {}'.format(a))
rotation_forward([1,2,3,4,5],3)
rotation_forward('ABCDEF',3)


def rotation_backward(a,n):
	print ('Original : {}'.format(a))
	change = False
	if type(a) !=list:
		change = True
		a = list(a)

	for i in range(n):
		a = a[-1:] + a[:-1]
	if change:
		a = ''.join(a)

	print ('Result : {}'.format(a))
rotation_backward([1,2,3,4,5],3)
rotation_backward('ABCDEFGHIJ',3)


import datetime

class EnterExitLog():
    def __init__(self, funcName):
        self.funcName = funcName

    def __enter__(self):
        print ('Started: %s' % self.funcName)
        self.init_time = datetime.datetime.now()
        return self

    def __exit__(self, type, value, tb):
        print('Finished: %s in: %s seconds' % (self.funcName, datetime.datetime.now() - self.init_time))

def func_timer_decorator(func):
    def func_wrapper(*args, **kwargs):
        with EnterExitLog(func.__name__):
            return func(*args, **kwargs)
    return func_wrapper

@func_timer_decorator
def my_func():
	pass

my_func()

def greetings(func):
	def wrapper(*args):
		print ('Start of the function - {}'.format(func.__name__))
		res = func(*args)
		return res
		print ('End of the function')
		
	return wrapper

@greetings
def add(a,b):
	return a+b

s = add(10,4)
print ('sum of {} and {} is {}'.format(10,4,s))


from collections import defaultdict
def test2():
	nums = [1,2,4,8,16,32,64,128,256,512,1024,32768,65536,4294967296]
	d1 = defaultdict(list)
	for num in nums:
		d1[len(str(num))].append(num)
	print (d1)

test2()

def frequency_finder():
	nums = [1,2,4,8,16,32,64,128,256,512,1024,32768,65536,4294967296]
	d = dict()

	for num in nums:
		try:
			d[len(str(num))].append(num)
		except:
			d[len(str(num))] = [num]
	print (d)

frequency_finder()

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

# file_list('/Users/smaheshwari/')

from collections import defaultdict

def frequency_of_characters():
	line = 'This is the test line to find the frequency of each and every letters.'
	d = defaultdict(int)

	for char in line:
		d[char.lower()] +=1

	for key in d:
		print ('{} : {}'.format(key, d[key]))

frequency_of_characters()


# Maximum sum in circular array such that no two elements are adjacent
def sum_of_non_adjacents():
	a = [1, 2, 3, 4, 5, 6, 7, 8, 1]
	a = [1,1,1,1,1,1,1,1,1,1,1]
	sub_list = [a[0]]

	s = 0

	for num in a:
		if not (num in sub_list or (num-1)  in sub_list or (num+1)  in sub_list):
			sub_list.append(num)

	for i in sub_list:
		s +=i
	print ('the sum of all non-adjacent numbers : {} is : {}'.format(sub_list, s))

sum_of_non_adjacents()


add =lambda a,b : a + b


print map(add,[1,2,3],[3,2,1])
print (add (4,3))


def my_file_test():
	with open('ttest.txt', 'w') as f:
		f.write('This is my first file\n')
		f.write('this is my second line\n')
		f.write('this is my third line\n')

	with open('ttest.txt', 'r') as f:
		for line in f:
			print (line.upper())
my_file_test()


def os_walk():
	import os
	for root, dirs, files in os.walk(".", topdown=False):
	    for file in files:
	        print(os.path.join(root, file))
	    for dir in dirs:
	        print(os.path.join(root, dir))

os_walk()

# find the missing number from the list of numbers.
def solution(A):
    m = max(A)
    s = sum(range(min(A), m+1))
    print (s)
    s1 = 0
    for num in A:
        s1 +=num
    print s1
    if s1 == s:
    	return m+1
    else:
    	return s - s1

A = [1,2,3,5]
print solution(A)

A = [1,3,5,6,7,9]
def solution1(A):
	diff = list()
	for i in range(len(A)-1):
		s1 = 0
		s2 = 0
		for j in range (i+1, len(A)):
			s2 +=A[j]
		for k in range(i+1):
			s1 +=A[k]

		diff.append(abs(s1-s2))
		print ('difference : {}'.format(diff))
	res = min(diff)
	return res

solution1(A)


def check_permutation(A):

	if len(A) == 1:
		return 0
	A.sort()
	i = 0
	while (i<len(A)-1):
		if A[i+1] - A[i] != 1:
			return 0
		i +=1
	return 1
A = [1]
print check_permutation(A)


def remove_duplicate(A):
	i = 0

	while i < len(A)-1:
		j = i+1
		while (j<len(A)):
			if A[i] == A[j]:
				A.pop(j)
			else:
				j +=1
		i +=1

	print (A)

A = [1,2,3,4,2,1,2,4,3,2,1]
# A = [1,1,1,1,1,1]

remove_duplicate(A)

# 1000010000000

n = 525000
def dec_to_bin(n):
	res = ''
	tmp = n
	while n > 0:
		res = str(n%2) + res
		n = n//2
	print ('{} to {}'.format(tmp, res))

dec_to_bin(n)

def binary_gap(n):
	count = 0
	max_count = 0
	flag = False
	while n > 0:
		if n%2 == 1:
			flag = True
			if count > max_count:
				max_count = count
				count = 0
		else:
			if flag:
				count +=1
		n = n/2

	print ('gap count : {}'.format(max_count))
binary_gap(n)


def solution1234(T, R):
    import re
    ok_counter = 0
    from collections import defaultdict
    res_dict = defaultdict(list)
    i = 0
    while i < len(T):
        test_group = filter(str.isdigit, T[i])
        res_dict[test_group].append(R[i])
        i +=1
    
    number_of_group = res_dict.keys()
    result_lists = list(res_dict.values())
    
    for res in result_lists:
        if not ("Wrong answer" in res or  "Runtime error" in res or  "Time limit exceeded" in res):
            ok_counter +=1
            
    final_res = int(ok_counter*100/len(number_of_group))
    
    return final_res

T = ['test1a', 'test2', 'test1b', 'test1c', 'test3']
R = ['Wrong answer', 'OK', 'Runtime error', 'OK', 'Time limit exceeded']

print solution1234(T,R)

import math
def isPrime(n):
	status = True
	if n < 2:
		return False
	elif n == 2:
		return True
	elif n % 2 == 0:
		return False
	else:
		for i in range(3, int(math.sqrt(n)) + 1, 2):
			if n%i == 0:
				return False
	return True


def find_cofactors(n):
	cofactor_counter = 0
	if isPrime(n):
		return 2
	else:
		for i in range(1,n+1):
			if n % i == 0:
				cofactor_counter +=1
	return cofactor_counter

print find_cofactors(24000)


def test_exception():
	print ('start of the test case')
	try:
		print (40/0)
	except ZeroDivisionError:
		print ('integer division or module by zero')
	else:
		print ('Exception raised and now i have to handle the exception other then ZeroDivisionError')
	finally:
		print ('love u')

test_exception()

def raise_exception():
	x = 5
	if x < 10:
		raise Exception('number {} is less then 10'.format(x))

raise_exception()

# class FileNotFoundError1:
# 	pass

# class FileNotFoundError:
# 	pass

def read_and_write_file():
	try:
		with open('readme.txt', 'r') as f:
			data = f.read()
			print (data)
	except FileNotFoundError as err:
		print ('unable to find the find the file')
	# except FileNotFoundError1 as err:
	# 	print (err)
	except IOError as err:
		print ('this is the error while reading the file : {}'.format(err))
	else:
		print ('unable to open the file ..')
	finally:
		with open('readme.txt', 'a') as f:
			f.write('1. Hello Saurabh what is going on in your life.\n')
			f.write('2. Need to get a new job as soon as possible\n')
			f.write('3. trying to find some better position in cisco or amazon or any good org\n')

		with open('readme.txt','r') as f:
			for line in f:
				print (line)


# read_and_write_file()


def read_and_create_sep_file():
	try:
		with open('readme.txt' ,'r') as f:
			for line in f:
				if '1' in line:
					with open('readme1.txt','a') as f1:
						f1.write(line)
				elif '2' in line:
					with open('readme2.txt','a') as f2:
						f2.write(line)
				elif '3' in line:
					with open('readme3.txt','a') as f3:
						f3.write(line)
	except IOError as err:
		print ('error is : {}'.format(err))
	else:
		print ('something is wrong with this file.. please take a look')
	finally:
		try:
			with open('readme1.txt','r') as f1:
				data = f1.read()
				data = data.split('\n')
				print ('number of line in data : {}'.format(len(data)))
				for line in data:
					print (line)
		except IOError as err:
			print (err)
		try:
			with open('readme2.txt', 'r') as f2:
				print (f2.readlines())
		except IOError as err:
			print (err)
		try:
			with open('readme3.txt','r') as f3:
				for line in f3:
					print (line)
		except IOError as err:
			print (err)

read_and_create_sep_file()


def action(x):
	return (lambda y : x + y)

res = action(10)
res2 = res(30)
print (res2)

action2 = lambda x:(lambda y: x+y)

import re
def test_reg():
	string = "           This is my        name        saurabh          maheshwari                    "
	string = re.sub(r'\s{2,}', r'\s',string).strip()
	if string:
		print ('result : {}'.format(string))

	line = list(string)

	l = len(line)
	i = 0
	while (i < l-1):
		if re.search(r'[a-z]',line[i+1]) and re.search(r'\s',line[i]):
			line[i+1] = (line[i+1]).upper()
			i = i+2
		else:
			i +=1
	string = ''.join(line)
	print (string)

test_reg()


def test_reg2():
	line = "this is my phone number 425-633-4144"
	line = re.sub(r'[a-zA-Z]+','',line)
	print (line)
	# line = line.strip()
	line = line.strip().split('-')
	line = '(' + str(line[0]) + ')' + line[1] + '-' + line[2]
	print (line)

test_reg2()


def remove_item():
	a = [1,1,1,1,1,1,1,1,1,1,1]
	print (a)
	i = 0
	l = len(a)

	for i in range(len(a)-1):
		j = i + 1
		while (j < len(a)):
			if a[i] == a[j]:
				a.pop(j)
			else:
				j +=1
	print (a)
remove_item()


def os_walk():
	import os
	for root, dirs, files in os.walk(".", topdown=False):
	    for file in files:
	        print(os.path.join(root, file))
	    for dir in dirs:
	        print(os.path.join(root, dir))

# os_walk()


#  year%4 and not year%100 and year%400
def is_leap_year(year):
	leap_year = False
	if year % 4 == 0:
		leap_year = True
		if year % 100  == 0:
			leap_year = False
			if year % 400 == 0:
				leap_year = True

	return leap_year

print ('list of leap years : ')
for year in range(1900,2019):
	if is_leap_year(year):
		print (year)


def read_yaml_file():
	try:
		yaml_file = os.path.join(os.getcwd(), 'config.yaml')
		print (yaml_file)

		with open(yaml_file, 'r') as stream:
		    data_loaded = yaml.load(stream)

		# with open(yaml_file, 'r') as f:
		# 	d = yaml.load(f)
		print (data_loaded)
	except:
		print ('file not found')
		raise Exception ('Please check the file ..')

# # read_yaml_file()
# import yaml
# import io
# def read_yaml_file1():
# 	try:
# 		yaml_file = os.path.join(os.getcwd(), 'config.yaml')
# 		print (yaml_file)

# 		with open(yaml_file, 'r') as stream:
# 		    data_loaded = yaml.load(stream)

# 		# with open(yaml_file, 'r') as f:
# 		# 	d = yaml.load(f)
# 		print (data_loaded) # its a dictionary type
# 	except:
# 		print ('file not found')
# 		raise Exception ('Please check the file ..')

# read_yaml_file1()

import argparse
def read_arguments():
	parser = argparse.ArgumentParser('Reading ArgumentParser')
	parser.add_argument('--name', default="Saurabh", help="Enter your name")
	parser.add_argument('--age', default=40, help="enter your age")
	print (parser.parse_args())
	return parser.parse_args()

def main():
	args = read_arguments()
	print ('your name : {}'.format(args.name))
	print ('Age : {}'.format(args.age))

if __name__ == '__main__':
	main()


# >>> import datetime
# >>> datetime.datetime.now
# <built-in method now of type object at 0x10b963588>
# >>> datetime.datetime.now()
# datetime.datetime(2019, 4, 13, 19, 14, 31, 541791)
# >>> print datetime.datetime.now()
# 2019-04-13 19:14:51.494242
# >>> print datetime.datetime.now()
# 2019-04-13 19:14:54.505727
# >>> print datetime.datetime.now().time
# <built-in method time of datetime.datetime object at 0x10b97fcd8>
# >>> print datetime.datetime.now().time()
# 19:15:07.510434
# >>> print datetime.datetime.now().date()
# 2019-04-13


def reverse_rotation(s='Saurabh',n=4):
	print ('Original String : {}'.format(s))
	s = list(s)
	for i in range(n):
		s = s[-1:] + s[:-1]
	s = ''.join(s)

	print ('After rotation: {}'.format(s))

reverse_rotation()

# swap the elements in an array with the next following greater number of it from right side of the element.
def replace_number():
	a = [12,4,5,41,44,50,1,2,3,78,4,3,5,13]
	# a = [1,2,3,4,5,6,7,8,9]
	i = 0
	l = len(a)

	while (i < l):
		if (a[i] >= a[l-1]):
			l -=1
		else:
			a[i] , a[l-1] = a[l-1], a[i]
			i +=1
			l -=1
	print ('Iteration - {}: {}'.format(i, a))
replace_number()


print map((lambda a,b: a+b), [1,2,3,4],[5,6,7,8])

def IsNested(s):
    stack = []
    for x in s:
        if x in ['(', '{', '[']:
            stack.append(x)
        elif x in [')', '}', ']']:
            if len(stack) == 0:
                return 0
            # Pop an element to see if matches
            y = stack.pop()
            if x == ')' and y != '(':
                return 0
            elif x == ']' and y != '[':
                return 0
            elif x == '}' and y != '{':
                return 0
    if len(stack) > 0:
    	return 0
    return 1     
    
if __name__ == '__main__':
    # Define Test Cases
    testcases = {
    	"{{{{{": 0,
        "([)()]": 0,
        "{[()()]}": 1,
        "": 1,
        "{}": 1,
        "[]()": 1,
        ")(": 0,
        "}{()": 0,
        "()[}": 0      
    }
    
    for test in testcases.keys():
        assert testcases[test] == IsNested(test), "Test " + test + " Failed"
    
    print ("All OK.")


def rotation3(a,n):
	for i in range(n):
		a = a[1:] + a[:1]

	print (a)
a = [1,2,3]
n = 5
rotation3(a,n)


def os_walk1():
	import os
	for root, dirs, files in os.walk("../../"):
	    for file in files:
	        print(os.path.join(root, file))
	    for dir in dirs:
	        print(os.path.join(root, dir))

# os_walk1()


# Maximum sum in circular array such that no two elements are adjacent
def sum_of_non_adjacents1():
	a = [1, 2, 3, 4, 5, 6, 7, 8, 1]
	sub_list = list()
	sub_list.append(a[0])

	for num in a:
		if not (num in sub_list or num-1 in sub_list or num+1 in sub_list):
			sub_list.append(num)

	print (sub_list)
	s = 0
	for num in sub_list:
		s +=num
	print ('non adjacent sum is : {}'.format(s))

sum_of_non_adjacents1()



import re
def test_reg1():
	string = "           This is my        name        saurabh          maheshwari                    "
	string = re.sub(r'\s{2,}', r'\s',string).strip()
	if string:
		print ('result : {}'.format(string))

test_reg1()


def ip_address_validate(ipaddr):
	status = False
	try:
		ipaddr = ipaddr.split('.')
		if len(ipaddr) != 4:
			return False
		try:
			for item in ipaddr:
				if not (int(item) >= 0 and int(item) <= 255):
					return False
		except:
			return False

	except:
		return False
	return True

if __name__ == '__main__':
	testcases = {
	'1.1.1.1':True,
	'12.32.434.43':False,
	'a.b.c.4':False,
	'saurabh':False,
	'':False,
	'1232':False,
	'255.255.255.255':True,
	'0.0.0..':False,
	'1.2.3.a':False,
	'254.255.256.1':False
	}
	for test in testcases.keys():
		assert ip_address_validate(test) == testcases[test], "Test" + test + "Falsed"

	print ('All test passed')

def highest_freq_of_letter():
	line = 'This is my test case to find out the frequecy of letters aaaaaaaaaa'
	line = re.sub(r'\s{1,}','',line)
	res_dict = defaultdict(int)
	line = list(line)
	m = 0
	res = ''
	for c in line:
		res_dict[c] +=1
		if res_dict[c] > m:
			m = res_dict[c]
			res = c
	print ('The highest frequecy letter is  {} and its frequecy is {}'.format(res,m))

highest_freq_of_letter()

def a(x):
	return lambda y:x+y

b = a(10)
print ('type of b : {}'.format(b))
c = b(20)

print c

###############


from collections import defaultdict
import re
from datetime import datetime

def pictures_sorting(S):
    s = S.split('\n')
    cities = defaultdict(list)
    for line in s:
        line = line.split(',')
        d1 = datetime.strptime(line[2].strip(),"%Y-%m-%d %H:%M:%S")
        cities[line[1]].append(d1)

    for city, datetimes in cities.items():
    	cities[city] = sorted(datetimes)


    for line in s:
    	line = line.split(',')
    	d1 = datetime.strptime(line[2].strip(),"%Y-%m-%d %H:%M:%S")
    	counter = 1
    	values = cities[line[1]]
    	for val in values:
    		if d1 == val:
    			if len(cities[line[1]]) < 10:
    				name = line[1]+str(counter) +'.' + line[0].split('.')[1]
    			elif len(cities[line[1]]) >=10 and len(cities[line[1]]) <=99:
    				if len(str(counter)) == 1:
    					counter = '0{}'.format(counter)
    				name = line[1]+str(counter) +'.'+ line[0].split('.')[1]
    			counter = 0
    			print (name)
    			break
    		else:
    			counter +=1




S = """photo.jpg, Warsaw, 2013-09-05 14:08:15
john.png, London, 2015-06-20 15:13:22
myFriends.png, Warsaw, 2013-09-05 14:07:13
Eiffel.jpg, Paris, 2015-07-23 08:03:02
pisatower.jpg, Paris, 2015-07-22 23:59:59
BOB.jpg, London, 2015-08-05 00:02:03
notredame.png, Paris, 2015-09-01 12:00:00
me.jpg, Warsaw, 2013-09-06 15:40:22
a.png, Warsaw, 2016-02-13 13:33:50
b.jpg, Warsaw, 2016-01-02 15:12:22
c.jpg, Warsaw, 2016-01-02 14:34:30
d.jpg, Warsaw, 2016-01-02 15:15:01
e.png, Warsaw, 2016-01-02 09:49:09
f.png, Warsaw, 2016-01-02 10:55:32
g.jpg, Warsaw, 2016-02-29 22:13:11"""
pictures_sorting(S)

 # Warsaw02.jpg
 # London1.png
 # Warsaw01.png
 # Paris2.jpg
 # Paris1.jpg
 # London2.jpg
 # Paris3.png
 # Warsaw03.jpg
 # Warsaw09.png
 # Warsaw07.jpg
 # Warsaw06.jpg
 # Warsaw08.jpg
 # Warsaw04.png
 # Warsaw05.png
 # Warsaw10.jpg

add = lambda x,y : x+y

print add(10,30)

def b(n):
	return lambda x: x+n

c = b(10)
a = c(20)

print a

def  isArray_Balanced(arr):
    l = len(arr)
    i = 0
    sum_left = arr[i]
    sum_right = arr[l-1]
    
    while (i < l ):
        if sum_left > sum_right:
            l -=1
            sum_right += arr[l-1]
        elif sum_right > sum_left:
            i +=1
            sum_left +=arr[i]
        else:
            return (i+1)
        print ('i : {}'.format(i))
        print ('l : {}'.format(l-1))
        print ('sum1 : {}'.format(sum_left))
        print ('sum_right : {}'.format(sum_right))
        
    return -1
arr = [1,2,3,3]
print isArray_Balanced(arr)



def  removeNodes(list1, x):
	l = len(list1)

	i = 0
	while (i < len(list1)):
		if list1[i] > x:
			list1.pop(i)
		else:
			i +=1
	return list1

print removeNodes([1,2,3,4,5,6,7,8,9],4)
import re


class Mystr():
	def __init__(self, string1):
		self.string1 = string1 

	def __sub__(self,substr):
		return str(re.sub(substr,'',self.string1))

	def __add__(self, substr):
		return str('saurabh ' + self.string1 + ' ' + substr)

mstr = Mystr('Hello')
print mstr - 'llo'

print mstr + 'how are you'



import math
from datetime import datetime
def my_shuffle(list1):
	l = len(list1)
	i = 0
	sub_list = []
	while i < l:
		second = datetime.now().second
		counter = int(math.sqrt(i*second)) * second*10
		while counter > len(list1)-1:
			counter = int(math.sqrt(counter)/2*second)
			print ('counter : {}'.format(counter))
		list1[i],list1[counter] = list1[counter],list1[i]			
		list1.reverse()
		i +=1
	return list1

l1 = range(1,53)
print my_shuffle(l1)


# New Year Chaos:

def check_chaos():
	a = [1,3,5,4,2]
	a = [2,1,5,3,4]
	a = [2,5,1,3,4]
	counter = 0
	l = len(a)
	i = 0

	while i < l-1:
		j = i+1
		while j<l:
			if a[i] > a[j]:
				counter +=1
				a[i] ,a[j] = a[j],a[i]
			j +=1
		i +=1
		print (a)
	print ('counter : {}'.format(counter))

check_chaos()


class Mystr():
	def __init__(self, string1):
		self.string1 = string1 

	def __sub__(self,substr):
		return str(re.sub(substr,'',self.string1))

	def __add__(self, substr):
		return str(self.string1 + ' '+ substr)

	def __iadd__(self, substr):
		self.string1 = self.string1 + ' ' + substr
		return str(self.string1)

mstr = Mystr('Hello')

a = mstr - 'llo'
print a
print mstr.string1

a =  mstr + 'how are you'

print a
print mstr.string1

mstr +='Aaryan'

print mstr


def plusMinus(arr):
    pos = [num for num in arr if num >=0]
    neg = [num for num in arr if num <0]
    zero = [num for num in arr if num ==0]
    print (pos)
    pper = len(pos)/float(len(arr))
    nper = len(neg)/float(len(arr))
    zper = len(zero)/float(len(arr))

	# print pper
    print nper
    print zper
    return pper, nper, zper

plusMinus([-4,3,-9,3,0,1])

def staircase(n):
    i = 0
    j = 0
    k = 0
    while i<n:
        j = 0
        while j < n-i-1:
            print ' ',
            j +=1
        k = 0
        while k < i+1:
            print '#',
            k+=1
        print ''
        i +=1

staircase(6)



def staircase1(n):
    i = 0
    j = 0
    k = 0
    while i<n:
        j = 0
        while j<n-i-1:
            print '',
            j +=1
        k = 0
        t=''
        while k < i+1:
            t +='#'
            k+=1

        print t
        i +=1

staircase1(6)

def timeConversion(s):
    addme = False
    s = s.split(':')
    if 'PM' in s and int(s[0]) !=12:
        s[0] = str(int(s[0]) + 12)
    if int(s[0]) == 12 and not 'PM' in s[2]:
        s[0] = '00'
    s[2] = re.sub(r'\D+','',s[2])
    s = ':'.join(s)
    return s

print timeConversion('12:45:54PM')


import itertools

class Customer(object):
	cust_id = 0
	# cust_id = itertools.count().next
	def __init__(self, name):
		self.name = name
		# self.cust_id = Customer.cust_id()
		self.cust_id = Customer.cust_id 
		Customer.cust_id +=1

class Bank_Account(Customer): 
    def __init__(self, name): 
    	super(Bank_Account,self).__init__(name)
        self.balance=0
        print("Hello {} !!! Welcome to Banking system Machine".format(self.name)) 
  
    def deposit(self):
    	try: 
        	amount=float(input("Enter amount to be Deposited: ")) 
        except:
        	raise Exception('Entered input is not interger or float')
        self.balance += amount 
        print("Amount Deposited: {}".format(amount)) 
  
    def withdraw(self): 
    	try:
        	amount = float(input("Enter amount to be Withdrawn: ")) 
        except:
        	raise Exception ('Eterned value isnot interger')

        if self.balance>=amount: 
            self.balance-=amount 
            print("You Withdrew:", amount) 
        else: 
            print("Insufficient balance  ") 
  
    def display(self): 
        print("your id: {} Name: {} and his Net Available Balance: {} ".format(self.cust_id, self.name,self.balance)) 

# b1 = Bank_Account('saurabh')
# b1.deposit()
# # b1.deposit()
# b1.display()
# b1.withdraw()
# b1.display()

# b2 = Bank_Account('Aaryan')
# b2.deposit()
# b2.display()
# b2.withdraw()
# b2.display()




import re
def swapping_chars():
  a = '     this is my first test         today.'
  print ('original string : {}'.format(a))
  a = list(a)
  l = len(a)

  i = 0
  while (i < l-1):
    if re.search(r'\S',a[i]) and re.search(r'\S',a[i+1]):
      a[i], a[i+1] = a[i+1], a[i]
      i +=2
    else:
      i +=1
  a = ''.join(a)
  print ('updated string : {}'.format(a))
swapping_chars()


def swapping_numbers():
  a = [1,2,3,4,5,6,7,8]

  l = len(a)
  count = l if l%2 == 0 else l-1

  i = 0
  while (i < count):
    a[i], a[i+1] = a[i+1], a[i]
    i +=2
  print (a)

swapping_numbers()

# swappinng first vowels from last vowels
def swapping_vowels():
    a = 'this is my test strings'
    a = ' a e i o u i k a e'
    print ('original string : {}'.format(a))
    a = list(a)

    l = len(a)
    i = 0
    while (i<l):
        if not a[i].lower() in 'aeiou':
            i +=1
        elif not a[l-1].lower() in 'aeiou':
            l -=1
        else:
            a[i], a[l-1] = a[l-1], a[i]
            i +=1
            l -=1
    a = ''.join(a)
    print ('updated string : {}'.format(a))

swapping_vowels()

# validate two strings are anagram.
def anagram():
    str1 = 'acbcdca '
    str2 = 'aabccdc'
    str1 = sorted(list(str1.strip()))
    str2 = sorted(list(str2.strip()))

    if len(str1) != len(str2):
        print ('strings are not anagram')
        return
    status = True
    i = 0
    while i < len(str1):
        if str1[i] != str2[i]:
            status = False
            break
        else:
            i +=1

    if status:
        print ('strings are anagram')
    else:
        print ('strings are not anagram')

anagram()


def check_palindrom():
    a = 'aa'
    a = list(a)
    l = len(a)
    i = 0
    status = True
    while (i < l/2):
        if a[i] != a[l-1-i]:
            status = False
            break
        else:
            i +=1

    if status:
        print ('string is palindrom')
    else:
        print ('not palindrom')

check_palindrom()

def reverse():
    a = '    Saurabh    Maheshwari   '
    print ('original string : {}'.format(a))
    a = list(a)
    print (a)
    l = len(a)
    i = 0

    while (i < l/):
        a[i], a[l-1] = a[l-1], a[i]
        i +=1
    a = ''.join(a)

    print ('reverse string : {}'.format(a))

reverse()

def array_sum_mix_max_diff_1():
    # a = [3, 3, 1,4, 4, 5, 6]
    # a = [7, 7, 7]
    a = [1,9,2, 8, 8, 9, 9, 10]


def is_leap(year):
    leap = False
    
    # Write your logic here
    if year%4 ==0:
        leap = True
        if year%100 ==0:
            leap = False
            if year %400==0:
                leap = True

    
    return leap
print is_leap(200)

# swap the elements in an array with the next following greater number of it from right side of the element.
def replace_number():
    a = [12,4,5,41,44,50,1,2,3]#,78,4,3,5,13]
    # outcome should be : [50,44,41,41,44,50,1,2,3]
    print ('original : {}'.format(a))
    l = len(a)
    i = 0
    while (i<l):
        if a[i] > a[l-1]:
            l -=1
        else:
            a[i], a[l-1] = a[l-1], a[i]
            i +=1
            l -=1
    print ('result : {}'.format(a))

replace_number()
import math
def isPrime(n):
    status = True
    if n < 2:
        status = False

    elif n == 2:
        status = True
    elif n %2 == 0:
        status = False
    else:
	    for i in range(3, int(math.sqrt(n))+1,2):
	        if n%i == 0:
	            status = False
	            break
    if status:
        print ('I am prime')
    else:
        print ('not prime')
isPrime(57)

# objective: we need to move numbers from b to a in a sorted order.
def add_sorted_list1():
    a = [1,3,5,7,9,23,55,111,112,119,120,121]
    b = [1,3,5,7,19,20,24,100,101,104,108,120]

    print (a)
    print (b)

    i = j = 0
    l = len(a)
    m = len(b)

    while (i<len(a) and j<len(b)):
        if a[i] == b[j]:
            i +=1
            j +=1
        elif a[i] < b[j]:
            i +=1
        else:
            a.insert(i, b[j])
            j +=1

    if j<m:
        for k in range(j,m):
            a.append(b[k])

    print ('result : {}'.format(a))

add_sorted_list1()

def rotate_string(str1, n):

    print ('original : {}'.format(str1))
    str1 = str1.split()
    for i in range(n):
        str1 = str1[1:] + str1[:1]

    str1 = ' '.join(str1)

    print ('result : {}'.format(str1))

rotate_string('this is my test string', 2)
rotate_string('   this     is   my test string', 2)
rotate_string('this is ', 2)
rotate_string('this is my test string', 0)
rotate_string('this is my test string', -1)
rotate_string('this is my test string', 20)


def meta_string():
    s1 = 'geeks'
    s2 = 'keegs'

    if len(s1) != len(s2):
        print ('strings are not meta strings')
        return

    if s1 == s2:
        print ('strings are not meta strings')
        return

    s1 = list(s1)
    s2 = list(s2)

    i = 0
    l = len(s1)
    count = 0
    mis_match_s1 = list()
    mis_match_s2 = list()

    while (i < l):
        if s1[i] != s2[i]:
            count +=1
            mis_match_s1.append(s1[i])
            mis_match_s2.append(s2[i])

        i +=1
    if count == 2:
        if mis_match_s1[0] == mis_match_s2[1] and mis_match_s1[1] == mis_match_s2[0]:
            print ('strings are meta strings')
        else:
            print ('not meta strings')
    else:
        print ('not meta strings')


meta_string()


def isPalindrom():	
    string1 = 'abcdegdcba'
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

def binary_search(num):
    a = range(50)
    begin = 0
    end = len(a)
    found = False

    while (begin < end and not found):
        mid = (begin + end)/2
        if a[mid] > num:
            end = mid - 1
        elif a[mid] < num:
            begin = mid + 1 
        else:
            found = True
    if found:
        print ('{} found in the list.'.format(num))
    else:
        print ('not found')

binary_search(5)

#  In general, the local part can have these ASCII characters:

# lowercase Latin letters: abcdefghijklmnopqrstuvwxyz,
# uppercase Latin letters: ABCDEFGHIJKLMNOPQRSTUVWXYZ,
# digits: 0123456789,
# special characters: !#$%&'*+-/=?^_`{|}~,
# dot: . (not first or last character or repeated unless quoted),
# space punctuations such as: "(),:;<>@[\] (with some restrictions),
# comments: () (are allowed within parentheses, e.g. (comment)john.smith@example.com).
# Domain part:

# lowercase Latin letters: abcdefghijklmnopqrstuvwxyz,
# uppercase Latin letters: ABCDEFGHIJKLMNOPQRSTUVWXYZ,
# digits: 0123456789,
# hyphen: - (not first or last character),
# can contain IP address surrounded by square brackets: jsmith@[192.168.2.1] or jsmith@[IPv6:2001:db8::1].


def validate_email_address(s):
	res = s.rsplit('@',1)
	if len(res) != 2:
		return False
	local = res[0]
	domain = res[1]

	print ('local : {}'.format(local))
	print ('domain : {} and test'.format(domain))
	if local.startswith('.') or local.startswith(' ') or local.endswith(' ') or local.endswith('.') or local.startswith('-') or local.endswith('-'):
		return False
	if '@' in local or ' ' in local:
		if not (local.startswith('"') and local.endswith('"')) or (local.startswith("'") and local.endswith("'")):
			return False
	if not local.startswith('"'):
		if '"' in local:
			return False
	if '..' in domain:
		return False
	return True



if __name__ == '__main__':
	testcases = {
"prettyandsimple@example.com":True,
"very.common@example.com":True,
"disposable.style.email.with+symbol@example.com":True,
"other.email-with-dash@example.com":True,
"x@example.com (one-letter local part)":True,
'"much.more unusual"@example.com':True,
'"very.unusual.@.unusual.com"@example.com':True,
'"very.(),:;<>[]\".VERY.\"very@\ \"very\".unusual"@strange.example.com':True,
'example-indeed@strange-example.com':True,
'admin@mailserver1 (local domain name with no top-level domain)':True,
"#!$%&'*+-/=?^_`{}|~@example.org":True,
'''"()<>[]:,;@\\"!#$%&'-/=?^_`{}| ~.a"@example.org''':True,
'" "@example.org (space between the quotes)':True,
'example@localhost (sent from localhost)':True,
'example@s.solutions (see the List of Internet top-level domains)':True,
'user@com':True,
'user@localserver':True,
'user@[IPv6:2001:db8::1]':True,


'Abc.example.com':False, #(no @ character)':False,
'A@b@c@example.com':False,
'a"b(c)d,e:f;gi[j\k]l@example.com':False,
'just"not"right@example.com':False, #(quoted strings must be dot separated or the only element making up the local part)
'this is"not\allowed@example.com':False, #(spaces, quotes, and backslashes may only exist when within quoted strings and preceded by a backslash)
'this\ still\"not\allowed@example.com':False, #(even if escaped (preceded by a backslash), spaces, quotes, and backslashes must still be contained by quotes)
'john.doe@example..com':False, #(double dot after @)
' infosaurabh@gmail.com':False,
'infosaurabnh1 @gmail.com     ':False #a valid address with a trailing space'
	}
	for test in testcases.keys():
		print 'Email address - {}'.format(test)
		assert validate_email_address(test) == testcases[test], "Test " + test + " Falsed"



def is_substring():
	main = 'Saurabh Maheshwari'
	sub = 'hwai '

	i = 0
	j = 0

	while (i<len(main) and j<len(sub)):
		if main[i] == sub[j]:
			i+=1
			j+=1
		else:
			i+=1
			j=0

	if j == len(sub):
		return True
	else:
		return False

print is_substring()


class b:
	def __init__(self, x): 
		print ('i am init')
		self.x = x
	def __call__(self, y):
		print ('Hi, i am call')
		return self.x +y

c = b(10)
a = c(20)
print a