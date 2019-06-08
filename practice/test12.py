import os

def file_list(dir):
	base_dir = dir
	sub_dir = list()
	for item in os.listdir(dir):
		fullpath = os.path.join(base_dir, item)
		if os.path.isdir(fullpath):
			sub_dir.append(fullpath)
		else:
			print (fullpath)

	for d in sub_dir:
		file_list(d)
# file_list('./')


def file_list1(dir):
	for root, dirs, files in os.walk(dir):
		for dir in dirs:
			print os.path.join(root, dir)
		for file in files:
			print os.path.join(root, file)

file_list1('./')

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

A = [1,2,3,4,5]
print solution(A)

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

for i in range(101):
	if isPrime(i):
		print i,


def test_exception():
	print ('start of the test case')
	try:
		print (0/10)
	except ZeroDivisionError:
		print ('integer division or module by zero')
	else:
		print ('Exception raised and now i have to handle the exception other then ZeroDivisionError')
	finally:
		print ('love u')

test_exception()


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
    	"{[(" : 0,
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

from collections import defaultdict
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
    				name = line[1] + str(counter) + '.' + line[0].split('.')[1]
    			elif len(cities[line[1]]) >=10 and len(cities[line[1]]) <=99:
    				if len(str(counter)) == 1:
    					counter = '0{}'.format(counter)
    				name = line[1] + str(counter) + '.' + line[0].split('.')[1]
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


def anagram():
    str1 = 'acbcdca '
    str2 = 'aabccdc'
    str1 = sorted(list(str1.strip()))
    str2 = sorted(list(str2.strip()))

    if str1 == str2:
        print ('strings are anagram')
    else:
        print ('strings are not anagram')

anagram()


def reverse():
    a = '    Saurabh    Maheshwari   '
    print ('original string : {}'.format(a))
    a = list(a)

    l = len(a)
    i = 0

    while (i < l):
        a[i], a[l-1] = a[l-1], a[i]
        i +=1
        l -=1
    a = ''.join(a)

    print ('reverse string : {}'.format(a))

reverse()

def reverse_words():
    a = ' this is the   Saurabh    Maheshwari   '
    print ('original string : {}'.format(a))
    a = a.split()

    l = len(a)
    i = 0

    t = a[:]
    t.reverse()
    print (t)
    while (i < l):
        a[i], a[l-1] = a[l-1], a[i]
        i +=1
        l -=1
    a = ' '.join(a)

    print ('reverse string : {}'.format(a))

reverse_words()


def rotate_string(str1, n):

    print ('original : {}'.format(str1))
    str1 = str1.split()
    for i in range(n):
        str1 = str1[1:] + str1[:1]

    str1 = ' '.join(str1)

    print ('result : {}'.format(str1))

rotate_string('this is my test string', 2)
rotate_string('   this     is   my test string', 2)
# rotate_string('this is ', 2)
rotate_string('this is my test string', 0)
rotate_string('this is my test string', -1)
# rotate_string('this is my test string', 20)


def max_slice_sum(A):

	if len(A) == 1:
		return A[0]

	m = A[0]
	for i in range(0,len(A)-1):
		s = A[i]
		if s > m:
			m = s
		for j in range(i+1, len(A)):
			if A[j] > m:
				m = A[j]
			s += A[j]
			if s > m:
				m = s
	return m

A = [3,2,4,-5,6,7,-10]
# A = [-2,-2]
# A = [2]
print max_slice_sum(A)
