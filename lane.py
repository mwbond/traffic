# Matthew Bond
# Mar 25, 2010
# lane.py

from collections import deque
import copy
import car

class Lane:
	# Lane_becomes is the lane that self turn into.
	# It equals 0 if the lane ends.
	# It equals None if the lane dissapears into the ether.
	def __init__(self, length, n_lane=None, s_lane=None, e_lane=None, w_lane=None):
		self.length = length
		self.car_queue = deque([])
		self.refrence_queue = deque([])
		self.n_lane = n_lane
		self.s_lane = s_lane
		self.e_lane = e_lane
		self.w_lane = w_lane

	def add_car(self, car):
		if car.offset >= self.length:
			if self.n_lane != None:
				car.offset = car.offset - self.length
				self.n_lane.add_car(car)
		else:
			self.car_queue.appendleft(car)

	def get_info_ahead(self, offset):
		for car in self.refrence_queue:
			if car.offset > offset:
				return [car.offset - car.length - offset, car.vel]
		if self.n_lane is None:
			return [None, 0]
		if self.n_lane == 0:
			return [self.length - offset, 0]
		dist, vel = self.n_lane.get_info_ahead(-1)
		if dist is not None:
			if offset == -1:
				offset = 0
			dist = dist + self.length
		return [dist, vel]

	def get_info_behind(self, offset):
		for car in reversed(self.refrence_queue):
			if car.offset <= offset:
				return [offset - car.offset, car]
		if self.n_lane is None:
			return [None, 0]
		dist, car = self.s_lane.get_info_behind(self.s_lane.length)
		if dist is not None:
			dist = dist + offset
		return [dist, car]

	# Updates the lane.
	def update_lane(self):
		for car in self.car_queue:
			ninfo = self.get_info_ahead(car.offset)
			if self.e_lane is None:
				e_info = None
			else:
				e_info = (self.e_lane.get_info_ahead(car.offset) +
						self.e_lane.get_info_behind(car.offset - car.length))
			if self.w_lane is None:
				w_info = None
			else:
				w_info = (self.w_lane.get_info_ahead(car.offset) +
						self.w_lane.get_info_behind(car.offset - car.length))
			car.update_car(ninfo, e_info, w_info)

	def check_offsets(self):
		count = 0
		for car in reversed(self.car_queue):
			if car.offset >= self.length:
				count = count + 1
			else:
				break
		for foo in range(count):
			car = self.car_queue.pop()
			if self.n_lane != None:
				car.offset = car.offset - self.length
				self.n_lane.add_car(car)

	def print_lane(self):
		"""Print out all of the car's id, offset, and vel"""
		print "        --LANE--"
		for car in reversed(self.car_queue):
			print "\tCar", car.id
			print "Pos", car.offset, "m"
			print "Speed", car.vel, "m/s"

		self.refrence_queue = copy.copy(self.car_queue)
