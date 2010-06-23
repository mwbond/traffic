# Matthew Bond
# Mar 25, 2010
# lane.py

from collections import deque
import car

class Lane:
	# Lane_becomes is the lane that self turn into.
	# It equals 0 if the lane ends.
	# It equals None if the lane dissapears into the ether.
	def __init__(self, length):
		self.length = length
		self.car_queue = deque([])
		self.refrence_queue = deque([])
		self.stop_at_end= False

	def add_car(self, car):
		if len(self.car_queue):
			assert self.car_queue[0].offset > self.car_queue[0].length
		self.car_queue.appendleft(car)
		self.refrence_queue.appendleft(car)

	def get_unbounded(self):
		unbounded = {}
		num_cars = len(self.car_queue)
		for index in reversed(range(num_cars)):
			if self.car_queue[index].offset >= self.length:
				car = self.car_queue.pop()
				if car.stream_id not in unbounded:
					unbounded[car.stream_id] = [car]
				else:
					unbounded[car.stream_id].append(car)
			else:
				break
		return unbounded

	def print_lane(self):
		"""Print out all of the car's id, offset, and vel"""
		for car in reversed(self.refrence_queue):
			print "Pos", car.offset, "m"
			print "Speed", car.vel, "m/s"
