import os
base = os.path.dirname(os.path.realpath(__file__)) + '/'

class jp():

	def save(self, data):
		self.file = open(base + "data.txt","w") 
		self.file.write(data)
		self.file.close()

	def read(self):
		self.file = open(base + "data.txt","r")
		self.data = self.file.read()
		return self.data

