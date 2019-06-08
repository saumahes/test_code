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

b1 = Bank_Account('saurabh')
b1.deposit()
# b1.deposit()
b1.display()
b1.withdraw()
b1.display()

b2 = Bank_Account('Aaryan')
b2.deposit()
b2.display()
b2.withdraw()
b2.display()
