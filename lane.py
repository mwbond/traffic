# Matthew Bond
# Mar 25, 2010
# lane.py

import copy
import car

class Lane:
	# Lane_becomes is the lane that self turn into.
	# It equals 0 if the lane ends.
	# It equals None if the lane dissapears into the ether.
	def __init__(self, length, n_lane=None, s_lane=None, e_lane=None,
					w_lane=None):
		self.length = length
		self.car_queue = []
		self.refrence_queue = []
		self.n_lane = n_lane
		self.s_lane = s_lane
		self.e_lane = e_lane
		self.w_lane = w_lane
		self.index = -1

	# Returns the offset of the car indicated by self.index
	# Returns None if index is invalid
	def get_index_offset(self):
		if self.index < 0:
			return None
		else:
			return self.refrence_queue[self.index].offset

	# Removes the car from self.refrence_queue
	def refrence_remove(self, car_id):
		for index in range(len(self.refrence_queue)):
			if self.refrence_queue[index].id == car_id:
				self.refrence_queue.pop(index)
				break

	# Inserts given the car into self.car_queue based on offset
	# If ref is True, it also inserts the given car into self.refrence_queue
	def add_car(self, car, ref=False, ref_car=None):
		if car.offset >= self.length:
			if self.n_lane != None:
				car.offset = car.offset - self.length
				self.n_lane.add_car(car, ref)
		else:
			foo = -1
			for index in range(len(self.car_queue)):
				if self.car_queue[index].offset < car.offset:
					foo = index
			self.car_queue.insert(foo + 1, car)

			if ref:
				assert ref_car is not None
				foo = -1
				for index in range(len(self.refrence_queue)):
					if self.refrence_queue[index].offset < car.offset:
						foo = index
				self.refrence_queue.insert(foo + 1, ref_car)

	# Returns the distance from the front of car A to the back of car B and
	# the velocity of car B where car B is the car immediately in front of
	# car A in this lane
	def get_info_ahead(self, offset):
		for car in self.refrence_queue:
			if car.offset > offset:
				offset = max(offset, 0)
				return [car.offset - car.length - offset, car.vel]
		if self.n_lane is None:
			return [None, 0]
		if self.n_lane == 0:
			offset = max(offset, 0)
			return [self.length - offset, 0]
		dist, vel = self.n_lane.get_info_ahead(-1)
		dist = dist and dist + self.length
		return [dist, vel]

	# Returns the distance from the front of car A to the front of car B and
	# car B itself where car B is the car immediately behind car A in this lane
	def get_info_behind(self, offset):
		for car in reversed(self.refrence_queue):
			if car.offset <= offset:
				return [offset - car.offset, car]
		if self.n_lane is None:
			return [None, None]
		dist, car = self.s_lane.get_info_behind(self.s_lane.length)
		if dist is not None:
			dist = dist + offset
		return [dist, car]

	# Updates the car in self.car_queue indicated by self.index
	def update_lane(self):
		car = self.car_queue[self.index]
		n_info = self.get_info_ahead(car.offset)
		if self.e_lane is None:
			e_info = None
		else:
			e_info = (self.e_lane.get_info_ahead(car.offset) +
					self.e_lane.get_info_behind(car.offset))
		if self.w_lane is None:
			w_info = None
		else:
			w_info = (self.w_lane.get_info_ahead(car.offset) +
					self.w_lane.get_info_behind(car.offset))
		dir, vel = car.update_car(n_info, e_info, w_info)
		if dir == 1:
			target_lane = self.e_lane
		elif dir == -1:
			target_lane = self.w_lane
		else:
			target_lane = self
		ref_car = copy.deepcopy(car)
		car.vel = vel
		car.offset = car.offset + car.vel * car.prt
		if target_lane is not self:
			target_lane.add_car(car, True, ref_car)
			self.refrence_remove(car.id)
			self.car_queue.remove(car)
		self.index = self.index - 1

	# Moves cars to the next lane if their offsets are longer than the
	# length of the lane
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

	# Prints out relevent info for the lane; also last two lines do important
	# stuff every cycle
	def print_lane(self):
		"""Print out all of the car's id, offset, and vel"""
		print "        --LANE--"
		for car in reversed(self.car_queue):
			print "\tCar", car.id
			print "Pos", car.offset, "m"
			print "Speed", car.vel, "m/s"

		self.refrence_queue = copy.deepcopy(self.car_queue)
		self.index = len(self.refrence_queue) - 1
