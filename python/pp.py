def rotation():
	line = 'this is my test line'
	line = line.split()
	n = 2

	for i in range(n):
		line =  line[-1:] + line[:-1]

	line = ' '.join(line)

	print (line)

rotation()

import os
def file_list(dir):
	sub_dir = []

	base_dir = dir
	for item in os.listdir(dir):
		fullpath = os.path.join(base_dir, item)
		if os.path.isdir(fullpath):
			sub_dir.append(fullpath)
		else:
			print(fullpath)
	for item in sub_dir:
		file_list(item)

file_list('./')


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
		return str('saurabh ' + self.string1 + ' '+ substr)

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
		counter = int(math.sqrt(i)) * second*10
		while counter >len(list1)-1:
			counter = int(math.sqrt(counter)/2)
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















