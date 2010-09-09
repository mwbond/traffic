# Matthew Bond
# Mar 25, 2010
# lane.py

from collections import deque
import car

class Lane:
	# Lane_becomes is the lane that self turn into.
	# It equals 0 if the lane ends.
	# It equals None if the lane dissapears into the ether.
	def __init__(self, length, nlane=None, slane=None, elane=None, wlane=None):
		self.length = length
		self.car_queue = deque([])
		self.refrence_queue = deque([])
		self.nlane = nlane
		self.slane = slane
		self.elane = elane
		self.wlane = wlane

	def add_car(self, car):
		if car.offset >= self.length:
			if self.nlane != None:
				car.offset = car.offset - self.length
				self.nlane.add_car(car)
		else:
			self.car_queue.appendleft(car)

	def get_info_ahead(self, offset):
		ahead = [None, 0]
		for car in self.refrence_queue:
			if car.offset > offset:
				return [car.offset - car.length - offset, car.vel]
		if self.nlane is None:
			return [None, 0]
		if self.nlane == 0:
			return [self.length - offset, 0]
		dist, vel = self.nlane.get_info_ahead(-1)
		if dist is not None:
			if offset == -1:
				offset = 0
			dist = dist + self.length
		return [dist, vel]

	def get_info_behind(self, offset):
		behind = [None, 0]
		for car in reversed(self.refrence_queue):
			if car.offset <= offset:
				return [offset - car.offset, car]
		if self.nlane is None:
			return None
		dist, car = self.slane.get_info_behind(self.slane.length)
		if dist is not None:
			dist = dist + offset
		return [dist, car]

	# Updates the lane.
	def update_lane(self):
		for car in self.car_queue:
			ninfo = self.get_info_ahead(car.offset)
			if self.elane is None:
				einfo = None
			else:
				einfo = (self.elane.get_info_ahead(car.offset) +
						self.elane.get_info_behind(car.offset - car.length))
			if self.wlane is None:
				winfo = None
			else:
				winfo = (self.wlane.get_info_ahead(car.offset) +
						self.wlane.get_info_behind(car.offset - car.length))
			car.update_car(ninfo, einfo, winfo)

	def check_offsets(self):
		count = 0
		for car in reversed(self.car_queue):
			if car.offset >= self.length:
				count = count + 1
			else:
				break
		for foo in range(count):
			car = self.car_queue.pop()
			if self.nlane != None:
				car.offset = car.offset - self.length
				self.nlane.add_car(car)

	def print_lane(self):
		"""Print out all of the car's id, offset, and vel"""
		print "        --LANE--"
		for car in reversed(self.car_queue):
			print "\tCar", car.id
			print "Pos", car.offset, "m"
			print "Speed", car.vel, "m/s"
