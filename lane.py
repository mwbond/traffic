# Matthew Bond
# Mar 25, 2010
# lane.py

from collections import deque
import car

class Lane:
	# Lane_becomes is the lane that self turn into.
	# It equals 0 if the lane ends.
	# It equals None if the lane dissapears into the ether.
	def __init__(self, length, lane_becomes=None):
		self.length = length
		self._car_queue = deque([])
		self._lane_becomes = lane_becomes
	
	def add_car(self, car):
		self._car_queue.appendleft(car)

	def get_info_ahead(self, is_cur_lane=False):
		if (len(self._car_queue) != 0) and (not is_cur_lane):
			lead = self._car_queue[0]
			return (lead.offset, lead.vel, lead.length)
		elif self._lane_becomes == None:
			return (None, 0, 0)
		elif self._lane_becomes == 0:
			return (self.length, 0, 0)
		else:
			info = self._lane_becomes.get_info_ahead()
			if info[0] == None:
				return (None, info[1], info[2])
			else:
				return (self.length + info[0], info[1], info[2]) 

	# Updates the lane.
	def update_lane(self):
		num_cars = len(self._car_queue)
		if num_cars == 0:
			return
		for index in range(num_cars - 1):
			follow = self._car_queue[index]
			lead = self._car_queue[index + 1]
			follow.update_car(lead.offset, lead.vel, lead.length)
		lead_info = self.get_info_ahead(True)
		self._car_queue[-1].update_car(lead_info[0], lead_info[1], lead_info[2])

	def check_offsets(self):
		count = 0
		for car in reversed(self._car_queue):
			if car.offset > self.length:
				count = count + 1
			else:
				break
		for foo in range(count):
			car = self._car_queue.pop()
			if self._lane_becomes != None:
				car.offset = car.offset - self.length
				self._lane_becomes.add_car(car)
			del car

	# Print out all of the car's id, offset, and vel
	def print_lane(self):
		for car in reversed(self._car_queue):
			print "\tCar", car.id
			print "Pos", car.offset, "m"
			print "Speed", car.vel, "m/s"
