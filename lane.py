# Matthew Bond
# Mar 25, 2010
# lane.py

from collections import deque
import car

class Lane:
	# Lane_becomes is the lane that self turn into.
	# It equals 0 if the lane ends.
	# It equals None if the lane dissapears into the ether.
	def __init__(self, length, time):
		self.length = length
		self.car_queue = deque([])
		self.time = time

	def add_car(self, car):
		self.car_queue.appendleft(car)

	def get_info_ahead(self, offset=0):
		pass
		'''if (len(self.car_queue) != 0) and (not is_cur_lane):
			lead = self.car_queue[0]
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
				return (self.length + info[0], info[1], info[2]) '''

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
		self.time += 1

	def check_offsets(self, id):
		cars = []
		count = 0
		num_cars = len(self.car_queue)
		for index in reversed(range(num_cars)):
			if self.car_queue[index].offset < self.length:
				break
			elif self.car_queue[index].stream_id == id:
				cars.append(self.car_queue[index])
				self.car_queue.remove(index)
		return cars

	def print_lane(self):
		"""Print out all of the car's id, offset, and vel"""
		for car in reversed(self.car_queue):
			print "\tCar", car.id
			print "Pos", car.offset, "m"
			print "Speed", car.vel, "m/s"
