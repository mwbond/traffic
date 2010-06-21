# Matthew Bond
# Mar 25, 2010
# lane.py

from collections import deque
import car

class Lane:
	# Lane_becomes is the lane that self turn into.
	# It equals 0 if the lane ends.
	# It equals None if the lane dissapears into the ether.
	def __init__(self, length, time=0):
		self.length = length
		self.car_queue = deque([])
		self.queue_refrence = deque([])
		self.time = time

	def add_car(self, car):
		self.car_queue.appendleft(car)

	def commit_queue(self):
		self.queue_refrence = self.car_queue[:]

	# Updates the lane.
	def update_lane(self):
		num_cars = len(self.car_queue)
		if num_cars == 0:
			return None
		for index in range(num_cars - 1):
			follow = self.car_queue[index]
			lead = self.car_queue[index + 1]
			gap_length = lead.offset - lead.length - follow.offset
			follow.update_car(gap_length, lead.vel)
		return self.car_queue[num_cars - 1]


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
		for car in reversed(self.car_queue):
			print "Pos", car.offset, "m"
			print "Speed", car.vel, "m/s"
