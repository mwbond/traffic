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

	def get_info_ahead(self, is_cur_lane=False):
		if (len(self.car_queue) != 0) and (not is_cur_lane):
			lead = self.car_queue[0]
			return (lead.offset, lead.vel, lead.length)
		elif self.nlane == None:
			return (None, 0, 0)
		elif self.nlane == 0:
			return (self.length, 0, 0)
		else:
			info = self.nlane.get_info_ahead()
			if info[0] == None:
				return (None, info[1], info[2])
			else:
				return (self.length + info[0], info[1], info[2]) 

	# Updates the lane.
	def update_lane(self):
		num_cars = len(self.car_queue)
		if num_cars == 0:
			return
		for index in range(num_cars - 1):
			follow = self.car_queue[index]
			lead = self.car_queue[index + 1]
			follow.update_car(lead.offset, lead.vel, lead.length)
		lead_info = self.get_info_ahead(True)
		self.car_queue[-1].update_car(*lead_info)

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
