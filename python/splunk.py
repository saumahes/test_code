def binary_gap(n):

	max_gap = 0
	status = False
	counter = 0
	bin = ''
	while n > 0:
		bin =  bin + str(n%2)
		if n % 2 == 1:
			status = True
			if counter > max_gap:
				max_gap = counter
				counter = 0

		else:
			if status:
				counter +=1
		

		print('n : {} counter : {} and max_gap : {} binary : {}'.format(n, counter, max_gap,bin))
		n = int(n / 2)
	return max_gap



	print ('gap count : {}'.format(max_count))


n = 1376796946
n = 11098
n = 346
n = 173
n = 43

print binary_gap(n)

def binary(n):
	bin = ''

	while n>0:
		bin = str(n%2) + bin
		n = int (n/2)
	# print (bin)

binary(n)


# that, given an array A consisting of N integers,  returns the value of the unpaired element.
from collections import defaultdict
def find_unpaired(A):
	d = defaultdict(int)

	for num in A:
		d[num] +=1

	for key in d:
		if d[key] %2 ==1:
			return key

A = [9,3,9,3,9,7,9]
find_unpaired(A)

# Write a function:

# def solution(X, Y, D)

# that, given three integers X, Y and D, returns the minimal number of jumps from position X to a position equal to or greater than Y.

def count_frog_jump_count(X, Y, D):

	distance = Y - X
	if distance%D == 0:
		return int(distance/D)
	else:
		return (int(distance/D) + 1)

print count_frog_jump_count(1,6,2)

# Your goal is to find that missing element.

# Write a function:

# class Solution { public int solution(int[] A); }

# that, given an array A, returns the value of the missing element.


def find_missing_number(A):
	A = set(A)
	if len(A) == 0:
		return 0
	s1 = 0
	s = sum(range(min(A), max(A)+1))

	if sum(A) < 0:
		return 1
	for num in A:
		s1 +=num

	if s - s1 == 0:
		return max(A)+1
	else:
		return s - s1


A = [1,2,3,4,5,6]

print find_missing_number(A)

# that, given a non-empty array A of N integers, returns the minimal difference that can be achieved.

def minimun_diff(A):
	l = len(A)
	i = 1

	suma = sum(A)
	min_diff = suma

	while i < l:
		j = 0
		suml = 0
		while j < i:
			suml +=A[j]
			j +=1
		sumr = abs(suma - suml)
		diff = abs(suml - sumr)
		print diff
		if diff < min_diff:
			min_diff = diff

		i +=1
	return min_diff

	print 'min diff : {}'.format(min_diff)

A = [3,1,2,4,3,4,5]
minimun_diff(A)

def minimun_diff(A):
	l = len(A)
	i = 0

	suma = sum(A)
	A.sort(reverse=True)
	min_diff = suma

	while i < l :
		j = 0
		suml = 0
		while j < i:
			suml +=A[j]
			j +=1
		sumr = abs(suma - suml)
		diff = abs(suml - sumr)
		print diff
		if diff < min_diff:
			min_diff = diff

		i +=1
	return min_diff

	print 'min diff : {}'.format(min_diff)

A = [3,1,2,4,3,4,5]
minimun_diff(A)


def distinct_values(A):
	A = set(A)
	return len(A)


# Your goal is to find the maximal product of any triplets
# that, given a non-empty array A, returns the value of the maximal product of any triplet.

def max_3_numbers(A):

	first = second = third = min(A)

	for num in A:
		if num > first:
			third = second
			second = first
			first = num
		elif num > second:
			third = second
			second = num
		elif num > third:
			third = num
	# print ('first : {} second : {} third : {}'.format(first, second, third))
	first1 = second1 = third1 = max(A)
	for num in A:
		if num < first1:
			third1 = second1
			second1 = first1
			first1 = num
		elif num < second1:
			third1 = second1
			second1 = num
		elif num < third1:
			third1 = num
	# print ('first1 : {} second1 : {} third1 : {}'.format(first1, second1, third1))

	if second1 < 0 and first > 0:
		if second1 * first1 > third * second:
			return first * second1 * first1
	return first * second * third

A = [-3,1,2,-2,5,6]
A = [-10,-2,-4]
A = [-5, 5, -5, 4]
A =  [-5, -6, -4, -7, -10]
print max_3_numbers(A)



def is_triangle_possilbe(A):

	if len(A) < 3:
		return 0

	A.sort()

	for i in range(len(A)-2):
		if A[i] + A[i+1] > A[i+2]:
			return 1

	return 0

A = [10,2,5,1,8,20]
A = [10,50,5,1]
print is_triangle_possilbe(A)

# Determine whether a given string of parentheses (multiple types) is properly nested.

def brackets_test(S):
	stack = []
	S = list(S)

	for char in S:
		if char in '{([':
			stack.append(char)
		else:
			if char in '}])':
				if len(stack) == 0:
					return 0
				y = stack.pop()

				if char == ')' and y != '(':
					return 0
				elif char == '}' and y != '{':
					return 0
				elif char == ']' and y != '[':
					return 0
	if len(stack) > 0:
		return 0
	return 1

S = "{[()()]}}"
# S = '{{{{{'

print brackets_test(S)


def living_fish(A,B):
	l = len(A)
	i = 0

	while i < len(A)-1:
		if B[i] > B[i+1] and A[i] > A[i+1]:
			B.pop(i+1)
			A.pop(i+1)
			print ("A : {} and B : {} and length : {}".format(A,B, len(A)))
		else:
			i +=1
	print ("A : {} and B : {} and length : {}".format(A,B, len(A)))

	return len(A)

A = [4,3,2,1,5]
B = [0,1,0,0,0]

living_fish(A,B)

# Find an index of an array such that its value occurs at more than half of indices in the array.
from collections import defaultdict
def denominator(A):
	d = defaultdict(list)

	l = len(A)

	# print ('value of len(A) : {}'.format(l))

	for index, num in enumerate(A):
		d[num].append(index)
	print d

	m = 0

	for key in d:
		if len((d[key])) > m:
			m = len((d[key]))
			res = d[key]

	# print ('value of l : {} and m : {}'.format(l,m))
	if m > int (l/2):
		return res
	else:
		return -1
A = [1,1,1,2,1,1,1,1,1,1,1,1,1,3,5,1,1,2,3,3,3,2]
print denominator(A)

# You would like to set a password for a bank account. However, there are three restrictions on the format of the password:



def longest_password(S):
	s = S.split()

	def ismyalnum(s1):
		if not s1.isalnum():
			return 0
		char_count = 0
		digit_count = 0
		s1 = list(s1)
		for char in s1:
			if char.isdigit():
				digit_count +=1
			elif char.isalpha():
				char_count +=1

		if digit_count % 2 == 1 and char_count %2 == 0:
			return digit_count + char_count
		else:
			return 0

	m = 0

	for s1 in s:
		count = ismyalnum(s1)
		if count != None:
			if count > m:
				m = count

	if m !=0:
		return m
	else:
		return -1

S = "test12345 5 a0A pass007 ?xy1"
print longest_password(S)
		

# find the bigger profit from the sequende of days. if no profit, return 0 else return maximum profit.

def max_profit1(A):
	m = 0
	for i in range(len(A)-1):
		for j in range(i+1, len(A)):
			if A[j] > A[i]:
				diff  = A[j] - A[i]
				if diff > m:
					m = diff

	return m

A = [23171,21011,21123,21366,21013,21367]

print max_profit1(A)

# find the maximun slice size from the Array A

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

A = [3,2]
A = [-2,-2]
A = [2]
print max_slice_sum(A)

import math
def find_cofactor(N):
	def is_prime(n):
		if n %2 == 0:
			return False
		elif n == 2:
			return 2
		elif n < 2:
			return 1
		else:
			for i in range(3, int(math.sqrt(n)) + 1, 2):
				if n % i == 0:
					return False
		return 2


	count = 0
	res = is_prime(N)

	if type(res) == int:
		return res
	else: 
		for i in range(1,N+1):
			if N%i == 0:
				count +=1

	return count
print find_cofactor(99)

import math
def find_cofactor(N):
	count = 0

	for i in range(1,N+1):
		if N%i == 0:
			count +=1

	return count
print find_cofactor(3)




def semiprimes(N, P, Q):
	def is_prime(n):
		if n < 2:
			return False
		elif n == 2:
			return True

		elif n %2 == 0:
			return False

		else:
			for i in range(3, int(math.sqrt(n))+1, 2):
				if n % i == 0:
					return False

		return True

	n = N
	semi_prime = list()
	prime = list()
	res = list()
	for i in range(n/2+1):
		if is_prime(i):
			prime.append(i)
	for i in range(len(prime)-1):
		# semi_prime.append(prime[i])
		for j in range(i, len(prime)):
			if prime[i] * prime[j] <=N:
				semi_prime.append(prime[i] * prime[j])
	print (prime)
	semi_prime.sort()
	print semi_prime

	l = len(P)

	for i in range(l):
		count = 0

		for num in range(P[i], Q[i]+1):
			if num in semi_prime:
				count +=1
		res.append(count)
	return res

N = 26 
P = [1,4,16] 
Q = [26,10,20]
print semiprimes(N, P, Q)

def non_divisor(A):
	l = len(A)
	i = 0
	res = []
	for i in range(len(A)):
		count = 0
		for j in range(i+1, len(A)):
			if A[i] % A[j] !=0:
				count +=1
		print ('count in j : {}'.format(count))
		for k in range(i):
			if A[i] % A[k] !=0:
				count +=1
		print ('count in k : {}'.format(count))
		res.append(count)
	# print res
	return res

A = [3,1,2,3,6]
non_divisor(A)

def common_prime_divisor(A, B):
	l = len(A)
	res = 0
	def is_prime(n):
		if n < 2:
			return False
		elif n == 2:
			return True

		elif n %2 == 0:
			return False

		else:
			for i in range(3, int(math.sqrt(n))+1, 2):
				if n % i == 0:
					return False

		return True

	for i in range(l):
		counter_A = []
		counter_B = []

		for j in range(1,A[i]):
			if is_prime(j):
				if A[i] % j == 0:
					counter_A.append(j)

		for j in range(1, B[i]):
			if is_prime(j):
				if B[i] % j == 0:
					counter_B.append(j)

		print ('counterA : {} and counterB : {}'.format(counter_A, counter_B))
		if len(counter_A) !=0 and len(counter_B) !=0:
			if counter_A == counter_B:
				res	+=1

	return res
A = [15,10,3]
B = [75,30,5]
print common_prime_divisor(A, B)

# Find the minimal absolute value of a sum of two elements.
def minimun_abs_sum_of_two(A):
	neg = False
	for num in A:
		if num < 0:
			neg = True

	if neg:
		pos_max = max(A)
		negative = []
		for num in A:
			if num <0:
				negative.append(num)
		#print negative

		neg_max = max(negative)
		# print ('pos : {} and neg : {}'.format(pos_max, neg_max))
		return abs(pos_max + neg_max)
	else:
		first = second = max(A)
		for num in A:
			if first > num:
				second = first
				first = num
			elif second > num:
				second = num

		return first + first


A = [1, 4, -3]
A = [0]
A = [8, 5, 3, 4, 6, 8]

print minimun_abs_sum_of_two(A)

def absdistinct(A):
	B = []
	for num in A:
		if num < 0:
			B.append(abs(num))
		else:
			B.append(num)

	return len(set(B))

A = [-5,-3,-1,0,3,6]

print absdistinct(A)

def non_overlaping_segment(A, B):
	l = len(A)
	i = 0
	overlap = []
	non_overlap = []
	while i < l-1:
		if B[i] > A[i+1]:
			overlap.append(i)
			overlap.append(i+1)
		else:
			non_overlap.append(i+1)
		i +=1
	# print ('overlap : {}'.format(overlap))
	# print ('non overlap : {}'.format(non_overlap))

	if len(non_overlap) < 2:
		return 0

	non_overlap_sets  = 0
	for i in range(len(non_overlap)-1):
		for j in range(i+1, len(non_overlap)):
			non_overlap_sets +=1

	# print ('non_overlap_sets : {}'.format(non_overlap_sets))
	# print ('total : {}'.format(non_overlap_sets * len(overlap)))
	return non_overlap_sets * len(overlap)
A = [1,3,7,9,9]
B = [5,6,8,9,10]
non_overlaping_segment(A, B)

def tie_ropes(K, A):
	res = 0
	counter = 0
	while len(A) > 0:
		m = max(A)

		if K < m:
			res +=1
			A.remove(m)
			print ('m1 : {}'.format(m))
		else:
			print ('m2 : {}'.format(m))
			A.remove(m)
			diff = K + 1 - m
			if diff in A:
				print ('diff1 : {}'.format(diff))
				A.remove(diff)
				res +=1
			else:
				print ('hi A : {}'.format(A))
				for num in A:
					if diff >= num:
						A.remove(num)
						print ('num : {}'.format(num))
						diff = diff - num
						print ('diff : {}'.format(diff))
						print ('A : {}'.format(A))
						if diff == 0:
							res +=1
		counter +=1
		print A
		print ('res : {}'.format(res))
		print ('counter : {}'.format(counter))
	# return res

A = [1,2,3,4,1,1,3]
print tie_ropes(4,A)


#You have 100 doors in a row that are all initially closed. you make 100 passes by the doors starting with the 
#first door every time. the first time through you visit every door and toggle the door (if the door is closed, 
#you open it, if its open, you close it). the second time you only visit every 2nd door (door #2, #4, #6). the 
#third time, every 3rd door (door #3, #6, #9), ec, until you only visit the 100th door.

def divisor_cal(n):
	d = defaultdict(list)

	for i in range(1, n+1):
		for j in range(1, i+1):
			if i %j ==0:
				d[i].append(j)

	print d

divisor_cal(100)


# convert word numbers to digits number
# seventy one hundread ninteen -> 7119

def conversion(s):
	numbers = {"one":1, "two":2, "three":3, "four":4, "five":5,
				"six":6, "seven":7, "eight":8, "nine": 9, "ten": 10,
				"eleven":11, "twelve": 12, "thirteen": 13, "fourteen": 14,
				"fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "ninteen": 19,
				"twenty": 20, "thirty": 30, "fourty": 40, "fifty": 50, "sixty": 60,
				"seventy": 70, "eighty": 80, "ninety": 90}

	multiplier = {"hundred": 100, "thousand": 1000, "milion": 1000000}
	print ('number string : {}'.format(s))
	s = s.split()
	i = 0
	l = len(s)
	m = 0
	res = 0	
	d = 0
	k = 0
	while i < l:
		if s[i] in numbers:
			d += numbers[s[i].strip().lower()]
			res +=d
			print d
		elif s[i] in multiplier:
			m = multiplier[s[i].strip().lower()]
			k = d * m 
			res += k
			d = 0
		i +=1
	print res

s = "seventy one hundred ninteen"
# s = "eleven thousand   nine hundred one" # 11000 + 6900 + 1
conversion(s)

