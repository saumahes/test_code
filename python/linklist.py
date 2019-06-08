class Node(object):
	def __init__(self,data):
		self.data = data
		self.next = None


class LinkedList(object):
	def __init__(self):
		self.head = None

	def add(self, data):
		temp = Node(data)
		temp.next = self.head
		self.head = temp

	def add_at_end(self, data):
		temp = Node(data)

		current = self.head
		if self.head == None:
			self.head = temp
			return

		while current.next !=None:
			current = current.next
		current.next = temp

	def display(self):
		current = self.head
		if self.head == None:
			print ('Link list is empty')
			return

		while current != None:
			print current.data
			current = current.next

	def remove(self, data):
		current = self.head
		found = False
		if self.head == None:
			print ('link list is empty')
			return

		elif current.data == data:
			self.head = current.next
			return
		else:
			while current.next !=None and not found:
				previous = current
				current = current.next
				if current.data == data:
					previous.next = current.next
					found = True
					return
		if not found:
			print ('data is not present in the list')

l1 = LinkedList()
l1.display()
l1.add_at_end(1)
l1.add_at_end(2)
l1.add_at_end(3)
l1.add_at_end(4)
l1.add_at_end(5)
l1.display()

l1.remove(2)
l1.display()
