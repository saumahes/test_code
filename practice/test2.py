def match():
	d = dict()
	d['name'] = 'Saurabh'
	d['age'] = 35
	d['last_name'] = 'Maheshwari'
	d['job'] = 'Rambus'
	d['address'] = 'Milpitas'

	print ('Name    | last Name    | Age  |  Address')
	res = ''
	for i in d:
		if i == 'name':
			res +=d[i] + ' |'
			break

	for i in d:
		if i == 'last_name':
			res +=d[i] + ' |'
			break

	for i in d:
		if i == 'age':
			res +=str(d[i]) + ' |'
			break

	for i in d:
		if i == 'address':
			res +=d[i] + ' |'
			break


	print (res),

match()