import heapq,random,time,copy

class Median():


	def __init__(self, records):
		"""Initialization of variables required for algorithm"""
		
		self.data = {}
		#The two heaps that calculate the median
		self.minheap = []
		self.maxheap = []
		#Helper variables to determine which heap is bigger in size
		self.biggerHeap =  []
		self.smallerHeap = []
		
		self.records = records
		self.changedRecords = [0 for x in range (100)]
		self.size = len(self.records)

		self.medians = [0 for x in range(self.size+100)]
		self.flag = 0 #flag==0 if minheap is bigger, 1 if smaller
		self.runningMedian = 0
		self.runningCount = 0 #Helper variable for itterating the medians array

	

	def solution(self):
		"""Solution algorithm skeleton:

		>Records array is itterated over for a record to be chosen.
		>Current value of record (before any changes occur) is stored in variable prev.
		>In case of reoccurance, old value in data is replaced by new temperature value for a given (x,y) tuple.
		>Record is then added to the appropriate heap.
		>Heaps are checked for imbalances in size.
		>Running median is calculated and stored in a medians array.
		>Medians array is returned.
		"""
		for i in range (self.size):
			record = self.records[i]

			prev = self.data.get((record.x,record.y),None)
			if prev:
				prev.heap.remove(prev)
				self.runningMedian = self.getMedian()
			self.data.update({(record.x,record.y):record})

			self.addRecord(record)
			self.rebalance()
			self.runningMedian = self.getMedian()
			self.medians[self.runningCount] = self.runningMedian
			self.runningCount += 1
		
		return self.medians


	def tempChanges(self):
		"""Changes to the first 100 temperatures and new medians"""

		print("\nChanges in 100 first temperatures")
		self.changedRecords = copy.copy(self.records)
		for i in range (100):
			newrecord = self.changedRecords[i]
			#Changing the temperature value
			newrecord.t = round(random.uniform(-50,50),2)

			prev = self.data.get((newrecord.x,newrecord.y),None)
			if prev:
				prev.heap.remove(prev)
				self.runningMedian = self.getMedian()
			self.data.update({(newrecord.x,newrecord.y):newrecord})

			self.addRecord(newrecord)
			self.rebalance()
			self.runningMedian = self.getMedian()
			self.medians[self.runningCount] = self.runningMedian
			self.runningCount += 1
			
			#Only the last 100 changes
			print("{0},{1} --> {2:.2f}".format((newrecord.x,newrecord.y),newrecord.t, self.runningMedian))

		return self.medians


	def addRecord(self, record):
		"""Puts record in appropriate heap depending on the value."""
		if 	record.t > self.runningMedian:
			heapq.heappush(self.minheap, record)
			record.setHeap(self.minheap)
			
		else:
			#Python's heapq only implements a minheap DS. We can invert the numbers and add them into a minheap, 
			#thus giving us a maxheap DS, essentially changing the sign of the inequality.
			#This little mathematical trick saves us the trouble of actually writting two different data structures for the heaps.
			record.t *= -1
			heapq.heappush(self.maxheap, record)
			record.setHeap(self.maxheap)
			

	def rebalance(self):
		"""Checks for imbalances in two heaps and keeps the difference in size <= 1"""
		
		sh = len(self.minheap)
		sl = len(self.maxheap)

		self.biggerHeap = self.maxheap
		self.smallerHeap = self.minheap
		self.flag = 1

		if sh > sl:
			self.biggerHeap = self.minheap
			self.smallerHeap = self.maxheap
			self.flag = 0

		if abs(sh - sl) >= 2:
			temp = self.biggerHeap[0]
			temp.t *= -1
			heapq.heappush(self.smallerHeap, temp)
			temp.setHeap(self.smallerHeap)
			self.biggerHeap.remove(temp)


	def getMedian(self):
		"""Calculates running median of two heaps"""

		#Edge case
		if len(self.maxheap) == 0 and len(self.minheap) == 0:	
			return 0
		
		#Heaps are balanced
		elif len(self.biggerHeap) == len(self.smallerHeap):
			return (self.minheap[0].t - self.maxheap[0].t) / 2
		
		#Heaps are unbalanced and flag gives us the appropriate heap to return from
		elif self.flag == 0:
			return self.biggerHeap[0].t
		else:
			return -self.biggerHeap[0].t
			

class Record():
	"""Utility class for storing and processing space and temperature data. 
	Magic methods are used for representation of data, as well as comparisons between the class' temperature value."""

	def __init__(self):
		self.x = random.randint(0,50)
		self.y = random.randint(0,50)
		self.t = round(random.uniform(-50,50),2)
		self.heap = None

	def __repr__(self):
		return f"({self.x},{self.y}),{self.t}"

	def __lt__(self, other):
		return self.t < other.t

	def __gt__(self, other):
		return self.t > other.t

	def setHeap(self, heap):
		self.heap = heap


def main():
	"""Driver code for random number generator, time calculations and records initialization."""
	random.seed(1)
	records = [Record() for _ in range(50000)]

	#Ερώτημα 1	
	t1 = time.time()
	s = Median(records).solution()
	t2 = time.time()
	print("\n\nData\n\n")
	for r,m in zip(records,s):
		#(x,y),t --> median
		print("{!r} --> {:.2f}".format(r,m))
	print("Time elapsed: {} seconds".format(t2-t1))

	#Ερώτημα 2
	print("\n\n\n\n\n")
	t1 = time.time()
	p = Median(records).tempChanges()
	t2 = time.time()
	print("Time elapsed: {} seconds".format(t2-t1))

if __name__ == "__main__":
	main()
