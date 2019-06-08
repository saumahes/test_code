def f(n):
	for i in range(n):
		yield i**3

print f(5)

def reverse1(a):
	print ('original string : {}'.format(a))
	a = list(a)
	l = len(a)
	i = 0
	while (i<l):
		a[i], a[l-1] = a[l-1], a[i]
		i +=1
		l -=1

	print ('reverse of given string is : {}'.format(''.join(a)))

reverse1('Saurabh')


def calculate_upper_case_lower_case(a):
	print ('original string : {}'.format(a))
	a = list(a)
	upper_count = 0
	lower_count = 0
	for char in a:
		if char.isupper():
			upper_count +=1
		elif char.islower():
			lower_count +=1
		else:
			pass

	print ('Total upper count in a given string : {}'.format(upper_count))
	print ('Total lower count in a given string : {}'.format(lower_count))

calculate_upper_case_lower_case('Tutorials POINT123456')

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

add1(100,-30)

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
